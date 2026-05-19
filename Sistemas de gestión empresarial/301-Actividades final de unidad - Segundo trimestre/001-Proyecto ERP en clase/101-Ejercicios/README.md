# ⚽ TotalKit ERP - Sistema de Gestión de Camisetas de Fútbol

## 📋 Descripción del Proyecto

**TotalKit ERP** es un sistema de gestión empresarial (ERP) desarrollado para la administración de una tienda online especializada en camisetas de fútbol. Este proyecto es una versión personalizada basada en los ejercicios de clase, adaptado específicamente para el comercio de camisetas de equipos profesionales y selecciones nacionales.

## 🎯 Temática y Diferenciación

A diferencia del proyecto de clase que manejaba una tienda online genérica, **TotalKit ERP** está especializado en:

- **Camisetas de clubes** (Real Madrid, Barcelona, Manchester United, etc.)
- **Camisetas de selecciones** (España, Brasil, Argentina, etc.)
- **Diferentes equipaciones** (titular, suplente, tercera)
- **Versiones personalizadas** con nombres y números de jugadores
- **Múltiples temporadas** y tallas

## ✨ Funcionalidades Principales

### 🔐 Sistema de Autenticación
- Login seguro con sesiones PHP
- Control de acceso al sistema
- Usuario: `admin` / Contraseña: `admin123`

### 📊 Dashboard Interactivo
- **Estadísticas en tiempo real:**
  - Total de camisetas en inventario
  - Número de clientes registrados
  - Cantidad de pedidos procesados
  - Ingresos totales generados

- **Gráficos visuales:**
  - Distribución de camisetas por equipo (donut chart)
  - Estado de pedidos (donut chart)

- **Listados destacados:**
  - Camisetas destacadas del catálogo

### 🗃️ Gestión de Datos
- **CRUD completo** para todas las tablas:
  - Productos (camisetas con especificaciones)
  - Equipos y ligas
  - Marcas deportivas
  - Clientes y direcciones
  - Pedidos y artículos
  - Métodos de pago y envío
  - Reseñas de productos

### 👕 Características Específicas de Camisetas de Fútbol

#### Para Camisetas:
- Equipo o selección
- Temporada (2024/25, 2025/26, etc.)
- Tipo de equipación (titular, suplente, tercera, portero)
- Talla (XS, S, M, L, XL, XXL)
- Jugador y número de dorsal (opcional)
- Versión jugador o aficionado
- Manga corta o larga
- Parches de competiciones
- Material (poliéster, reciclado, etc.)
- Código de producto único

#### Para Equipos:
- Nombre completo del equipo
- Liga o competición
- País
- Año de fundación
- Estadio
- Diferenciación entre club y selección

#### Para Marcas:
- Nike, Adidas, Puma, New Balance, etc.
- País de origen
- Sitio web oficial

## 🗄️ Estructura de Base de Datos

### Tablas Principales:
1. **productos** - Catálogo de camisetas de fútbol
2. **equipos** - Equipos y selecciones
3. **ligas** - Competiciones y ligas
4. **marcas** - Fabricantes de camisetas
5. **clientes** - Información de clientes (con equipo favorito)
6. **pedidos** - Órdenes de compra
7. **articulos_pedido** - Detalles de productos en cada pedido

### Tablas de Referencia:
- **temporadas** - Temporadas futbolísticas (2024/25, etc.)
- **tallas** - Tallas disponibles (XS a XXL)
- **tipos_camiseta** - Tipos de equipación
- **estados_pedido** - Estados del flujo de pedidos
- **metodos_pago** - Formas de pago disponibles
- **metodos_envio** - Opciones de envío
- **paises** - Catálogo de países

### Tablas Relacionadas:
- **direcciones** - Direcciones de envío de clientes
- **imagenes_producto** - Galería de imágenes por producto
- **resenas_producto** - Reseñas y calificaciones

### Vistas Útiles:
- `vista_productos_completa` - Información completa de productos con joins
- `vista_pedidos_detalle` - Detalles completos de pedidos
- `vista_equipos_mas_vendidos` - Ranking de equipos más populares

## 🎨 Diseño y Estilos

El sistema cuenta con un diseño moderno y deportivo:

### Características Visuales:
- **Esquema de colores**: Verde césped, amarillo y blanco (temática futbolística)
- **Tipografía**: Inter (Google Fonts) para legibilidad óptima
- **Componentes modernos**:
  - Cards con sombras y efectos hover
  - Gráficos SVG interactivos (donut charts)
  - Formularios intuitivos con validación visual
  - Tablas responsivas con diseño limpio
  - Sidebar navegación verde oscuro con gradientes

### Efectos Especiales:
- Animaciones de entrada (fade-in, slide-up)
- Transiciones suaves en hover
- Scrollbar personalizado
- Gradientes verdes en botones y fondos
- Sombras dinámicas

### Responsive Design:
- Adaptable a dispositivos móviles
- Grid system flexible
- Sidebar colapsable en móviles

## 🚀 Instalación y Configuración

### Requisitos Previos:
- PHP 7.4 o superior
- MySQL 5.7 o superior
- Servidor web (Apache/XAMPP recomendado)

### Pasos de Instalación:

1. **Configurar la base de datos:**
   ```sql
   -- Crear la base de datos
   CREATE DATABASE tienda_camisetas CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   
   -- Ejecutar el script de creación
   SOURCE base_datos.sql;
   ```

2. **Configurar credenciales:**
   Editar `index.php` líneas 7-10:
   ```php
   $db_host = "localhost";
   $db_name = "tienda_camisetas";
   $db_user = "root";  // Tu usuario MySQL
   $db_pass = "";      // Tu contraseña MySQL
   ```

3. **Colocar archivos:**
   - Copiar todos los archivos en la carpeta del servidor web
   - Para XAMPP: `C:\xampp\htdocs\totalkit\`

4. **Acceder al sistema:**
   - Abrir navegador: `http://localhost/totalkit/`
   - Usuario: `admin`
   - Contraseña: `admin123`

## 📁 Estructura de Archivos

```
101-Ejercicios/
│
├── index.php           # Archivo principal del sistema
├── estilos.css        # Hoja de estilos
├── base_datos.sql     # Script de base de datos
├── README.md          # Esta documentación
├── ejercicio.md       # Resumen del ejercicio
└── INSTALACION.md     # Guía de instalación
```

## 🔧 Funciones PHP Principales

### Funciones de Metadatos:
- `obtener_claves_foraneas()` - Detecta relaciones entre tablas
- `obtener_meta_columnas()` - Obtiene información de columnas
- `obtener_pk_columna()` - Identifica clave primaria

### Funciones de Renderizado:
- `render_input_para_columna()` - Genera inputs según tipo de dato
- `render_tabla_html()` - Crea tablas HTML dinámicas
- `render_pie_chart()` - Genera gráficos SVG tipo donut

## 📈 Características Avanzadas

### 1. **Generación Dinámica de Formularios**
El sistema detecta automáticamente:
- Tipos de datos de cada columna
- Relaciones de claves foráneas
- Campos auto-incrementales
- Restricciones y validaciones

### 2. **Gestión Inteligente de Relaciones**
- Detecta foreign keys automáticamente
- Renderiza selects con datos relacionados
- Muestra información contextual en tablas

### 3. **Visualización de Datos**
- Gráficos SVG sin dependencias externas
- Tablas con scroll horizontal para móviles
- Colores dinámicos en gráficos

## 🎯 Mejoras Funcionales vs Proyecto de Clase

### Modificaciones en Base de Datos:
1. **Campos especializados** para camisetas de fútbol
2. **Tablas específicas** (equipos, ligas, temporadas, tallas)
3. **Relaciones complejas** entre equipos, ligas y países
4. **Control de versiones** (jugador vs aficionado)
5. **Tres vistas SQL** para consultas optimizadas

### Modificaciones en Código PHP:
1. **Mejor manejo de sesiones** y seguridad
2. **Funciones modulares** y reutilizables
3. **Generación dinámica** más robusta
4. **Consultas específicas** para camisetas por equipo
5. **Manejo de errores** mejorado

### Modificaciones Visuales:
1. **Paleta de colores** temática de fútbol (verde césped)
2. **Iconos emoji** deportivos (⚽, 👕, 🏆)
3. **Animaciones CSS** suaves
4. **Layouts responsivos** mejorados
5. **Gradientes verdes** y sombras deportivas

## 🔄 Flujo de Trabajo del Sistema

1. **Login** → Validación de credenciales
2. **Dashboard** → Vista general de estadísticas
3. **Navegación** → Selección de tabla a gestionar
4. **Gestión** → Inserción y visualización de datos
5. **Informes** → Consulta de datos con gráficos

## 🛡️ Seguridad

- Prevención de SQL Injection con `mysqli_real_escape_string()`
- Validación de sesiones PHP
- Escape de HTML con `htmlspecialchars()`
- Control de acceso basado en sesiones

## 📊 Datos de Ejemplo Incluidos

La base de datos incluye datos reales de prueba:
- 16 equipos famosos (Real Madrid, Barcelona, Manchester United, etc.)
- 18 camisetas en múltiples tallas y versiones
- 4 clientes con direcciones
- 3 pedidos completados
- 5 reseñas de productos
- 8 marcas deportivas
- 7 ligas/competiciones

## 🎓 Aspectos Evaluables

### 1. Modificaciones Funcionales:
- ✅ Base de datos especializada en camisetas de fútbol
- ✅ Campos técnicos específicos del dominio
- ✅ Relaciones complejas entre tablas
- ✅ Tres vistas SQL para optimización
- ✅ Sistema CRUD completo y funcional
- ✅ Gráficos específicos por equipo

### 2. Modificaciones Estéticas:
- ✅ Diseño completamente renovado
- ✅ Paleta de colores temática (verde césped)
- ✅ Componentes modernos (cards, charts)
- ✅ Animaciones y transiciones
- ✅ Responsive design

### 3. Calidad del Código:
- ✅ Código comentado en español
- ✅ Funciones modulares y reutilizables
- ✅ Buenas prácticas PHP
- ✅ Organización clara del proyecto

### 4. Documentación:
- ✅ README completo
- ✅ Comentarios en código
- ✅ Instrucciones de instalación
- ✅ Descripción de funcionalidades

## 🚀 Posibles Mejoras Futuras

- [ ] Sistema de búsqueda avanzada por equipo/jugador
- [ ] Filtros por liga, temporada, talla
- [ ] Comparador de precios entre camisetas
- [ ] Sistema de carrito de compras
- [ ] Integración con APIs de equipos
- [ ] Gestión de stock con alertas por talla
- [ ] Reportes PDF de ventas por equipo
- [ ] Sistema de roles (admin, vendedor, cliente)
- [ ] Galería de imágenes de camisetas
- [ ] Wishlist de equipos favoritos

## 👨‍💻 Autor

Sistema desarrollado como ejercicio final de evaluación para el módulo de Sistemas de Gestión Empresarial (SGE) - DAM 2º curso.

---

## 📝 Notas Adicionales

Este proyecto representa una **versión inicial básica** del sistema ERP, diseñada para ser mejorada progresivamente tanto en funcionalidad como en estilos visuales. El código está estructurado de manera modular para facilitar futuras ampliaciones.

La temática de **camisetas de fútbol** permite incorporar características especiales como:
- Gestión de versiones (jugador vs aficionado)
- Control de tallas y stock
- Temporadas deportivas
- Diferenciación entre clubes y selecciones
- Personalización con jugadores y dorsales

## 🎯 Cumplimiento de Criterios

### Respeta la temática de clase ✅
- Clase: Tienda online genérica
- Personal: Tienda online de camisetas de fútbol

### Modificaciones estéticas ✅
- Diseño completamente renovado
- Colores temáticos (verde césped, amarillo)
- Iconos deportivos (⚽, 👕, 🏆)
- Animaciones y efectos visuales modernos

### Modificaciones funcionales importantes ✅
- Base de datos especializada en fútbol
- Campos técnicos específicos (tallas, temporadas, equipaciones)
- Vistas SQL optimizadas
- Sistema completo de gestión

---

**¡El sistema está listo para gestionar tu tienda de camisetas de fútbol! ⚽👕🏆**
