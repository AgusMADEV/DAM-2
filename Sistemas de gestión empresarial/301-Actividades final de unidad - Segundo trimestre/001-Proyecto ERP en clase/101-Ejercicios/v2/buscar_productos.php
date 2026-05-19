<?php
session_start();

// Cargar configuración
require_once 'config.php';

// =============================================
// API DE BÚSQUEDA DE PRODUCTOS
// Sistema profesional de búsqueda con filtros avanzados
// =============================================

// Verificar sesión
if (!isset($_SESSION['usuario'])) {
    http_response_code(401);
    echo json_encode(['error' => 'No autorizado']);
    exit;
}

// Conexión a la base de datos
$conexion = obtener_conexion();
if (!$conexion) {
    http_response_code(500);
    echo json_encode(['error' => 'Error de conexión a la base de datos']);
    exit;
}

// =============================================
// PARÁMETROS DE BÚSQUEDA
// =============================================

$accion = $_GET['accion'] ?? 'buscar';

// Parámetros de búsqueda
$texto = $_GET['q'] ?? '';
$id_equipo = $_GET['equipo'] ?? '';
$id_liga = $_GET['liga'] ?? '';
$id_marca = $_GET['marca'] ?? '';
$id_temporada = $_GET['temporada'] ?? '';
$id_tipo_camiseta = $_GET['tipo'] ?? '';
$id_talla = $_GET['talla'] ?? '';
$precio_min = $_GET['precio_min'] ?? '';
$precio_max = $_GET['precio_max'] ?? '';
$solo_stock = isset($_GET['solo_stock']) && $_GET['solo_stock'] === '1';
$destacados = isset($_GET['destacados']) && $_GET['destacados'] === '1';
$es_seleccion = $_GET['es_seleccion'] ?? '';

// Parámetros de paginación y ordenamiento
$pagina = max(1, intval($_GET['pagina'] ?? 1));
$por_pagina = min(50, max(5, intval($_GET['por_pagina'] ?? 12)));
$orden_campo = $_GET['orden'] ?? 'p.fecha_creacion';
$orden_dir = (($_GET['dir'] ?? 'DESC') === 'ASC') ? 'ASC' : 'DESC';

$offset = ($pagina - 1) * $por_pagina;

// =============================================
// FUNCIONES AUXILIARES
// =============================================

/**
 * Construir consulta SQL con filtros dinámicos
 */
function construir_consulta_busqueda($conexion, $filtros) {
    $sql = "SELECT 
        p.id_producto,
        p.codigo_producto,
        p.nombre_producto,
        p.descripcion,
        p.precio,
        p.stock,
        p.jugador,
        p.numero_dorsal,
        p.version_jugador,
        p.destacado,
        p.activo,
        p.fecha_creacion,
        
        e.nombre_equipo,
        e.nombre_completo as equipo_completo,
        e.es_seleccion,
        
        m.nombre_marca,
        
        t.nombre_temporada,
        t.ano_inicio,
        t.ano_fin,
        
        tc.nombre_tipo as tipo_camiseta,
        
        ta.nombre_talla,
        
        l.nombre_liga,
        
        pa.nombre_pais
        
    FROM productos p
    INNER JOIN equipos e ON p.id_equipo = e.id_equipo
    INNER JOIN marcas m ON p.id_marca = m.id_marca
    INNER JOIN temporadas t ON p.id_temporada = t.id_temporada
    INNER JOIN tipos_camiseta tc ON p.id_tipo_camiseta = tc.id_tipo_camiseta
    INNER JOIN tallas ta ON p.id_talla = ta.id_talla
    LEFT JOIN ligas l ON e.id_liga = l.id_liga
    LEFT JOIN paises pa ON e.id_pais = pa.id_pais
    WHERE 1=1";
    
    $condiciones = [];
    
    // Búsqueda por texto
    if (!empty($filtros['texto'])) {
        $texto_escapado = mysqli_real_escape_string($conexion, $filtros['texto']);
        $condiciones[] = "(
            p.nombre_producto LIKE '%{$texto_escapado}%' OR
            p.descripcion LIKE '%{$texto_escapado}%' OR
            p.codigo_producto LIKE '%{$texto_escapado}%' OR
            e.nombre_equipo LIKE '%{$texto_escapado}%' OR
            e.nombre_completo LIKE '%{$texto_escapado}%' OR
            m.nombre_marca LIKE '%{$texto_escapado}%' OR
            p.jugador LIKE '%{$texto_escapado}%'
        )";
    }
    
    // Filtro por equipo
    if (!empty($filtros['id_equipo'])) {
        $id_equipo = intval($filtros['id_equipo']);
        $condiciones[] = "p.id_equipo = {$id_equipo}";
    }
    
    // Filtro por liga
    if (!empty($filtros['id_liga'])) {
        $id_liga = intval($filtros['id_liga']);
        $condiciones[] = "e.id_liga = {$id_liga}";
    }
    
    // Filtro por marca
    if (!empty($filtros['id_marca'])) {
        $id_marca = intval($filtros['id_marca']);
        $condiciones[] = "p.id_marca = {$id_marca}";
    }
    
    // Filtro por temporada
    if (!empty($filtros['id_temporada'])) {
        $id_temporada = intval($filtros['id_temporada']);
        $condiciones[] = "p.id_temporada = {$id_temporada}";
    }
    
    // Filtro por tipo de camiseta
    if (!empty($filtros['id_tipo_camiseta'])) {
        $id_tipo = intval($filtros['id_tipo_camiseta']);
        $condiciones[] = "p.id_tipo_camiseta = {$id_tipo}";
    }
    
    // Filtro por talla
    if (!empty($filtros['id_talla'])) {
        $id_talla = intval($filtros['id_talla']);
        $condiciones[] = "p.id_talla = {$id_talla}";
    }
    
    // Filtro por rango de precio
    if (!empty($filtros['precio_min'])) {
        $precio_min = floatval($filtros['precio_min']);
        $condiciones[] = "p.precio >= {$precio_min}";
    }
    
    if (!empty($filtros['precio_max'])) {
        $precio_max = floatval($filtros['precio_max']);
        $condiciones[] = "p.precio <= {$precio_max}";
    }
    
    // Solo productos con stock
    if ($filtros['solo_stock']) {
        $condiciones[] = "p.stock > 0";
    }
    
    // Solo productos destacados
    if ($filtros['destacados']) {
        $condiciones[] = "p.destacado = 1";
    }
    
    // Filtro por selección nacional o club
    if ($filtros['es_seleccion'] !== '') {
        $es_seleccion = intval($filtros['es_seleccion']);
        $condiciones[] = "e.es_seleccion = {$es_seleccion}";
    }
    
    // Solo productos activos
    $condiciones[] = "p.activo = 1";
    
    // Agregar condiciones a la consulta
    if (!empty($condiciones)) {
        $sql .= " AND " . implode(" AND ", $condiciones);
    }
    
    return $sql;
}

/**
 * Obtener opciones para filtros
 */
function obtener_opciones_filtros($conexion) {
    $opciones = [];
    
    // Equipos
    $sql_equipos = "SELECT id_equipo, nombre_equipo, es_seleccion FROM equipos WHERE activo = 1 ORDER BY nombre_equipo";
    $result = mysqli_query($conexion, $sql_equipos);
    $opciones['equipos'] = [];
    while ($row = mysqli_fetch_assoc($result)) {
        $opciones['equipos'][] = $row;
    }
    
    // Ligas
    $sql_ligas = "SELECT id_liga, nombre_liga FROM ligas WHERE activo = 1 ORDER BY nombre_liga";
    $result = mysqli_query($conexion, $sql_ligas);
    $opciones['ligas'] = [];
    while ($row = mysqli_fetch_assoc($result)) {
        $opciones['ligas'][] = $row;
    }
    
    // Marcas
    $sql_marcas = "SELECT id_marca, nombre_marca FROM marcas WHERE activo = 1 ORDER BY nombre_marca";
    $result = mysqli_query($conexion, $sql_marcas);
    $opciones['marcas'] = [];
    while ($row = mysqli_fetch_assoc($result)) {
        $opciones['marcas'][] = $row;
    }
    
    // Temporadas
    $sql_temporadas = "SELECT id_temporada, nombre_temporada FROM temporadas ORDER BY ano_inicio DESC";
    $result = mysqli_query($conexion, $sql_temporadas);
    $opciones['temporadas'] = [];
    while ($row = mysqli_fetch_assoc($result)) {
        $opciones['temporadas'][] = $row;
    }
    
    // Tipos de camiseta
    $sql_tipos = "SELECT id_tipo_camiseta, nombre_tipo FROM tipos_camiseta ORDER BY nombre_tipo";
    $result = mysqli_query($conexion, $sql_tipos);
    $opciones['tipos'] = [];
    while ($row = mysqli_fetch_assoc($result)) {
        $opciones['tipos'][] = $row;
    }
    
    // Tallas
    $sql_tallas = "SELECT id_talla, nombre_talla FROM tallas ORDER BY orden";
    $result = mysqli_query($conexion, $sql_tallas);
    $opciones['tallas'] = [];
    while ($row = mysqli_fetch_assoc($result)) {
        $opciones['tallas'][] = $row;
    }
    
    // Rango de precios
    $sql_precios = "SELECT MIN(precio) as min, MAX(precio) as max FROM productos WHERE activo = 1";
    $result = mysqli_query($conexion, $sql_precios);
    $row = mysqli_fetch_assoc($result);
    $opciones['precio_min'] = floatval($row['min'] ?? 0);
    $opciones['precio_max'] = floatval($row['max'] ?? 0);
    
    return $opciones;
}

/**
 * Obtener estadísticas de búsqueda
 */
function obtener_estadisticas($conexion, $filtros) {
    $sql_base = construir_consulta_busqueda($conexion, $filtros);
    
    $sql_stats = "SELECT 
        COUNT(*) as total,
        AVG(p.precio) as precio_promedio,
        MIN(p.precio) as precio_minimo,
        MAX(p.precio) as precio_maximo,
        SUM(p.stock) as stock_total
    FROM productos p
    INNER JOIN equipos e ON p.id_equipo = e.id_equipo
    INNER JOIN marcas m ON p.id_marca = m.id_marca
    INNER JOIN temporadas t ON p.id_temporada = t.id_temporada
    INNER JOIN tipos_camiseta tc ON p.id_tipo_camiseta = tc.id_tipo_camiseta
    INNER JOIN tallas ta ON p.id_talla = ta.id_talla
    LEFT JOIN ligas l ON e.id_liga = l.id_liga
    LEFT JOIN paises pa ON e.id_pais = pa.id_pais
    WHERE 1=1";
    
    // Copiar las mismas condiciones
    preg_match('/WHERE 1=1(.*)$/s', $sql_base, $matches);
    if (isset($matches[1])) {
        $sql_stats .= $matches[1];
    }
    
    $result = mysqli_query($conexion, $sql_stats);
    return mysqli_fetch_assoc($result);
}

// =============================================
// PROCESAMIENTO DE ACCIONES
// =============================================

header('Content-Type: application/json; charset=utf-8');

switch ($accion) {
    case 'buscar':
        // Construir filtros
        $filtros = [
            'texto' => $texto,
            'id_equipo' => $id_equipo,
            'id_liga' => $id_liga,
            'id_marca' => $id_marca,
            'id_temporada' => $id_temporada,
            'id_tipo_camiseta' => $id_tipo_camiseta,
            'id_talla' => $id_talla,
            'precio_min' => $precio_min,
            'precio_max' => $precio_max,
            'solo_stock' => $solo_stock,
            'destacados' => $destacados,
            'es_seleccion' => $es_seleccion
        ];
        
        // Construir consulta base
        $sql_base = construir_consulta_busqueda($conexion, $filtros);
        
        // Obtener estadísticas
        $stats = obtener_estadisticas($conexion, $filtros);
        
        // Agregar ordenamiento y límite
        $campos_orden_validos = [
            'p.nombre_producto',
            'p.precio',
            'p.stock',
            'p.fecha_creacion',
            'e.nombre_equipo',
            'm.nombre_marca',
            't.nombre_temporada'
        ];
        
        if (!in_array($orden_campo, $campos_orden_validos)) {
            $orden_campo = 'p.fecha_creacion';
        }
        
        $sql_completa = $sql_base . " ORDER BY {$orden_campo} {$orden_dir} LIMIT {$offset}, {$por_pagina}";
        
        // Ejecutar consulta
        $result = mysqli_query($conexion, $sql_completa);
        
        if (!$result) {
            echo json_encode([
                'error' => 'Error en la consulta: ' . mysqli_error($conexion)
            ]);
            break;
        }
        
        $productos = [];
        while ($row = mysqli_fetch_assoc($result)) {
            $productos[] = $row;
        }
        
        $total_resultados = intval($stats['total']);
        $total_paginas = ceil($total_resultados / $por_pagina);
        
        echo json_encode([
            'success' => true,
            'productos' => $productos,
            'total_resultados' => $total_resultados,
            'total_paginas' => $total_paginas,
            'pagina_actual' => $pagina,
            'por_pagina' => $por_pagina,
            'estadisticas' => [
                'total' => intval($stats['total']),
                'precio_promedio' => floatval($stats['precio_promedio'] ?? 0),
                'precio_minimo' => floatval($stats['precio_minimo'] ?? 0),
                'precio_maximo' => floatval($stats['precio_maximo'] ?? 0),
                'stock_total' => intval($stats['stock_total'] ?? 0)
            ]
        ], JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
        break;
    
    case 'filtros':
        // Devolver opciones para los filtros
        $opciones = obtener_opciones_filtros($conexion);
        echo json_encode([
            'success' => true,
            'opciones' => $opciones
        ], JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
        break;
    
    case 'autocompletar':
        // Autocompletado rápido
        if (strlen($texto) < 2) {
            echo json_encode(['sugerencias' => []]);
            break;
        }
        
        $texto_escapado = mysqli_real_escape_string($conexion, $texto);
        
        $sql = "SELECT DISTINCT
            p.nombre_producto,
            e.nombre_equipo,
            m.nombre_marca
        FROM productos p
        INNER JOIN equipos e ON p.id_equipo = e.id_equipo
        INNER JOIN marcas m ON p.id_marca = m.id_marca
        WHERE p.activo = 1 AND (
            p.nombre_producto LIKE '%{$texto_escapado}%' OR
            e.nombre_equipo LIKE '%{$texto_escapado}%' OR
            m.nombre_marca LIKE '%{$texto_escapado}%'
        )
        LIMIT 10";
        
        $result = mysqli_query($conexion, $sql);
        $sugerencias = [];
        
        while ($row = mysqli_fetch_assoc($result)) {
            $sugerencias[] = [
                'producto' => $row['nombre_producto'],
                'equipo' => $row['nombre_equipo'],
                'marca' => $row['nombre_marca']
            ];
        }
        
        echo json_encode([
            'success' => true,
            'sugerencias' => $sugerencias
        ], JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
        break;
    
    default:
        http_response_code(400);
        echo json_encode(['error' => 'Acción no válida']);
        break;
}

cerrar_conexion($conexion);
