En esta actividad he desarrollado **TAMEify**, una aplicación web móvil que simula una plataforma de streaming musical. El objetivo principal ha sido aplicar los conceptos fundamentales del desarrollo web moderno orientado a dispositivos móviles, específicamente trabajando con **carga asíncrona de datos**, **manipulación dinámica del DOM** y **gestión de eventos de usuario**.

Este tipo de aplicaciones son esenciales en el contexto actual del desarrollo móvil, donde la mayoría de usuarios acceden a contenidos multimedia desde sus smartphones. La carga dinámica de información desde APIs externas permite crear interfaces fluidas y reactivas sin necesidad de recargar la página completa, mejorando significativamente la experiencia de usuario.

El proyecto se enmarca en el estudio de **tecnologías web para dispositivos móviles**, donde es fundamental comprender cómo las aplicaciones web pueden competir con aplicaciones nativas mediante técnicas de desarrollo progresivo y optimización para pantallas táctiles.

---

###  Carga Asíncrona de Datos

La **Fetch API** es una interfaz moderna de JavaScript que permite realizar peticiones HTTP asíncronas de forma más limpia y eficiente que las antiguas técnicas como XMLHttpRequest. En mi proyecto, he implementado Fetch para cargar los datos de artistas favoritos desde un archivo JSON local:

```javascript
fetch("api/favoritos.json")
  .then(function(respuesta) {
    if (!respuesta.ok) {
      throw new Error('Error al cargar los datos');
    }
    return respuesta.json();
  })
  .then(function(datos) {
    datosFavoritos = datos;
    // Procesar y mostrar datos
  })
  .catch(function(error) {
    console.error("Error al cargar favoritos:", error);
  });
```

**Funcionamiento paso a paso:**

1. **Petición**: `fetch()` realiza una petición HTTP GET al archivo JSON
2. **Primera promesa**: Se verifica si la respuesta es correcta (`respuesta.ok`) y se convierte a JSON con `respuesta.json()`
3. **Segunda promesa**: Se procesan los datos recibidos y se almacenan en la variable global `datosFavoritos`
4. **Manejo de errores**: El `catch()` captura cualquier error de red o parsing

### Manipulación del DOM - Templates y Clonación

Para generar dinámicamente los elementos de la lista de favoritos, he utilizado el elemento **`<template>`**, que permite definir estructuras HTML reutilizables que no se renderizan hasta que se clonan mediante JavaScript:

```javascript
datos.favorites.forEach(function(dato) {
  let plantilla = document.querySelector("#elemento_lista");
  let instancia = plantilla.content.cloneNode(true);
  let articulo = instancia.querySelector("article");
  
  articulo.querySelector("p").textContent = dato.artist;
  articulo.querySelector("img").setAttribute("src", dato.image);
  
  contenedor.appendChild(instancia);
});
```

**Términos técnicos utilizados:**

- **`querySelector()`**: Selecciona el primer elemento que coincide con el selector CSS
- **`cloneNode(true)`**: Crea una copia profunda del nodo, incluyendo todos sus hijos
- **`textContent`**: Propiedad que establece el texto de un elemento de forma segura (evita XSS)
- **`setAttribute()`**: Modifica atributos HTML de forma dinámica
- **`appendChild()`**: Añade el nuevo nodo al DOM visible

### Gestión de Eventos

He implementado eventos `onclick` dinámicos para cada tarjeta de artista, permitiendo la navegación entre pantallas:

```javascript
articulo.onclick = function() {
  console.log("Has hecho click en:", dato.artist);
  mostrarPantallaLista(dato);
};

function mostrarPantallaLista(artista) {
  document.querySelector("#pantalla_inicio").style.display = "none";
  document.querySelector("#pantalla_lista").style.display = "block";
  
  const imgLista = document.querySelector("#pantalla_lista img");
  imgLista.onerror = function() {
    this.onerror = null;
    this.src = 'img/placeholder.png';
  };
  
  imgLista.setAttribute("src", artista.image);
}
```

**Aspectos clave:**
- Los eventos se asignan de forma **dinámica** a cada elemento generado
- Se implementa **closure** para capturar los datos específicos de cada artista
- El evento `onerror` maneja imágenes no disponibles, mejorando la robustez

### Diseño Responsive y Mobile-First

He aplicado CSS Grid y Flexbox para crear un diseño adaptativo:

```css
#favoritas {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 10px;
}

footer {
  display: flex;
  position: fixed;
  bottom: 0px;
  width: 100%;
}
```

El meta tag viewport asegura que la aplicación se renderice correctamente en móviles:

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
```

---

### Código Real Implementado

En mi proyecto TAMEify, la aplicación práctica de estos conceptos se refleja en el siguiente flujo completo:

**Estructura de datos (api/favoritos.json):**
```json
{
  "favorites": [
    {
      "artist": "Daft Punk",
      "image": "https://i.scdn.co/image/ab6761610000e5eb..."
    }
  ]
}
```

**Implementación completa del ciclo de carga y renderizado:**

```javascript
// Variable global para almacenar los datos
let datosFavoritos = null;

// Selección del contenedor
let contenedor = document.querySelector("#favoritas");

// Carga asíncrona
fetch("api/favoritos.json")
  .then(function(respuesta) {
    if (!respuesta.ok) {
      throw new Error('Error al cargar los datos');
    }
    return respuesta.json();
  })
  .then(function(datos) {
    datosFavoritos = datos;
    contenedor.innerHTML = ''; // Limpiar mensaje de carga
    
    // Iteración y renderizado
    datos.favorites.forEach(function(dato) {
      let plantilla = document.querySelector("#elemento_lista");
      let instancia = plantilla.content.cloneNode(true);
      let articulo = instancia.querySelector("article");
      
      // Personalización
      articulo.querySelector("p").textContent = dato.artist;
      articulo.querySelector("img").setAttribute("src", dato.image);
      
      // Evento de navegación
      articulo.onclick = function() {
        mostrarPantallaLista(dato);
      };
      
      contenedor.appendChild(instancia);
    });
  })
  .catch(function(error) {
    console.error("Error:", error);
    contenedor.innerHTML = '<p style="color: red;">Error al cargar favoritos</p>';
  });
```

### Errores Comunes y Soluciones

Durante el desarrollo, he identificado y corregido los siguientes errores típicos:

**Error 1: Handler `onerror` no se ejecuta al cambiar imagen dinámicamente**
```javascript
// ❌ INCORRECTO - El onerror del HTML no se re-ejecuta
imgLista.setAttribute("src", artista.image);

// ✅ CORRECTO - Resetear el handler antes de cambiar la imagen
imgLista.onerror = function() {
  this.onerror = null;
  this.src = 'img/placeholder.png';
};
imgLista.setAttribute("src", artista.image);
```

**Error 2: Olvidar limpiar el mensaje de carga**
```javascript
// ❌ INCORRECTO - Los elementos se añaden pero el mensaje persiste
contenedor.appendChild(instancia);

// ✅ CORRECTO - Limpiar antes de añadir elementos
contenedor.innerHTML = '';
datos.favorites.forEach(function(dato) { ... });
```

**Error 3: Rutas incorrectas en entornos locales**
```javascript
// ❌ INCORRECTO - Ruta absoluta o dependencia externa
fetch("../101-Ejercicios/api/favoritos.json")

// ✅ CORRECTO - Ruta relativa local
fetch("api/favoritos.json")
```

**Error 4: No manejar errores de red**
```javascript
// ❌ INCORRECTO - Sin manejo de errores
fetch("api/favoritos.json")
  .then(respuesta => respuesta.json())
  .then(datos => { ... });

// ✅ CORRECTO - Con validación y catch
fetch("api/favoritos.json")
  .then(function(respuesta) {
    if (!respuesta.ok) throw new Error('Error');
    return respuesta.json();
  })
  .catch(error => console.error(error));
```

### Resultado Visual

La aplicación final presenta:
- **8 tarjetas de artistas** cargadas dinámicamente desde JSON
- **Grid responsive** que se adapta al tamaño de pantalla
- **Navegación fluida** entre pantalla inicial y detalle de artista
- **Manejo robusto de errores** con placeholders para imágenes no disponibles
- **Footer fijo** con navegación persistente
- **Efectos hover** y transiciones suaves para mejorar UX

---

En esta actividad he aplicado con éxito los **tres pilares fundamentales del desarrollo web moderno para dispositivos móviles**:

1. **Fetch API**: Para cargar datos de forma asíncrona sin bloquear la interfaz
2. **Manipulación dinámica del DOM**: Utilizando templates y clonación para generar contenido bajo demanda
3. **Gestión de eventos**: Para crear una aplicación interactiva y reactiva

Estos conceptos se relacionan directamente con otros contenidos vistos en la unidad, como:
- **Promesas y programación asíncrona**: Base del funcionamiento de Fetch
- **Diseño responsive**: CSS Grid y Flexbox para adaptabilidad móvil
- **Accesibilidad y UX**: Manejo de errores, feedback visual y navegación intuitiva
- **APIs REST**: Aunque en este caso uso JSON local, la estructura prepara para consumir APIs reales (Spotify, Deezer, etc.)

El resultado es una **aplicación web funcional y escalable** que demuestra cómo las tecnologías web actuales permiten crear experiencias similares a aplicaciones nativas, con la ventaja de la portabilidad y facilidad de actualización. Este proyecto sienta las bases para desarrollar Progressive Web Apps (PWAs) más complejas en el futuro.

La comprensión de estos patrones es **esencial para cualquier desarrollador de aplicaciones móviles modernas**, ya que cada vez más empresas optan por soluciones híbridas o web que reducen costes de desarrollo y mantenimiento mientras ofrecen experiencias de usuario de alta calidad.
