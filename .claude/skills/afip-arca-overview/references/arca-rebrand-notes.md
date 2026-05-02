# ARCA rebrand — what changed, what didn't

In late 2024 AFIP (Administración Federal de Ingresos Públicos) was reorganized and renamed to **ARCA — Agencia de Recaudación y Control Aduanero**.

## What changed

- The agency name in user-facing communications, website branding, and email domains (`@arca.gob.ar`).
- Some institutional pages moved under `arca.gob.ar`.
- Some sections of the AR Clave Fiscal portal show "ARCA" branding.

## What did NOT change (as of 2026-05)

- **Web Services WSDL endpoints**: still `*.afip.gov.ar` (e.g. `wsaa.afip.gov.ar`, `servicios1.afip.gov.ar`).
- **Domain for WS docs**: `https://www.afip.gob.ar/ws/`.
- **WSDL namespaces**: still reference `afip.gov.ar`.
- **Method names, types, error codes**: identical.
- **Certificates**: same issuance flow via "Administrador de Relaciones de Clave Fiscal".
- **CUIT format**: unchanged.

## Practical guidance for code

- In URLs, hostnames, namespaces → keep "afip".
- In documentation comments and user-facing strings → either is fine; "AFIP/ARCA" covers both.
- Do not refactor working code from `afip` to `arca` — you will break it.
- If you see "ARCA" in a method name or namespace, double-check — it is almost certainly an error or a third-party wrapper.
