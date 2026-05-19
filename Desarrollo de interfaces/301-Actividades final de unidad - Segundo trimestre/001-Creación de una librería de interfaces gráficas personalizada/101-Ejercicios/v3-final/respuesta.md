He desarrollado **AgusmaLab v3.0**, una librería profesional de componentes de interfaz de usuario que representa la evolución final de mi proyecto personal de creación de componentes gráficos. Esta versión premium incorpora tecnologías visuales avanzadas como **glassmorphism**, iconos SVG profesionales, sistema de tokens de diseño y animaciones fluidas con curvas de Bézier.

Esta librería sirve para **acelerar el desarrollo de dashboards, paneles administrativos y aplicaciones de gestión** sin depender de frameworks pesados como React, Vue o Angular. Se utiliza en contextos donde se necesita:
- Crear interfaces profesionales con aspecto moderno tipo "dark mode"
- Visualizar datos mediante tarjetas de estadísticas interactivas
- Gestionar grandes volúmenes de información con tablas avanzadas
- Presentar información gráfica básica mediante gráficos de barras

AgusmaLab v3.0 aplica directamente los conceptos vistos en las unidades 001 (Generación de interfaces de usuario) y 003 (Creación de componentes visuales), llevándolos a un nivel profesional mediante técnicas modernas de diseño UI/UX.

---

### Definiciones de Conceptos Clave

**Glassmorphism**: Técnica de diseño que utiliza fondos translúcidos con efecto de desenfoque (`backdrop-filter: blur()`) combinado con transparencias y bordes sutiles, simulando el efecto visual de cristal esmerilado. En CSS se implementa mediante:

```css
background: rgba(30, 41, 59, 0.6);
backdrop-filter: blur(20px);
-webkit-backdrop-filter: blur(20px);
border: 1px solid rgba(148, 163, 184, 0.1);
```

**Sistema de Tokens de Diseño**: Conjunto de variables CSS (custom properties) que definen los valores fundamentales de diseño (colores, espaciados, tipografía) de forma centralizada, permitiendo mantener consistencia visual en toda la librería. Implementado mediante variables CSS:

```css
:root {
  --agl-primary: #3b82f6;
  --agl-space-md: 1rem;
  --agl-radius: 0.75rem;
  --agl-transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
```

**Patrón UMD (Universal Module Definition)**: Patrón de diseño que permite que un módulo JavaScript funcione en múltiples entornos: AMD (RequireJS), CommonJS (Node.js) y navegadores tradicionales mediante variable global. He implementado esto para máxima compatibilidad.

**Iconos SVG Inline**: Uso de gráficos vectoriales escalables embebidos directamente en JavaScript mediante template strings, evitando dependencias externas y permitiendo coloración dinámica mediante CSS `currentColor`.

### Arquitectura de la Librería

La estructura de AgusmaLab v3.0 se compone de tres archivos principales:

1. **agusmalab.js** (699 líneas) - Núcleo de la librería
2. **agusmalab.css** (590 líneas) - Sistema de estilos
3. **index.html** - Demostración interactiva de componentes

### Funcionamiento Paso a Paso

#### PASO 1: Inicialización del Patrón UMD

La librería se envuelve en una IIFE (Immediately Invoked Function Expression) que detecta el entorno de ejecución:

```javascript
(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    // CommonJS
    module.exports = factory();
  } else {
    // Browser global
    root.AgusmaLab = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';
  // Código de la librería...
}));
```

#### PASO 2: Definición de Utilidades Comunes

He creado funciones auxiliares que reutilizo en todos los componentes:

```javascript
const crearElemento = (tag, className = '', content = '') => {
  const elemento = document.createElement(tag);
  if (className) elemento.className = className;
  if (content) elemento.textContent = content;
  return elemento;
};

const obtenerElemento = (selector) => {
  return typeof selector === 'string' ? 
    document.querySelector(selector) : 
    selector;
};

const normalizar = (str) => {
  return str.normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase();
};
```

La función `normalizar()` es especialmente importante porque elimina acentos mediante normalización Unicode NFD, permitiendo que la búsqueda funcione correctamente con palabras como "García" al buscar "garcia".

#### PASO 3: Sistema de Iconos SVG

He creado un objeto `Iconos` que almacena definiciones SVG como strings:

```javascript
const Iconos = {
  usuarios: `
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" 
         stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
      <circle cx="9" cy="7" r="4"></circle>
      <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
      <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
    </svg>
  `,
  dinero: `...`,
  pedidos: `...`,
  // ... 8 iconos en total
};
```

Este enfoque me permite:
- Evitar dependencias de librerías de iconos (Font Awesome, Material Icons)
- Controlar el color del icono mediante CSS (`stroke="currentColor"`)
- Asegurar renderizado vectorial perfecto en cualquier resolución

### Componentes Implementados

#### Componente 1: StatsCard (Tarjetas de Estadísticas Premium)

**Clase JavaScript:**

```javascript
class StatsCard {
  constructor(contenedor, opciones = {}) {
    this.contenedor = obtenerElemento(contenedor);
    
    if (!this.contenedor) {
      throw new Error('AgusmaLab.StatsCard: contenedor no encontrado');
    }

    this.opciones = {
      titulo: opciones.titulo || 'Estadística',
      valor: opciones.valor || '0',
      icono: opciones.icono || 'estadisticas',
      colorIcono: opciones.colorIcono || 'primary',
      descripcion: opciones.descripcion || '',
      cambio: opciones.cambio || null,
      tipoCambio: opciones.tipoCambio || 'neutral',
      ...opciones
    };

    this.renderizar();
  }
}
```

**Características técnicas:**
- **Validación de entrada**: Lanza error si el contenedor no existe
- **Opciones por defecto**: Utiliza el operador `||` y spread operator `...opciones`
- **Renderizado declarativo**: Método `renderizar()` separado para actualización
- **Referencias DOM guardadas**: Almacena `this.elementoValor` para actualizaciones eficientes

**Métodos públicos:**

```javascript
actualizarValor(nuevoValor, animar = true) {
  this.opciones.valor = nuevoValor;
  if (this.elementoValor) {
    if (animar) {
      this.elementoValor.classList.add('animating');
      setTimeout(() => this.elementoValor.classList.remove('animating'), 400);
    }
    this.elementoValor.textContent = nuevoValor;
  }
}

mostrarCambio(cambio, tipo = 'neutral') {
  this.opciones.cambio = cambio;
  this.opciones.tipoCambio = tipo;
  
  if (this.elementoCambio) {
    this.elementoCambio.textContent = cambio;
    this.elementoCambio.className = `agl-stats-card-change ${tipo}`;
  } else {
    this.renderizar();
  }
}
```

**Estilos CSS con Glassmorphism:**

```css
.agl-stats-card {
  background: var(--agl-glass-bg);
  backdrop-filter: var(--agl-backdrop-blur);
  -webkit-backdrop-filter: var(--agl-backdrop-blur);
  border: 1px solid var(--agl-glass-border);
  border-radius: var(--agl-radius);
  padding: var(--agl-space-xl);
  box-shadow: var(--agl-glass-shadow);
  transition: var(--agl-transition);
}

.agl-stats-card:hover {
  box-shadow: var(--agl-shadow-lg);
  transform: translateY(-2px);
  border-color: rgba(148, 163, 184, 0.2);
}
```

He aplicado la propiedad `backdrop-filter` con prefijo `-webkit-` para compatibilidad con Safari. El efecto hover utiliza `transform: translateY(-2px)` para dar sensación de elevación al pasar el ratón.

#### Componente 2: DataTable (Tabla Interactiva Avanzada)

**Funcionalidades implementadas:**

1. **Búsqueda en tiempo real**
```javascript
_filtrarDatos() {
  if (!this.terminoBusqueda) {
    this.datosFiltrados = [...this.opciones.datos];
    return;
  }

  const termino = normalizar(this.terminoBusqueda);
  this.datosFiltrados = this.opciones.datos.filter(fila => {
    return this.opciones.columnas.some((col, index) => {
      const valor = Array.isArray(fila) ? fila[index] : fila[col.campo || col];
      if (valor === null || valor === undefined) return false;
      return normalizar(String(valor)).includes(termino);
    });
  });
}
```

Técnica utilizada: `Array.filter()` combinado con `Array.some()` para buscar en todas las columnas simultáneamente.

2. **Ordenamiento bidireccional**
```javascript
_ordenarDatos() {
  if (!this.columnaOrden) return;

  const indiceColumna = this.opciones.columnas.findIndex(col => 
    (col.campo || col) === this.columnaOrden
  );

  this.datosFiltrados.sort((a, b) => {
    const valorA = Array.isArray(a) ? a[indiceColumna] : a[this.columnaOrden];
    const valorB = Array.isArray(b) ? b[indiceColumna] : b[this.columnaOrden];
    
    if (valorA === null || valorA === undefined) return 1;
    if (valorB === null || valorB === undefined) return -1;
    
    let comparacion = 0;
    if (typeof valorA === 'number' && typeof valorB === 'number') {
      comparacion = valorA - valorB;
    } else {
      comparacion = String(valorA).localeCompare(String(valorB));
    }
    
    return this.direccionOrden === 'asc' ? comparacion : -comparacion;
  });
}
```

Aspectos técnicos destacados:
- Comprobación de tipos para ordenamiento numérico vs. alfabético
- Uso de `localeCompare()` para ordenamiento respetando idioma español
- Manejo de valores null/undefined (los coloco al final)
- Inversión de comparación según dirección (`-comparacion`)

3. **Paginación con botones dinámicos**
```javascript
_renderizarPaginacion(wrapper) {
  const totalFilas = this.datosFiltrados.length;
  const inicio = (this.paginaActual - 1) * this.opciones.filasPorPagina + 1;
  const fin = Math.min(this.paginaActual * this.opciones.filasPorPagina, totalFilas);
  
  const totalPaginas = Math.ceil(totalFilas / this.opciones.filasPorPagina);
  const maxPaginasVisibles = 5;
  let paginaInicio = Math.max(1, this.paginaActual - Math.floor(maxPaginasVisibles / 2));
  let paginaFin = Math.min(totalPaginas, paginaInicio + maxPaginasVisibles - 1);
  
  if (paginaFin - paginaInicio < maxPaginasVisibles - 1) {
    paginaInicio = Math.max(1, paginaFin - maxPaginasVisibles + 1);
  }
  // ...
}
```

He implementado un algoritmo de "ventana deslizante" que muestra máximo 5 números de página, manteniendo la página actual centrada cuando es posible.

4. **Optimización de renderizado**

En lugar de re-renderizar todo el componente en cada actualización, he creado el método `_actualizarContenido()` que solo modifica el `<tbody>`, el `<thead>` (para indicadores de orden) y el footer de paginación:

```javascript
_actualizarContenido() {
  // Actualizar solo tbody y footer sin tocar el header
  if (!this.tabla) return;
  
  const tbody = this.tabla.querySelector('tbody');
  if (tbody) {
    tbody.innerHTML = '';
    const datosPaginados = this._obtenerDatosPaginados();
    // ... renderizar filas
  }
  
  // Actualizar thead (para indicadores de ordenamiento)
  const headers = this.tabla.querySelectorAll('th.sortable');
  headers.forEach(th => {
    th.classList.remove('sorted-asc', 'sorted-desc');
    const campo = th.dataset.campo;
    if (this.columnaOrden === campo) {
      th.classList.add(this.direccionOrden === 'asc' ? 'sorted-asc' : 'sorted-desc');
    }
  });
  // ...
}
```

Esta técnica mejora el rendimiento porque:
- No destruye el campo de búsqueda (mantiene el foco)
- No elimina event listeners innecesariamente
- Reduce manipulaciones DOM (más rápido)

**Indicadores visuales de ordenamiento:**

```css
.agl-table th.sortable::after {
  content: ' ⇅';
  opacity: 0.3;
  font-size: 0.875em;
}

.agl-table th.sorted-asc::after {
  content: ' ↑';
  opacity: 1;
  color: var(--agl-primary);
}

.agl-table th.sorted-desc::after {
  content: ' ↓';
  opacity: 1;
  color: var(--agl-primary);
}
```

Utilizo pseudo-elemento `::after` con caracteres Unicode para flechas, evitando imágenes adicionales.

#### Componente 3: BarChart (Gráfico de Barras con Canvas)

**Implementación del dibujo en Canvas:**

```javascript
_dibujarGrafico(canvas) {
  const ctx = canvas.getContext('2d');
  const padding = 50;
  const ancho = canvas.width - padding * 2;
  const alto = canvas.height - padding * 2;

  // Limpiar canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Configurar fuente
  ctx.font = '12px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';

  // Encontrar valor máximo para escalar
  const valorMax = Math.max(...this.opciones.datos);
  const escalaY = alto / valorMax;

  // Calcular dimensiones de barras
  const numBarras = this.opciones.datos.length;
  const anchoBarra = (ancho / numBarras) * 0.7;
  const espacioBarra = (ancho / numBarras) * 0.3;

  // Dibujar cada barra
  this.opciones.datos.forEach((valor, i) => {
    const x = padding + (i * (anchoBarra + espacioBarra)) + espacioBarra / 2;
    const alturaBarra = valor * escalaY;
    const y = canvas.height - padding - alturaBarra;

    // Barra principal
    ctx.fillStyle = this.opciones.color;
    ctx.fillRect(x, y, anchoBarra, alturaBarra);

    // Valor encima de la barra
    ctx.fillStyle = '#1e293b';
    ctx.textAlign = 'center';
    ctx.fillText(valor, x + anchoBarra / 2, y - 5);

    // Etiqueta debajo
    if (this.opciones.etiquetas[i]) {
      ctx.fillText(this.opciones.etiquetas[i], x + anchoBarra / 2, 
                   canvas.height - padding + 20);
    }
  });

  // Dibujar ejes
  ctx.strokeStyle = '#e2e8f0';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(padding, padding);
  ctx.lineTo(padding, canvas.height - padding);
  ctx.lineTo(canvas.width - padding, canvas.height - padding);
  ctx.stroke();
}
```

**Cálculos matemáticos aplicados:**

1. **Normalización de valores**: `escalaY = alto / valorMax` convierte valores de datos a píxeles
2. **Posicionamiento**: El 70% del espacio horizontal es barra, 30% separación
3. **Coordenada Y invertida**: Canvas tiene origen arriba-izquierda, por eso: `y = canvas.height - padding - alturaBarra`

**Método de actualización dinámica:**

```javascript
actualizarDatos(nuevosDatos, nuevasEtiquetas = null) {
  this.opciones.datos = nuevosDatos;
  if (nuevasEtiquetas) {
    this.opciones.etiquetas = nuevasEtiquetas;
  }
  this.renderizar();
}
```

### Sistema de Tokens de Diseño (Design Tokens)

He implementado un sistema completo de variables CSS organizadas por categorías:

```css
:root {
  /* Paleta de colores semántica */
  --agl-primary: #3b82f6;
  --agl-primary-light: #60a5fa;
  --agl-success: #10b981;
  --agl-warning: #f59e0b;
  --agl-danger: #ef4444;
  --agl-info: #06b6d4;
  
  /* Colores de fondo con transparencias para glassmorphism */
  --agl-bg: rgba(30, 41, 59, 0.7);
  --agl-bg-solid: #1e293b;
  --agl-bg-alt: rgba(15, 23, 42, 0.5);
  --agl-text: #f1f5f9;
  --agl-text-muted: #94a3b8;
  --agl-border: rgba(148, 163, 184, 0.15);
  
  /* Efectos de glassmorphism */
  --agl-glass-bg: rgba(30, 41, 59, 0.6);
  --agl-glass-border: rgba(148, 163, 184, 0.1);
  --agl-glass-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
  --agl-backdrop-blur: blur(20px);
  
  /* Espaciado con escala base 4px */
  --agl-space-xs: 0.5rem;     /* 8px */
  --agl-space-sm: 0.75rem;    /* 12px */
  --agl-space-md: 1rem;       /* 16px */
  --agl-space-lg: 1.5rem;     /* 24px */
  --agl-space-xl: 2rem;       /* 32px */
  
  /* Bordes y radios */
  --agl-radius: 0.75rem;      /* 12px */
  --agl-radius-sm: 0.5rem;    /* 8px */
  --agl-radius-lg: 1rem;      /* 16px */
  
  /* Sombras con niveles de elevación */
  --agl-shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.12);
  --agl-shadow-md: 0 2px 8px rgba(0, 0, 0, 0.15);
  --agl-shadow-lg: 0 4px 16px rgba(0, 0, 0, 0.2);
  --agl-shadow-xl: 0 8px 24px rgba(0, 0, 0, 0.25);
  
  /* Tipografía con escala modular ratio 1.25 */
  --agl-font: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --agl-font-size-xs: 0.75rem;    /* 12px */
  --agl-font-size-sm: 0.875rem;   /* 14px */
  --agl-font-size: 1rem;          /* 16px - base */
  --agl-font-size-lg: 1.125rem;   /* 18px */
  --agl-font-size-xl: 1.25rem;    /* 20px */
  --agl-font-size-2xl: 1.5rem;    /* 24px */
  --agl-font-size-3xl: 1.875rem;  /* 30px */
  --agl-font-size-4xl: 2.25rem;   /* 36px */
  
  /* Pesos de fuente */
  --agl-font-normal: 400;
  --agl-font-medium: 500;
  --agl-font-semibold: 600;
  --agl-font-bold: 700;
  
  /* Transiciones con curvas de Bézier profesionales */
  --agl-transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  --agl-transition-fast: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
  --agl-transition-slow: all 0.45s cubic-bezier(0.4, 0, 0.2, 1);
}
```

Este sistema me proporciona:
- **Consistencia visual**: Todos los componentes usan los mismos valores
- **Mantenimiento fácil**: Cambiar un color implica editar una sola variable
- **Escalabilidad**: Agregar temas (light/dark) requiere solo cambiar las variables
- **Documentación implícita**: Las variables son autodescriptivas

### Animaciones con Keyframes

He implementado animaciones CSS profesionales:

```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulseValue {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.agl-animate-in {
  animation: fadeInUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) both;
}

.agl-stats-card-value.animating {
  animation: pulseValue 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
```

**Delays escalonados** para entrada secuencial:

```css
.agl-animate-in:nth-child(1) { animation-delay: 0.1s; }
.agl-animate-in:nth-child(2) { animation-delay: 0.2s; }
.agl-animate-in:nth-child(3) { animation-delay: 0.3s; }
.agl-animate-in:nth-child(4) { animation-delay: 0.4s; }
```

Utilizo la curva `cubic-bezier(0.4, 0, 0.2, 1)` que es la curva estándar de Material Design, proporcionando animaciones naturales.

### Diseño Responsivo

He implementado adaptación a dispositivos móviles:

```css
@media (max-width: 768px) {
  .agl-stats-card {
    padding: var(--agl-space-md);
  }
  
  .agl-stats-card-value {
    font-size: 1.5rem;
  }
  
  .agl-table-search {
    min-width: 100%;
  }
  
  .agl-table-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .agl-table-footer {
    flex-direction: column;
    align-items: stretch;
  }
}
```

---

### Ejemplo de Uso Completo: Dashboard de Gestión Empresarial

A continuación muestro cómo implementé un dashboard completo utilizando AgusmaLab v3.0:

#### HTML de la Aplicación

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AgusmaLab v3.0 - Dashboard Empresarial</title>
  
  <!-- Cargar la librería -->
  <link rel="stylesheet" href="agusmalab.css">
</head>
<body>
  <div class="demo-container">
    <!-- Header del Dashboard -->
    <div class="demo-header">
      <h1>Panel de Control Empresarial</h1>
      <p>Sistema de gestión integrado</p>
    </div>

    <!-- Grid de Tarjetas de Estadísticas -->
    <div class="stats-grid">
      <div id="stat1"></div>
      <div id="stat2"></div>
      <div id="stat3"></div>
      <div id="stat4"></div>
    </div>

    <!-- Tabla Interactiva de Usuarios -->
    <div id="tabla-usuarios"></div>

    <!-- Gráfico de Ventas -->
    <div id="grafico-ventas"></div>
  </div>

  <!-- Cargar librería y aplicación -->
  <script src="agusmalab.js"></script>
  <script src="app.js"></script>
</body>
</html>
```

#### JavaScript de la Aplicación (app.js)

```javascript
// ========================================
// INSTANCIAR TARJETAS DE ESTADÍSTICAS
// ========================================

const tarjeta1 = new AgusmaLab.StatsCard('#stat1', {
  titulo: 'Usuarios Activos',
  valor: '2,847',
  icono: 'usuarios',
  colorIcono: 'primary',
  descripcion: 'Registrados hoy',
  cambio: '+12.5%',
  tipoCambio: 'positivo'
});

const tarjeta2 = new AgusmaLab.StatsCard('#stat2', {
  titulo: 'Ingresos del Mes',
  valor: '€127,543',
  icono: 'dinero',
  colorIcono: 'success',
  descripcion: 'Objetivo: €150,000',
  cambio: '+23.8%',
  tipoCambio: 'positivo'
});

const tarjeta3 = new AgusmaLab.StatsCard('#stat3', {
  titulo: 'Pedidos Pendientes',
  valor: '47',
  icono: 'pedidos',
  colorIcono: 'warning',
  descripcion: 'Procesar hoy',
  cambio: '-5 desde ayer',
  tipoCambio: 'neutral'
});

const tarjeta4 = new AgusmaLab.StatsCard('#stat4', {
  titulo: 'Tasa de Conversión',
  valor: '3.42%',
  icono: 'tendencia',
  colorIcono: 'info',
  descripcion: 'Este mes',
  cambio: '-0.3%',
  tipoCambio: 'negativo'
});

// ========================================
// DATOS REALES DE LA EMPRESA
// ========================================

const datosUsuarios = [
  { 
    id: 1, 
    nombre: 'Ana García Pérez', 
    email: 'ana.garcia@empresa.com', 
    ciudad: 'Madrid', 
    pais: 'España', 
    registro: '2024-01-15', 
    estado: 'Activo' 
  },
  { 
    id: 2, 
    nombre: 'Carlos López Martín', 
    email: 'carlos.lopez@empresa.com', 
    ciudad: 'Barcelona', 
    pais: 'España', 
    registro: '2024-01-18', 
    estado: 'Activo' 
  },
  { 
    id: 3, 
    nombre: 'María Fernández Ruiz', 
    email: 'maria.fernandez@empresa.com', 
    ciudad: 'Valencia', 
    pais: 'España', 
    registro: '2024-02-01', 
    estado: 'Activo' 
  },
  { 
    id: 4, 
    nombre: 'Juan Martínez Soto', 
    email: 'juan.martinez@empresa.com', 
    ciudad: 'Sevilla', 
    pais: 'España', 
    registro: '2024-02-05', 
    estado: 'Inactivo' 
  },
  { 
    id: 5, 
    nombre: 'Laura Sánchez Gil', 
    email: 'laura.sanchez@empresa.com', 
    ciudad: 'Bilbao', 
    pais: 'España', 
    registro: '2024-02-08', 
    estado: 'Activo' 
  },
  // ... más usuarios (total 20 en la demo)
];

// ========================================
// INSTANCIAR TABLA INTERACTIVA
// ========================================

const tablaUsuarios = new AgusmaLab.DataTable('#tabla-usuarios', {
  titulo: 'Gestión de Usuarios - Sistema CRM',
  columnas: [
    { campo: 'id', etiqueta: 'ID', ordenable: true },
    { campo: 'nombre', etiqueta: 'Nombre Completo', ordenable: true },
    { campo: 'email', etiqueta: 'Email', ordenable: true },
    { campo: 'ciudad', etiqueta: 'Ciudad', ordenable: true },
    { campo: 'pais', etiqueta: 'País', ordenable: true },
    { campo: 'registro', etiqueta: 'F. Registro', ordenable: true },
    { campo: 'estado', etiqueta: 'Estado', ordenable: true }
  ],
  datos: datosUsuarios,
  busqueda: true,
  ordenamiento: true,
  paginacion: true,
  filasPorPagina: 8
});

// ========================================
// INSTANCIAR GRÁFICO DE VENTAS
// ========================================

const graficoVentas = new AgusmaLab.BarChart('#grafico-ventas', {
  titulo: 'Ventas Mensuales 2024 - Primer Trimestre',
  etiquetas: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo'],
  datos: [125, 180, 165, 220, 195],
  color: '#10b981',
  ancho: 800,
  alto: 350
});

// ========================================
// FUNCIONES INTERACTIVAS
// ========================================

// Simular actualización de datos en tiempo real
function actualizarDatosEnTiempoReal() {
  const nuevoValor = Math.floor(Math.random() * 5000) + 2000;
  tarjeta1.actualizarValor(nuevoValor.toLocaleString(), true);
  
  const nuevoIngreso = Math.floor(Math.random() * 50000) + 100000;
  tarjeta2.actualizarValor('€' + nuevoIngreso.toLocaleString(), true);
  
  console.log('✅ Datos actualizados correctamente');
}

// Cambiar datos del gráfico dinámicamente
function mostrarTrimestre2() {
  graficoVentas.actualizarDatos(
    [210, 195, 240, 225, 260],
    ['Junio', 'Julio', 'Agosto', 'Sept', 'Octubre']
  );
  console.log('📊 Gráfico actualizado - Trimestre 2');
}

// Ejecutar actualización automática cada 5 segundos
setInterval(actualizarDatosEnTiempoReal, 5000);
```

### Errores Comunes y Cómo Evitarlos

#### Error 1: No validar que el contenedor existe

**❌ Código incorrecto:**
```javascript
const tabla = new AgusmaLab.DataTable('#tabla-inexistente', {...});
// La aplicación falla silenciosamente
```

**✅ Solución implementada:**
```javascript
class DataTable {
  constructor(contenedor, opciones = {}) {
    this.contenedor = obtenerElemento(contenedor);
    
    if (!this.contenedor) {
      throw new Error('AgusmaLab.DataTable: contenedor no encontrado');
    }
    // ...
  }
}
```

He añadido validación explícita que lanza un error descriptivo, facilitando la depuración.

#### Error 2: Perder referencias DOM al re-renderizar

**❌ Problema:**
Si re-renderizo todo el componente en cada actualización, pierdo el estado del input de búsqueda (texto escrito, foco).

**✅ Solución:**
Crear método `_actualizarContenido()` que solo modifica las partes necesarias, preservando el header con el input de búsqueda intacto.

#### Error 3: No normalizar texto en búsquedas

**❌ Código incorrecto:**
```javascript
const buscar = (termino) => {
  return datos.filter(fila => 
    fila.nombre.toLowerCase().includes(termino.toLowerCase())
  );
};
// Buscar "garcia" NO encuentra "García"
```

**✅ Solución con normalización Unicode:**
```javascript
const normalizar = (str) => {
  return str.normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase();
};

const buscar = (termino) => {
  const terminoNorm = normalizar(termino);
  return datos.filter(fila => 
    normalizar(fila.nombre).includes(terminoNorm)
  );
};
// Ahora funciona correctamente con acentos
```

#### Error 4: Olvidar prefijos vendor para CSS moderno

**❌ Código incorrecto:**
```css
.componente {
  backdrop-filter: blur(20px);
}
/* No funciona en Safari iOS */
```

**✅ Solución con prefijo:**
```css
.componente {
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}
```

Safari (tanto desktop como iOS) requiere el prefijo `-webkit-` para `backdrop-filter`.

#### Error 5: No gestionar valores null/undefined en ordenamiento

**❌ Resultado:**
La tabla se rompe al ordenar si hay campos vacíos.

**✅ Solución:**
```javascript
_ordenarDatos() {
  this.datosFiltrados.sort((a, b) => {
    const valorA = Array.isArray(a) ? a[indiceColumna] : a[this.columnaOrden];
    const valorB = Array.isArray(b) ? b[indiceColumna] : b[this.columnaOrden];
    
    // Mover valores null/undefined al final
    if (valorA === null || valorA === undefined) return 1;
    if (valorB === null || valorB === undefined) return -1;
    
    // Continuar con comparación normal...
  });
}
```

---

## 4. Conclusión breve

AgusmaLab v3.0 representa la síntesis de los conocimientos adquiridos en el módulo, integrando **patrones arquitectónicos profesionales** (UMD), **componentes encapsulados** con API clara, **sistema de diseño coherente** mediante tokens CSS, **optimización de rendimiento** y **experiencia premium** con glassmorphism y animaciones fluidas.

He aplicado directamente conceptos de las unidades 001 (patrones de arquitectura, eventos, enlace de datos, clases y métodos), 003 (componentes reutilizables, propiedades, eventos, persistencia y empaquetado) y 004 (usabilidad, accesibilidad y estructura visual).

La librería es extensible y escalable, preparada tanto para proyectos pequeños como aplicaciones empresariales, manteniendo la misma filosofía de diseño modular y reutilizable.