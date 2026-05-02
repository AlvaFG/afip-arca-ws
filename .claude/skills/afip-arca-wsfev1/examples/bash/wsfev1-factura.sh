#!/usr/bin/env bash
# WSFEv1 Bash example — calls FEDummy (no auth) to verify connectivity and SOAP shape.
# For real factura issuance, use Python/Node/PHP examples in this skill's examples/.
# Usage: ./wsfev1-factura.sh [homo|prod]
set -euo pipefail

ENV="${1:-homo}"
if [[ "$ENV" == "prod" ]]; then
  URL="https://servicios1.afip.gov.ar/wsfev1/service.asmx"
else
  URL="https://wswhomo.afip.gov.ar/wsfev1/service.asmx"
fi

TMP=$(mktemp)
trap 'rm -f "$TMP"' EXIT

cat > "$TMP" <<'EOF'
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xmlns:xsd="http://www.w3.org/2001/XMLSchema"
               xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <FEDummy xmlns="http://ar.gov.afip.dif.FEV1/" />
  </soap:Body>
</soap:Envelope>
EOF

curl -sS -X POST "$URL" \
  -H "Content-Type: text/xml; charset=utf-8" \
  -H "SOAPAction: http://ar.gov.afip.dif.FEV1/FEDummy" \
  --data-binary "@$TMP"
