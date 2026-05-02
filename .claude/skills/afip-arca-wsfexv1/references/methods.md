# WSFEXv1 Methods reference

## FEXDummy

Auth: **none required**. Returns 3 booleans `AppServer/DbServer/AuthServer` (same shape as WSFEv1's FEDummy). Use for connectivity check.

## FEXAuthorize

The main method: solicits a CAE for one export comprobante (no batch — one per call).

**Auth:** `{ Token, Sign, Cuit }`.

**Request body** (`Cmp`):

```
Id: int                  # internal ID for traceability (= Cbte_nro typically)
Fecha_cbte: string       # YYYYMMDD
Cbte_Tipo: int           # 19=Factura E, 20=NDé E, 21=NCr E
Punto_vta: int
Cbte_nro: long           # next number (use FEXGetLast_CMP first)
Tipo_expo: int           # 1=Bienes, 2=Servicios, 4=Otros
Permiso_existente: "S"|"N"  # destinación de exportación previa
Permisos: array of:      # required if Permiso_existente=S
  Id_permiso: string
  Dst_merc: int          # país destino mercadería
Dst_cmp: int             # país destino del comprobante (cliente)
Cliente: string
Cuit_pais_cliente: string
Domicilio_cliente: string
Id_impositivo: string    # tax ID del cliente en su país
Moneda_Id: string        # PES, DOL, 002, ...
Moneda_ctz: decimal      # cotización a ARS
Obs_comerciales: string  # opcional
Imp_total: decimal       # total en moneda extranjera
Obs: string              # opcional
Forma_pago: string       # libre, e.g. "Wire transfer 30 days"
Incoterms: string        # FOB, CIF, etc.
Incoterms_Ds: string     # descripción legible
Idioma_cbte: int         # 1=Esp, 2=Eng, 3=Por
Items:
  Item: array of:
    Pro_codigo: string
    Pro_ds: string
    Pro_qty: decimal
    Pro_umed: int        # unidad de medida desde FEXGetPARAM_UMed
    Pro_precio_uni: decimal
    Pro_total_item: decimal
```

**Response** (`FEXResultAuth`):

```
Cuit, Cbte_Tipo, Punto_vta, Cbte_nro
Fch_cbte: string         # YYYYMMDD
Cae: string              # 14 dígitos (vacío si Resultado=R)
Fch_venc_Cae: string
Resultado: A | R
Reproceso: S | N
Motivos_Obs: string      # texto plano de errores
```

## FEXGetLast_CMP

Get last authorized number for (Pto_venta, Cbte_Tipo).

```
Auth: { Token, Sign, Cuit, Pto_venta, Cbte_Tipo }
Response: FEXResult_LastCMP { Cbte_nro, Cbte_tipo, Fecha_cbte, ... }
```

Note: the auth-like object has the query fields **inside** the Auth header in this method (legacy SOAP design). Check WSDL.

## FEXGetCMP

Lookup an authorized comprobante.

## FEXGetLast_ID

Returns the last `Id` (internal traceability ID) used by this CUIT.

## FEXGetPARAM family

Enums published by AFIP:

- `FEXGetPARAM_Cbte_Tipo` — tipos de comprobante de export (19/20/21/etc.)
- `FEXGetPARAM_MON` — monedas
- `FEXGetPARAM_DST_pais` — países destino
- `FEXGetPARAM_Idiomas`
- `FEXGetPARAM_Incoterms`
- `FEXGetPARAM_Tipo_Expo`
- `FEXGetPARAM_UMed` — unidades de medida
- `FEXGetPARAM_PtoVenta`
- `FEXGetPARAM_Ctz` — cotización oficial de una moneda a una fecha (útil)

Cache 24h.

## FEXCheck_Permiso

Valida un permiso de exportación contra Aduana. Llamar antes de armar el Cmp si tu flujo lo requiere.
