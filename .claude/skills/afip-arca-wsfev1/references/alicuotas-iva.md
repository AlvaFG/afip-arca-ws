# Alícuotas de IVA (`Iva.Id`)

Source: `FEParamGetTiposIva`.

| Código | Alícuota | Cómo se calcula |
|---|---|---|
| 3 | 0% | `Importe = 0` (úsalo solo si la operación está gravada al 0%) |
| 4 | 10.5% | `Importe = round2(BaseImp * 0.105)` |
| 5 | 21% | `Importe = round2(BaseImp * 0.21)` |
| 6 | 27% | `Importe = round2(BaseImp * 0.27)` |
| 8 | 5% | `Importe = round2(BaseImp * 0.05)` |
| 9 | 2.5% | `Importe = round2(BaseImp * 0.025)` |

## Worked example — alícuota 21%

```
ImpNeto    = 100.00
Iva.Id     = 5
Iva.BaseImp = 100.00
Iva.Importe = round(100.00 * 0.21, 2) = 21.00

ImpIVA     = 21.00     (suma de Iva[].Importe — solo el campo agregado)
ImpTotal   = 121.00    (ImpNeto + ImpIVA + ImpTotConc + ImpOpEx + ImpTrib)
```

## Multiple alícuotas en una sola factura

```
ImpNeto    = 150.00   (=100 al 21% + 50 al 10.5%)
Iva: [
  { Id: 5, BaseImp: 100.00, Importe: 21.00 },
  { Id: 4, BaseImp:  50.00, Importe:  5.25 }
]
ImpIVA     = 26.25
ImpTotal   = 176.25
```

## Redondeo

Usá **round-half-up** a 2 decimales (matemáticamente: 0.5 → arriba). En Python: `Decimal('0.105').quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)`. En PHP: `round(x, 2, PHP_ROUND_HALF_UP)`. En JS: hand-roll porque `Math.round` usa banker's rounding inconsistentemente — `Math.round(x * 100) / 100` está bien para la mayoría de los casos.

Si la suma `Iva[].Importe` no coincide con `ImpIVA` por error de redondeo de centavos, AFIP devuelve `10048` y rechaza la factura entera.
