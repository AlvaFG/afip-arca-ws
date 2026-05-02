# Flujo TRA → TA, paso a paso

El objetivo es obtener un Ticket de Acceso (TA) firmado por AFIP que vas a usar como credencial en cada Web Service.

## Step 1 — Build the TRA XML

El TRA (Ticket de Requerimiento de Acceso) es un XML simple con:

- `uniqueId`: un identificador único, típicamente `int(time.time())`. Si en la misma sesión hacés dos requests al loginCms con el mismo uniqueId, AFIP devuelve `coe.alreadyAuthenticated`. Workaround: incrementar en 1 si chocás dentro del mismo segundo.
- `generationTime`: ISO 8601 con timezone, e.g. `2026-05-02T14:30:00-03:00`. Si está en el futuro respecto del reloj de AFIP en más de 2 minutos, el request se rechaza. Práctica común: `now - 60 segundos`.
- `expirationTime`: ISO 8601 con timezone, hasta 24h después del generationTime. AFIP devuelve igual un TA que expira en 12h. Práctica común: `now + 10 minutos` para limitar la ventana de uso del TRA si se filtra.
- `service`: el scope del WS al que vas a llamar después. Valores típicos: `wsfe`, `wsfex`, `ws_sr_padron_a4`, `ws_sr_padron_a5`, `ws_sr_padron_a13`. **El TA solo sirve para el service que pediste.**

Ejemplo:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<loginTicketRequest version="1.0">
  <header>
    <uniqueId>1714668600</uniqueId>
    <generationTime>2026-05-02T14:29:00-03:00</generationTime>
    <expirationTime>2026-05-02T14:40:00-03:00</expirationTime>
  </header>
  <service>wsfe</service>
</loginTicketRequest>
```

## Step 2 — Sign as CMS

El TRA se firma como PKCS#7/CMS embebido (NO detached) usando tu `.crt` + `.key`. Equivalente openssl:

```bash
openssl smime -sign \
  -in tra.xml \
  -signer cert.crt \
  -inkey private.key \
  -outform DER \
  -nodetach \
  -out tra.cms
```

El `-nodetach` es crucial: AFIP necesita que el contenido del TRA viaje dentro del CMS, no por separado. Si firmás detached, el sign verification del lado de AFIP falla con `cms.sign.invalid`.

## Step 3 — Base64 encode

El CMS binario (DER) se codifica en base64 sin saltos de línea para meterlo en el SOAP envelope:

```bash
base64 -w0 tra.cms > tra.cms.b64
```

En lenguajes con SDK de PKCS#7 (cryptography en Python, node-forge en Node, openssl_pkcs7_sign en PHP), generalmente ya devuelven base64 listo o un buffer DER que codificás vos.

## Step 4 — SOAP POST to loginCms

El envelope mínimo:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:wsaa="http://wsaa.view.sua.dvadac.desein.afip.gov">
  <soapenv:Body>
    <wsaa:loginCms>
      <wsaa:in0>{{CMS_BASE64}}</wsaa:in0>
    </wsaa:loginCms>
  </soapenv:Body>
</soapenv:Envelope>
```

POST a `https://wsaahomo.afip.gov.ar/ws/services/LoginCms` (homologación) o `https://wsaa.afip.gov.ar/ws/services/LoginCms` (producción) con `Content-Type: text/xml; charset=utf-8` y `SOAPAction: ""`.

Si usás un SOAP client (zeep, node-soap, SoapClient) le pasás el base64 al método `loginCms` y el envelope se arma solo.

## Step 5 — Parse the TA

La respuesta es:

```xml
<?xml version="1.0"?>
<loginTicketResponse version="1.0">
  <header>
    <source>CN=wsaahomo, ...</source>
    <destination>CN=mi-empresa, ...</destination>
    <uniqueId>1234567890</uniqueId>
    <generationTime>2026-05-02T14:30:00.000-03:00</generationTime>
    <expirationTime>2026-05-03T02:30:00.000-03:00</expirationTime>
  </header>
  <credentials>
    <token>PD94bWwgdmVyc2lvbj0iMS4wIj8+CjxzcyB2ZXJzaW9uPSIxLjAiPgo...</token>
    <sign>jUx5sTVG78sD9...</sign>
  </credentials>
</loginTicketResponse>
```

Lo que necesitás del TA en cada llamada posterior:
- `<credentials>/<token>` — string opaco, va en el campo `Token` del `Auth` del WS.
- `<credentials>/<sign>` — string opaco, va en el campo `Sign`.
- `<header>/<expirationTime>` — para saber cuándo invalidar el cache.

## WSDL endpoints

| Ambiente | URL |
|---|---|
| Homologación | `https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl` |
| Producción | `https://wsaa.afip.gov.ar/ws/services/LoginCms?wsdl` |
