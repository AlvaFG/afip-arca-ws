# Historial del manual WSFEv1 (v4.0 en adelante)

Fuente: "Manual para el desarrollador RG 4291 – Proyecto FE v4.8", revisión del 1/12/2026,
<https://www.afip.gob.ar/fe/ayuda/documentos/wsfev1-RG-4291.pdf> (leído el 2026-11-08).
Las fechas son de vigencia. Antes de implementar algo de una versión futura, releer el manual.

| Ver | Vigencia | Cambio |
|---|---|---|
| 4.0 | 2025-03-17 | Campos `CanMisMonExt` y `CondicionIVAReceptorId`; método `FEParamGetCondicionIvaReceptor`; `FEParamGetCotizacion` acepta fecha. Enviar la condición IVA del receptor es opcional desde 2025-04-06 hasta que entre la obligatoriedad (RG 5616). |
| 4.1 | 2025-12-01 | Reemplazo de comprobantes clase M; cambia `FEParamGetCondicionIvaReceptor` y las descripciones de 814, 815, 1444, 1516, 10000, 10007, 10012, 10013, 10017, 10061, 10063, 10149, 10217, 10234, 10244. |
| 4.2 | 2026-02-01 | Validaciones de alertas y monitoreo: CAE 10247-10249, CAEA 827-829. |
| 4.3 | 2026-06-01 | Opcionales de comprobantes 63 y 64 (liquidaciones); CAEA 1517-1526; se modifican CAE 10068 y CAEA 700, 807, 1426, 15000; 15001 en desuso. |
| 4.4 | 2026-07-01 | Entidades financieras y seguros (RG 5866): CAE 10251. |
| 4.5 | 2026-07-02 | Tipo de documento receptor 31 "Fondo Común de Inversiones CNV"; CAE 10270-10272. |
| 4.6 | 2026-08-01 | CAEA (RG 5782): todos los puntos de venta CAEA pasan a ser Contingencia, deben asociarse a un domicilio de factura electrónica, y `CbteFchHsGen` pasa a ser obligatorio. Se modifica 15014; nuevos 15016 y 15017. |
| 4.7 | 2026-09-01 | Seguros de caución: CAE 10273-10282 y cambio en 10054. Comprobantes B con receptor Sujeto No Categorizado: CAE 10283, CAEA 1527; se modifican 10067 y 1425. Alertas: CAE 10284, CAEA 1528. |
| 4.8 | 2026-12-01 | **`CondicionIVAReceptorId` obligatorio** (RG 5616). Los códigos 10245 (CAE) y 825 (CAEA) quedan en desuso. |
