<?php
require_once '../config/database.php';

// Verificar autenticación
$user_data = requireAuth();

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    try {
        // Obtener estadísticas del dashboard
        
        // Total de clientes
        $stmt = $pdo->query("SELECT COUNT(*) as total FROM clientes WHERE activo = 1");
        $totalClientes = $stmt->fetch()['total'];
        
        // Total de productos
        $stmt = $pdo->query("SELECT COUNT(*) as total FROM productos WHERE activo = 1");
        $totalProductos = $stmt->fetch()['total'];
        
        // Ventas del mes actual
        $stmt = $pdo->query("
            SELECT COALESCE(SUM(total), 0) as ventas_mes 
            FROM ventas 
            WHERE MONTH(fecha_venta) = MONTH(CURRENT_DATE()) 
            AND YEAR(fecha_venta) = YEAR(CURRENT_DATE())
        ");
        $ventasMes = $stmt->fetch()['ventas_mes'];
        
        // Productos con stock bajo (menos de 10 unidades)
        $stmt = $pdo->query("SELECT COUNT(*) as total FROM productos WHERE stock < 10 AND activo = 1");
        $stockBajo = $stmt->fetch()['total'];
        
        echo json_encode([
            'success' => true,
            'stats' => [
                'totalClientes' => (int)$totalClientes,
                'totalProductos' => (int)$totalProductos,
                'ventasMes' => number_format($ventasMes, 2),
                'stockBajo' => (int)$stockBajo
            ]
        ]);
        
    } catch (PDOException $e) {
        http_response_code(500);
        echo json_encode(['success' => false, 'message' => 'Error al obtener estadísticas']);
        error_log("Error en dashboard-stats: " . $e->getMessage());
    }
} else {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Método no permitido']);
}
?>