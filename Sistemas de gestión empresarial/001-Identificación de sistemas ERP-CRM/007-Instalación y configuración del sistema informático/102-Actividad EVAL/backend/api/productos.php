<?php
require_once '../config/database.php';

// Verificar autenticación
$user_data = requireAuth();

switch ($_SERVER['REQUEST_METHOD']) {
    case 'GET':
        // Verificar si se solicita un producto específico por ID
        $producto_id = $_GET['id'] ?? null;
        
        try {
            if ($producto_id) {
                // Obtener producto específico
                $stmt = $pdo->prepare("
                    SELECT id, nombre, descripcion, precio, stock, fecha_creacion 
                    FROM productos 
                    WHERE id = ? AND activo = 1
                ");
                $stmt->execute([$producto_id]);
                $producto = $stmt->fetch();
                
                if ($producto) {
                    echo json_encode([
                        'success' => true,
                        'producto' => $producto
                    ]);
                } else {
                    http_response_code(404);
                    echo json_encode(['success' => false, 'message' => 'Producto no encontrado']);
                }
            } else {
                // Listar todos los productos
                $stmt = $pdo->query("
                    SELECT id, nombre, descripcion, precio, stock, fecha_creacion 
                    FROM productos 
                    WHERE activo = 1 
                    ORDER BY nombre ASC
                ");
                $productos = $stmt->fetchAll();
                
                echo json_encode([
                    'success' => true,
                    'productos' => $productos
                ]);
            }
        } catch (PDOException $e) {
            http_response_code(500);
            echo json_encode(['success' => false, 'message' => 'Error al obtener productos']);
        }
        break;
        
    case 'POST':
        // Crear nuevo producto
        $input = json_decode(file_get_contents('php://input'), true);
        $input = sanitizeInput($input);
        
        $required_fields = ['nombre', 'precio', 'stock'];
        $errors = validateInput($input, $required_fields);
        
        if (!empty($errors)) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => implode(', ', $errors)]);
            break;
        }
        
        // Validar precio y stock
        if (!is_numeric($input['precio']) || $input['precio'] < 0) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'El precio debe ser un número válido']);
            break;
        }
        
        if (!is_numeric($input['stock']) || $input['stock'] < 0) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'El stock debe ser un número válido']);
            break;
        }
        
        try {
            // Verificar si el nombre del producto ya existe
            $stmt = $pdo->prepare("SELECT id FROM productos WHERE nombre = ? AND activo = 1");
            $stmt->execute([$input['nombre']]);
            
            if ($stmt->fetch()) {
                http_response_code(409);
                echo json_encode(['success' => false, 'message' => 'Ya existe un producto con ese nombre']);
                break;
            }
            
            // Insertar nuevo producto
            $stmt = $pdo->prepare("
                INSERT INTO productos (nombre, descripcion, precio, stock, fecha_creacion, activo) 
                VALUES (?, ?, ?, ?, NOW(), 1)
            ");
            
            $stmt->execute([
                $input['nombre'],
                $input['descripcion'] ?? '',
                floatval($input['precio']),
                intval($input['stock'])
            ]);
            
            $producto_id = $pdo->lastInsertId();
            
            echo json_encode([
                'success' => true,
                'message' => 'Producto creado exitosamente',
                'producto_id' => $producto_id
            ]);
            
        } catch (PDOException $e) {
            http_response_code(500);
            echo json_encode(['success' => false, 'message' => 'Error al crear producto']);
            error_log("Error creando producto: " . $e->getMessage());
        }
        break;
        
    case 'PUT':
        // Actualizar producto existente
        $input = json_decode(file_get_contents('php://input'), true);
        $input = sanitizeInput($input);
        $producto_id = $input['id'] ?? null;
        
        if (!$producto_id) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'ID del producto requerido']);
            break;
        }
        
        $required_fields = ['nombre', 'precio', 'stock'];
        $errors = validateInput($input, $required_fields);
        
        if (!empty($errors)) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => implode(', ', $errors)]);
            break;
        }
        
        // Validar precio y stock
        if (!is_numeric($input['precio']) || $input['precio'] < 0) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'El precio debe ser un número válido']);
            break;
        }
        
        if (!is_numeric($input['stock']) || $input['stock'] < 0) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'El stock debe ser un número válido']);
            break;
        }
        
        try {
            // Verificar si el nombre del producto ya existe en otro producto
            $stmt = $pdo->prepare("SELECT id FROM productos WHERE nombre = ? AND id != ? AND activo = 1");
            $stmt->execute([$input['nombre'], $producto_id]);
            
            if ($stmt->fetch()) {
                http_response_code(409);
                echo json_encode(['success' => false, 'message' => 'Ya existe otro producto con ese nombre']);
                break;
            }
            
            // Actualizar producto
            $stmt = $pdo->prepare("
                UPDATE productos 
                SET nombre = ?, descripcion = ?, precio = ?, stock = ?
                WHERE id = ? AND activo = 1
            ");
            
            $result = $stmt->execute([
                $input['nombre'],
                $input['descripcion'] ?? '',
                floatval($input['precio']),
                intval($input['stock']),
                $producto_id
            ]);
            
            if ($result && $stmt->rowCount() > 0) {
                echo json_encode([
                    'success' => true,
                    'message' => 'Producto actualizado exitosamente'
                ]);
            } else {
                http_response_code(404);
                echo json_encode(['success' => false, 'message' => 'Producto no encontrado']);
            }
            
        } catch (PDOException $e) {
            http_response_code(500);
            echo json_encode(['success' => false, 'message' => 'Error al actualizar producto']);
            error_log("Error actualizando producto: " . $e->getMessage());
        }
        break;
        
    case 'DELETE':
        // Eliminar producto (soft delete)
        $producto_id = $_GET['id'] ?? null;
        
        if (!$producto_id) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'ID del producto requerido']);
            break;
        }
        
        try {
            // Verificar si el producto tiene ventas asociadas
            $stmt = $pdo->prepare("
                SELECT COUNT(*) as total 
                FROM detalle_venta dv 
                INNER JOIN ventas v ON dv.venta_id = v.id 
                WHERE dv.producto_id = ?
            ");
            $stmt->execute([$producto_id]);
            $ventas_count = $stmt->fetch()['total'];
            
            if ($ventas_count > 0) {
                http_response_code(409);
                echo json_encode(['success' => false, 'message' => 'No se puede eliminar el producto porque tiene ventas asociadas']);
                break;
            }
            
            // Soft delete
            $stmt = $pdo->prepare("UPDATE productos SET activo = 0 WHERE id = ?");
            $result = $stmt->execute([$producto_id]);
            
            if ($result && $stmt->rowCount() > 0) {
                echo json_encode([
                    'success' => true,
                    'message' => 'Producto eliminado exitosamente'
                ]);
            } else {
                http_response_code(404);
                echo json_encode(['success' => false, 'message' => 'Producto no encontrado']);
            }
            
        } catch (PDOException $e) {
            http_response_code(500);
            echo json_encode(['success' => false, 'message' => 'Error al eliminar producto']);
            error_log("Error eliminando producto: " . $e->getMessage());
        }
        break;
        
    default:
        http_response_code(405);
        echo json_encode(['success' => false, 'message' => 'Método no permitido']);
        break;
}
?>