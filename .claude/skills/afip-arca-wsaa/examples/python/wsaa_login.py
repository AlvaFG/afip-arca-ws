"""
WSAA login — get a TA for a given service (homologación by default).

Usage:
    python wsaa_login.py --cert path/to/cert.crt --key path/to/private.key --service wsfe

Outputs the TA XML to stdout. Save to a file and cache it until <expirationTime>.
"""
from __future__ import annotations

import argparse
import base64
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import pkcs7
from zeep import Client

WSAA_HOMO = "https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl"
WSAA_PROD = "https://wsaa.afip.gov.ar/ws/services/LoginCms?wsdl"

ART = timezone(timedelta(hours=-3))


def build_tra(service: str) -> bytes:
    now = datetime.now(ART)
    tra = f"""<?xml version="1.0" encoding="UTF-8"?>
<loginTicketRequest version="1.0">
  <header>
    <uniqueId>{int(now.timestamp())}</uniqueId>
    <generationTime>{(now - timedelta(minutes=1)).isoformat(timespec='seconds')}</generationTime>
    <expirationTime>{(now + timedelta(minutes=10)).isoformat(timespec='seconds')}</expirationTime>
  </header>
  <service>{service}</service>
</loginTicketRequest>
"""
    return tra.encode("utf-8")


def sign_cms(tra_bytes: bytes, cert_path: Path, key_path: Path) -> bytes:
    cert = x509.load_pem_x509_certificate(cert_path.read_bytes())
    key = serialization.load_pem_private_key(key_path.read_bytes(), password=None)
    cms = (
        pkcs7.PKCS7SignatureBuilder()
        .set_data(tra_bytes)
        .add_signer(cert, key, hashes.SHA256())
        .sign(serialization.Encoding.DER, [pkcs7.PKCS7Options.Binary])
    )
    return cms


def login(cms_b64: str, env: str) -> str:
    wsdl = WSAA_HOMO if env == "homo" else WSAA_PROD
    client = Client(wsdl=wsdl)
    return client.service.loginCms(in0=cms_b64)


def main() -> int:
    p = argparse.ArgumentParser(description="WSAA login — obtain a TA")
    p.add_argument("--cert", type=Path, required=True)
    p.add_argument("--key", type=Path, required=True)
    p.add_argument("--service", default="wsfe", help="WS scope: wsfe, wsfex, ws_sr_padron_a4, ...")
    p.add_argument("--env", choices=["homo", "prod"], default="homo")
    args = p.parse_args()

    tra = build_tra(args.service)
    cms = sign_cms(tra, args.cert, args.key)
    cms_b64 = base64.b64encode(cms).decode("ascii")
    ta_xml = login(cms_b64, args.env)
    print(ta_xml)
    return 0


if __name__ == "__main__":
    sys.exit(main())
