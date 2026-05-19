He desarrollado un **Sistema de Gestión de Tareas con Interfaces Naturales de Usuario (NUI)**, que permite interactuar con una aplicación web mediante **reconocimiento de voz** y **detección de gestos con las manos**, eliminando la dependencia del teclado y ratón tradicionales.

Las interfaces naturales de usuario son paradigmas de interacción que permiten a los usuarios comunicarse con sistemas digitales de forma intuitiva, utilizando métodos de entrada que imitan la comunicación humana natural. En este proyecto, he implementado dos tipos principales de NUI:

- **Reconocimiento de voz**: Permite dar comandos verbales en español para gestionar tareas.
- **Reconocimiento de gestos**: Utiliza la cámara web para detectar movimientos de las manos y ejecutar acciones.

Este tipo de interfaces se utilizan en contextos donde la interacción tradicional es limitada o poco práctica: aplicaciones de accesibilidad para personas con movilidad reducida, entornos industriales donde las manos están ocupadas, sistemas de domótica, asistentes virtuales, aplicaciones de realidad aumentada, y sistemas de control vehicular.

El proyecto está desarrollado completamente en **HTML5**, **CSS3** y **JavaScript vanilla**, utilizando las APIs nativas **Web Speech API** para reconocimiento de voz y síntesis de habla, y **MediaPipe Hands** de Google para detección de gestos mediante visión por computador.

---

### Arquitectura del Sistema

El proyecto sigue un patrón de arquitectura **basado en eventos** donde las entradas naturales (voz y gestos) desencadenan acciones en el modelo de datos, que luego actualiza la vista. La estructura se divide en tres capas principales:

1. **Capa de Presentación**: HTML semántico con CSS moderno (glassmorphism, CSS Variables)
2. **Capa de Lógica**: JavaScript con gestión de estado y procesamiento de comandos
3. **Capa de Entrada Natural**: APIs de reconocimiento de voz y gestos

### Reconocimiento de Voz (Web Speech API)

He implementado el reconocimiento de voz utilizando la **SpeechRecognition API**, que forma parte de la especificación Web Speech API del W3C. Esta API permite convertir voz a texto (Speech-to-Text) en tiempo real.

#### Funcionamiento paso a paso:

**Paso 1: Inicialización del reconocedor**
```javascript
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const reconocimiento = new SpeechRecognition();
reconocimiento.lang = "es-ES";
reconocimiento.interimResults = false;
reconocimiento.continuous = false;
```

- `lang = "es-ES"`: Configura el idioma español de España para el reconocimiento.
- `interimResults = false`: Solo devuelve resultados finales, no transcripciones parciales.
- `continuous = false`: El reconocimiento se detiene automáticamente tras detectar silencio.

**Paso 2: Gestión de eventos del ciclo de vida**
```javascript
reconocimiento.onstart = function() {
  document.getElementById("btnEscuchar").classList.add("listening");
  document.getElementById("statusVoz").textContent = "🎤 Escuchando... Habla ahora";
};

reconocimiento.onresult = function(event) {
  const textoReconocido = event.results[0][0].transcript.toLowerCase();
  procesarComandoVoz(textoReconocido);
};

reconocimiento.onerror = function(event) {
  document.getElementById("statusVoz").textContent = `❌ Error: ${event.error}`;
};
```

**Paso 3: Procesamiento de comandos mediante análisis léxico**
```javascript
function procesarComandoVoz(comando) {
  const palabras = comando.split(" ");
  const accion = palabras[0];
  
  switch(accion) {
    case "agregar":
    case "añadir":
    case "crear":
      const tarea = palabras.slice(1).join(" ");
      agregarTarea(tarea);
      break;
    
    case "eliminar":
    case "borrar":
      const num = convertirNumeroTexto(palabras[1]);
      if (num !== null) {
        eliminarTarea(num);
      }
      break;
    // ... más casos
  }
}
```

He implementado **sinónimos** para cada acción (agregar/añadir/crear, eliminar/borrar) para hacer la interfaz más natural y tolerante a variaciones lingüísticas.

**Paso 4: Conversión de números textuales a dígitos**
```javascript
function convertirNumeroTexto(texto) {
  const numeros = {
    "cero": 0, "uno": 1, "dos": 2, "tres": 3, "cuatro": 4,
    "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9,
    "diez": 10
  };
  
  if (numeros.hasOwnProperty(texto)) {
    return numeros[texto];
  }
  
  const numeroDigito = parseInt(texto);
  if (!isNaN(numeroDigito)) {
    return numeroDigito;
  }
  
  return null;
}
```

Esta función permite que el usuario diga tanto "eliminar tres" como "eliminar 3", mejorando la usabilidad.

### Síntesis de Voz (Speech Synthesis API)

Para el feedback auditivo al usuario, he implementado síntesis de voz (Text-to-Speech) que lee las confirmaciones de acciones:

```javascript
let voices = [];

function cargarVoces() {
  voices = speechSynthesis.getVoices();
}

function elegirVoz() {
  const voz = voices.find(v => /es-|Spanish/i.test(v.lang)) || voices[0];
  return voz || null;
}

function hablar(texto) {
  const utterance = new SpeechSynthesisUtterance(texto);
  const voz = elegirVoz();
  if (voz) utterance.voice = voz;
  utterance.lang = (voz && voz.lang) || 'es-ES';
  utterance.rate = 1.0;
  utterance.pitch = 1.0;
  speechSynthesis.cancel();
  speechSynthesis.speak(utterance);
}

cargarVoces();
speechSynthesis.onvoiceschanged = cargarVoces;
```

**Funcionamiento:**
1. `cargarVoces()`: Obtiene las voces disponibles del sistema operativo.
2. `elegirVoz()`: Busca automáticamente una voz en español usando regex.
3. `hablar()`: Crea un objeto `SpeechSynthesisUtterance` con el texto y lo reproduce.
4. `speechSynthesis.cancel()`: Cancela cualquier reproducción anterior para evitar solapamientos.

### Reconocimiento de Gestos con MediaPipe Hands

He utilizado **MediaPipe Hands**, una solución de Google basada en Machine Learning que detecta 21 puntos de referencia (landmarks) en cada mano mediante visión por computador.

#### Funcionamiento paso a paso:

**Paso 1: Inicialización de MediaPipe**
```javascript
const hands = new Hands({
  locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`
});

hands.setOptions({
  maxNumHands: 1,
  modelComplexity: 1,
  minDetectionConfidence: 0.7,
  minTrackingConfidence: 0.7
});
```

- `maxNumHands: 1`: Detecta solo una mano para optimizar rendimiento.
- `modelComplexity: 1`: Balance entre precisión y velocidad.
- `minDetectionConfidence: 0.7`: Umbral de confianza del 70% para considerar una detección válida.

**Paso 2: Stream de video desde la cámara**
```javascript
const camera = new Camera(video, {
  onFrame: async () => {
    await hands.send({image: video});
  },
  width: 400,
  height: 300
});

camera.start();
```

**Paso 3: Procesamiento de resultados**
```javascript
function onResults(results) {
  ctx.save();
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.drawImage(results.image, 0, 0, canvas.width, canvas.height);
  
  if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
    for (const landmarks of results.multiHandLandmarks) {
      drawConnectors(ctx, landmarks, HAND_CONNECTIONS, {color: '#00FF00', lineWidth: 2});
      drawLandmarks(ctx, landmarks, {color: '#FF0000', lineWidth: 1, radius: 3});
      
      const gesto = detectarGesto(landmarks);
      if (gesto) {
        ejecutarAccionGesto(gesto);
      }
    }
  }
  
  ctx.restore();
}
```

Este método se ejecuta en cada frame (aproximadamente 30 FPS) y:
1. Limpia el canvas.
2. Dibuja la imagen de la cámara.
3. Dibuja las conexiones entre landmarks (líneas verdes).
4. Dibuja los landmarks individuales (puntos rojos).
5. Detecta y ejecuta gestos.

**Paso 4: Algoritmo de detección de gestos**

He implementado un algoritmo basado en la **posición relativa de los landmarks** para clasificar 4 gestos diferentes:

```javascript
function detectarGesto(landmarks) {
  if (!landmarks || landmarks.length === 0) return null;
  
  const pulgar = landmarks[4];
  const indicePunta = landmarks[8];
  const medioTip = landmarks[12];
  const anularTip = landmarks[16];
  const meniqueTip = landmarks[20];
  
  function dedoExtendido(punta, base) {
    return punta.y < base.y; // En coordenadas de canvas, y menor = más arriba
  }
  
  const indiceExtendido = dedoExtendido(indicePunta, landmarks[6]);
  const medioExtendido = dedoExtendido(medioTip, landmarks[10]);
  const anularExtendido = dedoExtendido(anularTip, landmarks[14]);
  const meniqueExtendido = dedoExtendido(meniqueTip, landmarks[18]);
  const pulgarExtendido = pulgar.x < landmarks[3].x;
  
  const dedosExtendidos = [
    indiceExtendido,
    medioExtendido,
    anularExtendido,
    meniqueExtendido
  ].filter(Boolean).length;
  
  // Clasificación de gestos
  if (indiceExtendido && medioExtendido && !anularExtendido && !meniqueExtendido) {
    return "dos_dedos"; // ✌️
  }
  
  if (pulgarExtendido && !indiceExtendido && !medioExtendido && !anularExtendido && !meniqueExtendido) {
    return "pulgar_arriba"; // 👍
  }
  
  if (!indiceExtendido && !medioExtendido && !anularExtendido && !meniqueExtendido) {
    return "puno"; // ✊
  }
  
  if (dedosExtendidos >= 4) {
    return "mano_abierta"; // 🖐️
  }
  
  return null;
}
```

**Terminología técnica:**
- **Landmarks**: Puntos de referencia 3D (x, y, z) detectados en la mano.
- **Finger tip**: Punta del dedo (índice 8, 12, 16, 20 para índice, medio, anular y meñique).
- **MCP (Metacarpophalangeal)**: Base del dedo en la palma.
- **Heurística de extensión**: Compara la coordenada Y de la punta con la base para determinar si el dedo está extendido.

**Paso 5: Sistema de cooldown para evitar activaciones múltiples**
```javascript
let lastGestureTime = 0;
const GESTURE_COOLDOWN = 2000; // 2 segundos

function ejecutarAccionGesto(gesto) {
  const ahora = Date.now();
  if (ahora - lastGestureTime < GESTURE_COOLDOWN) {
    return; // Ignora el gesto si está en cooldown
  }
  
  lastGestureTime = ahora;
  
  switch(gesto) {
    case "dos_dedos":
      const tareaAleatoria = tareasAleatorias[Math.floor(Math.random() * tareasAleatorias.length)];
      agregarTarea(tareaAleatoria);
      break;
    // ... más casos
  }
}
```

Este mecanismo evita que un gesto mantenido durante varios frames active la acción repetidamente.

### Gestión del Estado de la Aplicación

El estado de la aplicación se gestiona mediante un array de objetos JavaScript:

```javascript
let tareas = [
  {"id": 1, "titulo": "Estudiar interfaces naturales", "completada": false},
  {"id": 2, "titulo": "Practicar reconocimiento de voz", "completada": false},
  {"id": 3, "titulo": "Desarrollar proyecto final", "completada": false}
];

let contadorId = 4;
```

Cada operación CRUD modifica el array y llama a `pintaTabla()` para re-renderizar la vista:

```javascript
function agregarTarea(titulo) {
  if (!titulo || titulo.trim() === '') {
    hablar("No puedo agregar una tarea vacía");
    return;
  }
  tareas.push({
    id: contadorId++,
    titulo: titulo.trim(),
    completada: false
  });
  pintaTabla();
  hablar(`Tarea agregada: ${titulo}`);
}
```

### 2.6. Diseño CSS Profesional

He aplicado un diseño **minimalista** con técnicas modernas:

**CSS Variables para mantener consistencia:**
```css
:root {
  --bg-primary: #f8f9fa;
  --bg-secondary: #ffffff;
  --bg-glass: rgba(255, 255, 255, 0.7);
  --border-color: rgba(0, 0, 0, 0.08);
  --text-primary: #1a1a1a;
  --accent: #2563eb;
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --radius: 12px;
}
```

**Glassmorphism para efecto de profundidad:**
```css
.panel {
  background: var(--bg-glass);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-radius: var(--radius);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-md);
}
```

**Grid Layout para diseño responsivo:**
```css
.container {
  display: grid;
  grid-template-columns: 1fr 420px;
  gap: 24px;
}

@media (max-width: 1200px) {
  .container {
    grid-template-columns: 1fr;
  }
}
```

---

### Ejemplo de uso completo del sistema

**Escenario:** Usuario quiere agregar tres tareas mediante diferentes métodos.

**Método 1: Comando de voz**
1. Usuario pulsa el botón "Escuchar".
2. Sistema muestra "🎤 Escuchando... Habla ahora".
3. Usuario dice: "agregar estudiar para el examen de desarrollo de interfaces".
4. `SpeechRecognition` captura: "agregar estudiar para el examen de desarrollo de interfaces".
5. `procesarComandoVoz()` identifica acción "agregar" y extrae resto como título.
6. `agregarTarea()` crea objeto: `{id: 4, titulo: "estudiar para el examen de desarrollo de interfaces", completada: false}`.
7. `pintaTabla()` re-renderiza la tabla con la nueva tarea.
8. `hablar()` confirma: "Tarea agregada: estudiar para el examen de desarrollo de interfaces".

**Método 2: Gesto de dos dedos (✌️)**
1. Usuario muestra gesto de paz con índice y medio extendidos.
2. MediaPipe detecta 21 landmarks cada frame (~30 FPS).
3. `detectarGesto()` verifica: `indiceExtendido && medioExtendido && !anularExtendido && !meniqueExtendido` → devuelve "dos_dedos".
4. `ejecutarAccionGesto()` verifica cooldown (debe haber pasado 2 segundos desde último gesto).
5. Selecciona tarea aleatoria: "Revisar correo electrónico".
6. Ejecuta `agregarTarea("Revisar correo electrónico")`.
7. Feedback visual: "✌️ Gesto: Dos dedos - Tarea añadida".
8. Feedback auditivo: "Tarea agregada: Revisar correo electrónico".

**Método 3: Completar tarea con comando de voz**
1. Usuario dice: "completar dos".
2. `procesarComandoVoz()` identifica acción "completar".
3. `convertirNumeroTexto("dos")` devuelve `2`.
4. `completarTarea(2)` marca `tareas[2].completada = true`.
5. `pintaTabla()` re-renderiza mostrando tarea con estilo tachado y icono ✅.
6. `hablar()` confirma: "Tarea completada: Desarrollar proyecto final".

### Código real de renderizado con estado vacío

```javascript
function pintaTabla() {
  if (tareas.length === 0) {
    document.querySelector("#contenedorTabla").innerHTML = `
      <div class="empty-state">
        <div class="empty-state-icon">
          <svg viewBox="0 0 24 24" width="48" height="48" stroke="currentColor" fill="none">
            <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
          </svg>
        </div>
        <p style="font-size: 1.1em; margin-bottom: 8px;">No hay tareas aún</p>
        <p style="font-size: 0.9em; opacity: 0.8;">Usa comandos de voz o gestos para agregar tareas</p>
      </div>
    `;
    return;
  }

  let cadena = `
    <table>
      <thead>
        <tr>
          <th style="width: 60px;">#</th>
          <th>Tarea</th>
          <th style="width: 100px; text-align: center;">Estado</th>
        </tr>
      </thead>
      <tbody>
  `;
  
  tareas.forEach((tarea, index) => {
    const estado = tarea.completada 
      ? '<svg viewBox="0 0 24 24" width="16" height="16" style="stroke: #10b981; fill: none; stroke-width: 2;"><polyline points="20 6 9 17 4 12"></polyline></svg>' 
      : '<svg viewBox="0 0 24 24" width="16" height="16" style="stroke: #94a3b8; fill: none; stroke-width: 2;"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>';
    const estilo = tarea.completada ? 'style="text-decoration: line-through; opacity: 0.6;"' : '';
    cadena += `
      <tr ${estilo}>
        <td>${index}</td>
        <td>${tarea.titulo}</td>
        <td style="text-align: center;">${estado}</td>
      </tr>
    `;
  });
  
  cadena += "</tbody></table>";
  document.querySelector("#contenedorTabla").innerHTML = cadena;
}
```

Este método implementa el patrón **"Empty State"** de diseño UX, mostrando un mensaje amigable cuando no hay datos en lugar de una tabla vacía.

### Errores comunes y cómo evitarlos

#### Error 1: Activación múltiple de gestos
**Problema:** MediaPipe procesa ~30 frames por segundo. Sin control, un gesto sostenido por 1 segundo ejecutaría la acción 30 veces.

**Solución implementada:** Sistema de cooldown con timestamp.
```javascript
const GESTURE_COOLDOWN = 2000;
let lastGestureTime = 0;

function ejecutarAccionGesto(gesto) {
  const ahora = Date.now();
  if (ahora - lastGestureTime < GESTURE_COOLDOWN) {
    return; // Ignora gestos dentro del periodo de cooldown
  }
  lastGestureTime = ahora;
  // ... ejecutar acción
}
```

#### Error 2: No cancelar síntesis de voz anterior
**Problema:** Si se ejecutan múltiples comandos rápidamente, las voces se solapan creando confusión.

**Solución implementada:** Cancelar síntesis anterior antes de iniciar nueva.
```javascript
function hablar(texto) {
  const utterance = new SpeechSynthesisUtterance(texto);
  speechSynthesis.cancel(); // ⬅️ CRÍTICO: Cancela reproducción anterior
  speechSynthesis.speak(utterance);
}
```

#### Error 3: Voces no cargadas al inicio
**Problema:** `speechSynthesis.getVoices()` devuelve array vacío si se llama antes de que el navegador cargue las voces del sistema.

**Solución implementada:** Escuchar evento `onvoiceschanged`.
```javascript
function cargarVoces() {
  voices = speechSynthesis.getVoices();
}

cargarVoces(); // Llamada inicial
speechSynthesis.onvoiceschanged = cargarVoces; // Recarga cuando estén disponibles
```

#### Error 4: Detección incorrecta con mala iluminación
**Problema:** MediaPipe requiere buena iluminación para detectar landmarks con precisión.

**Solución implementada:** Aumentar umbral de confianza.
```javascript
hands.setOptions({
  minDetectionConfidence: 0.7, // 70% de confianza mínima
  minTrackingConfidence: 0.7
});
```

**Recomendación adicional:** Mostrar feedback al usuario cuando no se detecta la mano:
```javascript
if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
  // ... procesar gestos
} else {
  document.getElementById("statusGestos").textContent = "👋 Muestra tu mano a la cámara...";
}
```

#### Error 5: No validar entrada vacía
**Problema:** Comando "agregar" sin texto crearía tarea sin título.

**Solución implementada:** Validación en la función.
```javascript
function agregarTarea(titulo) {
  if (!titulo || titulo.trim() === '') {
    hablar("No puedo agregar una tarea vacía");
    return; // Sale sin modificar el estado
  }
  // ... resto del código
}
```

#### Error 6: Coordenadas Y invertidas en canvas
**Problema:** En HTML canvas, Y aumenta hacia abajo, contrario a la intuición matemática.

**Solución:** Comparar `punta.y < base.y` para detectar dedo extendido (hacia arriba).
```javascript
function dedoExtendido(punta, base) {
  return punta.y < base.y; // Menor Y = más arriba en canvas
}
```

### Pruebas de funcionamiento

He realizado pruebas exhaustivas de todos los comandos:

| Comando de Voz | Entrada Ejemplo | Resultado Esperado | Estado |
|----------------|-----------------|-------------------|--------|
| Agregar tarea | "agregar comprar leche" | Tarea creada con ID único | ✅ OK |
| Sinónimo agregar | "añadir hacer ejercicio" | Mismo comportamiento | ✅ OK |
| Eliminar por índice | "eliminar dos" | Elimina tareas[2] | ✅ OK |
| Eliminar con número | "borrar 0" | Elimina tareas[0] | ✅ OK |
| Completar tarea | "completar tres" | Marca tareas[3] como completada | ✅ OK |
| Leer tareas | "leer tareas" | Lee todas las tareas por voz | ✅ OK |
| Limpiar todo | "limpiar todo" | Vacía array de tareas | ✅ OK |

| Gesto | Descripción | Resultado Esperado | Estado |
|-------|-------------|-------------------|--------|
| ✌️ Dos dedos | Índice y medio extendidos | Agrega tarea aleatoria | ✅ OK |
| 👍 Pulgar arriba | Solo pulgar extendido | Completa primera tarea pendiente | ✅ OK |
| ✊ Puño cerrado | Todos los dedos cerrados | Elimina última tarea | ✅ OK |
| 🖐️ Mano abierta | 4+ dedos extendidos | Lee tareas por voz | ✅ OK |

---

## Conclusión

He implementado con éxito un sistema de gestión de tareas que demuestra la viabilidad de aplicaciones web funcionales mediante interfaces naturales (voz y gestos), sin depender de teclado o ratón. El proyecto integra **Web Speech API** para reconocimiento de voz y síntesis, junto con **MediaPipe Hands** para detección de gestos mediante visión por computador.

Los logros principales incluyen: arquitectura basada en eventos, sistema de cooldown para evitar activaciones múltiples, validación de entradas, diseño profesional con glassmorphism, y procesamiento eficiente de 30 FPS sin bloquear el hilo principal.

Este proyecto conecta con contenidos del módulo: patrones Modelo-Vista y gestión de eventos (Unidad 1), implementación de interfaces naturales con ML (Unidad 2), modularización funcional (Unidad 3), principios de usabilidad y accesibilidad (Unidad 4), y pruebas documentadas (Unidad 8).

El aprendizaje clave ha sido comprender que MediaPipe permite ejecutar ML complejo en el navegador sin servidores especializados, y que la tolerancia a fallos es crítica en aplicaciones donde las condiciones ambientales varían. Este proyecto sirve de base para ampliaciones futuras como persistencia de datos, más gestos, o interfaces multimodales.
