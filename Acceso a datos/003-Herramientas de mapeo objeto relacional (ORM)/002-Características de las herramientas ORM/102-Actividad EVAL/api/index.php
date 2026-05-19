<?php
/**
 * API REST para Seguimiento de Entrenamientos
 * Maneja peticiones GET con rutas:
 * - action=tablas ............... Lista todas las tablas
 * - action=seleccionar&tabla=X .. Obtiene datos de una tabla
 * - action=buscar&tabla=X&campo=Y&valor=Z  Búsqueda
 */

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE');

require_once('../lib/JVDB.php');
require_once('../config.php');

// Obtener configuración
$config = obtenerConfiguracion();
$host = $config['host'];
$usuario = $config['usuario'];
$contrasena = $config['contrasena'];
$basedatos = $config['basedatos'];

try {
    // Conectar a BD
    $db = new JVDB($host, $usuario, $contrasena, $basedatos);
    
    // Obtener acción
    $action = isset($_GET['action']) ? $_GET['action'] : 'tablas';
    
    switch ($action) {
        case 'tablas':
            // Listar todas las tablas
            echo $db->tablas();
            break;
            
        case 'seleccionar':
            // Seleccionar datos de una tabla
            $tabla = isset($_GET['tabla']) ? $_GET['tabla'] : null;
            
            if (!$tabla) {
                http_response_code(400);
                echo json_encode(['error' => 'Parámetro tabla requerido'], JSON_UNESCAPED_UNICODE);
                break;
            }
            
            // Validar que tabla existe
            $todas = json_decode($db->tablas(), true);
            if (!in_array($tabla, $todas)) {
                http_response_code(400);
                echo json_encode(['error' => 'Tabla no permitida'], JSON_UNESCAPED_UNICODE);
                break;
            }
            
            echo $db->seleccionar($tabla);
            break;
            
        case 'buscar':
            // Buscar registros
            $tabla = isset($_GET['tabla']) ? $_GET['tabla'] : null;
            $campo = isset($_GET['campo']) ? $_GET['campo'] : null;
            $valor = isset($_GET['valor']) ? $_GET['valor'] : null;
            
            if (!$tabla || !$campo || !$valor) {
                http_response_code(400);
                echo json_encode(
                    ['error' => 'Parámetros tabla, campo y valor requeridos'],
                    JSON_UNESCAPED_UNICODE
                );
                break;
            }
            
            // Validar tabla
            $todas = json_decode($db->tablas(), true);
            if (!in_array($tabla, $todas)) {
                http_response_code(400);
                echo json_encode(['error' => 'Tabla no permitida'], JSON_UNESCAPED_UNICODE);
                break;
            }
            
            echo $db->buscar($tabla, $campo, $valor);
            break;
            
        default:
            http_response_code(400);
            echo json_encode(
                ['error' => 'Acción no reconocida', 'acciones_disponibles' => ['tablas', 'seleccionar', 'buscar']],
                JSON_UNESCAPED_UNICODE
            );
    }
    
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(
        ['error' => $e->getMessage()],
        JSON_UNESCAPED_UNICODE
    );
}
?>

