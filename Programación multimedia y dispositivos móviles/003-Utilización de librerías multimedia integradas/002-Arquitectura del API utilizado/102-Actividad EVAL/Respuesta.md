Las aplicaciones multimedia modernas utilizan librerías integradas para gestionar la reproducción de audio y video de manera eficiente. Ejemplos cotidianos incluyen:

- **Spotify**: Gestiona la reproducción de audio con controles de volumen, progreso visual y gestión de listas de reproducción.
- **YouTube**: Maneja video con controles de reproducción, pausar, adelantar/retroceder, y visualización de progreso con seek bar.
- **Reproductores nativos del navegador**: Utilizan el API HTML5 Audio/Video para proporcionar funcionalidades multimedia sin plugins externos.

#### Características Comunes de Gestión Multimedia

1. **Control de Reproducción**: 
   - Play/Pause mediante eventos onclick
   - Métodos como `audio.play()` y `audio.pause()`
   
2. **Control de Volumen**:
   - Utilización de sliders (`<input type="range">`) conectados a la propiedad `volume`
   - Rango típico: 0.0 a 1.0

3. **Visualización del Progreso**:
   - Barras de progreso (`<progress>`) que reflejan `currentTime/duration`
   - Actualización en tiempo real mediante bucles o eventos `timeupdate`
   - Seek bars interactivos que permiten al usuario saltar a diferentes posiciones

4. **Gestión de Eventos**:
   - `onchange`: Para detectar cambios en controles de usuario
   - `timeupdate`: Para sincronizar UI con reproducción
   - Bucles con `setTimeout` o `setInterval` para actualizaciones continuas

---

### Ejercicio 1: Desvelar Onda (0802.html)

#### Objetivo
Implementar la visualización de la onda del audio utilizando una imagen que se "desvela" progresivamente mediante una máscara que se reduce a medida que avanza la reproducción.

#### Análisis del Código Base

El ejercicio [007-desvelar onda.html](../101-Ejercicios/007-desvelar%20onda.html) implementa un reproductor avanzado con un efecto visual único:

```html
<div class="waveform-container">
    <div class="waveform-background"></div>
    <img src="0802.png" alt="Waveform" class="waveform-image">
    <div class="waveform-progress-mask" id="waveformProgress"></div>
    <div class="waveform-overlay"></div>
</div>
```

#### El Efecto "Desvelar Onda"

Este es el concepto clave del ejercicio: **revelar progresivamente la imagen de la onda del audio**.

**Técnica de implementación**:

1. **Capas superpuestas** (de abajo hacia arriba):
   - Fondo base (`waveform-background`)
   - Imagen de la onda completa (`waveform-image`)
   - **Máscara blanca** (`waveform-progress-mask`) - ¡Esta es la clave!
   - Overlay semitransparente opcional

2. **CSS para el efecto de máscara**:
```css
.waveform-container {
    position: relative;
    height: 100px;
    overflow: hidden;  /* Oculta lo que sobresale */
}

.waveform-image {
    position: absolute;
    width: 100%;
    height: 100%;
    z-index: 2;  /* La imagen de la onda */
}

.waveform-progress-mask {
    position: absolute;
    top: 0;
    right: 0;      /* Anclada a la derecha */
    width: 100%;   /* Empieza cubriendo todo */
    height: 100%;
    background: rgba(255, 255, 255, 0.9);  /* Máscara blanca */
    z-index: 3;    /* Por encima de la imagen */
    transition: width 0.1s linear;
}
```

3. **JavaScript para el desvelado**:
```javascript
function updateProgress() {
    const progress = audio.currentTime / audio.duration;
    // La máscara se reduce de derecha a izquierda
    // 100% = onda oculta (inicio)
    // 0% = onda completamente visible (final)
    waveformProgress.style.width = `${100 - (progress * 100)}%`;
}
```

#### Funcionamiento Visual

```
Inicio (0%):
┌────────────────────────┐
│████████████████████████│ ← Máscara blanca (100% ancho)
│   (Onda oculta)        │
└────────────────────────┘

Mitad (50%):
┌────────────────────────┐
│🌊🌊🌊🌊████████████████│ ← Máscara (50% ancho)
│ (50% visible)          │
└────────────────────────┘

Final (100%):
┌────────────────────────┐
│🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊│ ← Sin máscara (0% ancho)
│  (Totalmente visible)  │
└────────────────────────┘
```

#### Conceptos Clave Implementados

1. **Posicionamiento CSS absoluto**: Todas las capas se superponen en el mismo espacio
2. **z-index**: Control del orden de apilamiento (máscara encima de imagen)
3. **Anclaje a la derecha**: `right: 0` hace que la máscara se reduzca desde la derecha
4. **Sincronización con audio**: Cálculo `100 - (progreso * 100)` para invertir el valor

#### Ventajas del Efecto Visual

- **Feedback visual inmediato**: El usuario ve qué parte del audio ha sonado
- **Estéticamente atractivo**: Mejor que una simple barra de progreso
- **Intuitivo**: La onda "se va revelando" igual que el audio "se va escuchando"
- **Performance**: Solo cambia una propiedad CSS (`width`), muy eficiente

---

### Ejercicio 4: Bucle (bucle.html)

#### Objetivo
Crear un bucle que actualice el progreso del audio y la posición del seek bar en tiempo real, gestionando eventos de reproducción.

#### Análisis del Código

El archivo [004-bucle.html](004-bucle.html#L60-L75) implementa el sistema de bucle fundamental:

```javascript
var audio = document.querySelector("audio");
var boton = document.querySelector("button");
var tiempo = document.querySelector("input");
var progreso = document.querySelector("progress");

// Control de reproducción
boton.onclick = function() {
    audio.play();
}

// Navegación manual (seek)
tiempo.onchange = function() {
    let duracion = audio.duration;
    audio.currentTime = this.value * duracion;
}

// Bucle de actualización
let temporizador = setTimeout("bucle()", 1000);

function bucle() {
    let duracion = audio.duration;
    progreso.value = audio.currentTime / duracion;
    tiempo.value = audio.currentTime / duracion;
    clearTimeout(temporizador);
    setTimeout("bucle()", 100);
}
```

#### Conceptos Técnicos Clave

1. **Propiedades del API Audio**:
   - `audio.duration`: Duración total del archivo (en segundos)
   - `audio.currentTime`: Posición actual de reproducción (en segundos)
   - Ambas son esenciales para calcular el progreso normalizado (0 a 1)

2. **Normalización del Progreso**:
   ```javascript
   progreso.value = audio.currentTime / duracion; // Valor entre 0 y 1
   ```

3. **Conversión Bidireccional**:
   - **Audio → UI**: `currentTime/duration` para mostrar progreso
   - **UI → Audio**: `value * duration` para establecer posición

4. **Gestión de Temporizadores**:
   ```javascript
   clearTimeout(temporizador);          // Limpia el anterior
   setTimeout("bucle()", 100);          // Programa el siguiente
   ```
   
   Esto previene la acumulación de temporizadores y garantiza un único bucle activo.

#### Mejoras Técnicas Posibles

1. **Uso de requestAnimationFrame** (más eficiente):
```javascript
function bucle() {
    let duracion = audio.duration;
    if (!isNaN(duracion)) {
        progreso.value = audio.currentTime / duracion;
        tiempo.value = audio.currentTime / duracion;
    }
    requestAnimationFrame(bucle);
}
```

2. **Evento timeupdate nativo**:
```javascript
audio.addEventListener('timeupdate', function() {
    let duracion = audio.duration;
    progreso.value = audio.currentTime / duracion;
    tiempo.value = audio.currentTime / duracion;
});
```

3. **Control Play/Pause mejorado**:
```javascript
boton.onclick = function() {
    if (audio.paused) {
        audio.play();
        boton.textContent = "⏸";
    } else {
        audio.pause();
        boton.textContent = "▶";
    }
}
```

---

### Proyecto Integrado: Reproductor Multimedia Completo

He creado un reproductor que **combina ambos ejercicios (Desvelar Onda + Bucle)**, incluyendo:

✅ **Ejercicio 1 - Desvelar Onda**: Visualización de la onda que se revela progresivamente  
✅ **Ejercicio 4 - Bucle**: Sistema de actualización en tiempo real con `requestAnimationFrame`  
✅ Reproducción de audio con controles avanzados (Play/Pause, adelantar/retroceder)  
✅ Control de volumen con iconos dinámicos  
✅ Seek bar funcional sincronizado con la visualización  
✅ Información de tiempo formateada (mm:ss)  
✅ Controles de teclado para accesibilidad  
✅ Diseño moderno y responsive  

#### Estructura del Reproductor

El archivo [reproductor-completo.html](reproductor-completo.html) integra ambas técnicas:

**1. Implementación del Efecto Desvelar Onda (Ejercicio 1)**

```html
<!-- Visualización de onda que se desvela -->
<div class="waveform-container">
    <img src="0802.png" alt="Waveform" class="waveform-image">
    <div class="waveform-progress-mask" id="waveformProgress"></div>
    <div class="waveform-overlay"></div>
</div>
```

```css
.waveform-progress-mask {
    position: absolute;
    top: 0;
    right: 0;
    width: 100%;
    height: 100%;
    background: rgba(255, 255, 255, 0.9);
    z-index: 3;
    transition: width 0.1s linear;
}
```

**2. Implementación del Bucle de Actualización (Ejercicio 4)**

```javascript
// Bucle con requestAnimationFrame (más eficiente que setTimeout)
function actualizarProgreso() {
    if (!isNaN(audio.duration)) {
        const progreso = audio.currentTime / audio.duration;
        
        // Actualizar barra de progreso
        progressBar.value = progreso;
        seekBar.value = progreso;
        
        // Actualizar tiempo
        tiempoActual.textContent = formatearTiempo(audio.currentTime);
        
        // EFECTO DESVELAR ONDA: Reducir máscara de derecha a izquierda
        waveformProgress.style.width = `${100 - (progreso * 100)}%`;
    }
    
    // Continuar el bucle
    requestAnimationFrame(actualizarProgreso);
}

// Iniciar el bucle
requestAnimationFrame(actualizarProgreso);
```

**3. Sincronización Bidireccional con Seek Bar**

```javascript
// Cuando el usuario mueve el seek bar
seekBar.addEventListener('input', function() {
    const tiempo = this.value * audio.duration;
    audio.currentTime = tiempo;
    
    // Actualizar TAMBIÉN el efecto de desvelar onda
    const progreso = this.value;
    waveformProgress.style.width = `${100 - (progreso * 100)}%`;
});
```

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reproductor Multimedia Integrado</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        
        #reproductor {
            width: 400px;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }
        
        .cabecera {
            text-align: center;
            margin-bottom: 25px;
        }
        
        .cabecera h1 {
            color: #667eea;
            font-size: 24px;
            margin-bottom: 5px;
        }
        
        .info-cancion {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 25px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 12px;
        }
        
        .portada {
            width: 80px;
            height: 80px;
            border-radius: 8px;
            object-fit: cover;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        .detalles {
            flex: 1;
        }
        
        .titulo-cancion {
            font-weight: 600;
            font-size: 16px;
            color: #333;
            margin-bottom: 4px;
        }
        
        .artista {
            font-size: 14px;
            color: #666;
        }
        
        .controles-principales {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .boton-control {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            border: none;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-size: 24px;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            transition: all 0.3s ease;
        }
        
        .boton-control:hover {
            transform: scale(1.1);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        }
        
        .boton-control:active {
            transform: scale(0.95);
        }
        
        .boton-secundario {
            width: 45px;
            height: 45px;
            font-size: 18px;
            background: linear-gradient(135deg, #a8b4ea 0%, #9d8ab2 100%);
        }
        
        .seccion-progreso {
            margin-bottom: 20px;
        }
        
        .barra-progreso-container {
            position: relative;
            height: 6px;
            margin-bottom: 10px;
        }
        
        .seek-bar {
            position: absolute;
            top: 0;
            width: 100%;
            height: 6px;
            -webkit-appearance: none;
            appearance: none;
            background: transparent;
            cursor: pointer;
            z-index: 2;
        }
        
        .seek-bar::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: #667eea;
            cursor: pointer;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            transition: all 0.2s ease;
        }
        
        .seek-bar::-webkit-slider-thumb:hover {
            transform: scale(1.2);
            background: #764ba2;
        }
        
        .seek-bar::-moz-range-thumb {
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: #667eea;
            cursor: pointer;
            border: none;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }
        
        .barra-progreso {
            position: absolute;
            top: 0;
            width: 100%;
            height: 6px;
            background: #e0e0e0;
            border-radius: 3px;
            overflow: hidden;
            z-index: 1;
        }
        
        .barra-progreso::-webkit-progress-bar {
            background: #e0e0e0;
            border-radius: 3px;
        }
        
        .barra-progreso::-webkit-progress-value {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 3px;
        }
        
        .barra-progreso::-moz-progress-bar {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 3px;
        }
        
        .tiempo {
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            color: #666;
        }
        
        .control-volumen {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 12px;
        }
        
        .icono-volumen {
            font-size: 20px;
            color: #667eea;
            min-width: 25px;
        }
        
        .slider-volumen {
            flex: 1;
            -webkit-appearance: none;
            appearance: none;
            height: 6px;
            background: #e0e0e0;
            border-radius: 3px;
            outline: none;
        }
        
        .slider-volumen::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: #667eea;
            cursor: pointer;
        }
        
        .slider-volumen::-moz-range-thumb {
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: #667eea;
            cursor: pointer;
            border: none;
        }
        
        .valor-volumen {
            font-size: 12px;
            color: #666;
            min-width: 35px;
            text-align: right;
        }
        
        /* Animación de reproducción */
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .reproduciendo .portada {
            animation: pulse 2s ease-in-out infinite;
        }
    </style>
</head>
<body>
    <div id="reproductor">
        <div class="cabecera">
            <h1>🎵 Music Player</h1>
        </div>
        
        <div class="info-cancion">
            <img src="0802.png" alt="Portada" class="portada" id="portada">
            <div class="detalles">
                <div class="titulo-cancion">Audio Track</div>
                <div class="artista">Multimedia Learning</div>
            </div>
        </div>
        
        <div class="controles-principales">
            <button class="boton-control boton-secundario" id="retroceder" title="Retroceder 10s">⏮</button>
            <button class="boton-control" id="playPause">▶</button>
            <button class="boton-control boton-secundario" id="avanzar" title="Avanzar 10s">⏭</button>
        </div>
        
        <audio id="audio" src="0802.mp3"></audio>
        
        <div class="seccion-progreso">
            <div class="barra-progreso-container">
                <input type="range" min="0" max="1" step="0.001" value="0" class="seek-bar" id="seekBar">
                <progress value="0" max="1" class="barra-progreso" id="progressBar"></progress>
            </div>
            <div class="tiempo">
                <span id="tiempoActual">0:00</span>
                <span id="tiempoTotal">0:00</span>
            </div>
        </div>
        
        <div class="control-volumen">
            <span class="icono-volumen" id="iconoVolumen">🔊</span>
            <input type="range" min="0" max="100" value="70" class="slider-volumen" id="volumen">
            <span class="valor-volumen" id="valorVolumen">70%</span>
        </div>
    </div>
    
    <script>
        // Referencias a elementos del DOM
        const audio = document.getElementById('audio');
        const playPauseBtn = document.getElementById('playPause');
        const retrocederBtn = document.getElementById('retroceder');
        const avanzarBtn = document.getElementById('avanzar');
        const seekBar = document.getElementById('seekBar');
        const progressBar = document.getElementById('progressBar');
        const tiempoActual = document.getElementById('tiempoActual');
        const tiempoTotal = document.getElementById('tiempoTotal');
        const volumenSlider = document.getElementById('volumen');
        const valorVolumen = document.getElementById('valorVolumen');
        const iconoVolumen = document.getElementById('iconoVolumen');
        const reproductor = document.getElementById('reproductor');
        
        // Estado inicial
        let estáReproduciendo = false;
        
        // Configuración inicial del volumen
        audio.volume = volumenSlider.value / 100;
        
        // Función para formatear tiempo (segundos a mm:ss)
        function formatearTiempo(segundos) {
            if (isNaN(segundos)) return '0:00';
            const minutos = Math.floor(segundos / 60);
            const segs = Math.floor(segundos % 60);
            return `${minutos}:${segs.toString().padStart(2, '0')}`;
        }
        
        // Control Play/Pause
        playPauseBtn.addEventListener('click', function() {
            if (estáReproduciendo) {
                audio.pause();
                playPauseBtn.textContent = '▶';
                reproductor.classList.remove('reproduciendo');
            } else {
                audio.play();
                playPauseBtn.textContent = '⏸';
                reproductor.classList.add('reproduciendo');
            }
            estáReproduciendo = !estáReproduciendo;
        });
        
        // Retroceder 10 segundos
        retrocederBtn.addEventListener('click', function() {
            audio.currentTime = Math.max(0, audio.currentTime - 10);
        });
        
        // Avanzar 10 segundos
        avanzarBtn.addEventListener('click', function() {
            audio.currentTime = Math.min(audio.duration, audio.currentTime + 10);
        });
        
        // Actualizar duración total cuando se carga el audio
        audio.addEventListener('loadedmetadata', function() {
            tiempoTotal.textContent = formatearTiempo(audio.duration);
            progressBar.max = 1;
        });
        
        // Bucle de actualización del progreso
        function actualizarProgreso() {
            if (!isNaN(audio.duration)) {
                const progreso = audio.currentTime / audio.duration;
                
                // Actualizar barra de progreso visual
                progressBar.value = progreso;
                
                // Actualizar seek bar solo si el usuario no lo está moviendo
                if (!seekBar.matches(':active')) {
                    seekBar.value = progreso;
                }
                
                // Actualizar tiempo actual
                tiempoActual.textContent = formatearTiempo(audio.currentTime);
            }
            
            requestAnimationFrame(actualizarProgreso);
        }
        
        // Iniciar el bucle de actualización
        requestAnimationFrame(actualizarProgreso);
        
        // Navegación manual con seek bar
        seekBar.addEventListener('input', function() {
            const tiempo = this.value * audio.duration;
            audio.currentTime = tiempo;
        });
        
        // Control de volumen
        volumenSlider.addEventListener('input', function() {
            const volumen = this.value;
            audio.volume = volumen / 100;
            valorVolumen.textContent = volumen + '%';
            
            // Actualizar icono según el nivel de volumen
            if (volumen == 0) {
                iconoVolumen.textContent = '🔇';
            } else if (volumen < 50) {
                iconoVolumen.textContent = '🔉';
            } else {
                iconoVolumen.textContent = '🔊';
            }
        });
        
        // Mute/Unmute al hacer clic en el icono
        iconoVolumen.addEventListener('click', function() {
            if (audio.volume > 0) {
                audio.volume = 0;
                volumenSlider.value = 0;
                valorVolumen.textContent = '0%';
                iconoVolumen.textContent = '🔇';
            } else {
                audio.volume = 0.7;
                volumenSlider.value = 70;
                valorVolumen.textContent = '70%';
                iconoVolumen.textContent = '🔊';
            }
        });
        
        // Reiniciar cuando termina la canción
        audio.addEventListener('ended', function() {
            playPauseBtn.textContent = '▶';
            estáReproduciendo = false;
            reproductor.classList.remove('reproduciendo');
            audio.currentTime = 0;
        });
        
        // Controles de teclado
        document.addEventListener('keydown', function(e) {
            switch(e.code) {
                case 'Space':
                    e.preventDefault();
                    playPauseBtn.click();
                    break;
                case 'ArrowLeft':
                    retrocederBtn.click();
                    break;
                case 'ArrowRight':
                    avanzarBtn.click();
                    break;
                case 'ArrowUp':
                    e.preventDefault();
                    volumenSlider.value = Math.min(100, parseInt(volumenSlider.value) + 5);
                    volumenSlider.dispatchEvent(new Event('input'));
                    break;
                case 'ArrowDown':
                    e.preventDefault();
                    volumenSlider.value = Math.max(0, parseInt(volumenSlider.value) - 5);
                    volumenSlider.dispatchEvent(new Event('input'));
                    break;
            }
        });
    </script>
</body>
</html>
```

#### Características Implementadas

**Combinación de Ejercicios 1 y 4:**

1. **Reproducción Avanzada**:
   - Play/Pause con estado visual
   - Botones de avance/retroceso (±10 segundos)
   - Control por teclado (Espacio, flechas)

2. **Visualización Completa (Ejercicio 1 - Desvelar Onda)**:
   - Imagen de la onda del audio
   - Máscara blanca que se reduce progresivamente
   - Efecto visual de "desvelado" sincronizado con reproducción
   - Actualización en tiempo real tanto en reproducción como al usar seek bar

3. **Bucle de Actualización (Ejercicio 4)**:
   - `requestAnimationFrame` para actualizaciones eficientes (mejora sobre `setTimeout`)
   - Sincronización perfecta entre:
     * Barra de progreso (`<progress>`)
     * Seek bar (`<input type="range">`)
     * Tiempo actual/total (mm:ss)
     * **Efecto desvelar onda** (reducción de máscara)

4. **Control de Volumen Integral**:
   - Slider con valores 0-100%
   - Indicador numérico del nivel
   - Iconos dinámicos según volumen (🔇 🔉 🔊)
   - Click en icono para mute/unmute

5. **Optimizaciones Técnicas**:
   - `requestAnimationFrame` (60fps, más eficiente que `setTimeout`)
   - Formateo de tiempo con `padStart` para consistencia
   - Prevención de conflictos entre seek manual y actualización automática
   - Gestión adecuada del evento `ended`
   - Sincronización bidireccional (audio ↔ UI ↔ efecto visual)

#### Flujo de Funcionamiento Integrado

```
[Usuario hace click en Play]
    ↓
[audio.play() se ejecuta]
    ↓
[requestAnimationFrame inicia el bucle (Ejercicio 4)]
    ↓
[Cada frame (60 veces por segundo):]
    - Calcula progreso = currentTime / duration
    - Actualiza progressBar.value (barra de progreso)
    - Actualiza seekBar.value (si no está siendo usado)
    - Formatea y muestra tiempos (mm:ss)
    - 🌊 DESVELAR ONDA: waveformProgress.style.width = 100 - (progreso * 100)
    ↓
[Usuario mueve el seek bar manualmente]
    ↓
[Evento 'input' detectado]
    ↓
[audio.currentTime = seekBar.value * duration]
    ↓
[Actualiza TAMBIÉN el efecto de desvelar onda]
    ↓
[Bucle continúa desde nueva posición]
```

**Clave de la integración**: El bucle de actualización (Ejercicio 4) controla simultáneamente:
- Barra de progreso tradicional
- Display de tiempo
- **Efecto visual de desvelar onda (Ejercicio 1)**

Todo sincronizado con una única fuente de verdad: `audio.currentTime`

---

Los conceptos aprendidos en esta unidad sobre la arquitectura del API multimedia tienen aplicaciones directas en el desarrollo profesional:

#### 1. Reproductores Multimedia Completos

Las técnicas de control de audio estudiadas son fundamentales para crear reproductores avanzados como:

- **Aplicaciones de podcasts**: Gestión de múltiples episodios, marcadores de posición, velocidad de reproducción variable
- **Plataformas educativas**: Sincronización de audio/video con transcripciones, subtítulos y materiales didácticos
- **Sistemas de karaoke**: Visualización de letras sincronizadas con la reproducción de audio

**Integración necesaria**:
```javascript
// Control de velocidad de reproducción
audio.playbackRate = 1.5; // 1.5x velocidad

// Marcadores de tiempo
const marcadores = [
    { tiempo: 30, etiqueta: "Introducción" },
    { tiempo: 120, etiqueta: "Desarrollo" },
    { tiempo: 300, etiqueta: "Conclusión" }
];

// Saltar a marcador
function irAMarcador(indice) {
    audio.currentTime = marcadores[indice].tiempo;
}
```

#### 2. Plataformas de Streaming

Las funcionalidades básicas se escalan para sistemas complejos:

- **Gestión de listas de reproducción**: Arrays de objetos con rutas de archivos
- **Reproducción continua**: Detección del evento `ended` para cargar siguiente track
- **Historial y favoritos**: LocalStorage para persistencia de preferencias
- **Integración con APIs**: Obtención de metadatos y artwork de servicios externos

**Ejemplo de estructura de datos**:
```javascript
const playlist = [
    {
        id: 1,
        titulo: "Track 1",
        artista: "Artista A",
        album: "Album X",
        src: "audio/track1.mp3",
        portada: "img/album-x.jpg",
        duracion: 245
    },
    // ... más tracks
];

let indiceActual = 0;

audio.addEventListener('ended', function() {
    indiceActual = (indiceActual + 1) % playlist.length;
    cargarCancion(playlist[indiceActual]);
    audio.play();
});
```

#### 3. Aplicaciones de Edición Multimedia

Los bucles de actualización y control preciso del tiempo son esenciales para:

- **Editores de audio**: Selección de regiones, corte, pegado
- **Sincronización multipista**: Gestión de múltiples elementos `<audio>` simultáneos
- **Efectos en tiempo real**: Aplicación de filtros usando Web Audio API

**Ejemplo de Web Audio API**:
```javascript
const audioContext = new AudioContext();
const source = audioContext.createMediaElementSource(audio);
const gainNode = audioContext.createGain();
const biquadFilter = audioContext.createBiquadFilter();

// Configurar filtro pasa-bajos
biquadFilter.type = "lowpass";
biquadFilter.frequency.value = 1000;

// Conectar nodos
source.connect(biquadFilter);
biquadFilter.connect(gainNode);
gainNode.connect(audioContext.destination);
```

#### 4. Interfaces Adaptativas y Accesibilidad

Las técnicas aprendidas permiten crear interfaces inclusivas:

- **Controles de teclado**: Navegación sin mouse (implementado en el proyecto)
- **Lectura de pantalla**: Atributos ARIA para usuarios con discapacidad visual
- **Gestos táctiles**: Swipe para avanzar/retroceder en dispositivos móviles
- **Responsive design**: Adaptación a diferentes tamaños de pantalla

**Mejoras de accesibilidad**:
```html
<button 
    class="boton-control" 
    id="playPause"
    aria-label="Reproducir o pausar audio"
    aria-pressed="false">
    ▶
</button>

<input 
    type="range" 
    id="seekBar"
    aria-label="Barra de progreso del audio"
    aria-valuemin="0"
    aria-valuemax="100"
    aria-valuenow="0"
    aria-valuetext="0 segundos de 245 segundos">
```

### Reflexión sobre la Arquitectura del API

El API HTML5 Audio proporciona una base sólida pero limitada. Para aplicaciones profesionales, se recomienda:

1. **Usar Web Audio API** para procesamiento avanzado:
   - Análisis de frecuencias (visualización de espectro)
   - Efectos (reverb, delay, distorsión)
   - Mezcla multipista
   - Síntesis de audio

2. **Implementar almacenamiento persistente**:
   - LocalStorage para configuraciones simples
   - IndexedDB para datos complejos (playlists, historial)
   - Cache API para reproducción offline

3. **Considerar frameworks especializados**:
   - **Howler.js**: Gestión avanzada de audio cross-browser
   - **Wavesurfer.js**: Visualización de ondas interactiva
   - **Tone.js**: Síntesis y scheduling preciso

4. **Optimización de rendimiento**:
   - Lazy loading de recursos multimedia
   - Preloading estratégico
   - Service Workers para caché inteligente

### Conexión con el Temario de la Unidad

Esta actividad práctica consolida los conocimientos teóricos sobre:

- **Arquitectura del API**: Hemos trabajado directamente con propiedades y métodos del elemento `<audio>`
- **Fuentes de datos multimedia**: Carga de archivos locales (extensible a URLs remotas, streams)
- **Procesamiento de objetos multimedia**: Control de reproducción, volumen, posición
- **Gestión de eventos**: Listeners para interacción de usuario y cambios de estado
- **Tareas en segundo plano**: Bucles de actualización con `requestAnimationFrame`

### Próximos Pasos

Para continuar desarrollando habilidades en multimedia:

1. Implementar visualización de onda con Canvas y Web Audio API
2. Crear sistema de ecualización con múltiples bandas de frecuencia
3. Desarrollar un reproductor multi-formato (audio/video)
4. Integrar con APIs de servicios como Spotify o SoundCloud
5. Implementar reproducción sincronizada en múltiples dispositivos (WebRTC)

Esta actividad demuestra que los conceptos fundamentales del API multimedia, aunque sencillos en su forma básica, son la base para aplicaciones complejas y profesionales. La clave está en comprender profundamente los mecanismos de sincronización, gestión de eventos y optimización del rendimiento.
