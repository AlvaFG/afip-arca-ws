---
title: "afip-arca-ws — Multi-skill suite for AFIP/ARCA Web Services integration"
date: 2026-05-02
status: draft
authors: ["Alvaro Fernandez Guyot", "Claude (Opus 4.7)"]
---

# Spec: `afip-arca-ws` — Multi-skill para integraciones con AFIP/ARCA

## 1. Goal

Construir un repositorio Git público (`github.com/AlvaFG/afip-arca-ws`) que distribuye una **suite de 7 Claude Code skills** específicas por dominio para que Claude no solo conozca la documentación oficial de los Web Services de AFIP/ARCA, sino que sepa **integrarlos en código real** (Python, Node/TS, PHP, Bash) durante una sesión de desarrollo.

El repo cumple tres funciones:

1. **Mirror versionado** de la documentación oficial de <https://www.afip.gob.ar/ws/> en Markdown, refrescada semanalmente vía GitHub Actions.
2. **Suite de skills** instalables individualmente (`afip-arca-overview`, `afip-arca-certificates`, `afip-arca-wsaa`, `afip-arca-wsfev1`, `afip-arca-wsfexv1`, `afip-arca-padron`, `afip-arca-debugging`).
3. **Material reutilizable**: ejemplos end-to-end por lenguaje, scripts ejecutables (CSR, validación de TA, FEDummy), plantillas (`tra.xml`, `factura.json`, `openssl.cnf`), y referencias curadas (cheatsheets, error codes, flowcharts).

## 2. Non-goals

- **No** es una librería runtime: no exportamos un SDK ni un cliente. Los ejemplos son seed code que el desarrollador adapta.
- **No** es un mirror de PDFs de manuales completos — sólo HTML scrapeable. Si una sección sólo existe como PDF, se indexa pero no se convierte.
- **No** cubre servicios fuera del ámbito AFIP/ARCA (no ANSES, no RENAPER, no AFIP-DGA aduana siquiera, salvo que ya estén bajo el dominio `afip.gob.ar/ws/`).
- **No** publica certificados ni claves: ningún `.crt`/`.key` real va al repo, ni siquiera de homologación.

## 3. Target users

- **Persona primaria**: desarrolladores backend integrando facturación electrónica argentina por primera vez. Usan Claude Code y quieren que entienda el dominio sin pegar URLs.
- **Persona secundaria**: equipos que ya tienen un cliente AFIP en producción y necesitan agregar un servicio nuevo (WSFEXv1, padrón) o renovar certificados.
- **Persona terciaria**: contadores/consultores técnicos que validan implementaciones — quieren references rápidas de error codes y flujos.

## 4. Success criteria

| # | Criterio | Cómo se mide |
|---|---|---|
| C1 | Claude activa la skill correcta sin que el usuario la nombre | Test manual: pedir "necesito firmar un TRA" → debe activar `afip-arca-wsaa` |
| C2 | Cada ejemplo de código compila/lintea sin error | CI ejecuta `py_compile`, `tsc --noEmit`, `php -l`, `shellcheck` |
| C3 | El refresh semanal genera diffs útiles, no churn | Diff entre dos refreshes con HTML idéntico debe ser vacío |
| C4 | Instalable en un proyecto consumidor en <2 minutos | README documenta 3 modos (clone+symlink, submodule, plugin) |
| C5 | Documentación cubre las 4 secciones top-level de afip.gob.ar/ws/ | `docs/README.md` lista ≥1 página de Programadores, Documentación, Aplicativos, Ayuda |

## 5. Architecture

### 5.1 Repo layout

```
afip-arca-ws/
├── README.md
├── LICENSE                            # MIT
├── .gitignore
├── .github/
│   └── workflows/
│       ├── refresh-docs.yml           # weekly cron → PR
│       └── ci.yml                     # lint scraper, lint examples
├── docs/                              # OUTPUT del scraper (versionado)
│   ├── README.md                      # índice auto-generado
│   ├── _assets-index.md               # WSDLs, PDFs descubiertos (URL + checksum)
│   ├── programadores/...
│   ├── documentacion/...
│   ├── aplicativos/...
│   └── menu-ayuda/...
├── scraper/
│   ├── scrape.py
│   ├── config.yaml
│   ├── requirements.txt
│   └── tests/
│       ├── test_extract.py
│       └── fixtures/sample_page.html
└── .claude/
    └── skills/
        ├── afip-arca-overview/
        ├── afip-arca-certificates/
        ├── afip-arca-wsaa/
        ├── afip-arca-wsfev1/
        ├── afip-arca-wsfexv1/
        ├── afip-arca-padron/
        └── afip-arca-debugging/
```

### 5.2 Estructura común de cada skill

```
<skill-name>/
├── SKILL.md                # entry point — frontmatter + decision tree + gotchas
├── references/             # cargados a demanda por Claude
│   └── *.md
├── examples/               # opcional: código completo por lenguaje
│   ├── python/
│   ├── node/
│   ├── php/
│   └── bash/
├── scripts/                # opcional: ejecutables que Claude puede correr
│   └── *.sh|*.py
└── assets/                 # opcional: plantillas y configs
    └── *.tmpl
```

### 5.3 Las 7 skills — propósito y triggers

| Skill | Cuándo activa | Contenido clave |
|---|---|---|
| `afip-arca-overview` | Triggers amplios (AFIP, ARCA, factura electrónica argentina). Es el **router** | Decision tree → pide invocar la skill específica vía `Skill` tool |
| `afip-arca-certificates` | CSR, .crt, .key, .p12, "Administrador de Relaciones", renovación | Scripts: generate-csr.sh, check-cert.sh, pem-to-p12.sh; reference de portal Clave Fiscal |
| `afip-arca-wsaa` | TRA, loginCms, Ticket de Acceso, sign CMS, token+sign | Flow doc, TA caching rules, error codes WSAA; ejemplos en 4 lenguajes; script validate-ta.py |
| `afip-arca-wsfev1` | FECAESolicitar, CAE, factura electrónica mercado interno, FEParamGet | Methods, tipos comprobante/doc/IVA, error codes; ejemplos en 4 lenguajes; plantilla factura.json |
| `afip-arca-wsfexv1` | Factura exportación, FEXGetCMP, incoterms, monedas extranjeras | Methods, idiomas, monedas, incoterms, error codes; ejemplos en Python/Node/PHP |
| `afip-arca-padron` | Padrón A4/A5/A13/A100, constancia inscripción, getPersona | Reference por servicio; ejemplos en Python/Node/PHP |
| `afip-arca-debugging` | FEDummy, SoapUI, homologación vs producción, "no anda mi cliente AFIP" | Flowchart errores comunes, setup SoapUI, script test-fedummy.sh |

### 5.4 Inter-skill referencias

Las skills son **independientes pero acopladas por documentación**: cada SKILL.md declara en una sección "Depends on" qué otras skills producen artefactos que ésta consume. La dependencia es de conocimiento (necesitás haber leído la otra), no de runtime:

- `afip-arca-wsaa` depends on `afip-arca-certificates` (necesita un .crt/.key válido para firmar el TRA)
- `afip-arca-wsfev1` depends on `afip-arca-wsaa` (necesita un TA válido en cada request)
- `afip-arca-wsfexv1` depends on `afip-arca-wsaa`
- `afip-arca-padron` depends on `afip-arca-wsaa` (excepto A100 público, que no requiere TA — verificar en docs)

Claude lee esto en el SKILL.md y, si el usuario instaló sólo una, le sugiere instalar las dependencias.

### 5.5 Scraper

Mejoras sobre la versión existente (`scrape.py` actual ya hace lo básico bien):

- **Multi-root crawl**: empezar de `/programadores/`, `/documentacion/`, `/aplicativos/`, `/menu-ayuda/` explícitamente, no sólo desde `/`.
- **Tablas preservadas**: los error codes y tipos de comprobante están en tablas HTML — usar conversión de tabla → tabla Markdown (markdownify ya lo soporta, verificar).
- **Detección de assets descargables**: WSDL, XSD, PDF — listar en `docs/_assets-index.md` con URL + content-length + sha256.
- **Output diff-friendly**:
  - Frontmatter con campos en orden alfabético.
  - Normalizar whitespace y final newline.
  - `scraped_at` movido a un sidecar `docs/_meta.json` para que el contenido en sí no cambie cuando solo cambia la fecha.
- **Tests** con un HTML fixture mínimo: `test_extract.py` valida `extract_content`, `url_to_path`, `discover_links` sin tocar la red.

### 5.6 CI

`refresh-docs.yml` (mejora del existente):
- `concurrency: { group: refresh-docs, cancel-in-progress: false }` para no solapar runs.
- Comentario en el PR con resumen: páginas nuevas / modificadas / eliminadas.

`ci.yml` (nuevo):
- Job `scraper-tests`: ruff + pytest sobre `scraper/`.
- Job `examples-lint` (corre por cada skill que tiene `examples/`):
  - Python: `python -m py_compile $(find .claude/skills/*/examples/python -name '*.py')`
  - Node/TS: descubrir cada `.claude/skills/*/examples/node/` con `package.json`, instalar y correr `npx tsc --noEmit`
  - PHP: `php -l` por cada `.php` bajo `.claude/skills/*/examples/php/`
  - Bash: `shellcheck` por cada `.sh` bajo `.claude/skills/*/examples/bash/` y `.claude/skills/*/scripts/*.sh`
- Job `skill-lint`: verifica que cada `SKILL.md` tenga frontmatter válido (`name`, `description`) y description ≥40 caracteres.

## 6. Data flow

### 6.1 Refresh de docs

```
GitHub Actions cron (sundays 06:00 UTC)
  → checkout
  → pip install scraper deps
  → python scrape.py
    → crawl https://www.afip.gob.ar/ws/{programadores,documentacion,aplicativos,menu-ayuda}/
    → para cada página: fetch HTML → extract → markdown → write docs/<path>.md
    → write docs/README.md (índice) y docs/_assets-index.md
  → peter-evans/create-pull-request abre PR si hay diff
```

### 6.2 Uso por parte de Claude (en proyecto consumidor)

```
Usuario: "tengo que mandar una factura electrónica desde Python"
  → Claude lee description de skills disponibles
  → activa afip-arca-overview (description amplia matchea)
  → SKILL.md de overview indica decision tree
  → Claude invoca Skill(afip-arca-wsfev1)
  → SKILL.md de wsfev1 lista references y examples
  → Claude lee references/methods.md y examples/python/wsfev1_factura.py
  → genera código adaptado al proyecto del usuario
```

## 7. Components

### 7.1 `afip-arca-overview` (router)

- **Frontmatter description**: amplia, cubre todos los keywords del dominio, incluye el truco de "even 1% chance" para que Claude la active aún cuando la query es vaga.
- **Cuerpo**:
  - Tabla "what do you need? → which skill"
  - Decision tree en formato dot/ascii
  - Sección "ARCA rebrand notes" (qué cambió, qué no — el organismo cambió de AFIP a ARCA en 2024 pero los WS y dominios siguen iguales)
  - Punteros a `docs/README.md` para navegación de docs raw
- Sin `examples/`, sin `scripts/`. Solo SKILL.md + references mínimos.

### 7.2 `afip-arca-certificates`

- **SKILL.md**: cuándo, gotchas (renovación cada 2 años, alias de cert, separación key/crt vs p12).
- **references/csr-howto.md**: paso a paso generación CSR + upload al portal AR Clave Fiscal.
- **references/ar-clave-fiscal-portal.md**: capturas-en-texto del portal, dónde clickear.
- **references/renewal-checklist.md**: cuándo renovar, qué romper, cómo rotar sin downtime.
- **scripts/**:
  - `generate-csr.sh`: openssl req con sane defaults para AFIP.
  - `check-cert.sh`: muestra issuer, subject, fechas, fingerprint.
  - `pem-to-p12.sh`: bundle para Java/.NET.
- **assets/openssl.cnf.tmpl**: template con campos AFIP-friendly.

### 7.3 `afip-arca-wsaa`

- **SKILL.md**: gotchas críticos — TA cache obligatorio (≤12h), no llamar loginCms en cada request, namespace case-sensitive.
- **references/**:
  - `tra-flow.md`: pasos 1-4 del flujo TRA con diagrama secuencia.
  - `ta-caching-rules.md`: dónde cachear (filesystem vs DB vs memoria), cómo manejar concurrencia.
  - `wsaa-error-codes.md`: tabla ERR-* con causa y fix.
- **examples/{python,node,php,bash}/**: cada uno hace TRA → firma CMS → loginCms → parse TA → cache. Bash usa openssl smime.
- **scripts/validate-ta.py**: parsea TA.xml y muestra expiración.
- **assets/tra.xml.tmpl**: plantilla con placeholders.

### 7.4 `afip-arca-wsfev1`

- **SKILL.md**: enfoque en FECAESolicitar; gotchas (numeración por punto de venta, importes con 2 decimales).
- **references/**: `methods.md` (FECAESolicitar, FECompUltimoAutorizado, FEParamGetTiposCbte, FEDummy, etc.), `tipos-comprobante.md`, `tipos-doc.md`, `alicuotas-iva.md`, `error-codes.md`.
- **examples/{python,node,php,bash}/**: factura B simple end-to-end. Python con zeep, Node con `soap` package, PHP con SoapClient nativo, Bash con curl + plantilla XML.
- **assets/factura.json.tmpl**: estructura mínima para construir el request.

### 7.5 `afip-arca-wsfexv1`

- Análogo a wsfev1 pero para exportación. Skip Bash example (raro hacer export sólo con curl).
- references/ con monedas, incoterms, idiomas, métodos.

### 7.6 `afip-arca-padron`

- Una reference por servicio (A4, A5, A13, A100).
- examples/ en Python/Node/PHP haciendo `getPersona` por CUIT.
- Notar diferencias de scope: A4 mínimo, A5 con domicilio, A13 con datos impositivos completos, A100 público sin auth (verificar en docs).

### 7.7 `afip-arca-debugging`

- **references/homologacion-vs-prod.md**: tabla URL homo vs prod por servicio.
- **references/fedummy-checks.md**: cómo usar FEDummy para validar conectividad sin TA.
- **references/soapui-setup.md**: importar WSDL, configurar TLS con cert.
- **references/common-errors-flowchart.md**: dot graph "mi cliente da X → causas posibles → fixes".
- **scripts/test-fedummy.sh**: curl al endpoint dummy de varios servicios.

## 8. Error handling

- **Scraper**: errores HTTP per página → log + skip + cuenta en stats. Errores totales >25% del crawl → exit 1 (CI falla).
- **CI examples-lint**: cualquier ejemplo que no pase lint bloquea merge.
- **Skill discovery**: si dos skills tienen descriptions que se pisan, Claude puede activar la equivocada. Mitigación: descriptions estrechas + el `overview` reorienta.

## 9. Testing strategy

- **Scraper**: unit tests con HTML fixtures locales (`scraper/tests/fixtures/`). No hits a la red en CI.
- **Examples**: lint-only (CI). No se ejecutan en vivo porque requieren cert real + endpoint AFIP.
- **Skills**: `skill-lint` verifica frontmatter mínimo. No hay test runtime de "Claude activa la correcta" — es manual/empírico.
- **Smoke test manual** (documentado en README): clonar repo → instalar 1 skill → abrir Claude Code en proyecto vacío → pedir "implementame WSAA en Python" → verificar que activa `afip-arca-wsaa`.

## 10. Rollout

1. **v0.1.0** (este spec): estructura completa, scraper funcionando, todas las skills con SKILL.md + references mínimos. Ejemplos sólo en Python+Bash. Docs vacíos (esperando primer cron run).
2. **v0.2.0**: ejemplos completos en Node y PHP. Primer refresh de docs mergeado.
3. **v0.3.0**: tests del scraper, CI completo. README con guía de instalación pulida.
4. **v1.0.0**: cuando un usuario externo lo use exitosamente y reportemos cero gotchas críticos.

## 11. Open questions / risks

- **R1**: La estructura de `afip.gob.ar/ws/` puede cambiar — el scraper podría romperse silenciosamente. Mitigación: tests con fixture; alerta en CI si páginas crawled <50.
- **R2**: ARCA podría migrar de dominio (`arca.gob.ar`). Mitigación: mantener `base_url` configurable; hoy el portal vive en afip.gob.ar todavía.
- **R3**: Skills "router" no es un patrón super establecido. Si Claude no respeta la indirección, hay que colapsar a una skill grande. Mitigación: revisar tras smoke test de v0.1.0.
- **R4**: Algunas docs de AFIP están sólo en PDF (manuales largos). No las cubrimos en v1; podríamos agregar un job que liste PDFs y pida al usuario adjuntarlos manualmente.

## 12. Out of scope (futuro)

- Plugin marketplace (Claude Code plugins): publicar la skill como plugin instalable con `/plugin install afip-arca-ws@AlvaFG`.
- WSCT, WSMTXCA, WSBFE (otros servicios menos usados).
- Integración con servicios provinciales (ARBA, AGIP, API) — fuera del ámbito AFIP/ARCA.
- Internacionalización del README al inglés (público objetivo es Argentina).
