-- =============================================
-- INSTRUCCIONES DE INSTALACIÓN RÁPIDA
-- TotalKit ERP - Sistema de Gestión
-- =============================================

-- PASO 1: Ejecuta este script en MySQL para crear el usuario
-- (Puedes hacerlo desde phpMyAdmin o desde la línea de comandos)

-- Crear usuario para el ERP (ajusta la contraseña si lo deseas)
CREATE USER IF NOT EXISTS 'totalkit'@'localhost' IDENTIFIED BY 'totalkit';

-- Otorgar permisos completos sobre la base de datos
GRANT ALL PRIVILEGES ON tienda_camisetas.* TO 'totalkit'@'localhost';

-- Aplicar cambios
FLUSH PRIVILEGES;

-- Verificar que el usuario se creó correctamente
SELECT User, Host FROM mysql.user WHERE User = 'totalkit';

-- =============================================
-- PASO 2: Importa el archivo base_datos.sql
-- =============================================
-- Desde phpMyAdmin:
--   1. Selecciona "Importar"
--   2. Elige el archivo "base_datos.sql"
--   3. Haz clic en "Continuar"
--
-- Desde línea de comandos:
--   mysql -u root -p < base_datos.sql

-- =============================================
-- PASO 3: Configura config.php
-- =============================================
-- 1. Copia config_example.php a config.php
-- 2. Edita las credenciales si es necesario
-- 3. ¡Listo para usar!

-- =============================================
-- NOTAS:
-- =============================================
-- - Si ya existe el usuario 'totalkit', este script no dará error
-- - Puedes cambiar 'totalkit' por otro nombre de usuario
-- - Recuerda actualizar config.php con las mismas credenciales
-- - Para eliminar el usuario: DROP USER 'totalkit'@'localhost';
