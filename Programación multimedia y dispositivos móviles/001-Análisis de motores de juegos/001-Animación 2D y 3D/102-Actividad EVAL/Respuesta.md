Como aficionado al deporte y al dibujo digital, suelo bocetar personajes y pequeños escenarios en mi tiempo libre. En esta actividad uní ese hobby con la programación en HTML5 Canvas: cargué un **spritesheet de 8 frames** y lo animé sobre un **grid 16×16**, respetando las restricciones de la práctica (sin librerías externas y usando solo variables y funciones vistas en clase). El objetivo es entender los fundamentos de la **animación por sprites** y la **interacción básica con el ratón**, tal y como trabajaremos más adelante en motores 2D/3D.

---


**Estructura y buenas prácticas**
- Uso constantes para valores inmutables (`TAM_CELDA`, `FRAME_W`, `FRAME_H`, `TOTAL_FRAMES`) y variables claras para estado (`posx`, `posy`, `frame`, `temporizador`).
- Desactivo el suavizado de imagen (`contexto.imageSmoothingEnabled = false`) para mantener el pixel art nítido.
- Encapsulo tareas en funciones: `pintaEscenario()` solo dibuja el fondo y bloques; `animar()` gestiona el avance de frames y el repintado.
- Limpio el lienzo cada ciclo (`clearRect`) para evitar “fantasmas”.
- Calculo coordenadas de clic con `getBoundingClientRect()` y **convierto a celdas** con `Math.floor`, manteniendo coherencia con el grid.
- La animación usa `setTimeout(animar, 150)` y recorre el spritesheet con **módulo**: `frame = (frame + 1) % TOTAL_FRAMES;`.
- Cumplo la restricción de no usar nada externo: solo **Canvas 2D**, **eventos del DOM**, y un **spritesheet.png**.

**Ausencia de errores lógicos**
- El origen de cada frame se calcula con `sx = frame * FRAME_W` y el destino coincide con la celda (`posx`, `posy`), evitando recortes erróneos.
- El orden de pintado es correcto: primero escenario, luego sprite.
- El listener de clic actualiza posición y **repinta inmediato** para feedback visual, sin esperar al siguiente tick de la animación.

---

A continuación, explico cada paso del enunciado señalando **qué hace** y **dónde** sucede en mi código:

**1. Carga del spritesheet**
```js
const rejilla = new Image();
rejilla.src = "spritesheet.png";
rejilla.onload = function(){
  pintaEscenario();
  animar();
};
```

**2. Definición de variables**
```js
let posx = 64, posy = 64, temporizador = null;
const FRAME_W = 64, FRAME_H = 64, TOTAL_FRAMES = 8;
let frame = 0;
```

**3. Dibujo del escenario**
```js
function pintaEscenario(){
  contexto.clearRect(0,0,1024,1024);
  // Pintado del grid…
  // Relleno de celdas con 1…
}
```

**4. Animación del personaje**
```js
function animar(){
  pintaEscenario();
  const sx = frame * FRAME_W;
  contexto.drawImage(rejilla, sx, 0, FRAME_W, FRAME_H, posx, posy, FRAME_W, FRAME_H);
  frame = (frame + 1) % TOTAL_FRAMES;
  temporizador = setTimeout(animar, 150);
}
```

**5. Interacción con el ratón**
```js
lienzo.addEventListener("click", (e)=>{
  const r = lienzo.getBoundingClientRect();
  const cx = Math.floor((e.clientX - r.left)/TAM_CELDA);
  const cy = Math.floor((e.clientY - r.top)/TAM_CELDA);
  posx = cx * TAM_CELDA;
  posy = cy * TAM_CELDA;
  pintaEscenario();
  contexto.drawImage(rejilla, frame*FRAME_W, 0, FRAME_W, FRAME_H, posx, posy, FRAME_W, FRAME_H);
});
```

---

Esta práctica sienta las bases que luego abstraen los motores 2D/3D:
- **Sprites y tiles** ⇨ en motores se gestionan como **texturas** y **materiales** aplicados a entidades.
- **Bucle de animación** con `setTimeout` ⇨ en motores se usa un **game loop** (o sistema de **animaciones** y **timelines**) integrado.
- **Entrada de ratón** ⇨ en motores se canaliza por **sistemas de input** y **eventos** (con picking y colisiones).
- **Escenario por grid** ⇨ en motores se representa como **tilemaps**, **navmeshes** o **escenas** con jerarquías.

```html
<!doctype html>
<html>
  <body>
    <canvas width="1024" height="1024"></canvas>
    <script>
      // === Carga de la imagen del spritesheet ===
      const rejilla = new Image();
      rejilla.src = "spritesheet.png";

      // === Variables requeridas por el enunciado ===
      let posx = 64;          // posición en píxeles (x)
      let posy = 64;          // posición en píxeles (y)
      let temporizador = null; // id devuelto por setTimeout

      // === Mínimos necesarios para dibujar ===
      const lienzo = document.querySelector("canvas");
      const contexto = lienzo.getContext("2d");
      contexto.imageSmoothingEnabled = false;

      // Grid 16x16 (1024/16 = 64 px por celda)
      const TAM_CELDA = 64;

      // Matriz de escenario 16x16 (1 = pintar bloque)
      const escenario = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0],
        [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
        [0,1,0,0,0,1,1,1,1,1,0,0,0,0,1,0],
        [0,1,0,0,0,1,0,0,0,1,0,0,0,0,1,0],
        [0,1,0,0,0,1,0,0,0,1,0,0,0,0,1,0],
        [0,1,0,0,0,1,1,1,1,1,0,0,0,0,1,0],
        [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
        [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
        [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
        [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
        [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
        [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
      ];

      // === Dibuja el escenario (grid 16×16 y celdas con 1) ===
      function pintaEscenario(){
        contexto.clearRect(0,0,1024,1024);

        // Grid
        contexto.strokeStyle = "#222";
        for(let i=0;i<=16;i++){
          contexto.beginPath();
          contexto.moveTo(i*TAM_CELDA, 0);
          contexto.lineTo(i*TAM_CELDA, 1024);
          contexto.stroke();
          contexto.beginPath();
          contexto.moveTo(0, i*TAM_CELDA);
          contexto.lineTo(1024, i*TAM_CELDA);
          contexto.stroke();
        }

        // Celdas con valor 1
        contexto.fillStyle = "#2b2b2b";
        for(let y=0; y<16; y++){
          for(let x=0; x<16; x++){
            if(escenario[y][x] === 1){
              contexto.fillRect(
                x*TAM_CELDA, y*TAM_CELDA, TAM_CELDA, TAM_CELDA
              );
            }
          }
        }
      }

      // === Animación del personaje con setTimeout (cambia tramo) ===
      let frame = 0;            // tramo actual del spritesheet
      const FRAME_W = 64;       // ancho de frame
      const FRAME_H = 64;       // alto de frame
      const TOTAL_FRAMES = 8;   // nº tramos en fila

      function animar(){
        pintaEscenario();
        // pinta el frame actual en (posx,posy)
        const sx = frame * FRAME_W;
        contexto.drawImage(
          rejilla,
          sx, 0, FRAME_W, FRAME_H,
          posx, posy, FRAME_W, FRAME_H
        );
        frame = (frame + 1) % TOTAL_FRAMES;
        temporizador = setTimeout(animar, 150);
      }

      // === Interacción con ratón: mover el personaje al hacer clic ===
      lienzo.addEventListener("click", (e)=>{
        const r = lienzo.getBoundingClientRect();
        const cx = Math.floor((e.clientX - r.left)/TAM_CELDA);
        const cy = Math.floor((e.clientY - r.top)/TAM_CELDA);
        posx = cx * TAM_CELDA;
        posy = cy * TAM_CELDA;
        // repinta inmediato
        pintaEscenario();
        contexto.drawImage(rejilla, frame*FRAME_W, 0, FRAME_W, FRAME_H, posx, posy, FRAME_W, FRAME_H);
      });

      // === Inicio cuando cargue el spritesheet ===
      rejilla.onload = function(){
        pintaEscenario();
        animar();
      };
    </script>
  </body>
</html>
```

En resumen, he implementado una animación por sprites simple, interactiva y ordenada, respetando las restricciones del enunciado y aplicando buenas prácticas. Esto me ayuda a comprender cómo los motores encapsulan estos mismos conceptos a mayor escala y con más herramientas (sistemas de entidades, físicas y renderizado avanzado).
