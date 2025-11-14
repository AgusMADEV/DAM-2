-- Script de instalación para el Sistema ERP
-- Base de datos: MySQL
-- Autor: Sistema de Gestión Empresarial
-- Fecha: 2024

-- Crear base de datos
DROP DATABASE IF EXISTS erp_sistema;
CREATE DATABASE erp_sistema CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE erp_sistema;

-- =====================================================
-- TABLA DE USUARIOS
-- =====================================================
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso TIMESTAMP NULL,
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_activo (activo)
);

-- =====================================================
-- TABLA DE CLIENTES
-- =====================================================
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    direccion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre),
    INDEX idx_email (email),
    INDEX idx_activo (activo)
);

-- =====================================================
-- TABLA DE PRODUCTOS
-- =====================================================
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre),
    INDEX idx_precio (precio),
    INDEX idx_stock (stock),
    INDEX idx_activo (activo)
);

-- =====================================================
-- TABLA DE VENTAS
-- =====================================================
CREATE TABLE ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    usuario_id INT NOT NULL,
    fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL,
    estado ENUM('pendiente', 'completada', 'cancelada') DEFAULT 'pendiente',
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE RESTRICT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE RESTRICT,
    INDEX idx_cliente_id (cliente_id),
    INDEX idx_usuario_id (usuario_id),
    INDEX idx_fecha_venta (fecha_venta),
    INDEX idx_estado (estado)
);

-- =====================================================
-- TABLA DE DETALLE DE VENTAS
-- =====================================================
CREATE TABLE detalle_venta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    venta_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (venta_id) REFERENCES ventas(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE RESTRICT,
    INDEX idx_venta_id (venta_id),
    INDEX idx_producto_id (producto_id)
);

-- =====================================================
-- DATOS INICIALES
-- =====================================================

-- Insertar usuario administrador por defecto
-- Contraseña: admin123 (hash bcrypt)
INSERT INTO usuarios (username, password, nombre, email) VALUES 
('admin', '$2y$10$8mtJmtxgixYFxxbkV7WHM.KZcEawTLmGeKcteNE3yrXMFYNXX65AK', 'Administrador', 'admin@erp.com');

-- Insertar clientes de ejemplo
INSERT INTO clientes (nombre, email, telefono, direccion) VALUES 
('Juan Pérez', 'juan@email.com', '123456789', 'Calle Mayor 123, Madrid'),
('María García', 'maria@email.com', '987654321', 'Avenida Central 456, Barcelona'),
('Carlos López', 'carlos@email.com', '555123456', 'Plaza Principal 789, Valencia'),
('Ana Martínez', 'ana@email.com', '444987654', 'Calle Nueva 321, Sevilla'),
('Pedro González', 'pedro@email.com', '333654987', 'Avenida Sur 654, Bilbao');

-- Insertar productos de ejemplo
INSERT INTO productos (nombre, descripcion, precio, stock) VALUES 
('Ordenador Portátil Dell', 'Portátil Dell Inspiron 15 con procesador Intel i5', 699.99, 15),
('Monitor Samsung 24"', 'Monitor LED Samsung de 24 pulgadas Full HD', 199.99, 25),
('Teclado Mecánico Logitech', 'Teclado mecánico para gaming RGB', 89.99, 30),
('Ratón Inalámbrico HP', 'Ratón óptico inalámbrico ergonómico', 29.99, 50),
('Impresora Canon PIXMA', 'Impresora multifunción color WiFi', 149.99, 12),
('Disco Duro SSD 500GB', 'SSD Samsung EVO 500GB SATA III', 79.99, 40),
('Memoria RAM DDR4 16GB', 'Módulo de memoria RAM DDR4 16GB 3200MHz', 89.99, 35),
('Cámara Web Logitech', 'Webcam HD 1080p con micrófono integrado', 59.99, 20),
('Altavoces Bluetooth JBL', 'Altavoces portátiles Bluetooth 20W', 49.99, 18),
('Cable HDMI 2m', 'Cable HDMI 4K de alta velocidad 2 metros', 12.99, 8);

-- Insertar algunas ventas de ejemplo
INSERT INTO ventas (cliente_id, usuario_id, fecha_venta, total, estado) VALUES 
(1, 1, '2024-11-01 10:30:00', 699.99, 'completada'),
(2, 1, '2024-11-05 14:15:00', 289.98, 'completada'),
(3, 1, '2024-11-08 09:45:00', 139.98, 'completada'),
(4, 1, '2024-11-10 16:20:00', 199.99, 'completada'),
(5, 1, '2024-11-12 11:30:00', 89.99, 'completada');

-- Insertar detalles de ventas
INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio_unitario, subtotal) VALUES 
-- Venta 1: Ordenador Portátil
(1, 1, 1, 699.99, 699.99),
-- Venta 2: Monitor + Ratón
(2, 2, 1, 199.99, 199.99),
(2, 4, 3, 29.99, 89.97),
-- Venta 3: Teclado + Cable HDMI
(3, 3, 1, 89.99, 89.99),
(3, 10, 1, 12.99, 12.99),
(3, 10, 3, 12.99, 38.97),
-- Venta 4: Monitor
(4, 2, 1, 199.99, 199.99),
-- Venta 5: Teclado
(5, 3, 1, 89.99, 89.99);

-- =====================================================
-- VISTAS ÚTILES
-- =====================================================

-- Vista de ventas con información completa
CREATE VIEW vista_ventas AS
SELECT 
    v.id,
    v.fecha_venta,
    c.nombre as cliente,
    u.nombre as vendedor,
    v.total,
    v.estado,
    COUNT(dv.id) as items_count
FROM ventas v
INNER JOIN clientes c ON v.cliente_id = c.id
INNER JOIN usuarios u ON v.usuario_id = u.id
LEFT JOIN detalle_venta dv ON v.id = dv.venta_id
GROUP BY v.id, v.fecha_venta, c.nombre, u.nombre, v.total, v.estado;

-- Vista de productos con stock bajo
CREATE VIEW vista_stock_bajo AS
SELECT 
    id,
    nombre,
    stock,
    precio,
    (stock * precio) as valor_stock
FROM productos 
WHERE stock < 10 AND activo = 1
ORDER BY stock ASC;

-- Vista de estadísticas mensuales
CREATE VIEW vista_estadisticas_mes AS
SELECT 
    YEAR(fecha_venta) as año,
    MONTH(fecha_venta) as mes,
    COUNT(*) as total_ventas,
    SUM(total) as facturacion_total,
    AVG(total) as venta_promedio,
    COUNT(DISTINCT cliente_id) as clientes_unicos
FROM ventas 
WHERE estado = 'completada'
GROUP BY YEAR(fecha_venta), MONTH(fecha_venta)
ORDER BY año DESC, mes DESC;

-- =====================================================
-- PROCEDIMIENTOS ALMACENADOS
-- =====================================================

DELIMITER //

-- Procedimiento para procesar una venta
CREATE PROCEDURE ProcesarVenta(
    IN p_cliente_id INT,
    IN p_usuario_id INT,
    IN p_producto_id INT,
    IN p_cantidad INT,
    OUT p_venta_id INT,
    OUT p_mensaje VARCHAR(255)
)
BEGIN
    DECLARE v_precio DECIMAL(10,2);
    DECLARE v_stock INT;
    DECLARE v_total DECIMAL(10,2);
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_mensaje = 'Error al procesar la venta';
        SET p_venta_id = 0;
    END;
    
    START TRANSACTION;
    
    -- Verificar stock disponible
    SELECT precio, stock INTO v_precio, v_stock 
    FROM productos 
    WHERE id = p_producto_id AND activo = 1;
    
    IF v_stock < p_cantidad THEN
        SET p_mensaje = 'Stock insuficiente';
        SET p_venta_id = 0;
        ROLLBACK;
    ELSE
        -- Calcular total
        SET v_total = v_precio * p_cantidad;
        
        -- Crear venta
        INSERT INTO ventas (cliente_id, usuario_id, total, estado)
        VALUES (p_cliente_id, p_usuario_id, v_total, 'completada');
        
        SET p_venta_id = LAST_INSERT_ID();
        
        -- Crear detalle
        INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio_unitario, subtotal)
        VALUES (p_venta_id, p_producto_id, p_cantidad, v_precio, v_total);
        
        -- Actualizar stock
        UPDATE productos SET stock = stock - p_cantidad WHERE id = p_producto_id;
        
        SET p_mensaje = 'Venta procesada exitosamente';
        COMMIT;
    END IF;
END//

DELIMITER ;

-- =====================================================
-- TRIGGERS
-- =====================================================

-- Trigger para actualizar fecha de modificación en productos
DELIMITER //
CREATE TRIGGER actualizar_fecha_producto
    BEFORE UPDATE ON productos
    FOR EACH ROW
BEGIN
    SET NEW.fecha_actualizacion = NOW();
END//
DELIMITER ;

-- Trigger para validar stock antes de venta
DELIMITER //
CREATE TRIGGER validar_stock_venta
    BEFORE INSERT ON detalle_venta
    FOR EACH ROW
BEGIN
    DECLARE v_stock_actual INT;
    
    SELECT stock INTO v_stock_actual 
    FROM productos 
    WHERE id = NEW.producto_id;
    
    IF v_stock_actual < NEW.cantidad THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Stock insuficiente para completar la venta';
    END IF;
END//
DELIMITER ;

-- =====================================================
-- ÍNDICES ADICIONALES PARA PERFORMANCE
-- =====================================================

-- Índices compuestos para consultas frecuentes
CREATE INDEX idx_ventas_fecha_estado ON ventas(fecha_venta, estado);
CREATE INDEX idx_productos_precio_stock ON productos(precio, stock);
CREATE INDEX idx_clientes_nombre_activo ON clientes(nombre, activo);

-- =====================================================
-- GRANTS Y PERMISOS (si se usa un usuario específico)
-- =====================================================

-- Si se crea un usuario específico para la aplicación, usar estos comandos:
-- CREATE USER 'erp_user'@'localhost' IDENTIFIED BY 'erp_password';
-- GRANT SELECT, INSERT, UPDATE, DELETE ON erp_sistema.* TO 'erp_user'@'localhost';
-- FLUSH PRIVILEGES;

-- =====================================================
-- SCRIPT COMPLETADO
-- =====================================================

-- Mostrar resumen de instalación
SELECT 'Base de datos ERP creada exitosamente' AS mensaje;
SELECT COUNT(*) AS total_usuarios FROM usuarios;
SELECT COUNT(*) AS total_clientes FROM clientes;
SELECT COUNT(*) AS total_productos FROM productos;
SELECT COUNT(*) AS total_ventas FROM ventas;