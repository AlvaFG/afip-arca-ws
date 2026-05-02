---
source_url: "https://www.afip.gob.ar/ws/WSASS/html/crearcertificado.html"
title: "CÓMO CREAR UN CERTIFICADO NUEVO¶"
---

# CÓMO CREAR UN CERTIFICADO NUEVO¶

### Navegación

- [siguiente](crearautorizacion.html "CÓMO CREAR UNA AUTORIZACION DE ACCESO")
- [anterior](generarcsr.html "CÓMO GENERAR UNA SOLICITUD DE CERTIFICADO (CSR)") |
- [WSASS - MANUAL DEL USUARIO](index.html) »

### [Tabla de Contenidos](index.html)

- [CÓMO CREAR UN CERTIFICADO NUEVO](#)
  - [Obtención del certificado](#obtencion-del-certificado)
  - [Cómo crear un archivo PFX con clave privada](#como-crear-un-archivo-pfx-con-clave-privada)

#### Tema anterior

[CÓMO GENERAR UNA SOLICITUD DE CERTIFICADO (CSR)](generarcsr.html "capítulo anterior")

#### Próximo tema

[CÓMO CREAR UNA AUTORIZACION DE ACCESO](crearautorizacion.html "próximo capítulo")

### Búsqueda rápida

Introduzca los términos de búsqueda o un nombre de módulo, clase o función.

# CÓMO CREAR UN CERTIFICADO NUEVO[¶](#como-crear-un-certificado-nuevo "Enlazar permanentemente con este título")

## Obtención del certificado[¶](#obtencion-del-certificado "Enlazar permanentemente con este título")

MENU

Opción: “Nuevo Certificado” para acceder al formulario para crear un DN y el certificado inicialmente asociado al mismo.

Los campos a ingresar en el formulario son:

1. Nombre simbólico del DN. Es el alias o nombre simbólico del DN a crear. Este será el identificador por lo que debe ingresar un alias que no exista.
2. CUIT del contribuyente. Es la CUIT del contribuyente (persona física). Debe ser la mismo CUIT que se incluyó en la solicitud del certificado CSR (en el campo serialNumber del CSR). Este campo tiene automáticamente la CUIT del usuario conectado al WSASS y no puede editarse.
3. Solicitud de certificado en formato PKCS10. Es la solicitud de certificado (Certificate Signing Request, CSR) en formato PKCS10. El CSR debe contener en el SerialNumber el valor “CUIT nnnnn”, donde nnnnn es el número de CUIT del usuario conectado al WSASS.

Luego presionar “Crear DN y Obtener Certificado”. Si no hay errores, el sistema devuelve un certificado x509 en formato PEM. El aspecto del certificado es similar a lo siguiente:

```
-----BEGIN CERTIFICATE-----
MIIDSzCCAjOgAwIBAgIIS7JIkcfpQhswDQYJKoZIhvcNAQENBQAwMzEVMBMGA1UEAwwMQ29tcHV0
YWRvcmVzMQ0wCwYDVQQKDARBRklQMQswCQYDVQQGEwJBUjAeFw0xNjA5MzAxMTUzMjhaFw0xODA5
MzAxMTUzMjhaMDYxGTAXBgNVBAMMEENlcnRfZ2xhcnJpZXJhXzExGTAXBgNVBAUTEENVSVQgMjAx
OTAxNzgxNTQwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDK7tNlOMoR1cRk9HjAiEU7
...
z2JEQXFPkcxcG6DE9v4Q/8WSaiPRxbzjOkC5+cEuEtqxlwGsCDeFjSRco05XFWmzXg8jLrJIEk8l
jFRvrIR9Shm/p6RxU6ZeBkyeNAu3c5ShTyL0tntIEoXDpx4wqZ2ZkA4tinmbbI7LnnCyaniKw27h
bkQkLybJPc1LIzJb9tRzFQUu9PreRj1ggnhzzo/qtCicv6oVoi7nZW05lO5mG8JxJQhEFfnVgZqw
0QRQQb4/Ouequfgw84C1/dD2TKH9RsjiJ8tiVvsCuz5tjkb727tH/ZW3ce2bG9t4QQ==
-----END CERTIFICATE-----
```

Luego hay que copiarlo y pegarlo en un editor de texto plano, para grabarlo en su disco duro local (por ejemplo, en un archivo certificado.pem).

NOTA

El DN del certificado creado tiene el formato “SERIALNUMBER=CUIT nnnnnnnnnnn, CN=xxxxx”, donde ‘nnnnnnnnnnn’ es el número de la CUIT y ‘xxxxx’ es el alias que se indicó. Este formato es por diseño y no puede modificarse.

NOTA

Los certificados creados no pueden ser eliminados, ni aún después de su fecha de expiración. El usuario puede crear todos los certificados que crea necesario.

## Cómo crear un archivo PFX con clave privada[¶](#como-crear-un-archivo-pfx-con-clave-privada "Enlazar permanentemente con este título")

El formato PFX o PKCS#12 es un formato binario para almacenar el certificado del servidor, los certificados intermedios y la clave privada, todo en un único archivo encriptado. Los archivos PFX usualmente tienen la extensión .pfx o .p12 y son típicamente usados en Windows para importar o exportar certificados y claves privadas.

Si se necesita crear un archivo PFX se puede usar OpenSSL. Por ejemplo:

```
openssl pkcs12
-export
-inkey MiClavePrivada
-in certificado.pem
-out certificado.pfx
```

donde MiClavePrivada es la clave privada usada cuando se generó el CSR, certificado.pem es el certificado x509 en formato PEM obtenido usando el WSASS y certificado.pfx será el nuevo archivo PFX conteniendo al certificado firmado.

### Navegación

- [siguiente](crearautorizacion.html "CÓMO CREAR UNA AUTORIZACION DE ACCESO")
- [anterior](generarcsr.html "CÓMO GENERAR UNA SOLICITUD DE CERTIFICADO (CSR)") |
- [WSASS - MANUAL DEL USUARIO](index.html) »

© Copyright 2017, webservices-desa@afip.gob.ar.
