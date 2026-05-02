# Generar CSR para AFIP/ARCA

Pasos para generar la clave privada y el CSR (Certificate Signing Request) que después subís al portal de AFIP/ARCA para obtener tu `.crt`.

## 1. Generate the private key

Generá una clave RSA de 2048 bits (suficiente para AFIP; 4096 si tu política interna lo requiere y aceptás operaciones más lentas).

```bash
openssl genrsa -out private.key 2048
chmod 600 private.key
```

**Importante:** la clave NUNCA se sube a AFIP. Solo se usa localmente para firmar TRAs en el flujo WSAA. Si la perdés, tenés que generar una nueva y volver a obtener el `.crt`.

## 2. Build the openssl.cnf

Para evitar el modo interactivo de `openssl req`, usá un archivo de config. Ver `assets/openssl.cnf.tmpl` en esta skill — copialo, reemplazá los placeholders `{{ALIAS}}`, `{{CUIT}}`, `{{ORGANIZACION}}`. Los campos requeridos por AFIP son:

- **CN** = el alias que vas a usar (e.g. `mi-empresa-prod`). Este alias también es lo que vas a especificar al autorizar el cert para cada Web Service.
- **O** = razón social de la organización.
- **serialNumber** = `CUIT <11-dígitos>` (con espacio). Sin guiones, sin puntos.
- **C** = `AR`.

## 3. Generate the CSR

Con el openssl.cnf armado:

```bash
openssl req -new -config openssl.cnf -key private.key -out request.csr
```

O todo en una línea sin archivo de config:

```bash
openssl req -new -key private.key \
  -subj "/C=AR/O=Mi Organizacion/CN=mi-empresa-prod/serialNumber=CUIT 20111111112" \
  -out request.csr
```

Para el flujo automatizado, usá `scripts/generate-csr.sh` que también valida el formato del CUIT.

## 4. Verify the CSR locally

Antes de subirlo, confirmá que los datos son correctos:

```bash
openssl req -in request.csr -text -noout | head -20
```

Buscá en la salida la línea `Subject:` y verificá que coincida exactamente con lo que querés. Cualquier diferencia (typo en el CUIT, nombre incorrecto) significa empezar de nuevo.

## 5. What to upload

Solo subí el archivo `request.csr` al portal de AFIP. **Nunca subas la clave privada (`private.key`)** — si AFIP, un proveedor o cualquier third-party te pide la clave privada, es un intento de fraude.

El `.crt` que recibís de vuelta lo guardás junto a la clave privada con permisos `600`. Para la próxima renovación (en 2 años), generás un nuevo CSR pero **mantenés el mismo CN/alias** para no tener que re-autorizar el cert en cada Web Service.
