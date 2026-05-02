# Tipos de Comprobante (`CbteTipo`)

Source: `FEParamGetTiposCbte`. Estos códigos cambian con baja frecuencia pero verificá contra el WS al menos una vez por release.

| Código | Descripción | Cuándo se usa | Iva field |
|---|---|---|---|
| 1 | Factura A | Emitida por responsable inscripto a otro RI o monotributo | Requerido si ImpIVA>0 |
| 2 | Nota de Débito A | Para facturas A | Requerido si ImpIVA>0 |
| 3 | Nota de Crédito A | Para facturas A | Requerido si ImpIVA>0 |
| 6 | Factura B | RI a consumidor final / exento | Requerido si ImpIVA>0 |
| 7 | Nota de Débito B | Para facturas B | Requerido si ImpIVA>0 |
| 8 | Nota de Crédito B | Para facturas B | Requerido si ImpIVA>0 |
| 11 | Factura C | Emitida por monotributo a cualquier receptor | **NO enviar Iva** |
| 12 | Nota de Débito C | Para facturas C | NO enviar Iva |
| 13 | Nota de Crédito C | Para facturas C | NO enviar Iva |
| 51 | Factura M | RI a un nuevo cliente sin antecedentes (régimen especial) | Requerido si ImpIVA>0 |
| 52 | Nota de Débito M | Para facturas M | Requerido si ImpIVA>0 |
| 53 | Nota de Crédito M | Para facturas M | Requerido si ImpIVA>0 |
| 201 | Factura de Crédito Electrónica MiPyMEs A | Régimen FCE | Requerido si ImpIVA>0 |
| 202 | Nota de Débito FCE MiPyMEs A | | Requerido si ImpIVA>0 |
| 203 | Nota de Crédito FCE MiPyMEs A | | Requerido si ImpIVA>0 |
| 206 | Factura FCE MiPyMEs B | | Requerido si ImpIVA>0 |
| 207 | Nota de Débito FCE MiPyMEs B | | Requerido si ImpIVA>0 |
| 208 | Nota de Crédito FCE MiPyMEs B | | Requerido si ImpIVA>0 |
| 211 | Factura FCE MiPyMEs C | | NO enviar Iva |
| 212 | Nota de Débito FCE MiPyMEs C | | NO enviar Iva |
| 213 | Nota de Crédito FCE MiPyMEs C | | NO enviar Iva |

## Reglas rápidas

- **Si emisor es monotributo** → solo C (11/12/13) o FCE C (211/212/213). Nunca enviar Iva.
- **Si receptor es consumidor final** → solo B (6/7/8). DocTipo=99, DocNro=0 si no se identifica.
- **Notas de Crédito y Débito** deben ser del mismo grupo letra que la factura original.
- **Régimen FCE MiPyMEs**: requiere campos adicionales (`FchVtoPago`, `Tributos`); ver docs específicas en `docs/`.
