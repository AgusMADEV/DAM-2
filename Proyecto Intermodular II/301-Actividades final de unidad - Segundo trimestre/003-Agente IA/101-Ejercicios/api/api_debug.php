<?php
/**
 * API Simplificada SOLO para debugging obtener_mision
 */

// LOGGING PRIMERO
file_put_contents(__DIR__ . '/../logs/api_debug.log', "=== INICIO ===\n", FILE_APPEND);
file_put_contents(__DIR__ . '/../logs/api_debug.log', "REQUEST: " . $_SERVER['REQUEST_URI'] . "\n", FILE_APPEND);

// Headers
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');

file_put_contents(__DIR__ . '/../logs/api_debug.log', "Headers enviados\n", FILE_APPEND);

// Cargar archivos
try {
    require_once __DIR__ . '/../config/config.php';
    file_put_contents(__DIR__ . '/../logs/api_debug.log', "config.php cargado\n", FILE_APPEND);
    
    require_once __DIR__ . '/../config/database.php';
    file_put_contents(__DIR__ . '/../logs/api_debug.log', "database.php cargado\n", FILE_APPEND);
} catch (Exception $e) {
    file_put_contents(__DIR__ . '/../logs/api_debug.log', "ERROR cargando: " . $e->getMessage() . "\n", FILE_APPEND);
    http_response_code(500);
    echo json_encode(['error' => 'Error al cargar configuración: ' . $e->getMessage()]);
    exit;
}

// Obtener parámetros
$action = $_GET['action'] ?? '';
$id = $_GET['id'] ?? null;

file_put_contents(__DIR__ . '/../logs/api_debug.log', "Action: $action, ID: $id\n", FILE_APPEND);

if ($action !== 'obtener_mision') {
    file_put_contents(__DIR__ . '/../logs/api_debug.log', "Acción no es obtener_mision\n", FILE_APPEND);
    http_response_code(400);
    echo json_encode(['error' => 'Esta API solo soporta obtener_mision']);
    exit;
}

if (!$id) {
    file_put_contents(__DIR__ . '/../logs/api_debug.log', "ID no proporcionado\n", FILE_APPEND);
    http_response_code(400);
    echo json_encode(['error' => 'ID requerido']);
    exit;
}

// Conectar a BD
try {
    $db = Database::getInstance()->getConnection();
    file_put_contents(__DIR__ . '/../logs/api_debug.log', "Conexión BD establecida\n", FILE_APPEND);
} catch (Exception $e) {
    file_put_contents(__DIR__ . '/../logs/api_debug.log', "ERROR BD: " . $e->getMessage() . "\n", FILE_APPEND);
    http_response_code(500);
    echo json_encode(['error' => 'Error de base de datos: ' . $e->getMessage()]);
    exit;
}

// Consultar misión
try {
    file_put_contents(__DIR__ . '/../logs/api_debug.log', "Consultando misión ID: $id\n", FILE_APPEND);
    
    $stmt = $db->prepare("SELECT * FROM misiones WHERE id = ?");
    $stmt->execute([$id]);
    $mision = $stmt->fetch(PDO::FETCH_ASSOC);
    
    file_put_contents(__DIR__ . '/../logs/api_debug.log', "Misión encontrada: " . ($mision ? 'SÍ' : 'NO') . "\n", FILE_APPEND);
    
    if (!$mision) {
        http_response_code(404);
        echo json_encode(['error' => 'Misión no encontrada', 'exito' => false]);
        exit;
    }
    
    // Obtener iteraciones
    file_put_contents(__DIR__ . '/../logs/api_debug.log', "Consultando iteraciones\n", FILE_APPEND);
    
    $stmt = $db->prepare("
        SELECT * FROM iteraciones 
        WHERE mision_id = ? 
        ORDER BY numero_iteracion ASC
    ");
    $stmt->execute([$id]);
    $iteraciones = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    file_put_contents(__DIR__ . '/../logs/api_debug.log', "Iteraciones encontradas: " . count($iteraciones) . "\n", FILE_APPEND);
    
    // Preparar respuesta
    $respuesta = [
        'exito' => true,
        'mision' => $mision,
        'iteraciones' => $iteraciones
    ];
    
    file_put_contents(__DIR__ . '/../logs/api_debug.log', "Preparando JSON de respuesta...\n", FILE_APPEND);
    
    $json = json_encode($respuesta, JSON_UNESCAPED_UNICODE);
    
    if ($json === false) {
        file_put_contents(__DIR__ . '/../logs/api_debug.log', "ERROR json_encode: " . json_last_error_msg() . "\n", FILE_APPEND);
        http_response_code(500);
        echo json_encode(['error' => 'Error al generar JSON: ' . json_last_error_msg()]);
        exit;
    }
    
    file_put_contents(__DIR__ . '/../logs/api_debug.log', "JSON generado correctamente (longitud: " . strlen($json) . ")\n", FILE_APPEND);
    file_put_contents(__DIR__ . '/../logs/api_debug.log', "Enviando respuesta...\n", FILE_APPEND);
    
    http_response_code(200);
    echo $json;
    
    file_put_contents(__DIR__ . '/../logs/api_debug.log', "=== FIN EXITOSO ===\n\n", FILE_APPEND);
    
} catch (Exception $e) {
    file_put_contents(__DIR__ . '/../logs/api_debug.log', "EXCEPCIÓN: " . $e->getMessage() . " en " . $e->getFile() . ":" . $e->getLine() . "\n", FILE_APPEND);
    http_response_code(500);
    echo json_encode([
        'error' => $e->getMessage(),
        'archivo' => basename($e->getFile()),
        'linea' => $e->getLine()
    ]);
}
