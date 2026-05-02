/**
 * Padrón A4 — lookup a CUIT.
 * Usage: npx tsx padron-a4.ts --ta ta-padron.xml --cuit-rep 20111111112 --cuit 30500001735
 */
import { readFileSync } from "node:fs";
import { parseArgs } from "node:util";
import { DOMParser } from "@xmldom/xmldom";
import * as soap from "soap";

const HOMO = "https://awshomo.afip.gov.ar/sr-padron/webservices/personaServiceA4?WSDL";
const PROD = "https://aws.afip.gov.ar/sr-padron/webservices/personaServiceA4?WSDL";

function loadTa(path: string): { token: string; sign: string } {
  const xml = readFileSync(path, "utf8");
  const doc = new DOMParser().parseFromString(xml, "text/xml");
  const get = (tag: string): string =>
    doc.getElementsByTagName(tag)[0]?.textContent ?? "";
  return { token: get("token"), sign: get("sign") };
}

interface PersonaResponse {
  errorReturn?: { error?: Array<{ code: string; descripcion: string }> };
  personaReturn?: {
    persona: {
      tipoPersona: string;
      estadoClave: string;
      razonSocial?: string;
      nombre?: string;
      apellido?: string;
    };
  };
}

async function main(): Promise<void> {
  const { values } = parseArgs({
    options: {
      ta: { type: "string" },
      "cuit-rep": { type: "string" },
      cuit: { type: "string" },
      env: { type: "string", default: "homo" },
    },
  });
  if (!values.ta || !values["cuit-rep"] || !values.cuit) {
    throw new Error("--ta, --cuit-rep, --cuit required");
  }
  const ta = loadTa(values.ta);
  const wsdl = values.env === "prod" ? PROD : HOMO;
  const client = await soap.createClientAsync(wsdl);

  const [resp] = await client.getPersonaAsync({
    token: ta.token,
    sign: ta.sign,
    cuitRepresentada: values["cuit-rep"],
    idPersona: values.cuit,
  });
  const r = resp as PersonaResponse;

  if (r.errorReturn?.error?.length) {
    for (const e of r.errorReturn.error) {
      console.error(`ERROR ${e.code}: ${e.descripcion}`);
    }
    process.exit(1);
  }

  const persona = r.personaReturn!.persona;
  const nombre = persona.razonSocial ?? `${persona.nombre ?? ""} ${persona.apellido ?? ""}`.trim();
  console.log(`Nombre/Razón social: ${nombre}`);
  console.log(`Tipo persona:        ${persona.tipoPersona}`);
  console.log(`Estado clave:        ${persona.estadoClave}`);
}

main().catch((e: unknown) => { console.error(e); process.exit(1); });
