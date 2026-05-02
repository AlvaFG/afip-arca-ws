#!/usr/bin/env bash
# Inspect an AFIP cert: subject, issuer, validity dates, SHA-256 fingerprint.
# Usage: ./check-cert.sh <path-to.crt>
set -euo pipefail

CERT="${1:?Usage: $0 <path-to.crt>}"

if [[ ! -f "$CERT" ]]; then
  echo "ERROR: $CERT not found" >&2
  exit 1
fi

echo "=== Certificate: $CERT ==="
openssl x509 -in "$CERT" -noout -subject
openssl x509 -in "$CERT" -noout -issuer
openssl x509 -in "$CERT" -noout -dates
openssl x509 -in "$CERT" -noout -fingerprint -sha256

# Days until expiry
END=$(openssl x509 -in "$CERT" -noout -enddate | cut -d= -f2)
END_TS=$(date -d "$END" +%s 2>/dev/null || gdate -d "$END" +%s)
NOW_TS=$(date +%s)
DAYS=$(( (END_TS - NOW_TS) / 86400 ))

echo
if (( DAYS < 0 )); then
  echo "✗ EXPIRED $((-DAYS)) days ago"
  exit 2
elif (( DAYS < 30 )); then
  echo "⚠ EXPIRES in $DAYS days — renew now"
  exit 1
else
  echo "✓ Valid for $DAYS more days"
fi
