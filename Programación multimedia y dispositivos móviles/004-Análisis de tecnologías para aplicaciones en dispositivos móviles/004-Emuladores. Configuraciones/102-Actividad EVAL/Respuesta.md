He desarrollado una nueva funcionalidad para TAMEify, la aplicación de reproductor de música que hemos estado trabajando en clase. Esta aplicación permite a los usuarios gestionar y reproducir su música favorita de manera intuitiva.

En este ejercicio, mi objetivo ha sido crear una pantalla de favoritos que permita a los usuarios acceder rápidamente a sus artistas preferidos. Esta pantalla se integra perfectamente con la estructura existente de TAMEify y mejora significativamente la experiencia de usuario al proporcionar un acceso directo a los artistas que más escuchan.

La pantalla de favoritos cumple con las siguientes funcionalidades:
- Mostrar una lista de artistas favoritos obtenidos desde la API
- Permitir navegar a la lista de canciones de cada artista
- Incluir un botón de retorno para volver a la pantalla principal
- Mantener la coherencia visual con el resto de la aplicación

---

He implementado la pantalla de favoritos siguiendo las mejores prácticas vistas en clase y manteniendo la estructura del proyecto existente.

### Estructura de archivos creados/modificados:

#### **pantalla_favoritos.php**
He creado un nuevo componente en la carpeta `componentes/` que incluye:

**Estructura HTML:**
```php
<div id="pantalla_favoritos">
  <header>
    <button id="btn_volver">←</button>
    <h2>Favoritos</h2>
  </header>
  <section id="lista_favoritos">
    <!-- Contenido dinámico -->
  </section>
</div>
```

**Estilos CSS integrados:**
- Utilicé CSS embebido dentro del componente para mantener la modularidad
- Implementé un diseño responsivo con `display: grid` para organizar los artistas
- Añadí efectos hover para mejorar la interactividad
- Los estilos son coherentes con la paleta de colores oscura (#121212, #1a1a1a) de TAMEify

**JavaScript para funcionalidad dinámica:**
```javascript
// Conexión con la API de favoritos
fetch("api/favoritos.json")
.then(function(respuesta){return respuesta.json()})
.then(function(datos){
  datos.favorites.forEach(function(dato){
    // Clonación de plantilla y poblado de datos
    let plantilla = document.querySelector("#elemento_lista")
    let instancia = plantilla.content.cloneNode(true)
    let articulo = instancia.querySelector("article")
    articulo.querySelector("p").textContent = dato.artist
    articulo.querySelector("img").setAttribute("src",dato.image)
    contenedor_favoritos.appendChild(instancia)
    
    // Navegación a pantalla de lista
    articulo.onclick = function(){
      document.querySelector("#pantalla_favoritos").style.display = "none"
      document.querySelector("#pantalla_lista").style.display = "block"
    }
  })
})
```

#### **Modificaciones en index.php**
He añadido la inclusión del nuevo componente:
```php
<?php include "componentes/pantalla_favoritos.php";?>
```

#### **Modificaciones en pantalla_inicio.php**
He añadido un botón en el header para acceder a la pantalla de favoritos:
```php
<button id="btn_favoritos">❤️ Favoritos</button>
```

Y su funcionalidad JavaScript:
```javascript
document.querySelector("#btn_favoritos").onclick = function(){
  document.querySelector("#pantalla_inicio").style.display = "none"
  document.querySelector("#pantalla_favoritos").style.display = "block"
}
```

### Buenas prácticas aplicadas:
- **Código limpio y legible:** He utilizado nombres de variables descriptivos como `contenedor_favoritos`, `btn_volver`, etc.
- **Reutilización de plantillas:** Aproveché la plantilla `#elemento_lista` existente para mantener consistencia
- **Separación de responsabilidades:** Cada archivo tiene su propósito específico (estructura, estilos, comportamiento)
- **Manejo de errores en imágenes:** Implementé el atributo `onerror` para mostrar un placeholder si la imagen no carga

---

La pantalla de favoritos funciona de la siguiente manera:

### Flujo de navegación implementado:

1. **Acceso desde pantalla principal:**
   - El usuario hace clic en el botón "❤️ Favoritos" del header
   - La aplicación oculta `#pantalla_inicio` y muestra `#pantalla_favoritos`

2. **Carga dinámica de datos:**
   - Al cargar la pantalla, se realiza una petición `fetch` a `api/favoritos.json`
   - La API devuelve un objeto JSON con un array `favorites` que contiene artistas con sus imágenes

3. **Renderizado de artistas:**
   - Para cada artista en el array, clono la plantilla HTML
   - Reemplazo el texto del párrafo con el nombre del artista
   - Establezco la imagen usando `setAttribute("src", dato.image)`
   - Añado el elemento al contenedor `#lista_favoritos`

4. **Interacción del usuario:**
   - Al hacer clic en un artista, se navega a `#pantalla_lista` para ver sus canciones
   - El botón "←" permite volver a la pantalla de inicio

### Ejemplo de datos de la API (api/favoritos.json):
```json
{
  "favorites": [
    {
      "artist": "Daft Punk",
      "image": "https://example.com/images/daft_punk.jpg"
    },
    {
      "artist": "Coldplay",
      "image": "https://example.com/images/coldplay.jpg"
    }
  ]
}
```

### Resultado visual:
La pantalla muestra una cuadrícula vertical con tarjetas de artistas que incluyen:
- Imagen del artista (80x80px, redondeada)
- Nombre del artista en negrita
- Fondo oscuro (#1a1a1a) que cambia a #282828 al pasar el ratón
- Transiciones suaves para mejorar la experiencia de usuario

---

La implementación de la pantalla de favoritos ha sido una excelente práctica para consolidar los conceptos vistos en esta unidad sobre tecnologías para aplicaciones en dispositivos móviles.

### Conceptos aplicados de la unidad:

1. **PHP para estructura modular:** He utilizado `include` para crear componentes reutilizables, lo que facilita el mantenimiento del código.

2. **HTML semántico:** He empleado etiquetas apropiadas como `<header>`, `<section>`, `<article>` para estructurar el contenido de manera significativa.

3. **CSS responsivo:** He implementado layouts flexibles con Grid CSS que se adaptan correctamente a diferentes tamaños de pantalla.

4. **JavaScript asíncrono:** He trabajado con Promises mediante `fetch()` y `.then()` para obtener datos de la API sin bloquear la interfaz.

5. **Manipulación del DOM:** He clonado plantillas HTML y modificado dinámicamente el contenido usando métodos como `querySelector`, `cloneNode`, `appendChild`, etc.

6. **Gestión de eventos:** He implementado manejadores `onclick` para la navegación entre pantallas.

### Contribución a la experiencia del usuario:

Esta pantalla de favoritos mejora significativamente TAMEify porque:
- Reduce el tiempo de acceso a los artistas más escuchados
- Proporciona una navegación intuitiva y familiar (similar a Spotify)
- Mantiene la coherencia visual con el resto de la aplicación
- Ofrece feedback visual inmediato mediante efectos hover

### Reflexión personal:

Este ejercicio me ha permitido comprender mejor cómo se estructura una aplicación web moderna de una sola página (SPA) sin necesidad de frameworks complejos. He aprendido a gestionar la navegación entre vistas mediante manipulación del DOM y a trabajar con datos dinámicos de APIs.

La experiencia de crear una funcionalidad completa desde cero, integrándola con código existente, me ha dado confianza para afrontar proyectos más complejos en el futuro y entender mejor cómo funcionan las aplicaciones que usamos diariamente en nuestros dispositivos móviles.
