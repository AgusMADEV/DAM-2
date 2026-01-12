# Actividad Evaluable - Backoffice Empresarial

## Descripción del Proyecto

Aplicación web para un backoffice empresarial que incluye un sistema de login seguro y navegación completa entre diferentes secciones.

## Estructura del Proyecto

```
102-Actividad EVAL/
│
├── login.php           # Página de inicio de sesión
├── maestro.php         # Página principal que integra todos los componentes
├── README.md          # Este archivo
│
└── componentes/
    ├── login.php      # Componente del formulario de login con validación
    ├── menu.php       # Componente de menú de navegación lateral
    └── layout.php     # Componente de diseño general con header, menú y contenido
```

## Características Implementadas

### 1. Sistema de Login Seguro (login.php)
- ✅ Formulario con campos de usuario y contraseña
- ✅ Validación de campos en tiempo real
- ✅ Diseño limpio y moderno con estilos CSS
- ✅ Mensajes de error claros para el usuario
- ✅ Prevención de envío de formulario vacío
- ✅ Redirección automática tras login exitoso

### 2. Navegación Empresarial (menu.php)
- ✅ Menú lateral con 8 opciones de navegación:
  - Dashboard
  - Clientes
  - Productos
  - Ventas
  - Informes
  - Configuración
  - Usuarios
  - Cerrar Sesión
- ✅ Indicador visual de sección activa
- ✅ Efectos hover y transiciones suaves
- ✅ Confirmación antes de cerrar sesión

### 3. Layout Principal (layout.php)
- ✅ **Variables PHP integradas:**
  - `$tituloPagina`: Título de la aplicación
  - `$usuarioActual`: Usuario que ha iniciado sesión
  - `$seccionActual`: Sección actualmente visitada
- ✅ Header con información del usuario conectado
- ✅ Diseño responsive con flexbox
- ✅ Área de contenido principal dinámica
- ✅ Footer con información de copyright
- ✅ Estilos modernos y profesionales

### 4. Archivo Maestro (maestro.php)
- ✅ Integra todos los componentes
- ✅ Define variables PHP globales
- ✅ Estructura HTML5 válida
- ✅ Meta tags para responsive design

## Uso de la Aplicación

### Acceso al Sistema

1. **Iniciar la aplicación:**
   - Abrir en el navegador: `http://localhost/DAM-2/.../102-Actividad EVAL/login.php`

2. **Iniciar sesión:**
   - Ingresar usuario (cualquier nombre para propósitos de demostración)
   - Ingresar contraseña
   - Hacer clic en "Iniciar Sesión"

3. **Navegar por el backoffice:**
   - Utilizar el menú lateral para acceder a diferentes secciones
   - El sistema mostrará el nombre del usuario en el header
   - Cada sección actualiza la URL con parámetros GET

### Acceso Directo al Panel Principal

También se puede acceder directamente al panel:
```
http://localhost/.../102-Actividad EVAL/maestro.php?usuario=Admin&seccion=dashboard
```

## Variables PHP Implementadas

El proyecto utiliza variables PHP para gestionar información relevante:

```php
// En layout.php
$tituloPagina = "Backoffice Empresarial";
$usuarioActual = $_GET['usuario'] ?? "Invitado";
$seccionActual = $_GET['seccion'] ?? "Dashboard";
```

Estas variables permiten:
- Personalizar el título de cada página
- Mostrar el nombre del usuario conectado
- Identificar la sección actual
- Mantener el contexto de navegación

## Validaciones de Seguridad

- ✅ Uso de `htmlspecialchars()` para prevenir XSS
- ✅ Validación de campos en frontend con JavaScript
- ✅ Prevención de envío de formularios vacíos
- ✅ Encoding de URLs con `encodeURIComponent()`

## Características de Diseño

### Colores y Estilos
- Paleta de colores profesional (púrpura y tonos oscuros)
- Gradientes modernos
- Sombras sutiles para profundidad
- Transiciones suaves en interacciones

### Usabilidad
- Diseño responsive
- Feedback visual en hover
- Mensajes de error claros
- Confirmaciones para acciones críticas

## Restricciones Cumplidas

✅ **No se utilizaron librerías externas** - Todo el código es nativo PHP, HTML, CSS y JavaScript

✅ **Código dentro del tema actual** - Se siguió la estructura de los apuntes de la carpeta 101-Ejercicios

## Tecnologías Utilizadas

- **PHP**: Para variables y lógica del servidor
- **HTML5**: Estructura semántica
- **CSS3**: Estilos modernos con flexbox y gradientes
- **JavaScript**: Validación y navegación dinámica

## Mejoras Implementadas vs Apuntes

Comparado con los archivos de referencia en la carpeta 101-Ejercicios:

1. ✅ Validación completa del formulario
2. ✅ Variables PHP con valores por defecto
3. ✅ Sanitización de datos con `htmlspecialchars()`
4. ✅ Menú con opciones empresariales específicas
5. ✅ Header y footer informativos
6. ✅ Gestión de estados activos en el menú
7. ✅ Diseño más profesional y completo
8. ✅ Documentación completa del proyecto

## Autor

Desarrollado como actividad evaluable para el módulo de Desarrollo de Interfaces.

---

**Fecha de entrega:** Enero 2026
