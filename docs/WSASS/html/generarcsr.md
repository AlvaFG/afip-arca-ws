---
source_url: "https://www.afip.gob.ar/ws/WSASS/html/generarcsr.html"
title: "CÓMO GENERAR UNA SOLICITUD DE CERTIFICADO (CSR)¶"
---

# CÓMO GENERAR UNA SOLICITUD DE CERTIFICADO (CSR)¶

### Navegación

- [siguiente](crearcertificado.html "CÓMO CREAR UN CERTIFICADO NUEVO")
- [anterior](conceptos.html "CONCEPTOS BÁSICOS") |
- [WSASS - MANUAL DEL USUARIO](index.html) »

#### Tema anterior

[CONCEPTOS BÁSICOS](conceptos.html "capítulo anterior")

#### Próximo tema

[CÓMO CREAR UN CERTIFICADO NUEVO](crearcertificado.html "próximo capítulo")

### Búsqueda rápida

Introduzca los términos de búsqueda o un nombre de módulo, clase o función.

# CÓMO GENERAR UNA SOLICITUD DE CERTIFICADO (CSR)[¶](#como-generar-una-solicitud-de-certificado-csr "Enlazar permanentemente con este título")

Para obtener el certificado por primera vez, hay que dar de alta al DN. Para esto hay que presentar una “solicitud de certificado” o “Certificate Signing Request” (CSR). El CSR se genera en su computadora, usando la herramienta OpenSSL (disponible para Windows, UNIX/Linux y MacOSX). Primero hay que generar una clave privada en formato PKCS10 con un mínimo de 2048 bits:

```
openssl genrsa -out MiClavePrivada 2048
```

IMPORTANTE

Conserve el archivo de su clave privada en un lugar seguro.

Luego hay que generar el CSR propiamente dicho:

```
openssl req
    -new
    -key MiClavePrivada
    -subj "/C=AR/O=subj_o/CN=subj_cn/serialNumber=CUIT subj_cuit"
    -out MiPedidoCSR
```

donde hay que reemplazar:

- MiClavePrivada por nombre del archivo elegido en el primer paso.
- subj\_o por el nombre de su empresa
- subj\_cn por el nombre de su sistema cliente
- subj\_cuit por la CUIT (sólo los 11 dígitos, sin guiones) de la empresa o del programador (persona jurídica)
- MiClavePrivada por el nombre del archivo de la clave privada generado antes
- MiPedidoCSR por el nombre del archivo CSR que se va a crear

IMPORTANTE

Observar que en el serialNumber se escribe “CUIT” seguido de un espacio en blanco y a continuación los 11 dígitos de la CUIT sin separadores.

Por ejemplo, para una empresa llamada EmpresaPrueba, un sistema TestSystem, la CUIT 20123456789, con el archivo MiClavePrivada generado en el punto anterior:

```
openssl req
-new
-key MiClavePrivada
-subj "/C=AR/O=EmpresaPrueba/CN=TestSystem/serialNumber=CUIT 20123456789"
-out MiPedidoCSR
```

Si no hay errores, el archivo ‘MiPedidoCSR’ será utilizado al momento de obtener el DN y el certificado. El aspecto de un archivo CSR es similar a lo siguiente:

```
-----BEGIN CERTIFICATE REQUEST-----
MIIClTCCAX0CAQAwUDELMAkGA1UEBhMCQVIxEjAQBgNVBAoTCVNPUE9SVEVXUzES
MBAGA1UEAxMJU09QT1JURVdTMRkwFwYDVQQFExBDVUlUIDIwMTkwMTc4MTU0MIIB
IjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyu7TZTjKEdXEZPR4wIhFOw1S
...
QMNYAgJ/J2Zyy2JzxtsHzZDN1oM1SJbG9KyA5Rp02QZMMMsMWIIYKQLsoM5QAPQH
DWxkDa8dm7tBylM3u5+XT5G+w1xH4WjRHViAmUH2U+hTmaVAj7qSxsQzR/5HWoKX
cnMXsTGvi/5Y9q9kuOw6csm43z5XvxT4BBBKZn6FqWqSwUKxVuaJU8Q=
-----END CERTIFICATE REQUEST-----
```

### Navegación

- [siguiente](crearcertificado.html "CÓMO CREAR UN CERTIFICADO NUEVO")
- [anterior](conceptos.html "CONCEPTOS BÁSICOS") |
- [WSASS - MANUAL DEL USUARIO](index.html) »

© Copyright 2017, webservices-desa@afip.gob.ar.
