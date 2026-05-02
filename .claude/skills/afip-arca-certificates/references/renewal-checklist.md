# Certificate renewal checklist

Run through this 30 days before any AFIP cert expires.

- [ ] Identify expiry date for every cert in use:
      ```bash
      for f in *.crt; do echo "$f"; openssl x509 -in $f -noout -enddate; done
      ```
- [ ] Generate a new CSR with the **same** alias and CUIT serialNumber. Different alias = re-authorize every WS.
- [ ] Upload via WSASS, download the new `.crt`.
- [ ] Stage it alongside the old one (don't replace yet). Naming: `cert-2028.crt` next to `cert-2026.crt`.
- [ ] Run `scripts/check-cert.sh cert-2028.crt` — verify validity ≥720 days.
- [ ] Smoke test against homologación using new cert (`afip-arca-debugging` → test-fedummy.sh).
- [ ] Cutover: swap the file pointer in your config. Keep old cert until the new one has run a full day in prod.
- [ ] Invalidate any cached TA (`rm /var/cache/afip-ta.xml` or equivalent) — TAs are tied to the cert that signed them.
- [ ] Delete the old cert from disk only after 7 days of clean prod operation.

## Why "same alias" is critical

When AFIP issues the new cert, it gets a new serial number but keeps the same CN (alias). All Web Service authorizations in "Administrador de Relaciones" are linked to the **alias**, not the cert serial. So:

- Same alias → all existing service authorizations still valid for the new cert. Zero re-work.
- Different alias → you have to go to "Administrador de Relaciones" and re-authorize the new alias for every WS your app uses. Hours of manual work, error-prone, and any service you forget will fail in production.

## What can go wrong during cutover

- **Cached TA still references old cert**: WSAA returns `cms.cert.untrusted`. Fix: clear the TA cache.
- **Old cert still in load balancer / proxy**: connection from one node uses old cert, another uses new. Fix: blue/green or rolling deploy with verification.
- **Cert + key mismatch**: you accidentally pair the new `.crt` with the old `.key`. WSAA returns `cms.sign.invalid`. Fix: verify with `openssl x509 -in cert.crt -noout -modulus | md5sum` vs `openssl rsa -in key.key -noout -modulus | md5sum` — they must match.
