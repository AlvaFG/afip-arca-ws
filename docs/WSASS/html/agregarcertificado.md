---
source_url: "https://www.afip.gob.ar/ws/WSASS/html/agregarcertificado.html"
title: "CÓMO AGREGAR UN CERTIFICADO A UN ALIAS¶"
---

# CÓMO AGREGAR UN CERTIFICADO A UN ALIAS¶

### Navegación

- [siguiente](verservicios.html "CÓMO VER LOS SERVICIOS DISPONIBLES")
- [anterior](crearautorizacion.html "CÓMO CREAR UNA AUTORIZACION DE ACCESO") |
- [WSASS - MANUAL DEL USUARIO](index.html) »

#### Tema anterior

[CÓMO CREAR UNA AUTORIZACION DE ACCESO](crearautorizacion.html "capítulo anterior")

#### Próximo tema

[CÓMO VER LOS SERVICIOS DISPONIBLES](verservicios.html "próximo capítulo")

### Búsqueda rápida

Introduzca los términos de búsqueda o un nombre de módulo, clase o función.

# CÓMO AGREGAR UN CERTIFICADO A UN ALIAS[¶](#como-agregar-un-certificado-a-un-alias "Enlazar permanentemente con este título")

MENU

Opción: “Agregar Certificado a Alias” para acceder al formulario para solicitar la creación de un certificado adicional asociado a un DN existente.

Los campos a ingresar en el formulario son:

1. Nombre simbólico del DN. Es el alias o nombre simbólico del DN. Debe haberse creado previamente. Elegir el alias de la lista desplegable.
2. CUIT del DN. Es la CUIT del DN seleccionado en el Campo 1.
3. Nueva solicitud de certificado en formato PKCS10. Es la solicitud de certificado (Certificate Signing Request, CSR) en formato PKCS10. Se ignora el campo DN del CSR. Copiar y pegar en este campo el contenido del CSR generado oportunamente en su computuadora local.

Luego presionar “Crear Certificado Adicional para el DN”. Si no hay errores, el sistema devuelve un certificado x509 en formato PEM. Luego hay que copiarlo y pegarlo en un editor de texto plano, para grabarlo en su disco duro local.

### Navegación

- [siguiente](verservicios.html "CÓMO VER LOS SERVICIOS DISPONIBLES")
- [anterior](crearautorizacion.html "CÓMO CREAR UNA AUTORIZACION DE ACCESO") |
- [WSASS - MANUAL DEL USUARIO](index.html) »

© Copyright 2017, webservices-desa@afip.gob.ar.
