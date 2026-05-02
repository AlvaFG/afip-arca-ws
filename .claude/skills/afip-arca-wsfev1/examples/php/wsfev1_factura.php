<?php
/**
 * WSFEv1 — issue a Factura B end-to-end.
 * Usage: php wsfev1_factura.php --ta=ta-wsfe.xml --cuit=20111111112 --pto-vta=1 --neto=100.00 [--env=homo|prod]
 */
declare(strict_types=1);

const HOMO = 'https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL';
const PROD = 'https://servicios1.afip.gov.ar/wsfev1/service.asmx?WSDL';
const CBTE_FACTURA_B = 6;
const ALICUOTA_21 = 5;

function load_ta(string $path): array {
    $xml = simplexml_load_string(file_get_contents($path));
    if ($xml === false || !isset($xml->credentials)) {
        throw new RuntimeException("$path: not a TA");
    }
    return [
        'Token' => (string)$xml->credentials->token,
        'Sign'  => (string)$xml->credentials->sign,
    ];
}

function round2(float $n): float {
    return round($n, 2, PHP_ROUND_HALF_UP);
}

$opts = getopt('', ['ta:', 'cuit:', 'pto-vta:', 'neto:', 'env::']);
foreach (['ta', 'cuit', 'pto-vta', 'neto'] as $k) {
    if (empty($opts[$k])) {
        fwrite(STDERR, "Missing --$k\n");
        exit(2);
    }
}
$env = $opts['env'] ?? 'homo';

$ta = load_ta($opts['ta']);
$auth = ['Token' => $ta['Token'], 'Sign' => $ta['Sign'], 'Cuit' => $opts['cuit']];
$pto_vta = (int)$opts['pto-vta'];
$neto = round2((float)$opts['neto']);
$iva = round2($neto * 0.21);
$total = round2($neto + $iva);

$client = new SoapClient($env === 'prod' ? PROD : HOMO, ['soap_version' => SOAP_1_2]);

$last = $client->FECompUltimoAutorizado([
    'Auth' => $auth, 'PtoVta' => $pto_vta, 'CbteTipo' => CBTE_FACTURA_B,
]);
$next = ((int)$last->FECompUltimoAutorizadoResult->CbteNro) + 1;

$req = [
    'FeCabReq' => ['CantReg' => 1, 'PtoVta' => $pto_vta, 'CbteTipo' => CBTE_FACTURA_B],
    'FeDetReq' => ['FECAEDetRequest' => [[
        'Concepto' => 1, 'DocTipo' => 99, 'DocNro' => 0,
        'CbteDesde' => $next, 'CbteHasta' => $next, 'CbteFch' => date('Ymd'),
        'ImpTotal' => $total, 'ImpTotConc' => 0, 'ImpNeto' => $neto,
        'ImpOpEx' => 0, 'ImpIVA' => $iva, 'ImpTrib' => 0,
        'MonId' => 'PES', 'MonCotiz' => 1,
        'Iva' => ['AlicIva' => [['Id' => ALICUOTA_21, 'BaseImp' => $neto, 'Importe' => $iva]]],
    ]]],
];

$resp = $client->FECAESolicitar(['Auth' => $auth, 'FeCAEReq' => $req]);
print_r($resp);
