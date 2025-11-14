<?php
require_once '../config/database.php';

// Verificar autenticación
$user_data = requireAuth();

switch ($_SERVER['REQUEST_METHOD']) {
    case 'GET':
        // Listar todas las ventas
        try {
            $stmt = $pdo->query("
                SELECT 
                    v.id,
                    v.fecha_venta as fecha,
                    v.total,
                    v.estado,
                    c.nombre as cliente_nombre
                FROM ventas v
                INNER JOIN clientes c ON v.cliente_id = c.id
                ORDER BY v.fecha_venta DESC
            ");
            $ventas = $stmt->fetchAll();
            
            echo json_encode([
                'success' => true,
                'ventas' => $ventas
            ]);
        } catch (PDOException $e) {
            http_response_code(500);
            echo json_encode(['success' => false, 'message' => 'Error al obtener ventas']);
        }
        break;
        
    case 'POST':
        // Crear nueva venta
        $input = json_decode(file_get_contents('php://input'), true);
        $input = sanitizeInput($input);
        
        $required_fields = ['cliente_id', 'producto_id', 'cantidad'];
        $errors = validateInput($input, $required_fields);
        
        if (!empty($errors)) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => implode(', ', $errors)]);
            break;
        }
        
        // Validar cantidad
        if (!is_numeric($input['cantidad']) || $input['cantidad'] <= 0) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'La cantidad debe ser un número mayor a 0']);
            break;
        }
        
        try {
            $pdo->beginTransaction();
            
            // Verificar que el cliente existe
            $stmt = $pdo->prepare("SELECT id FROM clientes WHERE id = ? AND activo = 1");
            $stmt->execute([$input['cliente_id']]);
            if (!$stmt->fetch()) {
                throw new Exception('Cliente no encontrado');
            }
            
            // Obtener datos del producto y verificar stock
            $stmt = $pdo->prepare("SELECT id, nombre, precio, stock FROM productos WHERE id = ? AND activo = 1");
            $stmt->execute([$input['producto_id']]);
            $producto = $stmt->fetch();
            
            if (!$producto) {
                throw new Exception('Producto no encontrado');
            }
            
            $cantidad = intval($input['cantidad']);
            if ($producto['stock'] < $cantidad) {
                throw new Exception('Stock insuficiente. Disponible: ' . $producto['stock']);
            }
            
            // Calcular total
            $precio_unitario = floatval($producto['precio']);
            $total = $precio_unitario * $cantidad;
            
            // Crear la venta
            $stmt = $pdo->prepare("
                INSERT INTO ventas (cliente_id, fecha_venta, total, estado, usuario_id) 
                VALUES (?, NOW(), ?, 'completada', ?)
            ");
            $stmt->execute([$input['cliente_id'], $total, $user_data['user_id']]);
            $venta_id = $pdo->lastInsertId();
            
            // Crear detalle de venta
            $stmt = $pdo->prepare("
                INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio_unitario, subtotal) 
                VALUES (?, ?, ?, ?, ?)
            ");
            $stmt->execute([$venta_id, $input['producto_id'], $cantidad, $precio_unitario, $total]);
            
            // Actualizar stock del producto
            $stmt = $pdo->prepare("UPDATE productos SET stock = stock - ? WHERE id = ?");
            $stmt->execute([$cantidad, $input['producto_id']]);
            
            $pdo->commit();
            
            echo json_encode([
                'success' => true,
                'message' => 'Venta creada exitosamente',
                'venta_id' => $venta_id,
                'total' => $total
            ]);
            
        } catch (Exception $e) {
            $pdo->rollBack();
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => $e->getMessage()]);
        } catch (PDOException $e) {
            $pdo->rollBack();
            http_response_code(500);
            echo json_encode(['success' => false, 'message' => 'Error al crear venta']);
            error_log("Error creando venta: " . $e->getMessage());
        }
        break;
        
    case 'DELETE':
        // Eliminar venta (cancelar)
        $venta_id = $_GET['id'] ?? null;
        
        if (!$venta_id) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'ID de la venta requerido']);
            break;
        }
        
        try {
            $pdo->beginTransaction();
            
            // Obtener detalles de la venta para restaurar stock
            $stmt = $pdo->prepare("
                SELECT dv.producto_id, dv.cantidad 
                FROM detalle_venta dv 
                INNER JOIN ventas v ON dv.venta_id = v.id 
                WHERE v.id = ? AND v.estado != 'cancelada'
            ");
            $stmt->execute([$venta_id]);
            $detalles = $stmt->fetchAll();
            
            if (empty($detalles)) {
                throw new Exception('Venta no encontrada o ya está cancelada');
            }
            
            // Restaurar stock de los productos
            foreach ($detalles as $detalle) {
                $stmt = $pdo->prepare("UPDATE productos SET stock = stock + ? WHERE id = ?");
                $stmt->execute([$detalle['cantidad'], $detalle['producto_id']]);
            }
            
            // Cambiar estado de la venta a cancelada
            $stmt = $pdo->prepare("UPDATE ventas SET estado = 'cancelada' WHERE id = ?");
            $stmt->execute([$venta_id]);
            
            $pdo->commit();
            
            echo json_encode([
                'success' => true,
                'message' => 'Venta cancelada exitosamente'
            ]);
            
        } catch (Exception $e) {
            $pdo->rollBack();
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => $e->getMessage()]);
        } catch (PDOException $e) {
            $pdo->rollBack();
            http_response_code(500);
            echo json_encode(['success' => false, 'message' => 'Error al cancelar venta']);
            error_log("Error cancelando venta: " . $e->getMessage());
        }
        break;
        
    default:
        http_response_code(405);
        echo json_encode(['success' => false, 'message' => 'Método no permitido']);
        break;
}
?>