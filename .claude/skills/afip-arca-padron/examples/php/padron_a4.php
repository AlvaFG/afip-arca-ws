<?php
/**
 * Padrón A4 — lookup a CUIT.
 * Usage: php padron_a4.php --ta=ta-padron.xml --cuit-rep=20111111112 --cuit=30500001735
 */
declare(strict_types=1);

const HOMO = 'https://awshomo.afip.gov.ar/sr-padron/webservices/personaServiceA4?WSDL';
const PROD = 'https://aws.afip.gov.ar/sr-padron/webservices/personaServiceA4?WSDL';

function load_ta(string $path): array {
    $xml = simplexml_load_string(file_get_contents($path));
    if ($xml === false || !isset($xml->credentials)) {
        throw new RuntimeException("$path: not a TA");
    }
    return [
        'token' => (string)$xml->credentials->token,
        'sign'  => (string)$xml->credentials->sign,
    ];
}

$opts = getopt('', ['ta:', 'cuit-rep:', 'cuit:', 'env::']);
foreach (['ta', 'cuit-rep', 'cuit'] as $k) {
    if (empty($opts[$k])) {
        fwrite(STDERR, "Missing --$k\n");
        exit(2);
    }
}
$env = $opts['env'] ?? 'homo';
$ta = load_ta($opts['ta']);

$client = new SoapClient($env === 'prod' ? PROD : HOMO, ['soap_version' => SOAP_1_1]);
$resp = $client->getPersona([
    'token' => $ta['token'],
    'sign'  => $ta['sign'],
    'cuitRepresentada' => $opts['cuit-rep'],
    'idPersona' => $opts['cuit'],
]);

if (isset($resp->errorReturn->error)) {
    $errors = is_array($resp->errorReturn->error) ? $resp->errorReturn->error : [$resp->errorReturn->error];
    foreach ($errors as $e) {
        fwrite(STDERR, "ERROR {$e->code}: {$e->descripcion}\n");
    }
    exit(1);
}

$persona = $resp->personaReturn->persona;
$nombre = $persona->razonSocial ?? trim(($persona->nombre ?? '') . ' ' . ($persona->apellido ?? ''));
echo "Nombre/Razón social: $nombre\n";
echo "Tipo persona:        {$persona->tipoPersona}\n";
echo "Estado clave:        {$persona->estadoClave}\n";
