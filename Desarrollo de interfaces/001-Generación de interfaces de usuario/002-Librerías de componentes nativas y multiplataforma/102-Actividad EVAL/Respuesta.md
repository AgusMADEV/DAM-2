Un formulario en HTML funciona como un contenedor donde podemos meter distintos elementos de entrada. Por ejemplo, yo he puesto un campo de texto y un botón de enviar, y de esa manera se ve claro cómo todo lo que el usuario escriba se agrupa dentro del formulario para luego mandarlo al servidor.

A nivel técnico, el formulario está bien montado porque he usado la etiqueta (`"<form>"`) con sus atributos principales: el action, que indica a qué archivo se van a mandar los datos, y el method, que en este caso es POST. Dentro del formulario he metido un input de texto y un input de tipo submit, y todo está bien anidado, o sea, bien colocado dentro de la etiqueta (`"<form>"`).

```
<form action="quienteprocesa.php" method="POST"> 
      <input type="text">
      <input type="submit">
    </form>
```

El ejemplo es sencillo, pero práctico: un formulario que te deja escribir algo y enviarlo. Esto sirve para entender la base de cómo se recoge información del usuario. A partir de aquí se podría ampliar con más campos, como correo, contraseña, menús desplegables, etc. Pero la idea principal ya se ve en este ejercicio.
Aquí dejo el ejemplo, con un HTML básico:

```
<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8">
    <title>Ejemplo datalist</title>
  </head>
  <body>
    <h1>Componentes de formulario</h1>
    
    <form action="quienteprocesa.php" method="POST"> 
      <input type="text">
      <input type="submit">
    </form>
  </body>
</html>
```

Con este ejercicio se ve que los formularios son fundamentales porque permiten recoger los datos del usuario y enviarlos al servidor. Son la base de cualquier interfaz interactiva, ya que sin ellos no habría manera de procesar esa información dentro de la aplicación.