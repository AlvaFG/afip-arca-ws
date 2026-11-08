# Equipos homologados, documentos y reportes


## Impresoras fiscales (tipo 2, integrables con un punto de venta)

| Marca | Modelo | Versión | R.G. |
|---|---|---|---|
| Moretti | GÉNESIS | 01.00 | 4909 |
| Hasar | SMH/PT 1000F | 01.00 | 3809 |
| Hasar | SMH/PT-250F | 01.00 / 02.00 | 3954 / 4994 |
| Hasar | P-HAS-5100-FAR | 01.00 | 4528 |
| Epson | TM-T900FA | 01.00 "Ceres", 01.01 "Vesta", 01.02 "Jano", 01.03 "Neptuno" | 3954, 4206, 4528, 5067 |
| SAM4S | ELLIX 40 F | 01.00 / 01.01 | 4125 / 5001 |
| CRAMS | GX-9000 | 01.00 | 3954 |

Cajas registradoras (tipo 1, no integrables): Moretti CR KINDER, Hasar P-HAS-6100-FAR, Kretz NUM 100 TEA y LEGA 100 TEA, SAM4S NR 330 F.

El código actual solo conoce Hasar y Epson; qué marcas soportar es decisión de producto, no de norma. Antes de recomendar un modelo, confirmarlo con el fabricante o en la nómina de ARCA (si una versión vieja sigue vendiéndose: no confirmado).

## Documentos que emite (RG 3809, 4528, 4994)

| Código | Documento |
|---|---|
| 083 | Tique (consumidor final sin identificar) |
| 081 / 082 / 111 / 118 | Tique Factura A / B / C / M |
| 110 | Tique Nota de Crédito |
| 112 / 113 / 114 / 119 | Tique NC A / B / C / M |
| 115 / 116 / 117 / 120 | Tique ND A / B / C / M |
| 004 / 009 / 015 / 054 | Recibo / Tique Recibo A / B / C / M |
| 080 | Informe diario de cierre "Z" |
| 904 | Informe de auditoría |
| 9xx, 091 | No fiscales (remito X, presupuesto X, etc.): NO valen como factura |

- Controlador solo de tique (art. 18, texto RG 4444/2019 y RG 5700/2025): operaciones con inscriptos, exentos, monotributistas o consumidores finales a identificar van con comprobante electrónico (RG 4291), no con tique.
- Tique Factura / NC con receptor: datos del "Sector B del punto 1.1.2 del Capítulo B" del Anexo II. Contenido de ese sector: no confirmado (PDF escaneado).
- Clase C del monotributista "excepto tiques de controlador" contra el código 111 homologado: no confirmado, consultar contador.
- Consumidor final: identificación desde $10.000.000; ver `afip-arca-puntos-de-venta-y-modalidades`.

## Reportes y obligaciones del local con controlador

- Mensual (RG 3561 art. 19, RG 5801/2025): CTD (F. 8010) y Resumen de Totales (F. 8011), con "Presentación de DDJJ y Pagos - Controladores Fiscales" o webservice. Si un día no hubo movimientos, se emite un documento no fiscal antes de generar los reportes. Antes de dar de baja un equipo se envían sus reportes. La CTD puede ir en ZIP.
- Resguardo de la CTD con el plazo del art. 33 de la Ley 11.683; copias dentro de los 10 días del cierre del mes (Anexo II, Cap. B, pto. 1.5).
- Epson TM-T900FA 1.03 "Neptuno": archivo de rangos del fabricante para pasar las descargas a pendrive de semanales a mensuales (por comandos, SATF o "Epson Manager"). [FABRICANTE]
- Informe Z al cierre del día: obligatoriedad y frecuencia exactas, no confirmado (Anexo II).

## Contingencias (RG 4290 arts. 15 a 18, vigente 01/06/2026)

Controlador inoperable: electrónico (RG 4291), CAEA o RG 100. Webservice caído: CAEA primero; también vale un controlador de Nueva Tecnología. Usar contingencia en 5% o más de los comprobantes, dos meses seguidos o tres alternados en el año, rompe la excepcionalidad. Art. 14: en actividades del Anexo con consumidor final hay que tener habilitada una modalidad excepcional.
