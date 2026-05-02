---
name: afip-arca-overview
description: Use this skill whenever the user mentions AFIP, ARCA, factura electrónica argentina, CAE, CUIT, padrón, WSAA, WSFE, WSFEX, homologación, .crt/.key/.p12 for AFIP, or asks how to integrate any Argentine tax-authority Web Service. This is the ROUTER skill — its job is to direct you to the specific sub-skill (afip-arca-certificates, afip-arca-wsaa, afip-arca-wsfev1, afip-arca-wsfexv1, afip-arca-padron, afip-arca-debugging) that matches the user's task. If 1% of the conversation might be about AFIP/ARCA, invoke this.
---

# AFIP/ARCA Web Services — Overview / Router

This skill is the entry point for all AFIP/ARCA Web Services work. **You almost never answer from this skill alone** — your job is to identify which specific sub-skill applies and invoke it via the `Skill` tool.

## Decision tree — pick the right skill

| The user is working on… | Invoke this skill |
|---|---|
| Generating CSR, installing .crt, renewing certificates, AR Clave Fiscal portal | `afip-arca-certificates` |
| Generating a TRA, signing CMS, calling `loginCms`, caching the TA | `afip-arca-wsaa` |
| Issuing invoices in Argentina (FECAESolicitar, CAE, mercado interno) | `afip-arca-wsfev1` |
| Issuing export invoices (FEXAuthorize, monedas, incoterms) | `afip-arca-wsfexv1` |
| Querying CUIT data (padrón A4/A5/A13/A100, getPersona) | `afip-arca-padron` |
| "My AFIP client is failing" / FEDummy / homologación vs producción / SoapUI | `afip-arca-debugging` |

If the request crosses skills (e.g. "set up AFIP from scratch in Python"), invoke them in this order: `certificates` → `wsaa` → the service skill (`wsfev1`/`wsfexv1`/`padron`).

For the full decision tree with conditions and edge cases, read `references/decision-tree.md`.

## ARCA vs AFIP naming

The agency was renamed from **AFIP** to **ARCA** (Agencia de Recaudación y Control Aduanero) in late 2024. **The Web Services were not renamed.** WSDL endpoints, namespaces, and method names still use `afip.gob.ar` and the term "AFIP" internally. Treat the names as interchangeable in user-facing language; in code and URLs, keep AFIP. See `references/arca-rebrand-notes.md` for what changed and what didn't.

## Raw documentation

The mirrored official AFIP/ARCA WS docs live at the repo root under `docs/`. Start at `docs/README.md` (auto-generated index). Each page has frontmatter with `source_url` for citation. Prefer the local copy over fetching live pages — it's versioned and your context is already tight.
