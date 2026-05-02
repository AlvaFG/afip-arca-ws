# WSAA login — Python example

```bash
pip install -r requirements.txt
python wsaa_login.py --cert /path/to/cert.crt --key /path/to/private.key --service wsfe --env homo > ta-wsfe.xml
```

Cache `ta-wsfe.xml` until the `<expirationTime>` inside it. For caching strategies, see `../../references/ta-caching-rules.md`.

Use `../../scripts/validate-ta.py ta-wsfe.xml` to inspect the TA's validity window.
