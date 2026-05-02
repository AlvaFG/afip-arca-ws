# Tipos de Documento (`DocTipo`)

Source: `FEParamGetTiposDoc`.

| Código | Descripción | Notas |
|---|---|---|
| 80 | CUIT | Personas jurídicas y RI/monotributo. DocNro = 11 dígitos sin guiones |
| 86 | CUIL | Personas físicas en relación de dependencia |
| 87 | CDI | Clave de Identificación (extranjeros sin CUIT) |
| 89 | LE | Libreta de Enrolamiento (legacy) |
| 90 | LC | Libreta Cívica (legacy) |
| 91 | CI Extranjera | |
| 92 | en trámite | Para casos sin documento aún tramitado |
| 93 | Acta Nacimiento | |
| 94 | Pasaporte | Para extranjeros |
| 95 | CI Bs.As. RNP | |
| 96 | DNI | Personas físicas. DocNro = 7 u 8 dígitos sin puntos |
| 99 | Consumidor Final | DocNro = 0 — usado en facturas B sin identificar al receptor |

## Restricciones

- **Factura A/M y notas asociadas**: DocTipo debe ser 80 (CUIT). Otros tipos rechazados con `10054`.
- **Factura B**: cualquier DocTipo válido. Si `ImpTotal > $$ umbral` (ver normativa vigente), se requiere identificar al receptor (no usar 99).
- **Factura C**: cualquier DocTipo. Como en B, hay umbral para identificación obligatoria.
