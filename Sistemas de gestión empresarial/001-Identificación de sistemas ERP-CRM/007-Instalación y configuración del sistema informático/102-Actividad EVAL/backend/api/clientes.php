<?php
require_once '../config/database.php';

// Verificar autenticación
$user_data = requireAuth();

switch ($_SERVER['REQUEST_METHOD']) {
    case 'GET':
        // Verificar si se solicita un cliente específico por ID
        $cliente_id = $_GET['id'] ?? null;
        
        try {
            if ($cliente_id) {
                // Obtener cliente específico
                $stmt = $pdo->prepare("
                    SELECT id, nombre, email, telefono, direccion, fecha_registro 
                    FROM clientes 
                    WHERE id = ? AND activo = 1
                ");
                $stmt->execute([$cliente_id]);
                $cliente = $stmt->fetch();
                
                if ($cliente) {
                    echo json_encode([
                        'success' => true,
                        'cliente' => $cliente
                    ]);
                } else {
                    http_response_code(404);
                    echo json_encode(['success' => false, 'message' => 'Cliente no encontrado']);
                }
            } else {
                // Listar todos los clientes
                $stmt = $pdo->query("
                    SELECT id, nombre, email, telefono, direccion, fecha_registro 
                    FROM clientes 
                    WHERE activo = 1 
                    ORDER BY nombre ASC
                ");
                $clientes = $stmt->fetchAll();
                
                echo json_encode([
                    'success' => true,
                    'clientes' => $clientes
                ]);
            }
        } catch (PDOException $e) {
            http_response_code(500);
            echo json_encode(['success' => false, 'message' => 'Error al obtener clientes']);
        }
        break;
        
    case 'POST':
        // Crear nuevo cliente
        $input = json_decode(file_get_contents('php://input'), true);
        $input = sanitizeInput($input);
        
        $required_fields = ['nombre', 'email', 'telefono'];
        $errors = validateInput($input, $required_fields);
        
        if (!empty($errors)) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => implode(', ', $errors)]);
            break;
        }
        
        try {
            // Verificar si el email ya existe
            $stmt = $pdo->prepare("SELECT id FROM clientes WHERE email = ? AND activo = 1");
            $stmt->execute([$input['email']]);
            
            if ($stmt->fetch()) {
                http_response_code(409);
                echo json_encode(['success' => false, 'message' => 'El email ya está registrado']);
                break;
            }
            
            // Insertar nuevo cliente
            $stmt = $pdo->prepare("
                INSERT INTO clientes (nombre, email, telefono, direccion, fecha_registro, activo) 
                VALUES (?, ?, ?, ?, NOW(), 1)
            ");
            
            $stmt->execute([
                $input['nombre'],
                $input['email'],
                $input['telefono'],
                $input['direccion'] ?? ''
            ]);
            
            $cliente_id = $pdo->lastInsertId();
            
            echo json_encode([
                'success' => true,
                'message' => 'Cliente creado exitosamente',
                'cliente_id' => $cliente_id
            ]);
            
        } catch (PDOException $e) {
            http_response_code(500);
            echo json_encode(['success' => false, 'message' => 'Error al crear cliente']);
            error_log("Error creando cliente: " . $e->getMessage());
        }
        break;
        
    case 'PUT':
        // Actualizar cliente existente
        $input = json_decode(file_get_contents('php://input'), true);
        $input = sanitizeInput($input);
        $cliente_id = $input['id'] ?? null;
        
        if (!$cliente_id) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'ID del cliente requerido']);
            break;
        }
        
        $required_fields = ['nombre', 'email', 'telefono'];
        $errors = validateInput($input, $required_fields);
        
        if (!empty($errors)) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => implode(', ', $errors)]);
            break;
        }
        
        try {
            // Verificar si el email ya existe en otro cliente
            $stmt = $pdo->prepare("SELECT id FROM clientes WHERE email = ? AND id != ? AND activo = 1");
            $stmt->execute([$input['email'], $cliente_id]);
            
            if ($stmt->fetch()) {
                http_response_code(409);
                echo json_encode(['success' => false, 'message' => 'El email ya está registrado en otro cliente']);
                break;
            }
            
            // Actualizar cliente
            $stmt = $pdo->prepare("
                UPDATE clientes 
                SET nombre = ?, email = ?, telefono = ?, direccion = ? 
                WHERE id = ? AND activo = 1
            ");
            
            $result = $stmt->execute([
                $input['nombre'],
                $input['email'],
                $input['telefono'],
                $input['direccion'] ?? '',
                $cliente_id
            ]);
            
            if ($result && $stmt->rowCount() > 0) {
                echo json_encode([
                    'success' => true,
                    'message' => 'Cliente actualizado exitosamente'
                ]);
            } else {
                http_response_code(404);
                echo json_encode(['success' => false, 'message' => 'Cliente no encontrado']);
            }
            
        } catch (PDOException $e) {
            http_response_code(500);
            echo json_encode(['success' => false, 'message' => 'Error al actualizar cliente']);
            error_log("Error actualizando cliente: " . $e->getMessage());
        }
        break;
        
    case 'DELETE':
        // Eliminar cliente (soft delete)
        $cliente_id = $_GET['id'] ?? null;
        
        if (!$cliente_id) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'ID del cliente requerido']);
            break;
        }
        
        try {
            // Verificar si el cliente tiene ventas asociadas
            $stmt = $pdo->prepare("SELECT COUNT(*) as total FROM ventas WHERE cliente_id = ?");
            $stmt->execute([$cliente_id]);
            $ventas_count = $stmt->fetch()['total'];
            
            if ($ventas_count > 0) {
                http_response_code(409);
                echo json_encode(['success' => false, 'message' => 'No se puede eliminar el cliente porque tiene ventas asociadas']);
                break;
            }
            
            // Soft delete
            $stmt = $pdo->prepare("UPDATE clientes SET activo = 0 WHERE id = ?");
            $result = $stmt->execute([$cliente_id]);
            
            if ($result && $stmt->rowCount() > 0) {
                echo json_encode([
                    'success' => true,
                    'message' => 'Cliente eliminado exitosamente'
                ]);
            } else {
                http_response_code(404);
                echo json_encode(['success' => false, 'message' => 'Cliente no encontrado']);
            }
            
        } catch (PDOException $e) {
            http_response_code(500);
            echo json_encode(['success' => false, 'message' => 'Error al eliminar cliente']);
            error_log("Error eliminando cliente: " . $e->getMessage());
        }
        break;
        
    default:
        http_response_code(405);
        echo json_encode(['success' => false, 'message' => 'Método no permitido']);
        break;
}
?>