"""
WSFEv1 — issue a Factura B end-to-end.
Usage:
    python wsfev1_factura.py --ta ta-wsfe.xml --cuit 20111111112 --pto-vta 1 --neto 100.00
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from xml.etree import ElementTree as ET

from zeep import Client

WSFEV1_HOMO = "https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL"
WSFEV1_PROD = "https://servicios1.afip.gov.ar/wsfev1/service.asmx?WSDL"

CBTE_FACTURA_B = 6
ALICUOTA_21 = 5  # AFIP Iva.Id


def load_ta(path: Path) -> tuple[str, str]:
    root = ET.fromstring(path.read_bytes())
    creds = root.find("credentials")
    if creds is None:
        raise ValueError(f"{path}: not a TA — missing <credentials>")
    return creds.findtext("token", ""), creds.findtext("sign", "")


def round2(x: Decimal) -> Decimal:
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--ta", type=Path, required=True, help="TA xml from WSAA")
    p.add_argument("--cuit", required=True, help="CUIT emisor (sin guiones)")
    p.add_argument("--pto-vta", type=int, required=True)
    p.add_argument("--neto", type=Decimal, required=True, help="ImpNeto in pesos")
    p.add_argument("--env", choices=["homo", "prod"], default="homo")
    args = p.parse_args()

    token, sign = load_ta(args.ta)
    auth = {"Token": token, "Sign": sign, "Cuit": args.cuit}

    wsdl = WSFEV1_HOMO if args.env == "homo" else WSFEV1_PROD
    client = Client(wsdl=wsdl)

    last = client.service.FECompUltimoAutorizado(
        Auth=auth, PtoVta=args.pto_vta, CbteTipo=CBTE_FACTURA_B
    )
    next_nro = int(last.CbteNro) + 1

    neto = round2(args.neto)
    iva = round2(neto * Decimal("0.21"))
    total = neto + iva

    fecha = datetime.now().strftime("%Y%m%d")

    req = {
        "FeCabReq": {"CantReg": 1, "PtoVta": args.pto_vta, "CbteTipo": CBTE_FACTURA_B},
        "FeDetReq": {"FECAEDetRequest": [{
            "Concepto": 1,
            "DocTipo": 99,
            "DocNro": 0,
            "CbteDesde": next_nro,
            "CbteHasta": next_nro,
            "CbteFch": fecha,
            "ImpTotal": float(total),
            "ImpTotConc": 0,
            "ImpNeto": float(neto),
            "ImpOpEx": 0,
            "ImpIVA": float(iva),
            "ImpTrib": 0,
            "MonId": "PES",
            "MonCotiz": 1,
            "Iva": {"AlicIva": [{"Id": ALICUOTA_21, "BaseImp": float(neto), "Importe": float(iva)}]},
        }]},
    }

    resp = client.service.FECAESolicitar(Auth=auth, FeCAEReq=req)
    if resp.FeCabResp.Resultado != "A":
        print(f"REJECTED: {resp.FeCabResp.Resultado}", file=sys.stderr)
        for d in resp.FeDetResp.FECAEDetResponse or []:
            for o in (d.Observaciones.Obs if d.Observaciones else []) or []:
                print(f"  Obs {o.Code}: {o.Msg}", file=sys.stderr)
        return 1

    det = resp.FeDetResp.FECAEDetResponse[0]
    print(f"CAE:        {det.CAE}")
    print(f"CAEFchVto:  {det.CAEFchVto}")
    print(f"CbteNro:    {det.CbteDesde}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
