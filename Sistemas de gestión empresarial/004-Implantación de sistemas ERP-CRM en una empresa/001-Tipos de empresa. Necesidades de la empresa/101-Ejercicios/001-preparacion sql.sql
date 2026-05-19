-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS empresaia;
USE empresaia;

-- Crear la tabla de clientes
CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    ciudad VARCHAR(50) NOT NULL,
    pais VARCHAR(50) DEFAULT 'España',
    fecha_registro DATE NOT NULL,
    estado_civil ENUM('Soltero', 'Soltera', 'Casado', 'Casada', 'Divorciado', 'Divorciada', 'Viudo', 'Viuda') DEFAULT 'Soltero',
    edad INT,
    INDEX idx_ciudad (ciudad)
);

-- Insertar clientes
INSERT INTO clientes (nombre, apellidos, email, telefono, ciudad, pais, fecha_registro, estado_civil, edad) VALUES
('Carlos', 'García Martínez', 'carlos.garcia@email.com', '612345678', 'Madrid', 'España', '2023-01-15', 'Casado', 35),
('María', 'López Fernández', 'maria.lopez@email.com', '623456789', 'Barcelona', 'España', '2023-02-20', 'Soltera', 28),
('Juan', 'Rodríguez Sánchez', 'juan.rodriguez@email.com', '634567890', 'Valencia', 'España', '2023-03-10', 'Casado', 42),
('Ana', 'Martínez González', 'ana.martinez@email.com', '645678901', 'Madrid', 'España', '2023-04-05', 'Divorciada', 38),
('Pedro', 'Sánchez Pérez', 'pedro.sanchez@email.com', '656789012', 'Sevilla', 'España', '2023-05-12', 'Soltero', 31),
('Laura', 'Fernández Ruiz', 'laura.fernandez@email.com', '667890123', 'Barcelona', 'España', '2023-06-18', 'Casada', 29),
('Miguel', 'González Díaz', 'miguel.gonzalez@email.com', '678901234', 'Madrid', 'España', '2023-07-22', 'Soltero', 26),
('Carmen', 'Díaz Moreno', 'carmen.diaz@email.com', '689012345', 'Bilbao', 'España', '2023-08-30', 'Casada', 45),
('José', 'Moreno Muñoz', 'jose.moreno@email.com', '690123456', 'Valencia', 'España', '2023-09-14', 'Divorciado', 50),
('Isabel', 'Muñoz Álvarez', 'isabel.munoz@email.com', '601234567', 'Madrid', 'España', '2023-10-08', 'Viuda', 62),
('Francisco', 'Álvarez Romero', 'francisco.alvarez@email.com', '612345679', 'Zaragoza', 'España', '2023-11-19', 'Casado', 40),
('Lucía', 'Romero Torres', 'lucia.romero@email.com', '623456780', 'Barcelona', 'España', '2023-12-03', 'Soltera', 24),
('Antonio', 'Torres Ramírez', 'antonio.torres@email.com', '634567891', 'Málaga', 'España', '2024-01-11', 'Casado', 36),
('Marta', 'Ramírez Jiménez', 'marta.ramirez@email.com', '645678902', 'Madrid', 'España', '2024-02-16', 'Soltera', 27),
('David', 'Jiménez Navarro', 'david.jimenez@email.com', '656789013', 'Sevilla', 'España', '2024-03-20', 'Divorciado', 44),
('Sara', 'Navarro Herrera', 'sara.navarro@email.com', '667890124', 'Valencia', 'España', '2024-04-25', 'Casada', 33),
('Javier', 'Herrera Castro', 'javier.herrera@email.com', '678901235', 'Barcelona', 'España', '2024-05-30', 'Soltero', 30),
('Elena', 'Castro Ortiz', 'elena.castro@email.com', '689012346', 'Madrid', 'España', '2024-06-12', 'Casada', 39),
('Raúl', 'Ortiz Rubio', 'raul.ortiz@email.com', '690123457', 'Bilbao', 'España', '2024-07-18', 'Soltero', 25),
('Patricia', 'Rubio Molina', 'patricia.rubio@email.com', '601234568', 'Zaragoza', 'España', '2024-08-22', 'Casada', 41),
('Alberto', 'Molina Serrano', 'alberto.molina@email.com', '612345680', 'Madrid', 'España', '2024-09-05', 'Divorciado', 48),
('Cristina', 'Serrano Blanco', 'cristina.serrano@email.com', '623456781', 'Valencia', 'España', '2024-10-14', 'Soltera', 23),
('Roberto', 'Blanco Vega', 'roberto.blanco@email.com', '634567892', 'Barcelona', 'España', '2024-11-28', 'Casado', 37),
('Beatriz', 'Vega Mendoza', 'beatriz.vega@email.com', '645678903', 'Sevilla', 'España', '2024-12-02', 'Soltera', 32),
('Fernando', 'Mendoza Cruz', 'fernando.mendoza@email.com', '656789014', 'Madrid', 'España', '2025-01-09', 'Casado', 43),
('Silvia', 'Cruz Reyes', 'silvia.cruz@email.com', '667890125', 'Málaga', 'España', '2023-01-22', 'Divorciada', 46),
('Manuel', 'Reyes Santos', 'manuel.reyes@email.com', '678901236', 'Valencia', 'España', '2023-02-28', 'Soltero', 29),
('Teresa', 'Santos Iglesias', 'teresa.santos@email.com', '689012347', 'Barcelona', 'España', '2023-03-15', 'Casada', 34),
('Ángel', 'Iglesias Gil', 'angel.iglesias@email.com', '690123458', 'Madrid', 'España', '2023-04-19', 'Soltero', 28),
('Rosa', 'Gil Delgado', 'rosa.gil@email.com', '601234569', 'Bilbao', 'España', '2023-05-24', 'Casada', 51),
('Sergio', 'Delgado Vargas', 'sergio.delgado@email.com', '612345681', 'Zaragoza', 'España', '2023-06-30', 'Divorciado', 47),
('Pilar', 'Vargas Cortés', 'pilar.vargas@email.com', '623456782', 'Madrid', 'España', '2023-07-11', 'Soltera', 26),
('Jorge', 'Cortés Aguilar', 'jorge.cortes@email.com', '634567893', 'Sevilla', 'España', '2023-08-17', 'Casado', 38),
('Alicia', 'Aguilar Medina', 'alicia.aguilar@email.com', '645678904', 'Valencia', 'España', '2023-09-21', 'Soltera', 22),
('Daniel', 'Medina León', 'daniel.medina@email.com', '656789015', 'Barcelona', 'España', '2023-10-26', 'Casado', 35),
('Natalia', 'León Marín', 'natalia.leon@email.com', '667890126', 'Madrid', 'España', '2023-11-30', 'Divorciada', 40),
('Adrián', 'Marín Suárez', 'adrian.marin@email.com', '678901237', 'Málaga', 'España', '2023-12-15', 'Soltero', 31),
('Verónica', 'Suárez Ramos', 'veronica.suarez@email.com', '689012348', 'Sevilla', 'España', '2024-01-20', 'Casada', 36),
('Pablo', 'Ramos Carrasco', 'pablo.ramos@email.com', '690123459', 'Valencia', 'España', '2024-02-25', 'Soltero', 27),
('Nuria', 'Carrasco Domínguez', 'nuria.carrasco@email.com', '601234570', 'Barcelona', 'España', '2024-03-30', 'Casada', 33),
('Raquel', 'Domínguez Vázquez', 'raquel.dominguez@email.com', '612345682', 'Madrid', 'España', '2024-04-12', 'Soltera', 25),
('Iván', 'Vázquez Pascual', 'ivan.vazquez@email.com', '623456783', 'Bilbao', 'España', '2024-05-18', 'Divorciado', 49),
('Mónica', 'Pascual Guerrero', 'monica.pascual@email.com', '634567894', 'Zaragoza', 'España', '2024-06-23', 'Casada', 42),
('Rubén', 'Guerrero Calvo', 'ruben.guerrero@email.com', '645678905', 'Madrid', 'España', '2024-07-28', 'Soltero', 30),
('Sandra', 'Calvo Peña', 'sandra.calvo@email.com', '656789016', 'Valencia', 'España', '2024-08-31', 'Casada', 37),
('Óscar', 'Peña Santana', 'oscar.pena@email.com', '667890127', 'Barcelona', 'España', '2024-09-15', 'Soltero', 24),
('Andrea', 'Santana Hidalgo', 'andrea.santana@email.com', '678901238', 'Sevilla', 'España', '2024-10-20', 'Casada', 34),
('Víctor', 'Hidalgo Prieto', 'victor.hidalgo@email.com', '689012349', 'Madrid', 'España', '2024-11-25', 'Divorciado', 45),
('Diana', 'Prieto Montero', 'diana.prieto@email.com', '690123460', 'Málaga', 'España', '2024-12-10', 'Soltera', 29),
('Marcos', 'Montero Cano', 'marcos.montero@email.com', '601234571', 'Valencia', 'España', '2025-01-15', 'Casado', 39);

-- Consultas de ejemplo para agrupación
-- SELECT ciudad, COUNT(*) as total_clientes FROM clientes GROUP BY ciudad ORDER BY total_clientes DESC;
-- SELECT ciudad, AVG(edad) as edad_promedio FROM clientes GROUP BY ciudad;
-- SELECT estado_civil, COUNT(*) as total FROM clientes GROUP BY estado_civil;
