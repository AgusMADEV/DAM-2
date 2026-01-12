DROP DATABASE IF EXISTS erp_inteligente;
CREATE DATABASE erp_inteligente CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE erp_inteligente;

-- =====================================================
-- TABLA: usuarios
-- =====================================================
CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    rol ENUM('admin', 'vendedor', 'almacen', 'gerente') DEFAULT 'vendedor',
    activo BOOLEAN DEFAULT TRUE,
    ultimo_acceso TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLA: clientes
-- =====================================================
CREATE TABLE clientes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    telefono VARCHAR(20),
    direccion TEXT,
    ciudad VARCHAR(50),
    provincia VARCHAR(50),
    codigo_postal VARCHAR(10),
    pais VARCHAR(50) DEFAULT 'España',
    nif VARCHAR(20) UNIQUE,
    scoring INT DEFAULT 50 COMMENT 'Valoración del cliente 0-100',
    notas TEXT,
    ultima_compra DATE,
    total_compras DECIMAL(10,2) DEFAULT 0.00,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre),
    INDEX idx_email (email),
    INDEX idx_ultima_compra (ultima_compra),
    INDEX idx_scoring (scoring),
    INDEX idx_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLA: categorias_productos
-- =====================================================
CREATE TABLE categorias_productos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    activa BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLA: productos
-- =====================================================
CREATE TABLE productos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    categoria_id INT,
    precio_compra DECIMAL(10,2),
    precio_venta DECIMAL(10,2) NOT NULL,
    margen_porcentaje DECIMAL(5,2) GENERATED ALWAYS AS (
        CASE 
            WHEN precio_compra > 0 THEN ((precio_venta - precio_compra) / precio_compra * 100)
            ELSE 0 
        END
    ) STORED,
    stock_actual INT DEFAULT 0,
    stock_minimo INT DEFAULT 10,
    stock_maximo INT DEFAULT 100,
    unidad_medida VARCHAR(20) DEFAULT 'unidad',
    imagen_url VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias_productos(id) ON DELETE SET NULL,
    INDEX idx_codigo (codigo),
    INDEX idx_nombre (nombre),
    INDEX idx_categoria (categoria_id),
    INDEX idx_stock_bajo (stock_actual, stock_minimo),
    INDEX idx_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLA: ventas
-- =====================================================
CREATE TABLE ventas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    numero_factura VARCHAR(50) UNIQUE NOT NULL,
    cliente_id INT,
    usuario_id INT NOT NULL,
    fecha DATE NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    descuento DECIMAL(10,2) DEFAULT 0.00,
    iva_porcentaje DECIMAL(5,2) DEFAULT 21.00,
    iva DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    estado ENUM('pendiente', 'pagada', 'cancelada', 'devuelta') DEFAULT 'pendiente',
    metodo_pago ENUM('efectivo', 'tarjeta', 'transferencia', 'otro') DEFAULT 'efectivo',
    fecha_vencimiento DATE,
    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE SET NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    INDEX idx_numero_factura (numero_factura),
    INDEX idx_cliente (cliente_id),
    INDEX idx_usuario (usuario_id),
    INDEX idx_fecha (fecha),
    INDEX idx_estado (estado),
    INDEX idx_metodo_pago (metodo_pago)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLA: lineas_venta
-- =====================================================
CREATE TABLE lineas_venta (
    id INT PRIMARY KEY AUTO_INCREMENT,
    venta_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    descuento DECIMAL(10,2) DEFAULT 0.00,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (venta_id) REFERENCES ventas(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id),
    INDEX idx_venta (venta_id),
    INDEX idx_producto (producto_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLA: movimientos_inventario
-- =====================================================
CREATE TABLE movimientos_inventario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    producto_id INT NOT NULL,
    tipo ENUM('entrada', 'salida', 'ajuste', 'devolucion') NOT NULL,
    cantidad INT NOT NULL,
    stock_anterior INT NOT NULL,
    stock_nuevo INT NOT NULL,
    motivo VARCHAR(200),
    referencia VARCHAR(100) COMMENT 'Número de factura, albarán, etc.',
    usuario_id INT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (producto_id) REFERENCES productos(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    INDEX idx_producto (producto_id),
    INDEX idx_tipo (tipo),
    INDEX idx_fecha (fecha),
    INDEX idx_usuario (usuario_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLA: conversaciones_ia
-- =====================================================
CREATE TABLE conversaciones_ia (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    session_id VARCHAR(100) NOT NULL,
    mensaje_usuario TEXT NOT NULL,
    respuesta_ia TEXT NOT NULL,
    intencion VARCHAR(50) COMMENT 'consulta_stock, consulta_ventas, etc.',
    confianza DECIMAL(5,2) COMMENT 'Nivel de confianza 0-100',
    consulta_sql TEXT COMMENT 'SQL generado si aplica',
    tiempo_respuesta_ms INT COMMENT 'Milisegundos de procesamiento',
    metadata JSON COMMENT 'Datos adicionales de contexto',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    INDEX idx_usuario (usuario_id),
    INDEX idx_session (session_id),
    INDEX idx_intencion (intencion),
    INDEX idx_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLA: alertas
-- =====================================================
CREATE TABLE alertas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tipo VARCHAR(50) NOT NULL COMMENT 'stock_bajo, factura_vencida, cliente_inactivo, etc.',
    severidad ENUM('info', 'warning', 'critical') DEFAULT 'info',
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    entidad_tipo VARCHAR(50) COMMENT 'producto, cliente, venta',
    entidad_id INT COMMENT 'ID de la entidad relacionada',
    accion_sugerida TEXT,
    usuario_id INT COMMENT 'Usuario al que va dirigida la alerta',
    leida BOOLEAN DEFAULT FALSE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_leida TIMESTAMP NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    INDEX idx_tipo (tipo),
    INDEX idx_severidad (severidad),
    INDEX idx_leida (leida, severidad),
    INDEX idx_usuario (usuario_id),
    INDEX idx_fecha (fecha_creacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLA: configuracion_sistema
-- =====================================================
CREATE TABLE configuracion_sistema (
    id INT PRIMARY KEY AUTO_INCREMENT,
    clave VARCHAR(100) UNIQUE NOT NULL,
    valor TEXT NOT NULL,
    descripcion TEXT,
    tipo ENUM('string', 'number', 'boolean', 'json') DEFAULT 'string',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_clave (clave)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TRIGGERS
-- =====================================================

-- Trigger: Actualizar stock después de crear línea de venta
DELIMITER //
CREATE TRIGGER trg_after_linea_venta_insert
AFTER INSERT ON lineas_venta
FOR EACH ROW
BEGIN
    DECLARE stock_previo INT;
    
    -- Obtener stock actual
    SELECT stock_actual INTO stock_previo 
    FROM productos 
    WHERE id = NEW.producto_id;
    
    -- Actualizar stock del producto
    UPDATE productos 
    SET stock_actual = stock_actual - NEW.cantidad
    WHERE id = NEW.producto_id;
    
    -- Registrar movimiento de inventario
    INSERT INTO movimientos_inventario 
        (producto_id, tipo, cantidad, stock_anterior, stock_nuevo, motivo, usuario_id)
    SELECT 
        NEW.producto_id, 
        'salida', 
        NEW.cantidad, 
        stock_previo,
        stock_previo - NEW.cantidad,
        CONCAT('Venta #', v.numero_factura),
        v.usuario_id
    FROM ventas v
    WHERE v.id = NEW.venta_id;
    
    -- Crear alerta si stock bajo
    INSERT INTO alertas (tipo, severidad, titulo, descripcion, entidad_tipo, entidad_id)
    SELECT 
        'stock_bajo',
        CASE 
            WHEN p.stock_actual <= 0 THEN 'critical'
            WHEN p.stock_actual < (p.stock_minimo / 2) THEN 'critical'
            ELSE 'warning'
        END,
        CONCAT('Stock bajo: ', p.nombre),
        CONCAT('El producto "', p.nombre, '" tiene ', p.stock_actual, ' unidades (mínimo: ', p.stock_minimo, ')'),
        'producto',
        p.id
    FROM productos p
    WHERE p.id = NEW.producto_id 
        AND p.stock_actual < p.stock_minimo;
END//
DELIMITER ;

-- Trigger: Actualizar totales de cliente después de venta
DELIMITER //
CREATE TRIGGER trg_after_venta_insert
AFTER INSERT ON ventas
FOR EACH ROW
BEGIN
    IF NEW.cliente_id IS NOT NULL AND NEW.estado = 'pagada' THEN
        UPDATE clientes
        SET 
            ultima_compra = NEW.fecha,
            total_compras = total_compras + NEW.total
        WHERE id = NEW.cliente_id;
    END IF;
END//
DELIMITER ;

-- Trigger: Actualizar totales de cliente cuando cambia estado de venta
DELIMITER //
CREATE TRIGGER trg_after_venta_update
AFTER UPDATE ON ventas
FOR EACH ROW
BEGIN
    IF NEW.cliente_id IS NOT NULL THEN
        -- Si cambia a pagada, sumar
        IF NEW.estado = 'pagada' AND OLD.estado != 'pagada' THEN
            UPDATE clientes
            SET total_compras = total_compras + NEW.total
            WHERE id = NEW.cliente_id;
        END IF;
        
        -- Si cambia de pagada a otro estado, restar
        IF OLD.estado = 'pagada' AND NEW.estado != 'pagada' THEN
            UPDATE clientes
            SET total_compras = total_compras - OLD.total
            WHERE id = NEW.cliente_id;
        END IF;
    END IF;
END//
DELIMITER ;

-- =====================================================
-- VISTAS
-- =====================================================

-- Vista: Productos con stock bajo
CREATE VIEW v_productos_stock_bajo AS
SELECT 
    p.id,
    p.codigo,
    p.nombre,
    c.nombre AS categoria,
    p.stock_actual,
    p.stock_minimo,
    p.stock_minimo - p.stock_actual AS unidades_faltantes,
    p.precio_compra,
    (p.stock_minimo - p.stock_actual) * p.precio_compra AS valor_reposicion
FROM productos p
LEFT JOIN categorias_productos c ON p.categoria_id = c.id
WHERE p.stock_actual < p.stock_minimo 
    AND p.activo = TRUE
ORDER BY (p.stock_minimo - p.stock_actual) DESC;

-- Vista: Top clientes
CREATE VIEW v_top_clientes AS
SELECT 
    c.id,
    c.codigo,
    c.nombre,
    c.email,
    c.telefono,
    c.ciudad,
    c.total_compras,
    c.ultima_compra,
    COUNT(v.id) AS num_compras,
    c.scoring
FROM clientes c
LEFT JOIN ventas v ON c.id = v.cliente_id AND v.estado = 'pagada'
WHERE c.activo = TRUE
GROUP BY c.id
ORDER BY c.total_compras DESC;

-- Vista: Ventas del mes actual
CREATE VIEW v_ventas_mes_actual AS
SELECT 
    v.id,
    v.numero_factura,
    v.fecha,
    c.nombre AS cliente,
    u.nombre AS vendedor,
    v.total,
    v.estado,
    v.metodo_pago
FROM ventas v
LEFT JOIN clientes c ON v.cliente_id = c.id
JOIN usuarios u ON v.usuario_id = u.id
WHERE YEAR(v.fecha) = YEAR(CURDATE()) 
    AND MONTH(v.fecha) = MONTH(CURDATE())
ORDER BY v.fecha DESC;

-- Vista: Dashboard KPIs
CREATE VIEW v_dashboard_kpis AS
SELECT
    (SELECT COUNT(*) FROM productos WHERE activo = TRUE) AS total_productos,
    (SELECT COUNT(*) FROM productos WHERE stock_actual < stock_minimo AND activo = TRUE) AS productos_stock_bajo,
    (SELECT COUNT(*) FROM clientes WHERE activo = TRUE) AS total_clientes,
    (SELECT COUNT(*) FROM ventas WHERE fecha = CURDATE()) AS ventas_hoy,
    (SELECT COALESCE(SUM(total), 0) FROM ventas WHERE fecha = CURDATE() AND estado = 'pagada') AS ingresos_hoy,
    (SELECT COALESCE(SUM(total), 0) FROM ventas WHERE YEAR(fecha) = YEAR(CURDATE()) AND MONTH(fecha) = MONTH(CURDATE()) AND estado = 'pagada') AS ingresos_mes,
    (SELECT COUNT(*) FROM alertas WHERE leida = FALSE) AS alertas_pendientes,
    (SELECT COUNT(*) FROM alertas WHERE leida = FALSE AND severidad = 'critical') AS alertas_criticas;

-- =====================================================
-- PROCEDIMIENTOS ALMACENADOS
-- =====================================================

-- Procedimiento: Generar número de factura automático
DELIMITER //
CREATE PROCEDURE sp_generar_numero_factura(OUT nuevo_numero VARCHAR(50))
BEGIN
    DECLARE ultimo_numero INT;
    DECLARE anio_actual VARCHAR(4);
    
    SET anio_actual = YEAR(CURDATE());
    
    SELECT COALESCE(MAX(CAST(SUBSTRING(numero_factura, 6) AS UNSIGNED)), 0)
    INTO ultimo_numero
    FROM ventas
    WHERE numero_factura LIKE CONCAT(anio_actual, '%');
    
    SET nuevo_numero = CONCAT(anio_actual, '-', LPAD(ultimo_numero + 1, 6, '0'));
END//
DELIMITER ;

-- Procedimiento: Marcar alertas como leídas
DELIMITER //
CREATE PROCEDURE sp_marcar_alertas_leidas(IN p_usuario_id INT)
BEGIN
    UPDATE alertas
    SET leida = TRUE, fecha_leida = CURRENT_TIMESTAMP
    WHERE usuario_id = p_usuario_id AND leida = FALSE;
END//
DELIMITER ;

-- Procedimiento: Obtener estadísticas de producto
DELIMITER //
CREATE PROCEDURE sp_estadisticas_producto(IN p_producto_id INT)
BEGIN
    SELECT 
        p.id,
        p.codigo,
        p.nombre,
        p.stock_actual,
        p.precio_venta,
        COALESCE(SUM(lv.cantidad), 0) AS unidades_vendidas,
        COALESCE(COUNT(DISTINCT v.id), 0) AS num_ventas,
        COALESCE(SUM(lv.subtotal), 0) AS ingresos_totales,
        COALESCE(AVG(lv.cantidad), 0) AS promedio_unidades_venta
    FROM productos p
    LEFT JOIN lineas_venta lv ON p.id = lv.producto_id
    LEFT JOIN ventas v ON lv.venta_id = v.id AND v.estado = 'pagada'
    WHERE p.id = p_producto_id
    GROUP BY p.id;
END//
DELIMITER ;

-- =====================================================
-- COMENTARIOS Y DOCUMENTACIÓN
-- =====================================================

-- Este esquema está optimizado para:
-- 1. Consultas rápidas del asistente IA (índices estratégicos)
-- 2. Integridad referencial (foreign keys)
-- 3. Triggers automáticos para stock y alertas
-- 4. Vistas para consultas frecuentes
-- 5. Procedimientos para operaciones complejas

-- Los triggers se encargan de:
-- - Actualizar stock automáticamente al vender
-- - Crear alertas de stock bajo
-- - Mantener sincronizados los totales de clientes

-- Las vistas facilitan:
-- - Consultas del asistente IA
-- - Dashboard en tiempo real
-- - Reportes rápidos

-- La tabla conversaciones_ia almacena:
-- - Historial completo de interacciones
-- - Métricas de rendimiento
-- - Contexto para mejorar respuestas futuras
