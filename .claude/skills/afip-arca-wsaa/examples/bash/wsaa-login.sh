#!/usr/bin/env bash
# WSAA login using only openssl + curl.
# Usage: ./wsaa-login.sh <cert.crt> <key.key> <service> [homo|prod]
set -euo pipefail

CERT="${1:?Usage: $0 <cert.crt> <key.key> <service> [homo|prod]}"
KEY="${2:?Missing key}"
SERVICE="${3:?Missing service (e.g. wsfe)}"
ENV="${4:-homo}"

if [[ "$ENV" == "homo" ]]; then
  URL="https://wsaahomo.afip.gov.ar/ws/services/LoginCms"
else
  URL="https://wsaa.afip.gov.ar/ws/services/LoginCms"
fi

WORKDIR=$(mktemp -d)
trap 'rm -rf "$WORKDIR"' EXIT

NOW=$(date +%s)
# AFIP requires ISO 8601 with explicit timezone. Shift epoch back 3h then format
# as UTC and append "-03:00" — same approach as the PHP/Node examples.
ART_OFFSET=10800
fmt_art() {
  local t="$1"
  date -u -d "@$((t - ART_OFFSET))" +%Y-%m-%dT%H:%M:%S 2>/dev/null \
    || gdate -u -d "@$((t - ART_OFFSET))" +%Y-%m-%dT%H:%M:%S
}
GEN="$(fmt_art "$((NOW - 60))")-03:00"
EXP="$(fmt_art "$((NOW + 600))")-03:00"

cat > "$WORKDIR/tra.xml" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<loginTicketRequest version="1.0">
  <header>
    <uniqueId>${NOW}</uniqueId>
    <generationTime>${GEN}</generationTime>
    <expirationTime>${EXP}</expirationTime>
  </header>
  <service>${SERVICE}</service>
</loginTicketRequest>
EOF

openssl smime -sign \
  -in "$WORKDIR/tra.xml" \
  -signer "$CERT" \
  -inkey "$KEY" \
  -outform DER \
  -nodetach \
  -out "$WORKDIR/tra.cms"

CMS_B64=$(base64 -w0 "$WORKDIR/tra.cms" 2>/dev/null || base64 "$WORKDIR/tra.cms" | tr -d '\n')

cat > "$WORKDIR/req.xml" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:wsaa="http://wsaa.view.sua.dvadac.desein.afip.gov">
  <soapenv:Body>
    <wsaa:loginCms>
      <wsaa:in0>${CMS_B64}</wsaa:in0>
    </wsaa:loginCms>
  </soapenv:Body>
</soapenv:Envelope>
EOF

curl -sS -X POST "$URL" \
  -H "Content-Type: text/xml; charset=utf-8" \
  -H 'SOAPAction: ""' \
  --data-binary "@$WORKDIR/req.xml"
