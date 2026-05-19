<?php
session_start();

// Cargar configuración
require_once 'config.php';

$login_error = "";

// =============================================
// GESTIÓN DE SESIÓN
// =============================================

// Logout
if (isset($_GET['logout'])) {
    session_unset();
    session_destroy();
    header("Location: ?");
    exit;
}

// Login
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['accion']) && $_POST['accion'] === 'login') {
    $user = $_POST['usuario'] ?? '';
    $pass = $_POST['contrasena'] ?? '';

    if ($user === LOGIN_USUARIO && $pass === LOGIN_PASSWORD) {
        $_SESSION['usuario'] = $user;
        header("Location: ?");
        exit;
    } else {
        $login_error = "Usuario o contraseña incorrectos";
    }
}

$logged_in = isset($_SESSION['usuario']);

// Conexión a la base de datos solo si hay sesión iniciada
if ($logged_in) {
    $conexion = obtener_conexion();
    if (!$conexion) {
        die("Error de conexión: " . mysqli_connect_error());
    }
}

// =============================================
// FUNCIONES DE ICONOS SVG
// =============================================

/**
 * Generar icono SVG simple
 */
function svg_icon($type, $size = 20, $color = 'currentColor') {
    $icons = [
        'check' => '<svg width="' . $size . '" height="' . $size . '" viewBox="0 0 24 24" fill="none" stroke="' . $color . '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>',
        'x' => '<svg width="' . $size . '" height="' . $size . '" viewBox="0 0 24 24" fill="none" stroke="' . $color . '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>',
        'search' => '<svg width="' . $size . '" height="' . $size . '" viewBox="0 0 24 24" fill="none" stroke="' . $color . '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><path d="m21 21-4.35-4.35"></path></svg>',
        'box' => '<svg width="' . $size . '" height="' . $size . '" viewBox="0 0 24 24" fill="none" stroke="' . $color . '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>',
        'user' => '<svg width="' . $size . '" height="' . $size . '" viewBox="0 0 24 24" fill="none" stroke="' . $color . '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>',
        'chart' => '<svg width="' . $size . '" height="' . $size . '" viewBox="0 0 24 24" fill="none" stroke="' . $color . '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="20" x2="12" y2="10"></line><line x1="18" y1="20" x2="18" y2="4"></line><line x1="6" y1="20" x2="6" y2="16"></line></svg>',
        'dollar' => '<svg width="' . $size . '" height="' . $size . '" viewBox="0 0 24 24" fill="none" stroke="' . $color . '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>',
        'tag' => '<svg width="' . $size . '" height="' . $size . '" viewBox="0 0 24 24" fill="none" stroke="' . $color . '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path><line x1="7" y1="7" x2="7.01" y2="7"></line></svg>',
        'star' => '<svg width="' . $size . '" height="' . $size . '" viewBox="0 0 24 24" fill="' . $color . '" stroke="' . $color . '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>',
        'globe' => '<svg width="' . $size . '" height="' . $size . '" viewBox="0 0 24 24" fill="none" stroke="' . $color . '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>',
        'shield' => '<svg width="' . $size . '" height="' . $size . '" viewBox="0 0 24 24" fill="none" stroke="' . $color . '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>',
        'chevron-down' => '<svg width="' . $size . '" height="' . $size . '" viewBox="0 0 24 24" fill="none" stroke="' . $color . '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>',
        'edit' => '<svg width="' . $size . '" height="' . $size . '" viewBox="0 0 24 24" fill="none" stroke="' . $color . '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>',
        'trash' => '<svg width="' . $size . '" height="' . $size . '" viewBox="0 0 24 24" fill="none" stroke="' . $color . '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>',
        'plus' => '<svg width="' . $size . '" height="' . $size . '" viewBox="0 0 24 24" fill="none" stroke="' . $color . '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>',
        'save' => '<svg width="' . $size . '" height="' . $size . '" viewBox="0 0 24 24" fill="none" stroke="' . $color . '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path><polyline points="17 21 17 13 7 13 7 21"></polyline><polyline points="7 3 7 8 15 8"></polyline></svg>',
        'file-text' => '<svg width="' . $size . '" height="' . $size . '" viewBox="0 0 24 24" fill="none" stroke="' . $color . '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>',
        'info' => '<svg width="' . $size . '" height="' . $size . '" viewBox="0 0 24 24" fill="none" stroke="' . $color . '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>',
        'list' => '<svg width="' . $size . '" height="' . $size . '" viewBox="0 0 24 24" fill="none" stroke="' . $color . '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>',
        'grid' => '<svg width="' . $size . '" height="' . $size . '" viewBox="0 0 24 24" fill="none" stroke="' . $color . '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>',
    ];
    return $icons[$type] ?? '';
}

// =============================================
// FUNCIONES AUXILIARES
// =============================================

/**
 * Obtener claves foráneas de una tabla
 */
function obtener_claves_foraneas($conexion, $tabla, $bd = DB_NAME) {
    $fk = [];
    $sql = "
        SELECT COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = '" . mysqli_real_escape_string($conexion, $bd) . "'
          AND TABLE_NAME = '" . mysqli_real_escape_string($conexion, $tabla) . "'
          AND REFERENCED_TABLE_NAME IS NOT NULL
    ";
    $resultado = mysqli_query($conexion, $sql);
    if ($resultado) {
        while ($fila = mysqli_fetch_assoc($resultado)) {
            $fk[$fila['COLUMN_NAME']] = [
                'tabla' => $fila['REFERENCED_TABLE_NAME'],
                'columna' => $fila['REFERENCED_COLUMN_NAME']
            ];
        }
    }
    return $fk;
}

/**
 * Obtener claves foráneas entrantes (tablas que apuntan a esta tabla)
 */
function obtener_claves_foraneas_entrantes($conexion, $tabla, $bd = DB_NAME) {
    $fk_entrantes = [];
    $sql = "
        SELECT TABLE_NAME, COLUMN_NAME, REFERENCED_COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = '" . mysqli_real_escape_string($conexion, $bd) . "'
          AND REFERENCED_TABLE_NAME = '" . mysqli_real_escape_string($conexion, $tabla) . "'
    ";
    $resultado = mysqli_query($conexion, $sql);
    if ($resultado) {
        while ($fila = mysqli_fetch_assoc($resultado)) {
            $fk_entrantes[] = [
                'tabla' => $fila['TABLE_NAME'],
                'columna' => $fila['COLUMN_NAME'],
                'columna_referenciada' => $fila['REFERENCED_COLUMN_NAME']
            ];
        }
    }
    return $fk_entrantes;
}

/**
 * Obtener metadatos de columnas de una tabla
 */
function obtener_meta_columnas($conexion, $tabla, $bd = DB_NAME) {
    $meta = [];
    $sql = "
        SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT,
               COLUMN_KEY, EXTRA, CHARACTER_MAXIMUM_LENGTH, COLUMN_TYPE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = '" . mysqli_real_escape_string($conexion, $bd) . "'
          AND TABLE_NAME = '" . mysqli_real_escape_string($conexion, $tabla) . "'
    ";
    $resultado = mysqli_query($conexion, $sql);
    if ($resultado) {
        while ($fila = mysqli_fetch_assoc($resultado)) {
            $meta[$fila['COLUMN_NAME']] = $fila;
        }
    }
    return $meta;
}

/**
 * Obtener nombre de la columna clave primaria
 */
function obtener_pk_columna($conexion, $tabla, $bd = DB_NAME) {
    $sql = "
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = '" . mysqli_real_escape_string($conexion, $bd) . "'
          AND TABLE_NAME = '" . mysqli_real_escape_string($conexion, $tabla) . "'
          AND COLUMN_KEY = 'PRI'
        ORDER BY ORDINAL_POSITION
        LIMIT 1
    ";
    $resultado = mysqli_query($conexion, $sql);
    if ($resultado && $fila = mysqli_fetch_assoc($resultado)) {
        return $fila['COLUMN_NAME'];
    }
    return null;
}

/**
 * Renderizar input apropiado según tipo de dato
 */
function render_input_para_columna($nombre_columna, $meta_columna, $valor_actual = "") {
    $data_type = strtolower($meta_columna['DATA_TYPE']);
    $column_type = strtolower($meta_columna['COLUMN_TYPE']);
    $html = "";

    $html .= "<label>" . htmlspecialchars($nombre_columna) . "</label>";

    // tinyint(1) -> checkbox
    if ($data_type === 'tinyint' && strpos($column_type, '(1)') !== false) {
        $checked = ($valor_actual == 1 || $valor_actual === "1") ? "checked" : "";
        $html .= "<input type='checkbox' name='" . $nombre_columna . "' value='1' " . $checked . ">";
        return $html;
    }

    switch ($data_type) {
        case 'varchar':
        case 'char':
        case 'tinytext':
            $html .= "<input type='text' name='" . $nombre_columna . "' placeholder='" . $nombre_columna . "' value='" . htmlspecialchars($valor_actual, ENT_QUOTES) . "'>";
            break;

        case 'text':
        case 'mediumtext':
        case 'longtext':
            $html .= "<textarea name='" . $nombre_columna . "' placeholder='" . $nombre_columna . "' rows='4'>" . htmlspecialchars($valor_actual, ENT_QUOTES) . "</textarea>";
            break;

        case 'int':
        case 'integer':
        case 'tinyint':
        case 'smallint':
        case 'mediumint':
        case 'bigint':
            $html .= "<input type='number' name='" . $nombre_columna . "' placeholder='" . $nombre_columna . "' value='" . htmlspecialchars($valor_actual, ENT_QUOTES) . "' step='1'>";
            break;

        case 'decimal':
        case 'numeric':
        case 'float':
        case 'double':
            $html .= "<input type='number' name='" . $nombre_columna . "' placeholder='" . $nombre_columna . "' value='" . htmlspecialchars($valor_actual, ENT_QUOTES) . "' step='0.01'>";
            break;

        case 'date':
            $html .= "<input type='date' name='" . $nombre_columna . "' value='" . htmlspecialchars($valor_actual, ENT_QUOTES) . "'>";
            break;

        case 'datetime':
        case 'timestamp':
            $valor = str_replace(" ", "T", $valor_actual);
            $html .= "<input type='datetime-local' name='" . $nombre_columna . "' value='" . htmlspecialchars($valor, ENT_QUOTES) . "'>";
            break;

        case 'time':
            $html .= "<input type='time' name='" . $nombre_columna . "' value='" . htmlspecialchars($valor_actual, ENT_QUOTES) . "'>";
            break;

        case 'enum':
        case 'set':
            $html .= "<select name='" . $nombre_columna . "'>";
            $html .= "<option value=''>-- seleccionar --</option>";
            if (preg_match_all("/'([^']*)'/", $meta_columna['COLUMN_TYPE'], $matches)) {
                foreach ($matches[1] as $opcion) {
                    $selected = ($valor_actual == $opcion) ? "selected" : "";
                    $html .= "<option value='" . htmlspecialchars($opcion, ENT_QUOTES) . "' " . $selected . ">" . $opcion . "</option>";
                }
            }
            $html .= "</select>";
            break;

        default:
            $html .= "<input type='text' name='" . $nombre_columna . "' placeholder='" . $nombre_columna . "' value='" . htmlspecialchars($valor_actual, ENT_QUOTES) . "'>";
            break;
    }

    return $html;
}

/**
 * Renderizar tabla HTML de resultados con botones de acción
 */
function render_tabla_html($rows, $tabla_nombre = '', $pk_columna = '', $conexion = null, $bd = DB_NAME) {
    if (!$rows || count($rows) === 0) {
        echo "<p class='no-data'>No hay datos disponibles</p>";
        return;
    }

    // Obtener claves foráneas si hay conexión y tabla
    $foreignKeys = [];
    if ($conexion && $tabla_nombre) {
        $foreignKeys = obtener_claves_foraneas($conexion, $tabla_nombre, $bd);
    }

    echo "<div class='table-wrapper'>";
    echo "<table class='data-table'>";
    $first = $rows[0];
    echo "<thead><tr>";
    foreach ($first as $k => $_) {
        echo "<th>" . htmlspecialchars($k) . "</th>";
    }
    if ($tabla_nombre && $pk_columna) {
        echo "<th class='actions-column'>Acciones</th>";
    }
    echo "</tr></thead>";
    echo "<tbody>";

    foreach ($rows as $fila) {
        echo "<tr>";
        foreach ($fila as $clave => $valor) {
            // Expandir claves foráneas si es FK y hay conexión
            if ($conexion && isset($foreignKeys[$clave]) && $valor !== null && $valor !== '') {
                $fk = $foreignKeys[$clave];
                $tabla_fk = $fk['tabla'];
                $columna_fk = $fk['columna'];

                $sql_fk = "SELECT * FROM " . $tabla_fk . " WHERE " . $columna_fk . " = '" . mysqli_real_escape_string($conexion, $valor) . "' LIMIT 1";
                $res_fk = mysqli_query($conexion, $sql_fk);
                
                if ($res_fk && $fila_fk = mysqli_fetch_assoc($res_fk)) {
                    $partes = [];
                    foreach ($fila_fk as $k2 => $v2) {
                        $partes[] = $v2;
                    }
                    $texto_celda = implode(" | ", $partes);
                    echo "<td>" . htmlspecialchars($texto_celda, ENT_QUOTES) . "</td>";
                } else {
                    echo "<td>" . htmlspecialchars($valor ?? '', ENT_QUOTES) . "</td>";
                }
            } else {
                echo "<td>" . htmlspecialchars($valor ?? '', ENT_QUOTES) . "</td>";
            }
        }
        // Agregar botones de acción
        if ($tabla_nombre && $pk_columna && isset($fila[$pk_columna])) {
            $id_valor = $fila[$pk_columna];
            echo "<td class='actions-column'>";
            echo "<a href='?tabla=" . urlencode($tabla_nombre) . "&accion=reporte&id=" . urlencode($id_valor) . "' class='btn-action btn-report' title='Reporte'>" . svg_icon('info', 18) . "</a>";
            echo "<a href='?tabla=" . urlencode($tabla_nombre) . "&accion=editar&id=" . urlencode($id_valor) . "' class='btn-action btn-edit' title='Editar'>" . svg_icon('edit', 18) . "</a>";
            echo "<a href='?tabla=" . urlencode($tabla_nombre) . "&accion=eliminar&id=" . urlencode($id_valor) . "' class='btn-action btn-delete' title='Eliminar' onclick='return confirm(\"¿Estás seguro de eliminar este registro?\");'>" . svg_icon('trash', 18) . "</a>";
            echo "</td>";
        }
        echo "</tr>";
    }

    echo "</tbody></table>";
    echo "</div>";
}

/**
 * Renderizar tarjetas HTML de resultados con botones de acción
 */
function render_tarjetas_html($rows, $tabla_nombre = '', $pk_columna = '', $conexion = null, $bd = DB_NAME) {
    if (!$rows || count($rows) === 0) {
        echo "<p class='no-data'>No hay datos disponibles</p>";
        return;
    }

    // Obtener claves foráneas si hay conexión y tabla
    $foreignKeys = [];
    if ($conexion && $tabla_nombre) {
        $foreignKeys = obtener_claves_foraneas($conexion, $tabla_nombre, $bd);
    }

    echo "<div class='cards-grid'>";

    foreach ($rows as $fila) {
        echo "<div class='data-card'>";
        echo "<div class='card-body'>";
        
        foreach ($fila as $clave => $valor) {
            echo "<div class='card-field'>";
            echo "<span class='field-label'>" . htmlspecialchars($clave) . ":</span>";
            echo "<span class='field-value'>";
            
            // Expandir claves foráneas si es FK y hay conexión
            if ($conexion && isset($foreignKeys[$clave]) && $valor !== null && $valor !== '') {
                $fk = $foreignKeys[$clave];
                $tabla_fk = $fk['tabla'];
                $columna_fk = $fk['columna'];

                $sql_fk = "SELECT * FROM " . $tabla_fk . " WHERE " . $columna_fk . " = '" . mysqli_real_escape_string($conexion, $valor) . "' LIMIT 1";
                $res_fk = mysqli_query($conexion, $sql_fk);
                
                if ($res_fk && $fila_fk = mysqli_fetch_assoc($res_fk)) {
                    $partes = [];
                    foreach ($fila_fk as $k2 => $v2) {
                        $partes[] = $v2;
                    }
                    $texto_celda = implode(" | ", $partes);
                    echo htmlspecialchars($texto_celda, ENT_QUOTES);
                } else {
                    echo htmlspecialchars($valor ?? '', ENT_QUOTES);
                }
            } else {
                echo htmlspecialchars($valor ?? '', ENT_QUOTES);
            }
            
            echo "</span>";
            echo "</div>";
        }
        
        echo "</div>";
        
        // Agregar botones de acción
        if ($tabla_nombre && $pk_columna && isset($fila[$pk_columna])) {
            $id_valor = $fila[$pk_columna];
            echo "<div class='card-actions'>";
            echo "<a href='?tabla=" . urlencode($tabla_nombre) . "&accion=reporte&id=" . urlencode($id_valor) . "' class='btn-action btn-report' title='Reporte'>" . svg_icon('info', 18) . " Reporte</a>";
            echo "<a href='?tabla=" . urlencode($tabla_nombre) . "&accion=editar&id=" . urlencode($id_valor) . "' class='btn-action btn-edit' title='Editar'>" . svg_icon('edit', 18) . " Editar</a>";
            echo "<a href='?tabla=" . urlencode($tabla_nombre) . "&accion=eliminar&id=" . urlencode($id_valor) . "' class='btn-action btn-delete' title='Eliminar' onclick='return confirm(\"¿Estás seguro de eliminar este registro?\");'>" . svg_icon('trash', 18) . " Eliminar</a>";
            echo "</div>";
        }
        
        echo "</div>";
    }

    echo "</div>";
}

/**
 * Renderizar gráfico de tipo donut
 */
function render_pie_chart($segmentos, $titulo = "Gráfico") {
    $total = 0;
    foreach ($segmentos as $s) {
        $total += $s['total'];
    }
    if ($total <= 0) {
        echo "<p class='no-data'>Sin datos para el gráfico</p>";
        return;
    }

    $acumulado = 0.0;

    echo "<div class='chart-container'>";
    echo "<h3>" . htmlspecialchars($titulo) . "</h3>";
    echo "<div class='chart-pie-wrapper'>";
    echo "<div class='chart-pie'>";
    echo "<svg viewBox='0 0 42 42' class='donut'>";
    echo "<circle class='donut-ring' cx='21' cy='21' r='15.915'></circle>";

    $index = 0;
    // Colores de la paleta personalizada que coinciden con el CSS
    $colores = ['#6f8f72', '#f2a65a', '#99af9a', '#f6be8c', '#c4cfc5', '#f6d7be', '#BFC6C4', '#d87a68'];
    
    foreach ($segmentos as $s) {
        $valor = $s['total'];
        $percent = ($valor / $total) * 100.0;
        $dasharray = $percent . " " . (100 - $percent);
        $dashoffset = 25 - $acumulado;
 
        echo "<circle class='donut-segment segment-" . $index . "' cx='21' cy='21' r='15.915' ";
        echo "stroke-dasharray='" . $dasharray . "' stroke-dashoffset='" . $dashoffset . "'></circle>";

        $acumulado += $percent;
        $index++;
    }

    echo "</svg>";
    echo "<div class='donut-center'>";
    echo "<span class='donut-total'>" . $total . "</span>";
    echo "<span class='donut-label'>Total</span>";
    echo "</div>";
    echo "</div>";

    echo "<ul class='chart-legend'>";
    $index = 0;
    foreach ($segmentos as $s) {
        $label = htmlspecialchars($s['label'], ENT_QUOTES);
        $valor = (int)$s['total'];
        $color = $colores[$index % count($colores)];
        echo "<li>";
        echo "<span class='legend-color' style='background-color: " . $color . "'></span>";
        echo "<span class='legend-label'>" . $label . "</span>";
        echo "<span class='legend-value'>" . $valor . "</span>";
        echo "</li>";
        $index++;
    }
    echo "</ul>";
    echo "</div>";
    echo "</div>";
}

// =============================================
// PROCESAMIENTO DE ACCIONES
// =============================================

if ($logged_in) {
    $tabla_actual = $_GET['tabla'] ?? null;
    $vista_actual = $_GET['vista'] ?? ($tabla_actual ? 'tabla' : 'dashboard');
    $accion = $_GET['accion'] ?? '';
    $id_editar = $_GET['id'] ?? '';
    $mensaje_sistema = '';

    // =============================================
    // PROCESAMIENTO DE ACCIONES CRUD
    // =============================================

    // INSERTAR nuevo registro
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['accion']) && $_POST['accion'] === 'insertar' && $tabla_actual) {
        $campos = [];
        $valores = [];
        
        $meta = obtener_meta_columnas($conexion, $tabla_actual, DB_NAME);
        $pk = obtener_pk_columna($conexion, $tabla_actual, DB_NAME);
        
        foreach ($_POST as $campo => $valor) {
            if ($campo !== 'accion' && $campo !== $pk && isset($meta[$campo])) {
                $campos[] = $campo;
                if ($valor === '') {
                    $valores[] = "NULL";
                } else {
                    $valores[] = "'" . mysqli_real_escape_string($conexion, $valor) . "'";
                }
            }
        }
        
        if (count($campos) > 0) {
            $sql_insert = "INSERT INTO " . $tabla_actual . " (" . implode(", ", $campos) . ") VALUES (" . implode(", ", $valores) . ")";
            
            // Ejecutar con manejo de errores
            $resultado = @mysqli_query($conexion, $sql_insert);
            
            if ($resultado) {
                $mensaje_sistema = "<div class='mensaje-exito'>" . svg_icon('check', 16) . " Registro insertado correctamente</div>";
                $accion = ''; // Limpiar acción
            } else {
                $error_num = mysqli_errno($conexion);
                $error_msg = mysqli_error($conexion);
                
                // Mensajes de error más amigables
                if ($error_num == 1062) { // Duplicate entry
                    // Extraer el nombre del campo del mensaje de error
                    if (preg_match("/for key '(.+?)'/", $error_msg, $matches)) {
                        $campo = $matches[1];
                        $mensaje_sistema = "<div class='mensaje-error'>" . svg_icon('x', 16) . " Ya existe un registro con ese valor en el campo '<strong>" . htmlspecialchars($campo) . "</strong>'. Por favor, usa un valor diferente.</div>";
                    } else {
                        $mensaje_sistema = "<div class='mensaje-error'>" . svg_icon('x', 16) . " Ya existe un registro con esos datos. Por favor, verifica los campos únicos.</div>";
                    }
                } elseif ($error_num == 1452) { // Foreign key constraint
                    $mensaje_sistema = "<div class='mensaje-error'>" . svg_icon('x', 16) . " El valor seleccionado no existe en la tabla relacionada. Por favor, selecciona un valor válido.</div>";
                } elseif ($error_num == 1048) { // Column cannot be null
                    $mensaje_sistema = "<div class='mensaje-error'>" . svg_icon('x', 16) . " Falta completar un campo obligatorio. Por favor, revisa el formulario.</div>";
                } else {
                    $mensaje_sistema = "<div class='mensaje-error'>" . svg_icon('x', 16) . " Error al insertar: " . htmlspecialchars($error_msg) . "</div>";
                }
            }
        }
    }

    // ACTUALIZAR registro existente
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['accion']) && $_POST['accion'] === 'actualizar' && $tabla_actual && isset($_POST['id'])) {
        $sets = [];
        
        $meta = obtener_meta_columnas($conexion, $tabla_actual, DB_NAME);
        $pk = obtener_pk_columna($conexion, $tabla_actual, DB_NAME);
        $id = mysqli_real_escape_string($conexion, $_POST['id']);
        
        foreach ($_POST as $campo => $valor) {
            if ($campo !== 'accion' && $campo !== 'id' && $campo !== $pk && isset($meta[$campo])) {
                if ($valor === '') {
                    $sets[] = $campo . " = NULL";
                } else {
                    $sets[] = $campo . " = '" . mysqli_real_escape_string($conexion, $valor) . "'";
                }
            }
        }
        
        if (count($sets) > 0) {
            $sql_update = "UPDATE " . $tabla_actual . " SET " . implode(", ", $sets) . " WHERE " . $pk . " = '" . $id . "'";
            
            // Ejecutar con manejo de errores
            $resultado = @mysqli_query($conexion, $sql_update);
            
            if ($resultado) {
                $mensaje_sistema = "<div class='mensaje-exito'>" . svg_icon('check', 16) . " Registro actualizado correctamente</div>";
                $accion = '';
                $id_editar = '';
            } else {
                $error_num = mysqli_errno($conexion);
                $error_msg = mysqli_error($conexion);
                
                // Mensajes de error más amigables
                if ($error_num == 1062) { // Duplicate entry
                    if (preg_match("/for key '(.+?)'/", $error_msg, $matches)) {
                        $campo = $matches[1];
                        $mensaje_sistema = "<div class='mensaje-error'>" . svg_icon('x', 16) . " Ya existe otro registro con ese valor en el campo '<strong>" . htmlspecialchars($campo) . "</strong>'. Por favor, usa un valor diferente.</div>";
                    } else {
                        $mensaje_sistema = "<div class='mensaje-error'>" . svg_icon('x', 16) . " Ya existe otro registro con esos datos. Por favor, verifica los campos únicos.</div>";
                    }
                } elseif ($error_num == 1452) { // Foreign key constraint
                    $mensaje_sistema = "<div class='mensaje-error'>" . svg_icon('x', 16) . " El valor seleccionado no existe en la tabla relacionada. Por favor, selecciona un valor válido.</div>";
                } elseif ($error_num == 1048) { // Column cannot be null
                    $mensaje_sistema = "<div class='mensaje-error'>" . svg_icon('x', 16) . " Falta completar un campo obligatorio. Por favor, revisa el formulario.</div>";
                } else {
                    $mensaje_sistema = "<div class='mensaje-error'>" . svg_icon('x', 16) . " Error al actualizar: " . htmlspecialchars($error_msg) . "</div>";
                }
            }
        }
    }

    // ELIMINAR registro
    if ($accion === 'eliminar' && $tabla_actual && $id_editar) {
        $pk = obtener_pk_columna($conexion, $tabla_actual, DB_NAME);
        $id = mysqli_real_escape_string($conexion, $id_editar);
        
        $sql_delete = "DELETE FROM " . $tabla_actual . " WHERE " . $pk . " = '" . $id . "'";
        
        // Ejecutar con manejo de errores
        $resultado = @mysqli_query($conexion, $sql_delete);
        
        if ($resultado) {
            $mensaje_sistema = "<div class='mensaje-exito'>" . svg_icon('check', 16) . " Registro eliminado correctamente</div>";
            $accion = '';
            $id_editar = '';
        } else {
            $error_num = mysqli_errno($conexion);
            $error_msg = mysqli_error($conexion);
            
            // Mensajes de error más amigables
            if ($error_num == 1451) { // Foreign key constraint on delete
                $mensaje_sistema = "<div class='mensaje-error'>" . svg_icon('x', 16) . " No se puede eliminar este registro porque está siendo usado en otras tablas. Primero elimina los registros relacionados.</div>";
            } else {
                $mensaje_sistema = "<div class='mensaje-error'>" . svg_icon('x', 16) . " Error al eliminar: " . htmlspecialchars($error_msg) . "</div>";
            }
        }
    }

    // Obtener todas las tablas
    $tablas = [];
    $sql_tablas = "SHOW TABLES FROM " . DB_NAME;
    $resultado_tablas = mysqli_query($conexion, $sql_tablas);
    if ($resultado_tablas) {
        while ($fila = mysqli_fetch_row($resultado_tablas)) {
            if (strpos($fila[0], 'vista_') !== 0) { // Excluir vistas
                $tablas[] = $fila[0];
            }
        }
    }
}

?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TotalKit ERP - Sistema de Gestión</title>
    <link rel="icon" type="image/png" href="https://static.agusmadev.es/logos/logo-blanco-verde-invertido.png" />
    <link rel="stylesheet" href="estilos.css">
</head>
<body>

<?php if (!$logged_in): ?>
    <!-- PANTALLA DE LOGIN -->
    <div class="login-container">
        <div class="login-box">
            <div class="login-header">
                <div class="logo-circle">
                    <svg viewBox="0 0 48 48" width="48" height="48">
                        <text x="50%" y="50%" font-size="20" font-weight="600" fill="white" text-anchor="middle" dominant-baseline="central">TK</text>
                    </svg>
                </div>
                <h1>TotalKit ERP</h1>
                <p>Sistema de Gestión Empresarial</p>
            </div>
            
            <?php if ($login_error): ?>
                <div class="error-message"><?= htmlspecialchars($login_error) ?></div>
            <?php endif; ?>
            
            <form method="POST" action="">
                <input type="hidden" name="accion" value="login">
                
                <div class="form-group">
                    <label>Usuario</label>
                    <input type="text" name="usuario" placeholder="Ingresa tu usuario" required autofocus>
                </div>
                
                <div class="form-group">
                    <label>Contraseña</label>
                    <input type="password" name="contrasena" placeholder="Ingresa tu contraseña" required>
                </div>
                
                <button type="submit" class="btn-primary">Iniciar Sesión</button>
                
                <div class="login-hint">
                    Usuario: <strong>admin</strong> / Contraseña: <strong>admin123</strong>
                </div>
            </form>
        </div>
    </div>

<?php else: ?>
    <!-- SISTEMA ERP -->
    <div class="erp-container">
        <!-- SIDEBAR -->
        <aside class="sidebar">
            <div class="sidebar-header">
                <div class="logo-circle">
                    <svg viewBox="0 0 48 48" width="48" height="48">
                        <text x="50%" y="50%" font-size="18" font-weight="600" fill="white" text-anchor="middle" dominant-baseline="central">TK</text>
                    </svg>
                </div>
                <h2>TotalKit</h2>
                <p class="user-info"><?= htmlspecialchars($_SESSION['usuario']) ?></p>
            </div>

            <nav class="sidebar-nav">
                <h3>Panel Principal</h3>
                <a href="?vista=dashboard" class="nav-item <?= $vista_actual === 'dashboard' ? 'active' : '' ?>">
                    Dashboard
                </a>
                <a href="?vista=buscar" class="nav-item <?= $vista_actual === 'buscar' ? 'active' : '' ?>">
                    Buscar Productos
                </a>

                <h3>Gestión de Datos</h3>
                <?php foreach ($tablas as $tabla): ?>
                    <div class="nav-item-wrapper">
                        <a href="?tabla=<?= $tabla ?>" class="nav-item <?= $tabla_actual === $tabla ? 'active' : '' ?>">
                            <?= ucfirst(str_replace('_', ' ', $tabla)) ?>
                        </a>
                        <?php if ($tabla_actual === $tabla): ?>
                            <a href="?tabla=<?= $tabla ?>&accion=crear" class="btn-crear-sidebar" title="Crear nuevo registro"><?= svg_icon('plus', 16) ?></a>
                        <?php endif; ?>
                    </div>
                <?php endforeach; ?>
            </nav>

            <div class="sidebar-footer">
                <a href="?logout" class="btn-logout">Cerrar Sesión</a>
                <div class="sidebar-copyright">
                    <p>TotalKit ERP v1.0</p>
                    <p>© 2026 TotalKit</p>
                </div>
            </div>
        </aside>

        <!-- CONTENIDO PRINCIPAL -->
        <main class="main-content">
            <header class="content-header">
                <h1>
                    <?php if ($tabla_actual && $vista_actual !== 'dashboard' && $vista_actual !== 'buscar'): ?>
                        Gestión de <?= ucfirst(str_replace('_', ' ', $tabla_actual)) ?>
                    <?php elseif ($vista_actual === 'buscar'): ?>
                        Buscador de Productos
                    <?php else: ?>
                        Dashboard
                    <?php endif; ?>
                </h1>
            </header>

            <div class="content-body">
                <?php echo $mensaje_sistema; ?>
                
                <?php if ($tabla_actual && $vista_actual !== 'dashboard' && $vista_actual !== 'buscar'): ?>
                    <!-- VISTA DE TABLA -->
                    <div class="table-section">
                        
                        <?php if ($accion === 'crear'): ?>
                            <!-- Formulario de CREACIÓN -->
                            <div class="insert-form">
                                <div class="form-header">
                                    <h2><?= svg_icon('plus', 20) ?> Crear Nuevo Registro</h2>
                                    <a href="?tabla=<?= $tabla_actual ?>" class="btn-cancelar"><?= svg_icon('x', 16) ?> Cancelar</a>
                                </div>
                                <form method="POST" action="?tabla=<?= $tabla_actual ?>">
                                    <input type="hidden" name="accion" value="insertar">
                                
                                <div class="form-grid">
                                    <?php
                                    $meta = obtener_meta_columnas($conexion, $tabla_actual, DB_NAME);
                                    $pk = obtener_pk_columna($conexion, $tabla_actual, DB_NAME);
                                    $fks = obtener_claves_foraneas($conexion, $tabla_actual, DB_NAME);
                                    
                                    foreach ($meta as $nombre_col => $info_col) {
                                        // Saltar PK auto_increment y timestamps automáticos
                                        if ($nombre_col === $pk && strpos($info_col['EXTRA'], 'auto_increment') !== false) {
                                            continue;
                                        }
                                        if (in_array($nombre_col, ['fecha_creacion', 'fecha_registro', 'fecha_pedido', 'fecha_resena'])) {
                                            continue;
                                        }
                                        
                                        echo "<div class='form-field'>";
                                        
                                        // Si es FK, mostrar select
                                        if (isset($fks[$nombre_col])) {
                                            $tabla_ref = $fks[$nombre_col]['tabla'];
                                            $columna_ref = $fks[$nombre_col]['columna'];
                                            
                                            echo "<label>" . htmlspecialchars($nombre_col) . "</label>";
                                            echo "<select name='" . $nombre_col . "'>";
                                            echo "<option value=''>-- seleccionar --</option>";
                                            
                                            $sql_fk = "SELECT * FROM " . $tabla_ref;
                                            $result_fk = mysqli_query($conexion, $sql_fk);
                                            if ($result_fk) {
                                                while ($row_fk = mysqli_fetch_assoc($result_fk)) {
                                                    $texto = implode(" - ", array_slice($row_fk, 0, 3));
                                                    echo "<option value='" . $row_fk[$columna_ref] . "'>" . htmlspecialchars($texto) . "</option>";
                                                }
                                            }
                                            echo "</select>";
                                        } else {
                                            echo render_input_para_columna($nombre_col, $info_col);
                                        }
                                        
                                        echo "</div>";
                                    }
                                    ?>
                                </div>
                                
                                    <button type="submit" class="btn-primary"><?= svg_icon('save', 18) ?> Guardar Registro</button>
                                </form>
                            </div>
                        
                        <?php elseif ($accion === 'editar' && $id_editar): ?>
                            <!-- Formulario de EDICIÓN -->
                            <?php
                            $meta = obtener_meta_columnas($conexion, $tabla_actual, DB_NAME);
                            $pk = obtener_pk_columna($conexion, $tabla_actual, DB_NAME);
                            $fks = obtener_claves_foraneas($conexion, $tabla_actual, DB_NAME);
                            
                            // Obtener datos del registro
                            $sql_edit = "SELECT * FROM " . $tabla_actual . " WHERE " . $pk . " = '" . mysqli_real_escape_string($conexion, $id_editar) . "' LIMIT 1";
                            $result_edit = mysqli_query($conexion, $sql_edit);
                            $registro = mysqli_fetch_assoc($result_edit);
                            
                            if ($registro):
                            ?>
                            <div class="insert-form">
                                <div class="form-header">
                                    <h2><?= svg_icon('edit', 20) ?> Editar Registro</h2>
                                    <a href="?tabla=<?= $tabla_actual ?>" class="btn-cancelar"><?= svg_icon('x', 16) ?> Cancelar</a>
                                </div>
                                <form method="POST" action="?tabla=<?= $tabla_actual ?>">
                                    <input type="hidden" name="accion" value="actualizar">
                                    <input type="hidden" name="id" value="<?= htmlspecialchars($id_editar) ?>">
                                    
                                    <div class="form-grid">
                                        <?php
                                        foreach ($meta as $nombre_col => $info_col) {
                                            // Mostrar PK como solo lectura
                                            if ($nombre_col === $pk) {
                                                echo "<div class='form-field'>";
                                                echo "<label>" . htmlspecialchars($nombre_col) . " (ID)</label>";
                                                echo "<input type='text' value='" . htmlspecialchars($registro[$nombre_col]) . "' disabled style='background: #e8e2d8;'>";
                                                echo "</div>";
                                                continue;
                                            }
                                            
                                            // Saltar timestamps automáticos
                                            if (in_array($nombre_col, ['fecha_creacion', 'fecha_registro', 'fecha_pedido', 'fecha_resena'])) {
                                                continue;
                                            }
                                            
                                            echo "<div class='form-field'>";
                                            
                                            // Si es FK, mostrar select
                                            if (isset($fks[$nombre_col])) {
                                                $tabla_ref = $fks[$nombre_col]['tabla'];
                                                $columna_ref = $fks[$nombre_col]['columna'];
                                                $valor_actual = $registro[$nombre_col] ?? '';
                                                
                                                echo "<label>" . htmlspecialchars($nombre_col) . "</label>";
                                                echo "<select name='" . $nombre_col . "'>";
                                                echo "<option value=''>-- seleccionar --</option>";
                                                
                                                $sql_fk = "SELECT * FROM " . $tabla_ref;
                                                $result_fk = mysqli_query($conexion, $sql_fk);
                                                if ($result_fk) {
                                                    while ($row_fk = mysqli_fetch_assoc($result_fk)) {
                                                        $texto = implode(" - ", array_slice($row_fk, 0, 3));
                                                        $selected = ($row_fk[$columna_ref] == $valor_actual) ? 'selected' : '';
                                                        echo "<option value='" . htmlspecialchars($row_fk[$columna_ref]) . "' " . $selected . ">" . htmlspecialchars($texto) . "</option>";
                                                    }
                                                }
                                                echo "</select>";
                                            } else {
                                                echo render_input_para_columna($nombre_col, $info_col, $registro[$nombre_col] ?? '');
                                            }
                                            
                                            echo "</div>";
                                        }
                                        ?>
                                    </div>
                                    
                                    <button type="submit" class="btn-primary"><?= svg_icon('save', 18) ?> Guardar Registro</button>
                                </form>
                            </div>
                            <?php else: ?>
                                <p class='no-data'><?= svg_icon('x', 16) ?> Registro no encontrado</p>
                            <?php endif; ?>
                        
                        <?php elseif ($accion === 'reporte' && $id_editar): ?>
                            <!-- REPORTE DE RELACIONES -->
                            <?php
                            $pk = obtener_pk_columna($conexion, $tabla_actual, DB_NAME);
                            
                            // Obtener datos del registro
                            $sql_registro = "SELECT * FROM " . $tabla_actual . " WHERE " . $pk . " = '" . mysqli_real_escape_string($conexion, $id_editar) . "' LIMIT 1";
                            $result_registro = mysqli_query($conexion, $sql_registro);
                            $registro = mysqli_fetch_assoc($result_registro);
                            
                            if ($registro):
                                $fks_salientes = obtener_claves_foraneas($conexion, $tabla_actual, DB_NAME);
                                $fks_entrantes = obtener_claves_foraneas_entrantes($conexion, $tabla_actual, DB_NAME);
                            ?>
                            <div class="reporte-container">
                                <div class="form-header">
                                    <h2><?= svg_icon('info', 20) ?> Reporte de Relaciones</h2>
                                    <a href="?tabla=<?= $tabla_actual ?>" class="btn-cancelar"><?= svg_icon('x', 16) ?> Volver</a>
                                </div>
                                
                                <!-- Sección 1: Registro Principal -->
                                <div class="reporte-seccion">
                                    <h3><?= svg_icon('file-text', 18) ?> Registro Principal</h3>
                                    <?php render_tabla_html([$registro], $tabla_actual, '', $conexion, DB_NAME); ?>
                                </div>
                                
                                <!-- Sección 2: FK Salientes (este registro apunta a...) -->
                                <?php if (count($fks_salientes) > 0): ?>
                                <div class="reporte-seccion">
                                    <h3><?= svg_icon('box', 18) ?> Datos Referenciados por este Registro (FK Salientes)</h3>
                                    <?php foreach ($fks_salientes as $columna_fk => $info_fk):
                                        $valor_fk = $registro[$columna_fk];
                                        if ($valor_fk !== null && $valor_fk !== ''):
                                            $tabla_ref = $info_fk['tabla'];
                                            $columna_ref = $info_fk['columna'];
                                            
                                            $sql_ref = "SELECT * FROM " . $tabla_ref . " WHERE " . $columna_ref . " = '" . mysqli_real_escape_string($conexion, $valor_fk) . "' LIMIT 1";
                                            $result_ref = mysqli_query($conexion, $sql_ref);
                                            
                                            if ($result_ref && $fila_ref = mysqli_fetch_assoc($result_ref)):
                                    ?>
                                        <div class="reporte-item">
                                            <h4><?= htmlspecialchars($columna_fk) ?> → <?= htmlspecialchars($tabla_ref) ?></h4>
                                            <?php render_tabla_html([$fila_ref], $tabla_ref, '', $conexion, DB_NAME); ?>
                                        </div>
                                    <?php 
                                            endif;
                                        endif;
                                    endforeach; ?>
                                </div>
                                <?php endif; ?>
                                
                                <!-- Sección 3: FK Entrantes (otros registros apuntan a este) -->
                                <?php if (count($fks_entrantes) > 0): ?>
                                <div class="reporte-seccion">
                                    <h3><?= svg_icon('user', 18) ?> Datos Relacionados que Apuntan a Este Registro (FK Entrantes)</h3>
                                    <?php foreach ($fks_entrantes as $info_entrante):
                                        $tabla_origen = $info_entrante['tabla'];
                                        $columna_origen = $info_entrante['columna'];
                                        $columna_ref = $info_entrante['columna_referenciada'];
                                        $valor_pk = $registro[$pk];
                                        
                                        $sql_entrantes = "SELECT * FROM " . $tabla_origen . " WHERE " . $columna_origen . " = '" . mysqli_real_escape_string($conexion, $valor_pk) . "'";
                                        $result_entrantes = mysqli_query($conexion, $sql_entrantes);
                                        
                                        if ($result_entrantes && mysqli_num_rows($result_entrantes) > 0):
                                            $datos_entrantes = [];
                                            $num_registros = mysqli_num_rows($result_entrantes);
                                            while ($row = mysqli_fetch_assoc($result_entrantes)) {
                                                $datos_entrantes[] = $row;
                                            }
                                    ?>
                                        <div class="reporte-item">
                                            <h4><?= htmlspecialchars($tabla_origen) ?> (<?= $num_registros ?> registros)</h4>
                                            <?php render_tabla_html($datos_entrantes, $tabla_origen, '', $conexion, DB_NAME); ?>
                                        </div>
                                    <?php 
                                        endif;
                                    endforeach; ?>
                                </div>
                                <?php endif; ?>
                            </div>
                            <?php else: ?>
                                <p class='no-data'><?= svg_icon('x', 16) ?> Registro no encontrado</p>
                            <?php endif; ?>
                        
                        <?php else: ?>
                            <!-- Tabla de datos -->
                            <?php
                            $vista_datos = isset($_GET['vista']) ? $_GET['vista'] : 'tabla';
                            ?>
                            <div class="data-view">
                                <div class="data-header">
                                    <h2><?= svg_icon('file-text', 20) ?> Listado de Registros</h2>
                                    <div class="vista-botones">
                                        <a href="?tabla=<?= $tabla_actual ?>&vista=tabla" class="btn-vista <?= $vista_datos === 'tabla' ? 'active' : '' ?>" title="Vista de Tabla">
                                            <?= svg_icon('list', 18) ?> Tabla
                                        </a>
                                        <a href="?tabla=<?= $tabla_actual ?>&vista=tarjetas" class="btn-vista <?= $vista_datos === 'tarjetas' ? 'active' : '' ?>" title="Vista de Tarjetas">
                                            <?= svg_icon('grid', 18) ?> Tarjetas
                                        </a>
                                    </div>
                                </div>
                                <?php
                                $pk = obtener_pk_columna($conexion, $tabla_actual, DB_NAME);
                                $sql = "SELECT * FROM " . $tabla_actual . " LIMIT 100";
                                $result = mysqli_query($conexion, $sql);
                                if ($result) {
                                    $datos = [];
                                    while ($row = mysqli_fetch_assoc($result)) {
                                        $datos[] = $row;
                                    }
                                    if ($vista_datos === 'tarjetas') {
                                        render_tarjetas_html($datos, $tabla_actual, $pk, $conexion, DB_NAME);
                                    } else {
                                        render_tabla_html($datos, $tabla_actual, $pk, $conexion, DB_NAME);
                                    }
                                } else {
                                    echo "<p class='no-data'>" . svg_icon('x', 16) . " Error al cargar datos: " . mysqli_error($conexion) . "</p>";
                                }
                                ?>
                            </div>
                        <?php endif; ?>
                    </div>

                <?php elseif ($vista_actual === 'buscar'): ?>
                    <!-- BUSCADOR DE PRODUCTOS -->
                    <div class="search-container">
                        <div class="search-header">
                            <h2>Búsqueda Avanzada de Productos</h2>
                            <div class="search-bar">
                                <div class="search-input-wrapper">
                                    <input type="text" id="busqueda-texto" placeholder="Buscar por nombre, equipo, marca, jugador...">
                                </div>
                                <button class="btn-limpiar" id="btn-limpiar-filtros">Limpiar Filtros</button>
                            </div>
                        </div>

                        <div class="filtros-container">
                            <div class="filtros-toggle" onclick="this.nextElementSibling.classList.toggle('hidden'); this.querySelector('.toggle-icon').classList.toggle('rotated')">
                                <h3>Filtros Avanzados</h3>
                                <span class="toggle-icon">
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                        <polyline points="6 9 12 15 18 9"></polyline>
                                    </svg>
                                </span>
                            </div>
                            
                            <div class="filtros-content">
                                <div class="filtros-grid">
                                    <div class="filtro-grupo">
                                        <label>Equipo</label>
                                        <select id="filtro-equipo">
                                            <option value="">Todos los equipos</option>
                                        </select>
                                    </div>

                                    <div class="filtro-grupo">
                                        <label>Liga</label>
                                        <select id="filtro-liga">
                                            <option value="">Todas las ligas</option>
                                        </select>
                                    </div>

                                    <div class="filtro-grupo">
                                        <label>Marca</label>
                                        <select id="filtro-marca">
                                            <option value="">Todas las marcas</option>
                                        </select>
                                    </div>

                                    <div class="filtro-grupo">
                                        <label>Temporada</label>
                                        <select id="filtro-temporada">
                                            <option value="">Todas las temporadas</option>
                                        </select>
                                    </div>

                                    <div class="filtro-grupo">
                                        <label>Tipo de Camiseta</label>
                                        <select id="filtro-tipo">
                                            <option value="">Todos los tipos</option>
                                        </select>
                                    </div>

                                    <div class="filtro-grupo">
                                        <label>Talla</label>
                                        <select id="filtro-talla">
                                            <option value="">Todas las tallas</option>
                                        </select>
                                    </div>
                                </div>

                                <div class="filtros-grid" style="margin-top: 1rem;">
                                    <div class="filtro-grupo">
                                        <label>Rango de Precio</label>
                                        <div class="precio-range">
                                            <input type="number" id="filtro-precio-min" placeholder="Mínimo" step="0.01" min="0">
                                            <input type="number" id="filtro-precio-max" placeholder="Máximo" step="0.01" min="0">
                                        </div>
                                    </div>

                                    <div class="filtro-grupo">
                                        <label>Tipo de Equipo</label>
                                        <div class="radio-group">
                                            <div class="radio-item">
                                                <input type="radio" id="radio-todos-equipos" name="tipo-equipo" value="" checked>
                                                <label for="radio-todos-equipos">Todos</label>
                                            </div>
                                            <div class="radio-item">
                                                <input type="radio" id="radio-clubes" name="tipo-equipo" value="0">
                                                <label for="radio-clubes">Clubes</label>
                                            </div>
                                            <div class="radio-item">
                                                <input type="radio" id="radio-selecciones" name="tipo-equipo" value="1">
                                                <label for="radio-selecciones">Selecciones</label>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="filtros-checks">
                                    <div class="check-item">
                                        <input type="checkbox" id="filtro-solo-stock">
                                        <label for="filtro-solo-stock">Solo con stock disponible</label>
                                    </div>
                                    <div class="check-item">
                                        <input type="checkbox" id="filtro-destacados">
                                        <label for="filtro-destacados">Solo productos destacados</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Controles de vista y ordenamiento -->
                    <div class="search-container">
                        <div class="search-controls">
                            <div class="view-controls">
                                <button class="btn-view active" id="btn-vista-grid" title="Vista en cuadrícula">
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
                                </button>
                                <button class="btn-view" id="btn-vista-lista" title="Vista en lista">
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>
                                </button>
                            </div>

                            <div class="sort-controls">
                                <label>Ordenar por:</label>
                                <select id="select-orden">
                                    <option value="p.fecha_creacion|DESC">Más recientes</option>
                                    <option value="p.fecha_creacion|ASC">Más antiguos</option>
                                    <option value="p.nombre_producto|ASC">Nombre (A-Z)</option>
                                    <option value="p.nombre_producto|DESC">Nombre (Z-A)</option>
                                    <option value="e.nombre_equipo|ASC">Equipo (A-Z)</option>
                                    <option value="p.precio|ASC">Precio (menor a mayor)</option>
                                    <option value="p.precio|DESC">Precio (mayor a menor)</option>
                                    <option value="p.stock|DESC">Mayor stock</option>
                                </select>
                            </div>
                        </div>

                        <div class="estadisticas-busqueda" id="estadisticas-busqueda">
                            <!-- Las estadísticas se cargarán dinámicamente -->
                        </div>
                    </div>

                    <!-- Resultados de búsqueda -->
                    <div class="search-container">
                        <div class="resultados-container" id="resultados-busqueda">
                            <!-- Los resultados se cargarán dinámicamente -->
                        </div>
                    </div>

                    <!-- Script del buscador -->
                    <script src="buscador.js"></script>

                <?php else: ?>
                    <!-- DASHBOARD -->
                    <div class="dashboard-grid">
                        <!-- Estadísticas generales -->
                        <div class="stat-card">
                            <div class="stat-icon"><?= svg_icon('box') ?></div>
                            <div class="stat-info">
                                <h3>Total Productos</h3>
                                <?php
                                $result = mysqli_query($conexion, "SELECT COUNT(*) as total FROM productos");
                                $total = mysqli_fetch_assoc($result)['total'];
                                ?>
                                <p class="stat-number"><?= $total ?></p>
                            </div>
                        </div>

                        <div class="stat-card">
                            <div class="stat-icon"><?= svg_icon('user') ?></div>
                            <div class="stat-info">
                                <h3>Total Clientes</h3>
                                <?php
                                $result = mysqli_query($conexion, "SELECT COUNT(*) as total FROM clientes");
                                $total = mysqli_fetch_assoc($result)['total'];
                                ?>
                                <p class="stat-number"><?= $total ?></p>
                            </div>
                        </div>

                        <div class="stat-card">
                            <div class="stat-icon"><?= svg_icon('chart') ?></div>
                            <div class="stat-info">
                                <h3>Total Pedidos</h3>
                                <?php
                                $result = mysqli_query($conexion, "SELECT COUNT(*) as total FROM pedidos");
                                $total = mysqli_fetch_assoc($result)['total'];
                                ?>
                                <p class="stat-number"><?= $total ?></p>
                            </div>
                        </div>

                        <div class="stat-card">
                            <div class="stat-icon"><?= svg_icon('dollar') ?></div>
                            <div class="stat-info">
                                <h3>Ingresos Totales</h3>
                                <?php
                                $result = mysqli_query($conexion, "SELECT SUM(total) as total FROM pedidos");
                                $total = mysqli_fetch_assoc($result)['total'] ?? 0;
                                ?>
                                <p class="stat-number"><?= number_format($total, 2) ?>€</p>
                            </div>
                        </div>
                    </div>

                    <!-- Gráficos -->
                    <div class="charts-grid">
                        <?php
                        // Camisetas por equipo
                        $sql = "SELECT e.nombre_equipo as label, COUNT(p.id_producto) as total 
                                FROM equipos e 
                                LEFT JOIN productos p ON e.id_equipo = p.id_equipo 
                                GROUP BY e.id_equipo
                                ORDER BY total DESC
                                LIMIT 8";
                        $result = mysqli_query($conexion, $sql);
                        $datos = [];
                        while ($row = mysqli_fetch_assoc($result)) {
                            if ($row['total'] > 0) {
                                $datos[] = $row;
                            }
                        }
                        render_pie_chart($datos, "Productos por Equipo");
                        ?>

                        <?php
                        // Pedidos por estado
                        $sql = "SELECT e.nombre_estado as label, COUNT(p.id_pedido) as total 
                                FROM estados_pedido e 
                                LEFT JOIN pedidos p ON e.id_estado = p.id_estado 
                                GROUP BY e.id_estado";
                        $result = mysqli_query($conexion, $sql);
                        $datos = [];
                        while ($row = mysqli_fetch_assoc($result)) {
                            if ($row['total'] > 0) {
                                $datos[] = $row;
                            }
                        }
                        render_pie_chart($datos, "Pedidos por Estado");
                        ?>
                    </div>

                    <!-- Productos destacados -->
                    <div class="section">
                        <h2>Productos Destacados</h2>
                        <?php
                        // Verificar si la vista existe
                        $check_vista = mysqli_query($conexion, "SHOW TABLES LIKE 'vista_productos_completa'");
                        if (mysqli_num_rows($check_vista) > 0) {
                            $sql = "SELECT * FROM vista_productos_completa WHERE destacado = 1 LIMIT 10";
                        } else {
                            // Fallback si la vista no existe
                            $sql = "SELECT p.*, e.nombre_equipo, m.nombre_marca 
                                    FROM productos p 
                                    INNER JOIN equipos e ON p.id_equipo = e.id_equipo 
                                    INNER JOIN marcas m ON p.id_marca = m.id_marca 
                                    WHERE p.destacado = 1 
                                    LIMIT 10";
                        }
                        $result = mysqli_query($conexion, $sql);
                        if ($result) {
                            $productos = [];
                            while ($row = mysqli_fetch_assoc($result)) {
                                $productos[] = $row;
                            }
                            render_tabla_html($productos);
                        } else {
                            echo "<p class='no-data'>No hay productos destacados</p>";
                        }
                        ?>
                    </div>
                <?php endif; ?>
            </div>
        </main>
    </div>
<?php endif; ?>

</body>
</html>

<?php
if ($logged_in && isset($conexion)) {
    cerrar_conexion($conexion);
}
?>
