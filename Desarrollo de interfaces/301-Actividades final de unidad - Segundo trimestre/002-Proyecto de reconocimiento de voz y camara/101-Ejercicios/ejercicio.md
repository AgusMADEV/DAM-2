# 🎯 Proyecto de Interfaces Naturales: Sistema de Gestión con Voz y Gestos

## 📋 Descripción del Proyecto

Este proyecto implementa un sistema completo de gestión de tareas utilizando **interfaces naturales de usuario**, específicamente:
- 🎤 **Reconocimiento de voz** (Web Speech API)
- 🔊 **Síntesis de voz** (Text-to-Speech)
- 👋 **Reconocimiento de gestos de manos** (MediaPipe Hands)

El objetivo es demostrar cómo las tecnologías de interfaces naturales permiten una comunicación más fluida e intuitiva entre el usuario y la aplicación, sin necesidad de usar teclado o ratón.

## 🎓 Conceptos Aplicados

### 1. Web Speech API
- **SpeechRecognition**: Captura y transcribe comandos de voz en español
- **SpeechSynthesis**: Genera respuestas de voz para feedback al usuario
- Procesamiento de lenguaje natural para interpretar comandos

### 2. MediaPipe Hands
- Detección de landmarks (21 puntos) en la mano en tiempo real
- Identificación de gestos mediante análisis de posiciones de dedos
- Ejecución de acciones basadas en gestos detectados

### 3. Arquitectura del Código
- Separación de responsabilidades (datos, interfaz, reconocimiento)
- Sistema de cooldown para evitar detecciones múltiples
- Feedback visual y auditivo en tiempo real

## 🚀 Funcionalidades Implementadas

### Control por Voz 🎤

**Comandos disponibles:**

1. **"agregar [nombre de la tarea]"**
   - Ejemplo: "agregar estudiar para el examen"
   - Añade una nueva tarea a la lista

2. **"eliminar [número]"**
   - Ejemplo: "eliminar dos"
   - Elimina la tarea en la posición indicada
   - Acepta números en texto: cero, uno, dos, tres, etc.

3. **"completar [número]"**
   - Ejemplo: "completar uno"
   - Marca la tarea indicada como completada

4. **"leer tareas"**
   - Lee todas las tareas de la lista con su estado

5. **"limpiar todo"**
   - Elimina todas las tareas de la lista

### Control por Gestos 👋

**Gestos reconocidos:**

1. **✌️ Dos dedos (índice y medio extendidos)**
   - Acción: Añade una tarea aleatoria
   - Útil para pruebas rápidas

2. **👍 Pulgar arriba**
   - Acción: Completa la primera tarea pendiente
   - Feedback visual y auditivo

3. **✊ Puño cerrado**
   - Acción: Elimina la última tarea de la lista
   - Confirma acción por voz

4. **🖐️ Mano abierta (4+ dedos extendidos)**
   - Acción: Lee todas las tareas por voz
   - Equivalente al comando "leer tareas"

## 🛠️ Tecnologías Utilizadas

### APIs del Navegador
- **Web Speech API**: Reconocimiento y síntesis de voz
- **MediaStream API**: Acceso a la cámara web
- **Canvas API**: Renderizado de landmarks de la mano

### Bibliotecas Externas
```html
<!-- MediaPipe Hands -->
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/drawing_utils/drawing_utils.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js"></script>
```

### Lenguajes
- **HTML5**: Estructura semántica
- **CSS3**: Diseño responsive con gradientes y animaciones
- **JavaScript ES6+**: Lógica de la aplicación

## 📁 Estructura del Código

### 1. Gestión de Datos
```javascript
let tareas = [
  {"id": 1, "titulo": "...", "completada": false}
];
```
- Array de objetos para almacenar tareas
- Cada tarea tiene ID único, título y estado

### 2. Funciones Principales

#### `pintaTabla()`
Renderiza la tabla HTML con todas las tareas y su estado

#### `agregarTarea(titulo)`
Añade nueva tarea al array y actualiza la vista

#### `eliminarTarea(indice)`
Elimina tarea por índice y proporciona feedback

#### `completarTarea(indice)`
Marca tarea como completada

#### `leerTodasLasTareas()`
Genera mensaje de voz con todas las tareas

### 3. Reconocimiento de Voz

```javascript
const reconocimiento = new SpeechRecognition();
reconocimiento.lang = "es-ES";
reconocimiento.onresult = function(event) {
  const texto = event.results[0][0].transcript;
  procesarComandoVoz(texto);
};
```

### 4. Síntesis de Voz

```javascript
function hablar(texto) {
  const utterance = new SpeechSynthesisUtterance(texto);
  utterance.lang = 'es-ES';
  speechSynthesis.speak(utterance);
}
```

### 5. Detección de Gestos

```javascript
function detectarGesto(landmarks) {
  // Análisis de posiciones de dedos
  // Retorna tipo de gesto reconocido
}
```

## 🎨 Diseño Visual

### Características del Diseño
- **Gradiente moderno**: De violeta a morado
- **Layout responsive**: Grid que se adapta a pantallas pequeñas
- **Animaciones**: Efecto pulse en botón de escucha
- **Feedback visual**: Estados de escucha y detección de gestos
- **Glassmorphism**: Paneles con transparencia y blur

### Paleta de Colores
- Principal: `#667eea` (azul violeta)
- Secundario: `#764ba2` (morado)
- Fondo: Gradiente lineal
- Texto: `#333` sobre fondos claros

## 🧪 Cómo Usar la Aplicación

### Requisitos
- Navegador moderno (Chrome, Edge, Safari recomendados)
- Cámara web funcional
- Micrófono
- Permisos de navegador para cámara y micrófono

### Pasos de Uso

1. **Abrir el archivo HTML** en un navegador
2. **Conceder permisos** de cámara y micrófono
3. **Para usar voz:**
   - Pulsar el botón "🎙️ Escuchar Comando"
   - Decir el comando claramente
   - Esperar el feedback visual y auditivo
4. **Para usar gestos:**
   - Colocar la mano frente a la cámara
   - Hacer el gesto deseado
   - Mantenerlo 1-2 segundos
   - Esperar el cooldown (2 segundos) antes del siguiente gesto

## 🔧 Configuración y Personalización

### Ajustar Sensibilidad de Gestos
```javascript
hands.setOptions({
  maxNumHands: 1,
  modelComplexity: 1,
  minDetectionConfidence: 0.7,  // Ajustar 0.5-0.9
  minTrackingConfidence: 0.7    // Ajustar 0.5-0.9
});
```

### Modificar Cooldown de Gestos
```javascript
const GESTURE_COOLDOWN = 2000; // Milisegundos
```

### Añadir Nuevos Gestos
```javascript
function detectarGesto(landmarks) {
  // Añadir lógica de detección
  if (/* condición */) {
    return "nuevo_gesto";
  }
}
```

## 📊 Diferencias con el Ejercicio de Clase

### Mejoras Implementadas

1. **Interfaz más completa:**
   - Diseño visual profesional
   - Dos paneles coordinados
   - Feedback visual en tiempo real

2. **Más funcionalidades:**
   - Sistema de tareas con estado (completada/pendiente)
   - Gestos adicionales (4 tipos vs 2 en clase)
   - Tareas aleatorias para pruebas

3. **Mejor experiencia de usuario:**
   - Sistema de cooldown para gestos
   - Confirmación de acciones
   - Mensajes de estado descriptivos
   - Instrucciones visuales

4. **Código más robusto:**
   - Manejo de errores
   - Validación de datos
   - Separación de responsabilidades
   - Comentarios exhaustivos

5. **Integración completa:**
   - Voz + Gestos trabajando juntos
   - Feedback multimodal (visual + auditivo)
   - Estado sincronizado en tiempo real

## 🎯 Objetivos de Aprendizaje Cumplidos

✅ Implementación de reconocimiento de voz en español  
✅ Uso de síntesis de voz para feedback  
✅ Integración de MediaPipe para reconocimiento de gestos  
✅ Procesamiento de comandos de lenguaje natural  
✅ Diseño de interfaz responsive y moderna  
✅ Gestión de estado de aplicación  
✅ Sincronización de múltiples fuentes de entrada  
✅ Feedback multimodal (visual + auditivo)  

## 🚀 Posibles Extensiones

### Ideas para Mejorar el Proyecto

1. **Persistencia de datos:**
   - Guardar tareas en localStorage
   - Sincronización con backend

2. **Más gestos:**
   - Números con dedos para seleccionar tareas
   - Gestos de deslizamiento
   - Reconocimiento de posición de la mano

3. **Reconocimiento facial:**
   - Integrar MediaPipe Face Mesh
   - Expresiones faciales como comandos
   - Detección de atención del usuario

4. **Mejoras de voz:**
   - Comandos más complejos
   - Conversación natural
   - Múltiples idiomas

5. **Gamificación:**
   - Puntos por tareas completadas
   - Racha de días activos
   - Logros y recompensas

## 📝 Conclusiones

Este proyecto demuestra cómo las **interfaces naturales de usuario** pueden crear experiencias más intuitivas y accesibles. La combinación de voz y gestos permite múltiples formas de interacción, adaptándose a diferentes contextos y preferencias del usuario.

Las tecnologías utilizadas (Web Speech API y MediaPipe) son suficientemente maduras para aplicaciones en producción, y el navegador las soporta nativamente sin necesidad de instalaciones adicionales.

El resultado es una aplicación funcional, moderna y extensible que cumple con los objetivos del proyecto de interfaces naturales.

---

**Autor:** [Tu Nombre]  
**Fecha:** Febrero 2026  
**Asignatura:** Desarrollo de Interfaces - DAM 2  
**Proyecto:** Interfaces Naturales de Usuario
