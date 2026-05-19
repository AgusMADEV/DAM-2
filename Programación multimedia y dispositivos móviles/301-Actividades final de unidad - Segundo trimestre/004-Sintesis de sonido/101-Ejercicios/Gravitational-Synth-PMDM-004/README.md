# 🌌 Sintetizador de Partículas Gravitacionales

**Proyecto de síntesis de audio interactiva con física de partículas**

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![Web Audio API](https://img.shields.io/badge/Web_Audio_API-FF6B6B?style=flat-square&logo=html5&logoColor=white)
![Canvas 2D](https://img.shields.io/badge/Canvas_2D-4FC3F7?style=flat-square&logo=html5&logoColor=white)

_PMDM · Actividad 004 — Síntesis de Sonido · DAM2 2025 / 2026_

---

## 📋 Índice

1. [Descripción](#-descripción)
2. [Características](#-características)
3. [Cómo usar](#-cómo-usar)
4. [Controles disponibles](#-controles-disponibles)
5. [Tecnologías utilizadas](#-tecnologías-utilizadas)
6. [Modo de creación](#-modos-de-creación)
7. [Fundamento didáctico](#-fundamento-didáctico)
8. [Instalación](#-instalación)

---

## 🎯 Descripción

**Sintetizador de Partículas Gravitacionales** es una aplicación web interactiva que combina física de partículas, generación sintética de sonido y visualización en tiempo real. 

El proyecto permite al usuario crear partículas que:
- Se mueven con física realista (gravedad, colisiones, fricción)
- Generan notas musicales al colisionar entre sí y con los bordes
- Tienen diferentes propiedades visuales según la nota asignada
- Crean efectos visuales de rastro y brillo

Es una evolución creativa de los ejercicios de clase sobre síntesis de audio y animación, llevando el concepto de "pelotas rebotando en círculos" a un sistema de partículas más complejo y personalizable.

---

## ✨ Características

### 🎵 Síntesis de Audio
- **Web Audio API nativa** para generación de sonido en tiempo real
- **4 tipos de osciladores**: Sine, Triangle, Sawtooth, Square
- **25 notas disponibles** (C4 a C6 - 2 octavas completas)
- **Envelope ADSR simple** para dar forma a cada nota
- **Control de volumen maestro** y duración de notas
- **Efecto de reverb** ajustable
### 🎹 Secuenciador 16-Step
- **Grid interactivo** de 16 columnas × 7 filas (notas C5 a D4)
- **Reproducción sincronizada** con BPM ajustable (60-220)
- **Controles Play/Stop/Clear** para el secuenciador
- **Resaltado visual** de la columna activa durante playback
- **Integración completa** con el motor de síntesis de audio existente
- **Patrones editables** click para activar/desactivar celdas
### ⚛️ Motor de Física
- **Gravedad configurable** con toggle ON/OFF
- **Colisiones realistas** entre partículas usando impulsos
- **Conservación de momento** basado en masa
- **Rebote con pérdida de energía** (restitución 0.95)
- **Fricción aérea** para simulación realista

### 🎨 Visualización
- **Efectos de rastro** (trail) para cada partícula
- **Gradientes radiales** con glow effect
- **Colores únicos** para cada nota musical (25 colores)
- **Animación fluida** a 60 FPS
- **Estadísticas en tiempo real** (partículas, colisiones, notas)

### 🎮 Modos de Creación
1. **Partícula Individual** - Click para crear una partícula con dirección aleatoria
2. **Explosión (Burst)** - Crea 5 partículas en formación radial con notas aleatorias
3. **Fuente Continua** - Genera partículas automáticamente durante 2 segundos
4. **Sistema Orbital** - Crea un sistema planetario musical con órbitas

---

## 🚀 Cómo usar

### Inicio rápido
1. Abre `index.html` en un navegador moderno (Chrome, Firefox, Edge)
2. Haz click en **"🔊 Activar Audio"** (requerido por políticas de navegadores)
3. Haz click en el canvas para crear partículas
4. Las partículas colisionarán y generarán música

### Tips de uso
- Cambia la **nota musical** antes de crear partículas para asignarles diferentes frecuencias
- Usa el modo **"Explosión"** para crear patrones simétricos rápidamente
- El modo **"Sistema Orbital"** crea estructuras complejas automáticamente
- Juega con el **tipo de oscilador** para cambiar el timbre del sonido
- Desactiva la **gravedad** para crear patrones más caóticos
- Aumenta la **masa** de las partículas para colisiones más dramáticas
- Crea **patrones rítmicos** con el secuenciador 16-step mientras las partículas generan melodías aleatorias
- Combina **múltiples modos**: secuenciador para ritmo base + partículas para variación

---

## 🎛️ Controles disponibles

### Barra Superior
| Control | Función |
|---------|---------|
| 🔊 Activar Audio | Inicializa el contexto de audio (obligatorio) |
| 🗑️ Limpiar Todo | Elimina todas las partículas y resetea estadísticas |
| 🌍 Gravedad | Activa/desactiva la gravedad global |

### Panel de Control

#### 🎨 Modo de Creación
- **Partícula Individual** - Una partícula por click
- **Explosión (5 partículas)** - Patrón radial
- **Fuente Continua** - Generación automática temporal
- **Sistema Orbital** - Estructura compleja pre-diseñada

#### 🎵 Nota Musical
- Selector visual de 12 notas principales (C4 a G5)
- Cada nota tiene un color único asignado
- La nota seleccionada se aplica a las nuevas partículas

#### 🎹 Tipo de Oscilador
- **Sine** - Sonido suave y puro
- **Triangle** - Sonido cálido con armónicos impares
- **Sawtooth** - Sonido brillante y rico en armónicos
- **Square** - Sonido electrónico, agresivo

#### ⚙️ Propiedades Físicas
| Propiedad | Rango | Efecto |
|-----------|-------|--------|
| **Radio** | 5-40 px | Tamaño visual y área de colisión |
| **Velocidad** | 1-15 | Velocidad inicial al crear |
| **Masa** | 0.5-5.0 | Afecta las colisiones (mayor masa = menos afectada) |
| **Gravedad** | 0-1.0 | Intensidad de la aceleración hacia abajo |

#### 🎚️ Audio
| Control | Rango | Función |
|---------|-------|---------|
| **Volumen Principal** | 0-100% | Volumen global de salida |
| **Duración Nota** | 50-1000 ms | Cuánto dura cada nota al colisionar |
| **Reverb** | 0-100% | Cantidad de reverberación |

#### 🎹 Secuenciador 16-Step
| Control | Función |
|---------|----------|
| **▶️ Play** | Inicia la reproducción del patrón |
| **⏸️ Stop** | Detiene la reproducción |
| **🗑️ Clear** | Borra todo el patrón del grid |
| **BPM Slider** | Ajusta el tempo (60-220 BPM) |
| **Grid Cells** | Click para activar/desactivar notas en cada paso |

**Notas disponibles en el secuenciador:**
- C5, B4, A4, G4, F4, E4, D4 (7 notas en total)
- 16 pasos por patrón (1 compas de 4/4 en semicorcheas)
- Resaltado amarillo indica la columna actual durante playback
- Resaltado naranja indica notas activas siendo reproducidas

---

## 🛠️ Tecnologías utilizadas

### APIs Web
- **Web Audio API** - Síntesis de audio en tiempo real
  - `AudioContext` para el contexto de audio
  - `OscillatorNode` para generar ondas sonoras
  - `GainNode` para control de volumen y envelopes
  - Modulación de frecuencia y ADSR básico

- **Canvas 2D API** - Renderizado de gráficos
  - Gradientes radiales para efectos de luz
  - Composición alfa para efectos de rastro
  - Shadow blur para efectos de brillo

### JavaScript Moderno (ES6+)
- Clases ES6 para el sistema de partículas
- Arrow functions y template literals
- Destructuring y spread operators
- Map y Set para colecciones

### CSS3
- Gradientes lineales para el fondo
- Backdrop filter para efectos de vidrio esmerilado
- Flexbox y Grid para layout responsive
- Animaciones CSS (@keyframes)

---

## 🎨 Modos de Creación

### 1. Partícula Individual
```javascript
// Crea una partícula en la posición del click
// con velocidad aleatoria en cualquier dirección
const angle = Math.random() * Math.PI * 2;
const vx = Math.cos(angle) * velocity;
const vy = Math.sin(angle) * velocity;
```

### 2. Explosión (Burst)
```javascript
// Distribuye 5 partículas en círculo perfecto
// Cada una con nota aleatoria
for (let i = 0; i < 5; i++) {
    const angle = (Math.PI * 2 / 5) * i;
    // Velocidad radial desde el centro
}
```

### 3. Fuente Continua
```javascript
// Genera partículas cada 100ms durante 2 segundos
// Velocidad vertical negativa (hacia arriba)
// Velocidad horizontal aleatoria
```

### 4. Sistema Orbital
```javascript
// Crea un "sol" central masivo
// 3 órbitas con 4 "planetas" cada una
// Cada órbita tiene diferente radio y velocidad
// Velocidad tangencial para órbita estable
```

---

## 📚 Fundamento didáctico

Este proyecto se basa en los ejercicios vistos en la **Unidad 003 - Utilización de librerías multimedia integradas**, específicamente:

### Ejercicio base: `006-audio buffer.html`
- **Concepto original**: Pelotas que rebotan dentro de un círculo dividido en arcos
- **Mecánica**: Cada arco representa una nota, al colisionar con él se reproduce
- **Evolución aplicada**:
  - ✅ De círculo segmentado → Sistema de partículas libre
  - ✅ De colisión con arcos → Colisiones inter-partículas
  - ✅ De 7 notas fijas → 25 notas seleccionables
  - ✅ De physics básico → Motor completo con masa y gravedad

### Ejercicio complementario: `002-pentagrama.html`
- **Concepto**: Editor de notas musicales con reproducción
- **Aspectos incorporados**:
  - Sistema de notas organizado (escala cromática)
  - Control de duración de las notas
  - Interfaz de selección visual

### Modificaciones estéticas (Criterio 1)
- ✨ Diseño moderno tipo "dashboard" con glassmorphism
- ✨ Paleta de 25 colores única para cada nota
- ✨ Efectos visuales: trails, glows, gradientes radiales
- ✨ Animaciones CSS en botones y controles
- ✨ Layout responsive con sidebar de controles
- ✨ Estadísticas en tiempo real en overlay

### Modificaciones funcionales (Criterio 2)
- 🔧 **Motor de física completo**: gravedad, masa, impulsos
- 🔧 **4 modos de creación** vs 1 modo original
- 🔧 **Sistema de colisiones inter-partículas** (no solo con bordes)
- 🔧 **25 notas** (2 octavas) vs 7 notas originales
- 🔧 **4 tipos de osciladores** con cambio en tiempo real
- 🔧 **Controles avanzados**: reverb, ADSR, mass, velocity
- 🔧 **Sistema orbital** con matemática de velocidad tangencial
- 🔧 **Trail system** con buffer circular para cada partícula

---

## 🎓 Conceptos técnicos aplicados

### Física de partículas
#### Colisiones elásticas con conservación de momento
```javascript
// Impulse-based collision resolution
const impulse = (2 * dvn) / (mass1 + mass2);
v1 += impulse * mass2 * normal * restitution;
v2 -= impulse * mass1 * normal * restitution;
```

#### Separación de partículas solapadas
```javascript
const overlap = r1 + r2 - distance;
const separation = (overlap / 2) * normalVector;
```

### Síntesis de audio
#### Envelope ADSR simplificado
```javascript
gain.setValueAtTime(0, t0);
gain.linearRampToValueAtTime(1.0, t0 + attack);
gain.exponentialRampToValueAtTime(sustain, t0 + attack + decay);
```

#### Reverberación con GainNode
```javascript
// Señal seca + señal húmeda
oscillator → envelope → [masterGain → destination]
                         └→ [reverbGain → destination]
```

### Renderizado optimizado
#### Trail con alpha compositing
```javascript
ctx.fillStyle = 'rgba(102, 126, 234, 0.1)'; // Fade suave
// En lugar de clearRect completo
```

#### Gradient radial para efectos de luz
```javascript
const gradient = ctx.createRadialGradient(
    x - r/3, y - r/3, 0,  // Punto de luz off-center
    x, y, r                // Círculo exterior
);
gradient.addColorStop(0, 'white');
gradient.addColorStop(0.4, color);
```

---

## 💾 Instalación

### Opción 1: Servidor local simple
```bash
# Python 3
python -m http.server 8000

# Node.js
npx http-server -p 8000

# PHP
php -S localhost:8000
```

Luego abre: `http://localhost:8000`

### Opción 2: Abrir directamente
Simplemente abre `index.html` en tu navegador. La aplicación es 100% client-side y no requiere servidor.

> **Nota**: Algunos navegadores pueden bloquear AudioContext si se abre desde `file://`. En ese caso usa un servidor local.

---

## 📂 Estructura del proyecto

```
Gravitational-Synth-PMDM-004/
│
├── index.html          # Aplicación completa (HTML + CSS + JS)
├── README.md           # Esta documentación
└── docs/
    └── Actividad_SintesisSonido.md  # Documento de entrega académica
```

---

## 🎯 Criterios de evaluación cumplidos

### ✅ Criterio 1: Modificaciones estéticas y visuales
- [x] Interfaz moderna con glassmorphism y gradientes
- [x] 25 colores únicos para las notas
- [x] Efectos visuales: trails, glows, shadows
- [x] Animaciones en controles interactivos
- [x] Layout profesional con sidebar
- [x] Estadísticas visuales en tiempo real

### ✅ Criterio 2: Modificaciones funcionales de calado
- [x] Motor de física con colisiones realistas
- [x] 4 modos de creación diferentes
- [x] Sistema de masas y gravedad configurable
- [x] 25 notas vs 7 del original (expansión de 250%)
- [x] 4 tipos de osciladores intercambiables
- [x] Sistema orbital con matemática avanzada
- [x] Trail system con buffer circular
- [x] Controles de audio avanzados (reverb, ADSR)

### ✅ Base didáctica respetada
- [x] Parte del concepto de pelotas rebotando
- [x] Mantiene la generación sintética de sonido
- [x] Incorpora conceptos del editor de partituras
- [x] Expande y mejora los conceptos base

---

## 🧑‍💻 Autor

**Proyecto desarrollado como actividad académica**

- **Asignatura**: Programación multimedia y dispositivos móviles
- **Curso**: DAM2 - 2025/2026
- **Unidad**: 301 - Actividades final de unidad - Segundo trimestre
- **Actividad**: 004 - Síntesis de sonido

---

## 📄 Licencia

Este proyecto es de uso educativo. Desarrollado como parte del currículum de DAM (Desarrollo de Aplicaciones Multiplataforma).

---

## 🙏 Agradecimientos

Basado en los ejercicios de clase:
- `006-audio buffer.html` - Concepto de pelotas musicales
- `002-pentagrama.html` - Sistema de notas musicales
- Web Audio API - MDN Documentation
- Canvas 2D - HTML5 specification

---

**¿Preguntas o mejoras?** Este proyecto es evolutivo y acepta sugerencias de mejora. 🚀
