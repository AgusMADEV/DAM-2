Mi proyecto es una **página HTML sencilla** para mostrar **partidos** y **videojuegos favoritos**. El objetivo es practicar **estructura semántica**, **estilos mínimos** y **uso de un CSS reset externo**, tal y como hemos visto en clase.  
Se usa en el contexto de **Desarrollo de interfaces** (tema: *Empaquetado de componentes*), donde necesitamos maquetar contenido limpio y coherente que luego podría empaquetarse o integrarse en componentes reutilizables.

---

**Definiciones y decisiones técnicas aplicadas:**
- **HTML5 semántico:** uso de `section` para agrupar contenido temático (partidos y juegos), `h1`/`h2` para jerarquía clara, y listas `ul`/`ol` para colecciones.
- **CSS reset externo:** enlazado a `https://jocarsa.github.io/cssreset/cssreset.css` para partir de una base visual neutra y evitar estilos por defecto del navegador.
- **Reactivación de viñetas y numeración:** el reset las elimina; en la hoja de estilos local las restauro (`ul, ol { padding-left: 1.5rem; }`, `ul { list-style: disc; }`, `ol { list-style: decimal; }`).
- **Tipografía y contenedor:** fuente de sistema para rendimiento y `.container` con `max-width` para una lectura cómoda.

**Funcionamiento paso a paso (según mi código):**
1. **Estructura base del documento**:  
   ```html
   <!DOCTYPE html>
   <html lang="es">
   <head>
     <meta charset="UTF-8" />
     <meta name="viewport" content="width=device-width, initial-scale=1.0" />
     <title>Mi Pagina de Deportes y Videojuegos</title>
     <link rel="stylesheet" href="https://jocarsa.github.io/cssreset/cssreset.css" />
     <style>/* estilos locales mínimos */</style>
   </head>
   <body>…</body>
   </html>
   ```
2. **Contenedor y encabezados**:  
   ```html
   <div class="container">
     <h1>Mi Pagina de Deportes y Videojuegos</h1>
     …
   </div>
   ```
3. **Sección de partidos favoritos** (lista no ordenada, `ul`):  
   ```html
   <section class="partidos_favoritos">
     <h2>Partidos Favoritos</h2>
     <ul>
       <li><strong>El Clásico:</strong> Real Madrid vs FC Barcelona — …</li>
       <li><strong>Final de Champions:</strong> Liverpool vs Tottenham — …</li>
       <li><strong>Final NBA:</strong> Warriors vs Celtics (Juego 6) — …</li>
     </ul>
   </section>
   ```
4. **Sección de juegos favoritos** (lista ordenada, `ol`):  
   ```html
   <section class="juegos_favoritos">
     <h2>Juegos Favoritos</h2>
     <ol>
       <li><strong>EA Sports FC 25</strong> — …</li>
       <li><strong>Rocket League</strong> — …</li>
       <li><strong>The Legend of Zelda: Tears of the Kingdom</strong> — …</li>
     </ol>
   </section>
   ```

**Ejemplos reales (solo del proyecto):**
- **Reset + correcciones locales**:
  ```html
  <link rel="stylesheet" href="https://jocarsa.github.io/cssreset/cssreset.css" />
  <style>
    ul, ol { padding-left: 1.5rem; }
    ul { list-style: disc; }
    ol { list-style: decimal; }
  </style>
  ```
- **Jerarquía semántica clara** (`h1` → `h2` y secciones).  
- **Contenido temático** dividido en dos bloques: deportes y videojuegos.

---

´´´
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Mi Pagina de Deportes y Videojuegos</title>
  <!-- CSS reset desde GitHub (igual que en 005-carga desde GitHub.html) -->
  <link rel="stylesheet" href="https://jocarsa.github.io/cssreset/cssreset.css" />
  <style>
    /* Estilos mínimos de demo, fiel al estilo de clase */
    body {
      font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
      padding: 2rem;
      background: #f7f7f7;
      color: #222;
    }
    h1 { font-size: 2rem; margin-bottom: 1rem; color: steelblue; }
    h2 { margin-top: 1.5rem; margin-bottom: .5rem; color: #333; }
    /* Re-activar viñetas y numeración (el reset las quita por defecto) */
    ul, ol { padding-left: 1.5rem; }
    ul { list-style: disc; }
    ol { list-style: decimal; }
    /* Pequeño contenedor para centrar un poco el contenido */
    .container { max-width: 900px; margin: 0 auto; }
    .intro { margin-bottom: 1rem; color: #555; }
  </style>
</head>
<body>
  <div class="container">
    <!-- Encabezado -->
    <h1>Mi Pagina de Deportes y Videojuegos</h1>
    <section class="partidos_favoritos">
        <h2>Partidos Favoritos</h2>
        <ul>
        <li><strong>El Clásico:</strong> Real Madrid vs FC Barcelona — Remontada épica en el segundo tiempo y gol decisivo en el 90'.</li>
        <li><strong>Final de Champions:</strong> Liverpool vs Tottenham — Presión alta, intensidad constante y un inicio de partido eléctrico.</li>
        <li><strong>Final NBA:</strong> Warriors vs Celtics (Juego 6) — Exhibición de triples y defensa cerrando la serie con autoridad.</li>
        </ul>
    </section>
    <section class="juegos_favoritos">
        <!-- Juegos Favoritos -->
        <h2>Juegos Favoritos</h2>
        <ol>
            <li><strong>EA Sports FC 25</strong> — Partidas online con amigos, modo Carrera y desafíos semanales.</li>
            <li><strong>Rocket League</strong> — Fútbol con coches, mecánicas rápidas y partidas súper competitivas.</li>
            <li><strong>The Legend of Zelda: Tears of the Kingdom</strong> — Exploración, puzzles y un mundo abierto que atrapa horas.</li>
        </ol>
    </section>
  </div>
</body>
</html>
´´´

**Cómo se aplica en la práctica:**
- Esta maqueta sirve como base para **empaquetar** cada bloque (`partidos_favoritos`, `juegos_favoritos`) en **componentes reutilizables** en el siguiente paso de la unidad.
- El uso de **reset** asegura consistencia entre navegadores; las **correcciones locales** mantienen la intención (viñetas y numeración).

**Ejemplo claro (del propio código):**
- **Listas con estilo explícito tras reset**:
  ```css
  ul, ol { padding-left: 1.5rem; }
  ul { list-style: disc; }
  ol { list-style: decimal; }
  ```
  Esto evita que el reset “aplane” la semántica visual de las listas.

**Errores comunes y cómo evitarlos (aplicados a este proyecto):**
- *Olvidar reactivar viñetas tras el reset* → listas sin marcadores.  
  **Solución:** declarar `list-style` y `padding-left` como en el ejemplo.
- *No usar jerarquía de encabezados* → mala accesibilidad/SEO.  
  **Solución:** `h1` único para el título general y `h2` para secciones.
- *No ajustar tipografía o ancho de lectura* → texto incómodo.  
  **Solución:** `.container { max-width: 900px; }` y fuente de sistema.

---

**Puntos clave:** estructura HTML5 limpia, **CSS reset** controlado con **ajustes locales**, y **secciones semánticas** para contenido de deportes y videojuegos.  
**Conexión con la unidad:** esta base es adecuada para el **empaquetado de componentes**, ya que cada bloque puede transformarse en un **componente visual reutilizable** con estilos y contenido coherentes. Esto facilita mantener y escalar la interfaz en proyectos mayores.
