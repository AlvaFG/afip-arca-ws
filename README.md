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

Crawler Python (httpx + selectolax + markdownify) que convierte el portal de AFIP a Markdown limpio con frontmatter. Tests unitarios con fixtures HTML.

### CI

- `.github/workflows/refresh-docs.yml` — re-scrape semanal con PR automático.
- `.github/workflows/ci.yml` — lintea scraper (ruff + pytest), ejemplos en Python/Node/PHP/Bash, frontmatter de cada SKILL.md.

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
python -m venv .venv
source .venv/bin/activate           # Linux/Mac
source .venv/Scripts/activate       # Windows Git Bash
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

## ARCA vs AFIP

El organismo cambió de nombre AFIP → ARCA en 2024 pero los Web Services siguen igual (mismas URLs, namespaces, métodos). Por eso el repo cubre ambos términos. Más detalles en `.claude/skills/afip-arca-overview/references/arca-rebrand-notes.md`.

## Licencia

Código: **MIT**. Contenido de `docs/`: propiedad de AFIP/ARCA, reproducido como mirror funcional.
