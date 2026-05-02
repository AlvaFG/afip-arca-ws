# Decision tree — which AFIP/ARCA skill to use

```
User asks about AFIP/ARCA?
├─ About certificates (.crt/.key/.p12, CSR, AR Clave Fiscal, renewal)
│  └─→ afip-arca-certificates
├─ About authentication (TRA, TA, loginCms, sign CMS, token+sign)
│  └─→ afip-arca-wsaa  (depends on: certificates)
├─ About issuing an invoice (CAE, FECAESolicitar)
│  ├─ Domestic (mercado interno) →  afip-arca-wsfev1   (depends on: wsaa)
│  └─ Export                     →  afip-arca-wsfexv1  (depends on: wsaa)
├─ About querying a CUIT (padrón, getPersona)
│  └─→ afip-arca-padron  (depends on: wsaa, except A100 public)
└─ Something is broken / 404 / SOAP fault / TLS error / "doesn't connect"
   └─→ afip-arca-debugging
```

## Common multi-skill flows

### "I need to start integrating AFIP from zero in <language>"
1. `afip-arca-certificates` — get the .crt/.key first
2. `afip-arca-wsaa` — implement TA acquisition + caching
3. Pick service: `afip-arca-wsfev1` (typical) or others

### "Renew my certificate"
1. `afip-arca-certificates` (renewal-checklist.md is the entry doc)
2. After cutover, re-validate WSAA flow with `afip-arca-debugging` (test-fedummy.sh)

### "FECAESolicitar returns error 10016"
1. `afip-arca-wsfev1` references/error-codes.md (lookup) — first stop
2. If still stuck → `afip-arca-debugging`

### "My TA isn't being accepted by the service"
1. `afip-arca-wsaa` references/wsaa-error-codes.md — was loginCms even successful?
2. Check TA cache invalidation (was it stale?)
3. Check service scope mismatch (TA for `wsfe` against `wsfex` won't work)
4. Fallback → `afip-arca-debugging`

### "How do I test without breaking production?"
1. `afip-arca-debugging` references/homologacion-vs-prod.md — endpoints comparison
2. `afip-arca-certificates` — separate cert per environment
