# Common errors flowchart

```
AFIP request failed
│
├─ Type of failure?
│
├─ TLS handshake / connection refused / SSL error
│  ├─ Cert env mismatch?
│  │  └─ check ENV in URL (wsaa vs wsaahomo) vs el ambiente del cert → cambiar uno
│  ├─ Cert expired?
│  │  └─ openssl x509 -enddate → renovar
│  ├─ Reloj del server desincronizado?
│  │  └─ ntpdate o systemd-timesyncd
│  └─ Firewall / proxy bloqueando?
│     └─ curl -v desde el server → buscar "Could not resolve"/"Connection timed out"
│
├─ HTTP 200 con SOAP fault de WSAA loginCms
│  ├─ "cms.cert.untrusted" → cert env mismatch
│  ├─ "cms.cert.expired" → renovar
│  ├─ "cms.sign.invalid" → key/cert pair mismatch o firma detached
│  ├─ "coe.alreadyAuthenticated" → uniqueId reusado, bumpear
│  └─ "xml.generationTime.invalid" → reloj o tz mal
│
├─ HTTP 200 con SOAP fault de FECAESolicitar / FEXAuthorize
│  ├─ Errors[].Code = 600/601 → TA inválido, refresh y retry 1 vez
│  ├─ Errors[].Code = 1001 → cert no autorizado en WSASS para este WS
│  ├─ Observaciones[].Code = 10016 → numero fuera de secuencia, llamar FECompUltimoAutorizado
│  ├─ Observaciones[].Code = 10048/10049 → math wrong, recomputar imports con round_half_up
│  └─ Otros 1004x/1005x → revisar reference de error-codes del servicio
│
├─ Request hangs / timeout
│  ├─ FEDummy también falla? → AFIP down, esperar
│  ├─ Solo este WS falla? → sobrecarga, retry con backoff exponencial
│  └─ Tu lado: connection pool exhausted? → tunear cliente HTTP
│
├─ HTTP 5xx (raro pero pasa)
│  ├─ 500 con HTML body → AFIP hizo deploy y rompió el WS — esperar
│  ├─ 502/503 → balanceador AFIP, retry
│  └─ 504 → timeout del backend, retry
│
└─ Algo que no encaja arriba
   └─ Llamar FEDummy primero. Si sale OK pero tu request falla, es problema de tu request específico — usar SoapUI para comparar.
```

## "Mi código andaba ayer y hoy no"

Ranking por probabilidad:
1. **El TA expiró** y tu cache está en RAM (worker reiniciado).
2. **AFIP cambió algo silencioso** en el WSDL (raro pero pasa). Re-bajá el WSDL y compará.
3. **El cert venció** mientras nadie miraba. `openssl x509 -enddate`.
4. **Cambiaron el reloj del servidor** (DST, hostname switch). `date -u` y comparar con un NTP.
