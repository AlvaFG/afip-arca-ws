/**
 * WSFEXv1 — issue a Factura E (export) to a US buyer in USD.
 * Usage: npx tsx wsfexv1-factura.ts --ta ta-wsfex.xml --cuit 20111111112 --pto-vta 5 --total 1000.00 --cotiz 950.00
 */
import { readFileSync } from "node:fs";
import { parseArgs } from "node:util";
import { DOMParser } from "@xmldom/xmldom";
import * as soap from "soap";

const HOMO = "https://wswhomo.afip.gov.ar/wsfexv1/service.asmx?WSDL";
const PROD = "https://servicios1.afip.gov.ar/wsfexv1/service.asmx?WSDL";

const CBTE_FACTURA_E = 19;
const DST_USA = 212;
const INCOTERM_FOB = "FOB";
const IDIOMA_INGLES = 2;
const MON_USD = "DOL";

function loadTa(path: string): { token: string; sign: string } {
  const xml = readFileSync(path, "utf8");
  const doc = new DOMParser().parseFromString(xml, "text/xml");
  const get = (tag: string): string =>
    doc.getElementsByTagName(tag)[0]?.textContent ?? "";
  return { token: get("token"), sign: get("sign") };
}

async function main(): Promise<void> {
  const { values } = parseArgs({
    options: {
      ta: { type: "string" },
      cuit: { type: "string" },
      "pto-vta": { type: "string" },
      total: { type: "string" },
      cotiz: { type: "string" },
      env: { type: "string", default: "homo" },
    },
  });
  for (const k of ["ta", "cuit", "pto-vta", "total", "cotiz"] as const) {
    if (!values[k]) throw new Error(`--${k} is required`);
  }
  const ta = loadTa(values.ta!);
  const auth = { Token: ta.token, Sign: ta.sign, Cuit: values.cuit! };
  const ptoVta = Number(values["pto-vta"]);
  const total = Number(values.total);
  const cotiz = Number(values.cotiz);

  const wsdl = values.env === "prod" ? PROD : HOMO;
  const client = await soap.createClientAsync(wsdl);

  const [lastResp] = await client.FEXGetLast_CMPAsync({
    Auth: { ...auth, Pto_venta: ptoVta, Cbte_Tipo: CBTE_FACTURA_E },
  });
  const lastNro = Number(
    (lastResp as { FEXGetLast_CMPResult: { FEXResult_LastCMP: { Cbte_nro: number } } })
      .FEXGetLast_CMPResult.FEXResult_LastCMP.Cbte_nro
  );
  const nextId = lastNro + 1;
  const fecha = new Date().toISOString().slice(0, 10).replace(/-/g, "");

  const cmp = {
    Id: nextId, Fecha_cbte: fecha, Cbte_Tipo: CBTE_FACTURA_E,
    Punto_vta: ptoVta, Cbte_nro: nextId, Tipo_expo: 1, Permiso_existente: "N",
    Dst_cmp: DST_USA, Cliente: "Acme Inc.", Cuit_pais_cliente: "50000000016",
    Domicilio_cliente: "1 Acme Way, NY", Id_impositivo: "FED-12345",
    Moneda_Id: MON_USD, Moneda_ctz: cotiz, Obs_comerciales: "",
    Imp_total: total, Obs: "", Forma_pago: "Wire transfer",
    Incoterms: INCOTERM_FOB, Incoterms_Ds: "Free On Board",
    Idioma_cbte: IDIOMA_INGLES,
    Items: { Item: [{
      Pro_codigo: "SKU-001", Pro_ds: "Widget",
      Pro_qty: 10, Pro_umed: 7,
      Pro_precio_uni: total / 10, Pro_total_item: total,
    }] },
  };

  const [resp] = await client.FEXAuthorizeAsync({ Auth: auth, Cmp: cmp });
  console.log(JSON.stringify(resp, null, 2));
}

main().catch((e: unknown) => { console.error(e); process.exit(1); });
