# Padrón A13 — `ws_sr_padron_a13`

El más completo de los servicios privados. A5 + impuestos en los que el contribuyente está inscripto.

## Endpoints

| Ambiente | URL |
|---|---|
| Homologación | `https://awshomo.afip.gov.ar/sr-padron/webservices/personaServiceA13?WSDL` |
| Producción | `https://aws.afip.gov.ar/sr-padron/webservices/personaServiceA13?WSDL` |

## Método `getPersona_v2`

Mismo request shape. Response agrega sobre A5:

```
personaReturn.persona:
  ...campos A5...
  impuestos: array of:
    idImpuesto: int      # 11=Ganancias, 30=IVA, 32=Monotributo, ...
    descripcionImpuesto: string
    periodo: int         # YYYYMM
    estado: ACTIVO | BAJA
    fechaInscripcion: YYYY-MM-DD
    fechaBaja: YYYY-MM-DD  # si estado=BAJA
  categoriasMonotributo: array of:  # solo si inscripto en monotributo
    idCategoria: string  # A, B, C, ...
    periodo: int
    estado: string
  regimenes: array of:
    idRegimen: int
    descripcionRegimen: string
    ...
```

## Casos de uso

- **Validar régimen del receptor** antes de emitir factura A: solo se puede emitir A si el receptor está inscripto en IVA o monotributo. A13 te dice eso sin ambigüedad.
- **Reportes contables**: combinar A13 de varios CUITs para mapear quién paga qué impuestos.
- **Detección de baja en monotributo**: si un cliente histórico cambia a baja en monotributo, ya no podés facturarle como tal.

## Costo

A13 es más pesado (más datos, más latencia). Si solo necesitás razón social y domicilio, usá A5.
