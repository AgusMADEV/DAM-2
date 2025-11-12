En esta actividad he trabajado la creación de un personaje que se mueve sobre una rejilla isométrica usando **HTML5 Canvas y JavaScript**, aplicando conceptos vistos en clase de programación multimedia y motores de juegos 2D.

El objetivo principal es entender cómo transformar coordenadas lógicas (x, y) a una representación **isométrica**, y cómo conectar esa lógica con la interacción del usuario mediante el teclado. Este tipo de vista y control es muy común en RPGs, juegos de estrategia y simuladores, por lo que el ejercicio se relaciona directamente con la creación de interfaces y mundos jugables similares a los que se usan en motores de juegos reales.

---

En mi solución he seguido los pasos del enunciado utilizando únicamente estructuras vistas en clase:

#### a) Clase `Personaje`

He creado la clase `Personaje` con sus propiedades y métodos básicos:

```js
class Personaje{
  constructor(){
    this.x = 10;
    this.y = 10;
    this.puntos = 0;
  }
  dibuja(){
    let puntoiso = iso(this.x, this.y)
    contexto.beginPath()
    contexto.arc(puntoiso.x, puntoiso.y, 5, 0, Math.PI * 2)
    contexto.fillStyle = "red"
    contexto.fill()
  }
}
```

- `x` e `y` representan la posición del personaje en la **rejilla lógica**.
- `dibuja()` se encarga de pintar al personaje en el canvas usando la proyección isométrica.

#### b) Función de proyección isométrica `iso(i, j)`

Para convertir coordenadas de la rejilla a coordenadas isométricas he definido:

```js
function iso(i, j){
  return {
    x: 512 + (i - j) * paso,
    y: 512 + (i + j) * (paso / 2)
  }
}
```

- Uso `paso` como tamaño de celda.
- Centro la rejilla en `(512, 512)` para aprovechar todo el lienzo.
- La fórmula `(i - j, (i + j)/2)` es la base de la proyección isométrica vista en clase.

#### c) Dibujo de la rejilla

He creado `dibujoRejilla()` para mostrar visualmente la rejilla isométrica:

```js
function dibujoRejilla(){
  contexto.fillStyle = "#fff"
  contexto.fillRect(0, 0, 1024, 1024)
  contexto.strokeStyle = "#d0d0d0"

  for (let i = -60; i <= 60; i++) {
    const a = iso(i, -60);
    const b = iso(i,  60);
    contexto.beginPath();
    contexto.moveTo(a.x, a.y);
    contexto.lineTo(b.x, b.y);
    contexto.stroke();
  }

  for (let j = -60; j <= 60; j++) {
    const a = iso(-60, j);
    const b = iso( 60, j);
    contexto.beginPath();
    contexto.moveTo(a.x, a.y);
    contexto.lineTo(b.x, b.y);
    contexto.stroke();
  }
}
```

Esto ayuda a visualizar claramente por dónde se mueve el personaje.

#### d) Captura del teclado y movimiento

El movimiento del personaje lo controlo con las teclas **W, A, S, D**, modificando las coordenadas lógicas:

```js
document.onkeydown = function(event){
  let nuevoX = Personaje1.x;
  let nuevoY = Personaje1.y;
  
  switch(event.key){
    case "w":
    case "W":
      nuevoX--;
      break;
    case "s":
    case "S":
      nuevoX++;
      break;
    case "a":
    case "A":
      nuevoY++;
      break;
    case "d":
    case "D":
      nuevoY--;
      break;
  }

  if(nuevoX >= -60 && nuevoX <= 60){
    Personaje1.x = nuevoX;
  }
  if(nuevoY >= -60 && nuevoY <= 60){
    Personaje1.y = nuevoY;
  }

  // actualización de recogidas, texto y redibujado…
}
```

La lógica respeta los límites de la rejilla y después redibuja:
- la rejilla,
- los objetos recogibles,
- y el personaje en su nueva posición.

Todo el desarrollo se ha hecho sin librerías externas, usando solo canvas, clases, funciones y eventos de teclado.

---

```html
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Personaje Isométrico - Solución Completa</title>
    <style>
      body {
        margin: 0;
        padding: 20px;
        font-family: Arial, sans-serif;
        background-color: #f0f0f0;
      }
      #lienzo {
        border: 2px solid #333;
        background-color: white;
        display: block;
        margin: 0 auto;
      }
      .instrucciones {
        max-width: 1024px;
        margin: 10px auto;
        padding: 8px 12px;
        background-color: white;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
      }
      h2 {
        margin: 0 0 5px 0;
        color: #333;
        font-size: 16px;
      }
      .instrucciones p {
        margin: 5px 0;
        font-size: 13px;
      }
      .teclas {
        display: inline-block;
        padding: 3px 8px;
        margin: 1px;
        background-color: #4CAF50;
        color: white;
        border-radius: 3px;
        font-weight: bold;
        font-size: 12px;
      }
      .info {
        text-align: center;
        margin: 5px auto;
        max-width: 1024px;
        padding: 5px;
        background-color: #e8f5e9;
        border-radius: 5px;
        font-size: 13px;
      }
    </style>
  </head>
  <body>
    <div class="instrucciones">
      <h2>🎮 Control del Personaje</h2>
      <p>Usa las teclas para mover al personaje por la rejilla isométrica:</p>
      <p>
        <span class="teclas">W</span> Arriba | 
        <span class="teclas">A</span> Izquierda | 
        <span class="teclas">S</span> Abajo | 
        <span class="teclas">D</span> Derecha
      </p>
    </div>

    <div class="info" id="posicion">
      Posición: (10, 10)
    </div>

    <canvas id="lienzo"></canvas>

    <script>
      var lienzo = document.querySelector("#lienzo")
      var contexto = lienzo.getContext("2d")
      lienzo.width = 1024
      lienzo.height = 1024
      
      var paso = 20  // Tamaño de cada celda de la rejilla
      
      function iso(i, j){
        return {
          x: 512 + (i - j) * paso,
          y: 512 + (i + j) * (paso / 2)
        }
      }
      
      function dibujoRejilla(){
        // Limpio fondo
        contexto.fillStyle = "#fff"
        contexto.fillRect(0, 0, 1024, 1024)
        contexto.strokeStyle = "#d0d0d0"

        // Líneas paralelas al eje U (j variable, i constante)
        for (let i = -60; i <= 60; i++) {
          const a = iso(i, -60);
          const b = iso(i,  60);
          contexto.beginPath();
          contexto.moveTo(a.x, a.y);
          contexto.lineTo(b.x, b.y);
          contexto.stroke();
        }

        // Líneas paralelas al eje V (i variable, j constante)
        for (let j = -60; j <= 60; j++) {
          const a = iso(-60, j);
          const b = iso( 60, j);
          contexto.beginPath();
          contexto.moveTo(a.x, a.y);
          contexto.lineTo(b.x, b.y);
          contexto.stroke();
        }
      }
      
      class Recogible{
        constructor(){
          this.x = Math.round((Math.random() * 120) - 60); // [-60, 60]
          this.y = Math.round((Math.random() * 120) - 60); // [-60, 60]
        }
        dibuja(){
          let puntoiso = iso(this.x, this.y)
          contexto.beginPath();
          contexto.arc(puntoiso.x, puntoiso.y, 8, 0, Math.PI * 2)
          contexto.fillStyle = "green"
          contexto.fill()
        }
      }
      
      function distancia(x1, y1, x2, y2) {
        const dx = x2 - x1;
        const dy = y2 - y1;
        return Math.sqrt(dx * dx + dy * dy);
      }
      
      class Personaje{
        constructor(){
          this.x = 10;
          this.y = 10;
          this.puntos = 0;
        }
        dibuja(){
          let puntoiso = iso(this.x, this.y)
          contexto.beginPath()
          contexto.arc(puntoiso.x, puntoiso.y, 5, 0, Math.PI * 2)
          contexto.fillStyle = "red"
          contexto.fill()
        }
      }
      
      var Personaje1 = new Personaje();
      var recogibles = []
      var numeroRecogibles = 20;
      for(let i = 0; i < numeroRecogibles; i++){
        recogibles.push(new Recogible())
      }

      document.onkeydown = function(event){
        // Guardamos la posición anterior para validar
        let nuevoX = Personaje1.x;
        let nuevoY = Personaje1.y;
        
        switch(event.key){
          case "w":
          case "W":
            nuevoX--;
            break;
          case "s":
          case "S":
            nuevoX++;
            break;
          case "a":
          case "A":
            nuevoY++;
            break;
          case "d":
          case "D":
            nuevoY--;
            break;
        }
        
        // PASO 8: RESTRICCIONES - Validar límites
        if(nuevoX >= -60 && nuevoX <= 60){
          Personaje1.x = nuevoX;
        }
        if(nuevoY >= -60 && nuevoY <= 60){
          Personaje1.y = nuevoY;
        }
        
        // DESAFÍO: Detectar colisiones con recogibles
        for(let i = recogibles.length - 1; i >= 0; i--){
          if(distancia(Personaje1.x, Personaje1.y, recogibles[i].x, recogibles[i].y) < 2){
            recogibles.splice(i, 1)
            Personaje1.puntos++
          }
        }
        
        // Actualizar visualización de posición y puntos
        document.getElementById("posicion").textContent = 
          "Posición: (" + Personaje1.x + ", " + Personaje1.y + ") | Objetos recogidos: " + Personaje1.puntos + "/" + numeroRecogibles;
        
        // Redibujar todo
        dibujoRejilla()
        
        // Dibujar recogibles
        for(let i = 0; i < recogibles.length; i++){
          recogibles[i].dibuja()
        }
        
        Personaje1.dibuja()
      }

      dibujoRejilla()
      
      // Dibujar recogibles iniciales
      for(let i = 0; i < recogibles.length; i++){
        recogibles[i].dibuja()
      }
      
      Personaje1.dibuja()
      
      // Actualizar contador inicial
      document.getElementById("posicion").textContent = 
        "Posición: (" + Personaje1.x + ", " + Personaje1.y + ") | Objetos recogidos: 0/" + numeroRecogibles;
      
    </script>
  </body>
</html>
```

En la práctica, el flujo del juego queda así:

1. **Inicialización:**
   - Se dibuja la rejilla isométrica.
   - Se crean `numeroRecogibles = 20` objetos de la clase `Recogible`, colocados en posiciones aleatorias de la rejilla.
   - Se instancia `Personaje1` en la posición inicial `(10, 10)`.

2. **Movimiento del personaje:**
   - Al pulsar:
     - `W` → el personaje se desplaza hacia una dirección isométrica (ajustando `x`).
     - `S` → mueve en la dirección contraria.
     - `A` / `D` → desplazan en el otro eje isométrico.
   - Cada vez que se pulsa una tecla:
     - Se valida la nueva posición.
     - Se vuelve a dibujar todo el escenario en el lienzo.
     - Se actualiza el texto:
       ```js
       "Posición: (" + Personaje1.x + ", " + Personaje1.y + ") | Objetos recogidos: " + Personaje1.puntos + "/" + numeroRecogibles;
       ```

3. **Sistema de recogida de objetos:**
   - Uso la función `distancia` para comprobar si el personaje está lo suficientemente cerca de un recogible:
     ```js
     if(distancia(Personaje1.x, Personaje1.y, recogibles[i].x, recogibles[i].y) < 2){
       recogibles.splice(i, 1)
       Personaje1.puntos++
     }
     ```
   - Cuando pasa por encima (en coordenadas de rejilla), el objeto desaparece y se suma un punto.
   - Esto simula una mecánica típica de **coleccionables** en juegos isométricos.

Este ejemplo deja claro cómo:
- las coordenadas lógicas controlan la jugabilidad,
- la proyección isométrica controla la representación visual,
- y el teclado maneja la interacción del jugador.

---

Este ejercicio me ha ayudado a entender mejor cómo funcionan las **rejillas isométricas**, el manejo de coordenadas y la relación entre lógica de juego e interfaz visual, algo básico en el diseño de motores y juegos 2D/2.5D.

A partir de esta base puedo:
- ampliar el sistema con animaciones,
- añadir colisiones más complejas,
- crear mapas con distintos tipos de tiles,
- o integrar este personaje en un motor más grande.

En resumen, este proyecto encaja perfectamente con la unidad sobre análisis de motores de juegos y me ha servido para practicar una mecánica realista y reutilizable para futuros juegos isométricos que desarrolle.
