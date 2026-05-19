-- Sistema de Gestión de Tareas - Base de Datos
-- Generado por Agente IA Autónomo usando Ollama (qwen2.5-coder:7b)

CREATE DATABASE IF NOT EXISTS tasks_db;
USE tasks_db;

CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    status ENUM('pendiente', 'en_proceso', 'completada') NOT NULL DEFAULT 'pendiente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Índice para búsquedas por estado
CREATE INDEX idx_status ON tasks(status);

-- Índice para búsquedas por título
CREATE INDEX idx_title ON tasks(title);
