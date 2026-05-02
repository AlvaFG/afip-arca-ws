/**
 * WSAA login — TypeScript example.
 * Usage: npx tsx wsaa-login.ts --cert cert.crt --key key.key --service wsfe [--env homo|prod]
 */
import { readFileSync } from "node:fs";
import { parseArgs } from "node:util";
import forge from "node-forge";
import * as soap from "soap";

const WSAA_HOMO = "https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl";
const WSAA_PROD = "https://wsaa.afip.gov.ar/ws/services/LoginCms?wsdl";

function isoArt(ts: number): string {
  // Format unix seconds as ISO 8601 with -03:00 (ART) offset.
  const d = new Date((ts - 3 * 3600) * 1000);
  const pad = (n: number) => String(n).padStart(2, "0");
  return (
    `${d.getUTCFullYear()}-${pad(d.getUTCMonth() + 1)}-${pad(d.getUTCDate())}` +
    `T${pad(d.getUTCHours())}:${pad(d.getUTCMinutes())}:${pad(d.getUTCSeconds())}-03:00`
  );
}

function buildTra(service: string): string {
  const now = Math.floor(Date.now() / 1000);
  return `<?xml version="1.0" encoding="UTF-8"?>
<loginTicketRequest version="1.0">
  <header>
    <uniqueId>${now}</uniqueId>
    <generationTime>${isoArt(now - 60)}</generationTime>
    <expirationTime>${isoArt(now + 600)}</expirationTime>
  </header>
  <service>${service}</service>
</loginTicketRequest>`;
}

function signCms(tra: string, certPem: string, keyPem: string): string {
  const cert = forge.pki.certificateFromPem(certPem);
  const key = forge.pki.privateKeyFromPem(keyPem);
  const p7 = forge.pkcs7.createSignedData();
  p7.content = forge.util.createBuffer(tra, "utf8");
  p7.addCertificate(cert);
  p7.addSigner({
    key,
    certificate: cert,
    digestAlgorithm: forge.pki.oids.sha256,
  });
  p7.sign({ detached: false });
  const der = forge.asn1.toDer(p7.toAsn1()).getBytes();
  return forge.util.encode64(der);
}

async function main(): Promise<void> {
  const { values } = parseArgs({
    options: {
      cert: { type: "string" },
      key: { type: "string" },
      service: { type: "string", default: "wsfe" },
      env: { type: "string", default: "homo" },
    },
  });
  if (!values.cert || !values.key) {
    throw new Error("--cert and --key are required");
  }

  const certPem = readFileSync(values.cert, "utf8");
  const keyPem = readFileSync(values.key, "utf8");
  const tra = buildTra(values.service!);
  const cmsB64 = signCms(tra, certPem, keyPem);

  const wsdl = values.env === "prod" ? WSAA_PROD : WSAA_HOMO;
  const client = await soap.createClientAsync(wsdl);
  const [result] = await client.loginCmsAsync({ in0: cmsB64 });
  process.stdout.write((result as { loginCmsReturn: string }).loginCmsReturn);
}

main().catch((e: unknown) => {
  console.error(e);
  process.exit(1);
});
