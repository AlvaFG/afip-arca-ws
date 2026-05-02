# WSFEv1 Bash example (FEDummy only)

This script calls `FEDummy` to verify connectivity and the SOAP envelope shape. It does NOT issue a real factura — see `../python/`, `../node/`, or `../php/` for that, since hand-rolling FECAESolicitar in pure Bash is brittle.

```bash
./wsfev1-factura.sh homo
```
