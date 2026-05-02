# SoapUI setup for AFIP

SoapUI Open Source es la herramienta gráfica clásica para inspeccionar y debuggear llamadas SOAP a AFIP cuando tu cliente programático devuelve faults raros y querés ver qué se está enviando exactamente.

## Setup paso a paso

1. Descargar SoapUI Open Source desde <https://www.soapui.org/downloads/soapui/>.
2. **File → New SOAP Project**.
3. **Project Name**: `AFIP-WSFEv1-homo` (o lo que estés debuggeando).
4. **Initial WSDL**: pegá la URL del WSDL, e.g. `https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL`.
5. SoapUI descarga el WSDL e arma una operación por método (FEDummy, FECAESolicitar, etc.).

## Cargar el certificado cliente

1. Bundle tu cert + key en `.p12` con `scripts/pem-to-p12.sh` desde `afip-arca-certificates`.
2. En SoapUI: **File → Preferences → SSL Settings**.
3. **KeyStore**: navegá al `.p12`.
4. **KeyStore Password**: la que pusiste al exportar.
5. **Required**: dejá unchecked (solo para servicios que requieran client cert obligatorio).
6. OK.

## Hacer una llamada

1. En el árbol del proyecto, expandí la operación (e.g. `FECAESolicitar`).
2. Doble click en `Request 1`. Te abre el editor de SOAP.
3. Reemplazá los placeholders `?` con tus valores reales (Token, Sign, Cuit, etc.).
4. Click en el ícono "play" (▶). SoapUI envía la request usando el cert configurado.
5. La respuesta aparece en el panel de la derecha.

## Tips útiles

- **HTTP log** (View → HTTP Log): ves los bytes exactos enviados y recibidos. Útil para detectar caracteres invisibles (BOM en el TRA, encoding raro).
- **TestSuite + Properties**: si querés repetir la llamada con diferentes inputs, armá una TestSuite con properties como `${#Project#cuit}` que vas cambiando.
- **Mock Service**: SoapUI puede simular AFIP localmente — útil para tests automatizados sin pegarle a homo.

## Alternativa: Postman

Si tu equipo ya usa Postman, hace lo mismo con SOAP — importás el WSDL como collection. Pero la integración con cert cliente en Postman es menos cómoda; SoapUI es lo que la mayoría usa para AFIP.
