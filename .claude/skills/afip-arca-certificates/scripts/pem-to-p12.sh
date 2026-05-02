#!/usr/bin/env bash
# Bundle a PEM key + cert into a .p12 (PKCS#12) for Java/.NET runtimes.
# Usage: ./pem-to-p12.sh <key.key> <cert.crt> <alias> [out.p12]
set -euo pipefail

KEY="${1:?Usage: $0 <key.key> <cert.crt> <alias> [out.p12]}"
CRT="${2:?Missing cert}"
ALIAS="${3:?Missing alias}"
OUT="${4:-${ALIAS}.p12}"

if [[ -f "$OUT" ]]; then
  echo "ERROR: $OUT already exists. Refusing to overwrite." >&2
  exit 1
fi

openssl pkcs12 -export \
  -inkey "$KEY" \
  -in "$CRT" \
  -name "$ALIAS" \
  -out "$OUT"

chmod 600 "$OUT"
echo "✓ Wrote $OUT (chmod 600). Use the export password you just typed when loading into a keystore."
