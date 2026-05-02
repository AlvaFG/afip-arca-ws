# WSAA error codes

| Código / Mensaje | Causa típica | Fix |
|---|---|---|
| `coe.alreadyAuthenticated` | TRA reusado: mismo uniqueId enviado dos veces dentro del mismo minuto | Bumpear el uniqueId (sumar 1) o esperar 60s |
| `cms.cert.untrusted` | Cert no firmado por una CA confiable para AFIP, o cert de homologación contra prod (o viceversa) | Verificar el ambiente del cert vs URL del WSAA |
| `cms.cert.expired` | El cert cliente ya pasó su `notAfter` | Renovar cert (ver `afip-arca-certificates/references/renewal-checklist.md`) |
| `cms.bad_audience` | Cert para `wsaahomo` se usó contra `wsaa` (prod) o al revés | Usar el cert correspondiente al ambiente |
| `cms.sign.invalid` | La firma CMS no validó. Causas: clave privada no coincide con el cert, firma detached en lugar de embebida, formato PEM/DER mezclado | Verificar `openssl x509 -modulus` vs `openssl rsa -modulus`. Asegurar `-nodetach` al firmar |
| `xml.generationTime.invalid` | `generationTime` está fuera del rango aceptado (>2 min en futuro o demasiado en pasado) | Sincronizar reloj del servidor (NTP). Usar `now - 60s` |
| `xml.expirationTime.invalid` | `expirationTime <= generationTime` o `expirationTime > generationTime + 24h` | Validar antes de firmar: expiration entre generation+1min y generation+12h |
| `cms.cert.notFound` | Cert no autorizado en WSASS para el `service` solicitado | Ir a "Administrador de Relaciones" y autorizar el alias para el service |
| `xml.service.notAllowed` | El service del TRA no está habilitado para este CUIT | Revisar autorizaciones por service en WSASS |

## Diagnostic flow

```
loginCms returned a SOAP fault?
├─ Starts with "cms." → certificate or signing problem
│  ├─ cms.cert.* → check cert validity + environment match
│  └─ cms.sign.invalid → check key/cert pair and -nodetach
├─ Starts with "xml." → TRA structure problem
│  └─ Adjust generation/expiration times to within window
├─ "coe.alreadyAuthenticated" → uniqueId collision
│  └─ Increment uniqueId, retry
└─ Connection-level error (no SOAP fault) → afip-arca-debugging
```
