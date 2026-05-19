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
 * Renderizar tabla HTML de resultados
 */
function render_tabla_html($rows) {
    if (!$rows || count($rows) === 0) {
        echo "<p class='no-data'>No hay datos disponibles</p>";
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

    // Insertar nuevo registro
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['accion']) && $_POST['accion'] === 'insertar' && $tabla_actual) {
        $campos = [];
        $valores = [];
        
        $meta = obtener_meta_columnas($conexion, $tabla_actual, DB_NAME);
        $pk = obtener_pk_columna($conexion, $tabla_actual, DB_NAME);
        
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
    <link rel="icon" type="image/svg+xml" href="https://static.agusmadev.es/logos/logo-verde-blanco-invertido.svg" />
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
                    <a href="?tabla=<?= $tabla ?>" class="nav-item <?= $tabla_actual === $tabla ? 'active' : '' ?>">
                        <?= ucfirst(str_replace('_', ' ', $tabla)) ?>
                    </a>
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
                <?php if ($tabla_actual && $vista_actual !== 'dashboard' && $vista_actual !== 'buscar'): ?>
                    <!-- VISTA DE TABLA -->
                    <div class="table-section">
                        <!-- Formulario de inserción -->
                        <div class="insert-form">
                            <h2>Insertar Nuevo Registro</h2>
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
                                
                                <button type="submit" class="btn-primary">💾 Guardar Registro</button>
                            </form>
                        </div>

                        <!-- Tabla de datos -->
                        <div class="data-view">
                            <h2>📋 Listado de Registros</h2>
                            <?php
                            $sql = "SELECT * FROM " . $tabla_actual . " LIMIT 100";
                            $result = mysqli_query($conexion, $sql);
                            if ($result) {
                                $datos = [];
                                while ($row = mysqli_fetch_assoc($result)) {
                                    $datos[] = $row;
                                }
                                render_tabla_html($datos);
                            } else {
                                echo "<p class='no-data'>❌ Error al cargar datos: " . mysqli_error($conexion) . "</p>";
                            }
                            ?>
                        </div>
                    </div>

                <?php elseif ($vista_actual === 'buscar'): ?>
                    <!-- BUSCADOR DE PRODUCTOS -->
                    <div class="search-container">
                        <div class="search-header">
                            <h2>🔍 Búsqueda Avanzada de Productos</h2>
                            <div class="search-bar">
                                <div class="search-input-wrapper">
                                    <input type="text" id="busqueda-texto" placeholder="Buscar por nombre, equipo, marca, jugador...">
                                </div>
                                <button class="btn-limpiar" id="btn-limpiar-filtros">🧹 Limpiar Filtros</button>
                            </div>
                        </div>

                        <div class="filtros-container">
                            <div class="filtros-toggle" onclick="this.nextElementSibling.classList.toggle('hidden')">
                                <h3>⚙️ Filtros Avanzados</h3>
                                <span>▼</span>
                            </div>
                            
                            <div class="filtros-content">
                                <div class="filtros-grid">
                                    <div class="filtro-grupo">
                                        <label>⚽ Equipo</label>
                                        <select id="filtro-equipo">
                                            <option value="">Todos los equipos</option>
                                        </select>
                                    </div>

                                    <div class="filtro-grupo">
                                        <label>🏆 Liga</label>
                                        <select id="filtro-liga">
                                            <option value="">Todas las ligas</option>
                                        </select>
                                    </div>

                                    <div class="filtro-grupo">
                                        <label>🏷️ Marca</label>
                                        <select id="filtro-marca">
                                            <option value="">Todas las marcas</option>
                                        </select>
                                    </div>

                                    <div class="filtro-grupo">
                                        <label>📅 Temporada</label>
                                        <select id="filtro-temporada">
                                            <option value="">Todas las temporadas</option>
                                        </select>
                                    </div>

                                    <div class="filtro-grupo">
                                        <label>👕 Tipo de Camiseta</label>
                                        <select id="filtro-tipo">
                                            <option value="">Todos los tipos</option>
                                        </select>
                                    </div>

                                    <div class="filtro-grupo">
                                        <label>📏 Talla</label>
                                        <select id="filtro-talla">
                                            <option value="">Todas las tallas</option>
                                        </select>
                                    </div>
                                </div>

                                <div class="filtros-grid" style="margin-top: 1rem;">
                                    <div class="filtro-grupo">
                                        <label>💰 Rango de Precio</label>
                                        <div class="precio-range">
                                            <input type="number" id="filtro-precio-min" placeholder="Mínimo" step="0.01" min="0">
                                            <input type="number" id="filtro-precio-max" placeholder="Máximo" step="0.01" min="0">
                                        </div>
                                    </div>

                                    <div class="filtro-grupo">
                                        <label>🎯 Tipo de Equipo</label>
                                        <div class="radio-group">
                                            <div class="radio-item">
                                                <input type="radio" id="radio-todos-equipos" name="tipo-equipo" value="" checked>
                                                <label for="radio-todos-equipos">Todos</label>
                                            </div>
                                            <div class="radio-item">
                                                <input type="radio" id="radio-clubes" name="tipo-equipo" value="0">
                                                <label for="radio-clubes">⚽ Clubes</label>
                                            </div>
                                            <div class="radio-item">
                                                <input type="radio" id="radio-selecciones" name="tipo-equipo" value="1">
                                                <label for="radio-selecciones">🌍 Selecciones</label>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="filtros-checks">
                                    <div class="check-item">
                                        <input type="checkbox" id="filtro-solo-stock">
                                        <label for="filtro-solo-stock">📦 Solo con stock disponible</label>
                                    </div>
                                    <div class="check-item">
                                        <input type="checkbox" id="filtro-destacados">
                                        <label for="filtro-destacados">⭐ Solo productos destacados</label>
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
                                    ▦
                                </button>
                                <button class="btn-view" id="btn-vista-lista" title="Vista en lista">
                                    ☰
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
                            <div class="stat-icon">PR</div>
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
                            <div class="stat-icon">CL</div>
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
                            <div class="stat-icon">PD</div>
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
                            <div class="stat-icon">€</div>
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
