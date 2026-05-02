# Reglas de caching del TA

## Why caching is mandatory

AFIP rate-limita `loginCms` agresivamente. En producción, llamarlo en cada request al WS resulta en:

1. Latencia agregada de ~500ms por request (handshake TLS + WSAA call).
2. Cuando AFIP detecta un patrón de abuso, suspende temporalmente el cert por horas.
3. En picos de tráfico, el TA se vuelve cuello de botella aún antes de llegar al WS de negocio.

El TA es válido por 12h por design — el sistema se diseñó con caching como pre-requisito, no como optimización.

## Cache key

La clave de cache es la tupla `(cuit, service, environment)`:

- `cuit`: el CUIT del emisor (no el del cert, que en general son el mismo pero pueden no serlo en escenarios de delegación).
- `service`: scope del TA, e.g. `wsfe`, `wsfex`, `ws_sr_padron_a4`. Distintos services requieren distintos TAs.
- `environment`: `homo` o `prod`. Nunca compartas TA entre ambientes.

## Storage options

### Filesystem (single instance, simplest)

Un archivo por (service, env), e.g. `cache/ta-wsfe-prod.xml`. Cargás al startup y antes de cada uso checkeás expiration. Lock file (`flock`) para evitar dos procesos refrescando simultáneamente.

```python
def get_ta(service, env):
    path = Path(f"cache/ta-{service}-{env}.xml")
    if path.exists():
        ta = parse(path)
        if ta.expiration > now() + timedelta(minutes=5):
            return ta
    return refresh_ta(service, env, path)  # acquires lock, writes, returns
```

### Database (multi-instance)

Tabla `afip_ta(cuit, service, env, token, sign, expires_at, created_at)` con PK = `(cuit, service, env)`. Antes de usar, `SELECT ... WHERE expires_at > NOW() + INTERVAL '5 minutes'`. Si miss, lock de fila y refresh.

### In-memory + lock (workers cortos)

Para procesos efímeros (lambdas, workers en cola), in-memory dict con un mutex. No persiste entre invocations — cada cold start hace un loginCms. Aceptable si el volume es bajo.

## Concurrency

Cuando N workers piden el TA al mismo tiempo:

```
Worker 1: TA expirado → empieza refresh
Worker 2: TA expirado → empieza refresh (¡colisión!)
Worker 3: TA expirado → empieza refresh
```

Esto es el patrón "thundering herd" y es la causa #1 de bloqueos en AFIP.

Solución: double-checked locking.

```python
def get_or_refresh_ta(key):
    ta = cache.get(key)
    if ta and not ta.is_expired():
        return ta
    with lock(key):  # named lock, e.g. Postgres advisory lock or Redis SETNX
        ta = cache.get(key)  # check again — another worker may have refreshed
        if ta and not ta.is_expired():
            return ta
        ta = wsaa_login(key)
        cache.set(key, ta)
        return ta
```

## When to invalidate

- **Cert renewed**: drop all cached TAs (TA está firmado por el cert que ya no existe).
- **WS returns "TA expired" error (600/601 in WSFEv1)**: refresh y reintentar 1 vez.
- **Tiempo restante < 5 min**: refresh proactivo para no romper requests in-flight.
- **Cambio de ambiente** (test → prod): no compartir, son keys distintas.
