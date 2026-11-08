# WSFEv1 Error Codes

| Código | Mensaje (es) | Causa típica | Fix |
|---|---|---|---|
| 600 | Token inválido | El TA está expirado o el formato no es el correcto | Obtener un TA nuevo (puede haber expirado el cache) |
| 601 | Sign inválido | Mismatch en el sign del TA | Re-obtener TA; verificar que no se haya modificado en transit |
| 1001 | El CUIT no se encuentra autorizado | El CUIT del Auth no está habilitado para WSFEv1 | Autorizar en "Administrador de Relaciones" → WSFEv1 → alias del cert |
| 10000 | Familia de rechazos de habilitación; el sub-código va en el mensaje: `01` el emisor no es Responsable Inscripto, `03` domicilio fiscal, `04` no autorizado a emitir clase A, `09` no autorizado a emitir A con leyenda (RG 5762, tipos 51-54) | El CUIT no tiene habilitada esa clase de comprobante en ARCA | Para `04`/`09`: la variante de Factura A configurada no coincide con la habilitada (ARCA la reevalúa cada trimestre); corregir la modalidad en Datos fiscales o el alta en ARCA |
| 10005 | Punto de venta no dado de alta o no habilitado para RECE | El punto de venta no existe en ARCA o es de otro sistema | Dar de alta un punto de venta "RECE para aplicativo y web services" |
| 10015 | Umbral de Factura B en pedidos múltiples | Según el manual, en una solicitud con varios comprobantes un monto de Factura B supera el umbral permitido sin identificar al receptor | Identificar al receptor o emitir los comprobantes por separado; NO es "CbteTipo no autorizado" |
| 1429 / 815 | Observación: no habilitado a emitir clase A a la fecha de emisión | El CUIT aún no estaba habilitado para esa clase en la fecha del comprobante | Revisar la habilitación en ARCA y la fecha de emisión |
| 10016 | El número del comprobante está fuera de secuencia | CbteDesde no es `lastAuthorized + 1` | Llamar `FECompUltimoAutorizado` y usar `+1` |
| 10017 | La fecha del comprobante está fuera del rango permitido | CbteFch >5 días en pasado o >5 en futuro | Validar fecha; AFIP permite ±5 días |
| 10018 | DocTipo no informado | Falta el campo DocTipo | Completar el campo |
| 10019 | DocNro inválido para el DocTipo | E.g. DocTipo=80 (CUIT) con DocNro de 8 dígitos | Validar formato del docnro |
| 10039 | Importe IVA no informado | ImpIVA=0 con factura A/M (debe haber IVA discriminado) | Calcular IVA correctamente |
| 10048 | Sumatoria de importes no coincide con ImpTotal | `ImpNeto + ImpIVA + ImpTrib + ImpOpEx + ImpTotConc != ImpTotal` | Validar suma exacta a 2 decimales |
| 10049 | Sumatoria de Iva[].Importe no coincide con ImpIVA | Error de redondeo en alícuotas | Recalcular cada Iva.Importe con `round_half_up` |
| 10054 | DocTipo no válido para este CbteTipo | Factura A/M con DocTipo distinto de 80 (CUIT) | Cambiar a CUIT o cambiar a factura B |
| 10063 | El receptor no está categorizado como RI | Factura A a un consumidor final | Cambiar a factura B |
| 10071 | Concepto no válido | Concepto fuera de {1, 2, 3} | Usar 1=Productos, 2=Servicios, 3=Ambos |

## Diagnostic flow

```
FECAESolicitar returned Resultado=R?
├─ Look at FECAEDetResponse[*].Observaciones[*].Code
│  ├─ 10016 → use FECompUltimoAutorizado, retry with +1
│  ├─ 10048/10049 → fix imports math
│  └─ 1004x/1005x/1006x → check field validity
└─ Look at top-level Errors[*].Code
   ├─ 600/601 → TA problem, refresh and retry once
   └─ 1001 → autorización en WSASS faltante
```

Para errores 6xx siempre vale la pena llamar `FEDummy` para descartar que AFIP esté caído.
