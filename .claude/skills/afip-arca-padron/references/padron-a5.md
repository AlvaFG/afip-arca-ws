# Padrón A5 — `ws_sr_padron_a5`

Igual a A4 pero incluye **domicilio fiscal**. Es el más usado para emisión de comprobantes electrónicos.

## Endpoints

| Ambiente | URL |
|---|---|
| Homologación | `https://awshomo.afip.gov.ar/sr-padron/webservices/personaServiceA5?WSDL` |
| Producción | `https://aws.afip.gov.ar/sr-padron/webservices/personaServiceA5?WSDL` |

## Método `getPersona_v2`

Mismo request shape que A4 (`token, sign, cuitRepresentada, idPersona`). El response agrega:

```
personaReturn.persona:
  ...campos A4...
  domicilioFiscal:
    direccion: string
    codPostal: string
    localidad: string
    idProvincia: int     # 0=CABA, 1=BsAs, 2=Catamarca, ...
    descripcionProvincia: string
    tipoDomicilio: FISCAL | ...
    estadoDomicilio: ACTUALIZADO | NO_ACTUALIZADO
```

## Validaciones útiles

- `estadoClave == ACTIVO` antes de facturar — si es INACTIVO, AFIP rechaza la factura.
- `estadoDomicilio == ACTUALIZADO` — domicilio sin actualizar puede causar problemas en facturas de exportación o transporte.

## Limitaciones

- Una sola consulta por request (no batch).
- Retry: si AFIP devuelve timeout, esperar ≥30s antes del retry — el padrón es uno de los servicios más sobrecargados.
