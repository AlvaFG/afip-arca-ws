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
    // openssl_pkcs7_sign with flags=0 produces a signed S/MIME message:
    //
    //   MIME-Version: 1.0
    //   Content-Disposition: attachment; filename="smime.p7m"
    //   Content-Type: application/x-pkcs7-mime; smime-type=signed-data; ...
    //   Content-Transfer-Encoding: base64
    //
    //   <base64 of CMS DER bytes>
    //
    // We split on the blank line separator (handling both LF and CRLF line
    // endings — OpenSSL builds vary) and strip whitespace from the body.
    // The result is the base64 of the DER CMS, ready to send to AFIP.
    $tmp_in  = tempnam(sys_get_temp_dir(), 'tra_');
    $tmp_out = tempnam(sys_get_temp_dir(), 'cms_');
    file_put_contents($tmp_in, $tra);

    // Flag 0 = neither DETACHED nor BINARY: produces a signed S/MIME message
    // with the content embedded. Passing the constant explicitly is clearer
    // than the historical idiom `!PKCS7_DETACHED` (which evaluates to 0 by
    // coincidence in PHP boolean→int coercion).
    $ok = openssl_pkcs7_sign(
        $tmp_in, $tmp_out,
        'file://' . $cert_path,
        ['file://' . $key_path, ''],
        [],
        0
    );
    if (!$ok) {
        unlink($tmp_in);
        @unlink($tmp_out);
        throw new RuntimeException('openssl_pkcs7_sign failed: ' . openssl_error_string());
    }
    $signed = file_get_contents($tmp_out);
    unlink($tmp_in);
    unlink($tmp_out);

    $parts = preg_split('/\r?\n\r?\n/', $signed, 2);
    if (count($parts) !== 2) {
        throw new RuntimeException('Unexpected S/MIME output: missing header/body separator');
    }
    return preg_replace('/\s+/', '', $parts[1]);
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
