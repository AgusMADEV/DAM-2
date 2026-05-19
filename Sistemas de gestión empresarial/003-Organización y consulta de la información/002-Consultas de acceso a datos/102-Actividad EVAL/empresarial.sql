-- Script para crear la base de datos empresarial
-- Eliminar base de datos si existe (opcional)
DROP DATABASE IF EXISTS empresarial;

-- Crear la base de datos
CREATE DATABASE empresarial CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci;

-- Usar la base de datos
USE empresarial;

-- Crear tabla de clientes
CREATE TABLE clientes (
    Identificador INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    telefono VARCHAR(20),
    direccion VARCHAR(200),
    ciudad VARCHAR(100),
    codigo_postal VARCHAR(10),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla de productos
CREATE TABLE productos (
    Identificador INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT DEFAULT 0,
    categoria VARCHAR(50),
    fecha_alta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla de pedidos
CREATE TABLE pedidos (
    Identificador INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(50) DEFAULT 'Pendiente',
    total DECIMAL(10, 2) DEFAULT 0.00,
    observaciones TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(Identificador) ON DELETE CASCADE
);

-- Crear tabla de lineas de pedidos
CREATE TABLE lineaspedidos (
    Identificador INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(Identificador) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(Identificador) ON DELETE CASCADE
);

-- Crear tabla de pedidos con lineas (tabla intermedia o de resumen)
CREATE TABLE pedidosconlineas (
    Identificador INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    numero_lineas INT DEFAULT 0,
    total_productos INT DEFAULT 0,
    importe_total DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(Identificador) ON DELETE CASCADE
);

-- Crear vista de pedidos (combina información de varias tablas)
CREATE VIEW vista_pedidos AS
SELECT 
    p.Identificador AS pedido_id,
    p.fecha_pedido,
    p.estado,
    c.Identificador AS cliente_id,
    c.nombre AS cliente_nombre,
    c.apellidos AS cliente_apellidos,
    c.email AS cliente_email,
    COUNT(lp.Identificador) AS numero_lineas,
    SUM(lp.cantidad) AS total_productos,
    SUM(lp.subtotal) AS importe_total
FROM pedidos p
LEFT JOIN clientes c ON p.cliente_id = c.Identificador
LEFT JOIN lineaspedidos lp ON p.Identificador = lp.pedido_id
GROUP BY p.Identificador, c.Identificador;

-- Insertar datos de ejemplo en clientes
INSERT INTO clientes (nombre, apellidos, email, telefono, direccion, ciudad, codigo_postal) VALUES
('Juan', 'García López', 'juan.garcia@email.com', '666111222', 'Calle Mayor 10', 'Madrid', '28001'),
('María', 'Rodríguez Pérez', 'maria.rodriguez@email.com', '666222333', 'Avenida Principal 25', 'Barcelona', '08001'),
('Carlos', 'Martínez Sánchez', 'carlos.martinez@email.com', '666333444', 'Plaza España 5', 'Valencia', '46001'),
('Ana', 'López Fernández', 'ana.lopez@email.com', '666444555', 'Calle del Sol 15', 'Sevilla', '41001'),
('Pedro', 'González Ruiz', 'pedro.gonzalez@email.com', '666555666', 'Avenida Libertad 30', 'Zaragoza', '50001');

-- Insertar datos de ejemplo en productos
INSERT INTO productos (nombre, descripcion, precio, stock, categoria) VALUES
('Ordenador portátil HP', 'Portátil 15 pulgadas, Intel i5, 8GB RAM', 599.99, 15, 'Informática'),
('Ratón inalámbrico Logitech', 'Ratón ergonómico inalámbrico', 29.99, 50, 'Periféricos'),
('Teclado mecánico RGB', 'Teclado gaming con iluminación RGB', 89.99, 30, 'Periféricos'),
('Monitor Samsung 24"', 'Monitor Full HD 24 pulgadas', 159.99, 20, 'Monitores'),
('Impresora multifunción Canon', 'Impresora, escáner y fotocopiadora', 129.99, 10, 'Impresoras'),
('Disco duro externo 1TB', 'Almacenamiento externo portátil', 59.99, 40, 'Almacenamiento'),
('Webcam HD Logitech', 'Cámara web 1080p', 79.99, 25, 'Periféricos'),
('Auriculares Bluetooth', 'Auriculares inalámbricos con cancelación de ruido', 149.99, 35, 'Audio');

-- Insertar datos de ejemplo en pedidos
INSERT INTO pedidos (cliente_id, estado, total, observaciones) VALUES
(1, 'Completado', 689.98, 'Entrega urgente'),
(2, 'Pendiente', 239.98, NULL),
(3, 'En proceso', 319.97, 'Envío estándar'),
(1, 'Completado', 159.99, NULL),
(4, 'Pendiente', 419.96, 'Llamar antes de entregar');

-- Insertar datos de ejemplo en lineaspedidos
INSERT INTO lineaspedidos (pedido_id, producto_id, cantidad, precio_unitario, subtotal) VALUES
(1, 1, 1, 599.99, 599.99),
(1, 3, 1, 89.99, 89.99),
(2, 2, 2, 29.99, 59.98),
(2, 6, 3, 59.99, 179.97),
(3, 4, 2, 159.99, 319.98),
(4, 4, 1, 159.99, 159.99),
(5, 5, 2, 129.99, 259.98),
(5, 7, 2, 79.99, 159.98);

-- Insertar datos en pedidosconlineas
INSERT INTO pedidosconlineas (pedido_id, numero_lineas, total_productos, importe_total) VALUES
(1, 2, 2, 689.98),
(2, 2, 5, 239.95),
(3, 1, 2, 319.98),
(4, 1, 1, 159.99),
(5, 2, 4, 419.96);

-- Crear usuario y otorgar permisos
-- Eliminar usuario si existe
DROP USER IF EXISTS 'usuarioempresarial'@'localhost';

-- Crear el usuario
CREATE USER 'usuarioempresarial'@'localhost' IDENTIFIED BY 'usuarioempresarial';

-- Otorgar todos los privilegios sobre la base de datos empresarial
GRANT ALL PRIVILEGES ON empresarial.* TO 'usuarioempresarial'@'localhost';

-- Aplicar los cambios
FLUSH PRIVILEGES;

-- Mensaje de confirmación
SELECT 'Base de datos empresarial creada correctamente' AS Mensaje;
SELECT 'Usuario usuarioempresarial creado con todos los privilegios' AS Mensaje;
