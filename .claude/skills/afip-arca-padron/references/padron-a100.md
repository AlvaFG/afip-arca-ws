# Padrón A100 — Constancia de Inscripción (público)

Es el WS público de AFIP equivalente a la "Constancia de Inscripción" que cualquiera puede descargar desde el portal sin autenticación. **No requiere TA ni certificado.**

## Endpoints

| Ambiente | URL |
|---|---|
| Producción | `https://soa.afip.gob.ar/sr-padron/v2/persona/{cuit}` (REST/JSON) |
| Producción (SOAP legacy) | `https://aws.afip.gov.ar/sr-padron/webservices/personaServiceA100?WSDL` |

Para nuevas integraciones, usá la API REST. El SOAP queda como compatibilidad.

## REST GET

```
GET https://soa.afip.gob.ar/sr-padron/v2/persona/20111111112
```

Response (JSON):

```json
{
  "success": true,
  "data": {
    "idPersona": 20111111112,
    "tipoPersona": "FISICA",
    "estadoClave": "ACTIVO",
    "nombre": "JUAN",
    "apellido": "PEREZ",
    "domicilioFiscal": { ... },
    "categoriasMonotributo": [ ... ]
  }
}
```

Si el CUIT no existe: `{"success": false, "error": "..."}`.

## Limitaciones

- **Rate limit fuerte** (es público — abusos cortan acceso por IP).
- **Sin garantías de SLA** — para uso productivo masivo, mejor pagar el costo de A4/A5/A13 que tienen acceso autenticado.
- **Solo lectura del padrón "público"**: no incluye datos sensibles (puede no incluir todos los impuestos).

## Cuándo usarlo

- Validación rápida de CUITs en formularios web públicos (KYC light).
- Scripts ad-hoc de auditoría.
- Cuando no querés gestionar certs y no sos misión-crítico.
