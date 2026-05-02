# Incoterms (`Incoterms` + `Incoterms_Ds`)

Source: `FEXGetPARAM_Incoterms`. Standard Incoterms 2020:

| Código | Descripción | Quién paga el flete |
|---|---|---|
| EXW | Ex Works | Comprador (desde la planta del vendedor) |
| FCA | Free Carrier | Comprador (vendedor entrega a transportista en origen) |
| CPT | Carriage Paid To | Vendedor paga transporte al destino convenido |
| CIP | Carriage and Insurance Paid To | Vendedor paga transporte + seguro |
| DAP | Delivered At Place | Vendedor entrega al lugar acordado |
| DPU | Delivered at Place Unloaded | Vendedor entrega + descarga |
| DDP | Delivered Duty Paid | Vendedor paga todo, incluso impuestos del país destino |
| FAS | Free Alongside Ship | Vendedor entrega al costado del buque (puerto origen) |
| FOB | Free On Board | Vendedor entrega a bordo del buque |
| CFR | Cost and Freight | Vendedor paga flete marítimo (no seguro) |
| CIF | Cost, Insurance and Freight | Vendedor paga flete + seguro marítimo |

## Reglas en el comprobante

- Tanto `Incoterms` (código) como `Incoterms_Ds` (descripción legible para el comprador) son requeridos.
- `Incoterms_Ds` es texto libre — puede repetir la descripción de la tabla o agregar contexto (e.g. `"FOB Buenos Aires Port, Argentina"`).
- Si el incoterm no está en la tabla AFIP, el WS rechaza con error 1505.
