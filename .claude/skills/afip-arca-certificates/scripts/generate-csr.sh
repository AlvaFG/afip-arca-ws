#!/usr/bin/env bash
# Generate a private key + CSR for AFIP/ARCA using safe defaults.
# Usage: ./generate-csr.sh <ALIAS> <CUIT> [ORGANIZACION]
set -euo pipefail

ALIAS="${1:?Usage: $0 <ALIAS> <CUIT> [ORGANIZACION]}"
CUIT="${2:?Missing CUIT}"
ORG="${3:-${ALIAS}}"

if [[ ! "$CUIT" =~ ^[0-9]{11}$ ]]; then
  echo "ERROR: CUIT must be exactly 11 digits, got: $CUIT" >&2
  exit 1
fi

KEY_FILE="${ALIAS}.key"
CSR_FILE="${ALIAS}.csr"

if [[ -f "$KEY_FILE" ]]; then
  echo "ERROR: $KEY_FILE already exists. Refusing to overwrite." >&2
  exit 1
fi

openssl req -new -newkey rsa:2048 -nodes \
  -keyout "$KEY_FILE" \
  -out "$CSR_FILE" \
  -subj "/C=AR/O=${ORG}/CN=${ALIAS}/serialNumber=CUIT ${CUIT}"

chmod 600 "$KEY_FILE"

echo
echo "✓ Generated:"
echo "  Private key: $KEY_FILE  (chmod 600)"
echo "  CSR:         $CSR_FILE  (upload this to WSASS)"
echo
echo "Next: upload $CSR_FILE via https://auth.afip.gob.ar → WSASS → Crear Certificado"
