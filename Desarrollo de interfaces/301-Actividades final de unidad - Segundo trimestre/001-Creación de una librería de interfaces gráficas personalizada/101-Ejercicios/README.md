# 🎨 Ejercicio Personal - Librería de Interfaces Gráficas Personalizada

**Alumno:** Agust�n Mateo  
**Curso:** DAM 2 - Desarrollo de Interfaces  
**Actividad:** 301-001 Creación de una librería de interfaces gráficas personalizada  
**Fecha:** 17 de febrero de 2026

---

## 📋 Descripción del Proyecto

Este proyecto es una implementación personal del ejercicio de clase sobre creación de componentes de interfaz de usuario personalizados. El objetivo es demostrar el dominio sobre los elementos de interfaz gráfica existentes en HTML y CSS, y la capacidad de ampliar y personalizar estos elementos tanto desde un punto de vista visual como funcional.

El proyecto sigue la temática base del ejercicio trabajado en clase (la librería UILib), pero está desarrollado de forma independiente con una aproximación progresiva, comenzando con una versión básica y mejorándola gradualmente.

---

## 🎯 Objetivos del Ejercicio

1. **Demostrar control sobre elementos de interfaz de usuario:** Crear componentes que manejen correctamente HTML, CSS y JavaScript.

2. **Personalización visual y funcional:** Los componentes deben ser visualmente atractivos y funcionalmente útiles.

3. **Código reutilizable y modular:** Implementar patrones de diseño que permitan la reutilización en diferentes proyectos.

4. **Progresión incremental:** Desarrollar el ejercicio en versiones, comenzando simple y agregando complejidad.

---

## 📁 Estructura del Proyecto

```
301-Actividades final de unidad - Segundo trimestre/
└── 001-Creación de una librería de interfaces gráficas personalizada/
    └── 101-Ejercicios/
        ├── README.md (este archivo)
        ├── v1-basico/
        │   ├── README.md
        │   ├── agusmalab.css
        │   ├── agusmalab.js
        │   └── index.html
        └── v2-mejorado/
            ├── README.md
            ├── agusmalab.css
            ├── agusmalab.js
            └── index.html
```

---

## 📦 Versiones Desarrolladas

### Versión 1.0 - Básica

**Objetivo:** Crear los componentes fundamentales con funcionalidad básica.

**Componentes implementados:**
- ✅ **StatsCard** - Tarjetas de estadísticas visuales
- ✅ **SimpleTable** - Tabla HTML mejorada con estilos

**Características:**
- CSS con variables personalizables
- Patrón UMD para compatibilidad de módulos
- Diseño responsive básico
- Modo oscuro automático

**Ver carpeta:** `v1-basico/`

---

### Versión 2.0 - Mejorada

**Objetivo:** Agregar interactividad y nuevas funcionalidades.

**Componentes implementados:**
- ✅ **StatsCard Mejorada** - Con animaciones e indicadores de cambio
- ✅ **DataTable** - Tabla con búsqueda, ordenamiento y paginación
- ✅ **BarChart** - Gráfico de barras con Canvas

**Características nuevas:**
- 🔍 Búsqueda en tiempo real con normalización de texto
- 🔄 Ordenamiento ascendente/descendente por columnas
- 📄 Paginación con navegación completa
- 📊 Gráficos dinámicos con Canvas HTML5
- ✨ Animaciones y transiciones suaves
- 🎮 Métodos públicos para actualización dinámica
- 📈 Indicadores de cambio positivo/negativo

**Ver carpeta:** `v2-mejorado/`

---

## 🚀 Cómo Usar

### Instalación

1. Descargar los archivos de la versión deseada (v1-basico o v2-mejorado)
2. Incluir los archivos CSS y JS en tu HTML:

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <link rel="stylesheet" href="agusmalab.css">
</head>
<body>
  <div id="mi-componente"></div>
  
  <script src="agusmalab.js"></script>
  <script>
    new AgusmaLab.StatsCard('#mi-componente', {
      titulo: 'Usuarios',
      valor: '1,234'
    });
  </script>
</body>
</html>
```

### Ejemplos en Acción

Cada versión incluye un archivo `index.html` con ejemplos completos de uso de todos los componentes.

---

## 💡 Conceptos Aplicados del Curso

### De la Unidad 001 - Generación de interfaces de usuario
- ✅ Patrones de arquitectura (componentes modulares)
- ✅ Componentes reutilizables
- ✅ Enlace de componentes a orígenes de datos
- ✅ Asociación de acciones a eventos
- ✅ Clases, propiedades, métodos

### De la Unidad 003 - Creación de componentes visuales
- ✅ Concepto de componente
- ✅ Propiedades, atributos y métodos
- ✅ Eventos y asociación de acciones
- ✅ Persistencia del componente (a través de variables)
- ✅ Empaquetado de componentes (patrón UMD)

### De la Unidad 004 - Diseño de interfaces gráficas
- ✅ Usabilidad y accesibilidad
- ✅ Pautas de diseño de la estructura
- ✅ Pautas de diseño del aspecto visual
- ✅ Diseño responsive

---

## 🎨 Características Técnicas

### CSS
- Variables CSS (Custom Properties) para fácil personalización
- Sistema de diseño con tokens
- Flexbox y Grid para layouts
- Media queries para responsive
- Modo oscuro automático con `prefers-color-scheme`
- Transiciones y animaciones CSS

### JavaScript
- Patrón UMD para compatibilidad con AMD, CommonJS y navegador
- Clases ES6 con encapsulación
- Métodos públicos y privados
- Eventos del DOM
- Normalización de texto para búsquedas
- Canvas API para gráficos

### HTML
- Semántica correcta
- Accesibilidad básica
- Estructura modular

---

## 📊 Comparación de Versiones

| Característica | v1.0 Básica | v2.0 Mejorada |
|----------------|-------------|---------------|
| StatsCard | ✅ Básica | ✅ Con animaciones |
| Tabla básica | ✅ | ⬆️ DataTable |
| Búsqueda | ❌ | ✅ |
| Ordenamiento | ❌ | ✅ |
| Paginación | ❌ | ✅ |
| Gráficos | ❌ | ✅ BarChart |
| Métodos públicos | Limitados | ✅ Completos |
| Interactividad | Baja | Alta |

---

## 🔄 Mejoras Futuras (v3 - Planificada)

### Nuevos Componentes
- 📉 LineChart - Gráfico de líneas
- 🥧 PieChart - Gráfico circular
- 📝 FormBuilder - Constructor de formularios
- 🔔 Notifications - Sistema de notificaciones
- 🪟 Modal - Ventanas modales
- 🎨 ColorPicker - Selector de color

### Mejoras en Componentes Existentes
- Exportación de datos (CSV, JSON, Excel)
- Filtros avanzados en tablas
- Agrupación de filas
- Edición in-line
- Drag & drop para reordenar
- Temas personalizables (no solo modo oscuro)

### Características Técnicas
- TypeScript para tipado estático
- Tests unitarios con Jest
- Documentación automática con JSDoc
- Build system con Webpack/Vite
- NPM package publicado
- CDN para carga rápida

---

## 📚 Referencias y Recursos

### Inspiración del Ejercicio de Clase
- UILib v1.0 (003-Creación de componentes visuales/101-Ejercicio de final de unidad)
- Ejemplos vistos en clase sobre componentes personalizados

### Tecnologías Utilizadas
- HTML5
- CSS3 (Custom Properties, Flexbox, Grid)
- JavaScript ES6+ (Classes, Arrow Functions, Modules)
- Canvas API para gráficos

### Patrones de Diseño
- UMD (Universal Module Definition)
- Component Pattern
- Observer Pattern (para eventos)

---

## ✅ Criterios de Evaluación Cumplidos

1. **Control sobre elementos de interfaz de usuario existentes**
   - ✅ Uso correcto de HTML semántico
   - ✅ Estilos CSS avanzados con variables
   - ✅ Manipulación del DOM con JavaScript

2. **Personalización visual**
   - ✅ Sistema de diseño coherente
   - ✅ Paleta de colores definida
   - ✅ Iconos y tipografía consistente
   - ✅ Responsive design

3. **Personalización funcional**
   - ✅ Búsqueda interactiva
   - ✅ Ordenamiento de datos
   - ✅ Paginación
   - ✅ Actualización dinámica
   - ✅ Gráficos interactivos

4. **Código reutilizable**
   - ✅ Componentes modulares
   - ✅ API consistente
   - ✅ Documentación clara
   - ✅ Ejemplos de uso

5. **Evolución progresiva**
   - ✅ Versión básica funcional
   - ✅ Versión mejorada con features avanzadas
   - ✅ Plan de mejoras futuras

---

## 🎓 Conclusiones

Este proyecto demuestra la capacidad de:

1. Crear componentes de interfaz de usuario personalizados desde cero
2. Aplicar conocimientos de HTML, CSS y JavaScript de forma integrada
3. Seguir patrones de diseño y buenas prácticas
4. Desarrollar soluciones de forma incremental
5. Documentar y presentar el trabajo de manera profesional

La librería AgusmaLab creada es funcional, reutilizable y puede ser integrada en proyectos reales. Además, su arquitectura modular permite futuras expansiones y mejoras.

---

**Desarrollado como parte del ejercicio final de la unidad**  
**Asignatura: Desarrollo de Interfaces - DAM 2**  
**Fecha: 17 de febrero de 2026**



