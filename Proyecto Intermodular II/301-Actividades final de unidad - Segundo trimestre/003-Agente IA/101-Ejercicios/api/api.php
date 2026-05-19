<?php
/**
 * API REST para el Agente IA Autónomo
 * Endpoints principales para controlar el agente
 */

// Headers PRIMERO, antes de cualquier salida
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization');

// Si es OPTIONS, devolver 200
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

// Capturar errores y devolverlos como JSON
set_error_handler(function($errno, $errstr, $errfile, $errline) {
    // Limpiar cualquier salida previa
    if (ob_get_length()) {
        ob_clean();
    }
    
    http_response_code(500);
    echo json_encode([
        'exito' => false,
        'error' => $errstr,
        'archivo' => basename($errfile),
        'linea' => $errline
    ]);
    exit;
});

// Iniciar output buffering para capturar errores
ob_start();

require_once __DIR__ . '/../config/config.php';
require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/../classes/Logger.php';
require_once __DIR__ . '/../classes/IAService.php';
require_once __DIR__ . '/../classes/AgenteIA.php';

// Router simple basado en parámetros
$method = $_SERVER['REQUEST_METHOD'];
$action = $_GET['action'] ?? $_POST['action'] ?? '';

// Leer datos POST como JSON
$inputData = file_get_contents('php://input');
$data = json_decode($inputData, true) ?? $_POST;

try {
    switch ($action) {
        // Listar misiones
        case 'listar_misiones':
            listarMisiones();
            break;

        // Crear nueva misión
        case 'crear_mision':
            crearMision($data);
            break;

        // Obtener detalle de misión
        case 'obtener_mision':
            $id = $_GET['id'] ?? $data['id'] ?? null;
            if ($id) obtenerMision($id);
            else respuestaJSON(['error' => 'ID requerido'], 400);
            break;

        // Obtener iteración completa (sin truncar)
        case 'obtener_iteracion_completa':
            $iteracionId = $_GET['iteracion_id'] ?? $data['iteracion_id'] ?? null;
            if ($iteracionId) obtenerIteracionCompleta($iteracionId);
            else respuestaJSON(['error' => 'iteracion_id requerido'], 400);
            break;

        // Ejecutar misión
        case 'ejecutar_mision':
            $id = $_GET['id'] ?? $data['id'] ?? null;
            if ($id) ejecutarMision($id);
            else respuestaJSON(['error' => 'ID requerido'], 400);
            break;

        // Eliminar misión
        case 'eliminar_mision':
            $id = $_GET['id'] ?? $data['id'] ?? null;
            if ($id) eliminarMision($id);
            else respuestaJSON(['error' => 'ID requerido'], 400);
            break;

        // Reiniciar misión
        case 'reiniciar_mision':
            $id = $_GET['id'] ?? $data['id'] ?? null;
            if ($id) reiniciarMision($id);
            else respuestaJSON(['error' => 'ID requerido'], 400);
            break;

        // Listar iteraciones
        case 'listar_iteraciones':
            $id = $_GET['id'] ?? $data['id'] ?? null;
            if ($id) listarIteraciones($id);
            else respuestaJSON(['error' => 'ID requerido'], 400);
            break;

        // Obtener logs
        case 'logs':
            obtenerLogs($data);
            break;

        // Obtener configuración
        case 'obtener_config':
            obtenerConfiguracion();
            break;

        // Actualizar configuración
        case 'actualizar_config':
            actualizarConfiguracion($data);
            break;

        // Estadísticas
        case 'stats':
            obtenerEstadisticas();
            break;

        default:
            respuestaJSON(['error' => 'Acción no válida: ' . $action], 400);
    }
} catch (Exception $e) {
    // Limpiar buffer de salida
    if (ob_get_length()) {
        ob_clean();
    }
    
    error_log("API Error: " . $e->getMessage() . " in " . $e->getFile() . ":" . $e->getLine());
    
    respuestaJSON([
        'error' => $e->getMessage(),
        'archivo' => basename($e->getFile()),
        'linea' => $e->getLine(),
        'trace' => explode("\n", $e->getTraceAsString())
    ], 500);
} catch (Error $e) {
    // Capturar errores fatales de PHP 7+
    if (ob_get_length()) {
        ob_clean();
    }
    
    error_log("API Fatal Error: " . $e->getMessage() . " in " . $e->getFile() . ":" . $e->getLine());
    
    respuestaJSON([
        'error' => 'Error fatal: ' . $e->getMessage(),
        'archivo' => basename($e->getFile()),
        'linea' => $e->getLine()
    ], 500);
}

// ============ FUNCIONES DE LA API ============

function crearMision($data) {
    if (empty($data['titulo']) || empty($data['objetivo_final'])) {
        respuestaJSON(['error' => 'Faltan datos obligatorios'], 400);
    }

    $db = Database::getInstance()->getConnection();
    
    $stmt = $db->prepare("
        INSERT INTO misiones (titulo, descripcion, objetivo_final, prioridad)
        VALUES (?, ?, ?, ?)
    ");
    
    $stmt->execute([
        $data['titulo'],
        $data['descripcion'] ?? '',
        $data['objetivo_final'],
        $data['prioridad'] ?? 'media'
    ]);

    $misionId = $db->lastInsertId();

    respuestaJSON([
        'exito' => true,
        'mensaje' => 'Misión creada exitosamente',
        'mision_id' => $misionId
    ], 201);
}

function listarMisiones() {
    $db = Database::getInstance()->getConnection();
    
    $stmt = $db->query("
        SELECT m.*, 
               COUNT(i.id) as total_iteraciones,
               MAX(i.timestamp_inicio) as ultima_iteracion
        FROM misiones m
        LEFT JOIN iteraciones i ON m.id = i.mision_id
        GROUP BY m.id
        ORDER BY m.fecha_creacion DESC
    ");
    
    $misiones = $stmt->fetchAll();

    respuestaJSON([
        'exito' => true,
        'misiones' => $misiones,
        'total' => count($misiones)
    ]);
}

function obtenerMision($misionId) {
    try {
        $db = Database::getInstance()->getConnection();
        
        $stmt = $db->prepare("SELECT * FROM misiones WHERE id = ?");
        $stmt->execute([$misionId]);
        $mision = $stmt->fetch(PDO::FETCH_ASSOC);

        if (!$mision) {
            respuestaJSON(['error' => 'Misión no encontrada', 'exito' => false], 404);
        }

        // Obtener iteraciones (solo campos esenciales para evitar memory exhaustion)
        $stmt = $db->prepare("
            SELECT 
                id,
                mision_id,
                numero_iteracion,
                tipo_accion,
                SUBSTR(descripcion, 1, 500) as descripcion,
                resultado,
                SUBSTR(error_mensaje, 1, 500) as error_mensaje,
                duracion_segundos,
                timestamp_inicio,
                timestamp_fin
            FROM iteraciones 
            WHERE mision_id = ? 
            ORDER BY numero_iteracion ASC
            LIMIT 50
        ");
        $stmt->execute([$misionId]);
        $iteraciones = $stmt->fetchAll(PDO::FETCH_ASSOC);

        respuestaJSON([
            'exito' => true,
            'mision' => $mision,
            'iteraciones' => $iteraciones,
            'total_iteraciones' => count($iteraciones)
        ]);
    } catch (Exception $e) {
        error_log("Error en obtenerMision: " . $e->getMessage());
        respuestaJSON([
            'error' => 'Error al obtener misión: ' . $e->getMessage(),
            'exito' => false
        ], 500);
    }
}

/**
 * Obtener iteración completa con todos los campos (análisis, planificación, ejecución, validación)
 */
function obtenerIteracionCompleta($iteracionId) {
    try {
        $db = Database::getInstance()->getConnection();
        
        $stmt = $db->prepare("
            SELECT 
                id,
                mision_id,
                numero_iteracion,
                tipo_accion,
                descripcion,
                entrada,
                salida,
                codigo_generado,
                resultado,
                error_mensaje,
                duracion_segundos,
                timestamp_inicio,
                timestamp_fin,
                metadata
            FROM iteraciones 
            WHERE id = ?
        ");
        $stmt->execute([$iteracionId]);
        $iteracion = $stmt->fetch(PDO::FETCH_ASSOC);

        if (!$iteracion) {
            respuestaJSON(['error' => 'Iteración no encontrada', 'exito' => false], 404);
        }

        // Decodificar JSON fields
        if ($iteracion['metadata']) {
            $iteracion['metadata_decoded'] = json_decode($iteracion['metadata'], true);
        }
        if ($iteracion['salida']) {
            $iteracion['salida_decoded'] = json_decode($iteracion['salida'], true);
        }

        respuestaJSON([
            'exito' => true,
            'iteracion' => $iteracion
        ]);
    } catch (Exception $e) {
        error_log("Error en obtenerIteracionCompleta: " . $e->getMessage());
        respuestaJSON([
            'error' => 'Error al obtener iteración: ' . $e->getMessage(),
            'exito' => false
        ], 500);
    }
}

function ejecutarMision($misionId) {
    // Sin límite de tiempo para misiones complejas
    set_time_limit(0);
    ini_set('max_execution_time', 0);
    
    // Esta función ejecuta el agente
    // NOTA: En un entorno real, esto debería ejecutarse en background
    
    try {
        // Verificar que las clases necesarias existan
        if (!class_exists('AgenteIA')) {
            require_once __DIR__ . '/../classes/AgenteIA.php';
        }
        if (!class_exists('Logger')) {
            require_once __DIR__ . '/../classes/Logger.php';
        }
        
        $agente = new AgenteIA($misionId);
        $resultado = $agente->ejecutar();
        
        respuestaJSON([
            'exito' => true,
            'resultado' => $resultado
        ]);
    } catch (Exception $e) {
        respuestaJSON([
            'exito' => false,
            'error' => $e->getMessage(),
            'trace' => $e->getTraceAsString()
        ], 500);
    } catch (Error $e) {
        respuestaJSON([
            'exito' => false,
            'error' => 'Error fatal: ' . $e->getMessage(),
            'trace' => $e->getTraceAsString()
        ], 500);
    }
}

function listarIteraciones($misionId) {
    $db = Database::getInstance()->getConnection();
    
    $stmt = $db->prepare("
        SELECT i.*, 
               COUNT(d.id) as total_decisiones
        FROM iteraciones i
        LEFT JOIN decisiones d ON i.id = d.iteracion_id
        WHERE i.mision_id = ?
        GROUP BY i.id
        ORDER BY i.numero_iteracion ASC
    ");
    $stmt->execute([$misionId]);
    $iteraciones = $stmt->fetchAll();

    respuestaJSON([
        'exito' => true,
        'iteraciones' => $iteraciones,
        'total' => count($iteraciones)
    ]);
}

function obtenerLogs($params) {
    $db = Database::getInstance()->getConnection();
    
    $where = [];
    $values = [];
    
    if (!empty($params['mision_id'])) {
        $where[] = 'mision_id = ?';
        $values[] = $params['mision_id'];
    }
    
    if (!empty($params['nivel'])) {
        $where[] = 'nivel = ?';
        $values[] = $params['nivel'];
    }
    
    $limit = $params['limit'] ?? 100;
    
    $sql = "SELECT * FROM logs_agente";
    if (!empty($where)) {
        $sql .= " WHERE " . implode(' AND ', $where);
    }
    $sql .= " ORDER BY timestamp DESC LIMIT ?";
    $values[] = $limit;
    
    $stmt = $db->prepare($sql);
    $stmt->execute($values);
    $logs = $stmt->fetchAll();

    respuestaJSON([
        'exito' => true,
        'logs' => $logs,
        'total' => count($logs)
    ]);
}

function obtenerConfiguracion() {
    $db = Database::getInstance()->getConnection();
    
    $stmt = $db->query("SELECT * FROM configuracion ORDER BY clave ASC");
    $config = $stmt->fetchAll();

    respuestaJSON([
        'exito' => true,
        'configuracion' => $config
    ]);
}

function actualizarConfiguracion($data) {
    $db = Database::getInstance()->getConnection();
    
    foreach ($data as $clave => $valor) {
        $stmt = $db->prepare("
            UPDATE configuracion SET valor = ? WHERE clave = ?
        ");
        $stmt->execute([$valor, $clave]);
    }

    respuestaJSON([
        'exito' => true,
        'mensaje' => 'Configuración actualizada'
    ]);
}

function obtenerEstadisticas() {
    $db = Database::getInstance()->getConnection();
    
    // Misiones por estado
    $stmt = $db->query("
        SELECT estado, COUNT(*) as total
        FROM misiones
        GROUP BY estado
    ");
    $misionesPorEstado = $stmt->fetchAll(PDO::FETCH_KEY_PAIR);

    // Total de iteraciones
    $stmt = $db->query("SELECT COUNT(*) FROM iteraciones");
    $totalIteraciones = $stmt->fetchColumn();

    // Tasa de éxito
    $stmt = $db->query("
        SELECT 
            COUNT(CASE WHEN estado = 'completada' THEN 1 END) as completadas,
            COUNT(*) as total
        FROM misiones
    ");
    $tasas = $stmt->fetch();
    $tasaExito = $tasas['total'] > 0 ? ($tasas['completadas'] / $tasas['total']) * 100 : 0;

    // Promedio de iteraciones por misión
    $stmt = $db->query("
        SELECT AVG(total_iter) as promedio
        FROM (
            SELECT COUNT(*) as total_iter
            FROM iteraciones
            GROUP BY mision_id
        ) sub
    ");
    $promedioIteraciones = $stmt->fetchColumn() ?? 0;

    respuestaJSON([
        'exito' => true,
        'estadisticas' => [
            'misiones_por_estado' => $misionesPorEstado,
            'total_iteraciones' => $totalIteraciones,
            'tasa_exito' => round($tasaExito, 2),
            'promedio_iteraciones' => round($promedioIteraciones, 2)
        ]
    ]);
}

function eliminarMision($misionId) {
    $db = Database::getInstance()->getConnection();
    
    $stmt = $db->prepare("DELETE FROM misiones WHERE id = ?");
    $stmt->execute([$misionId]);

    respuestaJSON([
        'exito' => true,
        'mensaje' => 'Misión eliminada'
    ]);
}

function reiniciarMision($misionId) {
    $db = Database::getInstance()->getConnection();
    
    // Resetear el estado de la misión
    $stmt = $db->prepare("
        UPDATE misiones 
        SET estado = 'pendiente',
            progreso = 0,
            fecha_inicio = NULL,
            fecha_finalizacion = NULL,
            intentos_totales = 0,
            exitos = 0,
            fallos = 0
        WHERE id = ?
    ");
    $stmt->execute([$misionId]);
    
    // Eliminar iteraciones anteriores para empezar limpio
    $stmt = $db->prepare("DELETE FROM iteraciones WHERE mision_id = ?");
    $stmt->execute([$misionId]);

    respuestaJSON([
        'exito' => true,
        'mensaje' => 'Misión reiniciada correctamente'
    ]);
}

// Helper para respuestas JSON
function respuestaJSON($data, $statusCode = 200) {
    // Limpiar cualquier salida previa (errores, warnings, etc)
    if (ob_get_length()) {
        ob_clean();
    }
    
    // Asegurar que el header está configurado
    if (!headers_sent()) {
        header('Content-Type: application/json; charset=utf-8');
    }
    
    http_response_code($statusCode);
    echo json_encode($data, JSON_UNESCAPED_UNICODE);
    exit;
}
