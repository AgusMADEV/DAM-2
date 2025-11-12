En esta actividad he creado una **interfaz 3D interactiva** pensada como menú o “hub” visual para un videojuego. El objetivo principal es practicar con **CSS3D** y **JavaScript** para simular profundidad, parallax y reacción al movimiento del ratón, conceptos muy relacionados con los **motores de juegos modernos**, donde la interfaz no es algo plano, sino parte de la experiencia visual.

La escena que he construido representa diferentes componentes típicos de un juego:

- Personaje principal  
- Sistema de enemigos  
- Arsenal de armas  
- Mundo abierto  
- Sistema de misiones  
- Modo multijugador  

Cada uno se muestra como una tarjeta flotando en un entorno 3D. De esta forma conecto directamente el ejercicio con la creación de interfaces para videojuegos: no solo muestro información, también transmito sensación de espacio, jerarquía visual y “feedback” al jugador.

---

He trabajado únicamente con **HTML, CSS3D y JavaScript**, sin librerías externas, siguiendo lo visto en clase.

### Capas 3D y escena

La estructura principal parte de estos contenedores:

```html
<div class="scene" id="scene">
  <header>...</header>
  <div class="stage" id="stage">
    <!-- depth-layer + floor-shadow + game-grid -->
  </div>
</div>
```

- `.scene` define la **perspectiva** con `perspective: var(--perspective);`.
- `.stage` usa `transform-style: preserve-3d;` y variables `--rx` y `--ry` para rotar toda la escena en función del ratón.
- Las capas SVG con clase `.depth-layer` funcionan como **planos de fondo** con diferentes valores `--z`, `--px` y `--py` para lograr el efecto **parallax 3D**.

### Tarjetas 3D interactivas

Cada elemento del juego es una tarjeta:

```html
<article class="game-card" data-type="player" tabindex="0">
  <div class="card-bg"></div>
  <div class="card-overlay"></div>
  <div class="card-content">
    <div class="card-icon">⚔️</div>
    <h2 class="card-title">Personaje Principal</h2>
    <p class="card-description">Héroe personalizable con habilidades únicas y sistema de progresión</p>
    <span class="card-tag">Jugador</span>
  </div>
</article>
```

En CSS:

- Uso `transform-style: preserve-3d;` en `.game-card`.
- Cada tarjeta tiene una variable `--dz` controlada por JS para ajustar su **profundidad**.
- En `:hover` aplico:

```css
.game-card:hover{
  transform:
    translateZ(calc(var(--dz) + 80px))
    rotateX(-3deg)
    rotateY(3deg)
    scale(1.02);
}
```

Esto respeta el criterio: las capas 3D están correctamente implementadas con transformaciones y se añade interactividad visual sin salirnos de CSS3D.

### Lógica JavaScript (sin librerías)

En el `<script>`:

- Referencio `scene`, `stage` y todas las `.game-card`.
- Normalizo la posición del ratón y actualizo las variables CSS:

```js
const { nx, ny } = normalizePointer(pointer.clientX, pointer.clientY);
stage.style.setProperty('--mx', nx.toFixed(4));
stage.style.setProperty('--my', ny.toFixed(4));
targetRY = -nx * config.maxRotateY;
targetRX = ny * config.maxRotateX;
```

- En función de la cercanía del ratón a cada tarjeta, calculo una profundidad:

```js
const depth = influence * config.maxCardDepth;
element.style.setProperty('--dz', `${depth.toFixed(2)}px`);
```

- Uso un bucle con `requestAnimationFrame` para interpolar suavemente (`ease`) entre la rotación actual y la deseada, simulando una **cámara suave**, muy típico en motores de juego.

Todo el desarrollo respeta las restricciones: sin librerías externas, solo HTML, CSS3D y JS básico.

---

Al probar la interfaz, el comportamiento es el siguiente:

1. **Movimiento del ratón sobre la escena**  
   - Al mover el ratón, la cámara rota ligeramente (`rotateX`, `rotateY`) y las capas `.depth-layer` se desplazan con distinta intensidad.  
   - Esto genera un **efecto 3D dinámico** que simula un menú de videojuego vivo.

2. **Interacción con las tarjetas (`.game-card`)**  
   - Cuando acerco el ratón a una tarjeta, su variable `--dz` aumenta y la tarjeta se “acerca” visualmente al jugador.  
   - Al pasar por encima (`hover`), la tarjeta:
     - Se eleva más (`translateZ`),
     - Se inclina un poco,
     - Aumenta la sombra y resalta el borde.
   - El resultado es un feedback muy claro para el usuario, como si seleccionara un módulo del juego (personaje, misiones, multijugador…).

3. **Accesibilidad básica con teclado**
   - Cada `.game-card` tiene `tabindex="0"`.
   - En foco (`focus`) se incrementa `--dz`, así que también hay **feedback visual** si navego con teclado.

Gracias a estas pruebas puedo ver claramente cómo la interfaz responde a la interacción y cómo los elementos 3D ayudan a guiar al jugador hacia las secciones importantes del juego.

---

Este ejercicio me ha servido para entender cómo los **componentes visuales 3D** que usamos en interfaces web se parecen mucho a los que encontramos en un **motor de videojuegos**:

- He trabajado con **capas**, **profundidad**, **cámara**, **parallax** y **feedback al usuario**, igual que haría en un HUD o menú principal dentro de un juego.
- Sin usar librerías externas, solo con **CSS3D + JavaScript**, he conseguido una interfaz fluida y atractiva, aplicando conceptos vistos en clase (transformaciones 3D, eventos de ratón, animación con `requestAnimationFrame`).

En futuros proyectos de videojuegos podría reutilizar este enfoque para:
- Menús principales 3D,
- Selección de personajes o mapas,
- Pantallas de configuración con tarjetas interactivas,
- Dashboards de juego con información contextual.

En resumen, esta práctica me ayuda a conectar directamente la teoría de **componentes de un motor de juegos** con una implementación real y visual que podría formar parte del frontend de un videojuego moderno.
