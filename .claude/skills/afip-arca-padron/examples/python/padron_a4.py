"""
Padrón A4 — lookup a CUIT.
Usage: python padron_a4.py --ta ta-padron.xml --cuit-rep 20111111112 --cuit 30500001735
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

from zeep import Client

HOMO = "https://awshomo.afip.gov.ar/sr-padron/webservices/personaServiceA4?WSDL"
PROD = "https://aws.afip.gov.ar/sr-padron/webservices/personaServiceA4?WSDL"


def load_ta(path: Path) -> tuple[str, str]:
    root = ET.fromstring(path.read_bytes())
    creds = root.find("credentials")
    if creds is None:
        raise ValueError(f"{path}: not a TA")
    return creds.findtext("token", ""), creds.findtext("sign", "")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--ta", type=Path, required=True)
    p.add_argument("--cuit-rep", required=True, help="CUIT que ejecuta la consulta")
    p.add_argument("--cuit", required=True, help="CUIT a consultar")
    p.add_argument("--env", choices=["homo", "prod"], default="homo")
    args = p.parse_args()

    token, sign = load_ta(args.ta)
    client = Client(wsdl=HOMO if args.env == "homo" else PROD)

    resp = client.service.getPersona(
        token=token, sign=sign,
        cuitRepresentada=int(args.cuit_rep), idPersona=int(args.cuit),
    )
    if resp.errorReturn and resp.errorReturn.error:
        for e in resp.errorReturn.error:
            print(f"ERROR {e.code}: {e.descripcion}", file=sys.stderr)
        return 1
    persona = resp.personaReturn.persona
    nombre = persona.razonSocial or f"{persona.nombre or ''} {persona.apellido or ''}".strip()
    print(f"Nombre/Razón social: {nombre}")
    print(f"Tipo persona:        {persona.tipoPersona}")
    print(f"Estado clave:        {persona.estadoClave}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
