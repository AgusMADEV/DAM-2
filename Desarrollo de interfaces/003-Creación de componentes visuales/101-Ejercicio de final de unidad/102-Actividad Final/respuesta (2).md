
En esta actividad he desarrollado una **librería simple de componentes de interfaz de usuario** que se integra en cualquier proyecto **HTML + CSS + JavaScript** sin dependencias. La librería aborda cuatro familias habituales en entornos empresariales:

- **Componentes de tabla** con búsqueda integrada.
- **Componentes de informes** (panel con cabecera y cuerpo).
- **Componentes de gráficas** (gráfico de barras en `<canvas>` 2D).
- **Componentes de formularios** (select con búsqueda) y **tarjetas de estadística** para KPIs.

El objetivo es **reutilizar** estos bloques en diferentes pantallas mediante una **API clara** basada en funciones y un **CSS desacoplado**. El contexto de uso es cualquier frontend con necesidades de **listado, filtrado, visualización de métricas e informes** sin frameworks.

---

###  Estructura general
- **`componentes.js`** expone funciones puras que generan UI en un contenedor destino.
- **`estilos.css`** define los estilos reutilizables (tablas, paneles, tarjetas, select buscable, canvas).
- **`index.html`** actúa como demo de integración y de la **API pública**.

###  Componentes y API

#### A) Tabla con búsqueda
- **Función pública:** `crearTabla(contenedorId, opciones)`  
- **Parámetros de `opciones`:**  
  - `titulo`: título del listado.  
  - `columnas`: `{ campo, label }` para mapear claves de datos a cabeceras.  
  - `datos`: array de objetos a renderizar.
- **Comportamiento:** crea una cabecera con buscador, renderiza `<table>` y filtra en tiempo real usando `input[type=search]`.  
- **Código usado (del proyecto):**
```js
crearTabla('tabla', {
  titulo: 'Lista de Empleados',
  columnas: [
    { campo: 'id', label: 'ID' },
    { campo: 'nombre', label: 'Nombre' },
    { campo: 'puesto', label: 'Puesto' },
    { campo: 'salario', label: 'Salario' }
  ],
  datos: empleados
});
```

#### Select con búsqueda (formulario)
- **Función pública:** `crearSelectBuscable(selectId)`  
- **Comportamiento:** envuelve un `<select>` existente, oculta el original y crea un **input de búsqueda** + panel de opciones filtrables. Al hacer clic en una opción, **sincroniza** `select.value` e **inyecta** el texto en el input.
- **Código usado (del proyecto):**
```js
crearSelectBuscable('paises');
```

#### Gráfico de barras (visualización)
- **Función pública:** `crearGrafico(canvasId, opciones)`  
- **Parámetros de `opciones`:** `titulo`, `etiquetas`, `valores`.  
- **Comportamiento:** con **Canvas 2D** calcula escalas básicas (padding, ancho de barra, altura relativa por `maxValor`) y dibuja barras + etiquetas y valores.
- **Código usado (del proyecto):**
```js
crearGrafico('grafico', {
  titulo: 'Ventas Mensuales',
  etiquetas: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
  valores: [65, 78, 90, 81, 95, 102]
});
```

#### Tarjeta de estadística (KPI)
- **Función pública:** `crearTarjeta(contenedorId, opciones)` con `titulo`, `valor`, `icono`, `color`.  
- **Comportamiento:** muestra una **card semántica** con icono grande, texto y un borde de color (inline style) que indica el **estado/métrica**.
- **Código usado (del proyecto):**
```js
crearTarjeta('tarjeta1', {
  titulo: 'Empleados',
  valor: '125',
  icono: '👥',
  color: '#3b82f6'
});
```

#### Panel de informe
- **Función pública:** `crearInforme(contenedorId, opciones)` con `titulo` y `contenido` (HTML).  
- **Comportamiento:** compone cabecera **gradiente** y cuerpo con **tipografía de lectura** para resúmenes.
- **Código usado (del proyecto):**
```js
crearInforme('informe', {
  titulo: 'Resumen del Mes',
  contenido: `
    <p><strong>Total de ventas:</strong> €89,450</p>
    <p><strong>Nuevos clientes:</strong> 23</p>
    <p><strong>Proyectos completados:</strong> 8</p>
    <p>El mes ha sido muy productivo con un incremento del 15% en ventas.</p>
  `
});
```

###  Funcionamiento paso a paso (ejemplo: tabla)
1. **Inicialización:** `crearTabla` compone el contenedor con buscador + `<table>` y cabezera calculada desde `columnas`.
2. **Render:** genera `<tbody>` mapeando `datos` → `td` en el orden de `columnas`.
3. **Filtrado:** en `input` se recalcula `datosFiltrados` buscando el término en **todas** las columnas (`toLowerCase()`), y se vuelve a renderizar el cuerpo.
4. **Estilos:** las clases `.tabla-*` del CSS aplican jerarquía visual, estados hover y tipografía.

### Decisiones técnicas
- **API mínima** y **tipada por contrato** (nombres de claves en `columnas`), para favorecer la **reutilización**.
- **Separación de responsabilidades:** datos en JS, estilos en CSS, estructura en HTML.
- **Sin dependencias externas**, alineado con los contenidos de la unidad.

---

### Integración en una vista (demo del proyecto)
En `index.html` instancia cada componente pasando **solo datos y configuración**, lo que demuestra la **reutilización** en una página cualquiera.

- **Datos de ejemplo** usados por la tabla:
```js
const empleados = [
  { id: 1, nombre: 'Ana García', puesto: 'Desarrolladora', salario: '45000€' },
  { id: 2, nombre: 'Carlos López', puesto: 'Diseñador', salario: '38000€' },
  { id: 3, nombre: 'María Fernández', puesto: 'Gerente', salario: '55000€' },
  { id: 4, nombre: 'Juan Martínez', puesto: 'Analista', salario: '42000€' },
  { id: 5, nombre: 'Laura Sánchez', puesto: 'Desarrolladora', salario: '47000€' }
];
```

- **Select buscable** aplicado a un `<select id="paises">` con varias opciones.
- **Gráficos de barras** en dos `canvas` independientes para verificar **reusabilidad**.

### Errores comunes y cómo evitarlos
1. **IDs inexistentes** en el DOM: asegurar que el `contenedorId`/`canvasId`/`selectId` **existe** antes de invocar la función.
2. **Desalineo datos‑columnas:** las claves en `columnas[i].campo` deben **coincidir** con las propiedades reales de cada objeto en `datos` (p. ej., `nombre`, `puesto`, etc.).
3. **Canvas sin tamaño adecuado:** fijar `width` y `height` en el `<canvas>` para evitar borrosidad.
4. **Estilos no cargados:** incluir `estilos.css` para jerarquía visual, focus states y responsividad.
5. **Clic fuera del select:** el panel se cierra al hacer clic fuera; mantener el **listener** global cargado por el componente.
6. **Accesibilidad básica:** garantizar contraste y textos descriptivos (títulos/labels).

---

La librería encapsula **patrones UI empresariales**: listados con búsqueda, KPIs, informes y selección asistida, además de gráficos básicos. La **API simple** y la **separación HTML‑CSS‑JS** facilitan **reutilización, mantenimiento y extensión**.

Conecta con: **componentización**, **estilos modulares**, **eventos DOM**, **renderizado desde datos** y **layout responsive**. La base queda lista para ampliar con paginación, nuevas visualizaciones en canvas y validaciones, manteniendo la misma filosofía.
