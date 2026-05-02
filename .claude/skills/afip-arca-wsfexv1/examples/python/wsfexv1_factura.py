"""
WSFEXv1 — issue a Factura E (export) to a US buyer in USD.
Usage:
    python wsfexv1_factura.py --ta ta-wsfex.xml --cuit 20111111112 --pto-vta 5 --total 1000.00 --cotiz 950.00
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET

from zeep import Client

HOMO = "https://wswhomo.afip.gov.ar/wsfexv1/service.asmx?WSDL"
PROD = "https://servicios1.afip.gov.ar/wsfexv1/service.asmx?WSDL"

CBTE_FACTURA_E = 19
DST_USA = 212  # per FEXGetPARAM_DST_pais
INCOTERM_FOB = "FOB"
IDIOMA_INGLES = 2
MON_USD = "DOL"


def load_ta(path: Path) -> tuple[str, str]:
    root = ET.fromstring(path.read_bytes())
    creds = root.find("credentials")
    if creds is None:
        raise ValueError(f"{path}: not a TA")
    return creds.findtext("token", ""), creds.findtext("sign", "")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--ta", type=Path, required=True)
    p.add_argument("--cuit", required=True)
    p.add_argument("--pto-vta", type=int, required=True)
    p.add_argument("--total", type=float, required=True, help="Total in USD")
    p.add_argument("--cotiz", type=float, required=True, help="USD→ARS rate")
    p.add_argument("--env", choices=["homo", "prod"], default="homo")
    args = p.parse_args()

    token, sign = load_ta(args.ta)
    auth = {"Token": token, "Sign": sign, "Cuit": args.cuit}
    client = Client(wsdl=HOMO if args.env == "homo" else PROD)

    last = client.service.FEXGetLast_CMP(
        Auth={**auth, "Pto_venta": args.pto_vta, "Cbte_Tipo": CBTE_FACTURA_E}
    )
    next_id = int(last.FEXResult_LastCMP.Cbte_nro) + 1

    cmp = {
        "Id": next_id,
        "Fecha_cbte": datetime.now().strftime("%Y%m%d"),
        "Cbte_Tipo": CBTE_FACTURA_E,
        "Punto_vta": args.pto_vta,
        "Cbte_nro": next_id,
        "Tipo_expo": 1,
        "Permiso_existente": "N",
        "Dst_cmp": DST_USA,
        "Cliente": "Acme Inc.",
        "Cuit_pais_cliente": "50000000016",
        "Domicilio_cliente": "1 Acme Way, NY",
        "Id_impositivo": "FED-12345",
        "Moneda_Id": MON_USD,
        "Moneda_ctz": args.cotiz,
        "Obs_comerciales": "",
        "Imp_total": args.total,
        "Obs": "",
        "Forma_pago": "Wire transfer",
        "Incoterms": INCOTERM_FOB,
        "Incoterms_Ds": "Free On Board",
        "Idioma_cbte": IDIOMA_INGLES,
        "Items": {"Item": [{
            "Pro_codigo": "SKU-001",
            "Pro_ds": "Widget",
            "Pro_qty": 10,
            "Pro_umed": 7,
            "Pro_precio_uni": args.total / 10,
            "Pro_total_item": args.total,
        }]},
    }

    resp = client.service.FEXAuthorize(Auth=auth, Cmp=cmp)
    if resp.FEXResultAuth.Resultado != "A":
        print(f"REJECTED: {resp.FEXResultAuth.Motivos_Obs}", file=sys.stderr)
        return 1
    print(f"CAE: {resp.FEXResultAuth.Cae}")
    print(f"Vto: {resp.FEXResultAuth.Fch_venc_Cae}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
