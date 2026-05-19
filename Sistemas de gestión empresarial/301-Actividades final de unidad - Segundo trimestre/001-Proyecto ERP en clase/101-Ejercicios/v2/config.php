<?php
// =============================================
// TOTALKIT ERP - ARCHIVO DE CONFIGURACIÓN
// =============================================

// =============================================
// CONFIGURACIÓN DE BASE DE DATOS
// =============================================
define('DB_HOST', 'localhost');
define('DB_NAME', 'tienda_camisetas');
define('DB_USER', 'totalkit');
define('DB_PASS', 'totalkit');

// =============================================
// CREDENCIALES DE LOGIN
// =============================================
define('LOGIN_USUARIO', 'admin');
define('LOGIN_PASSWORD', 'admin123');

// =============================================
// CONFIGURACIÓN GENERAL
// =============================================
define('APP_NAME', 'TotalKit ERP');
define('APP_VERSION', '1.0.0');
define('TIMEZONE', 'Europe/Madrid');

// Establecer zona horaria
date_default_timezone_set(TIMEZONE);

// =============================================
// FUNCIÓN DE CONEXIÓN A BASE DE DATOS
// =============================================

/**
 * Crear conexión a la base de datos
 * @return mysqli|false Objeto de conexión o false en caso de error
 */
function obtener_conexion() {
    $conexion = mysqli_connect(DB_HOST, DB_USER, DB_PASS, DB_NAME);
    
    if (!$conexion) {
        error_log("Error de conexión a la base de datos: " . mysqli_connect_error());
        return false;
    }
    
    mysqli_set_charset($conexion, "utf8");
    
    return $conexion;
}

/**
 * Cerrar conexión a la base de datos de forma segura
 * @param mysqli $conexion Objeto de conexión
 */
function cerrar_conexion($conexion) {
    if ($conexion && $conexion instanceof mysqli) {
        mysqli_close($conexion);
    }
}
