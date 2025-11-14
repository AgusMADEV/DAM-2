# Instalación del Sistema ERP

Este script instala la base de datos y crea los datos iniciales para el sistema ERP.

## Requisitos Previos
- MySQL 5.7 o superior
- PHP 7.4 o superior con extensión PDO-MySQL
- Servidor web (Apache recomendado)

## Instrucciones de Instalación

### 1. Configurar Base de Datos
```bash
# Conectar a MySQL como root
mysql -u root -p

# Ejecutar el script de instalación
source erp_sistema.sql

# O alternativamente:
mysql -u root -p < erp_sistema.sql
```

### 2. Configurar Conexión
Editar el archivo `backend/config/database.php` con los datos de conexión:

```php
$host = "localhost";
$dbname = "erp_sistema";
$username = "root";  // Cambiar por el usuario de BD
$password = "";      // Cambiar por la contraseña
```

### 3. Datos de Acceso por Defecto
- **Usuario:** admin
- **Contraseña:** admin123

## Estructura de la Base de Datos

### Tablas Principales
- `usuarios`: Gestión de usuarios del sistema
- `clientes`: Información de clientes
- `productos`: Catálogo de productos
- `ventas`: Registro de ventas
- `detalle_venta`: Detalles de cada venta

### Datos de Ejemplo
El script incluye:
- 1 usuario administrador
- 5 clientes de ejemplo
- 10 productos de ejemplo
- 5 ventas de ejemplo

## Verificación de Instalación
Después de ejecutar el script, verificar que se crearon las tablas:

```sql
USE erp_sistema;
SHOW TABLES;
SELECT COUNT(*) FROM usuarios;
SELECT COUNT(*) FROM clientes;
SELECT COUNT(*) FROM productos;
```