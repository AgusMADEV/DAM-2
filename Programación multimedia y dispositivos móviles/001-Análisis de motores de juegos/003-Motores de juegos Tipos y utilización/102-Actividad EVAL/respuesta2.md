En esta actividad he creado un **sistema sencillo de partículas en HTML5 Canvas y JavaScript** para simular un efecto visual parecido a los que se utilizan en motores de juegos (por ejemplo, chispas, disparos, humo o magia).  
El objetivo es entender cómo, a partir de una clase `Particula` y unos cuantos controles (`ángulo`, `velocidad` y `amplitud`), se puede generar un comportamiento visual dinámico, muy similar al de un **emisor de partículas** real en un motor de videojuegos.

Este ejercicio conecta directamente con la unidad de **Análisis de motores de juegos**, porque me ayuda a ver “a mano” cómo funciona internamente la lógica básica que luego encontramos ya empaquetada en motores como Unity, Unreal o Godot.

---

En el código he definido la clase `Particula` siguiendo las restricciones del enunciado (sin librerías externas, solo HTML + JS visto en clase):

```js
class Particula{
  constructor(x,y,v,a){
    this.x = x;
    this.y = y;
    this.v = v;
    this.a = a;
  } 
  dibuja(){
    contexto.fillStyle = "#ae2e33"
    contexto.fillRect(this.x,this.y,1,1)
  }
  mueve(){
    this.x += Math.cos(this.a)*this.v
    this.y += Math.sin(this.a)*this.v
  }
}
```

- El **constructor** recibe:
  - `x`, `y`: posición inicial de la partícula (el punto donde hago clic).
  - `v`: velocidad, leída del `input range` de velocidad.
  - `a`: ángulo, calculado a partir del slider `angulo` y modificado con la `amplitud` para repartir las partículas.

- El método `dibuja()`:
  - Usa el contexto 2D del canvas (`contexto`) para pintar un píxel (1x1) en el color `#ae2e33`.
  - Esto simula cada partícula como un punto rojo.

- El método `mueve()`:
  - Actualiza la posición de la partícula con trigonometría simple:
    - `x += cos(a) * v`
    - `y += sin(a) * v`
  - De esta forma, la dirección viene dada por el ángulo `a` y la velocidad `v`, como en un sistema de partículas real.

En el resto del código:

- Se inicializan las variables globales (`lienzo`, `contexto`, `particulas`, `numeroparticulas`, sliders, etc.).
- En `inicio()` se registra el evento `onclick` sobre el canvas:
  - Cada clic crea 50 partículas nuevas en la posición del ratón con:
    ```js
    new Particula(
      event.offsetX,
      event.offsetY,
      parseFloat(velocidad.value),
      parseFloat(angulo.value)+(Math.random()-0.5)*parseFloat(amplitud.value)
    )
    ```
- En `bucle()`:
  - Se dibuja un rectángulo blanco semitransparente (`rgba(255,255,255,0.4)`) para crear efecto de “estela”.
  - Se mueve y dibuja cada partícula.
  - Se eliminan las partículas que salen fuera del canvas.
  - Se relanza el bucle con `setTimeout("bucle()",10)`.

Todo esto respeta las estructuras vistas en clase: `canvas`, eventos de ratón, arrays, bucles y `setTimeout`.

---

```html
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <style>
      #lienzo{
        border: 2px solid #932324;
      }
    </style>
  </head>
  <body>
    <input type="range" id="angulo" min="0" max="6.283185307" step="0.01" value="0">
    <label>Ángulo</label>
    <br>
    <input type="range" id="velocidad" min="0" max="10" step="0.1" value="2">
    <label>Velocidad</label>
    <br>
    <input type="range" id="amplitud" min="0" max="2" step="0.01" value="1">
    <label>Amplitud</label>
    <br>
    <canvas id="lienzo" width="512" height="512"></canvas>
    <script>
      class Particula{
        constructor(x,y,v,a){
          this.x = x;
          this.y = y;
          this.v = v;
          this.a = a;
        } 
        dibuja(){
          contexto.fillStyle = "#ae2e33"
          contexto.fillRect(this.x,this.y,1,1)
        }
        mueve(){
          this.x += Math.cos(this.a)*this.v
          this.y += Math.sin(this.a)*this.v
        }
      }
      
      // Variables globales
      var lienzo = document.querySelector("canvas")
      var contexto = lienzo.getContext("2d")
      var temporizador;
      var numeroparticulas = 50
      var particulas = []
      var blancotransparente = "rgba(255,255,255,0.4)";
      var angulo = document.querySelector("#angulo")
      var velocidad = document.querySelector("#velocidad")
      var amplitud = document.querySelector("#amplitud")
      
      inicio();
      
      function inicio(){
        lienzo.onclick = function(event){
          for(let i = 0;i<numeroparticulas;i++){
            particulas.push(
              new Particula(
                event.offsetX,
                event.offsetY,
                parseFloat(velocidad.value),
                parseFloat(angulo.value)+(Math.random()-0.5)*parseFloat(amplitud.value)
              )
            )
          }
        }
        temporizador = setTimeout("bucle()",1000)
      }
      
      function bucle(){
        contexto.fillStyle = blancotransparente
        contexto.fillRect(0,0,512,512)
        particulas.forEach(function(particula){
          particula.mueve()
          particula.dibuja()
        })
        // Eliminamos particulas
        for(let i = 0;i<particulas.length;i++){
          if(
            particulas[i].x < 0 || 
            particulas[i].x > 512 ||
            particulas[i].y < 0 || 
            particulas[i].y > 512 
            ){
              particulas.splice(i,1)
            }
        }
        clearTimeout(temporizador)
        temporizador = setTimeout("bucle()",10)
      }
    </script>
  </body>
</html>
```

He probado el sistema interactuando con los **tres controles deslizantes**:

- **Ángulo (`#angulo`)**:
  - Cambia la dirección principal en la que salen las partículas.
  - Por ejemplo:
    - Valor cercano a `0` → partículas hacia la derecha.
    - Valor cercano a `1.57` (π/2) → partículas hacia abajo.
    - Valor cercano a `3.14` (π) → partículas hacia la izquierda.

- **Velocidad (`#velocidad`)**:
  - Controla lo rápido que se desplazan las partículas.
  - Si pongo velocidad baja (por ejemplo `1`), el efecto es suave.
  - Si subo a valores altos (`8`-`10`), las partículas salen disparadas mucho más lejos.

- **Amplitud (`#amplitud`)**:
  - Afecta a la dispersión del ángulo:
    - Valores pequeños → haz de partículas concentrado.
    - Valores mayores → las partículas se abren en forma de cono más ancho.
  - Esto se consigue con:
    ```js
    parseFloat(angulo.value) + (Math.random()-0.5)*parseFloat(amplitud.value)
    ```
    que introduce una variación aleatoria alrededor del ángulo principal.

**Ejemplo de uso práctico:**

1. Selecciono un ángulo hacia arriba.
2. Aumento la velocidad.
3. Subo la amplitud.
4. Hago clic varias veces en la parte inferior del canvas.

El resultado se parece a un **emisor de chispas o partículas** saliendo desde el punto de impacto hacia una dirección, como en muchos videojuegos cuando hay explosiones, hechizos o efectos de energía.

---

Este ejercicio me ha ayudado a entender, de forma sencilla, cómo funcionan los **emisores de partículas** que luego vemos en los motores de juegos profesionales:

- Cada partícula es un objeto con sus propios datos (posición, velocidad, ángulo).
- Un “emisor” es simplemente un punto donde generamos muchas partículas con pequeñas variaciones.
- El bucle de animación se encarga de actualizar, dibujar y limpiar las partículas.

Trabajando solo con **HTML, Canvas y JavaScript básico**, he replicado la lógica que está detrás de muchos efectos visuales en videojuegos.  
Esto me prepara para reconocer estos mismos parámetros (ángulo, velocidad, dispersión, vida útil) cuando los configure en motores como Unity o Godot, entendiendo qué ocurre “por debajo”.

En resumen, este proyecto conecta directamente con la unidad de **motores de juegos y creación de efectos visuales**, y demuestra cómo un sistema simple de partículas puede convertirse en la base de un **emisor de juegos** real dentro de un videojuego.
