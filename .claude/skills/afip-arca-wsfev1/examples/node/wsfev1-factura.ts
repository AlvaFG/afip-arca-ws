/**
 * WSFEv1 — issue a Factura B end-to-end.
 * Usage: npx tsx wsfev1-factura.ts --ta ta-wsfe.xml --cuit 20111111112 --pto-vta 1 --neto 100.00 [--env homo|prod]
 */
import { readFileSync } from "node:fs";
import { parseArgs } from "node:util";
import { DOMParser } from "@xmldom/xmldom";
import * as soap from "soap";

const HOMO = "https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL";
const PROD = "https://servicios1.afip.gov.ar/wsfev1/service.asmx?WSDL";
const CBTE_FACTURA_B = 6;
const ALICUOTA_21 = 5;

function loadTa(path: string): { token: string; sign: string } {
  const xml = readFileSync(path, "utf8");
  const doc = new DOMParser().parseFromString(xml, "text/xml");
  const get = (tag: string): string =>
    doc.getElementsByTagName(tag)[0]?.textContent ?? "";
  return { token: get("token"), sign: get("sign") };
}

function round2(n: number): number {
  return Math.round(n * 100) / 100;
}

async function main(): Promise<void> {
  const { values } = parseArgs({
    options: {
      ta: { type: "string" },
      cuit: { type: "string" },
      "pto-vta": { type: "string" },
      neto: { type: "string" },
      env: { type: "string", default: "homo" },
    },
  });
  if (!values.ta || !values.cuit || !values["pto-vta"] || !values.neto) {
    throw new Error("--ta, --cuit, --pto-vta and --neto are required");
  }
  const ta = loadTa(values.ta);
  const auth = { Token: ta.token, Sign: ta.sign, Cuit: values.cuit };
  const ptoVta = Number(values["pto-vta"]);
  const neto = round2(Number(values.neto));
  const iva = round2(neto * 0.21);
  const total = round2(neto + iva);

  const wsdl = values.env === "prod" ? PROD : HOMO;
  const client = await soap.createClientAsync(wsdl);

  const [lastResp] = await client.FECompUltimoAutorizadoAsync({
    Auth: auth, PtoVta: ptoVta, CbteTipo: CBTE_FACTURA_B,
  });
  const nextNro = Number((lastResp as { FECompUltimoAutorizadoResult: { CbteNro: number } })
    .FECompUltimoAutorizadoResult.CbteNro) + 1;

  const fecha = new Date().toISOString().slice(0, 10).replace(/-/g, "");
  const req = {
    FeCabReq: { CantReg: 1, PtoVta: ptoVta, CbteTipo: CBTE_FACTURA_B },
    FeDetReq: { FECAEDetRequest: [{
      Concepto: 1, DocTipo: 99, DocNro: 0,
      CbteDesde: nextNro, CbteHasta: nextNro, CbteFch: fecha,
      ImpTotal: total, ImpTotConc: 0, ImpNeto: neto,
      ImpOpEx: 0, ImpIVA: iva, ImpTrib: 0,
      MonId: "PES", MonCotiz: 1,
      Iva: { AlicIva: [{ Id: ALICUOTA_21, BaseImp: neto, Importe: iva }] },
    }]},
  };

  const [resp] = await client.FECAESolicitarAsync({ Auth: auth, FeCAEReq: req });
  console.log(JSON.stringify(resp, null, 2));
}

main().catch((e: unknown) => { console.error(e); process.exit(1); });
