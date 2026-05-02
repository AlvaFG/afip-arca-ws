---
name: afip-arca-padron
description: Use when the user queries the AFIP/ARCA padrón to look up CUIT/CUIL data — getPersona, padrón A4 (datos básicos), A5 (con domicilio), A13 (impositivos completos), A100 (constancia inscripción pública). Triggers padrón, getPersona, consultar CUIT, constancia de inscripción, A4/A5/A13/A100, persona física vs jurídica.
---

# AFIP/ARCA Padrón Services

Four flavors of CUIT lookup, differing in scope and authorization required:

| Servicio | Scope | TA service | Auth nivel |
|---|---|---|---|
| A4 (`ws_sr_padron_a4`) | Básicos: razón social, tipo persona, estado | `ws_sr_padron_a4` | Privado |
| A5 (`ws_sr_padron_a5`) | A4 + domicilio fiscal | `ws_sr_padron_a5` | Privado |
| A13 (`ws_sr_padron_a13`) | A5 + impuestos en los que está inscripto | `ws_sr_padron_a13` | Privado |
| A100 (`ws_sr_constancia_inscripcion`) | Constancia pública | (no TA) | Público |

## Critical gotchas

- **A100 is the only one that doesn't require TA.** It's the public "constancia de inscripción".
- **Each privado service requires separate authorization** of your cert in the AR Clave Fiscal portal. Asking A4 doesn't give you A5.
- **Some services return `Errores` even on a 200 OK SOAP**, e.g. CUIT inexistente. Always check `personaReturn.errorReturn` (or analog) before consuming `personaReturn.persona`.
- **Endpoints**: docs lists per-service URLs in `references/padron-a{4,5,13,100}.md`.

## Quick flow (private padrón, e.g. A4)

1. TA from `afip-arca-wsaa` with `service=ws_sr_padron_a4`.
2. Call `getPersona({ token, sign, cuitRepresentada, idPersona })`.
3. Parse `personaReturn.persona` for the data.

## Examples

`examples/{python,node,php}/` show A4 lookups. A5/A13 differ only by endpoint and response fields.

## Depends on / leads to

- A4/A5/A13: depends on `afip-arca-wsaa` and `afip-arca-certificates`.
- A100: standalone (no auth).
