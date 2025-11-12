En el mundo de los videojuegos modernos, los sistemas de partículas son fundamentales para crear efectos visuales impresionantes como explosiones, fuego, humo, chispas o estelas mágicas. Este ejercicio me ha permitido comprender cómo funcionan estos sistemas desde sus fundamentos, implementando un motor básico de partículas donde puedo controlar parámetros clave como el ángulo de emisión, la velocidad de las partículas y su amplitud de dispersión.

Al trabajar con este sistema, he podido experimentar de primera mano cómo pequeños cambios en estos parámetros pueden generar efectos visuales completamente diferentes, desde un chorro concentrado hasta una explosión dispersa en múltiples direcciones.

---

Esta actividad implementa un sistema simple de partículas controlado por tres parámetros ajustables mediante controles deslizantes.

## Estructura del código

### 1. Clase Particula

```javascript
class Particula{
  constructor(x,y,v,a){
    this.x = x;
    this.y = y;
    this.v = v;
    this.a = a;
  } 
  dibuja(){
    contexto.fillStyle = "black"
    contexto.fillRect(this.x,this.y,1,1)
  }
  mueve(){
    this.x += Math.cos(this.a)*this.v
    this.y += Math.sin(this.a)*this.v
  }
}
```

La clase `Particula` contiene:
- **Propiedades**: posición (x, y), velocidad (v) y ángulo (a)
- **Método dibuja()**: dibuja la partícula como un píxel negro en el lienzo
- **Método mueve()**: actualiza la posición usando trigonometría (coseno y seno del ángulo multiplicado por la velocidad)

### 2. Controles deslizantes

```html
<input type="range" id="angulo" min="0" max="6.283185307" step="0.01" value="0">
<input type="range" id="velocidad" min="0" max="10" step="0.1" value="2">
<input type="range" id="amplitud" min="0" max="2" step="0.01" value="1">
```

- **Ángulo**: de 0 a 2π (6.283185307 radianes, equivalente a 360°)
- **Velocidad**: de 0 a 10 píxeles por frame
- **Amplitud**: de 0 a 2 radianes, controla la dispersión de las partículas

### 3. Interacción

Al hacer clic en el lienzo, se crean 50 partículas en la posición del cursor. Cada partícula usa:
- Los valores actuales de los controles deslizantes
- El ángulo base más un valor aleatorio dentro de la amplitud especificada

### 4. Bucle principal

El bucle de animación:
1. Limpia el lienzo con un blanco semi-transparente (efecto de estela)
2. Mueve todas las partículas
3. Dibuja todas las partículas
4. Elimina las partículas que salen de la pantalla
5. Se ejecuta cada 10 milisegundos

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

Al probar el ejercicio, he observado diferentes comportamientos según los valores de los controles:

### Ejemplos de configuración:

**Efecto de chorro concentrado:**
- Ángulo: 0 radianes (dirección horizontal derecha)
- Velocidad: 5
- Amplitud: 0.2
- Resultado: Las partículas se emiten en una dirección muy precisa, creando un efecto similar a un láser o chorro de agua.

**Efecto de explosión:**
- Ángulo: cualquier valor
- Velocidad: 3-4
- Amplitud: 2
- Resultado: Las partículas se dispersan en todas direcciones desde el punto de clic, simulando una explosión.

**Efecto de fuente:**
- Ángulo: 4.71 radianes (270°, hacia arriba)
- Velocidad: 6
- Amplitud: 0.5
- Resultado: Las partículas se lanzan hacia arriba con cierta dispersión, como una fuente de agua.

**Efecto de emisión lenta:**
- Ángulo: cualquier valor
- Velocidad: 1
- Amplitud: 1
- Resultado: Las partículas se mueven lentamente, creando un efecto más suave y orgánico.

He comprobado que el sistema funciona correctamente eliminando las partículas que salen del lienzo, lo que evita problemas de rendimiento al mantener el array de partículas en un tamaño manejable.

---

Este ejercicio me ha permitido comprender los principios fundamentales de los sistemas de partículas que se utilizan en los motores de juegos profesionales. Aunque nuestro sistema es básico, los conceptos son los mismos que utilizan motores como Unity, Unreal Engine o Godot en sus particle systems.

**Aplicaciones prácticas en videojuegos:**
- **Efectos de impacto:** Al disparar o golpear, se pueden crear partículas en el punto de impacto
- **Efectos ambientales:** Lluvia, nieve, polvo o chispas pueden simularse con emisores continuos
- **Feedback visual:** Las partículas ayudan a comunicar al jugador que algo ha sucedido (daño, recolección de objetos, etc.)
- **Efectos mágicos:** Hechizos, auras o poderes especiales pueden representarse con diferentes configuraciones de partículas

La optimización también es crucial: he implementado la eliminación de partículas fuera de pantalla, una técnica esencial en el desarrollo de juegos para mantener el rendimiento. En motores profesionales, además se utilizan técnicas como object pooling para reutilizar partículas en lugar de crear y destruir constantemente.

Este ejercicio me ha dado las bases para entender cómo funcionan los emisores de partículas en los motores de juegos actuales y cómo puedo crear mis propios efectos visuales personalizados en futuros proyectos.
