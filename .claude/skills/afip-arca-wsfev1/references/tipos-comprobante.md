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
| 51 | Factura A con Leyenda "Operación Sujeta a Retención" | RI a un nuevo cliente sin antecedentes suficientes (régimen de retención) | Requerido si ImpIVA>0 |
| 52 | Nota de Débito A con Leyenda "Operación Sujeta a Retención" | Para facturas 51 | Requerido si ImpIVA>0 |
| 53 | Nota de Crédito A con Leyenda "Operación Sujeta a Retención" | Para facturas 51 | Requerido si ImpIVA>0 |
| 54 | Recibo A con Leyenda "Operación Sujeta a Retención" | Recibo bajo el mismo régimen | Requerido si ImpIVA>0 |
| 201 | Factura de Crédito Electrónica MiPyMEs A | Régimen FCE | Requerido si ImpIVA>0 |
| 202 | Nota de Débito FCE MiPyMEs A | | Requerido si ImpIVA>0 |
| 203 | Nota de Crédito FCE MiPyMEs A | | Requerido si ImpIVA>0 |
| 206 | Factura FCE MiPyMEs B | | Requerido si ImpIVA>0 |
| 207 | Nota de Débito FCE MiPyMEs B | | Requerido si ImpIVA>0 |
| 208 | Nota de Crédito FCE MiPyMEs B | | Requerido si ImpIVA>0 |
| 211 | Factura FCE MiPyMEs C | | NO enviar Iva |
| 212 | Nota de Débito FCE MiPyMEs C | | NO enviar Iva |
| 213 | Nota de Crédito FCE MiPyMEs C | | NO enviar Iva |

**51/52/53/54 — régimen M reemplazado por la leyenda (RG 3665, vigente desde
2015-05-22):** los códigos 51-53 fueron alguna vez "Factura/ND/NC M", el
régimen para responsables inscriptos sin antecedentes suficientes que exigía
retención adicional del comprador. RG 3665 discontinuó el régimen M y lo
reemplazó por facturas tipo A con la leyenda "Operación Sujeta a Retención" —
mismo código numérico, descripción y tratamiento distintos. `54` es el recibo
equivalente. No queda emisión bajo "M" vigente: si algo en el código o en
docs viejos dice "Factura M", está describiendo el régimen pre-2015.

## Reglas rápidas

- **Si emisor es monotributo** → solo C (11/12/13) o FCE C (211/212/213). Nunca enviar Iva.
- **Si receptor es consumidor final** → solo B (6/7/8). DocTipo=99, DocNro=0 si no se identifica.
- **Notas de Crédito y Débito** deben ser del mismo grupo letra que la factura original.
- **Régimen FCE MiPyMEs**: requiere campos adicionales (`FchVtoPago`, `Tributos`); ver docs específicas en `docs/`.

## Fuera del alcance de un restaurante típico

Estos códigos existen en el catálogo de `FEParamGetTiposCbte` pero el sistema no
los emite. Se listan acá para que nadie los interprete como un olvido al leer
la tabla de arriba y los implemente sin necesidad real.

| Código | Descripción | Por qué está fuera de alcance |
|---|---|---|
| 4 | Recibo A | Un restaurante típico no emite recibos independientes — el comprobante de venta es la factura/nota. |
| 9 | Recibo B | Idem 4, letra B. |
| 15 | Recibo C | Idem 4, letra C. |
| 5 | Nota de Venta al Contado A | Comprobante alternativo a factura para venta al contado; no forma parte del flujo de un restaurante. |
| 10 | Nota de Venta al Contado B | Idem 5, letra B. |
| 63 | Liquidación A | Comprobante de liquidación de operaciones por cuenta de terceros (consignación, corretaje); no aplica al modelo de negocio de un restaurante. |
| 64 | Liquidación B | Idem 63, letra B. |
| 34, 35, 39, 40 | Comprobantes del régimen RG 1415 (Anexo I, Apartado A, inc. f) y "otros comprobantes" A/B) | Régimen sectorial específico, no aplica a restaurantes. Confirmado que los cuatro códigos existen en el catálogo; las etiquetas exactas por código no se re-verificaron en este pase — no se usan, así que no hace falta precisión ahí. |
| 49 | Compra de Bienes Usados a Consumidor Final | Comprobante de compra (no de venta) para el régimen de bienes usados; no aplica — Un restaurante solo emite comprobantes de venta. |

## Verificación

Tabla de códigos en uso (arriba de "Fuera del alcance") verificada contra
`FEParamGetTiposCbte` en homologación el 2026-08-13.
