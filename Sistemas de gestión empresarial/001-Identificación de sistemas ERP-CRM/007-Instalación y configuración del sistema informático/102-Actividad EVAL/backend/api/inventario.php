<?php
require_once '../config/database.php';

// Verificar autenticación
$user_data = requireAuth();

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    try {
        // Obtener productos con stock bajo (menos de 10 unidades)
        $stmt = $pdo->query("
            SELECT id, nombre, stock 
            FROM productos 
            WHERE stock < 10 AND activo = 1 
            ORDER BY stock ASC
        ");
        $lowStock = $stmt->fetchAll();
        
        echo json_encode([
            'success' => true,
            'lowStock' => $lowStock
        ]);
        
    } catch (PDOException $e) {
        http_response_code(500);
        echo json_encode(['success' => false, 'message' => 'Error al obtener información de inventario']);
        error_log("Error en inventario: " . $e->getMessage());
    }
} else {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Método no permitido']);
}
?>