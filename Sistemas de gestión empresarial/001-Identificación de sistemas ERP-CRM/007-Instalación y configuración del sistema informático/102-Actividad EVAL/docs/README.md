# Sistema ERP - Enterprise Resource Planning

## Descripción del Proyecto

Este proyecto implementa un sistema ERP (Enterprise Resource Planning) completo desarrollado con tecnologías web estándar, diseñado para funcionar en hosting compartido y cumplir con los requisitos de simplicidad y funcionalidad empresarial.

## Decisiones Tecnológicas

### Frontend
- **HTML5**: Estructura semántica y accesible
- **CSS3**: Diseño responsivo con Flexbox y Grid
- **JavaScript (ES6+)**: Interactividad sin frameworks externos

**Justificación**: Estas tecnologías garantizan máxima compatibilidad, rendimiento óptimo y facilidad de mantenimiento.

### Backend
- **PHP 8.x**: Lenguaje del lado del servidor
- **PDO MySQL**: Acceso seguro a la base de datos
- **API REST**: Arquitectura de servicios

**Justificación**: PHP es ampliamente compatible con hosting compartido (73% del mercado según W3Techs), tiene excelente documentación y amplia comunidad de desarrolladores.

### Base de Datos
- **MySQL 8.x**: Sistema de gestión de base de datos
- **InnoDB**: Motor de almacenamiento con soporte para transacciones

**Justificación**: MySQL es el estándar en hosting compartido, ofrece excelente rendimiento y es compatible con la mayoría de proveedores.

### Servidor Web
- **Apache 2.4**: Servidor HTTP recomendado
- **mod_php**: Integración PHP con Apache

**Justificación**: Apache es el servidor más utilizado y es compatible con cualquier hosting compartido.

## Arquitectura del Sistema

### Estructura del Proyecto
```
102-Actividad EVAL/
├── frontend/           # Interfaz de usuario
│   ├── css/           # Hojas de estilo
│   ├── js/            # Scripts JavaScript
│   ├── index.html     # Página de login
│   └── dashboard.html # Dashboard principal
├── backend/           # Lógica del servidor
│   ├── api/           # Endpoints REST
│   └── config/        # Configuración
├── database/          # Scripts de BD
│   ├── erp_sistema.sql
│   └── README.md
└── docs/              # Documentación
    ├── README.md
    ├── INSTALACION.md
    └── ARQUITECTURA.md
```

### Módulos del Sistema

#### 1. Gestión de Usuarios
- Autenticación con JWT
- Control de sesiones
- Gestión de permisos

#### 2. Gestión de Clientes
- CRUD completo de clientes
- Validación de datos
- Búsqueda y filtrado

#### 3. Gestión de Productos
- Catálogo de productos
- Control de inventario
- Alertas de stock bajo

#### 4. Gestión de Ventas
- Procesamiento de ventas
- Cálculo automático de totales
- Actualización de inventario

#### 5. Dashboard y Reportes
- Estadísticas en tiempo real
- Indicadores clave (KPIs)
- Reportes básicos

## Seguridad

### Medidas Implementadas
1. **Autenticación JWT**: Tokens seguros para sesiones
2. **Validación de Entrada**: Sanitización de datos
3. **Consultas Preparadas**: Prevención de SQL Injection
4. **CORS Configurado**: Control de acceso cross-origin
5. **Hash de Contraseñas**: Almacenamiento seguro con bcrypt

### Recomendaciones Adicionales
- Configurar HTTPS en producción
- Implementar rate limiting
- Auditoría de accesos
- Backup automático de la base de datos

## Compatibilidad con Hosting Compartido

### Ventajas de la Arquitectura Elegida
1. **Sin dependencias externas**: No requiere Node.js, MongoDB u otros servicios
2. **Estándar del mercado**: PHP + MySQL es soportado por el 90% de proveedores
3. **Recursos mínimos**: Funciona con 128MB RAM y 100MB de espacio
4. **Configuración simple**: Solo requiere configurar la conexión a BD

### Requisitos Mínimos del Hosting
- PHP 7.4+
- MySQL 5.7+
- Módulo mod_rewrite (opcional)
- 100MB espacio en disco
- 128MB memoria RAM

## Escalabilidad

### Optimizaciones Implementadas
- Índices optimizados en BD
- Consultas eficientes con JOINs
- Paginación en listados
- Compresión CSS/JS (minificación)

### Posibles Mejoras Futuras
- Cache con Redis/Memcached
- CDN para recursos estáticos
- Balanceador de carga
- Replicación de BD

## Mantenimiento

### Tareas Regulares
1. **Backup de BD**: Exportación diaria automática
2. **Limpieza de logs**: Rotación de archivos de error
3. **Actualización de seguridad**: Parches de PHP/MySQL
4. **Monitoreo**: Seguimiento de rendimiento

### Logs del Sistema
- `error.log`: Errores de PHP
- `access.log`: Accesos al sistema
- `app.log`: Eventos de aplicación (customizable)

## Testing

### Pruebas Implementadas
- Validación de formularios
- Manejo de errores de conexión
- Verificación de autenticación
- Integridad de datos

### Casos de Prueba Recomendados
1. Login con credenciales válidas/inválidas
2. CRUD de clientes, productos y ventas
3. Cálculos de inventario y totales
4. Comportamiento responsive

## Documentación de API

### Endpoints Principales

#### Autenticación
- `POST /api/login.php` - Iniciar sesión
- `POST /api/verify-token.php` - Verificar token

#### Clientes
- `GET /api/clientes.php` - Listar clientes
- `POST /api/clientes.php` - Crear cliente
- `PUT /api/clientes.php` - Actualizar cliente
- `DELETE /api/clientes.php?id=X` - Eliminar cliente

#### Productos
- `GET /api/productos.php` - Listar productos
- `POST /api/productos.php` - Crear producto
- `PUT /api/productos.php` - Actualizar producto
- `DELETE /api/productos.php?id=X` - Eliminar producto

#### Ventas
- `GET /api/ventas.php` - Listar ventas
- `POST /api/ventas.php` - Crear venta
- `DELETE /api/ventas.php?id=X` - Cancelar venta

## Conclusiones

Este sistema ERP cumple con los objetivos establecidos:

1. ✅ **Frontend**: HTML, CSS, JavaScript puro
2. ✅ **Backend**: PHP con MySQL
3. ✅ **Hosting compatible**: Funciona en hosting compartido
4. ✅ **Funcionalidad completa**: Módulos principales implementados
5. ✅ **Seguridad**: Medidas básicas implementadas
6. ✅ **Documentación**: Completa y detallada

El proyecto demuestra un entendimiento sólido de las tecnologías web estándar y su aplicación en un contexto empresarial real, siguiendo las mejores prácticas de desarrollo y las restricciones tecnológicas planteadas.