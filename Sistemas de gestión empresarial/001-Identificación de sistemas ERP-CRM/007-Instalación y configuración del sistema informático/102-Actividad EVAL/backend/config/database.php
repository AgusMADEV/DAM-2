<?php
// Configuración de la base de datos
$host = "localhost";
$dbname = "erp_sistema";
$username = "erp_sistema";
$password = "erp_sistema";

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
} catch (PDOException $e) {
    http_response_code(500);
    die(json_encode(['success' => false, 'message' => 'Error de conexión a la base de datos: ' . $e->getMessage()]));
}

// Configuración de JWT (simple)
$jwt_secret = "erp_secret_key_2024";

// Configuración de CORS
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type, Authorization");
header("Content-Type: application/json; charset=utf-8");

// Manejar preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Función para generar JWT simple
function generateJWT($user_id, $username) {
    global $jwt_secret;
    $payload = [
        'user_id' => $user_id,
        'username' => $username,
        'exp' => time() + (24 * 60 * 60) // 24 horas
    ];
    return base64_encode(json_encode($payload)) . '.' . hash_hmac('sha256', base64_encode(json_encode($payload)), $jwt_secret);
}

// Función para verificar JWT simple
function verifyJWT($token) {
    global $jwt_secret;
    $parts = explode('.', $token);
    
    if (count($parts) !== 2) {
        return false;
    }
    
    $payload = $parts[0];
    $signature = $parts[1];
    
    // Verificar firma
    $expected_signature = hash_hmac('sha256', $payload, $jwt_secret);
    if (!hash_equals($signature, $expected_signature)) {
        return false;
    }
    
    // Decodificar payload
    $decoded_payload = json_decode(base64_decode($payload), true);
    
    // Verificar expiración
    if ($decoded_payload['exp'] < time()) {
        return false;
    }
    
    return $decoded_payload;
}

// Función para verificar autenticación
function requireAuth() {
    $headers = getallheaders();
    $auth_header = $headers['Authorization'] ?? '';
    
    if (!$auth_header || !preg_match('/Bearer\s(\S+)/', $auth_header, $matches)) {
        http_response_code(401);
        echo json_encode(['success' => false, 'message' => 'Token de autenticación requerido']);
        exit();
    }
    
    $token = $matches[1];
    $user_data = verifyJWT($token);
    
    if (!$user_data) {
        http_response_code(401);
        echo json_encode(['success' => false, 'message' => 'Token inválido o expirado']);
        exit();
    }
    
    return $user_data;
}

// Función para validar entrada
function validateInput($data, $required_fields) {
    $errors = [];
    
    foreach ($required_fields as $field) {
        if (!isset($data[$field]) || empty(trim($data[$field]))) {
            $errors[] = "El campo '$field' es requerido";
        }
    }
    
    return $errors;
}

// Función para sanitizar entrada
function sanitizeInput($data) {
    if (is_array($data)) {
        return array_map('sanitizeInput', $data);
    }
    return htmlspecialchars(trim($data), ENT_QUOTES, 'UTF-8');
}
?>