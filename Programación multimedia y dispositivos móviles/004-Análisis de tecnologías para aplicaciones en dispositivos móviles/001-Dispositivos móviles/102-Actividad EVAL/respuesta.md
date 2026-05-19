En esta actividad he desarrollado una interfaz web responsiva para un reproductor de música optimizado para dispositivos móviles. Mi objetivo ha sido aplicar las tecnologías fundamentales del desarrollo web (HTML5, CSS3 y JavaScript) para crear una aplicación multimedia interactiva que simula la experiencia de aplicaciones nativas como Spotify o Apple Music.

He trabajado en el contexto del desarrollo de Progressive Web Apps (PWA) y aplicaciones híbridas para dispositivos móviles, donde la interfaz web se adapta al comportamiento y diseño esperado en smartphones y tablets.

---

### Estructura HTML5

En mi estructura del documento he utilizado elementos semánticos de HTML5:

- **`<meta name="viewport">`**: He configurado el viewport con `width=device-width` y `user-scalable=no` para garantizar una visualización óptima en dispositivos móviles sin permitir zoom no deseado.
- **`<header>`**: Aquí he colocado los botones de navegación entre diferentes secciones del reproductor.
- **`<section id="favoritas">`**: He creado este contenedor para las canciones favoritas del usuario.
- **`<section id="reproductor">`**: He implementado un área fija inferior que muestra el reproductor activo.
- **`<audio>`**: He usado el elemento nativo HTML5 con controles para reproducir archivos de audio.

### Estilos CSS3

**Técnicas de diseño que he implementado:**

- **Reset CSS**: He eliminado los estilos por defecto del navegador con `* { margin: 0; padding: 0; box-sizing: border-box; }`.
- **Flexbox**: Lo he utilizado en `body` para organizar verticalmente los elementos con `flex-direction: column`.
- **CSS Grid**: Lo he implementado en `#favoritas` con `grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))` para crear un layout responsivo que se adapta automáticamente al ancho disponible.
- **Posicionamiento fijo**: En el reproductor he usado `position: fixed` con `bottom: 0` para mantenerlo siempre visible.
- **Gradientes lineales**: He aplicado `linear-gradient(135deg, #d946ef 0%, #a855f7 100%)` para crear efectos visuales modernos.
- **Transiciones**: He añadido `transition: all 0.3s ease` para animaciones suaves en hover y interacciones.
- **Media queries**: He implementado adaptación responsive para pantallas menores a 600px.
- **Custom scrollbar**: He personalizado la barra de desplazamiento con pseudo-elementos `::-webkit-scrollbar`.

### JavaScript para interactividad

He creado la función `reproducirCancion(index)` que implementa la lógica de reproducción:

```javascript
function reproducirCancion(index) {
  const audioPlayer = document.getElementById('audioPlayer');
  const canciones = ['0802.mp3', 'cancion2.mp3', 'cancion3.mp3'];
  audioPlayer.src = canciones[index];
}
```

**Funcionamiento paso a paso:**
1. Obtengo la referencia al elemento `<audio>` mediante `getElementById`.
2. Defino un array con las rutas de los archivos de audio.
3. Actualizo el atributo `src` del reproductor con la canción correspondiente al índice recibido.
4. El navegador carga automáticamente el nuevo archivo.

---

### Código real que he implementado

**Ejemplo de botón interactivo:**
```html
<button onclick="reproducirCancion(0)">J</button>
```

Este botón que he creado ejecuta la función JavaScript pasando el índice 0, que corresponde al archivo '0802.mp3'.

**Ejemplo de tarjeta de canción:**
```html
<article onclick="reproducirCancion(1)">
  <img src="cancion.jpg" alt="Canción">
  <p>Título de la canción</p>
</article>
```

### Características clave de mi implementación

- **Responsividad**: He configurado el grid para que cambie de múltiples columnas a una sola en pantallas pequeñas.
- **Accesibilidad**: He usado atributos `alt` en imágenes y controles nativos de audio.
- **Performance**: He optimizado el CSS con `will-change` implícito en las transiciones.
- **UX moderna**: He añadido efectos hover, sombras y animaciones para feedback visual.

### Errores comunes que he aprendido a evitar

❌ **Error 1**: No incluir `user-scalable=no` en el viewport.
✅ **Solución que apliqué**: Añadí `<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">` para evitar zoom accidental.

❌ **Error 2**: Usar `position: absolute` sin considerar el scroll del contenido.
✅ **Solución que apliqué**: Usé `position: fixed` para el reproductor y ajusté el `padding-bottom` del body.

❌ **Error 3**: No añadir `box-sizing: border-box` causando desbordamientos.
✅ **Solución que apliqué**: Apliqué reset CSS completo con `* { box-sizing: border-box; }`.

❌ **Error 4**: Rutas de archivos de audio incorrectas.
✅ **Solución que apliqué**: Verifiqué que los archivos .mp3 y .jpg estuvieran en la misma carpeta que el HTML o usé rutas relativas correctas.

❌ **Error 5**: Grid con columnas fijas que no se adaptan.
✅ **Solución que apliqué**: Usé `repeat(auto-fit, minmax(280px, 1fr))` para responsividad automática.

---

En esta actividad he integrado los tres pilares del desarrollo web moderno (HTML5, CSS3 y JavaScript) para crear una interfaz funcional de reproductor de música optimizada para dispositivos móviles. Los conceptos que he aplicado incluyen:

- **Estructura semántica** con HTML5
- **Diseño responsive** mediante Flexbox, Grid y media queries
- **Interactividad** con JavaScript y manipulación del DOM
- **API de audio HTML5** para reproducción multimedia
- **Optimización móvil** con viewport y controles táctiles

Estos conocimientos son fundamentales para mi formación en el análisis de tecnologías para dispositivos móviles (tema actual de la unidad) y se conectan directamente con:
- Las tecnologías que hemos visto en ejercicios anteriores (001-007)
- Los conceptos de responsive design y viewport que he aprendido
- Mi preparación para el desarrollo con frameworks móviles como Android Studio (ejercicio 007)
- Las bases que necesito para entender Progressive Web Apps y aplicaciones híbridas

Con esta actividad he demostrado cómo las tecnologías web pueden emular experiencias nativas en dispositivos móviles, siendo una alternativa viable al desarrollo nativo tradicional que estudiaremos más adelante en 2º DAM.
