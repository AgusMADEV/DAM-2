-- =============================================
-- SISTEMA ERP - TIENDA ONLINE DE CAMISETAS DE FÚTBOL
-- Base de datos para gestión de camisetas de equipos y selecciones
-- =============================================

CREATE DATABASE IF NOT EXISTS tienda_camisetas 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE tienda_camisetas;

-- Eliminar tablas si existen (en orden inverso de dependencias)
DROP TABLE IF EXISTS articulos_pedido;
DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS resenas_producto;
DROP TABLE IF EXISTS imagenes_producto;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS equipos;
DROP TABLE IF EXISTS ligas;
DROP TABLE IF EXISTS marcas;
DROP TABLE IF EXISTS tipos_camiseta;
DROP TABLE IF EXISTS tallas;
DROP TABLE IF EXISTS temporadas;
DROP TABLE IF EXISTS metodos_pago;
DROP TABLE IF EXISTS metodos_envio;
DROP TABLE IF EXISTS direcciones;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS paises;
DROP TABLE IF EXISTS estados_pedido;

-- =============================================
-- TABLAS DE REFERENCIA
-- =============================================

-- Tabla de países
CREATE TABLE paises (
    id_pais INT PRIMARY KEY AUTO_INCREMENT,
    nombre_pais VARCHAR(100) NOT NULL UNIQUE,
    codigo_pais CHAR(2) NOT NULL UNIQUE
);

-- Estados de pedido
CREATE TABLE estados_pedido (
    id_estado INT PRIMARY KEY AUTO_INCREMENT,
    nombre_estado VARCHAR(50) NOT NULL UNIQUE,
    descripcion_estado VARCHAR(255)
);

-- Temporadas (2023/24, 2024/25, etc.)
CREATE TABLE temporadas (
    id_temporada INT PRIMARY KEY AUTO_INCREMENT,
    nombre_temporada VARCHAR(20) NOT NULL UNIQUE,
    ano_inicio INT NOT NULL,
    ano_fin INT NOT NULL,
    activo TINYINT(1) DEFAULT 1
);

-- Tallas disponibles
CREATE TABLE tallas (
    id_talla INT PRIMARY KEY AUTO_INCREMENT,
    nombre_talla VARCHAR(10) NOT NULL UNIQUE,
    orden INT DEFAULT 0
);

-- Tipos de camiseta (titular, suplente, tercera, etc.)
CREATE TABLE tipos_camiseta (
    id_tipo_camiseta INT PRIMARY KEY AUTO_INCREMENT,
    nombre_tipo VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(255)
);

-- Ligas y competiciones
CREATE TABLE ligas (
    id_liga INT PRIMARY KEY AUTO_INCREMENT,
    nombre_liga VARCHAR(100) NOT NULL UNIQUE,
    id_pais INT,
    nivel VARCHAR(50),
    activo TINYINT(1) DEFAULT 1,
    FOREIGN KEY (id_pais) REFERENCES paises(id_pais)
);

-- =============================================
-- TABLAS DE PRODUCTOS
-- =============================================

-- Marcas de camisetas
CREATE TABLE marcas (
    id_marca INT PRIMARY KEY AUTO_INCREMENT,
    nombre_marca VARCHAR(100) NOT NULL UNIQUE,
    pais_origen VARCHAR(100),
    sitio_web VARCHAR(255),
    activo TINYINT(1) DEFAULT 1
);

-- Equipos de fútbol
CREATE TABLE equipos (
    id_equipo INT PRIMARY KEY AUTO_INCREMENT,
    nombre_equipo VARCHAR(100) NOT NULL UNIQUE,
    nombre_completo VARCHAR(200),
    id_liga INT,
    id_pais INT,
    fundacion INT,
    estadio VARCHAR(100),
    es_seleccion TINYINT(1) DEFAULT 0,
    activo TINYINT(1) DEFAULT 1,
    FOREIGN KEY (id_liga) REFERENCES ligas(id_liga),
    FOREIGN KEY (id_pais) REFERENCES paises(id_pais)
);

-- Productos (camisetas)
CREATE TABLE productos (
    id_producto INT PRIMARY KEY AUTO_INCREMENT,
    nombre_producto VARCHAR(200) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0,
    id_equipo INT NOT NULL,
    id_marca INT NOT NULL,
    id_temporada INT NOT NULL,
    id_tipo_camiseta INT NOT NULL,
    id_talla INT NOT NULL,
    
    -- Campos específicos para camisetas
    jugador VARCHAR(100) COMMENT 'Nombre del jugador (opcional)',
    numero_dorsal INT COMMENT 'Número de dorsal (opcional)',
    version_jugador TINYINT(1) DEFAULT 0 COMMENT 'Si es versión de jugador o aficionado',
    manga_corta TINYINT(1) DEFAULT 1,
    incluye_parches TINYINT(1) DEFAULT 0 COMMENT 'Parches de competiciones',
    
    -- Campos generales
    material VARCHAR(100) DEFAULT 'Poliéster',
    codigo_producto VARCHAR(50) UNIQUE,
    peso INT COMMENT 'Peso en gramos',
    fecha_lanzamiento DATE,
    destacado TINYINT(1) DEFAULT 0,
    activo TINYINT(1) DEFAULT 1,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_equipo) REFERENCES equipos(id_equipo),
    FOREIGN KEY (id_marca) REFERENCES marcas(id_marca),
    FOREIGN KEY (id_temporada) REFERENCES temporadas(id_temporada),
    FOREIGN KEY (id_tipo_camiseta) REFERENCES tipos_camiseta(id_tipo_camiseta),
    FOREIGN KEY (id_talla) REFERENCES tallas(id_talla)
);

-- Imágenes de productos
CREATE TABLE imagenes_producto (
    id_imagen INT PRIMARY KEY AUTO_INCREMENT,
    id_producto INT NOT NULL,
    url_imagen VARCHAR(255) NOT NULL,
    es_principal TINYINT(1) DEFAULT 0,
    orden INT DEFAULT 0,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto) ON DELETE CASCADE
);

-- Reseñas de productos
CREATE TABLE resenas_producto (
    id_resena INT PRIMARY KEY AUTO_INCREMENT,
    id_producto INT NOT NULL,
    id_cliente INT,
    calificacion INT NOT NULL CHECK (calificacion BETWEEN 1 AND 5),
    titulo VARCHAR(200),
    comentario TEXT,
    fecha_resena TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verificado TINYINT(1) DEFAULT 0,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto) ON DELETE CASCADE
);

-- =============================================
-- TABLAS DE CLIENTES
-- =============================================

-- Clientes
CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    equipo_favorito INT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo TINYINT(1) DEFAULT 1,
    FOREIGN KEY (equipo_favorito) REFERENCES equipos(id_equipo)
);

-- Direcciones de clientes
CREATE TABLE direcciones (
    id_direccion INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT NOT NULL,
    direccion_linea1 VARCHAR(255) NOT NULL,
    direccion_linea2 VARCHAR(255),
    ciudad VARCHAR(100) NOT NULL,
    codigo_postal VARCHAR(20) NOT NULL,
    id_pais INT NOT NULL,
    es_principal TINYINT(1) DEFAULT 0,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    FOREIGN KEY (id_pais) REFERENCES paises(id_pais)
);

-- =============================================
-- TABLAS DE PEDIDOS
-- =============================================

-- Métodos de envío
CREATE TABLE metodos_envio (
    id_metodo_envio INT PRIMARY KEY AUTO_INCREMENT,
    nombre_metodo VARCHAR(100) NOT NULL UNIQUE,
    costo DECIMAL(10,2) NOT NULL,
    dias_estimados INT,
    activo TINYINT(1) DEFAULT 1
);

-- Métodos de pago
CREATE TABLE metodos_pago (
    id_metodo_pago INT PRIMARY KEY AUTO_INCREMENT,
    nombre_metodo VARCHAR(100) NOT NULL UNIQUE,
    activo TINYINT(1) DEFAULT 1
);

-- Pedidos
CREATE TABLE pedidos (
    id_pedido INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT NOT NULL,
    id_direccion INT NOT NULL,
    id_metodo_envio INT NOT NULL,
    id_metodo_pago INT NOT NULL,
    id_estado INT NOT NULL,
    fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    subtotal DECIMAL(10,2) NOT NULL,
    costo_envio DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    notas TEXT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_direccion) REFERENCES direcciones(id_direccion),
    FOREIGN KEY (id_metodo_envio) REFERENCES metodos_envio(id_metodo_envio),
    FOREIGN KEY (id_metodo_pago) REFERENCES metodos_pago(id_metodo_pago),
    FOREIGN KEY (id_estado) REFERENCES estados_pedido(id_estado)
);

-- Artículos del pedido
CREATE TABLE articulos_pedido (
    id_articulo_pedido INT PRIMARY KEY AUTO_INCREMENT,
    id_pedido INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- =============================================
-- DATOS INICIALES
-- =============================================

-- Países
INSERT INTO paises (nombre_pais, codigo_pais) VALUES
('España', 'ES'),
('Inglaterra', 'GB'),
('Italia', 'IT'),
('Alemania', 'DE'),
('Francia', 'FR'),
('Brasil', 'BR'),
('Argentina', 'AR'),
('Portugal', 'PT'),
('Países Bajos', 'NL'),
('Bélgica', 'BE');

-- Estados de pedido
INSERT INTO estados_pedido (nombre_estado, descripcion_estado) VALUES
('Pendiente', 'Pedido recibido, pendiente de procesar'),
('Procesando', 'Pedido en preparación'),
('Enviado', 'Pedido enviado al cliente'),
('Entregado', 'Pedido entregado'),
('Cancelado', 'Pedido cancelado');

-- Temporadas
INSERT INTO temporadas (nombre_temporada, ano_inicio, ano_fin, activo) VALUES
('2022/23', 2022, 2023, 0),
('2023/24', 2023, 2024, 0),
('2024/25', 2024, 2025, 1),
('2025/26', 2025, 2026, 1),
('2026/27', 2026, 2027, 0);

-- Tallas
INSERT INTO tallas (nombre_talla, orden) VALUES
('XS', 1),
('S', 2),
('M', 3),
('L', 4),
('XL', 5),
('XXL', 6);

-- Tipos de camiseta
INSERT INTO tipos_camiseta (nombre_tipo, descripcion) VALUES
('Primera Equipación', 'Camiseta titular del equipo'),
('Segunda Equipación', 'Camiseta suplente'),
('Tercera Equipación', 'Camiseta alternativa'),
('Portero', 'Camiseta de guardameta'),
('Edición Especial', 'Camisetas conmemorativas o especiales'),
('Entrenamiento', 'Camiseta de entrenamiento');

-- Ligas
INSERT INTO ligas (nombre_liga, id_pais, nivel, activo) VALUES
('LaLiga EA Sports', 1, 'Primera División', 1),
('Premier League', 2, 'Primera División', 1),
('Serie A', 3, 'Primera División', 1),
('Bundesliga', 4, 'Primera División', 1),
('Ligue 1', 5, 'Primera División', 1),
('UEFA Champions League', NULL, 'Competición Europea', 1),
('Copa del Mundo FIFA', NULL, 'Competición Internacional', 1);

-- Marcas
INSERT INTO marcas (nombre_marca, pais_origen, sitio_web, activo) VALUES
('Nike', 'Estados Unidos', 'www.nike.com', 1),
('Adidas', 'Alemania', 'www.adidas.com', 1),
('Puma', 'Alemania', 'www.puma.com', 1),
('New Balance', 'Estados Unidos', 'www.newbalance.com', 1),
('Umbro', 'Inglaterra', 'www.umbro.com', 1),
('Kappa', 'Italia', 'www.kappa.com', 1),
('Macron', 'Italia', 'www.macron.com', 1),
('Joma', 'España', 'www.joma-sport.com', 1);

-- Equipos
INSERT INTO equipos (nombre_equipo, nombre_completo, id_liga, id_pais, fundacion, estadio, es_seleccion, activo) VALUES
('Real Madrid', 'Real Madrid Club de Fútbol', 1, 1, 1902, 'Santiago Bernabéu', 0, 1),
('FC Barcelona', 'Fútbol Club Barcelona', 1, 1, 1899, 'Spotify Camp Nou', 0, 1),
('Atlético Madrid', 'Club Atlético de Madrid', 1, 1, 1903, 'Cívitas Metropolitano', 0, 1),
('Manchester United', 'Manchester United Football Club', 2, 2, 1878, 'Old Trafford', 0, 1),
('Liverpool FC', 'Liverpool Football Club', 2, 2, 1892, 'Anfield', 0, 1),
('Manchester City', 'Manchester City Football Club', 2, 2, 1880, 'Etihad Stadium', 0, 1),
('AC Milan', 'Associazione Calcio Milan', 3, 3, 1899, 'San Siro', 0, 1),
('Inter Milan', 'Football Club Internazionale Milano', 3, 3, 1908, 'San Siro', 0, 1),
('Juventus', 'Juventus Football Club', 3, 3, 1897, 'Allianz Stadium', 0, 1),
('Bayern München', 'Fußball-Club Bayern München', 4, 4, 1900, 'Allianz Arena', 0, 1),
('Borussia Dortmund', 'Ballspielverein Borussia 09 Dortmund', 4, 4, 1909, 'Signal Iduna Park', 0, 1),
('Paris Saint-Germain', 'Paris Saint-Germain Football Club', 5, 5, 1970, 'Parc des Princes', 0, 1),
('España', 'Selección Española de Fútbol', 7, 1, 1913, NULL, 1, 1),
('Brasil', 'Seleção Brasileira de Futebol', 7, 6, 1914, NULL, 1, 1),
('Argentina', 'Selección Argentina de Fútbol', 7, 7, 1893, NULL, 1, 1),
('Portugal', 'Seleção Portuguesa de Futebol', 7, 8, 1914, NULL, 1, 1);

-- Productos de ejemplo (camisetas)
INSERT INTO productos (nombre_producto, descripcion, precio, stock, id_equipo, id_marca, id_temporada, id_tipo_camiseta, id_talla, jugador, numero_dorsal, version_jugador, manga_corta, incluye_parches, material, codigo_producto, peso, fecha_lanzamiento, destacado, activo) VALUES
('Camiseta Real Madrid 2024/25 Titular', 'Camiseta oficial primera equipación Real Madrid temporada 2024/25', 89.99, 50, 1, 2, 4, 1, 3, NULL, NULL, 0, 1, 0, 'Poliéster reciclado', 'RM-2425-H-M', 180, '2024-07-01', 1, 1),
('Camiseta Real Madrid 2024/25 Bellingham #5', 'Camiseta oficial Real Madrid con nombre y número de Jude Bellingham', 119.99, 30, 1, 2, 4, 1, 3, 'BELLINGHAM', 5, 1, 1, 1, 'Poliéster reciclado', 'RM-2425-H-M-B5', 180, '2024-07-01', 1, 1),
('Camiseta FC Barcelona 2024/25 Titular', 'Camiseta oficial primera equipación FC Barcelona temporada 2024/25', 89.99, 45, 2, 1, 4, 1, 3, NULL, NULL, 0, 1, 0, 'Poliéster reciclado', 'FCB-2425-H-M', 175, '2024-07-01', 1, 1),
('Camiseta Barcelona 2024/25 Lewandowski #9', 'Camiseta oficial FC Barcelona con nombre y número de Robert Lewandowski', 119.99, 25, 2, 1, 4, 1, 3, 'LEWANDOWSKI', 9, 1, 1, 1, 'Poliéster reciclado', 'FCB-2425-H-M-L9', 175, '2024-07-01', 1, 1),
('Camiseta Manchester United 2024/25 Titular', 'Camiseta oficial primera equipación Manchester United', 84.99, 40, 4, 2, 4, 1, 3, NULL, NULL, 0, 1, 0, 'Poliéster Dri-FIT', 'MU-2425-H-M', 185, '2024-07-15', 1, 1),
('Camiseta Liverpool 2024/25 Titular', 'Camiseta oficial primera equipación Liverpool FC', 84.99, 38, 5, 1, 4, 1, 3, NULL, NULL, 0, 1, 0, 'Poliéster', 'LFC-2425-H-M', 180, '2024-07-01', 1, 1),
('Camiseta PSG 2024/25 Mbappé #7', 'Camiseta oficial PSG con nombre y número de Kylian Mbappé', 124.99, 20, 12, 1, 4, 1, 3, 'MBAPPÉ', 7, 1, 1, 1, 'Poliéster', 'PSG-2425-H-M-M7', 180, '2024-07-01', 1, 1),
('Camiseta Bayern München 2024/25 Titular', 'Camiseta oficial primera equipación Bayern München', 89.99, 35, 10, 2, 4, 1, 3, NULL, NULL, 0, 1, 0, 'Poliéster', 'BAY-2425-H-M', 182, '2024-07-10', 0, 1);

-- Más tallas para algunos productos populares
INSERT INTO productos (nombre_producto, descripcion, precio, stock, id_equipo, id_marca, id_temporada, id_tipo_camiseta, id_talla, jugador, numero_dorsal, version_jugador, manga_corta, incluye_parches, material, codigo_producto, peso, fecha_lanzamiento, destacado, activo) VALUES
('Camiseta Real Madrid 2024/25 Titular', 'Camiseta oficial primera equipación Real Madrid temporada 2024/25 - Talla S', 89.99, 45, 1, 2, 4, 1, 2, NULL, NULL, 0, 1, 0, 'Poliéster reciclado', 'RM-2425-H-S', 180, '2024-07-01', 1, 1),
('Camiseta Real Madrid 2024/25 Titular', 'Camiseta oficial primera equipación Real Madrid temporada 2024/25 - Talla L', 89.99, 55, 1, 2, 4, 1, 4, NULL, NULL, 0, 1, 0, 'Poliéster reciclado', 'RM-2425-H-L', 180, '2024-07-01', 1, 1),
('Camiseta FC Barcelona 2024/25 Titular', 'Camiseta oficial primera equipación FC Barcelona temporada 2024/25 - Talla S', 89.99, 40, 2, 1, 4, 1, 2, NULL, NULL, 0, 1, 0, 'Poliéster reciclado', 'FCB-2425-H-S', 175, '2024-07-01', 1, 1),
('Camiseta FC Barcelona 2024/25 Titular', 'Camiseta oficial primera equipación FC Barcelona temporada 2024/25 - Talla L', 89.99, 50, 2, 1, 4, 1, 4, NULL, NULL, 0, 1, 0, 'Poliéster reciclado', 'FCB-2425-H-L', 175, '2024-07-01', 1, 1);

-- Segundas equipaciones
INSERT INTO productos (nombre_producto, descripcion, precio, stock, id_equipo, id_marca, id_temporada, id_tipo_camiseta, id_talla, jugador, numero_dorsal, version_jugador, manga_corta, incluye_parches, material, codigo_producto, peso, fecha_lanzamiento, destacado, activo) VALUES
('Camiseta Real Madrid 2024/25 Segunda', 'Camiseta oficial segunda equipación Real Madrid', 89.99, 30, 1, 2, 4, 2, 3, NULL, NULL, 0, 1, 0, 'Poliéster reciclado', 'RM-2425-A-M', 180, '2024-08-01', 0, 1),
('Camiseta FC Barcelona 2024/25 Segunda', 'Camiseta oficial segunda equipación FC Barcelona', 89.99, 28, 2, 1, 4, 2, 3, NULL, NULL, 0, 1, 0, 'Poliéster reciclado', 'FCB-2425-A-M', 175, '2024-08-01', 0, 1);

-- Selecciones nacionales
INSERT INTO productos (nombre_producto, descripcion, precio, stock, id_equipo, id_marca, id_temporada, id_tipo_camiseta, id_talla, jugador, numero_dorsal, version_jugador, manga_corta, incluye_parches, material, codigo_producto, peso, fecha_lanzamiento, destacado, activo) VALUES
('Camiseta España 2024/25 Titular', 'Camiseta oficial selección española', 84.99, 60, 13, 2, 4, 1, 3, NULL, NULL, 0, 1, 0, 'Poliéster', 'ESP-2425-H-M', 178, '2024-06-01', 1, 1),
('Camiseta Brasil 2024/25 Titular', 'Camiseta oficial selección brasileña', 84.99, 55, 14, 1, 4, 1, 3, NULL, NULL, 0, 1, 0, 'Poliéster', 'BRA-2425-H-M', 178, '2024-06-01', 1, 1),
('Camiseta Argentina 2024/25 Titular', 'Camiseta oficial selección argentina', 84.99, 65, 15, 2, 4, 1, 3, NULL, NULL, 0, 1, 0, 'Poliéster', 'ARG-2425-H-M', 178, '2024-06-01', 1, 1),
('Camiseta Argentina 2024/25 Messi #10', 'Camiseta oficial Argentina con nombre y número de Lionel Messi', 129.99, 40, 15, 2, 4, 1, 3, 'MESSI', 10, 1, 1, 1, 'Poliéster', 'ARG-2425-H-M-M10', 178, '2024-06-01', 1, 1);

-- Clientes de ejemplo
INSERT INTO clientes (nombre, apellidos, email, telefono, equipo_favorito, activo) VALUES
('Carlos', 'García Martínez', 'carlos.garcia@email.com', '+34 600 111 222', 1, 1),
('Laura', 'Fernández López', 'laura.fernandez@email.com', '+34 600 333 444', 2, 1),
('Miguel', 'Rodríguez Santos', 'miguel.rodriguez@email.com', '+34 600 555 666', 4, 1),
('Ana', 'Martín Pérez', 'ana.martin@email.com', '+34 600 777 888', 13, 1);

-- Direcciones de ejemplo
INSERT INTO direcciones (id_cliente, direccion_linea1, ciudad, codigo_postal, id_pais, es_principal) VALUES
(1, 'Calle Gran Vía 25, 3º A', 'Madrid', '28013', 1, 1),
(2, 'Avenida Diagonal 456', 'Barcelona', '08019', 1, 1),
(3, 'Calle Real 78, 2º B', 'Valencia', '46002', 1, 1),
(4, 'Plaza Mayor 12', 'Sevilla', '41001', 1, 1);

-- Métodos de envío
INSERT INTO metodos_envio (nombre_metodo, costo, dias_estimados, activo) VALUES
('Estándar', 4.99, 5, 1),
('Express 24-48h', 9.99, 2, 1),
('Recogida en tienda', 0.00, 0, 1),
('Internacional', 19.99, 10, 1);

-- Métodos de pago
INSERT INTO metodos_pago (nombre_metodo, activo) VALUES
('Tarjeta de crédito', 1),
('PayPal', 1),
('Transferencia bancaria', 1),
('Bizum', 1),
('Contrareembolso', 1);

-- Pedidos de ejemplo
INSERT INTO pedidos (id_cliente, id_direccion, id_metodo_envio, id_metodo_pago, id_estado, subtotal, costo_envio, total) VALUES
(1, 1, 2, 1, 3, 119.99, 9.99, 129.98),
(2, 2, 1, 2, 2, 209.98, 4.99, 214.97),
(3, 3, 1, 1, 4, 84.99, 4.99, 89.98);

-- Artículos de pedidos
INSERT INTO articulos_pedido (id_pedido, id_producto, cantidad, precio_unitario, subtotal) VALUES
(1, 2, 1, 119.99, 119.99),
(2, 3, 1, 89.99, 89.99),
(2, 4, 1, 119.99, 119.99),
(3, 5, 1, 84.99, 84.99);

-- Reseñas de ejemplo
INSERT INTO resenas_producto (id_producto, id_cliente, calificacion, titulo, comentario, verificado) VALUES
(1, 1, 5, '¡Brutal! Hala Madrid', 'La camiseta es de excelente calidad. Los colores son vibrantes y el ajuste perfecto. Muy contento con la compra.', 1),
(2, 1, 5, 'Bellingham es el mejor', 'Me encanta llevar la camiseta de mi jugador favorito. La calidad de impresión del nombre es perfecta.', 1),
(3, 2, 5, 'Visca el Barça', 'Como siempre, Nike hace un trabajo increíble. La camiseta es cómoda y el diseño es espectacular.', 1),
(5, 3, 4, 'Glory Glory Man United', 'Buena camiseta, aunque esperaba que fuera un poco más ligera. Aún así, muy contento.', 1),
(18, 4, 5, 'La albiceleste campeona', 'Camiseta oficial de la mejor selección del mundo. Calidad top y llegó muy rápido.', 1);

-- =============================================
-- VISTAS ÚTILES
-- =============================================

-- Vista de productos con información completa
CREATE VIEW vista_productos_completa AS
SELECT 
    p.id_producto,
    p.nombre_producto,
    p.descripcion,
    p.precio,
    p.stock,
    e.nombre_equipo,
    e.es_seleccion,
    l.nombre_liga,
    m.nombre_marca,
    temp.nombre_temporada,
    tc.nombre_tipo as tipo_camiseta,
    t.nombre_talla as talla,
    p.jugador,
    p.numero_dorsal,
    p.version_jugador,
    p.manga_corta,
    p.incluye_parches,
    p.material,
    p.codigo_producto,
    p.peso,
    p.fecha_lanzamiento,
    p.destacado,
    p.activo,
    (SELECT AVG(calificacion) FROM resenas_producto WHERE id_producto = p.id_producto) as calificacion_promedio,
    (SELECT COUNT(*) FROM resenas_producto WHERE id_producto = p.id_producto) as total_resenas
FROM productos p
LEFT JOIN equipos e ON p.id_equipo = e.id_equipo
LEFT JOIN ligas l ON e.id_liga = l.id_liga
LEFT JOIN marcas m ON p.id_marca = m.id_marca
LEFT JOIN temporadas temp ON p.id_temporada = temp.id_temporada
LEFT JOIN tipos_camiseta tc ON p.id_tipo_camiseta = tc.id_tipo_camiseta
LEFT JOIN tallas t ON p.id_talla = t.id_talla;

-- Vista de pedidos con detalles
CREATE VIEW vista_pedidos_detalle AS
SELECT 
    ped.id_pedido,
    ped.fecha_pedido,
    CONCAT(cli.nombre, ' ', cli.apellidos) as cliente,
    cli.email,
    CONCAT(dir.direccion_linea1, ', ', dir.ciudad, ', ', dir.codigo_postal) as direccion_envio,
    p.nombre_pais,
    me.nombre_metodo as metodo_envio,
    mp.nombre_metodo as metodo_pago,
    ep.nombre_estado as estado,
    ped.subtotal,
    ped.costo_envio,
    ped.total
FROM pedidos ped
JOIN clientes cli ON ped.id_cliente = cli.id_cliente
JOIN direcciones dir ON ped.id_direccion = dir.id_direccion
JOIN paises p ON dir.id_pais = p.id_pais
JOIN metodos_envio me ON ped.id_metodo_envio = me.id_metodo_envio
JOIN metodos_pago mp ON ped.id_metodo_pago = mp.id_metodo_pago
JOIN estados_pedido ep ON ped.id_estado = ep.id_estado;

-- Vista de equipos más vendidos
CREATE VIEW vista_equipos_mas_vendidos AS
SELECT 
    e.nombre_equipo,
    COUNT(ap.id_articulo_pedido) as total_ventas,
    SUM(ap.cantidad) as unidades_vendidas,
    SUM(ap.subtotal) as ingresos_totales
FROM equipos e
JOIN productos p ON e.id_equipo = p.id_equipo
JOIN articulos_pedido ap ON p.id_producto = ap.id_producto
GROUP BY e.id_equipo
ORDER BY total_ventas DESC;
