---
source_url: "https://www.afip.gob.ar/ws/documentacion/wsaa.asp"
title: "Web Services SOAP"
---

# Web Services SOAP

## WSAA (Webservice de Autenticación y Autorización)

Para poder autenticarse ante el WSAA se requiere obtener un certificado digital X.509 emitido por la Autoridad Certificante de ARCA. La obtención de un certificado digital para usar en el entorno de testing se debe gestionar mediante la aplicación web WSASS (Autoservicio de Acceso a APIs de Homologación), que está disponible  [accediendo con clave fiscal](https://auth.afip.gob.ar/contribuyente_/login.xhtml ). Asimismo, para obtener un certificado digital para el entorno de producción se debe usar la aplicación web “Administrador de Certificados Digitales”.

Una vez obtenido el certificado digital, hay que asociarlo al Web Service de negocio al que se va a acceder. Esta asociación se realiza en la aplicación WSASS -para el caso del entorno de testing- o en la aplicación “Administrador de Relaciones de Clave Fiscal”, para el caso del entorno de producción.

- **Documentación**

  - [¿Cómo obtener el Certificado Digital para entorno de producción?](/ws/WSAA/wsaa_obtener_certificado_produccion.pdf)
  - [¿Cómo asociar el Certificado Digital a un WSN (Web Service de Negocio)?](/ws/WSAA/wsaa_asociar_certificado_a_wsn_produccion.pdf)
  - [Especificación Técnica del WebService de Autenticación y Autorización](/ws/WSAA/Especificacion_Tecnica_WSAA_1.2.2.pdf)
  - [Manual del Desarrollador del WSAA](/ws/WSAA/WSAAmanualDev.pdf)
- **Ejemplos de aplicaciones clientes del WSAA**

  #### [Código fuente Java](/ws/WSAA/ejemplos/wsaa_client_java.tgz)

  #### [Código fuente PHP](/ws/WSAA/ejemplos/wsaa-client-php.zip)

  #### [Código fuente C#](/ws/WSAA/ejemplos/dev-wsaa-cliente-dotnet-cs.zip)

  #### [Código fuente VB](/ws/WSAA/ejemplos/dev-wsaa-cliente-dotnet-vb.zip)

  #### [Código fuente PowerShell](/ws/WSAA/ejemplos/dev-wsaa-cliente-powershell.zip)
- **URLs**

  - Entorno de Testing del WSAA: <https://wsaahomo.afip.gov.ar/ws/services/LoginCms>
  - Entorno de Producción del WSAA: <https://wsaa.afip.gov.ar/ws/services/LoginCms>
