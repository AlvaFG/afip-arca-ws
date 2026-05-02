---
name: afip-arca-certificates
description: Use when the user works with X.509 certificates for AFIP/ARCA — generating a CSR, requesting a .crt via the AR Clave Fiscal portal, bundling key+cert into .p12 for Java/.NET, inspecting expiration, or renewing. Triggers on .crt, .key, .p12, CSR, "Administrador de Relaciones", "Clave Fiscal", certificate renewal in any AFIP context.
---

# AFIP/ARCA Certificates

AFIP requires an X.509 client certificate for every Web Service request (the certificate is what authorizes a CUIT to call a service). This skill covers obtaining, installing, and renewing them.

## Critical gotchas

- **Validity is 2 years.** Track expiration; expiry mid-flight returns `WSAA-001` style errors.
- **Alias matters.** When you upload the CSR via the portal, the "Alias" you choose becomes the CN of the cert. Keep it stable across renewals or you'll have to re-authorize the cert against each WS.
- **Production and homologación are separate certs.** Same CUIT can have one cert per environment. Don't mix them.
- **Do not commit `.crt` or `.key` to Git.** Even homologación certs.

## Workflow — first-time setup

1. Generate private key + CSR locally — see `references/csr-howto.md` (or run `scripts/generate-csr.sh`).
2. Log in to the AFIP portal with Clave Fiscal — see `references/ar-clave-fiscal-portal.md`.
3. Upload the CSR, get the `.crt`.
4. Authorize the cert to use specific Web Services (per service: WSAA, WSFEv1, etc.) via "Administrador de Relaciones".
5. Verify with `scripts/check-cert.sh path/to/cert.crt`.
6. Optionally bundle into `.p12` for Java/.NET runtimes — `scripts/pem-to-p12.sh`.

## Workflow — renewal

See `references/renewal-checklist.md`. Key points: renew at least 30 days before expiry, keep the same alias, do a side-by-side smoke test against homologación before swapping production.

## Depends on / leads to

- Standalone: this skill produces the `.crt` + `.key` consumed by `afip-arca-wsaa`.
- After certificate is in place → invoke `afip-arca-wsaa` to get a TA.
