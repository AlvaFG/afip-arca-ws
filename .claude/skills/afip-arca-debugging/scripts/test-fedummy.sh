#!/usr/bin/env bash
# Smoke-test AFIP services by calling their dummy methods.
# Usage: ./test-fedummy.sh [homo|prod]
set -euo pipefail

ENV="${1:-homo}"

if [[ "$ENV" == "prod" ]]; then
  WSFE="https://servicios1.afip.gov.ar/wsfev1/service.asmx"
  WSFEX="https://servicios1.afip.gov.ar/wsfexv1/service.asmx"
else
  WSFE="https://wswhomo.afip.gov.ar/wsfev1/service.asmx"
  WSFEX="https://wswhomo.afip.gov.ar/wsfexv1/service.asmx"
fi

call_dummy() {
  local name="$1"; local url="$2"; local soapaction="$3"; local body="$4"
  echo "▶ $name → $url"
  if curl -sS -m 10 -X POST "$url" \
      -H "Content-Type: text/xml; charset=utf-8" \
      -H "SOAPAction: $soapaction" \
      --data-binary "$body" | grep -E "AppServer|DbServer|AuthServer" || true; then
    echo "✓ $name responded"
  else
    echo "✗ $name no response"
  fi
  echo
}

call_dummy "WSFEv1 FEDummy" "$WSFE" "http://ar.gov.afip.dif.FEV1/FEDummy" \
  '<?xml version="1.0"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><FEDummy xmlns="http://ar.gov.afip.dif.FEV1/"/></soap:Body></soap:Envelope>'

call_dummy "WSFEXv1 FEXDummy" "$WSFEX" "http://ar.gov.afip.dif.fex/FEXDummy" \
  '<?xml version="1.0"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><FEXDummy xmlns="http://ar.gov.afip.dif.fex/"/></soap:Body></soap:Envelope>'
