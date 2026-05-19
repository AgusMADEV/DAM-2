-- Base de datos para el Agente de IA Autónomo
-- Sistema de iteración persistente

CREATE DATABASE IF NOT EXISTS agente_ia_autonomo
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE agente_ia_autonomo;

-- Tabla de misiones/objetivos del agente
CREATE TABLE IF NOT EXISTS misiones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    objetivo_final TEXT NOT NULL,
    estado ENUM('pendiente', 'en_proceso', 'completada', 'fallida') DEFAULT 'pendiente',
    prioridad ENUM('baja', 'media', 'alta', 'critica') DEFAULT 'media',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_inicio TIMESTAMP NULL,
    fecha_finalizacion TIMESTAMP NULL,
    progreso INT DEFAULT 0,
    intentos_totales INT DEFAULT 0,
    exitos INT DEFAULT 0,
    fallos INT DEFAULT 0,
    tiempo_estimado INT NULL COMMENT 'Tiempo estimado en minutos',
    INDEX idx_estado (estado),
    INDEX idx_fecha_creacion (fecha_creacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de iteraciones del agente
CREATE TABLE IF NOT EXISTS iteraciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mision_id INT NOT NULL,
    numero_iteracion INT NOT NULL,
    tipo_accion ENUM('analisis', 'planificacion', 'ejecucion', 'validacion', 'correccion') NOT NULL,
    descripcion TEXT NOT NULL,
    entrada TEXT NULL COMMENT 'Input que recibe la iteración',
    salida LONGTEXT NULL COMMENT 'Output generado',
    codigo_generado LONGTEXT NULL,
    resultado ENUM('exito', 'fallo', 'parcial', 'pendiente') DEFAULT 'pendiente',
    error_mensaje TEXT NULL,
    duracion_segundos DECIMAL(10,2) NULL,
    timestamp_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    timestamp_fin TIMESTAMP NULL,
    metadata JSON NULL COMMENT 'Datos adicionales de la iteración',
    FOREIGN KEY (mision_id) REFERENCES misiones(id) ON DELETE CASCADE,
    INDEX idx_mision (mision_id),
    INDEX idx_timestamp (timestamp_inicio)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de decisiones del agente
CREATE TABLE IF NOT EXISTS decisiones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    iteracion_id INT NOT NULL,
    tipo_decision VARCHAR(100) NOT NULL,
    razonamiento TEXT NOT NULL,
    alternativas JSON NULL COMMENT 'Otras opciones consideradas',
    decision_tomada TEXT NOT NULL,
    confianza DECIMAL(3,2) NULL COMMENT 'Nivel de confianza 0-1',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (iteracion_id) REFERENCES iteraciones(id) ON DELETE CASCADE,
    INDEX idx_iteracion (iteracion_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de artefactos generados (archivos, código, documentos)
CREATE TABLE IF NOT EXISTS artefactos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mision_id INT NOT NULL,
    iteracion_id INT NULL,
    tipo VARCHAR(50) NOT NULL COMMENT 'php, javascript, html, css, sql, etc',
    nombre_archivo VARCHAR(255) NOT NULL,
    ruta_archivo VARCHAR(500) NULL,
    contenido LONGTEXT NOT NULL,
    version INT DEFAULT 1,
    es_final BOOLEAN DEFAULT FALSE,
    validado BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (mision_id) REFERENCES misiones(id) ON DELETE CASCADE,
    FOREIGN KEY (iteracion_id) REFERENCES iteraciones(id) ON DELETE SET NULL,
    INDEX idx_mision (mision_id),
    INDEX idx_tipo (tipo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de logs del agente
CREATE TABLE IF NOT EXISTS logs_agente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mision_id INT NULL,
    iteracion_id INT NULL,
    nivel ENUM('debug', 'info', 'warning', 'error', 'critical') DEFAULT 'info',
    mensaje TEXT NOT NULL,
    contexto JSON NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (mision_id) REFERENCES misiones(id) ON DELETE SET NULL,
    FOREIGN KEY (iteracion_id) REFERENCES iteraciones(id) ON DELETE SET NULL,
    INDEX idx_nivel (nivel),
    INDEX idx_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de conocimiento aprendido (memoria del agente)
CREATE TABLE IF NOT EXISTS conocimiento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    categoria VARCHAR(100) NOT NULL,
    concepto VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    ejemplos JSON NULL,
    fuente VARCHAR(255) NULL COMMENT 'De qué misión/iteración se aprendió',
    utilidad_score DECIMAL(3,2) DEFAULT 0.5,
    veces_usado INT DEFAULT 0,
    fecha_aprendizaje TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_ultimo_uso TIMESTAMP NULL,
    INDEX idx_categoria (categoria),
    INDEX idx_utilidad (utilidad_score)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de configuración del agente
CREATE TABLE IF NOT EXISTS configuracion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    clave VARCHAR(100) UNIQUE NOT NULL,
    valor TEXT NOT NULL,
    tipo ENUM('string', 'integer', 'boolean', 'json') DEFAULT 'string',
    descripcion TEXT NULL,
    ultima_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Configuración por defecto
INSERT INTO configuracion (clave, valor, tipo, descripcion) VALUES
('api_url', 'https://api.openai.com/v1/chat/completions', 'string', 'URL de la API de IA'),
('api_key', '', 'string', 'Clave API (vacío por defecto)'),
('max_iteraciones', '50', 'integer', 'Máximo de iteraciones por misión'),
('timeout_iteracion', '120', 'integer', 'Timeout por iteración en segundos'),
('modelo_ia', 'gpt-4', 'string', 'Modelo de IA a utilizar'),
('modo_verbose', 'true', 'boolean', 'Logging detallado'),
('auto_validacion', 'true', 'boolean', 'Validar automáticamente el código generado'),
('persistencia_codigo', 'true', 'boolean', 'Guardar código generado en archivos');

-- Insertar una misión de ejemplo
INSERT INTO misiones (titulo, descripcion, objetivo_final, prioridad) VALUES
('Sistema de Login', 
 'Crear un sistema de autenticación de usuarios con registro, login y recuperación de contraseña',
 'Implementar sistema completo de autenticación funcional con base de datos, validaciones y seguridad',
 'alta');
