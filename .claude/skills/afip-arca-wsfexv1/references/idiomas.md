# Idiomas del comprobante (`Idioma_cbte`)

Source: `FEXGetPARAM_Idiomas`.

| Código | Idioma |
|---|---|
| 1 | Español |
| 2 | Inglés |
| 3 | Portugués |

El idioma afecta cómo AFIP renderiza el comprobante PDF en algunos servicios secundarios. Para integraciones puras de WSFEXv1 (que solo devuelven CAE), elegí el que coincida con el idioma de tu factura impresa.

Si tu cliente está en Brasil → 3. Si en EEUU/Europa/Asia → 2. En LatAm → 1.
