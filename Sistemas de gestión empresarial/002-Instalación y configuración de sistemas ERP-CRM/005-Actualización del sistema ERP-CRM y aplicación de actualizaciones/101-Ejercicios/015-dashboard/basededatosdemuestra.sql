-- ============================================
-- BASE DE DATOS TIENDA ONLINE
-- ============================================

-- Eliminar tablas si existen
DROP TABLE IF EXISTS detalle_pedidos;
DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS valoraciones;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS categorias;
DROP TABLE IF EXISTS direcciones_envio;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS metodos_pago;

-- ============================================
-- TABLA: clientes
-- ============================================
CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE,
    INDEX idx_email (email),
    INDEX idx_fecha_registro (fecha_registro)
);

-- ============================================
-- TABLA: direcciones_envio
-- ============================================
CREATE TABLE direcciones_envio (
    id_direccion INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT NOT NULL,
    nombre_destinatario VARCHAR(150) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    provincia VARCHAR(100) NOT NULL,
    codigo_postal VARCHAR(10) NOT NULL,
    pais VARCHAR(50) DEFAULT 'España',
    telefono VARCHAR(20),
    es_predeterminada BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    INDEX idx_cliente (id_cliente)
);

-- ============================================
-- TABLA: categorias
-- ============================================
CREATE TABLE categorias (
    id_categoria INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    categoria_padre INT,
    activa BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (categoria_padre) REFERENCES categorias(id_categoria) ON DELETE SET NULL,
    INDEX idx_categoria_padre (categoria_padre)
);

-- ============================================
-- TABLA: productos
-- ============================================
CREATE TABLE productos (
    id_producto INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    id_categoria INT,
    precio DECIMAL(10, 2) NOT NULL,
    precio_oferta DECIMAL(10, 2),
    stock INT DEFAULT 0,
    imagen_url VARCHAR(255),
    peso_kg DECIMAL(6, 2),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria) ON DELETE SET NULL,
    INDEX idx_categoria (id_categoria),
    INDEX idx_precio (precio),
    INDEX idx_activo (activo)
);

-- ============================================
-- TABLA: metodos_pago
-- ============================================
CREATE TABLE metodos_pago (
    id_metodo_pago INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE
);

-- ============================================
-- TABLA: pedidos
-- ============================================
CREATE TABLE pedidos (
    id_pedido INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT NOT NULL,
    id_direccion_envio INT NOT NULL,
    id_metodo_pago INT NOT NULL,
    fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('pendiente', 'procesando', 'enviado', 'entregado', 'cancelado') DEFAULT 'pendiente',
    subtotal DECIMAL(10, 2) NOT NULL,
    gastos_envio DECIMAL(10, 2) DEFAULT 0.00,
    impuestos DECIMAL(10, 2) DEFAULT 0.00,
    total DECIMAL(10, 2) NOT NULL,
    notas TEXT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    FOREIGN KEY (id_direccion_envio) REFERENCES direcciones_envio(id_direccion),
    FOREIGN KEY (id_metodo_pago) REFERENCES metodos_pago(id_metodo_pago),
    INDEX idx_cliente (id_cliente),
    INDEX idx_fecha_pedido (fecha_pedido),
    INDEX idx_estado (estado)
);

-- ============================================
-- TABLA: detalle_pedidos
-- ============================================
CREATE TABLE detalle_pedidos (
    id_detalle INT PRIMARY KEY AUTO_INCREMENT,
    id_pedido INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    INDEX idx_pedido (id_pedido),
    INDEX idx_producto (id_producto)
);

-- ============================================
-- TABLA: valoraciones
-- ============================================
CREATE TABLE valoraciones (
    id_valoracion INT PRIMARY KEY AUTO_INCREMENT,
    id_producto INT NOT NULL,
    id_cliente INT NOT NULL,
    puntuacion INT CHECK (puntuacion BETWEEN 1 AND 5),
    comentario TEXT,
    fecha_valoracion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto) ON DELETE CASCADE,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    INDEX idx_producto (id_producto),
    INDEX idx_cliente (id_cliente),
    UNIQUE KEY unique_valoracion (id_producto, id_cliente)
);

-- ============================================
-- VISTAS
-- ============================================

-- Vista: Resumen de pedidos por cliente
CREATE VIEW vista_pedidos_cliente AS
SELECT 
    c.id_cliente,
    c.nombre,
    c.apellidos,
    c.email,
    COUNT(p.id_pedido) AS total_pedidos,
    SUM(p.total) AS total_gastado,
    MAX(p.fecha_pedido) AS ultimo_pedido
FROM clientes c
LEFT JOIN pedidos p ON c.id_cliente = p.id_cliente
GROUP BY c.id_cliente, c.nombre, c.apellidos, c.email;

-- Vista: Productos más vendidos
CREATE VIEW vista_productos_mas_vendidos AS
SELECT 
    pr.id_producto,
    pr.nombre,
    pr.precio,
    cat.nombre AS categoria,
    SUM(dp.cantidad) AS unidades_vendidas,
    SUM(dp.subtotal) AS ingresos_totales,
    COUNT(DISTINCT dp.id_pedido) AS numero_pedidos
FROM productos pr
JOIN detalle_pedidos dp ON pr.id_producto = dp.id_producto
JOIN categorias cat ON pr.id_categoria = cat.id_categoria
GROUP BY pr.id_producto, pr.nombre, pr.precio, cat.nombre
ORDER BY unidades_vendidas DESC;

-- Vista: Estado del inventario
CREATE VIEW vista_inventario AS
SELECT 
    p.id_producto,
    p.nombre,
    c.nombre AS categoria,
    p.precio,
    p.stock,
    CASE 
        WHEN p.stock = 0 THEN 'Sin stock'
        WHEN p.stock < 10 THEN 'Stock bajo'
        ELSE 'Stock disponible'
    END AS estado_stock,
    COALESCE(AVG(v.puntuacion), 0) AS valoracion_media,
    COUNT(v.id_valoracion) AS numero_valoraciones
FROM productos p
LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
LEFT JOIN valoraciones v ON p.id_producto = v.id_producto
WHERE p.activo = TRUE
GROUP BY p.id_producto, p.nombre, c.nombre, p.precio, p.stock;

-- Vista: Detalles completos de pedidos
CREATE VIEW vista_detalle_pedidos_completo AS
SELECT 
    ped.id_pedido,
    ped.fecha_pedido,
    ped.estado,
    c.nombre AS nombre_cliente,
    c.apellidos AS apellidos_cliente,
    c.email,
    pr.nombre AS producto,
    dp.cantidad,
    dp.precio_unitario,
    dp.subtotal,
    ped.total AS total_pedido,
    mp.nombre AS metodo_pago,
    CONCAT(d.direccion, ', ', d.ciudad, ', ', d.provincia, ' ', d.codigo_postal) AS direccion_envio
FROM pedidos ped
JOIN clientes c ON ped.id_cliente = c.id_cliente
JOIN detalle_pedidos dp ON ped.id_pedido = dp.id_pedido
JOIN productos pr ON dp.id_producto = pr.id_producto
JOIN metodos_pago mp ON ped.id_metodo_pago = mp.id_metodo_pago
JOIN direcciones_envio d ON ped.id_direccion_envio = d.id_direccion;

-- ============================================
-- INSERCIONES DE DATOS
-- ============================================

-- Insertar categorías
INSERT INTO categorias (nombre, descripcion, categoria_padre) VALUES
('Electrónica', 'Productos electrónicos y tecnología', NULL),
('Ordenadores', 'Ordenadores portátiles y de sobremesa', 1),
('Móviles y Tablets', 'Smartphones y tabletas', 1),
('Accesorios Electrónicos', 'Accesorios para dispositivos electrónicos', 1),
('Hogar y Cocina', 'Artículos para el hogar y cocina', NULL),
('Electrodomésticos', 'Electrodomésticos grandes y pequeños', 5),
('Decoración', 'Artículos decorativos para el hogar', 5),
('Ropa y Moda', 'Prendas de vestir y accesorios', NULL),
('Ropa Hombre', 'Moda masculina', 8),
('Ropa Mujer', 'Moda femenina', 8),
('Deportes', 'Artículos deportivos y fitness', NULL),
('Equipamiento Deportivo', 'Equipos y accesorios deportivos', 11),
('Libros', 'Libros físicos y digitales', NULL),
('Juguetes', 'Juguetes y juegos para niños', NULL),
('Salud y Belleza', 'Productos de cuidado personal', NULL);

-- Insertar productos
INSERT INTO productos (nombre, descripcion, id_categoria, precio, precio_oferta, stock, peso_kg) VALUES
-- Electrónica
('Portátil Dell XPS 15', 'Portátil de alto rendimiento con pantalla 4K', 2, 1499.99, 1299.99, 15, 2.5),
('MacBook Air M2', 'Portátil ultraligero de Apple con chip M2', 2, 1399.99, NULL, 20, 1.2),
('iPhone 15 Pro', 'Smartphone de última generación con cámara profesional', 3, 1199.99, 1099.99, 30, 0.2),
('Samsung Galaxy S24', 'Smartphone Android flagship', 3, 999.99, 899.99, 25, 0.18),
('iPad Pro 12.9"', 'Tablet profesional de Apple', 3, 1299.99, NULL, 12, 0.68),
('Auriculares Sony WH-1000XM5', 'Auriculares con cancelación de ruido premium', 4, 399.99, 349.99, 40, 0.25),
('Teclado Mecánico Logitech', 'Teclado gaming RGB', 4, 129.99, 99.99, 50, 1.0),
('Ratón Inalámbrico Logitech MX Master 3', 'Ratón ergonómico profesional', 4, 99.99, NULL, 60, 0.14),
('Monitor LG 27" 4K', 'Monitor UHD para profesionales', 2, 449.99, 399.99, 18, 6.5),
('Webcam Logitech C920', 'Cámara web Full HD', 4, 79.99, 69.99, 35, 0.16),

-- Hogar y Cocina
('Robot Aspirador Roomba i7', 'Robot aspirador inteligente con mapeo', 6, 599.99, 499.99, 10, 3.5),
('Batidora KitchenAid', 'Batidora de pie profesional', 6, 449.99, NULL, 15, 10.0),
('Cafetera Nespresso', 'Cafetera de cápsulas automática', 6, 179.99, 149.99, 25, 4.0),
('Air Fryer Philips XXL', 'Freidora de aire de gran capacidad', 6, 249.99, 219.99, 20, 8.0),
('Set de Sartenes Tefal', 'Set de 3 sartenes antiadherentes', 5, 89.99, 69.99, 40, 3.0),
('Lámpara LED de Diseño', 'Lámpara de mesa moderna', 7, 59.99, NULL, 50, 1.5),
('Cojines Decorativos Set 4', 'Set de cojines de terciopelo', 7, 39.99, 29.99, 60, 1.0),
('Alfombra Moderna 160x230cm', 'Alfombra de salón contemporánea', 7, 149.99, 129.99, 15, 5.0),

-- Ropa y Moda
('Vaqueros Levi\'s 501', 'Vaqueros clásicos', 9, 89.99, NULL, 100, 0.6),
('Camiseta Nike Dri-FIT', 'Camiseta deportiva transpirable', 9, 29.99, 24.99, 150, 0.2),
('Zapatillas Adidas Ultraboost', 'Zapatillas running premium', 12, 179.99, 149.99, 45, 0.8),
('Chaqueta North Face', 'Chaqueta impermeable outdoor', 9, 199.99, 179.99, 30, 1.0),
('Vestido Zara Elegante', 'Vestido de fiesta', 10, 79.99, 59.99, 40, 0.4),
('Bolso Michael Kors', 'Bolso de mano de cuero', 10, 249.99, 199.99, 20, 0.8),
('Reloj Casio G-Shock', 'Reloj deportivo resistente', 8, 129.99, NULL, 35, 0.05),

-- Deportes
('Bicicleta de Montaña', 'MTB 29" con suspensión', 12, 899.99, 799.99, 8, 15.0),
('Mancuernas Ajustables 20kg', 'Set de mancuernas regulables', 12, 149.99, 129.99, 25, 20.0),
('Esterilla Yoga Premium', 'Esterilla antideslizante 6mm', 12, 39.99, 29.99, 60, 1.2),
('Balón Fútbol Adidas', 'Balón oficial Champions League', 12, 49.99, 39.99, 50, 0.4),
('Cinta de Correr Plegable', 'Cinta running para casa', 12, 599.99, 499.99, 5, 45.0),

-- Libros
('Don Quijote de la Mancha', 'Clásico de la literatura española', 13, 19.99, NULL, 100, 1.2),
('Cien Años de Soledad', 'Obra maestra de García Márquez', 13, 17.99, NULL, 80, 0.8),
('Sapiens de Yuval Noah Harari', 'Bestseller sobre la historia humana', 13, 22.99, 18.99, 70, 0.9),
('El Principito', 'Cuento filosófico clásico', 13, 12.99, NULL, 150, 0.3),
('Libro de Cocina Mediterránea', 'Recetas tradicionales', 13, 24.99, 19.99, 40, 1.5),

-- Juguetes
('LEGO Star Wars Millennium Falcon', 'Set de construcción detallado', 14, 169.99, 149.99, 20, 2.0),
('Muñeca Barbie Dreamhouse', 'Casa de muñecas con accesorios', 14, 199.99, 179.99, 15, 5.0),
('Monopoly Edición España', 'Juego de mesa clásico', 14, 29.99, 24.99, 60, 1.0),
('Puzzle 1000 Piezas Paisaje', 'Puzzle de alta calidad', 14, 19.99, 14.99, 80, 0.8),
('Hot Wheels Pista de Carreras', 'Pista de coches con looping', 14, 49.99, 39.99, 30, 2.5),

-- Salud y Belleza
('Crema Facial Olay Regenerist', 'Crema antiarrugas', 15, 34.99, 29.99, 50, 0.05),
('Perfume Carolina Herrera', 'Fragancia femenina 100ml', 15, 89.99, 79.99, 40, 0.3),
('Set de Maquillaje Maybelline', 'Kit completo de maquillaje', 15, 59.99, 49.99, 35, 0.5),
('Cepillo Eléctrico Oral-B', 'Cepillo dental recargable', 15, 79.99, 69.99, 45, 0.2),
('Báscula Inteligente Xiaomi', 'Báscula con análisis corporal', 15, 29.99, 24.99, 55, 1.5);

-- Insertar clientes
INSERT INTO clientes (nombre, apellidos, email, telefono) VALUES
('Carlos', 'García Fernández', 'carlos.garcia@email.com', '612345678'),
('María', 'López Martínez', 'maria.lopez@email.com', '623456789'),
('Juan', 'Rodríguez Sánchez', 'juan.rodriguez@email.com', '634567890'),
('Ana', 'Martínez González', 'ana.martinez@email.com', '645678901'),
('Pedro', 'Hernández Pérez', 'pedro.hernandez@email.com', '656789012'),
('Laura', 'González Ruiz', 'laura.gonzalez@email.com', '667890123'),
('David', 'Díaz Moreno', 'david.diaz@email.com', '678901234'),
('Carmen', 'Muñoz Romero', 'carmen.munoz@email.com', '689012345'),
('Miguel', 'Álvarez Jiménez', 'miguel.alvarez@email.com', '690123456'),
('Isabel', 'Torres Navarro', 'isabel.torres@email.com', '601234567'),
('Francisco', 'Ramírez Molina', 'francisco.ramirez@email.com', '612345679'),
('Patricia', 'Sánchez Ortega', 'patricia.sanchez@email.com', '623456780'),
('Antonio', 'Jiménez Castro', 'antonio.jimenez@email.com', '634567891'),
('Lucía', 'Ruiz Serrano', 'lucia.ruiz@email.com', '645678902'),
('José', 'Moreno Gil', 'jose.moreno@email.com', '656789013');

-- Insertar direcciones de envío
INSERT INTO direcciones_envio (id_cliente, nombre_destinatario, direccion, ciudad, provincia, codigo_postal, telefono, es_predeterminada) VALUES
(1, 'Carlos García Fernández', 'Calle Mayor 25, 3ºB', 'Madrid', 'Madrid', '28001', '612345678', TRUE),
(2, 'María López Martínez', 'Avenida Diagonal 120', 'Barcelona', 'Barcelona', '08015', '623456789', TRUE),
(3, 'Juan Rodríguez Sánchez', 'Calle Sierpes 45', 'Sevilla', 'Sevilla', '41004', '634567890', TRUE),
(4, 'Ana Martínez González', 'Gran Vía 88, 2ºA', 'Valencia', 'Valencia', '46005', '645678901', TRUE),
(5, 'Pedro Hernández Pérez', 'Rambla Nova 50', 'Tarragona', 'Tarragona', '43001', '656789012', TRUE),
(6, 'Laura González Ruiz', 'Calle Alcalá 200, 5ºC', 'Madrid', 'Madrid', '28028', '667890123', TRUE),
(7, 'David Díaz Moreno', 'Paseo de Gracia 75', 'Barcelona', 'Barcelona', '08008', '678901234', TRUE),
(8, 'Carmen Muñoz Romero', 'Avenida Constitución 15', 'Málaga', 'Málaga', '29001', '689012345', TRUE),
(9, 'Miguel Álvarez Jiménez', 'Calle Colón 30', 'Valencia', 'Valencia', '46004', '690123456', TRUE),
(10, 'Isabel Torres Navarro', 'Plaza España 10', 'Zaragoza', 'Zaragoza', '50001', '601234567', TRUE),
(1, 'Carlos García (Oficina)', 'Calle Serrano 100, Oficina 5', 'Madrid', 'Madrid', '28006', '612345678', FALSE),
(2, 'María López (Casa)', 'Calle Aragón 234, Ático', 'Barcelona', 'Barcelona', '08011', '623456789', FALSE),
(11, 'Francisco Ramírez Molina', 'Calle Real 67', 'La Coruña', 'La Coruña', '15001', '612345679', TRUE),
(12, 'Patricia Sánchez Ortega', 'Avenida Libertad 42', 'Bilbao', 'Vizcaya', '48001', '623456780', TRUE),
(13, 'Antonio Jiménez Castro', 'Calle Mayor 155', 'Murcia', 'Murcia', '30001', '634567891', TRUE);

-- Insertar métodos de pago
INSERT INTO metodos_pago (nombre, descripcion) VALUES
('Tarjeta de Crédito', 'Pago con tarjeta Visa, Mastercard o American Express'),
('Tarjeta de Débito', 'Pago con tarjeta de débito'),
('PayPal', 'Pago a través de cuenta PayPal'),
('Transferencia Bancaria', 'Transferencia bancaria directa'),
('Contra Reembolso', 'Pago en efectivo al recibir el pedido'),
('Bizum', 'Pago instantáneo con Bizum');

-- Insertar pedidos
INSERT INTO pedidos (id_cliente, id_direccion_envio, id_metodo_pago, fecha_pedido, estado, subtotal, gastos_envio, impuestos, total) VALUES
(1, 1, 1, '2024-10-01 10:30:00', 'entregado', 1299.99, 0.00, 273.00, 1572.99),
(2, 2, 3, '2024-10-02 14:15:00', 'entregado', 449.99, 15.00, 97.65, 562.64),
(3, 3, 2, '2024-10-03 09:20:00', 'entregado', 179.99, 5.00, 38.85, 223.84),
(4, 4, 1, '2024-10-05 16:45:00', 'enviado', 999.99, 0.00, 210.00, 1209.99),
(5, 5, 4, '2024-10-07 11:00:00', 'procesando', 899.99, 25.00, 194.25, 1119.24),
(6, 6, 1, '2024-10-08 13:30:00', 'entregado', 349.99, 5.00, 74.55, 429.54),
(7, 7, 3, '2024-10-10 10:15:00', 'entregado', 89.99, 3.00, 19.53, 112.52),
(8, 8, 2, '2024-10-12 15:20:00', 'entregado', 599.99, 0.00, 126.00, 725.99),
(9, 9, 1, '2024-10-14 12:00:00', 'enviado', 249.99, 5.00, 53.55, 308.54),
(10, 10, 5, '2024-10-15 09:30:00', 'procesando', 149.99, 10.00, 33.60, 193.59),
(1, 11, 1, '2024-10-18 14:45:00', 'entregado', 99.99, 3.00, 21.63, 124.62),
(2, 2, 6, '2024-10-20 11:20:00', 'entregado', 199.99, 5.00, 43.05, 248.04),
(3, 3, 1, '2024-10-22 16:10:00', 'enviado', 79.99, 3.00, 17.43, 100.42),
(4, 4, 3, '2024-10-24 10:00:00', 'procesando', 1499.99, 0.00, 315.00, 1814.99),
(5, 5, 2, '2024-10-25 13:15:00', 'pendiente', 499.99, 15.00, 108.15, 623.14),
(6, 6, 1, '2024-10-26 15:30:00', 'entregado', 129.99, 3.00, 27.93, 160.92),
(7, 7, 1, '2024-10-27 09:45:00', 'entregado', 399.99, 0.00, 84.00, 483.99),
(8, 8, 3, '2024-10-28 12:20:00', 'enviado', 169.99, 5.00, 36.75, 211.74),
(11, 13, 1, '2024-10-29 14:00:00', 'procesando', 299.99, 10.00, 65.10, 375.09),
(12, 14, 2, '2024-10-30 10:30:00', 'pendiente', 89.99, 5.00, 19.95, 114.94);

-- Insertar detalles de pedidos
INSERT INTO detalle_pedidos (id_pedido, id_producto, cantidad, precio_unitario, subtotal) VALUES
-- Pedido 1
(1, 1, 1, 1299.99, 1299.99),
-- Pedido 2
(2, 9, 1, 399.99, 399.99),
(2, 16, 1, 59.99, 50.00),
-- Pedido 3
(3, 21, 2, 89.99, 179.98),
-- Pedido 4
(4, 4, 1, 899.99, 899.99),
(4, 7, 1, 99.99, 99.99),
-- Pedido 5
(5, 26, 1, 799.99, 799.99),
(5, 27, 1, 129.99, 100.00),
-- Pedido 6
(6, 6, 1, 349.99, 349.99),
-- Pedido 7
(7, 19, 1, 89.99, 89.99),
-- Pedido 8
(8, 11, 1, 499.99, 499.99),
(8, 13, 1, 149.99, 100.00),
-- Pedido 9
(9, 14, 1, 219.99, 219.99),
(9, 20, 1, 24.99, 30.00),
-- Pedido 10
(10, 21, 1, 149.99, 149.99),
-- Pedido 11
(11, 8, 1, 99.99, 99.99),
-- Pedido 12
(12, 24, 1, 199.99, 199.99),
-- Pedido 13
(13, 10, 1, 69.99, 69.99),
(13, 44, 1, 29.99, 10.00),
-- Pedido 14
(14, 1, 1, 1299.99, 1299.99),
(14, 8, 2, 99.99, 199.99),
-- Pedido 15
(15, 11, 1, 499.99, 499.99),
-- Pedido 16
(16, 7, 1, 99.99, 99.99),
(16, 28, 1, 29.99, 30.00),
-- Pedido 17
(17, 6, 1, 399.99, 399.99),
-- Pedido 18
(18, 36, 1, 149.99, 149.99),
(18, 34, 1, 18.99, 20.00),
-- Pedido 19
(19, 27, 1, 129.99, 129.99),
(19, 37, 2, 79.99, 169.99),
-- Pedido 20
(20, 15, 1, 69.99, 69.99),
(20, 17, 1, 29.99, 20.00);

-- Insertar valoraciones
INSERT INTO valoraciones (id_producto, id_cliente, puntuacion, comentario, fecha_valoracion) VALUES
(1, 1, 5, 'Excelente portátil, muy rápido y con pantalla espectacular', '2024-10-05 18:30:00'),
(9, 2, 4, 'Buen monitor, aunque el precio es algo elevado', '2024-10-10 12:15:00'),
(21, 3, 5, 'Las zapatillas más cómodas que he tenido', '2024-10-12 14:20:00'),
(4, 4, 5, 'Smartphone increíble, la cámara es profesional', '2024-10-15 10:45:00'),
(26, 5, 4, 'Buena bicicleta, solo le falta algún accesorio', '2024-10-18 16:00:00'),
(6, 6, 5, 'Los mejores auriculares con cancelación de ruido', '2024-10-20 09:30:00'),
(19, 7, 4, 'Vaqueros de calidad, aunque podrían ser más económicos', '2024-10-22 11:45:00'),
(11, 8, 5, 'El robot aspirador funciona de maravilla, muy recomendado', '2024-10-24 13:20:00'),
(14, 9, 5, 'La freidora de aire es lo mejor que he comprado', '2024-10-26 15:00:00'),
(21, 10, 5, 'Súper cómodas y con estilo', '2024-10-28 10:30:00'),
(8, 1, 5, 'Ratón ergonómico perfecto para trabajar todo el día', '2024-10-29 12:00:00'),
(24, 2, 4, 'Bonito bolso, la calidad del cuero es buena', '2024-10-30 14:15:00'),
(10, 3, 3, 'Funciona bien pero esperaba mejor calidad de imagen', '2024-10-15 16:30:00'),
(13, 4, 5, 'Perfecta para hacer café por las mañanas', '2024-10-17 09:00:00'),
(20, 5, 5, 'Camiseta muy cómoda y transpirable', '2024-10-19 11:20:00'),
(27, 6, 4, 'Buenas mancuernas, ajuste fácil', '2024-10-21 13:40:00'),
(6, 7, 5, 'Cancelación de ruido espectacular', '2024-10-23 15:50:00'),
(36, 8, 5, 'Set de LEGO increíble, muchas horas de diversión', '2024-10-25 10:10:00'),
(34, 9, 5, 'Libro fascinante, lo recomiendo totalmente', '2024-10-27 12:30:00'),
(1, 11, 5, 'Mejor compra del año, portátil espectacular', '2024-10-28 14:00:00'),
(7, 12, 4, 'Buen teclado mecánico, las teclas suenan bien', '2024-10-29 16:20:00'),
(15, 13, 3, 'El set de sartenes está bien pero se rayaron rápido', '2024-10-30 09:45:00'),
(12, 14, 5, 'Batidora potente y silenciosa', '2024-10-16 11:00:00'),
(22, 15, 4, 'Chaqueta resistente al agua, perfecta para montaña', '2024-10-18 13:15:00'),
(28, 1, 5, 'Esterilla de yoga de excelente calidad', '2024-10-20 15:30:00'),
(3, 2, 5, 'iPhone 15 Pro es una maravilla, la cámara es brutal', '2024-10-22 10:00:00'),
(5, 3, 4, 'iPad potente aunque algo caro', '2024-10-24 12:20:00'),
(16, 4, 5, 'Lámpara bonita y con buena luz', '2024-10-26 14:40:00'),
(17, 5, 4, 'Cojines suaves y decorativos', '2024-10-28 16:50:00'),
(25, 6, 5, 'Reloj resistente y con muchas funciones', '2024-10-29 09:10:00'),
(30, 7, 5, 'El mejor libro que he leído este año', '2024-10-30 11:30:00'),
(31, 8, 5, 'Cien años de soledad es una obra maestra', '2024-10-14 13:45:00'),
(32, 9, 4, 'Sapiens te hace pensar, muy interesante', '2024-10-16 15:55:00'),
(33, 10, 5, 'El Principito nunca pasa de moda', '2024-10-18 10:15:00'),
(37, 11, 5, 'Casa de muñecas completa, a mi hija le encanta', '2024-10-20 12:35:00'),
(38, 12, 4, 'Monopoly clásico, perfecto para la familia', '2024-10-22 14:50:00'),
(41, 13, 5, 'Crema facial efectiva, se nota la diferencia', '2024-10-24 16:05:00'),
(42, 14, 4, 'Perfume con buen olor y duradero', '2024-10-26 09:20:00'),
(43, 15, 5, 'Set de maquillaje completo y de calidad', '2024-10-28 11:40:00'),
(44, 1, 5, 'Cepillo eléctrico excelente, limpieza profunda', '2024-10-29 13:55:00'),
(45, 2, 4, 'Báscula precisa y con muchas métricas', '2024-10-30 15:10:00'),
(29, 3, 3, 'El balón está bien pero se desinfla un poco rápido', '2024-10-17 10:25:00'),
(35, 4, 5, 'Recetas deliciosas y fáciles de seguir', '2024-10-19 12:40:00'),
(39, 5, 4, 'Puzzle entretenido, buena calidad de imagen', '2024-10-21 14:55:00'),
(40, 6, 5, 'Pista de Hot Wheels muy divertida', '2024-10-23 16:10:00'),
(18, 7, 4, 'Alfombra bonita y suave', '2024-10-25 09:25:00'),
(23, 8, 5, 'Vestido elegante y favorecedor', '2024-10-27 11:45:00'),
(2, 9, 5, 'MacBook Air M2 es rápido y ligero, perfecto', '2024-10-29 14:00:00'),
(4, 10, 5, 'Samsung Galaxy S24 tiene una pantalla increíble', '2024-10-30 16:15:00');

-- ============================================
-- PROCEDIMIENTOS ALMACENADOS
-- ============================================

DELIMITER //

-- Procedimiento: Obtener resumen de ventas por periodo
CREATE PROCEDURE sp_resumen_ventas_periodo(
    IN fecha_inicio DATE,
    IN fecha_fin DATE
)
BEGIN
    SELECT 
        DATE(fecha_pedido) AS fecha,
        COUNT(id_pedido) AS total_pedidos,
        SUM(total) AS ingresos_totales,
        AVG(total) AS ticket_medio,
        COUNT(DISTINCT id_cliente) AS clientes_unicos
    FROM pedidos
    WHERE DATE(fecha_pedido) BETWEEN fecha_inicio AND fecha_fin
    GROUP BY DATE(fecha_pedido)
    ORDER BY fecha DESC;
END //

-- Procedimiento: Top productos por categoría
CREATE PROCEDURE sp_top_productos_categoria(
    IN id_cat INT,
    IN limite INT
)
BEGIN
    SELECT 
        p.id_producto,
        p.nombre,
        p.precio,
        COALESCE(SUM(dp.cantidad), 0) AS unidades_vendidas,
        COALESCE(AVG(v.puntuacion), 0) AS valoracion_media
    FROM productos p
    LEFT JOIN detalle_pedidos dp ON p.id_producto = dp.id_producto
    LEFT JOIN valoraciones v ON p.id_producto = v.id_producto
    WHERE p.id_categoria = id_cat AND p.activo = TRUE
    GROUP BY p.id_producto, p.nombre, p.precio
    ORDER BY unidades_vendidas DESC
    LIMIT limite;
END //

-- Procedimiento: Historial de compras de cliente
CREATE PROCEDURE sp_historial_cliente(
    IN cliente_id INT
)
BEGIN
    SELECT 
        p.id_pedido,
        p.fecha_pedido,
        p.estado,
        p.total,
        COUNT(dp.id_detalle) AS num_productos,
        GROUP_CONCAT(pr.nombre SEPARATOR ', ') AS productos
    FROM pedidos p
    JOIN detalle_pedidos dp ON p.id_pedido = dp.id_pedido
    JOIN productos pr ON dp.id_producto = pr.id_producto
    WHERE p.id_cliente = cliente_id
    GROUP BY p.id_pedido, p.fecha_pedido, p.estado, p.total
    ORDER BY p.fecha_pedido DESC;
END //

-- Procedimiento: Actualizar stock después de pedido
CREATE PROCEDURE sp_actualizar_stock_pedido(
    IN pedido_id INT
)
BEGIN
    UPDATE productos p
    JOIN detalle_pedidos dp ON p.id_producto = dp.id_producto
    SET p.stock = p.stock - dp.cantidad
    WHERE dp.id_pedido = pedido_id;
END //

-- Procedimiento: Productos con stock bajo
CREATE PROCEDURE sp_productos_stock_bajo(
    IN umbral INT
)
BEGIN
    SELECT 
        p.id_producto,
        p.nombre,
        c.nombre AS categoria,
        p.stock,
        p.precio
    FROM productos p
    JOIN categorias c ON p.id_categoria = c.id_categoria
    WHERE p.stock <= umbral AND p.activo = TRUE
    ORDER BY p.stock ASC;
END //

DELIMITER ;

-- ============================================
-- TRIGGERS
-- ============================================

DELIMITER //

-- Trigger: Calcular subtotal en detalle_pedidos antes de insertar
CREATE TRIGGER trg_calcular_subtotal_detalle
BEFORE INSERT ON detalle_pedidos
FOR EACH ROW
BEGIN
    SET NEW.subtotal = NEW.cantidad * NEW.precio_unitario;
END //

-- Trigger: Actualizar stock al insertar detalle de pedido
CREATE TRIGGER trg_reducir_stock_detalle
AFTER INSERT ON detalle_pedidos
FOR EACH ROW
BEGIN
    UPDATE productos
    SET stock = stock - NEW.cantidad
    WHERE id_producto = NEW.id_producto;
END //

-- Trigger: Validar stock disponible antes de insertar detalle
CREATE TRIGGER trg_validar_stock_antes_venta
BEFORE INSERT ON detalle_pedidos
FOR EACH ROW
BEGIN
    DECLARE stock_actual INT;
    
    SELECT stock INTO stock_actual
    FROM productos
    WHERE id_producto = NEW.id_producto;
    
    IF stock_actual < NEW.cantidad THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Stock insuficiente para completar la venta';
    END IF;
END //

-- Trigger: Registrar fecha de última modificación en productos
CREATE TRIGGER trg_actualizar_fecha_modificacion_producto
BEFORE UPDATE ON productos
FOR EACH ROW
BEGIN
    SET NEW.fecha_creacion = OLD.fecha_creacion;
END //

DELIMITER ;

-- ============================================
-- FUNCIONES
-- ============================================

DELIMITER //

-- Función: Calcular total de pedido con impuestos
CREATE FUNCTION fn_calcular_total_pedido(
    subtotal DECIMAL(10,2),
    gastos_envio DECIMAL(10,2),
    tipo_iva DECIMAL(4,2)
)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE impuestos DECIMAL(10,2);
    DECLARE total DECIMAL(10,2);
    
    SET impuestos = subtotal * tipo_iva;
    SET total = subtotal + gastos_envio + impuestos;
    
    RETURN total;
END //

-- Función: Obtener número de pedidos de un cliente
CREATE FUNCTION fn_total_pedidos_cliente(cliente_id INT)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE total INT;
    
    SELECT COUNT(*) INTO total
    FROM pedidos
    WHERE id_cliente = cliente_id;
    
    RETURN total;
END //

-- Función: Calcular valoración media de producto
CREATE FUNCTION fn_valoracion_media_producto(producto_id INT)
RETURNS DECIMAL(3,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE media DECIMAL(3,2);
    
    SELECT COALESCE(AVG(puntuacion), 0) INTO media
    FROM valoraciones
    WHERE id_producto = producto_id;
    
    RETURN media;
END //

DELIMITER ;

-- ============================================
-- ÍNDICES ADICIONALES PARA OPTIMIZACIÓN
-- ============================================

CREATE INDEX idx_productos_precio_stock ON productos(precio, stock);
CREATE INDEX idx_pedidos_fecha_estado ON pedidos(fecha_pedido, estado);
CREATE INDEX idx_valoraciones_producto_puntuacion ON valoraciones(id_producto, puntuacion);

-- ============================================
-- CONSULTAS DE EJEMPLO ÚTILES
-- ============================================

-- Ver todos los pedidos con información del cliente
-- SELECT * FROM vista_detalle_pedidos_completo;

-- Ver productos más vendidos
-- SELECT * FROM vista_productos_mas_vendidos LIMIT 10;

-- Ver resumen de compras por cliente
-- SELECT * FROM vista_pedidos_cliente ORDER BY total_gastado DESC;

-- Ver estado del inventario
-- SELECT * FROM vista_inventario WHERE estado_stock = 'Stock bajo';

-- Obtener ventas del último mes
-- CALL sp_resumen_ventas_periodo('2024-10-01', '2024-10-31');

-- Ver productos con stock bajo (menos de 20 unidades)
-- CALL sp_productos_stock_bajo(20);

-- Ver historial de compras de un cliente específico
-- CALL sp_historial_cliente(1);

-- Top 5 productos de una categoría
-- CALL sp_top_productos_categoria(1, 5);

-- ============================================
-- FIN DEL SCRIPT
-- ============================================
