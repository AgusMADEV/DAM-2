-- ════════════════════════════════════════════════════════════════════════════
-- SCRIPT SQL - CREAR BASE DE DATOS Y TABLAS DE ENTRENAMIENTOS
-- ════════════════════════════════════════════════════════════════════════════
--
-- TABLAS CREADAS:
--   1. usuarios ............. Atletas/deportistas
--   2. planes_entrenamiento . Planes de entrenamiento
--   3. entrenamientos ....... Sesiones de entrenamiento
--
-- INSTRUCCIONES:
-- 1. Abre phpMyAdmin: http://localhost/phpmyadmin/
-- 2. Haz clic en la pestaña "SQL"
-- 3. Copia y pega TODO el código de este archivo
-- 4. Haz clic en "Ejecutar"
--
-- ════════════════════════════════════════════════════════════════════════════


-- ────────────────────────────────────────────────────────────────────────────
-- 1. CREAR BASE DE DATOS
-- ────────────────────────────────────────────────────────────────────────────

CREATE DATABASE IF NOT EXISTS entrenamientos_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Seleccionar la base de datos
USE entrenamientos_db;


-- ────────────────────────────────────────────────────────────────────────────
-- 2. CREAR TABLA DE USUARIOS (ATLETAS)
-- ────────────────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS usuarios (
    -- ID del usuario
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Nombre del atleta
    nombre VARCHAR(100) NOT NULL,
    
    -- Apellido del atleta
    apellido VARCHAR(100) NOT NULL,
    
    -- Email del atleta
    email VARCHAR(100) UNIQUE NOT NULL,
    
    -- Edad en años
    edad INT NULL,
    
    -- Peso corporal en kg
    peso_corporal DECIMAL(5, 2) NULL COMMENT 'Peso en kilogramos',
    
    -- Altura en cm
    altura INT NULL COMMENT 'Altura en centímetros',
    
    -- Especialidad o deporte principal
    especialidad VARCHAR(100) NULL,
    
    -- Nivel de experiencia (principiante, intermedio, avanzado)
    nivel_experiencia ENUM('Principiante', 'Intermedio', 'Avanzado') DEFAULT 'Principiante',
    
    -- Teléfono de contacto
    telefono VARCHAR(20) NULL,
    
    -- Fecha de registro
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Último login
    ultimo_login TIMESTAMP NULL
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ────────────────────────────────────────────────────────────────────────────
-- 3. CREAR TABLA DE PLANES DE ENTRENAMIENTO
-- ────────────────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS planes_entrenamiento (
    -- ID del plan
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Nombre del plan
    nombre VARCHAR(150) NOT NULL,
    
    -- Descripción del plan
    descripcion TEXT NULL,
    
    -- ID del usuario (relación con tabla usuarios)
    usuario_id INT NOT NULL,
    
    -- Objetivo del plan (pérdida de peso, ganancia muscular, resistencia, flexibilidad, etc)
    objetivo VARCHAR(100) NOT NULL,
    
    -- Duración del plan en semanas
    duracion_semanas INT NOT NULL,
    
    -- Frecuencia de entrenamientos por semana
    frecuencia_semanal INT NOT NULL DEFAULT 3,
    
    -- Intensidad (baja, media, alta)
    intensidad ENUM('Baja', 'Media', 'Alta') DEFAULT 'Media',
    
    -- Fecha de inicio del plan
    fecha_inicio DATE NOT NULL,
    
    -- Fecha de finalización del plan
    fecha_fin DATE NULL,
    
    -- Estado del plan (activo, completado, pausado)
    estado ENUM('Activo', 'Completado', 'Pausado') DEFAULT 'Activo',
    
    -- Fecha de creación
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Clave foránea
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ────────────────────────────────────────────────────────────────────────────
-- 4. CREAR TABLA DE ENTRENAMIENTOS
-- ────────────────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS entrenamientos (
    -- Campo ID (clave primaria, auto-incremento)
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- ID del usuario que realizó el entrenamiento
    usuario_id INT NOT NULL,
    
    -- ID del plan al que pertenece (opcional)
    plan_id INT NULL,
    
    -- Tipo de ejercicio realizado
    tipo_ejercicio VARCHAR(100) NOT NULL,
    
    -- Duración del entrenamiento en minutos
    duracion INT NOT NULL COMMENT 'Duración en minutos',
    
    -- Número de repeticiones realizadas
    repeticiones INT NULL COMMENT 'Número de repeticiones',
    
    -- Series realizadas
    series INT NULL,
    
    -- Peso utilizado en kilogramos
    peso DECIMAL(5, 2) NULL COMMENT 'Peso en kilogramos',
    
    -- Calorías quemadas (estimadas)
    calorias_quemadas INT NULL,
    
    -- Fecha del entrenamiento
    fecha DATE NOT NULL,
    
    -- Hora del entrenamiento
    hora TIME NULL,
    
    -- Dificultad (fácil, normal, difícil)
    dificultad ENUM('Fácil', 'Normal', 'Difícil') DEFAULT 'Normal',
    
    -- Observaciones o comentarios sobre el entrenamiento
    comentarios TEXT NULL,
    
    -- Fecha y hora de creación del registro
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Claves foráneas
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (plan_id) REFERENCES planes_entrenamiento(id) ON DELETE SET NULL
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ────────────────────────────────────────────────────────────────────────────
-- 5. CREAR ÍNDICES PARA MEJOR RENDIMIENTO
-- ────────────────────────────────────────────────────────────────────────────

-- Índices en usuarios
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_especialidad ON usuarios(especialidad);

-- Índices en planes_entrenamiento
CREATE INDEX idx_planes_usuario ON planes_entrenamiento(usuario_id);
CREATE INDEX idx_planes_estado ON planes_entrenamiento(estado);
CREATE INDEX idx_planes_objetivo ON planes_entrenamiento(objetivo);

-- Índices en entrenamientos
CREATE INDEX idx_entrenamientos_usuario ON entrenamientos(usuario_id);
CREATE INDEX idx_entrenamientos_plan ON entrenamientos(plan_id);
CREATE INDEX idx_entrenamientos_fecha ON entrenamientos(fecha);
CREATE INDEX idx_entrenamientos_tipo ON entrenamientos(tipo_ejercicio);


-- ════════════════════════════════════════════════════════════════════════════
-- INSERTAR DATOS DE EJEMPLO
-- ════════════════════════════════════════════════════════════════════════════

-- ────────────────────────────────────────────────────────────────────────────
-- INSERTAR USUARIOS
-- ────────────────────────────────────────────────────────────────────────────

INSERT INTO usuarios (nombre, apellido, email, edad, peso_corporal, altura, especialidad, nivel_experiencia, telefono) VALUES
('Juan', 'García López', 'juan.garcia@email.com', 28, 78.5, 180, 'Fitness', 'Intermedio', '123456789'),
('María', 'Rodríguez Pérez', 'maria.rodriguez@email.com', 32, 65.0, 165, 'Atletismo', 'Avanzado', '987654321'),
('Carlos', 'Martínez Ruiz', 'carlos.martinez@email.com', 25, 82.0, 185, 'Musculación', 'Principiante', '555444333');


-- ────────────────────────────────────────────────────────────────────────────
-- INSERTAR PLANES DE ENTRENAMIENTO
-- ────────────────────────────────────────────────────────────────────────────

INSERT INTO planes_entrenamiento (nombre, descripcion, usuario_id, objetivo, duracion_semanas, frecuencia_semanal, intensidad, fecha_inicio, fecha_fin, estado) VALUES
('Plan Ganancia Muscular', 'Plan intensivo de 8 semanas para ganar masa muscular', 1, 'Ganancia muscular', 8, 4, 'Alta', '2024-01-15', '2024-03-10', 'Activo'),
('Plan Resistencia Cardio', 'Plan de resistencia cardiovascular de 6 semanas', 2, 'Resistencia', 6, 5, 'Alta', '2024-01-20', '2024-03-02', 'Activo'),
('Plan Principiante', 'Plan suave de iniciación para principiantes', 3, 'Fitness general', 4, 3, 'Baja', '2024-01-22', '2024-02-19', 'Activo');


-- ────────────────────────────────────────────────────────────────────────────
-- INSERTAR ENTRENAMIENTOS
-- ────────────────────────────────────────────────────────────────────────────

INSERT INTO entrenamientos (usuario_id, plan_id, tipo_ejercicio, duracion, repeticiones, series, peso, calorias_quemadas, fecha, hora, dificultad, comentarios) VALUES

-- Entrenamientos de Juan García
(1, 1, 'Flexiones', 30, 50, 5, 0, 150, '2024-01-22', '07:00:00', 'Normal', 'Buen entrenamiento con buena forma'),
(1, 1, 'Sentadillas', 45, 30, 4, 20, 250, '2024-01-22', '07:35:00', 'Normal', 'Peso moderado, excelente control'),
(1, 1, 'Press de banca', 60, 8, 4, 60, 300, '2024-01-20', '18:00:00', 'Difícil', 'Peso pesado, buen rendimiento'),
(1, 1, 'Fondos', 25, 30, 3, 0, 120, '2024-01-19', '07:30:00', 'Normal', 'Trabajo en barras paralelas'),

-- Entrenamientos de María Rodríguez
(2, 2, 'Correr', 60, 0, 1, 0, 500, '2024-01-21', '06:30:00', 'Difícil', '10 km en pista a ritmo constante'),
(2, 2, 'Natación', 45, 0, 1, 0, 400, '2024-01-19', '17:00:00', 'Normal', '2 km a ritmo moderado'),
(2, 2, 'Ciclismo', 90, 0, 1, 0, 450, '2024-01-18', '06:00:00', 'Difícil', 'Ruta de montaña, 35 km'),
(2, 2, 'Correr', 30, 0, 1, 0, 250, '2024-01-17', '07:00:00', 'Normal', '5 km trote suave'),

-- Entrenamientos de Carlos Martínez
(3, 3, 'Abdominales', 20, 100, 5, 0, 100, '2024-01-18', '08:00:00', 'Fácil', '5 series de 20 repeticiones'),
(3, 3, 'Flexiones', 15, 20, 3, 0, 80, '2024-01-17', '08:15:00', 'Fácil', 'Flexiones básicas de inicio'),
(3, 3, 'Sentadillas', 20, 25, 3, 0, 100, '2024-01-16', '08:30:00', 'Fácil', 'Sin peso corporal, movimiento controlado'),
(3, 3, 'Caminata', 45, 0, 1, 0, 200, '2024-01-15', '18:00:00', 'Fácil', 'Caminata ligera en parque');


-- ────────────────────────────────────────────────────────────────────────────
-- CONSULTAS ÚTILES DE PRUEBA
-- ────────────────────────────────────────────────────────────────────────────

-- VER TODOS LOS DATOS
-- SELECT * FROM usuarios;
-- SELECT * FROM planes_entrenamiento;
-- SELECT * FROM entrenamientos;

-- CONSULTAS CON JOINS (Relaciones)
-- SELECT u.nombre, u.apellido, p.nombre as plan, p.objetivo 
-- FROM usuarios u 
-- JOIN planes_entrenamiento p ON u.id = p.usuario_id;

-- ENTRENAMIENTOS POR USUARIO
-- SELECT u.nombre, e.tipo_ejercicio, e.duracion, e.fecha 
-- FROM usuarios u 
-- JOIN entrenamientos e ON u.id = e.usuario_id 
-- ORDER BY e.fecha DESC;

-- ESTADÍSTICAS POR USUARIO
-- SELECT u.nombre, COUNT(e.id) as total_entrenamientos, SUM(e.duracion) as duracion_total, AVG(e.duracion) as duracion_promedio
-- FROM usuarios u 
-- LEFT JOIN entrenamientos e ON u.id = e.usuario_id 
-- GROUP BY u.id;

-- ENTRENAMIENTOS POR TIPO
-- SELECT tipo_ejercicio, COUNT(*) as cantidad, SUM(duracion) as duracion_total, AVG(peso) as peso_promedio
-- FROM entrenamientos 
-- WHERE peso > 0
-- GROUP BY tipo_ejercicio;

-- CALORIAS QUEMADAS POR USUARIO
-- SELECT u.nombre, SUM(e.calorias_quemadas) as total_calorias
-- FROM usuarios u 
-- JOIN entrenamientos e ON u.id = e.usuario_id 
-- GROUP BY u.id 
-- ORDER BY total_calorias DESC;


-- ════════════════════════════════════════════════════════════════════════════
-- ✅ SCRIPT COMPLETADO
-- ════════════════════════════════════════════════════════════════════════════
--
-- Base de datos: entrenamientos_db
-- Tablas creadas: 3
--   • usuarios (3 registros)
--   • planes_entrenamiento (3 registros)
--   • entrenamientos (12 registros)
--
-- Relaciones:
--   • entrenamientos -> usuarios (muchos a uno)
--   • entrenamientos -> planes_entrenamiento (muchos a uno)
--   • planes_entrenamiento -> usuarios (muchos a uno)
--
-- La aplicación PHP está lista para usar esta base de datos mejorada.
-- ════════════════════════════════════════════════════════════════════════════


