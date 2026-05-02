---
name: afip-arca-wsaa
description: Use when the user works with AFIP/ARCA WSAA — generating a TRA (Ticket de Requerimiento de Acceso), signing it as CMS/PKCS#7 with a private key, calling loginCms, parsing the TA (Ticket de Acceso), or caching a TA for reuse. Triggers on TRA, TA, loginCms, "Ticket de Acceso", sign CMS, token+sign, WSAA in any AFIP context.
---

# AFIP/ARCA WSAA — Ticket de Acceso flow

WSAA is the gatekeeper. Every other AFIP Web Service requires a valid TA. The TA is the result of: build XML → sign as CMS → base64 → POST to `loginCms` → parse the returned XML for `<token>` and `<sign>`.

## Critical gotchas

- **TAs are valid for 12 hours.** Cache them. Do NOT call `loginCms` on every request — AFIP will rate-limit and may temporarily block the cert.
- **One TA per service.** A TA for `wsfe` cannot be reused against `padron`. Cache key = (cuit, service, environment).
- **Generation/expiration time is in `<generationTime>`/`<expirationTime>` of the TRA.** Use ISO 8601 with timezone (e.g. `2026-05-02T14:30:00-03:00`). Submit ≤2 minutes before generation, ≤24h before expiration. Most clients use generation = now-60s, expiration = now+10min.
- **uniqueId must be unique.** Use a Unix timestamp; the same uniqueId can't be used twice within the same minute.
- **Endpoints**: homologación `https://wsaahomo.afip.gov.ar/ws/services/LoginCms`, producción `https://wsaa.afip.gov.ar/ws/services/LoginCms`. Mismatch → SOAP fault.

## Quick flow

1. Build TRA XML — see `assets/tra.xml.tmpl`.
2. Sign as CMS/PKCS#7 with the cert+key from `afip-arca-certificates`.
3. Base64-encode the CMS bytes.
4. SOAP POST to `loginCms` with `<in0>` containing the base64 string.
5. Parse `<loginTicketResponse>` from the response — extract `<token>` and `<sign>`.
6. Cache TA until `<expirationTime>`.

Detailed flow: `references/tra-flow.md`. Caching strategies (filesystem, DB, in-memory): `references/ta-caching-rules.md`. Error code lookup: `references/wsaa-error-codes.md`.

## Examples

End-to-end TA acquisition by language: `examples/{python,node,php,bash}/`. Each is self-contained — only requires a cert + key path.

## Depends on / leads to

- Depends on: `afip-arca-certificates` (need a working .crt + .key first).
- Leads to: invoke `afip-arca-wsfev1` / `afip-arca-wsfexv1` / `afip-arca-padron` once the TA is in hand.
