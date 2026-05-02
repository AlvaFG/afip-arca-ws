<?php
/**
 * WSFEXv1 — issue a Factura E (export).
 * Usage: php wsfexv1_factura.php --ta=ta-wsfex.xml --cuit=20111111112 --pto-vta=5 --total=1000.00 --cotiz=950.00
 */
declare(strict_types=1);

const HOMO = 'https://wswhomo.afip.gov.ar/wsfexv1/service.asmx?WSDL';
const PROD = 'https://servicios1.afip.gov.ar/wsfexv1/service.asmx?WSDL';

const CBTE_FACTURA_E = 19;
const DST_USA = 212;
const INCOTERM_FOB = 'FOB';
const IDIOMA_INGLES = 2;
const MON_USD = 'DOL';

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

$opts = getopt('', ['ta:', 'cuit:', 'pto-vta:', 'total:', 'cotiz:', 'env::']);
foreach (['ta', 'cuit', 'pto-vta', 'total', 'cotiz'] as $k) {
    if (empty($opts[$k])) {
        fwrite(STDERR, "Missing --$k\n");
        exit(2);
    }
}
$env = $opts['env'] ?? 'homo';

$ta = load_ta($opts['ta']);
$auth = ['Token' => $ta['Token'], 'Sign' => $ta['Sign'], 'Cuit' => $opts['cuit']];
$pto_vta = (int)$opts['pto-vta'];
$total = (float)$opts['total'];
$cotiz = (float)$opts['cotiz'];

$client = new SoapClient($env === 'prod' ? PROD : HOMO, ['soap_version' => SOAP_1_2]);

$last = $client->FEXGetLast_CMP([
    'Auth' => $auth + ['Pto_venta' => $pto_vta, 'Cbte_Tipo' => CBTE_FACTURA_E],
]);
$next = ((int)$last->FEXGetLast_CMPResult->FEXResult_LastCMP->Cbte_nro) + 1;

$cmp = [
    'Id' => $next, 'Fecha_cbte' => date('Ymd'), 'Cbte_Tipo' => CBTE_FACTURA_E,
    'Punto_vta' => $pto_vta, 'Cbte_nro' => $next, 'Tipo_expo' => 1,
    'Permiso_existente' => 'N', 'Dst_cmp' => DST_USA,
    'Cliente' => 'Acme Inc.', 'Cuit_pais_cliente' => '50000000016',
    'Domicilio_cliente' => '1 Acme Way, NY', 'Id_impositivo' => 'FED-12345',
    'Moneda_Id' => MON_USD, 'Moneda_ctz' => $cotiz, 'Obs_comerciales' => '',
    'Imp_total' => $total, 'Obs' => '', 'Forma_pago' => 'Wire transfer',
    'Incoterms' => INCOTERM_FOB, 'Incoterms_Ds' => 'Free On Board',
    'Idioma_cbte' => IDIOMA_INGLES,
    'Items' => ['Item' => [[
        'Pro_codigo' => 'SKU-001', 'Pro_ds' => 'Widget',
        'Pro_qty' => 10, 'Pro_umed' => 7,
        'Pro_precio_uni' => $total / 10, 'Pro_total_item' => $total,
    ]]],
];

$resp = $client->FEXAuthorize(['Auth' => $auth, 'Cmp' => $cmp]);
print_r($resp);
