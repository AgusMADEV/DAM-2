<?php
require_once '../config/database.php';

// Obtener datos del POST
$input = json_decode(file_get_contents('php://input'), true);

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = sanitizeInput($input['username'] ?? '');
    $password = $input['password'] ?? '';
    
    // Validar campos requeridos
    if (empty($username) || empty($password)) {
        http_response_code(400);
        echo json_encode(['success' => false, 'message' => 'Usuario y contraseña son requeridos']);
        exit();
    }
    
    try {
        // Buscar usuario en la base de datos
        $stmt = $pdo->prepare("SELECT id, username, password, nombre, email, activo FROM usuarios WHERE username = ? AND activo = 1");
        $stmt->execute([$username]);
        $user = $stmt->fetch();
        
        if ($user && password_verify($password, $user['password'])) {
            // Actualizar último acceso
            $update_stmt = $pdo->prepare("UPDATE usuarios SET ultimo_acceso = NOW() WHERE id = ?");
            $update_stmt->execute([$user['id']]);
            
            // Generar token JWT
            $token = generateJWT($user['id'], $user['username']);
            
            // Preparar datos del usuario (sin contraseña)
            unset($user['password']);
            
            echo json_encode([
                'success' => true,
                'token' => $token,
                'user' => $user,
                'message' => 'Login exitoso'
            ]);
        } else {
            http_response_code(401);
            echo json_encode(['success' => false, 'message' => 'Credenciales inválidas']);
        }
    } catch (PDOException $e) {
        http_response_code(500);
        echo json_encode(['success' => false, 'message' => 'Error del servidor']);
        error_log("Error en login: " . $e->getMessage());
    }
} else {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Método no permitido']);
}
?>