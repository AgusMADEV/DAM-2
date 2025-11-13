# 📚 Guía de Uso - Librería de Componentes UI

## 🎯 ¿Qué es esta librería?

Una librería simple de componentes visuales reutilizables para proyectos HTML/CSS/JS sin dependencias externas. Incluye 5 componentes listos para usar: tablas, selectores, gráficos, tarjetas estadísticas y paneles de informe.

## 📦 Estructura del Proyecto

```
102-Actividad Final/
├── componentes.js    → Funciones de los componentes
├── estilos.css       → Estilos de todos los componentes
├── index.html        → Ejemplo de uso completo
├── README.md         → Documentación básica
└── GUIA-DE-USO.md    → Este archivo
```

## 🚀 Instalación

### 1. Incluir los archivos en tu proyecto

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Mi Proyecto</title>
    <!-- Incluir los estilos -->
    <link rel="stylesheet" href="estilos.css">
</head>
<body>
    <div id="app">
        <!-- Aquí van tus componentes -->
    </div>

    <!-- Incluir el JavaScript -->
    <script src="componentes.js"></script>
    <script>
        // Tu código aquí
    </script>
</body>
</html>
```

## 🔧 Componentes Disponibles

### 1️⃣ Tabla de Datos (`crearTabla`)

**¿Qué hace?** Crea una tabla con búsqueda integrada.

**Sintaxis:**
```javascript
crearTabla(contenedor, datos, columnas, config)
```

**Parámetros:**
- `contenedor` (string): ID del elemento donde se insertará
- `datos` (array): Array de objetos con los datos
- `columnas` (array): Array de objetos con `{campo, titulo}`
- `config` (object): Configuración opcional `{busqueda: true, placeholder: "..."}`

**Ejemplo:**
```javascript
const estudiantes = [
    { nombre: "Ana García", edad: 22, curso: "DAM" },
    { nombre: "Luis Pérez", edad: 21, curso: "DAW" },
    { nombre: "María López", edad: 23, curso: "DAM" }
];

crearTabla('contenedor-tabla', estudiantes, [
    { campo: 'nombre', titulo: 'Nombre Completo' },
    { campo: 'edad', titulo: 'Edad' },
    { campo: 'curso', titulo: 'Curso' }
], {
    busqueda: true,
    placeholder: 'Buscar estudiante...'
});
```

**Características:**
- ✅ Búsqueda en tiempo real
- ✅ Resaltado de coincidencias
- ✅ Diseño responsive
- ✅ Hover effects

---

### 2️⃣ Select Buscable (`crearSelectBuscable`)

**¿Qué hace?** Crea un desplegable con buscador integrado.

**Sintaxis:**
```javascript
crearSelectBuscable(contenedor, opciones, config)
```

**Parámetros:**
- `contenedor` (string): ID del elemento donde se insertará
- `opciones` (array): Array de objetos con `{valor, texto}`
- `config` (object): Configuración `{placeholder, onChange}`

**Ejemplo:**
```javascript
const paises = [
    { valor: 'es', texto: 'España 🇪🇸' },
    { valor: 'mx', texto: 'México 🇲🇽' },
    { valor: 'ar', texto: 'Argentina 🇦🇷' },
    { valor: 'co', texto: 'Colombia 🇨🇴' }
];

crearSelectBuscable('selector-pais', paises, {
    placeholder: 'Selecciona un país...',
    onChange: (valor, texto) => {
        console.log('País seleccionado:', valor, texto);
        alert(`Has elegido: ${texto}`);
    }
});
```

**Características:**
- ✅ Búsqueda fuzzy (tolerante a errores)
- ✅ Filtrado en tiempo real
- ✅ Callback al seleccionar
- ✅ Cierre automático al hacer clic fuera
- ✅ Scrollbar personalizada

---

### 3️⃣ Gráfico de Barras (`crearGrafico`)

**¿Qué hace?** Dibuja un gráfico de barras usando Canvas API.

**Sintaxis:**
```javascript
crearGrafico(contenedor, datos, config)
```

**Parámetros:**
- `contenedor` (string): ID del elemento donde se insertará
- `datos` (array): Array de objetos con `{etiqueta, valor}`
- `config` (object): Configuración `{color, ancho, alto}`

**Ejemplo:**
```javascript
const ventasMensuales = [
    { etiqueta: 'Enero', valor: 4500 },
    { etiqueta: 'Febrero', valor: 5200 },
    { etiqueta: 'Marzo', valor: 6800 },
    { etiqueta: 'Abril', valor: 5900 },
    { etiqueta: 'Mayo', valor: 7200 }
];

crearGrafico('grafico-ventas', ventasMensuales, {
    color: '#3b82f6',
    ancho: 600,
    alto: 400
});
```

**Características:**
- ✅ Canvas nativo (sin librerías)
- ✅ Responsive
- ✅ Colores personalizables
- ✅ Tooltips al hover
- ✅ Animaciones suaves

---

### 4️⃣ Tarjeta de Estadística (`crearTarjeta`)

**¿Qué hace?** Muestra un KPI o estadística destacada.

**Sintaxis:**
```javascript
crearTarjeta(contenedor, datos)
```

**Parámetros:**
- `contenedor` (string): ID del elemento donde se insertará
- `datos` (object): Objeto con `{titulo, valor, icono, color}`

**Ejemplo:**
```javascript
crearTarjeta('tarjeta-usuarios', {
    titulo: 'Usuarios Activos',
    valor: '1,234',
    icono: '👥',
    color: '#10b981'
});

crearTarjeta('tarjeta-ventas', {
    titulo: 'Ventas del Mes',
    valor: '€45,678',
    icono: '💰',
    color: '#f59e0b'
});

crearTarjeta('tarjeta-productos', {
    titulo: 'Productos',
    valor: '89',
    icono: '📦',
    color: '#6366f1'
});
```

**Características:**
- ✅ Iconos emoji
- ✅ Colores personalizables
- ✅ Efecto de elevación al hover
- ✅ Borde de acento
- ✅ Diseño minimalista

---

### 5️⃣ Panel de Informe (`crearInforme`)

**¿Qué hace?** Crea un panel con título y contenido personalizado.

**Sintaxis:**
```javascript
crearInforme(contenedor, datos)
```

**Parámetros:**
- `contenedor` (string): ID del elemento donde se insertará
- `datos` (object): Objeto con `{titulo, contenido}`

**Ejemplo:**
```javascript
crearInforme('panel-resumen', {
    titulo: 'Resumen Ejecutivo 2024',
    contenido: `
        <h3>Análisis de Resultados</h3>
        <p>Durante el último trimestre hemos observado:</p>
        <ul>
            <li>Incremento del 35% en usuarios activos</li>
            <li>Mejora del 28% en conversiones</li>
            <li>Reducción del 15% en costes operativos</li>
        </ul>
        <p><strong>Conclusión:</strong> Los objetivos se han superado.</p>
    `
});
```

**Características:**
- ✅ Acepta HTML
- ✅ Encabezado con degradado
- ✅ Tipografía mejorada
- ✅ Contenedor flexible

---

## 💡 Ejemplo Completo

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Dashboard Empresarial</title>
    <link rel="stylesheet" href="estilos.css">
    <style>
        body {
            font-family: system-ui, -apple-system, sans-serif;
            margin: 0;
            padding: 2rem;
            background: #f9fafb;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        section {
            margin-bottom: 2rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Dashboard de Ventas</h1>
        
        <!-- Tarjetas de estadísticas -->
        <section class="grid-4">
            <div id="tarjeta-1"></div>
            <div id="tarjeta-2"></div>
            <div id="tarjeta-3"></div>
            <div id="tarjeta-4"></div>
        </section>

        <!-- Gráfico y Selector -->
        <section class="grid-2">
            <div id="contenedor-grafico"></div>
            <div id="contenedor-selector"></div>
        </section>

        <!-- Tabla de datos -->
        <section>
            <div id="contenedor-tabla"></div>
        </section>

        <!-- Panel de informe -->
        <section>
            <div id="contenedor-informe"></div>
        </section>
    </div>

    <script src="componentes.js"></script>
    <script>
        // Tarjetas KPI
        crearTarjeta('tarjeta-1', {
            titulo: 'Ventas Totales',
            valor: '€125,450',
            icono: '💰',
            color: '#10b981'
        });

        crearTarjeta('tarjeta-2', {
            titulo: 'Clientes Nuevos',
            valor: '342',
            icono: '👥',
            color: '#3b82f6'
        });

        crearTarjeta('tarjeta-3', {
            titulo: 'Pedidos',
            valor: '1,089',
            icono: '📦',
            color: '#f59e0b'
        });

        crearTarjeta('tarjeta-4', {
            titulo: 'Satisfacción',
            valor: '4.8/5',
            icono: '⭐',
            color: '#8b5cf6'
        });

        // Gráfico de ventas mensuales
        const ventasMensuales = [
            { etiqueta: 'Ene', valor: 12500 },
            { etiqueta: 'Feb', valor: 15800 },
            { etiqueta: 'Mar', valor: 18200 },
            { etiqueta: 'Abr', valor: 16900 },
            { etiqueta: 'May', valor: 21400 },
            { etiqueta: 'Jun', valor: 23700 }
        ];

        crearGrafico('contenedor-grafico', ventasMensuales, {
            color: '#3b82f6',
            ancho: 600,
            alto: 350
        });

        // Selector de región
        const regiones = [
            { valor: 'norte', texto: 'Región Norte' },
            { valor: 'sur', texto: 'Región Sur' },
            { valor: 'este', texto: 'Región Este' },
            { valor: 'oeste', texto: 'Región Oeste' },
            { valor: 'centro', texto: 'Región Centro' }
        ];

        crearSelectBuscable('contenedor-selector', regiones, {
            placeholder: 'Selecciona una región...',
            onChange: (valor, texto) => {
                console.log('Región seleccionada:', valor);
            }
        });

        // Tabla de productos top
        const productos = [
            { nombre: 'Laptop HP', ventas: 145, ingresos: 87000 },
            { nombre: 'Mouse Logitech', ventas: 432, ingresos: 12960 },
            { nombre: 'Teclado Mecánico', ventas: 287, ingresos: 28700 },
            { nombre: 'Monitor 27"', ventas: 98, ingresos: 34300 },
            { nombre: 'Webcam HD', ventas: 203, ingresos: 10150 }
        ];

        crearTabla('contenedor-tabla', productos, [
            { campo: 'nombre', titulo: 'Producto' },
            { campo: 'ventas', titulo: 'Unidades Vendidas' },
            { campo: 'ingresos', titulo: 'Ingresos (€)' }
        ], {
            busqueda: true,
            placeholder: 'Buscar producto...'
        });

        // Panel de informe
        crearInforme('contenedor-informe', {
            titulo: 'Informe del Trimestre',
            contenido: `
                <h3>Resultados Q2 2024</h3>
                <p>El segundo trimestre ha mostrado un crecimiento excepcional:</p>
                <ul>
                    <li><strong>Crecimiento:</strong> +45% respecto al trimestre anterior</li>
                    <li><strong>Nuevos clientes:</strong> 342 registros</li>
                    <li><strong>Tasa de retención:</strong> 92%</li>
                    <li><strong>Productos más vendidos:</strong> Laptops y periféricos</li>
                </ul>
                <p><em>Las proyecciones para Q3 son muy positivas.</em></p>
            `
        });
    </script>
</body>
</html>
```

---

## 🎨 Personalización de Estilos

### Cambiar colores globales

Edita las variables CSS en `estilos.css`:

```css
:root {
    --color-primario: #3b82f6;
    --color-hover: #2563eb;
    --color-fondo: #ffffff;
    --color-borde: #e5e7eb;
}
```

### Modificar el comportamiento de un componente

Edita la función correspondiente en `componentes.js`. Por ejemplo, para cambiar el algoritmo de búsqueda de la tabla:

```javascript
// En la función crearTabla, línea ~40
function filtrarTabla() {
    const busqueda = inputBuscar.value.toLowerCase();
    // Aquí puedes cambiar la lógica de búsqueda
}
```

---

## 📱 Responsive Design

Todos los componentes son responsive automáticamente:

- **Desktop** (>1024px): Grid de 4 columnas
- **Tablet** (768px-1024px): Grid de 2 columnas
- **Mobile** (<768px): 1 columna

Las clases de utilidad `.grid-2`, `.grid-3`, `.grid-4` se ajustan automáticamente.

---

## ⚡ Rendimiento

### Optimizaciones implementadas:

1. **Sin dependencias externas** → Carga rápida
2. **Vanilla JavaScript** → Sin overhead de frameworks
3. **Event delegation** → Menos listeners
4. **CSS moderno** → Transiciones GPU-accelerated
5. **Búsqueda eficiente** → Algoritmo optimizado

### Buenas prácticas:

- ✅ Limita las tablas a <1000 filas
- ✅ Usa selectores con <200 opciones
- ✅ Actualiza gráficos solo cuando cambien datos
- ✅ Reutiliza componentes en lugar de recrearlos

---

## 🐛 Solución de Problemas

### El componente no aparece

```javascript
// ❌ Incorrecto
crearTabla('tabla', datos, columnas);

// ✅ Correcto - El contenedor debe existir en el HTML
<div id="contenedor-tabla"></div>
crearTabla('contenedor-tabla', datos, columnas);
```

### Los estilos no se aplican

```html
<!-- Asegúrate de incluir el CSS ANTES del body -->
<head>
    <link rel="stylesheet" href="estilos.css">
</head>
```

### El select no filtra correctamente

```javascript
// El texto de búsqueda debe estar en minúsculas
const opciones = [
    { valor: '1', texto: 'España' }, // ✅ Correcto
    { valor: '2', texto: 'MÉXICO' }  // ⚠️ Funciona pero menos eficiente
];
```

### El gráfico no se redimensiona

```javascript
// Usa porcentaje de ancho en lugar de píxeles fijos
crearGrafico('grafico', datos, {
    ancho: contenedor.offsetWidth, // ✅ Se adapta al contenedor
    alto: 400
});
```

---

## 📚 Conceptos de Clase Aplicados

### 003 - Eventos
- `addEventListener` para clicks, inputs, focus, blur
- Event delegation en tablas
- Propagación de eventos (stopPropagation)
- Eventos de teclado en búsquedas

### 004 - Persistencia
- Componentes mantienen estado interno
- Datos encapsulados en closures
- Callbacks para comunicación entre componentes

### 007 - Empaquetado
- Librería modular y reutilizable
- Separación CSS/JS
- Sin conflictos de nombres (scoping)
- Fácil integración en cualquier proyecto

---

## 🚀 Próximos Pasos

1. **Practica** con los ejemplos en `index.html`
2. **Modifica** los estilos según tu marca
3. **Integra** en tu proyecto real
4. **Extiende** con nuevos componentes

---

## 📞 Soporte

Si tienes dudas o problemas:
1. Revisa esta guía completa
2. Inspecciona el código en `componentes.js`
3. Consulta el ejemplo en `index.html`
4. Experimenta en tu navegador con DevTools

---

**¡Listo para crear interfaces increíbles! 🎉**
