<?php
/**
 * Sistema de logging del agente
 */

class Logger {
    private $db = null;
    private $misionId = null;
    private $iteracionId = null;

    public function __construct() {
        try {
            $this->db = Database::getInstance()->getConnection();
        } catch (Exception $e) {
            // Si falla la BD, solo logueamos a archivo
            $this->db = null;
        }
    }

    public function setContext($misionId = null, $iteracionId = null) {
        $this->misionId = $misionId;
        $this->iteracionId = $iteracionId;
    }

    public function debug($mensaje, $contexto = []) {
        $this->log('debug', $mensaje, $contexto);
    }

    public function info($mensaje, $contexto = []) {
        $this->log('info', $mensaje, $contexto);
    }

    public function warning($mensaje, $contexto = []) {
        $this->log('warning', $mensaje, $contexto);
    }

    public function error($mensaje, $contexto = []) {
        $this->log('error', $mensaje, $contexto);
    }

    public function critical($mensaje, $contexto = []) {
        $this->log('critical', $mensaje, $contexto);
    }

    private function log($nivel, $mensaje, $contexto = []) {
        // Log a archivo PRIMERO (siempre funciona)
        $this->logToFile($nivel, $mensaje, $contexto);

        // Log a base de datos solo si está disponible
        if ($this->db !== null) {
            try {
                $stmt = $this->db->prepare("
                    INSERT INTO logs_agente (mision_id, iteracion_id, nivel, mensaje, contexto)
                    VALUES (?, ?, ?, ?, ?)
                ");
                $stmt->execute([
                    $this->misionId,
                    $this->iteracionId,
                    $nivel,
                    $mensaje,
                    empty($contexto) ? null : json_encode($contexto)
                ]);
            } catch (Exception $e) {
                // Si falla el log a DB, registrarlo en archivo
                error_log("Error al guardar log en BD: " . $e->getMessage());
            }
        }
    }

    private function logToFile($nivel, $mensaje, $contexto) {
        try {
            // Asegurar que el directorio existe
            $logsDir = defined('LOGS_PATH') ? LOGS_PATH : __DIR__ . '/../logs';
            if (!is_dir($logsDir)) {
                @mkdir($logsDir, 0755, true);
            }
            
            $logFile = $logsDir . '/agente_' . date('Y-m-d') . '.log';
            $timestamp = date('Y-m-d H:i:s');
            $nivelUpper = strtoupper($nivel);
            $linea = "[{$timestamp}] [{$nivelUpper}] {$mensaje}";
            
            if (!empty($contexto)) {
                $linea .= " | Contexto: " . json_encode($contexto, JSON_UNESCAPED_UNICODE);
            }
            
            $linea .= "\n";
            
            @file_put_contents($logFile, $linea, FILE_APPEND);
        } catch (Exception $e) {
            // Si incluso el log a archivo falla, usar error_log nativo
            error_log("Logger: {$nivel} - {$mensaje}");
        }
    }
}