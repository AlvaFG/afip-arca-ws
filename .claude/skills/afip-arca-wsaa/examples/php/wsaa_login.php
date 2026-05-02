<?php
/**
 * WSAA login — PHP example using SoapClient + openssl_pkcs7_sign.
 * Usage: php wsaa_login.php --cert=cert.crt --key=key.key --service=wsfe [--env=homo|prod]
 */
declare(strict_types=1);

const WSAA_HOMO = 'https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl';
const WSAA_PROD = 'https://wsaa.afip.gov.ar/ws/services/LoginCms?wsdl';

function build_tra(string $service): string {
    $now = time();
    $gen = gmdate('Y-m-d\TH:i:s', $now - 60 - 3 * 3600) . '-03:00';
    $exp = gmdate('Y-m-d\TH:i:s', $now + 600 - 3 * 3600) . '-03:00';
    return <<<XML
<?xml version="1.0" encoding="UTF-8"?>
<loginTicketRequest version="1.0">
  <header>
    <uniqueId>{$now}</uniqueId>
    <generationTime>{$gen}</generationTime>
    <expirationTime>{$exp}</expirationTime>
  </header>
  <service>{$service}</service>
</loginTicketRequest>
XML;
}

function sign_cms(string $tra, string $cert_path, string $key_path): string {
    $tmp_in = tempnam(sys_get_temp_dir(), 'tra_');
    $tmp_out = tempnam(sys_get_temp_dir(), 'cms_');
    file_put_contents($tmp_in, $tra);
    $ok = openssl_pkcs7_sign(
        $tmp_in, $tmp_out,
        'file://' . $cert_path,
        ['file://' . $key_path, ''],
        [],
        !PKCS7_DETACHED
    );
    if (!$ok) {
        throw new RuntimeException('openssl_pkcs7_sign failed: ' . openssl_error_string());
    }
    $signed = file_get_contents($tmp_out);
    unlink($tmp_in);
    unlink($tmp_out);
    // Strip MIME headers to keep the CMS bytes only, then base64
    [, $body] = explode("\n\n", $signed, 2);
    return preg_replace('/\s+/', '', $body);
}

function parse_args(): array {
    $opts = getopt('', ['cert:', 'key:', 'service:', 'env::']);
    foreach (['cert', 'key', 'service'] as $k) {
        if (empty($opts[$k])) {
            fwrite(STDERR, "Missing --$k\n");
            exit(2);
        }
    }
    $opts['env'] = $opts['env'] ?? 'homo';
    return $opts;
}

$args = parse_args();
$tra = build_tra($args['service']);
$cms_b64 = sign_cms($tra, $args['cert'], $args['key']);

$wsdl = $args['env'] === 'prod' ? WSAA_PROD : WSAA_HOMO;
$client = new SoapClient($wsdl, ['soap_version' => SOAP_1_2, 'trace' => 1]);
$result = $client->loginCms(['in0' => $cms_b64]);
echo $result->loginCmsReturn;
