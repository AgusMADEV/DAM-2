# 🚨 SecurePath - Sistema de Entrenamiento de Evacuación

**Serious Game - Simulación Empresarial de Seguridad con IA**

![Estado](https://img.shields.io/badge/Estado-Funcional-success)
![Tecnología](https://img.shields.io/badge/Three.js-r128-blue)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hands-orange)
![Algoritmo](https://img.shields.io/badge/IA-Genético-purple)

---

## 📋 Descripción del Proyecto

Sistema interactivo de simulación de evacuaciones de emergencia que combina:
- ✅ **Visualización 3D** de edificios con Three.js
- ✅ **Control por gestos** mediante webcam y MediaPipe Hands
- ✅ **Algoritmo genético** para optimizar rutas de evacuación
- ✅ **Análisis de datos** con heat maps y estadísticas en tiempo real

### 🎯 Objetivo

Ayudar a empresas y organizaciones a:
1. Simular evacuaciones de emergencia
2. Identificar cuellos de botella y zonas de congestión
3. Optimizar la ubicación de salidas de emergencia
4. Entrenar al personal mediante visualización interactiva

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Uso | Versión |
|------------|-----|---------|
| **Three.js** | Motor 3D para renderizar edificio y personas | r128 |
| **MediaPipe Hands** | Detección de manos en tiempo real | Latest |
| **Canvas API** | Overlay de heat maps y visualización de manos | HTML5 |
| **Algoritmo Genético** | Optimización de comportamientos de evacuación | Custom |

---

## 🚀 Cómo Usar

### 1. Abrir el Proyecto

Simplemente abre el archivo `index.html` en un navegador moderno:
```bash
# Opción 1: Doble clic en index.html

# Opción 2: Usar un servidor local (recomendado)
python -m http.server 8000
# Luego abre http://localhost:8000
```

### 2. Conceder Permisos de Webcam

Al abrir la aplicación, el navegador pedirá permiso para acceder a la webcam. **Acepta** para habilitar el control por gestos.

### 3. Controles por Gestos

| Gesto | Acción | Descripción |
|-------|--------|-------------|
| ✋ **Una mano abierta** | Pan (Desplazar) | Mueve la mano para desplazar la cámara lateralmente |
| 🤏 **Pinch (índice + pulgar)** | Rotación | Junta índice y pulgar y mueve para rotar la cámara |
| ✌️ **Dos manos abiertas** | Zoom | Separa/junta las manos para hacer zoom in/out |

### 4. Panel de Configuración

**Sliders disponibles:**
- 👥 **Número de personas**: 10-200 (ajusta la cantidad de evacuados)
- 🚪 **Número de salidas**: 1-6 (modifica salidas de emergencia)
- ⚡ **Velocidad de evolución**: 1-10 (rapidez del algoritmo genético)

**Botones:**
- ▶️ **Iniciar Simulación**: Comienza la evacuación
- 🔄 **Reiniciar**: Limpia la simulación y vuelve al estado inicial
- 🔥 **Mapa de Calor**: Activa/desactiva visualización de densidad

---

## 🧬 Algoritmo Genético

### Funcionamiento

El sistema usa un algoritmo genético para **evolucionar comportamientos óptimos de evacuación**:

1. **Población inicial**: Cada persona tiene genes aleatorios:
   - `followCrowd`: Tendencia a seguir a otros
   - `seekNearestExit`: Preferencia por la salida más cercana
   - `avoidCrowds`: Evitar aglomeraciones
   - `panicThreshold`: Nivel de pánico que afecta decisiones

2. **Evaluación (Fitness)**: Se mide el tiempo de evacuación de cada persona

3. **Selección**: Los individuos que evacuan más rápido tienen mayor probabilidad de reproducirse

4. **Cruce (Crossover)**: Dos padres combinan sus genes para crear hijos

5. **Mutación**: Pequeños cambios aleatorios (15%) para explorar nuevas soluciones

6. **Elitismo**: Los mejores 20% pasan sin cambios a la siguiente generación

### Evolución Visible

A medida que avanzan las generaciones, verás:
- ⏱️ **Tiempos de evacuación decrecientes**
- 📊 **Mejora en el promedio general**
- 🎯 **Convergencia hacia comportamientos óptimos**

---

## 📊 Visualización de Datos

### Panel Superior (Estadísticas)
- **Personas evacuadas**: Contador en tiempo real
- **Tiempo promedio**: Media de evacuación de la generación actual
- **Generación**: Número de iteración del algoritmo genético

### Mapa de Calor (Heatmap)
Actívalo con el botón 🔥. Muestra:
- 🟢 **Verde**: Baja densidad
- 🟡 **Amarillo**: Densidad media
- 🔴 **Rojo**: Alta densidad (zonas congestionadas)

**Uso empresarial**: Identificar dónde se forman cuellos de botella y ajustar salidas.

---

## 🏢 Estructura del Edificio

El edificio generado automáticamente incluye:
- 📦 **Planta rectangular**: 40m x 30m
- 🚪 **Salidas configurables**: 1-6 salidas en diferentes paredes
- 🧱 **Obstáculos internos**: Paredes divisorias y columnas
- 💡 **Iluminación de emergencia**: Luces rojas parpadeantes
- 🟢 **Señalización de salidas**: Luces verdes y carteles rojos

---

## 🎮 Características Técnicas

### Renderizado 3D
- **Sombras dinámicas** para realismo
- **Niebla atmosférica** para profundidad
- **60 FPS** con `requestAnimationFrame`
- **Responsive** a diferentes resoluciones

### Simulación Física
- **Pathfinding** hacia salidas
- **Velocidad variable** (2-4 m/s por persona)
- **Animación de caminar** (bobbing)
- **Rotación direccional** según movimiento

### Detección de Gestos
- **21 landmarks** por mano (MediaPipe)
- **Detección en tiempo real** a 30 FPS
- **Skeleton overlay** en canvas
- **Feedback visual** del gesto activo

---

## 📁 Estructura de Archivos

```
002-Proyecto serious games/
└── 101-Ejercicios/
    ├── index.html              # Página principal
    ├── styles.css              # Estilos y diseño UI
    ├── README.md               # Esta documentación
    └── scripts/
        ├── main.js             # Bucle principal y orquestación
        ├── building.js         # Generación del edificio 3D
        ├── person.js           # Clase de persona evacuando
        ├── genetic-algorithm.js # Implementación del AG
        └── hand-controls.js    # Control por gestos MediaPipe
```

---

## 🔧 Requisitos del Sistema

- ✅ Navegador moderno (Chrome 90+, Firefox 88+, Edge 90+)
- ✅ Webcam funcional
- ✅ GPU con soporte WebGL
- ✅ Conexión a internet (para CDNs de librerías)

**Recomendado:**
- 💻 Pantalla de al menos 1366x768
- 🎥 Webcam HD (720p o superior)
- 🖱️ No se requiere mouse (control por gestos)

---

## 🎓 Aplicaciones Educativas y Empresariales

### 1. Entrenamiento de Personal
- Visualizar rutas de evacuación antes de emergencias reales
- Practicar procedimientos sin riesgo

### 2. Planificación Arquitectónica
- Probar diferentes configuraciones de salidas
- Validar normativas de seguridad

### 3. Análisis de Capacidad
- Determinar tiempo máximo de evacuación
- Calcular número óptimo de salidas por ocupantes

### 4. Investigación en IA
- Estudiar algoritmos genéticos en acción
- Comparar diferentes estrategias de selección

---

## 📝 Criterios de Evaluación Cumplidos

### ✅ Modificaciones Estéticas y Visuales
- Interfaz moderna con glassmorphism
- Gradientes y sombras profesionales
- Iconos emoji para UX intuitiva
- Animaciones suaves (transiciones CSS)
- Responsive design
- Feedback visual en tiempo real

### ✅ Modificaciones Funcionales de Calado
- **Algoritmo genético completo** (selección, cruce, mutación, elitismo)
- **Detección de gestos con IA** (MediaPipe Hands)
- **Simulación física realista** (pathfinding, velocidades variables)
- **Sistema de datos en tiempo real** (heat maps, estadísticas)
- **Arquitectura modular** (5 archivos JS separados)
- **Optimización de rendimiento** (requestAnimationFrame, canvas textures)

---

## 🚧 Posibles Mejoras Futuras

1. **Exportar datos**: Guardar estadísticas en CSV/JSON
2. **Importar planos**: Cargar edificios desde archivos
3. **Modo multijugador**: Colaboración en tiempo real
4. **VR/AR**: Inmersión con WebXR
5. **Reconocimiento de voz**: Comandos hablados
6. **Base de datos**: Historial de simulaciones
7. **Patrones de multitudes**: Efectos de empuje, pánico en grupo
8. **Edificios multi-piso**: Escaleras y ascensores

---

## 👨‍💻 Autor

Proyecto desarrollado para la asignatura **Programación Multimedia y Dispositivos Móviles**.

**Fecha**: Marzo 2026  
**Categoría**: Actividad Final de Unidad - Segundo Trimestre  
**Tipo**: Serious Game - Aplicación Empresarial

---

## 📖 Referencias y Bibliotecas

- [Three.js Documentation](https://threejs.org/docs/)
- [MediaPipe Hands](https://google.github.io/mediapipe/solutions/hands.html)
- [Algoritmos Genéticos - Wikipedia](https://es.wikipedia.org/wiki/Algoritmo_gen%C3%A9tico)
- [WebGL Fundamentals](https://webglfundamentals.org/)

---

## 🎉 ¡Gracias por Probar el Sistema!

Si tienes preguntas o sugerencias, consulta los comentarios en el código fuente. Cada archivo tiene documentación detallada.

**¡Feliz Evacuación Virtual! 🏃‍♂️🚪**
