# afip-arca-ws Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Git repository (`github.com/AlvaFG/afip-arca-ws`) containing 7 Claude Code skills for AFIP/ARCA Web Services integration, a Markdown documentation scraper, GitHub Actions for weekly refresh, and lint CI for code examples in 4 languages.

**Architecture:** Multi-skill suite under `.claude/skills/` (one skill per AFIP service domain) + a Python scraper (`scraper/`) that mirrors `afip.gob.ar/ws/` to versioned Markdown under `docs/`. A "router" skill (`afip-arca-overview`) dispatches to specific skills via decision tree. CI workflows lint scraper, examples (Python/Node/PHP/Bash), and SKILL.md frontmatter.

**Tech Stack:** Python 3.12 (httpx, selectolax, markdownify, PyYAML, pytest, ruff), Node 20 (typescript), PHP 8.2, Bash + shellcheck, GitHub Actions, gh CLI.

**Working directory:** `C:\Users\alvar\Downloads\files\afip-arca-ws` (already a git repo with the spec committed).

**Code review checkpoints:** This plan invokes `superpowers:requesting-code-review` at the end of each major phase (after scraper, after every skill, after CI, and a final review before pushing to GitHub). Each review reads the diff since the previous review tag, checks against the spec section it implements, and any issues are fixed before tagging the phase complete.

---

## Phase 1: Repo skeleton

### Task 1: Add LICENSE, .gitignore, top-level README placeholder

**Files:**
- Create: `LICENSE`
- Create: `.gitignore`
- Create: `README.md`

- [ ] **Step 1: Write LICENSE (MIT)**

```
MIT License

Copyright (c) 2026 Alvaro Fernandez Guyot

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

The contents of the `docs/` directory are owned by AFIP/ARCA and reproduced
here as a functional mirror for technical reference.
```

- [ ] **Step 2: Write .gitignore**

```
__pycache__/
*.pyc
.venv/
venv/
.env
.DS_Store
*.log
node_modules/
dist/
*.tsbuildinfo
.idea/
.vscode/
```

- [ ] **Step 3: Write README.md placeholder (final version is Task 38)**

```markdown
# afip-arca-ws

Suite de Claude Code skills para integraciones con AFIP/ARCA Web Services.

**WIP** — see `docs/superpowers/plans/` for implementation status.
```

- [ ] **Step 4: Commit**

```bash
cd C:\Users\alvar\Downloads\files\afip-arca-ws
git add LICENSE .gitignore README.md
git commit -m "chore: add LICENSE, .gitignore, README placeholder"
```

### Task 2: Migrate scraper from existing prototype files

**Files:**
- Create: `scraper/scrape.py` (copy from `C:\Users\alvar\Downloads\files\scrape.py`)
- Create: `scraper/config.yaml` (copy from `C:\Users\alvar\Downloads\files\config.yaml`)
- Create: `scraper/requirements.txt`
- Create: `scraper/__init__.py` (empty)

- [ ] **Step 1: Copy prototype files**

```bash
cp /c/Users/alvar/Downloads/files/scrape.py /c/Users/alvar/Downloads/files/afip-arca-ws/scraper/scrape.py
cp /c/Users/alvar/Downloads/files/config.yaml /c/Users/alvar/Downloads/files/afip-arca-ws/scraper/config.yaml
touch /c/Users/alvar/Downloads/files/afip-arca-ws/scraper/__init__.py
```

- [ ] **Step 2: Write `scraper/requirements.txt`**

Content:
```
httpx>=0.27
selectolax>=0.3.21
markdownify>=0.13
PyYAML>=6.0
pytest>=8.0
ruff>=0.5
```

- [ ] **Step 3: Verify scrape.py runs --help**

Run: `cd /c/Users/alvar/Downloads/files/afip-arca-ws/scraper && python -m venv .venv && source .venv/Scripts/activate && pip install -r requirements.txt && python scrape.py --help`
Expected: argparse usage block prints, exit 0.

- [ ] **Step 4: Commit**

```bash
git add scraper/
git commit -m "chore(scraper): import initial scraper from prototype"
```

---

## Phase 2: Scraper improvements + tests

### Task 3: Multi-root crawl

**Files:**
- Modify: `scraper/scrape.py` (add `self.start_urls`, use it in `scrape()`)
- Modify: `scraper/config.yaml` (uncomment `start_urls`)

- [ ] **Step 1: Edit `scraper/config.yaml`** — replace the commented `start_urls:` block with:

```yaml
start_urls:
  - "https://www.afip.gob.ar/ws/"
  - "https://www.afip.gob.ar/ws/programadores/"
  - "https://www.afip.gob.ar/ws/documentacion/"
  - "https://www.afip.gob.ar/ws/aplicativos/"
  - "https://www.afip.gob.ar/ws/menu-ayuda/"
```

- [ ] **Step 2: In `scraper/scrape.py`, in `DocsScraper.__init__`, add after the `self.max_pages = ...` line**:

```python
        self.start_urls: list[str] = config.get("start_urls") or [self.base_url + "/"]
```

- [ ] **Step 3: In `scrape()`, replace the first line**:

Old:
```python
        queue: list[str] = list(start_urls) if start_urls else [self.base_url + "/"]
```

New:
```python
        queue: list[str] = list(start_urls) if start_urls else list(self.start_urls)
```

- [ ] **Step 4: Smoke test (network required)**

Run: `cd scraper && python scrape.py --max-pages 5`
Expected: 5 pages crawled across multiple roots; files appear under `../docs/`.

- [ ] **Step 5: Discard scraped output and commit code only**

```bash
rm -rf /c/Users/alvar/Downloads/files/afip-arca-ws/docs/programadores /c/Users/alvar/Downloads/files/afip-arca-ws/docs/documentacion /c/Users/alvar/Downloads/files/afip-arca-ws/docs/aplicativos /c/Users/alvar/Downloads/files/afip-arca-ws/docs/menu-ayuda /c/Users/alvar/Downloads/files/afip-arca-ws/docs/index.md /c/Users/alvar/Downloads/files/afip-arca-ws/docs/README.md /c/Users/alvar/Downloads/files/afip-arca-ws/docs/_meta.json /c/Users/alvar/Downloads/files/afip-arca-ws/docs/_assets-index.md 2>/dev/null
git add scraper/scrape.py scraper/config.yaml
git commit -m "feat(scraper): multi-root crawl from explicit start URLs"
```

### Task 4: Diff-friendly output (sorted frontmatter, sidecar meta)

**Files:**
- Modify: `scraper/scrape.py`

- [ ] **Step 1: In `scrape()`, replace the inline frontmatter block** (the lines starting with `frontmatter = (` through `f"---\n\n"`):

Old:
```python
                frontmatter = (
                    f"---\n"
                    f'source_url: "{url}"\n'
                    f'title: "{title.replace(chr(34), chr(39))}"\n'
                    f"scraped_at: {time.strftime('%Y-%m-%d')}\n"
                    f"---\n\n"
                )
```

New:
```python
                fm_fields = {
                    "source_url": url,
                    "title": title.replace('"', "'"),
                }
                fm_lines = ["---"]
                for key in sorted(fm_fields):
                    fm_lines.append(f'{key}: "{fm_fields[key]}"')
                fm_lines.append("---")
                fm_lines.append("")
                frontmatter = "\n".join(fm_lines) + "\n"
```

- [ ] **Step 2: Add `_write_meta` method** after `_write_index`:

```python
    def _write_meta(self, entries: list[tuple[str, str]]):
        import json
        meta = {
            "page_count": len(entries),
            "scraped_at": time.strftime("%Y-%m-%d"),
            "source": self.base_url,
        }
        (self.output_dir / "_meta.json").write_text(
            json.dumps(meta, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
```

- [ ] **Step 3: Call `_write_meta` from `scrape()`** — add right before `return stats`:

```python
        self._write_meta(index_entries)
```

- [ ] **Step 4: Determinism test (no network)**

Run a Python one-liner that uses the html fixture (created in Task 6) — for now, just verify scrape.py imports cleanly:
`cd scraper && python -c "from scrape import DocsScraper; print('OK')"`
Expected: `OK`

- [ ] **Step 5: Commit**

```bash
git add scraper/scrape.py
git commit -m "feat(scraper): diff-friendly output (sorted frontmatter, sidecar meta)"
```

### Task 5: Asset index (WSDL/PDF discovery)

**Files:**
- Modify: `scraper/scrape.py`

- [ ] **Step 1: Add class constant + helper** (insert after `is_internal_doc_link`):

```python
    ASSET_EXTENSIONS = (".wsdl", ".xsd", ".pdf", ".zip")

    def is_asset_link(self, url: str) -> bool:
        if not url.startswith(self.allowed_prefix):
            return False
        return urlparse(url).path.lower().endswith(self.ASSET_EXTENSIONS)
```

- [ ] **Step 2: Replace `discover_links` entirely**:

```python
    def discover_links(self, html: str, current_url: str) -> tuple[list[str], list[str]]:
        tree = HTMLParser(html)
        docs: list[str] = []
        assets: list[str] = []
        for node in tree.css("a[href]"):
            href = node.attributes.get("href", "").strip()
            if not href or href.startswith(("#", "mailto:", "javascript:", "tel:")):
                continue
            absolute = urljoin(current_url, href).split("#")[0]
            if self.is_asset_link(absolute) and absolute not in assets:
                assets.append(absolute)
            elif self.is_internal_doc_link(absolute) and absolute not in docs:
                docs.append(absolute)
        return docs, assets
```

- [ ] **Step 3: Update `scrape()` consumer** — at top of method add `discovered_assets: set[str] = set()`. Replace the `for link in self.discover_links(...)` block with:

```python
            doc_links, asset_links = self.discover_links(html, url)
            for link in doc_links:
                if link not in self.visited:
                    queue.append(link)
            discovered_assets.update(asset_links)
```

Then before `self._write_meta(...)` add:

```python
        self._write_assets_index(sorted(discovered_assets))
```

- [ ] **Step 4: Add `_write_assets_index` method**:

```python
    def _write_assets_index(self, assets: list[str]):
        if not assets:
            return
        lines = [
            "# AFIP/ARCA Web Services — Asset Index",
            "",
            "_Auto-generated. Lists downloadable WSDL/XSD/PDF/ZIP files referenced by the docs._",
            "",
        ]
        for url in assets:
            lines.append(f"- <{url}>")
        (self.output_dir / "_assets-index.md").write_text(
            "\n".join(lines) + "\n", encoding="utf-8"
        )
```

- [ ] **Step 5: Verify imports clean**

Run: `cd scraper && python -c "from scrape import DocsScraper; print('OK')"`
Expected: `OK`

- [ ] **Step 6: Commit**

```bash
git add scraper/scrape.py
git commit -m "feat(scraper): discover and index downloadable assets (WSDL/XSD/PDF)"
```

### Task 6: Scraper unit tests with HTML fixture

**Files:**
- Create: `scraper/tests/__init__.py` (empty)
- Create: `scraper/tests/conftest.py`
- Create: `scraper/tests/fixtures/sample_page.html`
- Create: `scraper/tests/test_extract.py`
- Create: `scraper/pytest.ini`

- [ ] **Step 1: Write `scraper/pytest.ini`**:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
addopts = -ra -q
```

- [ ] **Step 2: Write `scraper/tests/conftest.py`** to make `scrape` importable:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
```

- [ ] **Step 3: Write `scraper/tests/fixtures/sample_page.html`**:

```html
<!doctype html>
<html lang="es">
<head><title>WSAA - Web Service de Autenticación | ARCA</title></head>
<body>
<header><nav>menu noise</nav></header>
<main>
  <h1>WSAA - Web Service de Autenticación</h1>
  <p>El WSAA es el servicio responsable de generar el Ticket de Acceso (TA).</p>
  <h2>Endpoints</h2>
  <table>
    <tr><th>Ambiente</th><th>URL</th></tr>
    <tr><td>Homologación</td><td>https://wsaahomo.afip.gov.ar/ws/services/LoginCms</td></tr>
    <tr><td>Producción</td><td>https://wsaa.afip.gov.ar/ws/services/LoginCms</td></tr>
  </table>
  <p>Documentos: <a href="/ws/documentacion/wsaa-manual.pdf">Manual WSAA (PDF)</a> y <a href="/ws/programadores/certificados-digitales.asp">Certificados</a>.</p>
</main>
<footer>footer noise</footer>
</body>
</html>
```

- [ ] **Step 4: Write `scraper/tests/test_extract.py`**:

```python
from pathlib import Path

import pytest

from scrape import DocsScraper

FIXTURE = Path(__file__).parent / "fixtures" / "sample_page.html"


@pytest.fixture
def scraper(tmp_path):
    return DocsScraper({
        "base_url": "https://www.afip.gob.ar/ws",
        "allowed_prefix": "https://www.afip.gob.ar/ws",
        "output_dir": str(tmp_path),
        "content_selector": "main",
        "delay_seconds": 0,
        "max_pages": 10,
    })


def test_extract_strips_arca_suffix_from_title(scraper):
    html = FIXTURE.read_text(encoding="utf-8")
    title, _ = scraper.extract_content(html)
    assert title == "WSAA - Web Service de Autenticación"


def test_extract_keeps_table_content(scraper):
    html = FIXTURE.read_text(encoding="utf-8")
    _, md = scraper.extract_content(html)
    assert "Homologación" in md
    assert "wsaahomo.afip.gov.ar" in md


def test_extract_strips_nav_and_footer(scraper):
    html = FIXTURE.read_text(encoding="utf-8")
    _, md = scraper.extract_content(html)
    assert "menu noise" not in md
    assert "footer noise" not in md


def test_url_to_path_converts_asp_to_md(scraper, tmp_path):
    p = scraper.url_to_path("https://www.afip.gob.ar/ws/programadores/certificados-digitales.asp")
    assert p == tmp_path / "programadores" / "certificados-digitales.md"


def test_url_to_path_handles_root(scraper, tmp_path):
    p = scraper.url_to_path("https://www.afip.gob.ar/ws/")
    assert p == tmp_path / "index.md"


def test_discover_links_separates_docs_and_assets(scraper):
    html = FIXTURE.read_text(encoding="utf-8")
    docs, assets = scraper.discover_links(html, "https://www.afip.gob.ar/ws/")
    assert "https://www.afip.gob.ar/ws/programadores/certificados-digitales.asp" in docs
    assert "https://www.afip.gob.ar/ws/documentacion/wsaa-manual.pdf" in assets
```

- [ ] **Step 5: Run tests**

Run: `cd scraper && python -m pytest -v`
Expected: 6 passed.

- [ ] **Step 6: Commit**

```bash
git add scraper/tests/ scraper/pytest.ini
git commit -m "test(scraper): unit tests for extract/url/discover helpers"
```

### Task 7: Code review for Phase 2 (scraper)

- [ ] **Step 1: Tag the phase**

```bash
git tag phase-2-scraper-complete
```

- [ ] **Step 2: Invoke `superpowers:requesting-code-review`** with scope: all changes under `scraper/` since the initial repo skeleton commit. Provide spec section 5.5 ("Scraper") as the requirements baseline. Ask for: correctness of refactor, test coverage adequacy, any silent failure modes.

- [ ] **Step 3: Address findings inline.** Commit each fix with `fix(scraper): <issue>`.

- [ ] **Step 4: Re-tag if changes were made**

```bash
git tag -f phase-2-scraper-complete
```

---

## Phase 3: Skill `afip-arca-overview` (router)

### Task 8: Create `afip-arca-overview` SKILL.md

**Files:**
- Create: `.claude/skills/afip-arca-overview/SKILL.md`
- Create: `.claude/skills/afip-arca-overview/references/decision-tree.md`
- Create: `.claude/skills/afip-arca-overview/references/arca-rebrand-notes.md`

- [ ] **Step 1: Write `.claude/skills/afip-arca-overview/SKILL.md`** with this exact content:

````markdown
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
````

- [ ] **Step 2: Write `.claude/skills/afip-arca-overview/references/decision-tree.md`** with the following content:

````markdown
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
````

- [ ] **Step 3: Write `.claude/skills/afip-arca-overview/references/arca-rebrand-notes.md`**:

````markdown
# ARCA rebrand — what changed, what didn't

In late 2024 AFIP (Administración Federal de Ingresos Públicos) was reorganized and renamed to **ARCA — Agencia de Recaudación y Control Aduanero**.

## What changed

- The agency name in user-facing communications, website branding, and email domains (`@arca.gob.ar`).
- Some institutional pages moved under `arca.gob.ar`.

## What did NOT change (as of 2026-05)

- **Web Services WSDL endpoints**: still `*.afip.gov.ar` (e.g. `wsaa.afip.gov.ar`, `servicios1.afip.gov.ar`).
- **Domain for WS docs**: `https://www.afip.gob.ar/ws/`.
- **WSDL namespaces**: still reference `afip.gov.ar`.
- **Method names, types, error codes**: identical.
- **Certificates**: same issuance flow via "Administrador de Relaciones de Clave Fiscal".

## Practical guidance for code

- In URLs, hostnames, namespaces → keep "afip".
- In documentation comments and user-facing strings → either is fine; "AFIP/ARCA" covers both.
- Do not refactor working code from `afip` to `arca` — you will break it.
````

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/afip-arca-overview/
git commit -m "feat(skill): add afip-arca-overview router skill"
```

### Task 9: Code review for Phase 3 (overview)

- [ ] **Step 1: Tag**: `git tag phase-3-overview-complete`
- [ ] **Step 2: Invoke `superpowers:requesting-code-review`** scoped to `.claude/skills/afip-arca-overview/`. Reference spec section 7.1.
- [ ] **Step 3: Address findings.** Commit fixes with `fix(skill-overview): <issue>`.
- [ ] **Step 4: Re-tag if needed.**

---

## Phase 4: Skill `afip-arca-certificates`

### Task 10: SKILL.md + references

**Files:**
- Create: `.claude/skills/afip-arca-certificates/SKILL.md`
- Create: `.claude/skills/afip-arca-certificates/references/csr-howto.md`
- Create: `.claude/skills/afip-arca-certificates/references/ar-clave-fiscal-portal.md`
- Create: `.claude/skills/afip-arca-certificates/references/renewal-checklist.md`
- Create: `.claude/skills/afip-arca-certificates/assets/openssl.cnf.tmpl`

- [ ] **Step 1: Write `SKILL.md`**:

````markdown
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
````

- [ ] **Step 2: Write `references/csr-howto.md`** — content outline that the engineer fills following these required sections (each section ≥80 words, with verbatim openssl commands):
  - **Section: "Generate the private key"** — must show `openssl genrsa -out private.key 2048` and explain when to use 4096.
  - **Section: "Build the openssl.cnf"** — reference `assets/openssl.cnf.tmpl`, list required fields (CN, O, serialNumber=CUIT/<cuit>, C=AR).
  - **Section: "Generate the CSR"** — show `openssl req -new -key private.key -subj "/C=AR/O=<organizacion>/CN=<alias>/serialNumber=CUIT <cuit>" -out request.csr`.
  - **Section: "Verify the CSR locally"** — `openssl req -in request.csr -text -noout | head -20`.
  - **Section: "What to upload"** — only `request.csr`, never the key.

- [ ] **Step 3: Write `references/ar-clave-fiscal-portal.md`**:

````markdown
# AR Clave Fiscal portal — getting your AFIP cert

The portal is `https://auth.afip.gob.ar/contribuyente_/login.xhtml`. You need Clave Fiscal level 3 or higher.

## One-time setup per CUIT

1. Log in with CUIT + Clave Fiscal.
2. Find "Administrador de Relaciones de Clave Fiscal".
3. Adherir Servicio → AFIP → Servicios Interactivos → "WebServices Autenticación de Certificados Digitales (WSASS)".
4. Inside WSASS, choose "Crear Certificado".
5. Paste the CSR contents (as text). Choose alias and environment (homologación / producción).
6. Download the `.crt`.

## Authorize the cert per WS

For each Web Service the cert will use (WSFEv1, WSFEXv1, padrón, etc.):

1. From "Administrador de Relaciones", "Nueva Relación".
2. Buscar el servicio (e.g. "Facturación Electrónica").
3. Representante: el alias del certificado (no el CUIT).
4. Confirmar.

The cert can be used to call that WS within ~1 hour after authorization.

## Production vs homologación

The portal has two flavors. Homologación lives at `https://wsaahomo.afip.gov.ar/...`; the cert request UI is the same but the resulting cert only works against `*homo*` endpoints. Cross-using a homo cert against prod (or vice versa) returns SOAP fault `ns1:cms.bad_audience`.
````

- [ ] **Step 4: Write `references/renewal-checklist.md`**:

````markdown
# Certificate renewal checklist

Run through this 30 days before any AFIP cert expires.

- [ ] Identify expiry date for every cert in use: `for f in *.crt; do echo "$f"; openssl x509 -in $f -noout -enddate; done`
- [ ] Generate a new CSR with the **same** alias and CUIT serialNumber. Different alias = re-authorize every WS.
- [ ] Upload via WSASS, download the new `.crt`.
- [ ] Stage it alongside the old one (don't replace yet). Naming: `cert-2028.crt` next to `cert-2026.crt`.
- [ ] Run `scripts/check-cert.sh cert-2028.crt` — verify validity ≥720 days.
- [ ] Smoke test against homologación using new cert (`afip-arca-debugging` → test-fedummy.sh).
- [ ] Cutover: swap the file pointer in your config. Keep old cert until the new one has run a full day in prod.
- [ ] Invalidate any cached TA (`rm /var/cache/afip-ta.xml` or equivalent) — TAs are tied to the cert that signed them.
- [ ] Delete the old cert from disk only after 7 days of clean prod operation.
````

- [ ] **Step 5: Write `assets/openssl.cnf.tmpl`**:

```ini
# Template for AFIP cert CSR. Fill the placeholders, then:
#   openssl req -new -config openssl.cnf -keyout private.key -out request.csr
[ req ]
default_bits        = 2048
default_md          = sha256
distinguished_name  = req_dn
prompt              = no

[ req_dn ]
C  = AR
O  = {{ORGANIZACION}}
CN = {{ALIAS}}
serialNumber = CUIT {{CUIT}}
```

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/afip-arca-certificates/
git commit -m "feat(skill): afip-arca-certificates SKILL.md, references, openssl template"
```

### Task 11: Scripts for `afip-arca-certificates`

**Files:**
- Create: `.claude/skills/afip-arca-certificates/scripts/generate-csr.sh`
- Create: `.claude/skills/afip-arca-certificates/scripts/check-cert.sh`
- Create: `.claude/skills/afip-arca-certificates/scripts/pem-to-p12.sh`

- [ ] **Step 1: Write `scripts/generate-csr.sh`**:

```bash
#!/usr/bin/env bash
# Generate a private key + CSR for AFIP/ARCA using safe defaults.
# Usage: ./generate-csr.sh <ALIAS> <CUIT> [ORGANIZACION]
set -euo pipefail

ALIAS="${1:?Usage: $0 <ALIAS> <CUIT> [ORGANIZACION]}"
CUIT="${2:?Missing CUIT}"
ORG="${3:-${ALIAS}}"

if [[ ! "$CUIT" =~ ^[0-9]{11}$ ]]; then
  echo "ERROR: CUIT must be exactly 11 digits, got: $CUIT" >&2
  exit 1
fi

KEY_FILE="${ALIAS}.key"
CSR_FILE="${ALIAS}.csr"

if [[ -f "$KEY_FILE" ]]; then
  echo "ERROR: $KEY_FILE already exists. Refusing to overwrite." >&2
  exit 1
fi

openssl req -new -newkey rsa:2048 -nodes \
  -keyout "$KEY_FILE" \
  -out "$CSR_FILE" \
  -subj "/C=AR/O=${ORG}/CN=${ALIAS}/serialNumber=CUIT ${CUIT}"

chmod 600 "$KEY_FILE"

echo
echo "✓ Generated:"
echo "  Private key: $KEY_FILE  (chmod 600)"
echo "  CSR:         $CSR_FILE  (upload this to WSASS)"
echo
echo "Next: upload $CSR_FILE via https://auth.afip.gob.ar → WSASS → Crear Certificado"
```

- [ ] **Step 2: Write `scripts/check-cert.sh`**:

```bash
#!/usr/bin/env bash
# Inspect an AFIP cert: subject, issuer, validity dates, SHA-256 fingerprint.
# Usage: ./check-cert.sh <path-to.crt>
set -euo pipefail

CERT="${1:?Usage: $0 <path-to.crt>}"

if [[ ! -f "$CERT" ]]; then
  echo "ERROR: $CERT not found" >&2
  exit 1
fi

echo "=== Certificate: $CERT ==="
openssl x509 -in "$CERT" -noout -subject
openssl x509 -in "$CERT" -noout -issuer
openssl x509 -in "$CERT" -noout -dates
openssl x509 -in "$CERT" -noout -fingerprint -sha256

# Days until expiry
END=$(openssl x509 -in "$CERT" -noout -enddate | cut -d= -f2)
END_TS=$(date -d "$END" +%s 2>/dev/null || gdate -d "$END" +%s)
NOW_TS=$(date +%s)
DAYS=$(( (END_TS - NOW_TS) / 86400 ))

echo
if (( DAYS < 0 )); then
  echo "✗ EXPIRED $((-DAYS)) days ago"
  exit 2
elif (( DAYS < 30 )); then
  echo "⚠ EXPIRES in $DAYS days — renew now"
  exit 1
else
  echo "✓ Valid for $DAYS more days"
fi
```

- [ ] **Step 3: Write `scripts/pem-to-p12.sh`**:

```bash
#!/usr/bin/env bash
# Bundle a PEM key + cert into a .p12 (PKCS#12) for Java/.NET runtimes.
# Usage: ./pem-to-p12.sh <key.key> <cert.crt> <alias> [out.p12]
set -euo pipefail

KEY="${1:?Usage: $0 <key.key> <cert.crt> <alias> [out.p12]}"
CRT="${2:?Missing cert}"
ALIAS="${3:?Missing alias}"
OUT="${4:-${ALIAS}.p12}"

if [[ -f "$OUT" ]]; then
  echo "ERROR: $OUT already exists. Refusing to overwrite." >&2
  exit 1
fi

openssl pkcs12 -export \
  -inkey "$KEY" \
  -in "$CRT" \
  -name "$ALIAS" \
  -out "$OUT"

chmod 600 "$OUT"
echo "✓ Wrote $OUT (chmod 600). Use the export password you just typed when loading into a keystore."
```

- [ ] **Step 4: Lint with shellcheck**

Run: `shellcheck .claude/skills/afip-arca-certificates/scripts/*.sh`
Expected: no errors. (If `shellcheck` is not installed, install via `choco install shellcheck` on Windows.)

- [ ] **Step 5: Make executable bits in git**

```bash
git update-index --chmod=+x .claude/skills/afip-arca-certificates/scripts/generate-csr.sh
git update-index --chmod=+x .claude/skills/afip-arca-certificates/scripts/check-cert.sh
git update-index --chmod=+x .claude/skills/afip-arca-certificates/scripts/pem-to-p12.sh
```

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/afip-arca-certificates/scripts/
git commit -m "feat(skill-certs): scripts for CSR, cert inspection, PEM→P12 bundle"
```

### Task 12: Code review for Phase 4 (certificates)

- [ ] **Step 1: Tag**: `git tag phase-4-certificates-complete`
- [ ] **Step 2: Invoke `superpowers:requesting-code-review`** scoped to `.claude/skills/afip-arca-certificates/`. Reference spec section 7.2.
- [ ] **Step 3: Address findings; commit fixes with `fix(skill-certs): ...`.**
- [ ] **Step 4: Re-tag if needed.**

---

## Phase 5: Skill `afip-arca-wsaa`

### Task 13: SKILL.md + references

**Files:**
- Create: `.claude/skills/afip-arca-wsaa/SKILL.md`
- Create: `.claude/skills/afip-arca-wsaa/references/tra-flow.md`
- Create: `.claude/skills/afip-arca-wsaa/references/ta-caching-rules.md`
- Create: `.claude/skills/afip-arca-wsaa/references/wsaa-error-codes.md`
- Create: `.claude/skills/afip-arca-wsaa/assets/tra.xml.tmpl`

- [ ] **Step 1: Write `SKILL.md`**:

````markdown
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
````

- [ ] **Step 2: Write `assets/tra.xml.tmpl`**:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<loginTicketRequest version="1.0">
  <header>
    <uniqueId>{{UNIQUE_ID}}</uniqueId>
    <generationTime>{{GENERATION_TIME}}</generationTime>
    <expirationTime>{{EXPIRATION_TIME}}</expirationTime>
  </header>
  <service>{{SERVICE}}</service>
</loginTicketRequest>
```

- [ ] **Step 3: Write `references/tra-flow.md`** with these mandatory sections (full prose, ≥120 words each unless noted):
  - **"Step 1 — Build the TRA XML"**: explain `uniqueId` (use `int(time.time())`), `generationTime`/`expirationTime` (ISO 8601 with TZ), `service` (the WS scope: `wsfe`, `wsfex`, `ws_sr_padron_a4`, etc.). Show one full XML example.
  - **"Step 2 — Sign as CMS"**: explain PKCS#7 detached vs attached (we use attached/embedded), reference: `openssl smime -sign -in tra.xml -signer cert.crt -inkey key.key -outform DER -nodetach -out tra.cms`.
  - **"Step 3 — Base64 encode"**: `base64 -w0 tra.cms` or programmatic equivalents.
  - **"Step 4 — SOAP POST to loginCms"**: include the full SOAP envelope template with the `<in0>` placeholder.
  - **"Step 5 — Parse the TA"**: show example `<loginTicketResponse>` and which fields to extract (`<token>`, `<sign>`, `<expirationTime>`).
  - **"WSDL endpoints"**: table of homo + prod URLs.

- [ ] **Step 4: Write `references/ta-caching-rules.md`** with mandatory sections:
  - **"Why caching is mandatory"**: explain rate-limit risk; cite that AFIP can suspend a cert for abuse.
  - **"Cache key"**: must be `(cuit, service, environment)`.
  - **"Storage options"**:
    - Filesystem (single instance, simplest): file per service, e.g. `cache/ta-wsfe-prod.xml`.
    - Database (multi-instance): table `afip_ta(cuit, service, env, token, sign, expires_at)`.
    - In-memory + lock (for short-lived workers): show pseudocode with mutex.
  - **"Concurrency"**: when N workers request TA simultaneously, the first should fetch and the rest should wait. Show a "double-checked locking" pseudocode.
  - **"When to invalidate"**: cert renewed → drop all cached TAs; SOAP returns expired-TA error → fetch a new one.

- [ ] **Step 5: Write `references/wsaa-error-codes.md`** as a Markdown table, columns: Code, Mensaje original (es), Causa típica, Fix. Include at minimum these well-known errors:
  - `coe.alreadyAuthenticated` → TRA reused or `uniqueId` collided. Fix: bump uniqueId.
  - `cms.cert.untrusted` → cert not for this environment (homo cert against prod or vice versa).
  - `cms.cert.expired` → renew cert.
  - `cms.bad_audience` → mismatched WSAA URL vs cert env.
  - `cms.sign.invalid` → CMS signature didn't validate; check key matches cert.
  - `xml.generationTime.invalid` → generationTime out of allowed window (>2 min in future, or in the past beyond tolerance).

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/afip-arca-wsaa/SKILL.md .claude/skills/afip-arca-wsaa/references/ .claude/skills/afip-arca-wsaa/assets/
git commit -m "feat(skill-wsaa): SKILL.md, TRA template, references for flow/caching/errors"
```

### Task 14: WSAA Python example

**Files:**
- Create: `.claude/skills/afip-arca-wsaa/examples/python/wsaa_login.py`
- Create: `.claude/skills/afip-arca-wsaa/examples/python/requirements.txt`
- Create: `.claude/skills/afip-arca-wsaa/examples/python/README.md`

- [ ] **Step 1: Write `examples/python/requirements.txt`**:

```
zeep>=4.2
cryptography>=42.0
```

- [ ] **Step 2: Write `examples/python/wsaa_login.py`**:

```python
"""
WSAA login — get a TA for a given service (homologación by default).

Usage:
    python wsaa_login.py --cert path/to/cert.crt --key path/to/private.key --service wsfe

Outputs the TA XML to stdout. Save to a file and cache it until <expirationTime>.
"""
from __future__ import annotations

import argparse
import base64
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import pkcs7
from zeep import Client

WSAA_HOMO = "https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl"
WSAA_PROD = "https://wsaa.afip.gov.ar/ws/services/LoginCms?wsdl"

ART = timezone(timedelta(hours=-3))


def build_tra(service: str) -> bytes:
    now = datetime.now(ART)
    tra = f"""<?xml version="1.0" encoding="UTF-8"?>
<loginTicketRequest version="1.0">
  <header>
    <uniqueId>{int(now.timestamp())}</uniqueId>
    <generationTime>{(now - timedelta(minutes=1)).isoformat(timespec='seconds')}</generationTime>
    <expirationTime>{(now + timedelta(minutes=10)).isoformat(timespec='seconds')}</expirationTime>
  </header>
  <service>{service}</service>
</loginTicketRequest>
"""
    return tra.encode("utf-8")


def sign_cms(tra_bytes: bytes, cert_path: Path, key_path: Path) -> bytes:
    cert = x509.load_pem_x509_certificate(cert_path.read_bytes())
    key = serialization.load_pem_private_key(key_path.read_bytes(), password=None)
    cms = (
        pkcs7.PKCS7SignatureBuilder()
        .set_data(tra_bytes)
        .add_signer(cert, key, hashes.SHA256())
        .sign(serialization.Encoding.DER, [pkcs7.PKCS7Options.Binary])
    )
    return cms


def login(cms_b64: str, env: str) -> str:
    wsdl = WSAA_HOMO if env == "homo" else WSAA_PROD
    client = Client(wsdl=wsdl)
    return client.service.loginCms(in0=cms_b64)


def main() -> int:
    p = argparse.ArgumentParser(description="WSAA login — obtain a TA")
    p.add_argument("--cert", type=Path, required=True)
    p.add_argument("--key", type=Path, required=True)
    p.add_argument("--service", default="wsfe", help="WS scope: wsfe, wsfex, ws_sr_padron_a4, ...")
    p.add_argument("--env", choices=["homo", "prod"], default="homo")
    args = p.parse_args()

    tra = build_tra(args.service)
    cms = sign_cms(tra, args.cert, args.key)
    cms_b64 = base64.b64encode(cms).decode("ascii")
    ta_xml = login(cms_b64, args.env)
    print(ta_xml)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 3: Write `examples/python/README.md`**:

````markdown
# WSAA login — Python example

```bash
pip install -r requirements.txt
python wsaa_login.py --cert ../../scripts/test.crt --key ../../scripts/test.key --service wsfe --env homo > ta-wsfe.xml
```

Cache `ta-wsfe.xml` until the `<expirationTime>` inside it. For caching strategies, see `../../references/ta-caching-rules.md`.
````

- [ ] **Step 4: Lint compile**

Run: `python -m py_compile .claude/skills/afip-arca-wsaa/examples/python/wsaa_login.py`
Expected: exit 0, no output.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/afip-arca-wsaa/examples/python/
git commit -m "feat(skill-wsaa): Python example for TA acquisition"
```

### Task 15: WSAA Bash example (openssl + curl)

**Files:**
- Create: `.claude/skills/afip-arca-wsaa/examples/bash/wsaa-login.sh`

- [ ] **Step 1: Write `wsaa-login.sh`**:

```bash
#!/usr/bin/env bash
# WSAA login using only openssl + curl.
# Usage: ./wsaa-login.sh <cert.crt> <key.key> <service> [homo|prod]
set -euo pipefail

CERT="${1:?Usage: $0 <cert.crt> <key.key> <service> [homo|prod]}"
KEY="${2:?Missing key}"
SERVICE="${3:?Missing service (e.g. wsfe)}"
ENV="${4:-homo}"

if [[ "$ENV" == "homo" ]]; then
  URL="https://wsaahomo.afip.gov.ar/ws/services/LoginCms"
else
  URL="https://wsaa.afip.gov.ar/ws/services/LoginCms"
fi

WORKDIR=$(mktemp -d)
trap 'rm -rf "$WORKDIR"' EXIT

NOW=$(date +%s)
GEN=$(date -u -d "@$((NOW - 60))" +%Y-%m-%dT%H:%M:%S 2>/dev/null || gdate -u -d "@$((NOW - 60))" +%Y-%m-%dT%H:%M:%S)
EXP=$(date -u -d "@$((NOW + 600))" +%Y-%m-%dT%H:%M:%S 2>/dev/null || gdate -u -d "@$((NOW + 600))" +%Y-%m-%dT%H:%M:%S)

cat > "$WORKDIR/tra.xml" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<loginTicketRequest version="1.0">
  <header>
    <uniqueId>${NOW}</uniqueId>
    <generationTime>${GEN}</generationTime>
    <expirationTime>${EXP}</expirationTime>
  </header>
  <service>${SERVICE}</service>
</loginTicketRequest>
EOF

openssl smime -sign \
  -in "$WORKDIR/tra.xml" \
  -signer "$CERT" \
  -inkey "$KEY" \
  -outform DER \
  -nodetach \
  -out "$WORKDIR/tra.cms"

CMS_B64=$(base64 -w0 "$WORKDIR/tra.cms" 2>/dev/null || base64 "$WORKDIR/tra.cms" | tr -d '\n')

cat > "$WORKDIR/req.xml" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:wsaa="http://wsaa.view.sua.dvadac.desein.afip.gov">
  <soapenv:Body>
    <wsaa:loginCms>
      <wsaa:in0>${CMS_B64}</wsaa:in0>
    </wsaa:loginCms>
  </soapenv:Body>
</soapenv:Envelope>
EOF

curl -sS -X POST "$URL" \
  -H "Content-Type: text/xml; charset=utf-8" \
  -H 'SOAPAction: ""' \
  --data-binary "@$WORKDIR/req.xml"
```

- [ ] **Step 2: Lint**

Run: `shellcheck .claude/skills/afip-arca-wsaa/examples/bash/wsaa-login.sh`
Expected: no errors.

- [ ] **Step 3: chmod +x and commit**

```bash
git update-index --chmod=+x .claude/skills/afip-arca-wsaa/examples/bash/wsaa-login.sh
git add .claude/skills/afip-arca-wsaa/examples/bash/
git commit -m "feat(skill-wsaa): Bash/openssl example for TA acquisition"
```

### Task 16: WSAA Node/TS example

**Files:**
- Create: `.claude/skills/afip-arca-wsaa/examples/node/package.json`
- Create: `.claude/skills/afip-arca-wsaa/examples/node/tsconfig.json`
- Create: `.claude/skills/afip-arca-wsaa/examples/node/wsaa-login.ts`
- Create: `.claude/skills/afip-arca-wsaa/examples/node/README.md`

- [ ] **Step 1: Write `package.json`**:

```json
{
  "name": "afip-arca-wsaa-example",
  "private": true,
  "type": "module",
  "scripts": {
    "build": "tsc",
    "start": "tsx wsaa-login.ts"
  },
  "dependencies": {
    "node-forge": "^1.3.1",
    "soap": "^1.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/node-forge": "^1.3.11",
    "tsx": "^4.7.0",
    "typescript": "^5.4.0"
  }
}
```

- [ ] **Step 2: Write `tsconfig.json`**:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "moduleResolution": "Bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "noEmit": true
  },
  "include": ["*.ts"]
}
```

- [ ] **Step 3: Write `wsaa-login.ts`**:

```typescript
/**
 * WSAA login — TypeScript example.
 * Usage: npx tsx wsaa-login.ts --cert cert.crt --key key.key --service wsfe [--env homo|prod]
 */
import { readFileSync } from "node:fs";
import { parseArgs } from "node:util";
import forge from "node-forge";
import * as soap from "soap";

const WSAA_HOMO = "https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl";
const WSAA_PROD = "https://wsaa.afip.gov.ar/ws/services/LoginCms?wsdl";

function buildTra(service: string): string {
  const now = Math.floor(Date.now() / 1000);
  const fmt = (ts: number): string => {
    const d = new Date(ts * 1000);
    const off = "-03:00";
    const pad = (n: number) => String(n).padStart(2, "0");
    return (
      `${d.getUTCFullYear()}-${pad(d.getUTCMonth() + 1)}-${pad(d.getUTCDate())}` +
      `T${pad(d.getUTCHours() - 3)}:${pad(d.getUTCMinutes())}:${pad(d.getUTCSeconds())}${off}`
    );
  };
  return `<?xml version="1.0" encoding="UTF-8"?>
<loginTicketRequest version="1.0">
  <header>
    <uniqueId>${now}</uniqueId>
    <generationTime>${fmt(now - 60)}</generationTime>
    <expirationTime>${fmt(now + 600)}</expirationTime>
  </header>
  <service>${service}</service>
</loginTicketRequest>`;
}

function signCms(tra: string, certPem: string, keyPem: string): string {
  const cert = forge.pki.certificateFromPem(certPem);
  const key = forge.pki.privateKeyFromPem(keyPem);
  const p7 = forge.pkcs7.createSignedData();
  p7.content = forge.util.createBuffer(tra, "utf8");
  p7.addCertificate(cert);
  p7.addSigner({
    key,
    certificate: cert,
    digestAlgorithm: forge.pki.oids.sha256,
  });
  p7.sign({ detached: false });
  const der = forge.asn1.toDer(p7.toAsn1()).getBytes();
  return forge.util.encode64(der);
}

async function main(): Promise<void> {
  const { values } = parseArgs({
    options: {
      cert: { type: "string" },
      key: { type: "string" },
      service: { type: "string", default: "wsfe" },
      env: { type: "string", default: "homo" },
    },
  });
  if (!values.cert || !values.key) {
    throw new Error("--cert and --key are required");
  }

  const certPem = readFileSync(values.cert, "utf8");
  const keyPem = readFileSync(values.key, "utf8");
  const tra = buildTra(values.service!);
  const cmsB64 = signCms(tra, certPem, keyPem);

  const wsdl = values.env === "prod" ? WSAA_PROD : WSAA_HOMO;
  const client = await soap.createClientAsync(wsdl);
  const [result] = await client.loginCmsAsync({ in0: cmsB64 });
  process.stdout.write((result as { loginCmsReturn: string }).loginCmsReturn);
}

main().catch((e: unknown) => {
  console.error(e);
  process.exit(1);
});
```

- [ ] **Step 4: Write `README.md`**:

````markdown
# WSAA login — Node/TS example

```bash
npm install
npx tsx wsaa-login.ts --cert ../../../path/to/cert.crt --key ../../../path/to/key.key --service wsfe --env homo > ta-wsfe.xml
```
````

- [ ] **Step 5: Type-check (no install required if you have npm)**

Run: `cd .claude/skills/afip-arca-wsaa/examples/node && npm install && npx tsc --noEmit`
Expected: exit 0, no errors.

- [ ] **Step 6: Commit (do NOT commit `node_modules/`)**

```bash
git add .claude/skills/afip-arca-wsaa/examples/node/package.json .claude/skills/afip-arca-wsaa/examples/node/tsconfig.json .claude/skills/afip-arca-wsaa/examples/node/wsaa-login.ts .claude/skills/afip-arca-wsaa/examples/node/README.md
git commit -m "feat(skill-wsaa): Node/TypeScript example for TA acquisition"
```

### Task 17: WSAA PHP example

**Files:**
- Create: `.claude/skills/afip-arca-wsaa/examples/php/wsaa_login.php`
- Create: `.claude/skills/afip-arca-wsaa/examples/php/README.md`

- [ ] **Step 1: Write `wsaa_login.php`**:

```php
<?php
/**
 * WSAA login — PHP example using SoapClient + openssl_pkcs7_sign.
 * Usage: php wsaa_login.php --cert=cert.crt --key=key.key --service=wsfe [--env=homo|prod]
 */
declare(strict_types=1);

const WSAA_HOMO = 'https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl';
const WSAA_PROD = 'https://wsaa.afip.gov.ar/ws/services/LoginCms?wsdl';

function build_tra(string $service): string {
    $now = time();
    $gen = gmdate('Y-m-d\TH:i:s', $now - 60) . '-03:00';
    $exp = gmdate('Y-m-d\TH:i:s', $now + 600) . '-03:00';
    return <<<XML
<?xml version="1.0" encoding="UTF-8"?>
<loginTicketRequest version="1.0">
  <header>
    <uniqueId>{$now}</uniqueId>
    <generationTime>{$gen}</generationTime>
    <expirationTime>{$exp}</expirationTime>
  </header>
  <service>{$service}</service>
</loginTicketRequest>
XML;
}

function sign_cms(string $tra, string $cert_path, string $key_path): string {
    $tmp_in = tempnam(sys_get_temp_dir(), 'tra_');
    $tmp_out = tempnam(sys_get_temp_dir(), 'cms_');
    file_put_contents($tmp_in, $tra);
    $ok = openssl_pkcs7_sign(
        $tmp_in, $tmp_out,
        'file://' . $cert_path,
        ['file://' . $key_path, ''],
        [],
        !PKCS7_DETACHED
    );
    if (!$ok) {
        throw new RuntimeException('openssl_pkcs7_sign failed: ' . openssl_error_string());
    }
    $signed = file_get_contents($tmp_out);
    unlink($tmp_in);
    unlink($tmp_out);
    // Strip MIME headers to keep the CMS bytes only, then base64
    [$headers, $body] = explode("\n\n", $signed, 2);
    return preg_replace('/\s+/', '', $body);
}

function parse_args(): array {
    $opts = getopt('', ['cert:', 'key:', 'service:', 'env::']);
    foreach (['cert', 'key', 'service'] as $k) {
        if (empty($opts[$k])) {
            fwrite(STDERR, "Missing --$k\n");
            exit(2);
        }
    }
    $opts['env'] = $opts['env'] ?? 'homo';
    return $opts;
}

$args = parse_args();
$tra = build_tra($args['service']);
$cms_b64 = sign_cms($tra, $args['cert'], $args['key']);

$wsdl = $args['env'] === 'prod' ? WSAA_PROD : WSAA_HOMO;
$client = new SoapClient($wsdl, ['soap_version' => SOAP_1_2, 'trace' => 1]);
$result = $client->loginCms(['in0' => $cms_b64]);
echo $result->loginCmsReturn;
```

- [ ] **Step 2: Write `README.md`**:

````markdown
# WSAA login — PHP example

Requires PHP 8.0+ with `openssl` and `soap` extensions.

```bash
php wsaa_login.php --cert=cert.crt --key=key.key --service=wsfe --env=homo > ta-wsfe.xml
```
````

- [ ] **Step 3: Lint**

Run: `php -l .claude/skills/afip-arca-wsaa/examples/php/wsaa_login.php`
Expected: `No syntax errors detected`.

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/afip-arca-wsaa/examples/php/
git commit -m "feat(skill-wsaa): PHP example for TA acquisition"
```

### Task 18: WSAA helper script — validate-ta.py

**Files:**
- Create: `.claude/skills/afip-arca-wsaa/scripts/validate-ta.py`

- [ ] **Step 1: Write the script**:

```python
"""
Inspect a TA.xml: print token, sign (truncated), and time until expiration.
Usage: python validate-ta.py path/to/ta.xml
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python validate-ta.py <path/to/ta.xml>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    root = ET.fromstring(path.read_bytes())
    ns = ""
    creds = root.find(f"{ns}credentials") or root.find("credentials")
    header = root.find(f"{ns}header") or root.find("header")
    if creds is None or header is None:
        print("ERROR: not a valid TA — missing <credentials> or <header>", file=sys.stderr)
        return 1
    token = creds.findtext("token", "")
    sign = creds.findtext("sign", "")
    exp = header.findtext("expirationTime", "")

    print(f"Token (first 40):  {token[:40]}…")
    print(f"Sign  (first 40):  {sign[:40]}…")
    print(f"Expiration:        {exp}")

    if exp:
        try:
            exp_dt = datetime.fromisoformat(exp)
            remaining = exp_dt - datetime.now(exp_dt.tzinfo)
            mins = int(remaining.total_seconds() // 60)
            if mins <= 0:
                print(f"Status:            ✗ EXPIRED {abs(mins)} min ago")
                return 2
            print(f"Status:            ✓ valid for {mins} more minutes")
        except ValueError:
            print(f"Status:            ⚠ could not parse expirationTime")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Lint compile**

Run: `python -m py_compile .claude/skills/afip-arca-wsaa/scripts/validate-ta.py`
Expected: exit 0.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/afip-arca-wsaa/scripts/
git commit -m "feat(skill-wsaa): validate-ta.py helper"
```

### Task 19: Code review for Phase 5 (wsaa)

- [ ] **Step 1: Tag**: `git tag phase-5-wsaa-complete`
- [ ] **Step 2: Invoke `superpowers:requesting-code-review`** scoped to `.claude/skills/afip-arca-wsaa/`. Reference spec section 7.3. Ask reviewer to specifically check the CMS signing in each language for equivalence.
- [ ] **Step 3: Address findings; commit fixes with `fix(skill-wsaa): ...`.**
- [ ] **Step 4: Re-tag if needed.**

---

## Phase 6: Skill `afip-arca-wsfev1`

### Task 20: SKILL.md + references

**Files:**
- Create: `.claude/skills/afip-arca-wsfev1/SKILL.md`
- Create: `.claude/skills/afip-arca-wsfev1/references/methods.md`
- Create: `.claude/skills/afip-arca-wsfev1/references/tipos-comprobante.md`
- Create: `.claude/skills/afip-arca-wsfev1/references/tipos-doc.md`
- Create: `.claude/skills/afip-arca-wsfev1/references/alicuotas-iva.md`
- Create: `.claude/skills/afip-arca-wsfev1/references/error-codes.md`
- Create: `.claude/skills/afip-arca-wsfev1/assets/factura.json.tmpl`

- [ ] **Step 1: Write `SKILL.md`**:

````markdown
---
name: afip-arca-wsfev1
description: Use when the user issues domestic electronic invoices in Argentina via AFIP/ARCA WSFEv1 — calling FECAESolicitar to get a CAE, querying FECompUltimoAutorizado, looking up FEParamGetTiposCbte/IVA/Doc, debugging FECAEResponse errors, or designing the request payload (factura A/B/C/M, notas de crédito/débito). Triggers: WSFEv1, FECAE, CAE, factura electrónica, FEParamGet, "comprobante", punto de venta.
---

# AFIP/ARCA WSFEv1 — Factura Electrónica (mercado interno)

The main domestic invoicing Web Service. You build a `FECAERequest`, call `FECAESolicitar`, and get back a CAE (Código de Autorización Electrónico) plus its expiration. The CAE is what makes the invoice legally valid.

## Critical gotchas

- **Numbering is per (Punto de Venta, Tipo de Comprobante).** Always call `FECompUltimoAutorizado` first to get the last authorized number, then submit `last + 1`. Submitting a gap or duplicate fails with `10016`.
- **Importes are decimals with 2 places, sent as numbers (not strings).** Some clients send "100.50" and AFIP rejects with type errors.
- **Sum of `ImpNeto + ImpIVA + ImpTrib + ImpOpEx + ImpTotConc` must equal `ImpTotal` exactly.** Rounding errors are the #1 cause of `10048`.
- **`Iva` array is required when `ImpIVA > 0`** even for monotributistas issuing factura C? No — for factura C you do NOT send Iva. Different rules per `CbteTipo`. See `references/tipos-comprobante.md`.
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

End-to-end factura B in `examples/{python,node,php,bash}/`. The Python example shows zeep, the Node uses `soap`, PHP uses native `SoapClient`, Bash uses curl + a hand-built XML envelope.

## Depends on / leads to

- Depends on: `afip-arca-wsaa` (need TA with `service=wsfe`), `afip-arca-certificates`.
- Leads to: nothing — this is the leaf service.
````

- [ ] **Step 2: Write `references/methods.md`** with mandatory sections (each ≥80 words):
  - **"FEDummy"**: no auth required; returns 3 status booleans (`AppServer`, `DbServer`, `AuthServer`).
  - **"FECAESolicitar"**: full request shape (`Auth { Token, Sign, Cuit }` + `FeCAEReq { FeCabReq, FeDetReq }`); list every required field on `FECAEDetRequest` (`Concepto`, `DocTipo`, `DocNro`, `CbteDesde`, `CbteHasta`, `CbteFch`, `ImpTotal`, `ImpTotConc`, `ImpNeto`, `ImpOpEx`, `ImpIVA`, `ImpTrib`, `MonId`, `MonCotiz`, `Iva`).
  - **"FECompUltimoAutorizado"**: input `PtoVta` + `CbteTipo`; output `CbteNro` (0 if none yet).
  - **"FECompConsultar"**: lookup an already-authorized comprobante.
  - **"FEParamGetTiposCbte / FEParamGetTiposDoc / FEParamGetTiposIva / FEParamGetTiposMonedas / FEParamGetPtosVenta"**: enums published by AFIP. Cache locally (24h TTL).
  - **"FECAEARegInformativo"**: bulk-register comprobantes whose CAE was generated outside (e.g. controlador fiscal).

- [ ] **Step 3: Write `references/tipos-comprobante.md`** as a Markdown table with columns: Código, Descripción, Cuándo se usa, Iva field requerido. Include at minimum: 1 (Factura A), 6 (Factura B), 11 (Factura C), 51 (Factura M), 2/3 (Nota de Débito/Crédito A), 7/8 (NDé/NCr B), 12/13 (NDé/NCr C), 201/206/211 (FCE MiPyMEs A/B/C). Note that codes evolve — engineer should sanity-check against `FEParamGetTiposCbte` at runtime.

- [ ] **Step 4: Write `references/tipos-doc.md`** as a table with the AFIP DocTipo enum: 80 (CUIT), 86 (CUIL), 96 (DNI), 99 (Consumidor Final / "sin identificar"), plus passport (94) and CDI (87).

- [ ] **Step 5: Write `references/alicuotas-iva.md`** as a table: 3 (0%), 4 (10.5%), 5 (21%), 6 (27%), 8 (5%), 9 (2.5%). Include a worked example computing `ImpIVA` from `ImpNeto` for each.

- [ ] **Step 6: Write `references/error-codes.md`** as a table of common WSFEv1 errors. Must include: 10015 (CbteTipo no autorizado), 10016 (numero fuera de secuencia), 10017 (fecha fuera de rango), 10048 (suma de importes no coincide con ImpTotal), 10054 (DocTipo no válido para CbteTipo), 1001 (CUIT no autorizado en este servicio), 600/601 (errores de WSAA — TA expirado/inválido).

- [ ] **Step 7: Write `assets/factura.json.tmpl`** as a JSON skeleton:

```json
{
  "Auth": {
    "Token": "{{TA_TOKEN}}",
    "Sign": "{{TA_SIGN}}",
    "Cuit": "{{CUIT_EMISOR}}"
  },
  "FeCAEReq": {
    "FeCabReq": {
      "CantReg": 1,
      "PtoVta": {{PTO_VTA}},
      "CbteTipo": {{CBTE_TIPO}}
    },
    "FeDetReq": {
      "FECAEDetRequest": [{
        "Concepto": 1,
        "DocTipo": 80,
        "DocNro": "{{CUIT_RECEPTOR}}",
        "CbteDesde": {{CBTE_NRO}},
        "CbteHasta": {{CBTE_NRO}},
        "CbteFch": "{{YYYYMMDD}}",
        "ImpTotal": 121.00,
        "ImpTotConc": 0,
        "ImpNeto": 100.00,
        "ImpOpEx": 0,
        "ImpIVA": 21.00,
        "ImpTrib": 0,
        "MonId": "PES",
        "MonCotiz": 1,
        "Iva": [{ "Id": 5, "BaseImp": 100.00, "Importe": 21.00 }]
      }]
    }
  }
}
```

- [ ] **Step 8: Commit**

```bash
git add .claude/skills/afip-arca-wsfev1/SKILL.md .claude/skills/afip-arca-wsfev1/references/ .claude/skills/afip-arca-wsfev1/assets/
git commit -m "feat(skill-wsfev1): SKILL.md, method/type/error references, factura template"
```

### Task 21: WSFEv1 Python example

**Files:**
- Create: `.claude/skills/afip-arca-wsfev1/examples/python/wsfev1_factura.py`
- Create: `.claude/skills/afip-arca-wsfev1/examples/python/requirements.txt`
- Create: `.claude/skills/afip-arca-wsfev1/examples/python/README.md`

- [ ] **Step 1: `requirements.txt`**:

```
zeep>=4.2
```

- [ ] **Step 2: Write `wsfev1_factura.py`**:

```python
"""
WSFEv1 — issue a Factura B end-to-end.
Usage:
    python wsfev1_factura.py --ta ta-wsfe.xml --cuit 20111111112 --pto-vta 1 --neto 100.00
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from xml.etree import ElementTree as ET

from zeep import Client

WSFEV1_HOMO = "https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL"
WSFEV1_PROD = "https://servicios1.afip.gov.ar/wsfev1/service.asmx?WSDL"

CBTE_FACTURA_B = 6
ALICUOTA_21 = 5  # AFIP Iva.Id


def load_ta(path: Path) -> tuple[str, str]:
    root = ET.fromstring(path.read_bytes())
    creds = root.find("credentials")
    return creds.findtext("token"), creds.findtext("sign")


def round2(x: Decimal) -> Decimal:
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--ta", type=Path, required=True, help="TA xml from WSAA")
    p.add_argument("--cuit", required=True, help="CUIT emisor (sin guiones)")
    p.add_argument("--pto-vta", type=int, required=True)
    p.add_argument("--neto", type=Decimal, required=True, help="ImpNeto in pesos")
    p.add_argument("--env", choices=["homo", "prod"], default="homo")
    args = p.parse_args()

    token, sign = load_ta(args.ta)
    auth = {"Token": token, "Sign": sign, "Cuit": args.cuit}

    wsdl = WSFEV1_HOMO if args.env == "homo" else WSFEV1_PROD
    client = Client(wsdl=wsdl)

    # 1. last authorized
    last = client.service.FECompUltimoAutorizado(
        Auth=auth, PtoVta=args.pto_vta, CbteTipo=CBTE_FACTURA_B
    )
    next_nro = int(last.CbteNro) + 1

    # 2. compute amounts
    neto = round2(args.neto)
    iva = round2(neto * Decimal("0.21"))
    total = neto + iva

    fecha = datetime.now().strftime("%Y%m%d")

    req = {
        "FeCabReq": {"CantReg": 1, "PtoVta": args.pto_vta, "CbteTipo": CBTE_FACTURA_B},
        "FeDetReq": {"FECAEDetRequest": [{
            "Concepto": 1,
            "DocTipo": 99,
            "DocNro": 0,
            "CbteDesde": next_nro,
            "CbteHasta": next_nro,
            "CbteFch": fecha,
            "ImpTotal": float(total),
            "ImpTotConc": 0,
            "ImpNeto": float(neto),
            "ImpOpEx": 0,
            "ImpIVA": float(iva),
            "ImpTrib": 0,
            "MonId": "PES",
            "MonCotiz": 1,
            "Iva": {"AlicIva": [{"Id": ALICUOTA_21, "BaseImp": float(neto), "Importe": float(iva)}]},
        }]},
    }

    resp = client.service.FECAESolicitar(Auth=auth, FeCAEReq=req)
    if resp.FeCabResp.Resultado != "A":
        print(f"REJECTED: {resp.FeCabResp.Resultado}", file=sys.stderr)
        for d in resp.FeDetResp.FECAEDetResponse or []:
            for o in (d.Observaciones.Obs if d.Observaciones else []) or []:
                print(f"  Obs {o.Code}: {o.Msg}", file=sys.stderr)
        return 1

    det = resp.FeDetResp.FECAEDetResponse[0]
    print(f"CAE:        {det.CAE}")
    print(f"CAEFchVto:  {det.CAEFchVto}")
    print(f"CbteNro:    {det.CbteDesde}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 3: Write `README.md`**:

````markdown
# WSFEv1 Factura B — Python example

Prereq: a valid TA from `afip-arca-wsaa` (saved as `ta-wsfe.xml`).

```bash
pip install -r requirements.txt
python wsfev1_factura.py --ta ta-wsfe.xml --cuit 20111111112 --pto-vta 1 --neto 100.00 --env homo
```
````

- [ ] **Step 4: Compile check**

Run: `python -m py_compile .claude/skills/afip-arca-wsfev1/examples/python/wsfev1_factura.py`
Expected: exit 0.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/afip-arca-wsfev1/examples/python/
git commit -m "feat(skill-wsfev1): Python example issuing Factura B end-to-end"
```

### Task 22: WSFEv1 Node, PHP, Bash examples

**Files:**
- Create: `.claude/skills/afip-arca-wsfev1/examples/node/{package.json, tsconfig.json, wsfev1-factura.ts, README.md}`
- Create: `.claude/skills/afip-arca-wsfev1/examples/php/{wsfev1_factura.php, README.md}`
- Create: `.claude/skills/afip-arca-wsfev1/examples/bash/{wsfev1-factura.sh, soap-envelope.xml.tmpl, README.md}`

- [ ] **Step 1: Node `package.json`** (same shape as WSAA Node, but only `soap` dep):

```json
{
  "name": "afip-arca-wsfev1-example",
  "private": true,
  "type": "module",
  "scripts": { "build": "tsc", "start": "tsx wsfev1-factura.ts" },
  "dependencies": { "soap": "^1.0.0" },
  "devDependencies": { "@types/node": "^20.0.0", "tsx": "^4.7.0", "typescript": "^5.4.0" }
}
```

- [ ] **Step 2: Node `tsconfig.json`** (identical to WSAA Node tsconfig — copy from Task 16, Step 2).

- [ ] **Step 3: Node `wsfev1-factura.ts`**:

```typescript
/**
 * WSFEv1 — issue a Factura B end-to-end.
 * Usage: npx tsx wsfev1-factura.ts --ta ta-wsfe.xml --cuit 20111111112 --pto-vta 1 --neto 100.00 [--env homo|prod]
 */
import { readFileSync } from "node:fs";
import { parseArgs } from "node:util";
import { DOMParser } from "@xmldom/xmldom";
import * as soap from "soap";

const HOMO = "https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL";
const PROD = "https://servicios1.afip.gov.ar/wsfev1/service.asmx?WSDL";
const CBTE_FACTURA_B = 6;
const ALICUOTA_21 = 5;

function loadTa(path: string): { token: string; sign: string } {
  const xml = readFileSync(path, "utf8");
  const doc = new DOMParser().parseFromString(xml, "text/xml");
  const get = (tag: string): string =>
    doc.getElementsByTagName(tag)[0]?.textContent ?? "";
  return { token: get("token"), sign: get("sign") };
}

function round2(n: number): number {
  return Math.round(n * 100) / 100;
}

async function main(): Promise<void> {
  const { values } = parseArgs({
    options: {
      ta: { type: "string" },
      cuit: { type: "string" },
      "pto-vta": { type: "string" },
      neto: { type: "string" },
      env: { type: "string", default: "homo" },
    },
  });
  const ta = loadTa(values.ta!);
  const auth = { Token: ta.token, Sign: ta.sign, Cuit: values.cuit! };
  const ptoVta = Number(values["pto-vta"]);
  const neto = round2(Number(values.neto));
  const iva = round2(neto * 0.21);
  const total = round2(neto + iva);

  const wsdl = values.env === "prod" ? PROD : HOMO;
  const client = await soap.createClientAsync(wsdl);

  const [lastResp] = await client.FECompUltimoAutorizadoAsync({
    Auth: auth, PtoVta: ptoVta, CbteTipo: CBTE_FACTURA_B,
  });
  const nextNro = Number((lastResp as { FECompUltimoAutorizadoResult: { CbteNro: number } })
    .FECompUltimoAutorizadoResult.CbteNro) + 1;

  const fecha = new Date().toISOString().slice(0, 10).replace(/-/g, "");
  const req = {
    FeCabReq: { CantReg: 1, PtoVta: ptoVta, CbteTipo: CBTE_FACTURA_B },
    FeDetReq: { FECAEDetRequest: [{
      Concepto: 1, DocTipo: 99, DocNro: 0,
      CbteDesde: nextNro, CbteHasta: nextNro, CbteFch: fecha,
      ImpTotal: total, ImpTotConc: 0, ImpNeto: neto,
      ImpOpEx: 0, ImpIVA: iva, ImpTrib: 0,
      MonId: "PES", MonCotiz: 1,
      Iva: { AlicIva: [{ Id: ALICUOTA_21, BaseImp: neto, Importe: iva }] },
    }]},
  };

  const [resp] = await client.FECAESolicitarAsync({ Auth: auth, FeCAEReq: req });
  console.log(JSON.stringify(resp, null, 2));
}

main().catch((e: unknown) => { console.error(e); process.exit(1); });
```

Add to `package.json` `dependencies`: `"@xmldom/xmldom": "^0.8.10"` and `devDependencies`: `"@types/xmldom": "^0.1.34"`.

- [ ] **Step 4: Node README** — same shape as WSAA's README, with the wsfev1 invocation.

- [ ] **Step 5: Type-check**

Run: `cd .claude/skills/afip-arca-wsfev1/examples/node && npm install && npx tsc --noEmit`
Expected: exit 0.

- [ ] **Step 6: PHP `wsfev1_factura.php`**:

```php
<?php
declare(strict_types=1);

const HOMO = 'https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL';
const PROD = 'https://servicios1.afip.gov.ar/wsfev1/service.asmx?WSDL';
const CBTE_FACTURA_B = 6;
const ALICUOTA_21 = 5;

function load_ta(string $path): array {
    $xml = simplexml_load_string(file_get_contents($path));
    return [
        'Token' => (string)$xml->credentials->token,
        'Sign'  => (string)$xml->credentials->sign,
    ];
}

function round2(float $n): float { return round($n, 2); }

$opts = getopt('', ['ta:', 'cuit:', 'pto-vta:', 'neto:', 'env::']);
foreach (['ta', 'cuit', 'pto-vta', 'neto'] as $k) {
    if (empty($opts[$k])) { fwrite(STDERR, "Missing --$k\n"); exit(2); }
}
$env = $opts['env'] ?? 'homo';

$ta = load_ta($opts['ta']);
$auth = ['Token' => $ta['Token'], 'Sign' => $ta['Sign'], 'Cuit' => $opts['cuit']];
$pto_vta = (int)$opts['pto-vta'];
$neto = round2((float)$opts['neto']);
$iva = round2($neto * 0.21);
$total = round2($neto + $iva);

$client = new SoapClient($env === 'prod' ? PROD : HOMO, ['soap_version' => SOAP_1_2]);

$last = $client->FECompUltimoAutorizado([
    'Auth' => $auth, 'PtoVta' => $pto_vta, 'CbteTipo' => CBTE_FACTURA_B,
]);
$next = ((int)$last->FECompUltimoAutorizadoResult->CbteNro) + 1;

$req = [
    'FeCabReq' => ['CantReg' => 1, 'PtoVta' => $pto_vta, 'CbteTipo' => CBTE_FACTURA_B],
    'FeDetReq' => ['FECAEDetRequest' => [[
        'Concepto' => 1, 'DocTipo' => 99, 'DocNro' => 0,
        'CbteDesde' => $next, 'CbteHasta' => $next, 'CbteFch' => date('Ymd'),
        'ImpTotal' => $total, 'ImpTotConc' => 0, 'ImpNeto' => $neto,
        'ImpOpEx' => 0, 'ImpIVA' => $iva, 'ImpTrib' => 0,
        'MonId' => 'PES', 'MonCotiz' => 1,
        'Iva' => ['AlicIva' => [['Id' => ALICUOTA_21, 'BaseImp' => $neto, 'Importe' => $iva]]],
    ]]],
];

$resp = $client->FECAESolicitar(['Auth' => $auth, 'FeCAEReq' => $req]);
print_r($resp);
```

Lint: `php -l .claude/skills/afip-arca-wsfev1/examples/php/wsfev1_factura.php` → expect `No syntax errors`.

- [ ] **Step 7: PHP README** — analogous to others.

- [ ] **Step 8: Bash example** — `wsfev1-factura.sh` is intentionally simpler: it only calls `FEDummy` to demonstrate the SOAP envelope shape (issuing a real factura by hand-rolled curl is fragile and not how anyone does it in production). Write:

```bash
#!/usr/bin/env bash
# WSFEv1 Bash example — calls FEDummy (no auth) to verify connectivity and SOAP shape.
# For real factura issuance, use Python/Node/PHP examples in this skill's examples/.
set -euo pipefail

ENV="${1:-homo}"
URL=$([[ "$ENV" == "prod" ]] && echo "https://servicios1.afip.gov.ar/wsfev1/service.asmx" || echo "https://wswhomo.afip.gov.ar/wsfev1/service.asmx")

cat > /tmp/fedummy.xml <<'EOF'
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xmlns:xsd="http://www.w3.org/2001/XMLSchema"
               xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <FEDummy xmlns="http://ar.gov.afip.dif.FEV1/" />
  </soap:Body>
</soap:Envelope>
EOF

curl -sS -X POST "$URL" \
  -H "Content-Type: text/xml; charset=utf-8" \
  -H "SOAPAction: http://ar.gov.afip.dif.FEV1/FEDummy" \
  --data-binary @/tmp/fedummy.xml
```

Lint: `shellcheck .claude/skills/afip-arca-wsfev1/examples/bash/wsfev1-factura.sh`. chmod +x via git.

- [ ] **Step 9: Bash README** — explains it's connectivity-only, points to other languages for full factura issuance.

- [ ] **Step 10: Commit**

```bash
git add .claude/skills/afip-arca-wsfev1/examples/
git commit -m "feat(skill-wsfev1): Node/PHP/Bash examples (Bash limited to FEDummy)"
```

### Task 23: Code review for Phase 6 (wsfev1)

- [ ] **Step 1: Tag**: `git tag phase-6-wsfev1-complete`
- [ ] **Step 2: Invoke `superpowers:requesting-code-review`** scoped to `.claude/skills/afip-arca-wsfev1/`. Reference spec section 7.4. Ask reviewer to check importes math (round half up consistency across languages) and that all 4 examples agree on the request shape.
- [ ] **Step 3: Address findings; commit fixes with `fix(skill-wsfev1): ...`.**
- [ ] **Step 4: Re-tag if needed.**

---

## Phase 7: Skill `afip-arca-wsfexv1`

### Task 24: SKILL.md + references

**Files:**
- Create: `.claude/skills/afip-arca-wsfexv1/SKILL.md`
- Create: `.claude/skills/afip-arca-wsfexv1/references/{methods.md, idiomas.md, monedas.md, incoterms.md, error-codes.md}`

- [ ] **Step 1: Write `SKILL.md`**:

````markdown
---
name: afip-arca-wsfexv1
description: Use when the user issues export electronic invoices via AFIP/ARCA WSFEXv1 — calling FEXAuthorize for export comprobantes (factura E), querying FEXGetCMP, looking up monedas/incoterms/idiomas, dealing with foreign-currency invoices and destination countries. Triggers: WSFEXv1, FEXAuthorize, factura E, exportación, incoterms, FEXGetPARAM, monedas extranjeras.
---

# AFIP/ARCA WSFEXv1 — Factura Electrónica de Exportación

The export-invoice analog of WSFEv1. Different request shape (uses `Cmp` not `FECAEDetRequest`), supports foreign currency natively, and requires destination country + incoterm + idioma.

## Critical gotchas

- **Different from WSFEv1.** Don't try to reuse code.
- **Currency**: `Mon_id` from `FEXGetPARAM_MON`; `Mon_cotiz` is the conversion rate to ARS at invoice date.
- **Destino**: country code from `FEXGetPARAM_DST_pais`. Argentina (200) is invalid as destination.
- **Incoterms**: must come from `FEXGetPARAM_Incoterms` (FOB, CIF, etc.).
- **Idioma del comprobante**: 1 (Español), 2 (Inglés), 3 (Portugués) per `FEXGetPARAM_Idiomas`.
- **Endpoints**: homo `https://wswhomo.afip.gov.ar/wsfexv1/service.asmx?WSDL`, prod `https://servicios1.afip.gov.ar/wsfexv1/service.asmx?WSDL`.
- **TA service scope**: `wsfex` (not `wsfe`).

## Quick flow

1. TA from `afip-arca-wsaa` with `service=wsfex`.
2. `FEXGetLast_CMP(Pto_venta, Cbte_Tipo)` → ultimate authorized.
3. Build `Cmp` with required export fields (Dst_cmp, Idioma_cbte, Mon_id, Mon_cotiz, Incoterms, Items).
4. `FEXAuthorize(Auth, Cmp)` → returns `FEXResultAuth.Cae` + `FchVencCAE`.

References: `methods.md`, `idiomas.md`, `monedas.md`, `incoterms.md`, `error-codes.md`.

## Examples

`examples/{python,node,php}/` — issue a Factura E in USD to a US buyer. Bash skipped (export invoices are too verbose for hand-rolled curl).

## Depends on / leads to

- Depends on: `afip-arca-wsaa` (service=wsfex), `afip-arca-certificates`.
````

- [ ] **Step 2: Write `references/methods.md`** — sections for `FEXDummy`, `FEXAuthorize`, `FEXGetCMP`, `FEXGetLast_CMP`, `FEXGetLast_ID`, and the FEXGetPARAM family (one paragraph each describing input/output).

- [ ] **Step 3: Write `references/idiomas.md`** — table: 1 Español, 2 Inglés, 3 Portugués.

- [ ] **Step 4: Write `references/monedas.md`** — table of common AFIP monedas: PES, DOL, 002 (USD libre), 009 (Yen), 010 (Real), 012 (Euro), etc. Note: full list comes from `FEXGetPARAM_MON` (cache 24h).

- [ ] **Step 5: Write `references/incoterms.md`** — table from `FEXGetPARAM_Incoterms`: EXW, FCA, CPT, CIP, DAP, DPU, DDP, FAS, FOB, CFR, CIF. One sentence on responsibility split.

- [ ] **Step 6: Write `references/error-codes.md`** — table of common WSFEXv1 errors: 1500 (Pto_venta no autorizado para export), 1501 (Idioma inválido), 1502 (moneda inválida), 1503 (cotización fuera de rango), 1505 (incoterm inválido), 1510 (destino Argentina inválido), 600/601 (TA invalid).

- [ ] **Step 7: Commit**

```bash
git add .claude/skills/afip-arca-wsfexv1/SKILL.md .claude/skills/afip-arca-wsfexv1/references/
git commit -m "feat(skill-wsfexv1): SKILL.md + references"
```

### Task 25: WSFEXv1 examples (Python/Node/PHP)

**Files:**
- Create: `.claude/skills/afip-arca-wsfexv1/examples/python/{wsfexv1_factura.py, requirements.txt, README.md}`
- Create: `.claude/skills/afip-arca-wsfexv1/examples/node/{package.json, tsconfig.json, wsfexv1-factura.ts, README.md}`
- Create: `.claude/skills/afip-arca-wsfexv1/examples/php/{wsfexv1_factura.php, README.md}`

- [ ] **Step 1: Python `requirements.txt`**: `zeep>=4.2`

- [ ] **Step 2: Python `wsfexv1_factura.py`** — analogous to WSFEv1 Python example but using FEXAuthorize. Required code structure:

```python
"""
WSFEXv1 — issue a Factura E (export) to a US buyer in USD.
Usage:
    python wsfexv1_factura.py --ta ta-wsfex.xml --cuit 20111111112 --pto-vta 5 --total 1000.00 --cotiz 950.00
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET

from zeep import Client

HOMO = "https://wswhomo.afip.gov.ar/wsfexv1/service.asmx?WSDL"
PROD = "https://servicios1.afip.gov.ar/wsfexv1/service.asmx?WSDL"

CBTE_FACTURA_E = 19
DST_USA = 212  # per FEXGetPARAM_DST_pais
INCOTERM_FOB = "FOB"
IDIOMA_INGLES = 2
MON_USD = "DOL"


def load_ta(path: Path) -> tuple[str, str]:
    root = ET.fromstring(path.read_bytes())
    creds = root.find("credentials")
    return creds.findtext("token"), creds.findtext("sign")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--ta", type=Path, required=True)
    p.add_argument("--cuit", required=True)
    p.add_argument("--pto-vta", type=int, required=True)
    p.add_argument("--total", type=float, required=True, help="Total in USD")
    p.add_argument("--cotiz", type=float, required=True, help="USD→ARS rate")
    p.add_argument("--env", choices=["homo", "prod"], default="homo")
    args = p.parse_args()

    token, sign = load_ta(args.ta)
    auth = {"Token": token, "Sign": sign, "Cuit": args.cuit}
    client = Client(wsdl=HOMO if args.env == "homo" else PROD)

    last = client.service.FEXGetLast_CMP(Auth={**auth, "Pto_venta": args.pto_vta, "Cbte_Tipo": CBTE_FACTURA_E})
    next_id = int(last.FEXResult_LastCMP.Cbte_nro) + 1

    cmp = {
        "Id": next_id, "Fecha_cbte": datetime.now().strftime("%Y%m%d"),
        "Cbte_Tipo": CBTE_FACTURA_E, "Punto_vta": args.pto_vta,
        "Cbte_nro": next_id, "Tipo_expo": 1, "Permiso_existente": "N",
        "Dst_cmp": DST_USA, "Cliente": "Acme Inc.", "Cuit_pais_cliente": "50000000016",
        "Domicilio_cliente": "1 Acme Way, NY", "Id_impositivo": "FED-12345",
        "Moneda_Id": MON_USD, "Moneda_ctz": args.cotiz, "Obs_comerciales": "",
        "Imp_total": args.total, "Obs": "", "Forma_pago": "Wire transfer",
        "Incoterms": INCOTERM_FOB, "Incoterms_Ds": "Free On Board",
        "Idioma_cbte": IDIOMA_INGLES,
        "Items": {"Item": [{
            "Pro_codigo": "SKU-001", "Pro_ds": "Widget",
            "Pro_qty": 10, "Pro_umed": 7, "Pro_precio_uni": args.total / 10,
            "Pro_total_item": args.total,
        }]},
    }

    resp = client.service.FEXAuthorize(Auth=auth, Cmp=cmp)
    if resp.FEXResultAuth.Resultado != "A":
        print(f"REJECTED: {resp.FEXResultAuth.Motivos_Obs}", file=sys.stderr)
        return 1
    print(f"CAE: {resp.FEXResultAuth.Cae}")
    print(f"Vto: {resp.FEXResultAuth.Fch_venc_Cae}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Compile: `python -m py_compile`. README analogous to WSFEv1.

- [ ] **Step 3: Node example** — same structural pattern as WSFEv1 Node, but calling `FEXAuthorize` with the export request shape from Step 2 above. `package.json`/`tsconfig.json` follow Task 22 Step 1-2 templates. Type-check: `tsc --noEmit`.

- [ ] **Step 4: PHP example** — same structural pattern as WSFEv1 PHP, calling `FEXAuthorize`. Lint: `php -l`.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/afip-arca-wsfexv1/examples/
git commit -m "feat(skill-wsfexv1): Python/Node/PHP examples for Factura E"
```

### Task 26: Code review for Phase 7 (wsfexv1)

- [ ] **Step 1: Tag**: `git tag phase-7-wsfexv1-complete`
- [ ] **Step 2: Invoke `superpowers:requesting-code-review`** scoped to `.claude/skills/afip-arca-wsfexv1/`. Reference spec section 7.5.
- [ ] **Step 3: Address findings; commit `fix(skill-wsfexv1): ...`.**
- [ ] **Step 4: Re-tag if needed.**

---

## Phase 8: Skill `afip-arca-padron`

### Task 27: SKILL.md + references

**Files:**
- Create: `.claude/skills/afip-arca-padron/SKILL.md`
- Create: `.claude/skills/afip-arca-padron/references/{padron-a4.md, padron-a5.md, padron-a13.md, padron-a100.md}`

- [ ] **Step 1: Write `SKILL.md`**:

````markdown
---
name: afip-arca-padron
description: Use when the user queries the AFIP/ARCA padrón to look up CUIT/CUIL data — getPersona, padrón A4 (datos básicos), A5 (con domicilio), A13 (impositivos completos), A100 (constancia inscripción pública). Triggers: padrón, getPersona, consultar CUIT, constancia de inscripción, A4/A5/A13/A100, persona física vs jurídica.
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
2. Call `getPersona_v2({ token, sign, cuitRepresentada, idPersona })`.
3. Parse `personaReturn.persona` for the data.

## Examples

`examples/{python,node,php}/` show A4 lookups. A5/A13 differ only by endpoint and response fields.

## Depends on / leads to

- A4/A5/A13: depends on `afip-arca-wsaa` and `afip-arca-certificates`.
- A100: standalone (no auth).
````

- [ ] **Step 2: Write `references/padron-a4.md`** with sections: Endpoint URLs (homo/prod), método principal `getPersona_v2` con request fields, response shape, common errores (CUIT no existe, no autorizado).

- [ ] **Step 3: Write `references/padron-a5.md`** — same as A4 but with domicilio fields enumerated in the response.

- [ ] **Step 4: Write `references/padron-a13.md`** — same as A5 plus impuestos array (Id, Descripción, periodo, estado).

- [ ] **Step 5: Write `references/padron-a100.md`** — public service, no auth, output shape, link to AFIP "Constancia" page.

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/afip-arca-padron/SKILL.md .claude/skills/afip-arca-padron/references/
git commit -m "feat(skill-padron): SKILL.md + references for A4/A5/A13/A100"
```

### Task 28: Padrón A4 examples (Python/Node/PHP)

**Files:**
- Create: `.claude/skills/afip-arca-padron/examples/python/{padron_a4.py, requirements.txt, README.md}`
- Create: `.claude/skills/afip-arca-padron/examples/node/{package.json, tsconfig.json, padron-a4.ts, README.md}`
- Create: `.claude/skills/afip-arca-padron/examples/php/{padron_a4.php, README.md}`

- [ ] **Step 1: Python `padron_a4.py`**:

```python
"""
Padrón A4 — lookup a CUIT.
Usage: python padron_a4.py --ta ta-padron.xml --cuit-rep 20111111112 --cuit 30500001735
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

from zeep import Client

HOMO = "https://awshomo.afip.gov.ar/sr-padron/webservices/personaServiceA4?WSDL"
PROD = "https://aws.afip.gov.ar/sr-padron/webservices/personaServiceA4?WSDL"


def load_ta(path: Path) -> tuple[str, str]:
    root = ET.fromstring(path.read_bytes())
    creds = root.find("credentials")
    return creds.findtext("token"), creds.findtext("sign")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--ta", type=Path, required=True)
    p.add_argument("--cuit-rep", required=True, help="CUIT que ejecuta la consulta")
    p.add_argument("--cuit", required=True, help="CUIT a consultar")
    p.add_argument("--env", choices=["homo", "prod"], default="homo")
    args = p.parse_args()

    token, sign = load_ta(args.ta)
    client = Client(wsdl=HOMO if args.env == "homo" else PROD)

    resp = client.service.getPersona(
        token=token, sign=sign,
        cuitRepresentada=int(args.cuit_rep), idPersona=int(args.cuit),
    )
    if resp.errorReturn and resp.errorReturn.error:
        for e in resp.errorReturn.error:
            print(f"ERROR {e.code}: {e.descripcion}", file=sys.stderr)
        return 1
    persona = resp.personaReturn.persona
    print(f"Razón social: {persona.razonSocial or persona.nombre} {persona.apellido or ''}")
    print(f"Tipo:         {persona.tipoPersona}")
    print(f"Estado:       {persona.estadoClave}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

`requirements.txt`: `zeep>=4.2`. README analogous.

- [ ] **Step 2: Node `padron-a4.ts`** — analogous, using `soap` package. `package.json` + `tsconfig.json` follow Task 22 Step 1-2 templates with only `soap` + `@xmldom/xmldom` deps.

- [ ] **Step 3: PHP `padron_a4.php`** — analogous, using SoapClient.

- [ ] **Step 4: Lint each (`py_compile`, `tsc --noEmit`, `php -l`).**

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/afip-arca-padron/examples/
git commit -m "feat(skill-padron): Python/Node/PHP examples for A4 lookup"
```

### Task 29: Code review for Phase 8 (padron)

- [ ] **Step 1: Tag**: `git tag phase-8-padron-complete`
- [ ] **Step 2: Invoke `superpowers:requesting-code-review`** scoped to `.claude/skills/afip-arca-padron/`. Reference spec section 7.6.
- [ ] **Step 3: Address findings; commit `fix(skill-padron): ...`.**
- [ ] **Step 4: Re-tag if needed.**

---

## Phase 9: Skill `afip-arca-debugging`

### Task 30: SKILL.md + references + script

**Files:**
- Create: `.claude/skills/afip-arca-debugging/SKILL.md`
- Create: `.claude/skills/afip-arca-debugging/references/{homologacion-vs-prod.md, fedummy-checks.md, soapui-setup.md, common-errors-flowchart.md}`
- Create: `.claude/skills/afip-arca-debugging/scripts/test-fedummy.sh`

- [ ] **Step 1: Write `SKILL.md`**:

````markdown
---
name: afip-arca-debugging
description: Use when something is broken in an AFIP/ARCA integration — SOAP fault, TLS handshake error, "no anda mi cliente AFIP", FEDummy returning DOWN, mixing homologación vs producción endpoints, or wanting to set up SoapUI to inspect requests. Triggers: AFIP error, SOAP fault, FEDummy, homologación, sandbox, SoapUI, TLS afip, "no responde".
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
- `references/fedummy-checks.md` — how to call FEDummy for every service.
- `references/soapui-setup.md` — load WSDL + configure cert in SoapUI.
- `references/common-errors-flowchart.md` — flowchart for the most-asked errors.

## Tools

`scripts/test-fedummy.sh` — pings the dummy method of WSFEv1, WSFEXv1, and WSAA. No cert required (most dummies are public).
````

- [ ] **Step 2: Write `references/homologacion-vs-prod.md`** as a table covering every service this repo supports:

| Servicio | Homologación | Producción |
|---|---|---|
| WSAA | `https://wsaahomo.afip.gov.ar/ws/services/LoginCms` | `https://wsaa.afip.gov.ar/ws/services/LoginCms` |
| WSFEv1 | `https://wswhomo.afip.gov.ar/wsfev1/service.asmx` | `https://servicios1.afip.gov.ar/wsfev1/service.asmx` |
| WSFEXv1 | `https://wswhomo.afip.gov.ar/wsfexv1/service.asmx` | `https://servicios1.afip.gov.ar/wsfexv1/service.asmx` |
| Padrón A4 | `https://awshomo.afip.gov.ar/sr-padron/webservices/personaServiceA4` | `https://aws.afip.gov.ar/sr-padron/webservices/personaServiceA4` |
| Padrón A5 | `https://awshomo.afip.gov.ar/sr-padron/webservices/personaServiceA5` | `https://aws.afip.gov.ar/sr-padron/webservices/personaServiceA5` |
| Padrón A13 | `https://awshomo.afip.gov.ar/sr-padron/webservices/personaServiceA13` | `https://aws.afip.gov.ar/sr-padron/webservices/personaServiceA13` |

Add a paragraph below the table noting that mixing envs (e.g., homo cert against prod URL) returns `cms.bad_audience`.

- [ ] **Step 3: Write `references/fedummy-checks.md`** with the SOAP envelope for each service's dummy method (FEDummy / FEXDummy / WSAA dummy if available) and how to read the 3 booleans `AppServer`, `DbServer`, `AuthServer`.

- [ ] **Step 4: Write `references/soapui-setup.md`** — step-by-step: install SoapUI Open Source, File → New SOAP Project → paste WSDL URL, Project → Show Properties → "WSS Configuration" → Keystore → load .p12, then Test Request → set "Outgoing WSS" to the keystore alias.

- [ ] **Step 5: Write `references/common-errors-flowchart.md`** — a Markdown ASCII flowchart starting from "AFIP request failed" branching on (TLS error / 401 / SOAP fault / hang) → likely cause → fix.

- [ ] **Step 6: Write `scripts/test-fedummy.sh`**:

```bash
#!/usr/bin/env bash
# Smoke-test AFIP services by calling their dummy methods.
# Usage: ./test-fedummy.sh [homo|prod]
set -euo pipefail

ENV="${1:-homo}"

if [[ "$ENV" == "prod" ]]; then
  WSFE="https://servicios1.afip.gov.ar/wsfev1/service.asmx"
  WSFEX="https://servicios1.afip.gov.ar/wsfexv1/service.asmx"
else
  WSFE="https://wswhomo.afip.gov.ar/wsfev1/service.asmx"
  WSFEX="https://wswhomo.afip.gov.ar/wsfexv1/service.asmx"
fi

call_dummy() {
  local name="$1"; local url="$2"; local soapaction="$3"; local body="$4"
  echo "▶ $name → $url"
  if curl -sS -m 10 -X POST "$url" \
      -H "Content-Type: text/xml; charset=utf-8" \
      -H "SOAPAction: $soapaction" \
      --data-binary "$body" | grep -E "AppServer|DbServer|AuthServer" || true; then
    echo "✓ $name responded"
  else
    echo "✗ $name no response"
  fi
  echo
}

call_dummy "WSFEv1 FEDummy" "$WSFE" "http://ar.gov.afip.dif.FEV1/FEDummy" \
  '<?xml version="1.0"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><FEDummy xmlns="http://ar.gov.afip.dif.FEV1/"/></soap:Body></soap:Envelope>'

call_dummy "WSFEXv1 FEXDummy" "$WSFEX" "http://ar.gov.afip.dif.fex/FEXDummy" \
  '<?xml version="1.0"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><FEXDummy xmlns="http://ar.gov.afip.dif.fex/"/></soap:Body></soap:Envelope>'
```

Lint: `shellcheck`. chmod +x via git.

- [ ] **Step 7: Commit**

```bash
git add .claude/skills/afip-arca-debugging/
git commit -m "feat(skill-debugging): SKILL.md, references, test-fedummy.sh"
```

### Task 31: Code review for Phase 9 (debugging)

- [ ] **Step 1: Tag**: `git tag phase-9-debugging-complete`
- [ ] **Step 2: Invoke `superpowers:requesting-code-review`** scoped to `.claude/skills/afip-arca-debugging/`. Reference spec section 7.7.
- [ ] **Step 3: Address findings; commit `fix(skill-debugging): ...`.**
- [ ] **Step 4: Re-tag if needed.**

---

## Phase 10: CI workflows

### Task 32: `refresh-docs.yml` (improved from prototype)

**Files:**
- Create: `.github/workflows/refresh-docs.yml`

- [ ] **Step 1: Write the workflow**:

```yaml
name: Refresh AFIP docs

on:
  schedule:
    # Sundays 06:00 UTC (03:00 ART)
    - cron: "0 6 * * 0"
  workflow_dispatch: {}

permissions:
  contents: write
  pull-requests: write

concurrency:
  group: refresh-docs
  cancel-in-progress: false

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
          cache-dependency-path: scraper/requirements.txt

      - name: Install deps
        run: pip install -r scraper/requirements.txt

      - name: Run scraper
        working-directory: scraper
        run: python scrape.py

      - name: Compute diff stats
        id: stats
        run: |
          ADDED=$(git status --porcelain docs | grep -c '^??' || true)
          MOD=$(git status --porcelain docs | grep -c '^ M' || true)
          DEL=$(git status --porcelain docs | grep -c '^ D' || true)
          {
            echo "added=$ADDED"
            echo "modified=$MOD"
            echo "deleted=$DEL"
          } >> "$GITHUB_OUTPUT"

      - name: Open PR if changes
        uses: peter-evans/create-pull-request@v6
        with:
          commit-message: "docs: weekly auto-refresh"
          title: "chore(docs): weekly AFIP docs refresh"
          body: |
            Auto-generated by `.github/workflows/refresh-docs.yml`.

            **Pages added:** ${{ steps.stats.outputs.added }}
            **Pages modified:** ${{ steps.stats.outputs.modified }}
            **Pages deleted:** ${{ steps.stats.outputs.deleted }}

            Review the diff to spot meaningful AFIP doc changes.
          branch: auto/refresh-docs
          delete-branch: true
          add-paths: |
            docs/**
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/refresh-docs.yml
git commit -m "ci: refresh-docs workflow with concurrency + diff stats in PR body"
```

### Task 33: `ci.yml` — lint scraper, examples, skills

**Files:**
- Create: `.github/workflows/ci.yml`

- [ ] **Step 1: Write the workflow**:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  scraper-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
          cache-dependency-path: scraper/requirements.txt
      - run: pip install -r scraper/requirements.txt
      - name: Ruff
        run: ruff check scraper/
      - name: Pytest
        working-directory: scraper
        run: python -m pytest -v

  examples-python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - name: Compile every example .py and script .py
        run: |
          fail=0
          for f in $(find .claude/skills -path '*/examples/python/*.py' -o -path '*/scripts/*.py'); do
            echo "→ $f"
            python -m py_compile "$f" || fail=1
          done
          exit $fail

  examples-node:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "20" }
      - name: Install + tsc --noEmit per node example dir
        run: |
          fail=0
          for d in $(find .claude/skills -type d -path '*/examples/node'); do
            echo "→ $d"
            (cd "$d" && npm install --silent && npx tsc --noEmit) || fail=1
          done
          exit $fail

  examples-php:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with: { php-version: "8.2" }
      - name: php -l on every example .php
        run: |
          fail=0
          for f in $(find .claude/skills -path '*/examples/php/*.php'); do
            echo "→ $f"
            php -l "$f" || fail=1
          done
          exit $fail

  examples-bash:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install shellcheck
        run: sudo apt-get update && sudo apt-get install -y shellcheck
      - name: shellcheck every .sh under skills
        run: |
          fail=0
          for f in $(find .claude/skills -name '*.sh'); do
            echo "→ $f"
            shellcheck "$f" || fail=1
          done
          exit $fail

  skill-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install PyYAML
      - name: Verify SKILL.md frontmatter
        run: python .github/scripts/verify_skill_frontmatter.py
```

- [ ] **Step 2: Write `.github/scripts/verify_skill_frontmatter.py`**:

```python
"""Fail CI if any SKILL.md is missing required frontmatter or has too-short description."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2] / ".claude" / "skills"
REQUIRED = {"name", "description"}
MIN_DESC_LEN = 60


def main() -> int:
    failures: list[str] = []
    for skill_md in ROOT.glob("*/SKILL.md"):
        text = skill_md.read_text(encoding="utf-8")
        if not text.startswith("---"):
            failures.append(f"{skill_md}: missing frontmatter delimiter")
            continue
        try:
            _, fm, _ = text.split("---", 2)
        except ValueError:
            failures.append(f"{skill_md}: malformed frontmatter")
            continue
        data = yaml.safe_load(fm) or {}
        missing = REQUIRED - set(data)
        if missing:
            failures.append(f"{skill_md}: missing fields {sorted(missing)}")
        desc = data.get("description", "")
        if len(desc) < MIN_DESC_LEN:
            failures.append(f"{skill_md}: description too short ({len(desc)} chars, need ≥{MIN_DESC_LEN})")

    if failures:
        for f in failures:
            print(f"✗ {f}", file=sys.stderr)
        return 1
    print(f"✓ All {len(list(ROOT.glob('*/SKILL.md')))} SKILL.md files OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 3: Test locally**

Run: `python .github/scripts/verify_skill_frontmatter.py`
Expected: `✓ All 7 SKILL.md files OK`.

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/ci.yml .github/scripts/verify_skill_frontmatter.py
git commit -m "ci: lint scraper, examples (4 langs), and SKILL.md frontmatter"
```

### Task 34: Code review for Phase 10 (CI)

- [ ] **Step 1: Tag**: `git tag phase-10-ci-complete`
- [ ] **Step 2: Invoke `superpowers:requesting-code-review`** scoped to `.github/`. Reference spec section 5.6. Ask reviewer to verify the workflow YAML actually runs the right commands and that `npm install` per-example doesn't cache-thrash.
- [ ] **Step 3: Address findings; commit `fix(ci): ...`.**
- [ ] **Step 4: Re-tag if needed.**

---

## Phase 11: Final README + first scrape

### Task 35: Replace placeholder README with full version

**Files:**
- Modify: `README.md` (full rewrite)

- [ ] **Step 1: Write the new `README.md`**:

````markdown
# afip-arca-ws

Suite de **Claude Code skills** para integraciones con AFIP/ARCA Web Services + mirror Markdown de la documentación oficial de <https://www.afip.gob.ar/ws/>, versionado y actualizado semanalmente.

## ¿Qué incluye?

### 7 skills bajo `.claude/skills/`

| Skill | Para qué |
|---|---|
| `afip-arca-overview` | Router — orienta a la skill específica según la tarea |
| `afip-arca-certificates` | CSR, .crt/.key/.p12, AR Clave Fiscal, renovación |
| `afip-arca-wsaa` | TRA, firma CMS, loginCms, caching del TA |
| `afip-arca-wsfev1` | Factura electrónica mercado interno (CAE) |
| `afip-arca-wsfexv1` | Factura electrónica de exportación |
| `afip-arca-padron` | Padrón A4/A5/A13/A100 (lookup CUIT) |
| `afip-arca-debugging` | FEDummy, SoapUI, errores comunes, homo vs prod |

Cada skill tiene `SKILL.md` (entry point), `references/` (cargados a demanda por Claude), `examples/{python,node,php,bash}/` (código completo), `scripts/` (helpers ejecutables) y `assets/` (plantillas).

### `docs/`

Mirror Markdown de la documentación oficial. Auto-generado por `scraper/`. Versionado para detectar cambios semanales en AFIP.

### `scraper/`

Crawler Python (httpx + selectolax + markdownify) que convierte el portal de AFIP a Markdown limpio con frontmatter.

### CI

- `.github/workflows/refresh-docs.yml` — re-scrape semanal con PR automático.
- `.github/workflows/ci.yml` — lintea scraper, ejemplos en 4 lenguajes, frontmatter de SKILL.md.

## Instalación

### Opción A — Symlinkear todas las skills al proyecto consumidor

```bash
git clone https://github.com/AlvaFG/afip-arca-ws.git
cd mi-proyecto
mkdir -p .claude/skills
ln -s "$(pwd)/../afip-arca-ws/.claude/skills"/* .claude/skills/
```

### Opción B — Solo las skills que necesitás

```bash
ln -s ../../afip-arca-ws/.claude/skills/afip-arca-{overview,wsaa,wsfev1} .claude/skills/
```

### Opción C — Como submodule

```bash
git submodule add https://github.com/AlvaFG/afip-arca-ws.git vendor/afip-arca-ws
ln -s "$(pwd)/vendor/afip-arca-ws/.claude/skills"/* .claude/skills/
```

## Uso desde Claude Code

Una vez instaladas, las skills se activan automáticamente cuando Claude detecta menciones a AFIP/ARCA/WSAA/WSFE/factura electrónica. La skill `afip-arca-overview` actúa como router y te lleva a la específica.

Ejemplo:

> "Necesito firmar un TRA en Python para autenticarme contra WSFEv1"

Claude → activa `afip-arca-overview` → ve "TRA" + "WSFEv1" → invoca `afip-arca-wsaa` → lee `references/tra-flow.md` y `examples/python/wsaa_login.py` → genera código adaptado.

## Refrescar docs manualmente

```bash
cd scraper
pip install -r requirements.txt
python scrape.py
```

Opciones:
- `--max-pages N` — límite (default 500)
- `--url URL` — scrape una sola página

O forzar el workflow: `gh workflow run refresh-docs.yml`.

## Contribuir

PRs welcome. Para agregar un servicio nuevo (ej. WSCT, WSMTXCA):

1. Crear `.claude/skills/afip-arca-<servicio>/` siguiendo la estructura común.
2. Añadir referencia en `afip-arca-overview/SKILL.md` (decision tree).
3. CI verificará lint + frontmatter.

## Licencia

Código: **MIT**. Contenido de `docs/`: propiedad de AFIP/ARCA, reproducido como mirror funcional.
````

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: full README with install, usage, contribute sections"
```

### Task 36: Run scraper to populate `docs/` (optional pre-push)

**Files:**
- Will create: `docs/**/*.md`, `docs/README.md`, `docs/_meta.json`, `docs/_assets-index.md`

- [ ] **Step 1: Run scraper with sane page limit**

Run:
```bash
cd /c/Users/alvar/Downloads/files/afip-arca-ws/scraper
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
python scrape.py --max-pages 200
```
Expected: ≥30 pages scraped across the 4 top sections; `../docs/README.md` created.

- [ ] **Step 2: Spot-check output**

Verify a few pages exist and are well-formed:
```bash
ls /c/Users/alvar/Downloads/files/afip-arca-ws/docs/programadores/ | head -10
head -20 /c/Users/alvar/Downloads/files/afip-arca-ws/docs/README.md
cat /c/Users/alvar/Downloads/files/afip-arca-ws/docs/_meta.json
```

- [ ] **Step 3: Commit the docs**

```bash
cd /c/Users/alvar/Downloads/files/afip-arca-ws
git add docs/
git commit -m "docs: initial AFIP/ARCA docs scrape (seed)"
```

If AFIP is unreachable or scraping fails: skip this task. The scheduled workflow will populate `docs/` on its first run.

### Task 37: Final code review (full repo)

- [ ] **Step 1: Tag**: `git tag phase-11-pre-push`
- [ ] **Step 2: Invoke `superpowers:requesting-code-review`** scoped to the entire repo (no path filter). Provide the **spec** (`docs/superpowers/specs/2026-05-02-afip-arca-ws-skill-design.md`) as the requirements baseline. Ask reviewer to:
  - Verify every spec section has corresponding implementation.
  - Check for cross-skill consistency (description style, file layout uniformity).
  - Look for accidentally committed secrets.
  - Verify success criteria C1-C5 from spec section 4 are achievable.
- [ ] **Step 3: Address findings; commit fixes.**
- [ ] **Step 4: Re-tag if needed.**

---

## Phase 12: Push to GitHub

### Task 38: Create GitHub repo and push

- [ ] **Step 1: Verify gh auth**

Run: `gh auth status`
Expected: `Logged in to github.com account AlvaFG`.

- [ ] **Step 2: Create the repo (public)**

Run:
```bash
gh repo create AlvaFG/afip-arca-ws \
  --public \
  --description "Suite de Claude Code skills para integraciones con AFIP/ARCA Web Services (WSAA, WSFEv1, WSFEXv1, padrones, certificados, debugging) — docs scrapeados + ejemplos en Python/Node/PHP/Bash"
```
Expected: prints the new repo URL.

- [ ] **Step 3: Add remote and push**

```bash
cd /c/Users/alvar/Downloads/files/afip-arca-ws
git remote add origin https://github.com/AlvaFG/afip-arca-ws.git
git push -u origin main
git push --tags
```

- [ ] **Step 4: Verify CI runs green**

```bash
gh run list --limit 5
gh run watch
```
Expected: `ci.yml` passes (scraper-tests, examples-{python,node,php,bash}, skill-lint).

- [ ] **Step 5: Trigger first docs refresh manually (optional)**

```bash
gh workflow run refresh-docs.yml
gh run list --workflow=refresh-docs.yml
```

If a PR is opened by the action, review and merge it.

- [ ] **Step 6: Tag v0.1.0 release**

```bash
git tag -a v0.1.0 -m "v0.1.0 — initial release: 7 skills, scraper, CI"
git push origin v0.1.0
gh release create v0.1.0 --title "v0.1.0 — initial release" --generate-notes
```

- [ ] **Step 7: Final smoke test (manual)**

In a separate test project:

```bash
cd /tmp
mkdir test-afip && cd test-afip
git init
mkdir -p .claude/skills
ln -s ~/Downloads/files/afip-arca-ws/.claude/skills/* .claude/skills/
```

Open Claude Code in `/tmp/test-afip`, ask: *"How do I sign a TRA in Python for WSFEv1?"* — verify Claude activates `afip-arca-overview` → routes to `afip-arca-wsaa` → produces relevant code.

---

## Spec coverage map

| Spec section | Tasks |
|---|---|
| 4 / Success criteria C1 | Task 8 (router), 37 (final review verifies) |
| 4 / C2 (lint) | Tasks 14-17, 21-22, 25, 28, 33 |
| 4 / C3 (diff-friendly) | Task 4 |
| 4 / C4 (install <2 min) | Task 35 |
| 4 / C5 (4 sections) | Tasks 3, 36 |
| 5.1 Repo layout | Tasks 1, 2, all skills |
| 5.2 Skill structure | Tasks 8, 10-11, 13-18, 20-22, 24-25, 27-28, 30 |
| 5.3 7 skills | Tasks 8, 10, 13, 20, 24, 27, 30 |
| 5.4 Inter-skill deps | Tasks 8 (decision tree), 10/13/20/24/27/30 (Depends on sections) |
| 5.5 Scraper | Tasks 2-6 |
| 5.6 CI | Tasks 32-33 |
| 6.1 Refresh data flow | Task 32 |
| 6.2 Use by Claude | Tasks 8 (router) + smoke test in 38 |
| 7.1 overview | Task 8 |
| 7.2 certificates | Tasks 10-11 |
| 7.3 wsaa | Tasks 13-18 |
| 7.4 wsfev1 | Tasks 20-22 |
| 7.5 wsfexv1 | Tasks 24-25 |
| 7.6 padron | Tasks 27-28 |
| 7.7 debugging | Task 30 |
| 8 Error handling | Tasks 6 (scraper tests), 33 (lint blocks merge) |
| 9 Testing strategy | Tasks 6, 33, 38 (smoke) |
| 10 Rollout v0.1.0 | Task 38 (release) |






