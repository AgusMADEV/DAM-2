
Bueno, las librerías multimedia integradas básicamente son herramientas que vienen ya en los navegadores y que nos permiten trabajar con audio, vídeo e imágenes en nuestras apps web y móviles. Lo que he tenido que hacer en este ejercicio es crear un sistema para cambiar la calidad de los vídeos, porque no todo el mundo tiene buena conexión a internet o quiere gastar muchos datos.

He usado el elemento `<video>` de HTML5 con JavaScript para controlar los vídeos sin tener que instalar nada extra. Esto es lo que usan plataformas como YouTube o cualquier página web que tenga vídeos. 

La idea de poder cambiar entre diferentes resoluciones es súper útil porque así el usuario puede elegir la calidad según su conexión o si quiere ahorrar datos del móvil.

---

**Librerías Multimedia Integradas**: Son APIs (interfaces de programación) que ya vienen en los navegadores y que nos dejan trabajar con multimedia sin instalar nada. Yo he usado la API HTML5 Media Elements.

**Resolución de Video**: Básicamente son los píxeles que tiene el vídeo, tipo 1920x1080 (1080p). A más resolución, mejor se ve pero también pesa más y consume más datos.

### Lo que he usado para hacer esto

1. **Elemento `<video>`**: Es la etiqueta de HTML5 donde va el vídeo. Tiene cosas como `src` (la ruta del vídeo), `controls` (para que se vean los botones de play, pause, etc.), y funciones como `load()` y `play()`.

2. **Document Object Model (DOM)**: Esto es lo que uso para que JavaScript "hable" con el HTML. Los métodos principales que he usado son:
   - `document.getElementById()`: Para pillar un elemento por su ID
   - `document.querySelectorAll()`: Para coger todos los botones de una vez
   - `addEventListener()`: Para que se ejecute algo cuando haces click

3. **Eventos**: Son las cosas que pasan en la app, como cuando haces click en un botón. Yo he usado el evento `click` para saber cuándo el usuario pulsa un botón de resolución.

### Cómo funciona esto paso a paso

**Paso 1 - HTML**: Primero he creado el HTML con la etiqueta `<video>` y un botón para cada resolución (1080p, 720p, etc.). Cada botón tiene su propio ID.

**Paso 2 - Coger los elementos**: Con JavaScript pillo la referencia al vídeo y a todos los botones usando el DOM.

**Paso 3 - Poner los eventos**: Le pongo un `addEventListener` a cada botón para que cuando le des click pase algo.

**Paso 4 - Cambiar el vídeo**: Cuando haces click en un botón:
   - Miro qué botón has pulsado por su ID
   - Cambio el `src` del vídeo con la ruta del archivo que corresponde
   - Llamo a `load()` para que cargue el nuevo vídeo
   - Llamo a `play()` para que empiece a reproducirse solo

**Paso 5 - Ver el vídeo**: El navegador carga y reproduce el vídeo en la resolución que has elegido.

### Conceptos que he tenido que aprender

- **API**: Son un montón de funciones que te deja usar el navegador para hacer cosas con multimedia
- **Event Listener**: Es una función que está "escuchando" para ejecutarse cuando pasa algo (como un click)
- **Switch**: Estructura que he usado para comprobar qué botón se ha pulsado y hacer una cosa u otra
- **Método**: Básicamente es una función de un objeto, como `play()` o `load()`

---

Este es el código completo que he hecho para la práctica:

```html
<!doctype html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestión de Videos</title>
    <style>
        #video-container {
            width: 800px;
            height: 500px;
            position: relative;
            margin: auto;
        }
        video {
            width: 100%;
            height: 100%;
            border-radius: 10px;
        }
        .controls {
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 10px;
        }
        button {
            padding: 10px 20px;
            border: none;
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div id="video-container">
        <video id="myVideo" controls></video>
        <div class="controls">
            <button id="load1080">1080p</button>
            <button id="load720">720p</button>
            <button id="load480">480p</button>
            <button id="load360">360p</button>
            <button id="load240">240p</button>
            <button id="load144">144p</button>
        </div>
    </div>

    <script>
        const video = document.getElementById('myVideo');
        const buttons = document.querySelectorAll('.controls button');

        buttons.forEach(button => {
            button.addEventListener('click', () => {
                switch (button.id) {
                    case 'load1080':
                        video.src = '../101-Ejercicios/video/video_1080p.mp4';
                        break;
                    case 'load720':
                        video.src = '../101-Ejercicios/video/video_720p.mp4';
                        break;
                    case 'load480':
                        video.src = '../101-Ejercicios/video/video_480p.mp4';
                        break;
                    case 'load360':
                        video.src = '../101-Ejercicios/video/video_360p.mp4';
                        break;
                    case 'load240':
                        video.src = '../101-Ejercicios/video/video_240p.mp4';
                        break;
                    case 'load144':
                        video.src = '../101-Ejercicios/video/video_144p.mp4';
                        break;
                }
                video.load();
                video.play();
            });
        });
    </script>
</body>
</html>
```

### Explicación del código

**Parte HTML**:
- He puesto un contenedor `#video-container` para meter el vídeo y los botones
- La etiqueta `<video>` tiene el atributo `controls` para que se vean los controles típicos (play, pausa, volumen...)
- Los 6 botones son para elegir la resolución (desde 144p hasta 1080p)

**Parte CSS**:
- Le he puesto un tamaño fijo al contenedor (800x500px)
- Los botones están posicionados abajo del todo
- He usado `transform: translateX(-50%)` para centrar los botones, es un truco que aprendí en clase

**Parte JavaScript**:
- Con `getElementById` cojo el elemento del vídeo
- Con `querySelectorAll` cojo todos los botones de golpe
- El `forEach` me sirve para recorrer todos los botones y ponerles el evento click
- El `switch` mira qué botón has pulsado por su ID
- Cada `case` cambia la ruta del vídeo en el `src`
- Los métodos `load()` y `play()` cargan y reproducen el vídeo nuevo

### Errores que he tenido (y cómo los he solucionado)

1. **Las rutas de los archivos estaban mal**
   - Al principio me daba error porque la ruta no era correcta. Tuve que revisar bien dónde estaban los vídeos y poner la ruta relativa bien.

2. **El vídeo no se reproducía automáticamente**
   - Me olvidé de poner `load()` antes de `play()`. Hay que llamar primero a `load()` para cargar el vídeo y luego a `play()` para reproducirlo.

3. **No poner el método `load()`**
   - Este error me lo he comido varias veces. Después de cambiar el `src` siempre hay que llamar a `video.load()` si no, no carga el vídeo nuevo.

4. **Líos con las comillas**
   - Al principio se me olvidaban las comillas en las rutas o ponía unas simples y otras dobles mezcladas.

5. **Usar var en vez de const o let**
   - Al principio usaba `var` pero el profe nos dijo que en JavaScript moderno hay que usar `const` (si no cambia) o `let` (si cambia).

---

Bueno, con este ejercicio he aprendido a trabajar con las librerías multimedia de HTML5 para hacer una app que cambia la resolución de los vídeos. Lo más importante que me llevo es:

- El elemento `<video>` de HTML5 te deja controlar vídeos sin tener que instalar nada extra
- Con JavaScript puedes manipular el DOM para hacer que los elementos HTML hagan cosas cuando el usuario interactúa con ellos
- Cambiando el `src` dinámicamente puedes cargar diferentes vídeos sobre la marcha
- Los métodos `load()` y `play()` son súper importantes para controlar el vídeo

Este ejercicio tiene que ver con otros temas que hemos dado en la unidad:
- **Procesamiento de objetos multimedia**: He trabajado con objetos de tipo vídeo y sus propiedades
- **Fuentes de datos multimedia**: Los vídeos se cargan desde rutas locales
- **Arquitectura del API**: He usado la API HTML5 Media Elements

La verdad es que esto de poder cambiar la calidad del vídeo es muy útil para apps reales, sobre todo si el usuario tiene una conexión mala o está en el móvil y no quiere gastar muchos datos. Esto es la base para cosas más avanzadas como el streaming adaptativo (HLS, DASH) que supongo que veremos más adelante.