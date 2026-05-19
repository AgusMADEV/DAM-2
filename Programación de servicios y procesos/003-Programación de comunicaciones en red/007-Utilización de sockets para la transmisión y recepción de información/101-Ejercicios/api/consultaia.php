<?php
// api.php — relay to REMOTE ngrok AI API
// Receives (GET only):
//   ?question=...&model=...
// Sends to remote via POST:
//   - header: X-API-Key
//   - body: question=...&model=...

header('Content-Type: application/json; charset=utf-8');

// ===============================
// REMOTE CONFIG
// ===============================
$REMOTE_API_URL = 'https://covalently-untasked-d****.ngrok-free.dev/api.php';
$REMOTE_API_KEY = 'TEST_API_KEY_JOCARSA_123';

// ===============================
// READ GET PARAMETERS (STRICT)
// ===============================
$question = trim($_GET['question'] ?? '');
$model    = trim($_GET['model'] ?? ''); // optional, remote has default

if ($question === '') {
    http_response_code(400);
    echo json_encode([
        'error' => "Missing GET parameter: question"
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

// ===============================
// BUILD POST DATA FOR REMOTE
// ===============================
$postFields = [
    'question' => $question
];

if ($model !== '') {
    $postFields['model'] = $model;
}

// ===============================
// CALL REMOTE API
// ===============================
$ch = curl_init($REMOTE_API_URL);
curl_setopt_array($ch, [
    CURLOPT_POST           => true,
    CURLOPT_HTTPHEADER     => [
        'X-API-Key: ' . $REMOTE_API_KEY,
    ],
    CURLOPT_POSTFIELDS     => http_build_query($postFields),
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT        => 300,
    CURLOPT_SSL_VERIFYPEER => false,
    CURLOPT_SSL_VERIFYHOST => 0,
]);

$response = curl_exec($ch);

if ($response === false) {
    http_response_code(502);
    echo json_encode([
        'error'  => 'Remote request failed',
        'detail' => curl_error($ch)
    ], JSON_UNESCAPED_UNICODE);
    curl_close($ch);
    exit;
}

$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($httpCode < 200 || $httpCode >= 300) {
    http_response_code(502);
    echo json_encode([
        'error' => 'Remote returned non-2xx',
        'http'  => $httpCode,
        'body'  => $response
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

// ===============================
// PASS-THROUGH RESPONSE
// ===============================
$decoded = json_decode($response, true);

if (json_last_error() === JSON_ERROR_NONE) {
    echo json_encode($decoded, JSON_UNESCAPED_UNICODE);
} else {
    echo json_encode([
        'answer' => trim($response)
    ], JSON_UNESCAPED_UNICODE);
}

