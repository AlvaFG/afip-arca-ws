---
name: afip-arca-wsfev1
description: Use when the user issues domestic electronic invoices in Argentina via AFIP/ARCA WSFEv1 — calling FECAESolicitar to get a CAE, querying FECompUltimoAutorizado, looking up FEParamGetTiposCbte/IVA/Doc, debugging FECAEResponse errors, or designing the request payload (factura A/B/C/M, notas de crédito/débito). Triggers WSFEv1, FECAE, CAE, factura electrónica, FEParamGet, "comprobante", punto de venta.
---

# AFIP/ARCA WSFEv1 — Factura Electrónica (mercado interno)

The main domestic invoicing Web Service. You build a `FECAERequest`, call `FECAESolicitar`, and get back a CAE (Código de Autorización Electrónico) plus its expiration. The CAE is what makes the invoice legally valid.

## Critical gotchas

- **Numbering is per (Punto de Venta, Tipo de Comprobante).** Always call `FECompUltimoAutorizado` first to get the last authorized number, then submit `last + 1`. Submitting a gap or duplicate fails with `10016`.
- **Importes are decimals with 2 places, sent as numbers (not strings).** Some clients send "100.50" and AFIP rejects with type errors.
- **Sum of `ImpNeto + ImpIVA + ImpTrib + ImpOpEx + ImpTotConc` must equal `ImpTotal` exactly.** Rounding errors are the #1 cause of `10048`.
- **`Iva` array rules vary by `CbteTipo`.** Factura B (responsable inscripto a consumidor final) requires `Iva` if `ImpIVA > 0`; factura C (monotributo) does NOT send `Iva` at all. See `references/tipos-comprobante.md`.
- **Always call `FEDummy` first when debugging connectivity.** It doesn't consume a TA and confirms the WS is up.
- **Endpoints**: homo `https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL`, prod `https://servicios1.afip.gov.ar/wsfev1/service.asmx?WSDL`.

## Quick flow

1. Get TA via `afip-arca-wsaa` (service = `wsfe`).
2. `FECompUltimoAutorizado(PtoVta, CbteTipo)` → returns `CbteNro`.
3. Build `FECAERequest` with `CbteDesde = CbteHasta = CbteNro + 1`.
4. `FECAESolicitar(Auth, FeCAEReq)` → returns `FeCabResp.Resultado` (`A` = approved, `R` = rejected, `P` = partial) and per-comprobante `CAE` + `CAEFchVto`.
5. Persist CAE + numero + fecha for legal/tax record.

Detailed method ref: `references/methods.md`. Type tables: `tipos-comprobante.md`, `tipos-doc.md`, `alicuotas-iva.md`. Error codes: `error-codes.md`.

## Examples

End-to-end factura B in `examples/{python,node,php,bash}/`. The Python example shows zeep, the Node uses `soap`, PHP uses native `SoapClient`, Bash hits FEDummy only (real factura via curl is brittle).

## Depends on / leads to

- Depends on: `afip-arca-wsaa` (need TA with `service=wsfe`), `afip-arca-certificates`.
- Leads to: nothing — this is the leaf service.
