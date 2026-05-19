<?php
/**
 * Configuración general del Agente IA Autónomo
 */

// Configuración de la API de IA
// Ollama local (http://localhost:11434)
define('AI_API_URL', 'http://localhost:11434/v1/chat/completions');
define('AI_API_KEY', 'ollama'); // Ollama no requiere API key, pero ponemos algo por compatibilidad
define('AI_MODEL', 'qwen2.5-coder:7b'); // Especializado en código - ¡el mejor de tus modelos!
define('AI_TEMPERATURE', 0.7);
define('AI_MAX_TOKENS', 4000);

// Configuración del agente
define('MAX_ITERACIONES', 50);
define('TIMEOUT_ITERACION', 300); // segundos (5 minutos para proyectos complejos)
define('MODO_VERBOSE', true);
define('AUTO_VALIDACION', true);
define('PERSISTENCIA_CODIGO', true);

// Rutas del proyecto
define('BASE_PATH', __DIR__ . '/..');
define('OUTPUT_PATH', BASE_PATH . '/output');
define('LOGS_PATH', BASE_PATH . '/logs');
define('TEMP_PATH', BASE_PATH . '/temp');

// Crear directorios si no existen
$dirs = [OUTPUT_PATH, LOGS_PATH, TEMP_PATH];
foreach ($dirs as $dir) {
    if (!is_dir($dir)) {
        mkdir($dir, 0755, true);
    }
}

// Zona horaria
date_default_timezone_set('Europe/Madrid');

// Manejo de errores - NO mostrar errores en la salida (solo loguear)
ini_set('display_errors', 0);
ini_set('display_startup_errors', 0);
error_reporting(E_ALL);
ini_set('log_errors', 1);
ini_set('error_log', LOGS_PATH . '/php_errors.log');
