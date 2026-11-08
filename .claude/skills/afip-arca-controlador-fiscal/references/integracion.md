# Integración técnica con el equipo (todo PENDIENTE de decisión)


## Protocolos

- **Hasar 2G:** según el fabricante, protocolo empaquetado (ASCII CP437), XML o JSON; XML y JSON por HTTP. Cada respuesta trae "Estado Impresora" y "Estado Fiscal" que el programa debe analizar siempre; un comando rechazado responde solo con el estado; la respuesta trae numeradores para mantener sincronía. [FABRICANTE]
- Endpoint `POST http://<ip>/fiscal.json` con `{ "NombreComando": {...} }`: lo documenta un proyecto de terceros (gsaracca/FiscalClass). No confirmado contra el manual oficial.
- **Epson TM-T900FA:** existe un manual de especificaciones de comandos por versión de firmware y el asistente web "Epson Manager" (desde 1.03). Protocolo, transporte (USB/Ethernet) y si hay API HTTP/JSON: no confirmado; pedir el manual a Epson Argentina.
- Referencia abierta: Fiscalberry (servidor websocket en Python para Raspberry Pi; Hasar SMH/PT-250F y Epson TM-T900FA). Su readme dice Python 2.7: referencia, no dependencia.

## Dos caminos

| | Navegador directo | Agente local |
|---|---|---|
| Cómo | `fetch` del panel (https) al equipo (http, IP privada) | proceso en PC/Raspberry del local; conexión saliente a el sistema |
| Pros | nada que instalar | sin puertos ni CORS; cualquier navegador y app móvil; punto central para la regla de no reimprimir (consultar el último número del equipo antes de reintentar) |
| Contras | Chrome 142+ pide permiso de red local (`targetAddressSpace: "local"`); CORS de Hasar/Epson no confirmado (sin CORS no se lee la respuesta ni el número de tique); Safari, Firefox y Chrome móvil no confirmados | distribuir, firmar y actualizar un binario; PC encendida en el local |

Recomendación del runbook: agente local, backend ordena el tique (como con WSFE) e idempotencia por venta. La decisión es del dueño del producto.
