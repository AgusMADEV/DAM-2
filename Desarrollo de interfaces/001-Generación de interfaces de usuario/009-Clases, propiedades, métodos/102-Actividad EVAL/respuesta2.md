JocarsaUX es una clase JavaScript que funciona como **mini framework de generación de interfaces dinámicas a partir de datos JSON**, sin librerías externas. Su propósito es automatizar la creación de:

- Tablas interactivas con filtros, ordenación y paginación.
- Formularios inteligentes basados en los datos.
- Gráficos sencillos para analizar distribuciones.

Dentro de la asignatura *Desarrollo de interfaces*, JocarsaUX se usa para practicar:

- Clases, propiedades y métodos en JavaScript.
- Renderizado dinámico en el DOM usando solo JS nativo.
- Separación entre datos (`datos-*.js`), lógica (`jocarsaux4.js`) y vistas (`index.html`, `ejemplos-avanzados.html`).

Es especialmente útil cuando necesitamos prototipos rápidos y coherentes a partir de ficheros JSON locales, tal y como se plantea en la actividad EVAL.

---

### Arquitectura básica

En `jocarsaux4.js` se define:

- Un *namespace* visual (`jux-`) y `ensureStyles()`, que inyecta los estilos necesarios.
- Utilidades internas:
  - `normalizeTop(json)`: garantiza trabajar con un array de registros.
  - `flatten(value)`: aplana objetos/arrays anidados (clave.clave.hija) para poder mostrarlos.
  - `collectColumns(rows)`: detecta todas las columnas presentes.
  - `analyzeField(values)`: decide el tipo de input adecuado (texto, número, select, textarea).
  - `analyzeForChart(values)`: detecta columnas válidas para gráficos de distribución.
- Un estado interno por instancia:
  - `columns`, `rows`, `view`: datos originales y filtrados.
  - `sort`: campo y dirección de ordenación.
  - `query`: texto de búsqueda.
  - `page`, `rowsPerPage`: control de paginación.
  - Referencias a nodos del DOM para rerenderizar sin recargar.

Sobre esta base se construyen los métodos públicos clave:

- `tableRenderer(...)`
- `formRenderer(...)`
- `chartRenderer(...)`
- (y complementos: `gridRenderer`, `menuRenderer`)

Todos comparten la misma filosofía: **reciben datos JSON + un contenedor → generan interfaz completa y usable**.

### tableRenderer: tablas con búsqueda, orden y paginación

`tableRenderer({ target, data, title, subtitle, rowsPerPage, flattenObjects })`:

1. Limpia el contenedor (`target`) y aplica la estructura base.
2. Normaliza y aplana los datos (`normalizeTop`, `flatten`).
3. Calcula las columnas con `collectColumns`.
4. Pinta:
   - Barra superior con:
     - Etiqueta “Table demo”.
     - Cuadro de búsqueda que llama a `setFilter`.
   - Cabecera con columnas ordenables (`sortBy`).
   - Cuerpo paginado (`_renderBody`).
   - Controles de paginación (`_renderPagination`).

En `index.html` se aplica a `datosDeportivos`:

```js
const uxTabla = new JocarsaUX();
uxTabla.tableRenderer({
    target: mainContainer,
    data: datosDeportivos,
    title: '🏆 Estadísticas del Torneo de Fútbol',
    subtitle: 'Tabla interactiva con filtros y ordenamiento - Temporada 2024',
    rowsPerPage: 8
});
```

Esto permite al usuario:

- Buscar equipos por nombre, ciudad o entrenador.
- Ordenar por puntos, goles, etc.
- Navegar entre páginas sin recargar la web.

### formRenderer: formularios generados desde datos

`formRenderer({ target, data, title, columns, onSubmit, onReset })`:

1. Usa uno o varios registros como **modelo**.
2. Aplana y analiza cada columna con `analyzeField`:
   - Si todos los valores son numéricos → `input type="number"`.
   - Si hay pocas opciones repetidas → `select` con esas opciones.
   - Si los textos son largos → `textarea`.
   - En otros casos → `input type="text"`.
3. Construye una rejilla de campos (`columns` columnas).
4. Añade botones:
   - `Submit` → recoge valores y llama a `onSubmit`.
   - `Reset` → limpia el formulario y ejecuta `onReset` si existe.

Ejemplo real de la actividad con `datosGaming`:

```js
const uxForm = new JocarsaUX();
uxForm.formRenderer({
    target: mainContainer,
    data: [datosGaming[0]], // registro modelo
    title: '🎮 Registro de Puntuaciones Gaming',
    subtitle: 'Formulario inteligente con tipos de campo automáticos',
    columns: 2,
    onSubmit: (datos) => {
        alert(
          'Puntuación registrada:' + '\\n' +
          Object.entries(datos).map(([k, v]) => `${k}: ${v}`).join('\\n')
        );
    }
});
```

Esto conecta directamente con el hobby de videojuegos: el usuario puede introducir sus propias puntuaciones con una interfaz coherente y generada automáticamente.

### chartRenderer: gráficos automáticos a partir de categorías

`chartRenderer({ target, data, title, subtitle })`:

1. Normaliza y aplana los datos.
2. Recorre las columnas:
   - Para cada una, `analyzeForChart` calcula frecuencia de valores.
   - Solo genera gráfico si:
     - Hay valores repetidos (tiene sentido estadístico),
     - El número de categorías es razonable.
3. Crea un gráfico de pastel (pie) con SVG:
   - Cada sector representa una categoría.
   - Se acompaña de leyenda con etiqueta, recuento y porcentaje.

Ejemplo con `datosTurismo`:

```js
const uxCharts = new JocarsaUX();
uxCharts.chartRenderer({
    target: mainContainer,
    data: datosTurismo,
    title: '✈️ Estadísticas Turísticas Globales',
    subtitle: 'Gráficos automáticos por campos categóricos (región, temporada, tipo_turismo)'
});
```

Así se relaciona JocarsaUX con el hobby de viajar: se visualizan destinos, temporadas altas o tipos de turismo sin programar gráficos desde cero.

---

### Resumen de usos en la actividad

Con los ficheros proporcionados se cubren los tres ámbitos:

1. **Deportes (`datos-deportivos.js`)**  
   - `tableRenderer` para mostrar:
     - puntos, victorias, goles, etc.
   - `gridRenderer` para fichas visuales de equipos.
2. **Videojuegos (`datos-gaming.js`)**
   - `formRenderer` para registrar o simular altas de jugadores y puntuaciones.
   - `tableRenderer` para ranking de jugadores.
3. **Turismo (`datos-turismo.js`)**
   - `chartRenderer` para ver distribución por región / temporada / tipo.
   - `formRenderer` opcional para añadir nuevos destinos.

En `index.html` y `ejemplos-avanzados.html` se integran estos usos a través de `menuRenderer`, creando una navegación única que demuestra:

- Búsqueda y ordenación.
- Paginación.
- Vistas en tabla, cards y gráficos.
- Personalización de estilos y ejemplos avanzados sin salir del contexto del temario.

---

###  Ejemplo completo mínimo (adaptado al proyecto)

```html
<div id="app"></div>

<script src="jocarsaux4.js"></script>
<script src="datos-deportivos.js"></script>
<script>
  const ux = new JocarsaUX();

  // 1) Tabla deportiva
  ux.tableRenderer({
      target: '#app',
      data: datosDeportivos,
      title: 'Liga - Clasificación',
      subtitle: 'Buscar, ordenar y paginar equipos',
      rowsPerPage: 5
  });
</script>
```

---

JocarsaUX demuestra cómo, mediante una única clase bien diseñada, es posible:

- Reutilizar lógica de interfaz para diferentes dominios (deportes, gaming, turismo).
- Integrar:
  - Tablas con filtros y ordenación (`tableRenderer`),
  - Formularios autogenerados (`formRenderer`),
  - Gráficos categóricos (`chartRenderer`),
  - Navegación y vistas en tarjetas (`menuRenderer`, `gridRenderer`).
- Trabajar exclusivamente con tecnologías vistas en la unidad:
  - HTML + CSS,
  - JavaScript nativo,
  - Clases, métodos, manipulación del DOM, eventos.

Este enfoque conecta directamente con otros contenidos de la unidad como:
- **POO en JavaScript** (clases y encapsulación),
- **Componentes reutilizables de interfaz**,
- **Buenas prácticas de separación datos / lógica / presentación**.

La actividad EVAL, apoyada en JocarsaUX, no solo valida que se comprende la sintaxis, sino que el alumnado sabe aplicarla para construir interfaces funcionales, escalables y mantenibles sin depender de frameworks externos.
