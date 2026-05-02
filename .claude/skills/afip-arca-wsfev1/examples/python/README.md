# WSFEv1 Factura B — Python example

Prereq: a valid TA from `afip-arca-wsaa` (saved as `ta-wsfe.xml`).

```bash
pip install -r requirements.txt
python wsfev1_factura.py --ta ta-wsfe.xml --cuit 20111111112 --pto-vta 1 --neto 100.00 --env homo
```
