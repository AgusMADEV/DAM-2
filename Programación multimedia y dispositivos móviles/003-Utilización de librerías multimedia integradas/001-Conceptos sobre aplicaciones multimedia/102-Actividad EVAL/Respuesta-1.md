# 102-Actividad EVAL — Carga de resoluciones de vídeo (PMDM)

## 1) Introducción breve y contextualización (25%)
En esta actividad planteo una situación típica en una app de gestión de partidos: yo quiero ver **vídeos de partidos** y poder elegir **la resolución** según la calidad de mi conexión (por ejemplo, si estoy con datos móviles tiro de 360p/240p, y si estoy en Wi‑Fi uso 1080p).

A nivel de temario, esto encaja con **HTML5 Multimedia** y el uso de **librerías multimedia integradas del navegador**, concretamente el elemento `<video>` y su API en JavaScript (`src`, `load()`, `play()`, etc.). La idea es dar un control sencillo para **cambiar de “rendition”** (misma pieza de vídeo, diferentes calidades).

---

## 2) Desarrollo detallado y preciso (25%)

### Estructura base (HTML + contenedor)
En `102-Actividad EVAL/video.html` tengo:
- Un contenedor `#video-container` para delimitar el reproductor.
- Un `<video id="myVideo" controls></video>` que es el **reproductor HTML5**.
- Una capa `.controls` con varios `<button>` para seleccionar cada resolución (1080p, 720p, etc.).

Esto sigue el patrón visto en clase: **vídeo + controles propios** encima/abajo del vídeo.

### Estilo (CSS)
En el `<style>`:
- Ajusto el tamaño del contenedor a `800x500` y centro con `margin: auto`.
- Hago que el `<video>` ocupe el 100% y tenga `border-radius`.
- Coloco los botones con `position: absolute` en la parte inferior (`bottom: 20px`) y centrados con `left: 50%` + `transform: translateX(-50%)`.

### Lógica (JavaScript paso a paso)
En el `<script>`:
1. Selecciono el vídeo:
   ```js
   const video = document.getElementById('myVideo');
   ```
2. Selecciono todos los botones:
   ```js
   const buttons = document.querySelectorAll('.controls button');
   ```
3. Recorro botones con `forEach` y añado `addEventListener('click', ...)`.
4. Dentro del click, uso un `switch (button.id)` para decidir qué archivo cargar:
   - `video.src = '../101-Ejercicios/video/video_1080p.mp4';`  
   - `video.src = '../101-Ejercicios/video/video_720p.mp4';`  
   - etc.
5. Después de cambiar el `src`, ejecuto:
   ```js
   video.load();
   video.play();
   ```
   - `load()` fuerza a que el navegador recargue el recurso nuevo.
   - `play()` inicia la reproducción.

**Terminología aplicada (moderada):**
- *Rendition*: versión del mismo vídeo en distinta resolución.
- *Evento* `click`: disparador de cambio de calidad.
- *API del elemento vídeo*: propiedades/métodos del `<video>` (`src`, `load()`, `play()`).

---

## 3) Aplicación práctica (25%)

### Cómo se aplica en una app real
En una app de partidos, el usuario podría tocar “720p” cuando va con cobertura normal, o “240p” cuando va justo de datos. La lógica sería la misma: **cambiar la fuente** del vídeo al fichero correspondiente y reproducir.

Ejemplo real (de mi propio `video.html`):
```js
case 'load360':
  video.src = '../101-Ejercicios/video/video_360p.mp4';
  break;
video.load();
video.play();
```

### Errores comunes y cómo evitarlos
- **Rutas mal puestas**: si el `src` apunta mal, el vídeo no carga. Solución: comprobar la ruta relativa desde `102-Actividad EVAL` hacia `101-Ejercicios/video/`.
- **Olvidar `load()`**: a veces el navegador no “refresca” el vídeo si solo cambias `src`. Solución: llamar a `video.load()` tras cambiar la fuente.
- **Autoplay bloqueado**: algunos navegadores bloquean `play()` si no viene de una interacción real del usuario. Aquí lo llamo **dentro del click**, así que normalmente funciona.
- **Corte brusco al cambiar resolución**: el cambio reinicia el vídeo porque se vuelve a cargar. (En ejercicios más avanzados se puede guardar `currentTime` y restaurarlo, pero aquí me quedo en lo visto en clase).

---

## 4) Conclusión breve (25%)
En resumen, he montado un reproductor con `<video>` y controles personalizados para **cargar distintas resoluciones** usando JavaScript. Lo importante es:
- Seleccionar el botón,
- Cambiar `video.src`,
- Ejecutar `video.load()` y `video.play()`.

Esto se relaciona directamente con lo visto en la unidad: **multimedia en HTML5**, manejo de **eventos** y uso de la **API del elemento vídeo**. Como ampliación natural (siguiendo el temario), se puede evolucionar a un selector dinámico (con `<select>` y JSON de renditions) o incluso convertirlo en una mini “librería” reutilizable, igual que en los ejercicios posteriores.
