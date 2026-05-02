# Padrón A4 — `ws_sr_padron_a4`

Endpoint mínimo de consulta de personas en el padrón AFIP. Devuelve datos básicos: razón social/nombre, tipo de persona (física/jurídica), estado de la clave (activa/inactiva).

## Endpoints

| Ambiente | URL |
|---|---|
| Homologación | `https://awshomo.afip.gov.ar/sr-padron/webservices/personaServiceA4?WSDL` |
| Producción | `https://aws.afip.gov.ar/sr-padron/webservices/personaServiceA4?WSDL` |

## Métodos

### `getPersona`

```
Request:
  token: string
  sign: string
  cuitRepresentada: long   # CUIT del solicitante (= CUIT del Auth en otros WS)
  idPersona: long          # CUIT a consultar
Response:
  personaReturn:
    persona:
      idPersona: long
      tipoPersona: FISICA | JURIDICA
      tipoClave: CUIT | CUIL | ...
      estadoClave: ACTIVO | INACTIVO
      razonSocial: string         # solo si JURIDICA
      apellido, nombre: string    # solo si FISICA
      tipoDocumento, numeroDocumento: ...
    errorReturn:
      error: array of { code, descripcion }
```

### `dummy`

Healthcheck sin auth, devuelve `appserver/dbserver/authserver`.

## Errores comunes

- "No existe persona con ese Id" → CUIT no registrado o típico CUIT inválido (no tiene dígito verificador correcto).
- "Persona representada no autorizada" → tu cert no está autorizado en WSASS para A4 contra ese cuitRepresentada.

## Notas

- A4 NO devuelve domicilio fiscal — usá A5 si lo necesitás.
- A4 NO devuelve impuestos asociados — usá A13.
- Para producción, AFIP impone rate-limiting; cachear queries por al menos 24h.
