---
source_url: "https://www.afip.gob.ar/ws/WSASS/html/conceptos.html"
title: "CONCEPTOS BÁSICOS¶"
---

# CONCEPTOS BÁSICOS¶

### Navegación

- [siguiente](generarcsr.html "CÓMO GENERAR UNA SOLICITUD DE CERTIFICADO (CSR)")
- [anterior](funcionalidades.html "FUNCIONALIDADES DISPONIBLES") |
- [WSASS - MANUAL DEL USUARIO](index.html) »

### [Tabla de Contenidos](index.html)

- [CONCEPTOS BÁSICOS](#)
  - [Autoservicio de certificados](#autoservicio-de-certificados)
  - [Gestión de accesos a servicios](#gestion-de-accesos-a-servicios)
  - [Delegación de representación](#delegacion-de-representacion)

#### Tema anterior

[FUNCIONALIDADES DISPONIBLES](funcionalidades.html "capítulo anterior")

#### Próximo tema

[CÓMO GENERAR UNA SOLICITUD DE CERTIFICADO (CSR)](generarcsr.html "próximo capítulo")

### Búsqueda rápida

Introduzca los términos de búsqueda o un nombre de módulo, clase o función.

# CONCEPTOS BÁSICOS[¶](#conceptos-basicos "Enlazar permanentemente con este título")

Usando el WSASS los programadores de aplicaciones pueden solicitar acceso a los diversos webservices (denominados “servicios”) que están disponibles en el ambiente de testing/homologación de la AFIP. Básicamente, el WSASS genera certificados digitales para testing. Dichos certificados digitales no son de aplicación para el ambiente de producción.

Para poder acceder a un servicio en ambiente de testing, la aplicación a programar debe utilizar el certificado generado en el WSASS. Entre otras cosas, el certificado contiene un Distinguished Name (DN) que incluye una CUIT. Cada DN será identificado por un “alias” o “nombre simbólico”, que actúa como una abreviación.

## Autoservicio de certificados[¶](#autoservicio-de-certificados "Enlazar permanentemente con este título")

Para obtener el certificado, distinguimos dos casos según si el DN ya fué dado de alta (DN existente) o si aún no existe. Para eso utilizar uno de los formularios siguientes:

- Formulario para obtener el certificado por primera vez (menú: Nuevo Certificado).
- Formulario para obtener otro certificado adicional para un DN existente (menú: Agregar Certificado a Alias).
- Ver los certificados emitidos para una CUIT (menú: Certificados).

## Gestión de accesos a servicios[¶](#gestion-de-accesos-a-servicios "Enlazar permanentemente con este título")

Una vez generado el DN y obtenido el certificado, se puede gestionar la autorización de acceso a los servicios de AFIP, utilizando los siguientes formularios:

- Formulario de solicitud de autorización de acceso a servicio (menú: Crear Autorización a Servicio).
- Formulario para eliminar una autorización de acceso a servicio (menú: Eliminar Autorización a Servicio).
- Ver el catálogo de servicios disponibles (menú: Servicios).

## Delegación de representación[¶](#delegacion-de-representacion "Enlazar permanentemente con este título")

Una vez obtenido el certificado, se puede delegar la representación mediante la opción del menú Crear Autorización a Servicio, donde en el campo “CUIT representado” se debe colocar la CUIT a representar y además se debe seleccionar el servicio deseado.

### Navegación

- [siguiente](generarcsr.html "CÓMO GENERAR UNA SOLICITUD DE CERTIFICADO (CSR)")
- [anterior](funcionalidades.html "FUNCIONALIDADES DISPONIBLES") |
- [WSASS - MANUAL DEL USUARIO](index.html) »

© Copyright 2017, webservices-desa@afip.gob.ar.
