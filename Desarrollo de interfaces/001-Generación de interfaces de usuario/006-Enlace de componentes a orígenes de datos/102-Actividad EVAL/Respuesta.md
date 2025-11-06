La idea de este ejercicio es bastante sencilla: como me gusta mucho viajar y el fútbol, quería tener una forma de mostrar en una página web los equipos que he ido conociendo en mis viajes. Para eso pensé que lo más práctico era usar una tabla HTML, porque me permite organizar la información de manera clara: cada fila es un equipo y cada columna muestra un dato (el nombre, la ciudad, el país…).

De esta manera no tengo que escribir la tabla a mano en el HTML, sino que puedo vincularla a un origen de datos, en este caso un array en formato JSON, y que sea el propio código quien construya la tabla automáticamente. Así, si mañana quiero añadir otro equipo, no tengo que tocar la estructura de la tabla, solo sumo un objeto más en el array.

Lo primero que he hecho ha sido definir mis datos en un array con objetos, que tienen formato JSON. Cada objeto representa un equipo y dentro pongo sus claves: id, nombre, ciudad y país.

```
equipos = [
        {
          "id": 1,
          "nombre": "Real Madrid",
          "ciudad": "Madrid",
          "pais": "España"
        },
        {
          "id": 2,
          "nombre": "AC Milan",
          "ciudad": "Milán",
          "pais": "Italia"
        },
        {
          "id": 3,
          "nombre": "Bayern Múnich",
          "ciudad": "Múnich",
          "pais": "Alemania"
        },
        {
          "id": 4,
          "nombre": "Liverpool",
          "ciudad": "Liverpool",
          "pais": "Inglaterra"
        },
        {
          "id": 5,
          "nombre": "Ajax",
          "ciudad": "Ámsterdam",
          "pais": "Países Bajos"
        }
      ]
```

Después, con JavaScript, he seleccionado la tabla y le he metido tanto los encabezados como las filas de manera dinámica.

```
let tabla = document.querySelector("table")
let primerelemento = equipos[0]
let claves = Object.keys(primerelemento)
```

Para los encabezados lo que he cogido son las claves del primer objeto y las he convertido en `''<th>''`. 

```
cadena = "<tr>";
claves.forEach(function(clave){
    cadena += "<th>"+clave+"</th>";
})
cadena += "</tr>";
```

Luego, con un bucle for, recorro todos los equipos y genero las filas con sus datos en `''<td>''`. 

```
equipos.forEach(function(equipo){
    cadena += "<tr>";
    for(let clave in equipo){
        cadena += "<td>"+equipo[clave]+"</td>"
    }
        cadena += "</tr>";
})
```

Al final todo ese HTML lo meto en la tabla usando innerHTML.

```
tabla.innerHTML = cadena;
```

AL cargar la página, gracias a los estilos CSS, he conseguido que la tabla se vea de esta forma, y  como se puede apreciar aparece completa con todos los equipos. 

![Tabla de equipos](https://github.com/AgusMADEV/DAM-2/raw/main/Desarrollo%20de%20interfaces/001-Generaci%C3%B3n%20de%20interfaces%20de%20usuario/006-Enlace%20de%20componentes%20a%20or%C3%ADgenes%20de%20datos/102-Actividad%20EVAL/tabla.png)


Para mostrar este concepto de una forma consistente, aquí presento el ejercicio completo, en el que podemos enlazar un componente HTML (tabla) a un origen de datos, en este caso JSON. En este ejemplo se puede ver como muestro la información de los equipos de fútbol que he visitado en mis viajes.

```
<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8">
    <title>Equipos | Viajes</title>
    <style>
      /* Estilo simple con toque glass */
      body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: linear-gradient(135deg, #dbeafe, #e5e7eb);
      min-height: 100vh;
      display: grid;
      place-items: center;
      padding: 24px;
      }
      .panel {
      width: min(880px, 100%);
      background: rgba(255,255,255,0.35);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      border: 1px solid rgba(255,255,255,0.5);
      border-radius: 16px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.08);
      padding: 16px;
      }
      h1 {
      margin: 0 0 12px;
      font-size: 1.25rem;
      text-align: center;
      }
      table {
      width: 100%;
      border-collapse: collapse;
      overflow: hidden;
      border-radius: 12px;
      }
      th, td { padding: 12px 14px; text-align: left; }
      th {
      background: rgba(255,255,255,0.5);
      border-bottom: 1px solid rgba(0,0,0,0.06);
      }
      tr:nth-child(odd) td { background: rgba(255,255,255,0.35); }
      tr:nth-child(even) td { background: rgba(255,255,255,0.25); }
      tr:hover td { background: rgba(255,255,255,0.6); }
    </style>
  </head>
  <body>
    <table></table>
    <script>
        equipos = [
        {
          "id": 1,
          "nombre": "Real Madrid",
          "ciudad": "Madrid",
          "pais": "España"
        },
        {
          "id": 2,
          "nombre": "AC Milan",
          "ciudad": "Milán",
          "pais": "Italia"
        },
        {
          "id": 3,
          "nombre": "Bayern Múnich",
          "ciudad": "Múnich",
          "pais": "Alemania"
        },
        {
          "id": 4,
          "nombre": "Liverpool",
          "ciudad": "Liverpool",
          "pais": "Inglaterra"
        },
        {
          "id": 5,
          "nombre": "Ajax",
          "ciudad": "Ámsterdam",
          "pais": "Países Bajos"
        }
      ]

      let tabla = document.querySelector("table")
      let primerelemento = equipos[0]
      let claves = Object.keys(primerelemento)

      cadena = "<tr>";
      claves.forEach(function(clave){
        cadena += "<th>"+clave+"</th>";
      })
      cadena += "</tr>";
      equipos.forEach(function(equipo){
        cadena += "<tr>";
        for(let clave in equipo){
          cadena += "<td>"+equipo[clave]+"</td>"
        }
        cadena += "</tr>";
      })
      tabla.innerHTML = cadena;
    </script>
  </body>
</html>
```

Con este ejercicio he aprendido a mostrar en una tabla la información de los equipos de fútbol que voy viendo en mis viajes. Lo bueno es que ya no tengo que escribir la tabla a mano, sino que puedo enlazarla a un origen de datos. Esto me prepara para que en el futuro pueda traer la información desde un JSON externo o una API y así tener mi aplicación actualizada automáticamente con los equipos que vaya visitando.