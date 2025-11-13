# UILib v1.0 - Librería de Componentes UI

**Ejercicio Final de Unidad 3: Creación de Componentes Visuales**

Librería de componentes de interfaces de usuario reutilizables e integrables en proyectos front-end HTML-CSS-JS.

## 📋 Contenido

Esta librería incluye los siguientes componentes:

1. **DataTable** - Tabla con búsqueda, ordenamiento y paginación
2. **SearchableSelect** - Select mejorado con búsqueda integrada
3. **BarChart** - Gráfico de barras con Canvas
4. **StatsCard** - Tarjetas de estadísticas para dashboards
5. **ReportPanel** - Panel estructurado para informes

## 🚀 Instalación

### Carga Local

Incluye los archivos CSS y JS en tu HTML:

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <link rel="stylesheet" href="uilib.css">
</head>
<body>
  <!-- Tu contenido -->
  
  <script src="uilib.js"></script>
</body>
</html>
```

### Carga desde CDN (Ejemplo con GitHub Pages)

```html
<link rel="stylesheet" href="https://tu-usuario.github.io/uilib/uilib.css">
<script src="https://tu-usuario.github.io/uilib/uilib.js"></script>
```

## 📚 Documentación de Componentes

### 1. DataTable

Tabla con funcionalidades avanzadas de búsqueda, ordenamiento y paginación.

#### Uso Básico

```html
<div id="miTabla"></div>

<script>
  const tabla = new UILib.DataTable('#miTabla', {
    title: 'Lista de Usuarios',
    columns: [
      { field: 'id', label: 'ID' },
      { field: 'nombre', label: 'Nombre' },
      { field: 'email', label: 'Email' }
    ],
    data: [
      { id: 1, nombre: 'Ana García', email: 'ana@example.com' },
      { id: 2, nombre: 'Carlos López', email: 'carlos@example.com' }
    ],
    searchable: true,
    sortable: true,
    pagination: true,
    rowsPerPage: 10
  });
</script>
```

#### Opciones

| Opción | Tipo | Default | Descripción |
|--------|------|---------|-------------|
| `title` | String | `'Tabla de datos'` | Título de la tabla |
| `columns` | Array | `[]` | Definición de columnas |
| `data` | Array | `[]` | Datos de la tabla |
| `searchable` | Boolean | `true` | Activar búsqueda |
| `sortable` | Boolean | `true` | Activar ordenamiento |
| `pagination` | Boolean | `true` | Activar paginación |
| `rowsPerPage` | Number | `10` | Filas por página |

#### Columnas Personalizadas

```javascript
columns: [
  {
    field: 'salario',
    label: 'Salario',
    sortable: true,
    render: (value, row) => `€${value.toLocaleString()}`
  }
]
```

#### Métodos

```javascript
tabla.updateData(newData);    // Actualizar datos
tabla.nextPage();             // Página siguiente
tabla.previousPage();         // Página anterior
tabla.goToPage(3);            // Ir a página específica
```

---

### 2. SearchableSelect

Select mejorado con búsqueda en tiempo real, insensible a diacríticos.

#### Uso Básico

```html
<select id="miSelect">
  <option value="">-- Selecciona --</option>
  <option value="es">España</option>
  <option value="mx">México</option>
  <option value="ar">Argentina</option>
</select>

<script>
  const select = new UILib.SearchableSelect('#miSelect', {
    placeholder: 'Buscar país...',
    diacriticsInsensitive: true,
    closeOnSelect: true
  });
</script>
```

#### Opciones

| Opción | Tipo | Default | Descripción |
|--------|------|---------|-------------|
| `placeholder` | String | `'Escribe para buscar...'` | Texto del placeholder |
| `diacriticsInsensitive` | Boolean | `true` | Ignorar acentos en búsqueda |
| `closeOnSelect` | Boolean | `true` | Cerrar al seleccionar |

#### Eventos

```javascript
document.querySelector('#miSelect').addEventListener('change', (e) => {
  console.log('Valor seleccionado:', e.target.value);
});
```

---

### 3. BarChart

Gráfico de barras renderizado con Canvas.

#### Uso Básico

```html
<div id="miGrafico"></div>

<script>
  const grafico = new UILib.BarChart('#miGrafico', {
    title: 'Ventas Mensuales',
    labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
    data: [2400, 1398, 9800, 3908, 4800, 3800],
    color: '#2563eb',
    width: 600,
    height: 400,
    showValues: true
  });
</script>
```

#### Opciones

| Opción | Tipo | Default | Descripción |
|--------|------|---------|-------------|
| `title` | String | `'Gráfico de barras'` | Título del gráfico |
| `labels` | Array | `[]` | Etiquetas del eje X |
| `data` | Array | `[]` | Valores de las barras |
| `color` | String | `'#2563eb'` | Color de las barras |
| `width` | Number | `600` | Ancho en píxeles |
| `height` | Number | `400` | Alto en píxeles |
| `showValues` | Boolean | `true` | Mostrar valores sobre barras |

#### Métodos

```javascript
grafico.update([2500, 1500, 10000, 4000, 5000, 4000]);
```

---

### 4. StatsCard

Tarjeta de estadísticas para dashboards.

#### Uso Básico

```html
<div id="miStat"></div>

<script>
  const stat = new UILib.StatsCard('#miStat', {
    label: 'Ventas Totales',
    value: '€45,231',
    change: '+12.5',
    changeType: 'positive',
    icon: '💰',
    iconType: 'success'
  });
</script>
```

#### Opciones

| Opción | Tipo | Default | Descripción |
|--------|------|---------|-------------|
| `label` | String | `'Estadística'` | Etiqueta de la estadística |
| `value` | String | `'0'` | Valor principal |
| `change` | String/Number | `null` | Cambio porcentual |
| `changeType` | String | `'positive'` | `'positive'` o `'negative'` |
| `icon` | String | `'📊'` | Emoji o ícono |
| `iconType` | String | `'primary'` | `'primary'`, `'success'`, `'warning'`, `'danger'`, `'info'` |

#### Métodos

```javascript
stat.update({
  value: '€50,000',
  change: '+15.2'
});
```

---

### 5. ReportPanel

Panel estructurado para mostrar informes.

#### Uso Básico

```html
<div id="miInforme"></div>

<script>
  const informe = new UILib.ReportPanel('#miInforme', {
    title: 'Informe Trimestral',
    subtitle: 'Q4 2024',
    content: '<p>Contenido del informe...</p>',
    footer: 'Generado el 12/11/2025'
  });
</script>
```

#### Opciones

| Opción | Tipo | Default | Descripción |
|--------|------|---------|-------------|
| `title` | String | `'Informe'` | Título del informe |
| `subtitle` | String | `''` | Subtítulo |
| `content` | String/Element | `null` | Contenido HTML o elemento DOM |
| `footer` | String | `''` | Texto del footer |

#### Métodos

```javascript
informe.setContent('<p>Nuevo contenido...</p>');
```

---

## 🎨 Utilidades CSS

### Grid System

```html
<div class="uil-grid uil-grid-2">
  <!-- 2 columnas -->
</div>

<div class="uil-grid uil-grid-3">
  <!-- 3 columnas -->
</div>

<div class="uil-grid uil-grid-4">
  <!-- 4 columnas (responsivo) -->
</div>
```

### Inputs con Estilos

```html
<input type="text" class="uil-input" placeholder="Nombre">
<button class="uil-button">Enviar</button>
<button class="uil-button secondary">Cancelar</button>
```

### Clases de Utilidad

- `.uil-hidden` - Ocultar elemento
- `.uil-container` - Contenedor base

---

## 🎯 Ejemplo Completo

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Mi Dashboard</title>
  <link rel="stylesheet" href="uilib.css">
</head>
<body>
  <div class="uil-grid uil-grid-4">
    <div id="stat1"></div>
    <div id="stat2"></div>
    <div id="stat3"></div>
    <div id="stat4"></div>
  </div>

  <div id="tabla"></div>
  <div id="grafico"></div>

  <script src="uilib.js"></script>
  <script>
    // Stats
    new UILib.StatsCard('#stat1', {
      label: 'Usuarios',
      value: '1,234',
      icon: '👥',
      iconType: 'primary'
    });

    // Tabla
    new UILib.DataTable('#tabla', {
      title: 'Datos',
      columns: [
        { field: 'id', label: 'ID' },
        { field: 'nombre', label: 'Nombre' }
      ],
      data: [
        { id: 1, nombre: 'Ana' },
        { id: 2, nombre: 'Carlos' }
      ]
    });

    // Gráfico
    new UILib.BarChart('#grafico', {
      title: 'Ventas',
      labels: ['Ene', 'Feb', 'Mar'],
      data: [100, 200, 150]
    });
  </script>
</body>
</html>
```

---

## 🔧 Personalización

### Variables CSS

Puedes personalizar los colores y estilos modificando las variables CSS en `:root`:

```css
:root {
  --uil-primary: #2563eb;
  --uil-success: #16a34a;
  --uil-warning: #d97706;
  --uil-danger: #dc2626;
  --uil-radius: 0.5rem;
  /* ... más variables */
}
```

---

## 📦 Patrones de Diseño Implementados

Esta librería sigue los patrones vistos en clase:

1. **Componentización** (004-Persistencia del componente)
   - Encapsulación de funcionalidad
   - Reutilización de código
   - API consistente

2. **Eventos** (003-Eventos; asociación de acciones a eventos)
   - Event listeners para interactividad
   - Manejo de eventos del DOM
   - Propagación controlada

3. **Empaquetado** (007-Empaquetado de componentes)
   - UMD pattern para compatibilidad
   - CSS modular con prefijos
   - Carga externa optimizada

---

## 🌐 Compatibilidad

- Chrome/Edge: ✅
- Firefox: ✅
- Safari: ✅
- Opera: ✅

---

## 📝 Licencia

Proyecto educativo - DAM 2 - Desarrollo de Interfaces

---

## 👨‍💻 Autor

[Tu Nombre]  
DAM-2 - Desarrollo de Interfaces  
Ejercicio Final de Unidad 3: Creación de Componentes Visuales

---

## 🎬 Ejemplos de Proyectos Reales

### Demostración de Reutilización

Para demostrar que UILib es verdaderamente reutilizable en cualquier proyecto, se incluyen **3 proyectos completos y diferentes**:

#### 1. **index.html** - Demo Básica
Demostración de todos los componentes de forma aislada con ejemplos de código.
- **Propósito**: Tutorial y documentación visual
- **Componentes**: Todos (DataTable, Charts, Forms, Stats, Reports)
- **Caso de uso**: Aprendizaje y referencia rápida

#### 2. **ejemplo-proyecto-real.html** - Sistema de Gestión Empresarial
Aplicación completa de gestión con múltiples módulos.
- **Propósito**: Sistema administrativo corporativo
- **Características**:
  - Dashboard con KPIs en tiempo real
  - Gestión de empleados (CRUD completo)
  - Gestión de ventas y productos
  - Informes trimestrales y anuales
  - Navegación por tabs
  - Formularios complejos con validación
  - Filtrado avanzado de datos
- **Demuestra**: Integración completa en un sistema empresarial real

#### 3. **ejemplo-ecommerce.html** - Panel de E-Commerce
Dashboard analítico para tienda online.
- **Propósito**: Analytics de comercio electrónico
- **Características**:
  - KPIs de negocio (ingresos, conversión, clientes)
  - Análisis de ventas por categoría
  - Gestión de pedidos con filtros dinámicos
  - Ranking de productos más vendidos
  - Informes mensuales automáticos
  - Alertas de stock bajo
  - Badges de estado visuales
- **Demuestra**: Adaptabilidad a diferentes dominios de negocio

### Comparación de los Proyectos

| Aspecto | Demo Básica | Sistema Empresarial | E-Commerce |
|---------|-------------|---------------------|------------|
| Complejidad | Baja | Alta | Media-Alta |
| Componentes usados | 5/5 | 5/5 | 5/5 |
| Interactividad | Media | Alta | Alta |
| Datos dinámicos | Estáticos | Dinámicos + CRUD | Dinámicos + Filtros |
| Formularios | Simple | Complejos | Filtros avanzados |
| Navegación | No | Multi-tab | Single page |
| Tiempo de carga | Rápido | Rápido | Rápido |

### ¿Por qué esto demuestra reutilización?

1. **Misma librería, 3 contextos completamente diferentes**
   - Sin modificar ni una línea de `uilib.js` o `uilib.css`
   - Solo cargando 2 archivos: CSS + JS

2. **Sin dependencias adicionales**
   - No requiere jQuery, Bootstrap ni otras librerías
   - JavaScript vanilla puro
   - CSS moderno sin preprocesadores

3. **API consistente**
   - Misma sintaxis en todos los proyectos
   - Mismo patrón de inicialización
   - Mismas opciones de configuración

4. **Integración simple**
   ```html
   <link rel="stylesheet" href="uilib.css">
   <script src="uilib.js"></script>
   <script>
     new UILib.DataTable('#elemento', { /* opciones */ });
   </script>
   ```

5. **Personalización sin modificar la librería**
   - Estilos externos propios de cada proyecto
   - Lógica de negocio separada
   - Datos adaptados a cada caso de uso

### Pruébalo Tú Mismo

```bash
# Abre cualquiera de los 3 archivos HTML en tu navegador:

index.html                    # Demo educativa
ejemplo-proyecto-real.html    # Sistema empresarial
ejemplo-ecommerce.html        # Dashboard e-commerce
```

**Todos funcionan perfectamente con la misma librería UILib.**

---

## 📖 Referencias

Basado en los conceptos y patrones vistos en:
- 003-Eventos; asociación de acciones a eventos
- 004-Persistencia del componente
- 007-Empaquetado de componentes
