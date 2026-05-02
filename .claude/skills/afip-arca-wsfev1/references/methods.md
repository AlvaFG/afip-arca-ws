# WSFEv1 Methods reference

## FEDummy

Auth: **none required**. Returns three booleans indicating subsystem health.

```
Response:
  AppServer: OK | NO
  DbServer:  OK | NO
  AuthServer: OK | NO
```

If any returns `NO`, AFIP itself is down — don't waste time debugging your code. Use this as the first check whenever something looks broken.

## FECAESolicitar

The main method: solicits a CAE for one or more comprobantes.

**Auth:** `{ Token, Sign, Cuit }` — Cuit is the emisor.

**Request body** (`FeCAEReq`):

```
FeCabReq:
  CantReg: int           # number of comprobantes in this batch (max 250)
  PtoVta:  int           # punto de venta
  CbteTipo: int          # tipo de comprobante (see tipos-comprobante.md)

FeDetReq:
  FECAEDetRequest: array of:
    Concepto: int        # 1=Productos, 2=Servicios, 3=Productos y Servicios
    DocTipo: int         # see tipos-doc.md (80=CUIT, 99=Consumidor Final)
    DocNro: long         # 0 if DocTipo=99
    CbteDesde: long      # numero del primer comprobante
    CbteHasta: long      # numero del último (= CbteDesde for single)
    CbteFch: string      # YYYYMMDD; up to ±5 days from today
    ImpTotal: decimal    # total bruto de la factura (must equal sum below)
    ImpTotConc: decimal  # importe neto no gravado
    ImpNeto: decimal     # importe neto gravado
    ImpOpEx: decimal     # importe operaciones exentas
    ImpIVA: decimal      # importe IVA
    ImpTrib: decimal     # importe otros tributos
    MonId: string        # PES (pesos) — for foreign currency use WSFEXv1
    MonCotiz: decimal    # 1 for PES
    Iva: array of:       # required when ImpIVA > 0 (except factura C)
      Id: int            # alicuota id (see alicuotas-iva.md)
      BaseImp: decimal
      Importe: decimal
```

**Response** (`FECAEResponse`):

```
FeCabResp:
  Resultado: A | R | P   # Approved / Rejected / Partial
  Cuit, PtoVta, CbteTipo, FchProceso, CantReg, Reproceso

FeDetResp:
  FECAEDetResponse: array of:
    Concepto, DocTipo, DocNro, CbteDesde, CbteHasta, CbteFch
    Resultado: A | R
    CAE: string          # 14 digits — present iff Resultado=A
    CAEFchVto: string    # YYYYMMDD vencimiento del CAE
    Observaciones:
      Obs: array of { Code: int, Msg: string }

Errors: array of { Code: int, Msg: string }
Events: array of { Code: int, Msg: string }
```

## FECompUltimoAutorizado

Get the last authorized comprobante number for a given (PtoVta, CbteTipo). Returns `0` if none yet.

```
Request:  Auth, PtoVta, CbteTipo
Response: PtoVta, CbteTipo, CbteNro
```

Always call this before `FECAESolicitar` to compute the next number.

## FECompConsultar

Lookup the data of an already-authorized comprobante. Useful for reconciliation.

```
Request:  Auth, FeCompConsReq { CbteTipo, CbteNro, PtoVta }
Response: ResultGet { Concepto, DocTipo, ..., CodAutorizacion (=CAE), FchProceso }
```

## FEParamGetTiposCbte / FEParamGetTiposDoc / FEParamGetTiposIva / FEParamGetTiposMonedas / FEParamGetPtosVenta

Enums published by AFIP. Cache locally with 24h TTL — they almost never change but do evolve (new factura types).

```
FEParamGetTiposCbte → array of { Id, Desc, FchDesde, FchHasta }
```

`FEParamGetPtosVenta` is special: it returns the puntos de venta authorized for **this CUIT** (the one in the TA). Useful to validate that your config matches reality before sending invoices.

## FECAEARegInformativo

Informa a AFIP de comprobantes cuyo CAE fue generado afuera (controlador fiscal, software del taxista, etc.). No genera CAE; solo registra. Estructura similar a `FECAESolicitar` con campo extra `CAEA`.

Si tu integración solo emite con CAE (no CAEA), ignorá este método.
