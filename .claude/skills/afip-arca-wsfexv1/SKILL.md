---
name: afip-arca-wsfexv1
description: Use when the user issues export electronic invoices via AFIP/ARCA WSFEXv1 — calling FEXAuthorize for export comprobantes (factura E), querying FEXGetCMP, looking up monedas/incoterms/idiomas, dealing with foreign-currency invoices and destination countries. Triggers WSFEXv1, FEXAuthorize, factura E, exportación, incoterms, FEXGetPARAM, monedas extranjeras.
---

# AFIP/ARCA WSFEXv1 — Factura Electrónica de Exportación

The export-invoice analog of WSFEv1. Different request shape (uses `Cmp` not `FECAEDetRequest`), supports foreign currency natively, and requires destination country + incoterm + idioma.

## Critical gotchas

- **Different from WSFEv1.** Don't try to reuse code.
- **Currency**: `Mon_id` from `FEXGetPARAM_MON`; `Mon_ctz` is the conversion rate to ARS at invoice date (from BCRA cotización).
- **Destino**: country code from `FEXGetPARAM_DST_pais`. Argentina (200) is invalid as destination — error 1510.
- **Incoterms**: must come from `FEXGetPARAM_Incoterms` (FOB, CIF, etc.). Both `Incoterms` (code) and `Incoterms_Ds` (description) are required.
- **Idioma del comprobante**: 1 (Español), 2 (Inglés), 3 (Portugués) per `FEXGetPARAM_Idiomas`.
- **Endpoints**: homo `https://wswhomo.afip.gov.ar/wsfexv1/service.asmx?WSDL`, prod `https://servicios1.afip.gov.ar/wsfexv1/service.asmx?WSDL`.
- **TA service scope**: `wsfex` (not `wsfe`).

## Quick flow

1. TA from `afip-arca-wsaa` with `service=wsfex`.
2. `FEXGetLast_CMP(Pto_venta, Cbte_Tipo)` → ultimo autorizado.
3. Build `Cmp` with required export fields (`Dst_cmp`, `Idioma_cbte`, `Moneda_Id`, `Moneda_ctz`, `Incoterms`, `Items`).
4. `FEXAuthorize(Auth, Cmp)` → returns `FEXResultAuth.Cae` + `Fch_venc_Cae`.

References: `methods.md`, `idiomas.md`, `monedas.md`, `incoterms.md`, `error-codes.md`.

## Examples

`examples/{python,node,php}/` — issue a Factura E in USD to a US buyer. Bash skipped (export invoices are too verbose for hand-rolled curl).

## Depends on / leads to

- Depends on: `afip-arca-wsaa` (service=wsfex), `afip-arca-certificates`.
