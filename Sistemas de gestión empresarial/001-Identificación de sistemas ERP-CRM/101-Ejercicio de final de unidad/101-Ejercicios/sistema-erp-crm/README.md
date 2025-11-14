# Sistema de Gestión de Gimnasio 🏋️

## 📋 Descripción

Sistema de gestión integral para gimnasios que integra funcionalidades ERP (Enterprise Resource Planning) y CRM (Customer Relationship Management) desarrollado como proyecto final de la unidad "Identificación de sistemas ERP-CRM".

Este sistema combina conocimientos de múltiples asignaturas del ciclo DAM-2:
- **Sistemas de gestión empresarial**: Conceptos ERP-CRM, gestión de procesos empresariales
- **Acceso a datos**: Base de datos SQLite, modelos de datos, operaciones CRUD
- **Desarrollo de interfaces**: Interfaz web responsive, diseño UX/UI
- **Programación de servicios y procesos**: API REST, arquitectura cliente-servidor

## 🎯 Objetivos del Proyecto

### Objetivos Pedagógicos
1. **Identificar características de sistemas ERP-CRM**: Implementar módulos de gestión de socios, entrenadores, clases y membresías
2. **Aplicar acceso a datos**: Diseñar y implementar base de datos relacional con SQLite
3. **Desarrollar interfaces de usuario**: Crear interfaz web profesional y responsive
4. **Integrar servicios**: Conectar frontend y backend mediante API REST

### Objetivos Funcionales
- Gestión completa de socios (CRM)
- Administración de entrenadores y su disponibilidad
- Control de clases grupales y reservas
- Sistema de membresías con renovaciones
- Registro de asistencias al gimnasio
- Generación de informes y analíticas

## 🏗️ Arquitectura del Sistema

```
sistema-erp-crm/
├── backend/                    # Servidor API REST (Flask)
│   └── app.py                 # Aplicación principal del servidor
├── database/                   # Módulo de acceso a datos
│   ├── database.py            # Gestor de base de datos SQLite
│   └── models.py              # Modelos de datos (Cliente, Producto, Venta)
├── frontend/                   # Interfaz web
│   ├── index.html             # Página principal
│   ├── style.css              # Estilos CSS responsive
│   └── script.js              # Lógica JavaScript (SPA)
└── requirements.txt           # Dependencias Python
```

### Tecnologías Utilizadas

#### Backend (Programación de Servicios)
- **Python 3.x**: Lenguaje principal
- **Flask**: Framework web para API REST
- **SQLite**: Base de datos relacional integrada
- **Flask-CORS**: Manejo de CORS para frontend

#### Frontend (Desarrollo de Interfaces)
- **HTML5**: Estructura semántica
- **CSS3**: Estilos modernos con Grid/Flexbox
- **JavaScript ES6+**: Programación funcional y OOP
- **Font Awesome**: Iconografía

#### Base de Datos (Acceso a Datos)
- **SQLite**: Base de datos relacional
- **Modelo relacional**: Tablas normalizadas
- **Operaciones CRUD**: Create, Read, Update, Delete

## 🗄️ Modelo de Datos

### Entidades Principales

#### 👥 Clientes (CRM)
```sql
clientes:
- id (PK)
- nombre, apellidos
- email, telefono
- direccion, ciudad, codigo_postal
- fecha_registro, estado
```

#### 📦 Productos (ERP)
```sql
productos:
- id (PK)
- codigo (UNIQUE), nombre
- descripcion, categoria
- precio, stock, stock_minimo
- activo, fecha_creacion
```

#### 🛒 Ventas
```sql
ventas:
- id (PK)
- cliente_id (FK), usuario_id (FK)
- fecha, total, estado
```

#### 📋 Detalle de Ventas
```sql
detalle_ventas:
- id (PK)
- venta_id (FK), producto_id (FK)
- cantidad, precio_unitario, subtotal
```

#### 👤 Usuarios del Sistema
```sql
usuarios:
- id (PK)
- nombre, email, password_hash
- rol, fecha_creacion
```

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes Python)
- Navegador web moderno

### Pasos de Instalación

1. **Navegar al directorio del proyecto**
   ```bash
   cd sistema-erp-crm
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Inicializar la base de datos** (opcional, se crea automáticamente)
   ```bash
   python database/database.py
   ```

4. **Ejecutar el servidor**
   ```bash
   python backend/app.py
   ```

5. **Acceder al sistema**
   - Abrir navegador en: `http://localhost:5000`
   - Usuario por defecto: `admin@empresa.com` / `admin123`

## 💻 Uso del Sistema

### Dashboard Principal
- **Métricas clave**: Clientes, productos, ventas, ingresos
- **Alertas del sistema**: Stock bajo, notificaciones importantes
- **Vista ejecutiva**: Resumen del estado empresarial

### Módulo CRM - Clientes
- ➕ **Crear cliente**: Formulario completo con validaciones
- 👁️ **Consultar clientes**: Lista paginada con filtros
- ✏️ **Editar cliente**: Actualización de datos en tiempo real
- 🗑️ **Eliminar cliente**: Con confirmación de seguridad

### Módulo ERP - Productos
- 📦 **Gestión de inventario**: Control de stock en tiempo real
- 🏷️ **Categorización**: Organización por categorías
- ⚠️ **Alertas de stock**: Notificaciones automáticas de stock bajo
- 💰 **Control de precios**: Gestión de precios y márgenes

### Sistema de Ventas
- 🛒 **Nueva venta**: Proceso guiado de venta
- 📊 **Historial de ventas**: Registro completo de transacciones
- 📄 **Detalle de venta**: Vista detallada de cada transacción
- 🔄 **Estados de venta**: Seguimiento del estado (pendiente, completada)

### Informes y Analíticas
- 📈 **Ventas por mes**: Evolución temporal de ingresos
- 📦 **Productos con stock bajo**: Control de inventario
- 🏆 **Top clientes**: Ranking por volumen de compras
- 📊 **Métricas ejecutivas**: KPIs del negocio

## 🔧 API REST - Endpoints

### Clientes
```
GET    /api/clientes              # Listar todos los clientes
GET    /api/clientes/{id}         # Obtener cliente específico
POST   /api/clientes              # Crear nuevo cliente
PUT    /api/clientes/{id}         # Actualizar cliente
```

### Productos
```
GET    /api/productos             # Listar todos los productos
POST   /api/productos             # Crear nuevo producto
PUT    /api/productos/{id}/stock  # Actualizar stock
```

### Ventas
```
GET    /api/ventas                # Listar todas las ventas
POST   /api/ventas                # Crear nueva venta
GET    /api/ventas/{id}/detalle   # Detalle de venta específica
```

### Informes
```
GET    /api/informes/dashboard         # Métricas del dashboard
GET    /api/informes/ventas-mes        # Ventas por mes
GET    /api/informes/stock-bajo        # Productos con stock bajo
GET    /api/informes/top-clientes      # Top clientes
```

### Sistema
```
GET    /api/status                     # Estado del sistema
```

## 🎨 Características de la Interfaz

### Diseño Responsive
- **Desktop**: Layout completo con sidebar y contenido principal
- **Tablet**: Adaptación optimizada para pantallas medianas
- **Mobile**: Interfaz compacta y navegación touch-friendly

### Experiencia de Usuario (UX)
- **Navegación intuitiva**: Sidebar con iconos descriptivos
- **Feedback visual**: Notificaciones, alertas y confirmaciones
- **Estados de carga**: Indicadores de progreso y spinners
- **Validación de formularios**: Feedback en tiempo real

### Interfaz de Usuario (UI)
- **Paleta de colores profesional**: Azules corporativos
- **Tipografía clara**: Segoe UI para legibilidad
- **Iconografía consistente**: Font Awesome
- **Animaciones sutiles**: Transiciones CSS suaves

## 📊 Características ERP-CRM

### Funcionalidades ERP (Enterprise Resource Planning)
1. **Gestión de Inventario**
   - Control de stock en tiempo real
   - Alertas automáticas de stock mínimo
   - Categorización de productos
   - Seguimiento de precios y costos

2. **Gestión de Ventas**
   - Registro de transacciones
   - Cálculo automático de totales
   - Control de estados de venta
   - Historial completo de operaciones

3. **Reporting y Analíticas**
   - Informes de ventas por período
   - Análisis de productos más vendidos
   - Métricas de rendimiento empresarial

### Funcionalidades CRM (Customer Relationship Management)
1. **Gestión de Clientes**
   - Base de datos completa de clientes
   - Historial de interacciones
   - Segmentación por ubicación geográfica
   - Estados del cliente (activo, inactivo)

2. **Análisis de Clientes**
   - Top clientes por volumen de compras
   - Análisis de comportamiento de compra
   - Seguimiento de la relación comercial

## 🔒 Seguridad

- **Autenticación**: Sistema de usuarios con hash de contraseñas (SHA256)
- **Validación de datos**: Validación en frontend y backend
- **Prevención de SQL Injection**: Uso de parámetros preparados
- **CORS configurado**: Control de acceso desde dominios específicos

## 🧪 Testing y Calidad

### Datos de Prueba
El sistema incluye datos de ejemplo para facilitar las pruebas:
- 3 clientes de prueba
- 4 productos con diferentes estados de stock
- 3 ventas de ejemplo
- Usuario administrador: `admin@empresa.com` / `admin123`

### Validaciones Implementadas
- Campos obligatorios en formularios
- Validación de tipos de datos
- Verificación de rangos (precios, stock)
- Confirmaciones para operaciones destructivas

## 📚 Conocimientos Aplicados

### Sistemas de Gestión Empresarial
- ✅ Identificación de procesos ERP y CRM
- ✅ Integración de módulos empresariales
- ✅ Workflow de gestión de clientes y productos
- ✅ Generación de informes ejecutivos

### Acceso a Datos
- ✅ Diseño de base de datos relacional
- ✅ Normalización de tablas
- ✅ Operaciones CRUD completas
- ✅ Integridad referencial con claves foráneas
- ✅ Consultas complejas con JOIN

### Desarrollo de Interfaces
- ✅ Diseño responsive con CSS Grid/Flexbox
- ✅ Interfaz web moderna y profesional
- ✅ Programación JavaScript orientada a objetos
- ✅ Gestión de estados de aplicación
- ✅ Formularios dinámicos con validación

### Programación de Servicios
- ✅ API REST con Flask
- ✅ Arquitectura cliente-servidor
- ✅ Manejo de peticiones HTTP
- ✅ Serialización JSON
- ✅ Control de errores y excepciones

## 🚧 Posibles Mejoras Futuras

### Funcionalidades Adicionales
- [ ] Sistema de facturación
- [ ] Integración con pasarelas de pago
- [ ] Módulo de contabilidad
- [ ] Sistema de notificaciones email
- [ ] Backup automático de datos
- [ ] API de integración con sistemas externos

### Aspectos Técnicos
- [ ] Autenticación JWT
- [ ] Base de datos PostgreSQL/MySQL
- [ ] Deployment con Docker
- [ ] Tests automatizados
- [ ] Logs del sistema
- [ ] Caché con Redis

## 📄 Licencia

Este proyecto es desarrollado con fines educativos para el ciclo DAM-2. Libre uso para aprendizaje y enseñanza.

## 👨‍💻 Autor

Desarrollado como proyecto final de la unidad "Identificación de sistemas ERP-CRM" - Sistemas de Gestión Empresarial.

---

**Fecha de creación**: Noviembre 2024  
**Versión**: 1.0.0  
**Estado**: Proyecto educativo completo