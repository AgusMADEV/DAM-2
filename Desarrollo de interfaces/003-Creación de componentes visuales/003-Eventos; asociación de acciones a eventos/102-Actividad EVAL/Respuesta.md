Este ejercicio se enmarca dentro del tema de **eventos en JavaScript**, un concepto clave para crear páginas interactivas.  
En este caso, he utilizado el evento `dblclick` (doble clic) para ejecutar una acción concreta: mostrar por consola el progreso en dos áreas personales —**deportes** y **videojuegos**—. Este tipo de eventos permite que el usuario interactúe directamente con la interfaz, generando respuestas inmediatas del programa.

---

El código está estructurado de forma sencilla y cumple correctamente con el objetivo del ejercicio:  
- Se selecciona el elemento `button` mediante `document.querySelector`.  
- Se definen las variables `progresoDeportes` y `progresoVideojuegos`.  
- La función `mostrarProgreso()` imprime en consola el avance de cada una.  
- El evento `ondblclick` se asigna al botón, de modo que al hacer doble clic se ejecuta la función y muestra el resultado.

**Fragmento del código funcional:**
```
<button>Mostrar progreso</button>

<script>
  let boton = document.querySelector("button");

  let progresoDeportes = 60;  
  let progresoVideojuegos = 85;  

  function mostrarProgreso() {
    console.log("Progreso en deportes: " + progresoDeportes + "%");
    console.log("Progreso en videojuegos: " + progresoVideojuegos + "%");
  }

  boton.ondblclick = function() {
    console.log("Se ha hecho doble clic en el botón");
    mostrarProgreso();
  };
</script>
```

---

```
<!doctype html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Progreso</title>
  </head>
  <body>

    <button>Mostrar progreso</button>

    <script>
      let boton = document.querySelector("button");

      let progresoDeportes = 60;  
      let progresoVideojuegos = 85;  

      function mostrarProgreso() {
        console.log("Progreso en deportes: " + progresoDeportes + "%");
        console.log("Progreso en videojuegos: " + progresoVideojuegos + "%");
      }

      boton.ondblclick = function() {
        console.log("Se ha hecho doble clic en el botón");
        mostrarProgreso();
      };
    </script>
  </body>
</html>
```
Cuando el usuario hace **doble clic** sobre el botón, el navegador muestra en la consola:  
```
Se ha hecho doble clic en el botón  
Progreso en deportes: 60%  
Progreso en videojuegos: 85%
```

Este ejemplo demuestra claramente cómo usar el evento `dblclick` para ejecutar funciones personalizadas. La lógica puede ampliarse para mostrar los resultados en pantalla, actualizar barras de progreso o registrar estadísticas de usuario, lo que hace que este tipo de evento sea muy útil en interfaces reales.

---

Este ejercicio me ha servido para entender mejor cómo funcionan los **eventos en JavaScript** y cómo permiten que las páginas web respondan a las acciones del usuario.  
El evento `dblclick` es solo uno de los muchos que se pueden utilizar para **crear interfaces más dinámicas e interactivas**, algo esencial en el desarrollo de aplicaciones web modernas.
