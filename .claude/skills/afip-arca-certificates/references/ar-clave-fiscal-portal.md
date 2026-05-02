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

## Common pitfalls

- **Wrong "Representante"**: when authorizing a service, the representative must be the cert alias, not the CUIT. Selecting the CUIT silently does nothing.
- **Service not in the list**: not all WS are exposed in the same dropdown. WSFEv1 is under "Administración Federal de Ingresos Públicos", padrones under "AFIP - Servicios Web". If a service is missing, your CUIT may not be enabled for it — check the agency's onboarding requirements.
- **Multiple certs per CUIT**: AFIP allows multiple alias per CUIT. Useful for separating apps (e.g. `prod-billing` vs `prod-padron`) so you can rotate them independently.
