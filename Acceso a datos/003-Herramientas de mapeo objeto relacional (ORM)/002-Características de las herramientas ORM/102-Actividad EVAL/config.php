<?php
/**
 * config.php
 * 
 * Archivo de configuración centralizado para toda la aplicación.
 * Cambiar los datos aquí y se aplicarán en todos los archivos.
 */

// ════════════════════════════════════════════════════════════════════════════
// CONFIGURACIÓN DE CONEXIÓN A LA BASE DE DATOS
// ════════════════════════════════════════════════════════════════════════════

// Host/Servidor de la base de datos
define('DB_HOST', 'localhost');

// Usuario de MySQL
define('DB_USER', 'root');

// Contraseña de MySQL (vacío si es XAMPP por defecto)
define('DB_PASS', '');

// Nombre de la base de datos
define('DB_NAME', 'entrenamientos_db');

// Nombre de la tabla principal
define('DB_TABLE_ENTRENAMIENTOS', 'entrenamientos');


// ════════════════════════════════════════════════════════════════════════════
// CONFIGURACIÓN DEL SITIO
// ════════════════════════════════════════════════════════════════════════════

// Título de la aplicación
define('APP_TITLE', 'Seguimiento de Entrenamientos');

// Versión de la aplicación
define('APP_VERSION', '1.0');

// Zona horaria
define('TIMEZONE', 'Europe/Madrid');
date_default_timezone_set(TIMEZONE);

// Idioma
define('LANG', 'es');


// ════════════════════════════════════════════════════════════════════════════
// CONFIGURACIÓN DE DESARROLLO
// ════════════════════════════════════════════════════════════════════════════

// Modo depuración (mostrar errores)
define('DEBUG', true);

// Mostrar errores en la salida
if (DEBUG) {
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
} else {
    error_reporting(0);
    ini_set('display_errors', 0);
}


// ════════════════════════════════════════════════════════════════════════════
// FUNCIONES DE UTILIDAD
// ════════════════════════════════════════════════════════════════════════════

/**
 * Obtiene los parámetros de conexión como array
 * 
 * @return array Array con los parámetros de conexión
 */
function obtenerConfiguracion() {
    return [
        'host' => DB_HOST,
        'usuario' => DB_USER,
        'contrasena' => DB_PASS,
        'basedatos' => DB_NAME
    ];
}

/**
 * Imprime los datos de configuración (solo si DEBUG está activado)
 * 
 * @return void
 */
function mostrarConfiguracion() {
    if (!DEBUG) return;
    
    echo '<pre>';
    echo "╔════════════════════════════════════════╗\n";
    echo "║  CONFIGURACIÓN DE LA APLICACIÓN       ║\n";
    echo "╚════════════════════════════════════════╝\n\n";
    
    echo "Aplicación: " . APP_TITLE . " v" . APP_VERSION . "\n";
    echo "Host: " . DB_HOST . "\n";
    echo "Usuario: " . DB_USER . "\n";
    echo "Base de datos: " . DB_NAME . "\n";
    echo "Tabla: " . DB_TABLE_ENTRENAMIENTOS . "\n";
    echo "Zona horaria: " . TIMEZONE . "\n";
    echo "Idioma: " . LANG . "\n";
    echo '</pre>';
}
?>
