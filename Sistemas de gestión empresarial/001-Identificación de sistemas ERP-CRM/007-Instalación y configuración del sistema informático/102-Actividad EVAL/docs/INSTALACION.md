# Guía de Instalación - Sistema ERP

## Requisitos del Sistema

### Servidor
- **Sistema Operativo**: Windows, Linux o macOS
- **Servidor Web**: Apache 2.4+ (recomendado) o Nginx
- **PHP**: Versión 7.4 o superior
- **MySQL**: Versión 5.7 o superior
- **Memoria RAM**: Mínimo 128MB, recomendado 512MB
- **Espacio en disco**: Mínimo 100MB

### Extensiones PHP Requeridas
- `pdo_mysql`: Conexión a MySQL
- `json`: Manejo de JSON
- `openssl`: Para hashing de contraseñas
- `session`: Gestión de sesiones

## Instalación Paso a Paso

### 1. Preparación del Entorno

#### En XAMPP (Desarrollo Local)
1. Descargar e instalar XAMPP desde https://www.apachefriends.org/
2. Iniciar Apache y MySQL desde el panel de control
3. Verificar que funciona accediendo a http://localhost

#### En Hosting Compartido
1. Subir archivos via FTP al directorio público (public_html/)
2. Verificar que PHP y MySQL estén disponibles
3. Anotar datos de conexión a la base de datos

### 2. Configuración de la Base de Datos

#### Opción A: phpMyAdmin (Recomendado)
1. Acceder a phpMyAdmin: http://localhost/phpmyadmin
2. Crear nueva base de datos llamada `erp_sistema`
3. Importar el archivo `database/erp_sistema.sql`
4. Verificar que se crearon todas las tablas

#### Opción B: Línea de Comandos
```bash
# Conectar a MySQL
mysql -u root -p

# Crear la base de datos
CREATE DATABASE erp_sistema;
USE erp_sistema;

# Importar el script
source /ruta/al/proyecto/database/erp_sistema.sql;
```

### 3. Configuración del Backend

#### Editar archivo de configuración
Abrir `backend/config/database.php` y modificar los parámetros de conexión:

```php
<?php
$host = "localhost";        // Dirección del servidor MySQL
$dbname = "erp_sistema";   // Nombre de la base de datos
$username = "root";        // Usuario de MySQL
$password = "";            // Contraseña de MySQL (vacía en XAMPP)
```

#### Para hosting compartido típico:
```php
<?php
$host = "localhost";
$dbname = "tu_usuario_erp_sistema";
$username = "tu_usuario_mysql";
$password = "tu_contraseña_mysql";
```

### 4. Configuración del Servidor Web

#### Apache (.htaccess)
Crear archivo `.htaccess` en la raíz del proyecto:
```apache
RewriteEngine On

# Redirigir al frontend por defecto
DirectoryIndex frontend/index.html

# Permitir CORS para desarrollo
Header always set Access-Control-Allow-Origin "*"
Header always set Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS"
Header always set Access-Control-Allow-Headers "Content-Type, Authorization"

# Seguridad básica
<Files "*.php">
    Order allow,deny
    Allow from all
</Files>

<Files "config.php">
    Order deny,allow
    Deny from all
</Files>
```

#### Nginx (configuración del servidor)
```nginx
server {
    listen 80;
    server_name tu-dominio.com;
    root /ruta/al/proyecto;
    index frontend/index.html;

    # Servir archivos estáticos
    location /frontend/ {
        try_files $uri $uri/ =404;
    }

    # API PHP
    location /backend/ {
        try_files $uri $uri/ =404;
        location ~ \.php$ {
            fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            include fastcgi_params;
        }
    }
}
```

### 5. Configuración de Permisos

#### Linux/macOS
```bash
# Dar permisos de escritura a logs (si existen)
chmod -R 755 /ruta/al/proyecto
chmod -R 644 /ruta/al/proyecto/backend/config/

# Para directorios de cache/logs (si se crean)
mkdir logs
chmod 777 logs
```

#### Windows
- Verificar que el usuario de Apache tenga permisos de lectura en todos los archivos
- Dar permisos de escritura a carpetas de logs si se implementan

### 6. Verificación de la Instalación

#### Paso 1: Verificar Base de Datos
1. Acceder a phpMyAdmin
2. Verificar que existen las tablas:
   - `usuarios`
   - `clientes` 
   - `productos`
   - `ventas`
   - `detalle_venta`

#### Paso 2: Probar Backend
Acceder a: `http://tu-dominio.com/backend/api/verify-token.php`
Debería devolver: `{"valid":false,"message":"Token no proporcionado"}`

#### Paso 3: Probar Frontend
1. Acceder a: `http://tu-dominio.com/frontend/index.html`
2. Debería aparecer la página de login
3. Usar credenciales por defecto:
   - **Usuario**: admin
   - **Contraseña**: admin123

#### Paso 4: Verificar Funcionalidad
1. Hacer login exitoso
2. Verificar que aparece el dashboard
3. Probar navegación entre módulos
4. Crear un cliente de prueba
5. Crear un producto de prueba
6. Realizar una venta de prueba

## Troubleshooting (Resolución de Problemas)

### Error: "Connection refused" o "Can't connect to database"
**Solución:**
1. Verificar que MySQL esté ejecutándose
2. Comprobar credenciales en `config/database.php`
3. Verificar que la base de datos existe

### Error: "CORS policy" en el navegador
**Solución:**
1. Verificar headers CORS en `config/database.php`
2. En desarrollo, usar herramientas como CORS Unblock
3. Verificar que el servidor permite CORS

### Error: "404 Not Found" en API
**Solución:**
1. Verificar que mod_rewrite está habilitado
2. Comprobar permisos de archivos PHP
3. Verificar rutas en JavaScript

### Error: "Session start failed"
**Solución:**
1. Verificar permisos de directorio temporal
2. Comprobar configuración PHP de sesiones
3. En hosting compartido, contactar soporte

### El frontend no se conecta al backend
**Solución:**
1. Verificar rutas en archivos JavaScript
2. Comprobar que las URLs del backend son correctas
3. Revisar la consola del navegador para errores

## Configuración para Producción

### Seguridad Adicional
1. **Cambiar credenciales por defecto**
2. **Configurar HTTPS**
3. **Ocultar información de PHP**:
   ```php
   // En php.ini
   expose_php = Off
   display_errors = Off
   ```

### Optimización
1. **Habilitar compresión gzip**
2. **Configurar cache de navegador**
3. **Minificar CSS/JS** (opcional)

### Backup
1. **Configurar backup automático de BD**
2. **Backup de archivos del sistema**
3. **Probar procedimiento de restauración**

## Soporte

Para problemas técnicos:
1. Revisar logs de error de Apache/PHP
2. Verificar configuración paso a paso
3. Consultar documentación oficial de PHP/MySQL
4. Contactar soporte del hosting si es necesario

---

**Última actualización**: Noviembre 2024  
**Versión**: 1.0  
**Compatibilidad**: PHP 7.4+, MySQL 5.7+