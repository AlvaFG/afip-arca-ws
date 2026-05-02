# FEDummy / FEXDummy connectivity checks

Todos los servicios de facturación tienen un método "dummy" que NO requiere autenticación y devuelve 3 booleans:

```
AppServer:  OK | NO    # el servidor de aplicación está vivo
DbServer:   OK | NO    # el motor de DB respondió
AuthServer: OK | NO    # el servicio de autenticación interno responde
```

Si los tres son OK, AFIP está sano y el problema es tu lado. Si alguno es NO, AFIP está degradado — esperá y reintentá.

## WSFEv1 FEDummy

URL homo: `https://wswhomo.afip.gov.ar/wsfev1/service.asmx`
URL prod: `https://servicios1.afip.gov.ar/wsfev1/service.asmx`
SOAPAction: `http://ar.gov.afip.dif.FEV1/FEDummy`

Body:
```xml
<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <FEDummy xmlns="http://ar.gov.afip.dif.FEV1/" />
  </soap:Body>
</soap:Envelope>
```

## WSFEXv1 FEXDummy

URL homo: `https://wswhomo.afip.gov.ar/wsfexv1/service.asmx`
URL prod: `https://servicios1.afip.gov.ar/wsfexv1/service.asmx`
SOAPAction: `http://ar.gov.afip.dif.fex/FEXDummy`

Body:
```xml
<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <FEXDummy xmlns="http://ar.gov.afip.dif.fex/" />
  </soap:Body>
</soap:Envelope>
```

## Padrón dummy

Hay un método `dummy()` por servicio (A4, A5, A13). Mismo formato pero con namespace propio. Útil para verificar que tu cert está autorizado contra ese WS específico (el dummy NO requiere auth pero la conectividad TLS sí da pistas de configuración).

## Quick script

`scripts/test-fedummy.sh` automatiza FEDummy + FEXDummy con un argumento `homo`/`prod`.
