# Monedas (`Moneda_Id`)

Source: `FEXGetPARAM_MON`. Subset común:

| Código | Moneda |
|---|---|
| PES | Peso Argentino |
| DOL | Dólar Estadounidense |
| 002 | Dólar Estadounidense (libre) |
| 009 | Yen japonés |
| 010 | Real brasileño |
| 011 | Peso Mexicano |
| 012 | Euro |
| 014 | Coronas danesas |
| 022 | Libra esterlina |

## Cotización (`Moneda_ctz`)

Es la cotización a ARS al momento de emitir la factura. Para USD:
- Llamá `FEXGetPARAM_Ctz(Mon_id="DOL", Fch_cotiz="20260502")` → returns `Mon_ctz`.
- Si no hay cotización oficial publicada para esa fecha (fines de semana, feriados), usá la última publicada y AFIP la acepta.
- Para PES, `Moneda_ctz = 1` siempre.

## Restricción

Las facturas de exportación solo aceptan moneda extranjera (no PES). Si necesitás factura en PES → usás WSFEv1, no WSFEXv1.
