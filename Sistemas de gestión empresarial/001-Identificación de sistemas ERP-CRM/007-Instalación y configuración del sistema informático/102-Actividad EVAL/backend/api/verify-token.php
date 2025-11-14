<?php
require_once '../config/database.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $headers = getallheaders();
    $auth_header = $headers['Authorization'] ?? '';
    
    if (!$auth_header || !preg_match('/Bearer\s(\S+)/', $auth_header, $matches)) {
        echo json_encode(['valid' => false, 'message' => 'Token no proporcionado']);
        exit();
    }
    
    $token = $matches[1];
    $user_data = verifyJWT($token);
    
    if ($user_data) {
        // Verificar que el usuario sigue existiendo y activo en la base de datos
        try {
            $stmt = $pdo->prepare("SELECT id, username, nombre, email FROM usuarios WHERE id = ? AND activo = 1");
            $stmt->execute([$user_data['user_id']]);
            $user = $stmt->fetch();
            
            if ($user) {
                echo json_encode(['valid' => true, 'user' => $user]);
            } else {
                echo json_encode(['valid' => false, 'message' => 'Usuario no encontrado o inactivo']);
            }
        } catch (PDOException $e) {
            echo json_encode(['valid' => false, 'message' => 'Error del servidor']);
        }
    } else {
        echo json_encode(['valid' => false, 'message' => 'Token inválido o expirado']);
    }
} else {
    http_response_code(405);
    echo json_encode(['valid' => false, 'message' => 'Método no permitido']);
}
?>