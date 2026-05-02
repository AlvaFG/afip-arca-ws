# Homologación vs Producción — endpoint reference

Mezclar ambientes (cert de homo contra URL de prod, o viceversa) es la causa #1 de "no entiendo por qué no anda". Esta tabla es la que tenés que mirar primero.

| Servicio | Homologación | Producción |
|---|---|---|
| WSAA | `https://wsaahomo.afip.gov.ar/ws/services/LoginCms` | `https://wsaa.afip.gov.ar/ws/services/LoginCms` |
| WSFEv1 | `https://wswhomo.afip.gov.ar/wsfev1/service.asmx` | `https://servicios1.afip.gov.ar/wsfev1/service.asmx` |
| WSFEXv1 | `https://wswhomo.afip.gov.ar/wsfexv1/service.asmx` | `https://servicios1.afip.gov.ar/wsfexv1/service.asmx` |
| Padrón A4 | `https://awshomo.afip.gov.ar/sr-padron/webservices/personaServiceA4` | `https://aws.afip.gov.ar/sr-padron/webservices/personaServiceA4` |
| Padrón A5 | `https://awshomo.afip.gov.ar/sr-padron/webservices/personaServiceA5` | `https://aws.afip.gov.ar/sr-padron/webservices/personaServiceA5` |
| Padrón A13 | `https://awshomo.afip.gov.ar/sr-padron/webservices/personaServiceA13` | `https://aws.afip.gov.ar/sr-padron/webservices/personaServiceA13` |
| Padrón A100 (REST) | (no homo, prod-only público) | `https://soa.afip.gob.ar/sr-padron/v2/persona/{cuit}` |

## Rule of thumb

- Hostnames de homo casi siempre tienen `homo` en el medio (`wsaahomo`, `wswhomo`, `awshomo`).
- Hostnames de prod son `wsaa`, `servicios1`, `aws`.
- Mezclar → fault `cms.bad_audience` en login, o "Persona representada no autorizada" en padrones.

## Certs

Los certs son específicos por ambiente. Un cert solicitado contra homologación no funciona contra prod, ni siquiera tras "promover" — tenés que generar un cert nuevo desde la pantalla de prod del WSASS.

Convención común para distinguir: `mi-empresa-homo.crt` vs `mi-empresa-prod.crt`. Validar con `openssl x509 -in cert.crt -noout -subject` (el alias / CN no cambia, pero el environment se conoce por dónde lo solicitaste — guardalo en el nombre del archivo).
