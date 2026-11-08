---
name: afip-arca-puntos-de-venta-y-modalidades
description: Use when the work involves tipos de punto de venta de ARCA (web service vs "Controlador Fiscal"), modalidades de emisión (factura electrónica, controlador fiscal, ambas), duplicados electrónicos (RG 4290 art. 10 / RG 3685), identificación del consumidor final ($10.000.000, RG 5700/2025, "NR"), momento de entrega del comprobante, o qué comprobantes son válidos y no válidos. Triggers punto de venta, ABM puntos de venta, modalidad, duplicado electrónico, consumidor final, RG 4290, RG 5700, comprobante válido.
---

# ARCA — Puntos de venta y modalidades


## Reglas

- **Tipos de punto de venta.** Hay uno propio "Controlador Fiscal" (para quien usa controladores, RG 3561), distinto de los de factura electrónica por web service ("Factura Electrónica - RI IVA - Aplicativo y Webservices", "... Monotributo - Webservices"). Un local con controlador y el sistema de facturación por web service (WSFE) necesita **dos puntos de venta**, uno por modalidad. Un restaurante solo emite por el de web service. Un punto de venta bloqueado, dado de baja o CAEA no sirve para emitir por web service.
- **Modalidades.** Inscriptos, exentos y monotributistas (salvo inclusión social) usan controlador y/o factura electrónica, a elección y sin avisar. Excepción: una MiPyME que opera con una empresa grande u otra MiPyME adherida a Factura de Crédito Electrónica emite solo electrónico.
- **Duplicados electrónicos (RG 4290 art. 10).** Quien emite por web service a consumidores finales en una actividad del Anexo (restaurantes, bares, pizzerías, rotiserías) queda obligado a emitir y almacenar duplicados electrónicos (RG 3685, Título II, Caps. II a IV). Confirmado en la fuente oficial y **ya alcanza a los locales que facturan por web service**. Detalle en `references/duplicados-y-consumidor-final.md`. Si el sistema debe generar el archivo mensual: a decidir con un contador.
- **Consumidor final.** Identificación obligatoria desde $10.000.000 (RG 5700/2025; ya en `backend/src/constants/afip.ts`). Apellido, nombre y domicilio pueden ir como "NR". Sin actualización automática: un cambio de monto exige norma nueva.
- **Momento de entrega.** Con consumidores finales en locales, el comprobante se entrega al momento de la operación (al entregar la cosa o percibir el precio, lo primero), mínimo 2 ejemplares: original al cliente, duplicado al emisor.
- **Válidos:** facturas, tiques, tiques factura, notas de débito/crédito y tiques de ND/NC (solo las emite quien emitió la operación original).
- **No válidos:** documentos no fiscales de controladores homologados, remitos, notas de pedido, órdenes de trabajo, presupuestos, y recibos que respaldan un pago de una operación que debe facturarse.
- **Pendiente:** qué pasa con el punto de venta al cambiar de equipo y si un local puede tener varios PV de controlador: no confirmado, verificar en el ABM con un local real. La RG 5866/2026 (vigente 01/07/2026) reescribió el art. 47 de la RG 1415 (un PV dado de baja no se reactiva) [3RO].

## Relacionadas

`afip-arca-controlador-fiscal`, `afip-arca-wsfev1`, `afip-arca-overview`.
