En estas vacaciones he estado jugando bastante y me animé a crear mi propio mini‑juego en HTML5 Canvas. Para integrar movimiento (tema que veremos en motores 2D/3D), elegí una **roca** que se desplaza y rota suavemente por la pantalla. La idea es practicar **clases**, **bucle de juego** con temporizador y **dibujo vectorial** en el canvas, usando solo lo visto en clase.

---

**Estructura general**
- Defino clases reutilizables (p. ej., `Jugador`, `Roca`), aunque aquí me centro en la roca.
- Encapsulo el comportamiento de la roca en **métodos**: `dibuja()` y `mueve()`.
- Mantengo las **condiciones de inicio** separadas del **bucle principal** `bucle()`.
- No uso librerías externas; solo **Canvas 2D** y **temporizadores**.

**Puntos clave sin errores**
- En `Roca`, calculo una forma poligonal irregular controlando la *rugosidad* con un array de `puntas`.
- El método `dibuja()` abre/cierra la ruta correctamente con `beginPath()`/`closePath()` y aplica `stroke()`.
- El método `mueve()` actualiza **ángulo** y **posición** con pequeñas variaciones, logrando un movimiento orgánico.
- El bucle limpia el lienzo con `clearRect` antes de repintar, evitando “fantasmas”.

---

A continuación explico, con fragmentos del código del proyecto, cómo he resuelto cada paso del enunciado.

## Declaración de variables y clases

**Clases del juego (reutilizables) y la roca:**
```js
class Jugador{
  // (Reservado para futuras mecánicas)
}

class Roca{
  constructor(){
    this.posx = Math.random()*512;
    this.posy = Math.random()*512;
    this.angulo = Math.random()*Math.PI*2;
    this.lados = Math.round(Math.random()*20+5);
    this.radio = Math.random()*20+10;
    const rugosidad = 0.4;
    this.puntas = Array.from({length:this.lados}, () => 1 + (Math.random()*2 - 1) * rugosidad);
  }

  dibuja(){
    contexto.beginPath();
    for(let i = 0; i < this.lados; i++){
      const ang = (i/this.lados)*Math.PI*2 + this.angulo;
      const r   = this.radio * this.puntas[i];
      const x   = this.posx + Math.cos(ang)*r;
      const y   = this.posy + Math.sin(ang)*r;
      if(i===0) contexto.moveTo(x,y); else contexto.lineTo(x,y);
    }
    contexto.closePath();
    contexto.strokeStyle = "#333";
    contexto.stroke();
  }

  mueve(){
    this.angulo += (Math.random()-0.5)*0.1;
    this.posx += Math.cos(this.angulo);
    this.posy += Math.sin(this.angulo);
  }
}
```

## Condiciones de inicio

**Canvas, contexto y creación de rocas:**
```js
const lienzo = document.querySelector("canvas");
const contexto = lienzo.getContext("2d");

var rocas = [];
var numerorocas = 10;
for(let i = 0; i < numerorocas; i++){
  rocas.push(new Roca());
}
```

## Desplazamiento de la roca (bucle y temporizador)

**Bucle principal con temporizador y actualización de estado:**
```js
var temporizador = setTimeout("bucle()", 1000);

function bucle(){
  contexto.clearRect(0,0,512,512);

  rocas.forEach(function(roca){
    roca.dibuja();
    roca.mueve();
  });

  clearTimeout(temporizador);
  temporizador = setTimeout("bucle()", 1000);
}
```
*Qué hace:* cada iteración limpia el lienzo, **dibuja** y **mueve** todas las rocas, y programa la siguiente ejecución con `setTimeout`. (También sería válido pasar la **referencia** `bucle` en lugar del string).

## Dibujo de la roca

El dibujo se realiza con geometría básica (líneas) en torno a un centro, usando **ángulos** y **radio variable** para formar una silueta irregular:
```js
// Dentro de Roca.dibuja()
const ang = (i/this.lados)*Math.PI*2 + this.angulo;
const r   = this.radio * this.puntas[i];
const x   = this.posx + Math.cos(ang)*r;
const y   = this.posy + Math.sin(ang)*r;
```

**Resultado:** en pantalla aparecen varias rocas con **contorno poligonal rugoso** que se desplazan y rotan de forma suave y aleatoria.

---

En este ejercicio he aplicado conceptos base que luego abstraen los motores 2D/3D:
- **Clases** ⇨ en motores serán **componentes** o **entidades** con datos y comportamiento.
- **Bucle con temporizador** ⇨ evoluciona hacia un **game loop** estable (update/render).
- **Dibujo por rutas** ⇨ se convierte en **renderizado de mallas/texturas**.
- **Estado y movimiento** ⇨ se generaliza a **sistemas** (física, input, IA).
```
<!doctype html>
<html>
  <head>
    <style></style>
  </head>
  <body>
    <canvas width=512 height=512></canvas>
    <script>
      // Declarar las clases reutilizable (objetos del juego)
        class Jugador{
        }
        class Roca{
            constructor(){
                this.posx = Math.random()*512;
                this.posy = Math.random()*512;
                this.angulo = Math.random()*Math.PI*2
                this.lados = Math.round(Math.random()*20+5)
                this.radio = Math.random()*20+10
                const rugosidad = 0.4;
                this.puntas = Array.from({length:this.lados}, () => 1 + (Math.random()*2 - 1) * rugosidad);

            }
            dibuja(){
                contexto.beginPath();
                for(let i = 0; i < this.lados; i++){
                const ang = (i/this.lados)*Math.PI*2 + this.angulo;
                const r   = this.radio * this.puntas[i];
                const x   = this.posx + Math.cos(ang)*r;
                const y   = this.posy + Math.sin(ang)*r;
                if(i===0) contexto.moveTo(x,y); else contexto.lineTo(x,y);
                }
                contexto.closePath();
                contexto.strokeStyle = "#333";
                contexto.stroke();
            }
            mueve(){
            this.angulo += (Math.random()-0.5)*0.1
            this.posx += Math.cos(this.angulo)
            this.posy += Math.sin(this.angulo)
            }
      }
      // Condiciones de inicio
      const lienzo = document.querySelector("canvas");
      const contexto = lienzo.getContext("2d");
      var rocas = []
      var numerorocas = 10;
      for(let i = 0;i<numerorocas;i++){
        rocas.push(new Roca())
    }
      // Entramos en el bucle
      var temporizador = setTimeout("bucle()",1000)
      
      function bucle(){
        contexto.clearRect(0,0,512,512)
        rocas.forEach(function(roca){
          roca.dibuja()
          roca.mueve()
        })
        clearTimeout(temporizador)
        temporizador = setTimeout("bucle()",1000)
      }
    </script>
  </body>
</html>
```
Conclusión: he construido un esqueleto de juego simple y legible (clases, bucle, dibujo y movimiento) que puedo reutilizar para otros proyectos web o como base de prácticas en motores de juegos (añadiendo colisiones, input de teclado, o distintas velocidades por roca).
