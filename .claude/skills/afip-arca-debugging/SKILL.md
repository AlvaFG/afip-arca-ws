---
name: afip-arca-debugging
description: Use when something is broken in an AFIP/ARCA integration — SOAP fault, TLS handshake error, "no anda mi cliente AFIP", FEDummy returning DOWN, mixing homologación vs producción endpoints, or wanting to set up SoapUI to inspect requests. Triggers AFIP error, SOAP fault, FEDummy, homologación, sandbox, SoapUI, TLS afip, "no responde", "no conecta".
---

# AFIP/ARCA Debugging

When an AFIP integration breaks, the failure is usually one of: wrong endpoint env, expired/malformed cert, expired TA, malformed request, or AFIP service genuinely down.

## Triage flow

```
Something broken with AFIP?
├─ Network/TLS error → check cert env (homo cert against prod URL?)
├─ SOAP fault on loginCms → cert/TA related → afip-arca-wsaa wsaa-error-codes.md
├─ SOAP fault on FECAESolicitar / FEXAuthorize / getPersona
│  ├─ 600/601 → TA expired/invalid → re-issue
│  └─ Others → service-specific error code reference
├─ FEDummy returns AppServer=NO/DbServer=NO/AuthServer=NO → AFIP is down, not you
│  └─ Check Twitter/status pages; wait it out
└─ Nothing returned, hangs → TLS issue, check curl -v
```

## Reference docs

- `references/homologacion-vs-prod.md` — every endpoint URL pair, side by side.
- `references/fedummy-checks.md` — how to call FEDummy/FEXDummy for every service.
- `references/soapui-setup.md` — load WSDL + configure cert in SoapUI.
- `references/common-errors-flowchart.md` — flowchart for the most-asked errors.

## Tools

`scripts/test-fedummy.sh` — pings the dummy method of WSFEv1 and WSFEXv1 in a chosen environment. No cert required.
