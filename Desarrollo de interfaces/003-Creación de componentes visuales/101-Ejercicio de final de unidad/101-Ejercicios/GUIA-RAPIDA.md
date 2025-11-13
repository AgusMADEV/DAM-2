# 🚀 Guía Rápida: Integrar UILib en Tu Proyecto

## Plantilla Mínima (5 minutos)

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mi Proyecto con UILib</title>
  
  <!-- 1️⃣ CARGAR UILIB -->
  <link rel="stylesheet" href="uilib.css">
</head>
<body>
  
  <!-- 2️⃣ TUS CONTENEDORES -->
  <div class="uil-grid uil-grid-3">
    <div id="stat1"></div>
    <div id="stat2"></div>
    <div id="stat3"></div>
  </div>

  <div id="miTabla"></div>

  <!-- 3️⃣ CARGAR JS -->
  <script src="uilib.js"></script>
  
  <!-- 4️⃣ INICIALIZAR COMPONENTES -->
  <script>
    // Stats Cards
    new UILib.StatsCard('#stat1', {
      label: 'Usuarios',
      value: '1,234',
      icon: '👥'
    });

    // DataTable
    new UILib.DataTable('#miTabla', {
      title: 'Mis Datos',
      columns: [
        { field: 'id', label: 'ID' },
        { field: 'nombre', label: 'Nombre' }
      ],
      data: [
        { id: 1, nombre: 'Ejemplo 1' },
        { id: 2, nombre: 'Ejemplo 2' }
      ]
    });
  </script>
</body>
</html>
```

## Paso a Paso

### 1. Copiar los Archivos

Copia estos 2 archivos a tu proyecto:
```
tu-proyecto/
├── uilib.css
├── uilib.js
└── tu-pagina.html
```

### 2. Enlazar en tu HTML

```html
<head>
  <link rel="stylesheet" href="uilib.css">
</head>
<body>
  <!-- Tu contenido -->
  <script src="uilib.js"></script>
  <script>
    // Tu código
  </script>
</body>
```

### 3. Crear Componentes

#### Stats Card
```javascript
new UILib.StatsCard('#elemento', {
  label: 'Ventas',
  value: '€45,231',
  change: '+12.5',
  changeType: 'positive',
  icon: '💰',
  iconType: 'success'
});
```

#### Data Table
```javascript
new UILib.DataTable('#tabla', {
  title: 'Listado',
  columns: [
    { field: 'id', label: 'ID', sortable: true },
    { field: 'nombre', label: 'Nombre' }
  ],
  data: tuArrayDeDatos
});
```

#### SearchableSelect
```javascript
// HTML:
<select id="miSelect">
  <option value="1">Opción 1</option>
  <option value="2">Opción 2</option>
</select>

// JS:
new UILib.SearchableSelect('#miSelect', {
  placeholder: 'Buscar...'
});
```

#### Bar Chart
```javascript
new UILib.BarChart('#grafico', {
  title: 'Ventas 2024',
  labels: ['Ene', 'Feb', 'Mar'],
  data: [100, 200, 150],
  color: '#2563eb'
});
```

#### Report Panel
```javascript
new UILib.ReportPanel('#informe', {
  title: 'Mi Informe',
  subtitle: 'Subtítulo',
  content: '<p>Contenido HTML...</p>',
  footer: 'Pie de página'
});
```

## Personalizar Estilos

### Opción 1: Variables CSS
```css
:root {
  --uil-primary: #your-color;
  --uil-success: #your-color;
  --uil-radius: 1rem;
}
```

### Opción 2: Clases Custom
```html
<style>
  .mi-tabla-custom {
    /* Tus estilos específicos */
  }
</style>

<div id="tabla" class="mi-tabla-custom"></div>
```

## Trabajar con Datos Dinámicos

### Desde API
```javascript
// Fetch data desde backend
fetch('/api/datos')
  .then(res => res.json())
  .then(datos => {
    new UILib.DataTable('#tabla', {
      title: 'Datos desde API',
      columns: [...],
      data: datos
    });
  });
```

### Actualizar Datos
```javascript
const tabla = new UILib.DataTable('#tabla', {...});

// Más tarde, actualizar:
fetch('/api/datos-nuevos')
  .then(res => res.json())
  .then(nuevosDatos => {
    tabla.updateData(nuevosDatos);
  });
```

### Con Formularios
```javascript
document.getElementById('miForm').addEventListener('submit', (e) => {
  e.preventDefault();
  
  const nuevoItem = {
    id: Date.now(),
    nombre: document.getElementById('nombre').value,
    email: document.getElementById('email').value
  };
  
  // Añadir a los datos
  misDatos.push(nuevoItem);
  
  // Actualizar tabla
  miTabla.updateData(misDatos);
});
```

## Layouts Comunes

### Grid de Stats
```html
<div class="uil-grid uil-grid-4">
  <div id="stat1"></div>
  <div id="stat2"></div>
  <div id="stat3"></div>
  <div id="stat4"></div>
</div>
```

### Dashboard 2 Columnas
```html
<div class="uil-grid uil-grid-2">
  <div id="chart1"></div>
  <div id="chart2"></div>
</div>
```

### Responsive
```html
<!-- Automático: 4 cols en desktop, 1 col en móvil -->
<div class="uil-grid uil-grid-4">
  <!-- Contenido -->
</div>
```

## Errores Comunes

### ❌ Error: Contenedor no encontrado
```javascript
// Mal - El elemento no existe
new UILib.DataTable('#noExiste', {...});

// Bien - Asegúrate que existe en el HTML
new UILib.DataTable('#miTabla', {...});
```

### ❌ Error: Script antes del HTML
```html
<!-- Mal -->
<script>
  new UILib.DataTable('#tabla', {...}); // #tabla aún no existe
</script>
<div id="tabla"></div>

<!-- Bien -->
<div id="tabla"></div>
<script>
  new UILib.DataTable('#tabla', {...}); // Ahora sí existe
</script>
```

### ❌ Error: Olvidar cargar CSS
```html
<!-- Mal - Solo JS -->
<script src="uilib.js"></script>

<!-- Bien - CSS + JS -->
<link rel="stylesheet" href="uilib.css">
<script src="uilib.js"></script>
```

## Compatibilidad con Otros Frameworks

### Con Bootstrap
```html
<link rel="stylesheet" href="bootstrap.min.css">
<link rel="stylesheet" href="uilib.css"> <!-- Después de Bootstrap -->
```

### Con Tailwind
```html
<script src="https://cdn.tailwindcss.com"></script>
<link rel="stylesheet" href="uilib.css">
```

### Con jQuery
```javascript
$(document).ready(function() {
  new UILib.DataTable('#tabla', {...});
});
```

## Ejemplos por Caso de Uso

### Dashboard Administrativo
```javascript
// KPIs
new UILib.StatsCard('#users', {
  label: 'Usuarios',
  value: '1,234',
  icon: '👥'
});

// Tabla de usuarios
new UILib.DataTable('#usersTable', {
  title: 'Usuarios',
  columns: [...],
  data: usersData
});

// Gráfico
new UILib.BarChart('#chart', {
  title: 'Actividad',
  labels: ['L', 'M', 'X', 'J', 'V'],
  data: [10, 20, 15, 25, 30]
});
```

### Formulario de Contacto
```html
<form id="contactForm">
  <input type="text" class="uil-input" placeholder="Nombre">
  <input type="email" class="uil-input" placeholder="Email">
  
  <select id="asunto">
    <option>Consulta</option>
    <option>Soporte</option>
    <option>Ventas</option>
  </select>
  
  <button class="uil-button">Enviar</button>
</form>

<script>
  new UILib.SearchableSelect('#asunto');
</script>
```

### Reportes
```javascript
new UILib.ReportPanel('#report', {
  title: 'Informe Mensual',
  subtitle: 'Octubre 2024',
  content: `
    <h4>Resumen</h4>
    <p>Este mes hemos alcanzado...</p>
    <ul>
      <li>Objetivo 1: Cumplido ✓</li>
      <li>Objetivo 2: Cumplido ✓</li>
    </ul>
  `,
  footer: 'Generado automáticamente'
});
```

## Tips y Mejores Prácticas

✅ **DO's:**
- Carga CSS en el `<head>`
- Carga JS antes de cerrar `</body>`
- Usa IDs únicos para cada componente
- Guarda referencias si necesitas actualizar: `const tabla = new UILib.DataTable(...)`

❌ **DON'Ts:**
- No modifiques directamente `uilib.js` o `uilib.css`
- No uses el mismo ID para múltiples componentes
- No olvides cargar ambos archivos (CSS + JS)

## Recursos

- **Demo completa**: `index.html`
- **Ejemplo real**: `ejemplo-proyecto-real.html`
- **E-commerce**: `ejemplo-ecommerce.html`
- **Documentación**: `README.md`

---

¿Tienes dudas? Revisa los 3 ejemplos incluidos que muestran implementaciones reales.
