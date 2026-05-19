<?php
session_start();

// =============================================
// CONFIGURACIÓN
// =============================================
$db_host = "localhost";
$db_name = "tienda_camisetas";
$db_user = "totalkit";
$db_pass = "totalkit";

// Credenciales de login
$usuario_valido = "admin";
$contrasena_valida = "admin123";

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

    if ($user === $usuario_valido && $pass === $contrasena_valida) {
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
    $conexion = mysqli_connect($db_host, $db_user, $db_pass, $db_name);
    if (!$conexion) {
        die("Error de conexión: " . mysqli_connect_error());
    }
    mysqli_set_charset($conexion, "utf8");
}

// =============================================
// FUNCIONES AUXILIARES
// =============================================

/**
 * Obtener claves foráneas de una tabla
 */
function obtener_claves_foraneas($conexion, $tabla, $bd) {
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
 * Obtener metadatos de columnas de una tabla
 */
function obtener_meta_columnas($conexion, $tabla, $bd) {
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
function obtener_pk_columna($conexion, $tabla, $bd) {
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
 * Renderizar tabla HTML de resultados
 */
function render_tabla_html($rows) {
    if (!$rows || count($rows) === 0) {
        echo "<p class='no-data'>📭 No hay datos disponibles</p>";
        return;
    }

    echo "<div class='table-wrapper'>";
    echo "<table class='data-table'>";
    $first = $rows[0];
    echo "<thead><tr>";
    foreach ($first as $k => $_) {
        echo "<th>" . htmlspecialchars($k) . "</th>";
    }
    echo "</tr></thead>";
    echo "<tbody>";

    foreach ($rows as $fila) {
        echo "<tr>";
        foreach ($fila as $valor) {
            echo "<td>" . htmlspecialchars($valor ?? '', ENT_QUOTES) . "</td>";
        }
        echo "</tr>";
    }

    echo "</tbody></table>";
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
        echo "<p class='no-data'>📊 Sin datos para el gráfico</p>";
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
    $colores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2'];
    
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
    $vista_actual = $_GET['vista'] ?? 'dashboard';

    // Insertar nuevo registro
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['accion']) && $_POST['accion'] === 'insertar' && $tabla_actual) {
        $campos = [];
        $valores = [];
        
        $meta = obtener_meta_columnas($conexion, $tabla_actual, $db_name);
        $pk = obtener_pk_columna($conexion, $tabla_actual, $db_name);
        
        foreach ($_POST as $campo => $valor) {
            if ($campo !== 'accion' && $campo !== $pk && isset($meta[$campo])) {
                $campos[] = $campo;
                $valores[] = "'" . mysqli_real_escape_string($conexion, $valor) . "'";
            }
        }
        
        if (count($campos) > 0) {
            $sql_insert = "INSERT INTO " . $tabla_actual . " (" . implode(", ", $campos) . ") VALUES (" . implode(", ", $valores) . ")";
            if (mysqli_query($conexion, $sql_insert)) {
                echo "<script>alert('✅ Registro insertado correctamente');</script>";
            } else {
                echo "<script>alert('❌ Error al insertar: " . mysqli_error($conexion) . "');</script>";
            }
        }
    }

    // Obtener todas las tablas
    $tablas = [];
    $sql_tablas = "SHOW TABLES FROM " . $db_name;
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
    <title>⚽ TotalKit ERP - Sistema de Gestión</title>
    <link rel="stylesheet" href="estilos.css">
</head>
<body>

<?php if (!$logged_in): ?>
    <!-- PANTALLA DE LOGIN -->
    <div class="login-container">
        <div class="login-box">
            <div class="login-header">
                <div class="logo-circle">⚽</div>
                <h1>TotalKit ERP</h1>
                <p>Sistema de Gestión de Camisetas de Fútbol</p>
            </div>
            
            <?php if ($login_error): ?>
                <div class="error-message">⚠️ <?= htmlspecialchars($login_error) ?></div>
            <?php endif; ?>
            
            <form method="POST" action="">
                <input type="hidden" name="accion" value="login">
                
                <div class="form-group">
                    <label>👤 Usuario</label>
                    <input type="text" name="usuario" placeholder="Ingresa tu usuario" required autofocus>
                </div>
                
                <div class="form-group">
                    <label>🔒 Contraseña</label>
                    <input type="password" name="contrasena" placeholder="Ingresa tu contraseña" required>
                </div>
                
                <button type="submit" class="btn-primary">Iniciar Sesión</button>
                
                <div class="login-hint">
                    💡 Usuario: <strong>admin</strong> / Contraseña: <strong>admin123</strong>
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
                <div class="logo-circle">⚽</div>
                <h2>TotalKit</h2>
                <p class="user-info">👤 <?= htmlspecialchars($_SESSION['usuario']) ?></p>
            </div>

            <nav class="sidebar-nav">
                <h3>📊 Panel Principal</h3>
                <a href="?vista=dashboard" class="nav-item <?= $vista_actual === 'dashboard' ? 'active' : '' ?>">
                    🏠 Dashboard
                </a>

                <h3>📋 Gestión de Tablas</h3>
                <?php foreach ($tablas as $tabla): ?>
                    <a href="?tabla=<?= $tabla ?>" class="nav-item <?= $tabla_actual === $tabla ? 'active' : '' ?>">
                        📄 <?= ucfirst(str_replace('_', ' ', $tabla)) ?>
                    </a>
                <?php endforeach; ?>
            </nav>

            <div class="sidebar-footer">
                <a href="?logout" class="btn-logout">🚪 Cerrar Sesión</a>
            </div>
        </aside>

        <!-- CONTENIDO PRINCIPAL -->
        <main class="main-content">
            <header class="content-header">
                <h1>
                    <?php if ($vista_actual === 'dashboard'): ?>
                        📊 Dashboard Principal
                    <?php elseif ($tabla_actual): ?>
                        📄 Gestión de <?= ucfirst(str_replace('_', ' ', $tabla_actual)) ?>
                    <?php endif; ?>
                </h1>
            </header>

            <div class="content-body">
                <?php if ($vista_actual === 'dashboard'): ?>
                    <!-- DASHBOARD -->
                    <div class="dashboard-grid">
                        <!-- Estadísticas generales -->
                        <div class="stat-card">
                            <div class="stat-icon">�</div>
                            <div class="stat-info">
                                <h3>Total Camisetas</h3>
                                <?php
                                $result = mysqli_query($conexion, "SELECT COUNT(*) as total FROM productos");
                                $total = mysqli_fetch_assoc($result)['total'];
                                ?>
                                <p class="stat-number"><?= $total ?></p>
                            </div>
                        </div>

                        <div class="stat-card">
                            <div class="stat-icon">👥</div>
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
                            <div class="stat-icon">👕</div>
                            <div class="stat-info">
                                <h3>Total Camisetas</h3>
                                <?php
                                $result = mysqli_query($conexion, "SELECT COUNT(*) as total FROM pedidos");
                                $total = mysqli_fetch_assoc($result)['total'];
                                ?>
                                <p class="stat-number"><?= $total ?></p>
                            </div>
                        </div>

                        <div class="stat-card">
                            <div class="stat-icon">💰</div>
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
                        render_pie_chart($datos, "👕 Camisetas por Equipo");
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
                        render_pie_chart($datos, "🛒 Pedidos por Estado");
                        ?>
                    </div>

                    <!-- Productos destacados -->
                    <div class="section">
                        <h2>⭐ Camisetas Destacadas</h2>
                        <?php
                        $sql = "SELECT * FROM vista_productos_completa WHERE destacado = 1 LIMIT 10";
                        $result = mysqli_query($conexion, $sql);
                        $productos = [];
                        while ($row = mysqli_fetch_assoc($result)) {
                            $productos[] = $row;
                        }
                        render_tabla_html($productos);
                        ?>
                    </div>

                <?php elseif ($tabla_actual): ?>
                    <!-- VISTA DE TABLA -->
                    <div class="table-section">
                        <!-- Formulario de inserción -->
                        <div class="insert-form">
                            <h2>➕ Insertar Nuevo Registro</h2>
                            <form method="POST" action="?tabla=<?= $tabla_actual ?>">
                                <input type="hidden" name="accion" value="insertar">
                                
                                <div class="form-grid">
                                    <?php
                                    $meta = obtener_meta_columnas($conexion, $tabla_actual, $db_name);
                                    $pk = obtener_pk_columna($conexion, $tabla_actual, $db_name);
                                    $fks = obtener_claves_foraneas($conexion, $tabla_actual, $db_name);
                                    
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
                                
                                <button type="submit" class="btn-primary">💾 Guardar Registro</button>
                            </form>
                        </div>

                        <!-- Tabla de datos -->
                        <div class="data-view">
                            <h2>📋 Listado de Registros</h2>
                            <?php
                            $sql = "SELECT * FROM " . $tabla_actual . " LIMIT 100";
                            $result = mysqli_query($conexion, $sql);
                            $datos = [];
                            while ($row = mysqli_fetch_assoc($result)) {
                                $datos[] = $row;
                            }
                            render_tabla_html($datos);
                            ?>
                        </div>
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
    mysqli_close($conexion);
}
?>
