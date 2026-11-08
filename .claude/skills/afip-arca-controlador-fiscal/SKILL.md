---
name: afip-arca-controlador-fiscal
description: Use when the work involves controladores fiscales (impresoras fiscales Hasar, Epson, Moretti, SAM4S, CRAMS), RG 3561, tique / tique factura, informe Z, cinta testigo digital, `fiscal_mode='fiscal_controller'`, `fiscalController.service.ts`, comandas con importes, or whether a restaurant must use a controlador. Triggers controlador fiscal, impresora fiscal, tique fiscal, RG 3561, RG 4290, Hasar, Epson TM-T900FA, nueva tecnología, transparencia fiscal.
---

# ARCA — Controlador fiscal (RG 3561)


## Reglas que no hay que romper

- **El controlador NO es obligatorio.** El Capítulo C de la RG 3561 (actividades alcanzadas) lo derogó la RG 4292/2018. Por RG 4290 arts. 6 y 7 (texto RG 5893/2026, vigente 01/11/2026) el local elige factura electrónica, controlador, o las dos, sin avisar a ARCA. Los restaurantes figuran en el Anexo de la RG 4290, pero eso no obliga a tener controlador.
- **Solo equipos homologados.** Para integrar con un punto de venta sirven las impresoras fiscales (tipo 2); las cajas registradoras (tipo 1) son autónomas y no se manejan desde un sistema. Nómina en `references/equipos-y-documentos.md`.
- **Un ticket fiscal impreso no se reimprime** (regla de producto del dueño). Un reintento tras fallar el POST al backend no puede volver a mandar el ticket al equipo: se guarda el resultado del controlador (id y número) y se reenvía al backend. El PDF de la factura es otra cosa: es libre. Ningún local usa `fiscal_mode='fiscal_controller'` al 2026-10-23.
- **El tique no tiene CAE ni QR de ARCA.** el sistema no genera el QR `fe/qr` para un tique (ese QR codifica un CAE). WSCDC no constata tiques. Lo respaldan la memoria fiscal y los reportes mensuales.
- **Documentos no fiscales no valen como factura** (RG 3561 art. 16).
- **Comandas con importes:** quien usa controlador no puede emitir por otro medio comandas con valores monetarios (RG 3561 art. 16). Alcance exacto para precuentas y comandas de el sistema (`printing.service.ts`): no confirmado, falta contador.
- **Transparencia fiscal (RG 5614/2024, desde 01/04/2025):** el tique a consumidor final muestra "IVA Contenido" y "Otros Impuestos Nacionales Indirectos". Las impresoras homologadas antes lo informan en las "líneas libres del usuario" (art. 4), así que el sistema tiene que enviar esas líneas en cada tique a consumidor final. Que ARCA haya homologado firmware nuevo de impresora para esto: no confirmado.
- **Reportes mensuales** (art. 19, texto RG 5801/2025, desde el período enero 2026): CTD (F. 8010) y Resumen de Totales (F. 8011), aunque no haya movimientos; vencen el día 5 (inscriptos y exentos) o 7 (monotributo) del mes siguiente. Detalle en `references/equipos-y-documentos.md`.
- **Punto de venta propio:** el controlador usa un tipo de punto de venta "Controlador Fiscal", distinto del de web service. Un local con controlador y el sistema de facturación por web service (WSFE) necesita dos puntos de venta. Ver `afip-arca-puntos-de-venta-y-modalidades`.

## Estado del código (tomarlo como inexistente)

`web/src/services/fiscalController.service.ts` llama a `POST /api/fiscal/ticket` (Hasar) y `POST /cgi-bin/fpmate/fiscal` (Epson). No apareció ninguna fuente de esos endpoints para equipos argentinos y no coinciden con lo documentado para Hasar 2G (`fiscal.json`, comandos con nombre). Hay que reescribirlo contra el manual oficial de cada equipo. Los manuales de comandos y el CORS de los equipos: no confirmado.

## Arquitectura (PENDIENTE de decisión del dueño)

El runbook recomienda un **agente local** (PC o Raspberry del local que habla con el equipo por USB/serie/LAN y con el sistema por conexión saliente), con el backend ordenando el tique e idempotencia por venta. Alternativa: navegador directo contra el equipo (Local Network Access de Chrome 142+), que depende de CORS no confirmado y de un solo navegador de escritorio. No implementar ninguna de las dos hasta que el dueño decida. Comparación en `references/integracion.md`.

## Relacionadas

`afip-arca-puntos-de-venta-y-modalidades` (tipos de PV, duplicados electrónicos, consumidor final), `afip-arca-wsfev1` (el otro canal), `afip-arca-overview`.
