-- =====================================================
-- DATOS DE PRUEBA - ERP INTELIGENTE
-- Fecha: 14 de Noviembre de 2025
-- =====================================================

USE erp_inteligente;

-- =====================================================
-- 1. USUARIOS
-- =====================================================
-- Password: admin123 (en producción se hashearía con bcrypt)
INSERT INTO usuarios (username, password_hash, nombre, email, rol, activo) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIw3QxQE8a', 'Administrador Sistema', 'admin@erp.com', 'admin', TRUE),
('vendedor1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIw3QxQE8a', 'Juan Pérez', 'juan@erp.com', 'vendedor', TRUE),
('vendedor2', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIw3QxQE8a', 'María García', 'maria@erp.com', 'vendedor', TRUE),
('almacen1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIw3QxQE8a', 'Carlos Ruiz', 'carlos@erp.com', 'almacen', TRUE),
('gerente1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIw3QxQE8a', 'Laura Martínez', 'laura@erp.com', 'gerente', TRUE);

-- =====================================================
-- 2. CATEGORÍAS DE PRODUCTOS
-- =====================================================
INSERT INTO categorias_productos (nombre, descripcion, activa) VALUES
('Electrónica', 'Productos electrónicos y tecnología', TRUE),
('Informática', 'Ordenadores, portátiles y accesorios', TRUE),
('Periféricos', 'Teclados, ratones, auriculares', TRUE),
('Componentes', 'Componentes de PC', TRUE),
('Redes', 'Equipos de red y conectividad', TRUE),
('Almacenamiento', 'Discos duros, SSD, pendrives', TRUE),
('Accesorios', 'Cables, fundas, protectores', TRUE);

-- =====================================================
-- 3. CLIENTES
-- =====================================================
INSERT INTO clientes (codigo, nombre, email, telefono, direccion, ciudad, provincia, codigo_postal, nif, scoring, ultima_compra, total_compras, activo) VALUES
-- Clientes VIP (alta facturación)
('CLI-001', 'TechnoStore Valencia SL', 'info@technostore.com', '963123456', 'Av. del Puerto 123', 'Valencia', 'Valencia', '46021', 'B12345678', 95, '2025-11-13', 45600.00, TRUE),
('CLI-002', 'Informática Global SA', 'ventas@infoglobal.es', '961234567', 'C/ Colón 45', 'Valencia', 'Valencia', '46004', 'A23456789', 90, '2025-11-12', 38200.00, TRUE),
('CLI-003', 'Sistemas Empresariales', 'contacto@sisempresas.com', '962345678', 'C/ Poeta Querol 8', 'Valencia', 'Valencia', '46002', 'B34567890', 88, '2025-11-10', 32500.00, TRUE),

-- Clientes regulares
('CLI-004', 'Oficinas del Mediterráneo', 'admin@ofimediterraneo.es', '963456789', 'Av. Blasco Ibáñez 28', 'Valencia', 'Valencia', '46010', 'B45678901', 75, '2025-11-08', 15800.00, TRUE),
('CLI-005', 'Comercial López e Hijos', 'info@lopezehijos.com', '964567890', 'C/ Mayor 156', 'Castellón', 'Castellón', '12001', 'B56789012', 70, '2025-11-05', 12300.00, TRUE),
('CLI-006', 'Tecnología Alicante', 'ventas@tecalicante.es', '965678901', 'Rambla Méndez Núñez 42', 'Alicante', 'Alicante', '03002', 'B67890123', 80, '2025-11-11', 18900.00, TRUE),
('CLI-007', 'Pyme Digital SL', 'contacto@pymedigital.com', '966789012', 'C/ San Vicente 89', 'Valencia', 'Valencia', '46007', 'B78901234', 65, '2025-10-28', 9500.00, TRUE),

-- Clientes nuevos (poca facturación)
('CLI-008', 'Startup Tech Innovation', 'hola@startuptech.es', '967890123', 'C/ Pintor Sorolla 15', 'Valencia', 'Valencia', '46002', 'B89012345', 50, '2025-11-09', 2400.00, TRUE),
('CLI-009', 'Asesoría Martínez', 'info@asesoriamartinez.com', '968901234', 'C/ Paz 67', 'Valencia', 'Valencia', '46003', 'B90123456', 55, '2025-11-07', 3100.00, TRUE),
('CLI-010', 'Consultoría García', 'contacto@consultoriagarcia.es', '969012345', 'Av. Aragón 234', 'Valencia', 'Valencia', '46015', 'B01234567', 60, '2025-11-06', 4800.00, TRUE),

-- Clientes inactivos (más de 60 días sin comprar)
('CLI-011', 'Distribuciones Levante', 'ventas@distriblevante.com', '960123456', 'C/ Guillem de Castro 45', 'Valencia', 'Valencia', '46008', 'B11223344', 40, '2025-08-15', 6700.00, TRUE),
('CLI-012', 'Suministros Pérez', 'info@suministrosperez.es', '961234560', 'C/ Xàtiva 123', 'Valencia', 'Valencia', '46007', 'B22334455', 35, '2025-07-20', 5200.00, TRUE),
('CLI-013', 'Comercial Rodríguez', 'contacto@comrodriguez.com', '962345601', 'Av. Francia 78', 'Valencia', 'Valencia', '46023', 'B33445566', 30, '2025-06-10', 3800.00, TRUE),

-- Clientes particulares
('CLI-014', 'Juan Antonio Sánchez', 'jasanchez@gmail.com', '612345678', 'C/ Salamanca 23', 'Valencia', 'Valencia', '46005', '12345678A', 60, '2025-11-09', 1200.00, TRUE),
('CLI-015', 'María Carmen López', 'mclopez@hotmail.com', '623456789', 'C/ Botánico Cavanilles 56', 'Valencia', 'Valencia', '46010', '23456789B', 55, '2025-11-04', 890.00, TRUE);

-- =====================================================
-- 4. PRODUCTOS
-- =====================================================
INSERT INTO productos (codigo, nombre, descripcion, categoria_id, precio_compra, precio_venta, stock_actual, stock_minimo, stock_maximo, activo) VALUES
-- Portátiles (stock normal y bajo)
('PROD-001', 'Portátil Dell Latitude 5520', 'Portátil profesional 15.6" i5-11300H 16GB 512GB SSD', 2, 650.00, 899.00, 8, 5, 20, TRUE),
('PROD-002', 'Portátil HP ProBook 450 G9', 'Portátil empresarial 15.6" i7-1255U 16GB 512GB', 2, 720.00, 999.00, 12, 8, 25, TRUE),
('PROD-003', 'Portátil Lenovo ThinkPad E15', 'ThinkPad 15.6" i5-1235U 8GB 256GB SSD', 2, 550.00, 749.00, 3, 10, 20, TRUE), -- STOCK BAJO
('PROD-004', 'MacBook Air M2 13"', 'MacBook Air con chip M2 8GB 256GB', 2, 950.00, 1299.00, 5, 5, 15, TRUE),
('PROD-005', 'Portátil ASUS VivoBook 15', 'VivoBook 15.6" Ryzen 5 8GB 512GB', 2, 480.00, 649.00, 15, 10, 30, TRUE),

-- Monitores (stock normal)
('PROD-006', 'Monitor LG 27" 4K UHD', 'Monitor profesional 27" IPS 4K HDR10', 1, 280.00, 389.00, 18, 8, 30, TRUE),
('PROD-007', 'Monitor Dell 24" Full HD', 'Monitor 24" IPS Full HD ajustable', 1, 145.00, 199.00, 22, 15, 40, TRUE),
('PROD-008', 'Monitor Samsung 32" Curvo', 'Monitor gaming curvo 32" 165Hz', 1, 320.00, 449.00, 10, 6, 20, TRUE),

-- Periféricos (varios con stock bajo)
('PROD-009', 'Teclado Mecánico Logitech MX Keys', 'Teclado mecánico inalámbrico retroiluminado', 3, 85.00, 129.00, 2, 15, 40, TRUE), -- STOCK CRÍTICO
('PROD-010', 'Ratón Logitech MX Master 3S', 'Ratón inalámbrico ergonómico precisión', 3, 75.00, 109.00, 5, 20, 50, TRUE), -- STOCK BAJO
('PROD-011', 'Webcam Logitech C920 HD Pro', 'Webcam Full HD 1080p con micrófono', 3, 52.00, 79.00, 28, 15, 50, TRUE),
('PROD-012', 'Auriculares Sony WH-1000XM5', 'Auriculares inalámbricos cancelación ruido', 3, 280.00, 399.00, 8, 10, 25, TRUE), -- STOCK BAJO

-- Componentes (varios críticos)
('PROD-013', 'SSD Samsung 980 Pro 1TB', 'SSD NVMe M.2 1TB PCIe 4.0', 4, 85.00, 129.00, 1, 20, 60, TRUE), -- CRÍTICO
('PROD-014', 'RAM Kingston Fury 16GB DDR4', 'Memoria RAM DDR4 3200MHz 16GB Kit', 4, 45.00, 69.00, 35, 30, 80, TRUE),
('PROD-015', 'Disco Duro Seagate 2TB', 'HDD 3.5" 2TB 7200rpm', 6, 48.00, 72.00, 42, 25, 70, TRUE),

-- Redes
('PROD-016', 'Router TP-Link AX3000', 'Router WiFi 6 AX3000 Dual Band', 5, 65.00, 99.00, 4, 12, 35, TRUE), -- STOCK BAJO
('PROD-017', 'Switch Netgear 8 puertos', 'Switch Gigabit 8 puertos no gestionable', 5, 32.00, 49.00, 20, 10, 40, TRUE),
('PROD-018', 'Adaptador WiFi USB TP-Link', 'Adaptador USB WiFi 6 AX1800', 5, 18.00, 29.00, 45, 25, 80, TRUE),

-- Almacenamiento externo
('PROD-019', 'Disco Externo WD 4TB', 'Disco duro externo USB 3.0 4TB', 6, 82.00, 119.00, 16, 12, 35, TRUE),
('PROD-020', 'SSD Externo Samsung T7 1TB', 'SSD portátil USB 3.2 1TB', 6, 78.00, 115.00, 12, 10, 30, TRUE),

-- Accesorios (stock variado)
('PROD-021', 'Cable HDMI 2.1 2m', 'Cable HDMI 2.1 4K 120Hz 2 metros', 7, 6.50, 12.99, 150, 80, 200, TRUE),
('PROD-022', 'Hub USB-C 7 en 1', 'Hub multipuerto USB-C HDMI USB 3.0', 7, 22.00, 35.99, 38, 30, 80, TRUE),
('PROD-023', 'Alfombrilla XXL Gaming', 'Alfombrilla ratón gaming 900x400mm', 7, 12.00, 19.99, 55, 40, 100, TRUE),
('PROD-024', 'Soporte Portátil Ajustable', 'Soporte elevador portátil aluminio', 7, 18.00, 29.99, 6, 15, 50, TRUE), -- STOCK BAJO
('PROD-025', 'Regleta Protección 6 tomas', 'Regleta con protección sobretensión 6 tomas', 7, 9.50, 16.99, 72, 50, 150, TRUE);

-- =====================================================
-- 5. VENTAS
-- =====================================================

-- Ventas de HOY (14 nov 2025)
INSERT INTO ventas (numero_factura, cliente_id, usuario_id, fecha, subtotal, descuento, iva_porcentaje, iva, total, estado, metodo_pago, fecha_vencimiento) VALUES
('2025-000045', 1, 2, '2025-11-14', 1798.00, 0.00, 21.00, 377.58, 2175.58, 'pagada', 'tarjeta', NULL),
('2025-000046', 6, 3, '2025-11-14', 449.00, 22.45, 21.00, 89.58, 516.13, 'pagada', 'transferencia', NULL),
('2025-000047', 14, 2, '2025-11-14', 129.00, 0.00, 21.00, 27.09, 156.09, 'pagada', 'efectivo', NULL);

-- Ventas de AYER (13 nov)
INSERT INTO ventas (numero_factura, cliente_id, usuario_id, fecha, subtotal, descuento, iva_porcentaje, iva, total, estado, metodo_pago, fecha_vencimiento) VALUES
('2025-000042', 1, 2, '2025-11-13', 3896.00, 194.80, 21.00, 777.25, 4478.45, 'pagada', 'transferencia', NULL),
('2025-000043', 8, 3, '2025-11-13', 748.00, 0.00, 21.00, 157.08, 905.08, 'pagada', 'tarjeta', NULL),
('2025-000044', 9, 2, '2025-11-13', 578.00, 0.00, 21.00, 121.38, 699.38, 'pagada', 'efectivo', NULL);

-- Ventas de esta SEMANA (11-12 nov)
INSERT INTO ventas (numero_factura, cliente_id, usuario_id, fecha, subtotal, descuento, iva_porcentaje, iva, total, estado, metodo_pago, fecha_vencimiento) VALUES
('2025-000038', 2, 2, '2025-11-12', 5994.00, 299.70, 21.00, 1195.80, 6890.10, 'pagada', 'transferencia', NULL),
('2025-000039', 6, 3, '2025-11-12', 1297.00, 0.00, 21.00, 272.37, 1569.37, 'pagada', 'tarjeta', NULL),
('2025-000040', 15, 2, '2025-11-11', 398.00, 0.00, 21.00, 83.58, 481.58, 'pagada', 'efectivo', NULL),
('2025-000041', 3, 3, '2025-11-11', 2996.00, 149.80, 21.00, 597.70, 3443.90, 'pagada', 'transferencia', NULL);

-- Ventas semanas anteriores (octubre-noviembre)
INSERT INTO ventas (numero_factura, cliente_id, usuario_id, fecha, subtotal, descuento, iva_porcentaje, iva, total, estado, metodo_pago, fecha_vencimiento) VALUES
('2025-000034', 3, 2, '2025-11-10', 4494.00, 224.70, 21.00, 896.65, 5165.95, 'pagada', 'transferencia', NULL),
('2025-000035', 14, 3, '2025-11-09', 1028.00, 0.00, 21.00, 215.88, 1243.88, 'pagada', 'tarjeta', NULL),
('2025-000036', 8, 2, '2025-11-09', 199.00, 0.00, 21.00, 41.79, 240.79, 'pagada', 'efectivo', NULL),
('2025-000037', 4, 3, '2025-11-08', 2547.00, 127.35, 21.00, 508.23, 2927.88, 'pagada', 'transferencia', NULL),
('2025-000030', 5, 2, '2025-11-05', 1947.00, 0.00, 21.00, 408.87, 2355.87, 'pagada', 'transferencia', NULL),
('2025-000031', 6, 3, '2025-11-04', 890.00, 0.00, 21.00, 186.90, 1076.90, 'pagada', 'tarjeta', NULL),
('2025-000032', 15, 2, '2025-11-04', 490.00, 0.00, 21.00, 102.90, 592.90, 'pagada', 'efectivo', NULL),
('2025-000033', 7, 3, '2025-10-28', 1498.00, 0.00, 21.00, 314.58, 1812.58, 'pagada', 'transferencia', NULL);

-- Facturas PENDIENTES (algunas vencidas)
INSERT INTO ventas (numero_factura, cliente_id, usuario_id, fecha, subtotal, descuento, iva_porcentaje, iva, total, estado, metodo_pago, fecha_vencimiento) VALUES
('2025-000026', 4, 2, '2025-10-15', 2347.00, 0.00, 21.00, 492.87, 2839.87, 'pendiente', 'transferencia', '2025-10-30'),  -- Vencida hace 15 días
('2025-000027', 7, 3, '2025-10-20', 1678.00, 0.00, 21.00, 352.38, 2030.38, 'pendiente', 'transferencia', '2025-11-05'),  -- Vencida hace 9 días
('2025-000028', 10, 2, '2025-10-25', 945.00, 0.00, 21.00, 198.45, 1143.45, 'pendiente', 'transferencia', '2025-11-10'),  -- Vencida hace 4 días
('2025-000029', 5, 3, '2025-11-01', 1234.00, 0.00, 21.00, 259.14, 1493.14, 'pendiente', 'transferencia', '2025-11-20');  -- No vencida aún

-- =====================================================
-- 6. LÍNEAS DE VENTA
-- =====================================================

-- Venta 2025-000045 (HOY - TechnoStore)
INSERT INTO lineas_venta (venta_id, producto_id, cantidad, precio_unitario, descuento, subtotal) VALUES
(1, 1, 2, 899.00, 0.00, 1798.00);  -- 2 Dell Latitude

-- Venta 2025-000046 (HOY - Tecnología Alicante)
INSERT INTO lineas_venta (venta_id, producto_id, cantidad, precio_unitario, descuento, subtotal) VALUES
(2, 8, 1, 449.00, 22.45, 426.55);  -- 1 Monitor Samsung (con descuento)

-- Venta 2025-000047 (HOY - Juan Antonio)
INSERT INTO lineas_venta (venta_id, producto_id, cantidad, precio_unitario, descuento, subtotal) VALUES
(3, 9, 1, 129.00, 0.00, 129.00);  -- 1 Teclado Logitech

-- Venta 2025-000042 (AYER - TechnoStore)
INSERT INTO lineas_venta (venta_id, producto_id, cantidad, precio_unitario, descuento, subtotal) VALUES
(4, 2, 3, 999.00, 149.85, 2847.15),  -- 3 HP ProBook
(4, 10, 10, 109.00, 54.50, 1035.50);  -- 10 Ratones MX Master

-- Venta 2025-000043 (AYER - Startup Tech)
INSERT INTO lineas_venta (venta_id, producto_id, cantidad, precio_unitario, descuento, subtotal) VALUES
(5, 3, 1, 749.00, 0.00, 749.00);  -- 1 Lenovo ThinkPad

-- Venta 2025-000044 (AYER - Asesoría Martínez)
INSERT INTO lineas_venta (venta_id, producto_id, cantidad, precio_unitario, descuento, subtotal) VALUES
(6, 12, 1, 399.00, 0.00, 399.00),  -- 1 Auriculares Sony
(6, 7, 1, 199.00, 0.00, 199.00);   -- 1 Monitor Dell 24"

-- Venta 2025-000038 (12 nov - Informática Global)
INSERT INTO lineas_venta (venta_id, producto_id, cantidad, precio_unitario, descuento, subtotal) VALUES
(7, 6, 6, 389.00, 116.70, 2217.30),  -- 6 Monitores LG 27"
(7, 1, 4, 899.00, 179.80, 3416.20);  -- 4 Dell Latitude

-- Venta 2025-000039 (12 nov - Tecnología Alicante)
INSERT INTO lineas_venta (venta_id, producto_id, cantidad, precio_unitario, descuento, subtotal) VALUES
(8, 4, 1, 1299.00, 0.00, 1299.00);  -- 1 MacBook Air

-- Venta 2025-000040 (11 nov - María Carmen)
INSERT INTO lineas_venta (venta_id, producto_id, cantidad, precio_unitario, descuento, subtotal) VALUES
(9, 12, 1, 399.00, 0.00, 399.00);  -- 1 Auriculares Sony

-- Venta 2025-000041 (11 nov - Sistemas Empresariales)
INSERT INTO lineas_venta (venta_id, producto_id, cantidad, precio_unitario, descuento, subtotal) VALUES
(10, 1, 4, 899.00, 179.80, 3416.20);  -- 4 Dell Latitude

-- Venta 2025-000034 (10 nov - Sistemas Empresariales)
INSERT INTO lineas_venta (venta_id, producto_id, cantidad, precio_unitario, descuento, subtotal) VALUES
(11, 2, 5, 999.00, 249.75, 4745.25);  -- 5 HP ProBook

-- Venta 2025-000035 (9 nov - Juan Antonio)
INSERT INTO lineas_venta (venta_id, producto_id, cantidad, precio_unitario, descuento, subtotal) VALUES
(12, 10, 5, 109.00, 27.25, 517.75),  -- 5 Ratones
(12, 9, 4, 129.00, 25.80, 490.20);   -- 4 Teclados

-- Venta 2025-000036 (9 nov - Startup Tech)
INSERT INTO lineas_venta (venta_id, producto_id, cantidad, precio_unitario, descuento, subtotal) VALUES
(13, 7, 1, 199.00, 0.00, 199.00);  -- 1 Monitor Dell

-- Venta 2025-000037 (8 nov - Oficinas Mediterráneo)
INSERT INTO lineas_venta (venta_id, producto_id, cantidad, precio_unitario, descuento, subtotal) VALUES
(14, 7, 10, 199.00, 199.00, 1791.00),  -- 10 Monitores Dell
(14, 10, 7, 109.00, 38.15, 725.85);    -- 7 Ratones

-- Ventas más antiguas (resumen)
INSERT INTO lineas_venta (venta_id, producto_id, cantidad, precio_unitario, descuento, subtotal) VALUES
(15, 5, 3, 649.00, 0.00, 1947.00),   -- Venta 2025-000030
(16, 6, 2, 389.00, 0.00, 778.00),    -- Venta 2025-000031
(16, 20, 1, 115.00, 0.00, 115.00),
(17, 7, 2, 199.00, 0.00, 398.00),    -- Venta 2025-000032
(17, 10, 1, 109.00, 0.00, 109.00),
(18, 1, 1, 899.00, 0.00, 899.00),    -- Venta 2025-000033
(18, 2, 1, 999.00, 0.00, 999.00);

-- Facturas pendientes (líneas)
INSERT INTO lineas_venta (venta_id, producto_id, cantidad, precio_unitario, descuento, subtotal) VALUES
(19, 2, 2, 999.00, 0.00, 1998.00),   -- Venta 2025-000026
(19, 6, 1, 389.00, 0.00, 389.00),
(20, 3, 2, 749.00, 0.00, 1498.00),   -- Venta 2025-000027
(20, 11, 2, 79.00, 0.00, 158.00),
(21, 10, 5, 109.00, 0.00, 545.00),   -- Venta 2025-000028
(21, 12, 1, 399.00, 0.00, 399.00),
(22, 5, 2, 649.00, 0.00, 1298.00);   -- Venta 2025-000029

-- =====================================================
-- 7. CONFIGURACIÓN DEL SISTEMA
-- =====================================================
INSERT INTO configuracion_sistema (clave, valor, descripcion, tipo) VALUES
('nombre_empresa', 'ERP Inteligente SA', 'Nombre de la empresa', 'string'),
('iva_defecto', '21', 'IVA por defecto (%)', 'number'),
('dias_vencimiento_facturas', '30', 'Días para vencimiento de facturas', 'number'),
('moneda', 'EUR', 'Moneda del sistema', 'string'),
('stock_alerta_critica', '5', 'Stock para alerta crítica', 'number'),
('email_notificaciones', 'admin@erp.com', 'Email para notificaciones', 'string');

-- =====================================================
-- RESUMEN DE DATOS INSERTADOS
-- =====================================================
-- ✅ 5 usuarios (admin, 2 vendedores, 1 almacén, 1 gerente)
-- ✅ 7 categorías de productos
-- ✅ 15 clientes (3 VIP, 7 regulares, 3 inactivos, 2 particulares)
-- ✅ 25 productos (varios con stock bajo/crítico)
-- ✅ 23 ventas (3 hoy, 3 ayer, resto semanas anteriores)
-- ✅ 4 facturas pendientes (3 vencidas, 1 por vencer)
-- ✅ 44 líneas de venta con productos variados
-- ✅ 6 configuraciones del sistema

-- Las alertas se crearán automáticamente por los TRIGGERS al insertar ventas
-- Los totales de clientes se actualizarán automáticamente por los TRIGGERS

SELECT '✅ DATOS DE PRUEBA INSERTADOS CORRECTAMENTE' AS mensaje;
SELECT CONCAT('Total clientes: ', COUNT(*)) AS info FROM clientes;
SELECT CONCAT('Total productos: ', COUNT(*)) AS info FROM productos;
SELECT CONCAT('Total ventas: ', COUNT(*)) AS info FROM ventas;
SELECT CONCAT('Productos con stock bajo: ', COUNT(*)) AS info FROM productos WHERE stock_actual < stock_minimo;
