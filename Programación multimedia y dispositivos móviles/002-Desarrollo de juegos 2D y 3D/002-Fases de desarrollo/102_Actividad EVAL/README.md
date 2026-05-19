# 🎮 Actividad Evaluable: Sistema de Partículas con Interacciones

## 📖 Descripción General

Esta actividad desarrolla un **sistema completo de partículas interactivas** que simula comportamientos de agrupamiento basados en la física computacional. Las partículas se atraen o repelen según sus atributos, formando grupos de manera emergente sin programación explícita de esos grupos.

### 🎯 Objetivos de Aprendizaje

- ✅ Implementar sistemas de fuerzas físicas (atracción/repulsión)
- ✅ Aplicar integración numérica de ecuaciones de movimiento
- ✅ Desarrollar algoritmos de detección de proximidad
- ✅ Optimizar código para sistemas con muchas entidades
- ✅ Visualizar en tiempo real sistemas complejos

---

## 📁 Estructura del Proyecto

```
102_Actividad EVAL/
│
├── 📄 README.md (este archivo)
│   └─ Punto de entrada y índice de la actividad
│
├── 🌐 actividad-particulas-interactivas.html
│   └─ Aplicación principal interactiva (ABRIR ESTE ARCHIVO)
│
├── 📚 DOCUMENTACION-Y-REFLEXION.md
│   ├─ Fundamentos teóricos
│   ├─ Explicación detallada del algoritmo
│   ├─ Análisis de cada función clave
│   ├─ Optimizaciones implementadas
│   └─ Reflexión sobre conceptos aprendidos
│
└── 🧪 GUIA-EXPERIMENTACION.md
    ├─ 15 ejercicios prácticos
    ├─ Desde básicos hasta avanzados
    ├─ Modificaciones sugeridas
    └─ Proyecto final integrador
```

---

## 🚀 Inicio Rápido

### Paso 1: Ejecutar la Aplicación

1. Abre el archivo `actividad-particulas-interactivas.html` en tu navegador web
2. Observa cómo las partículas se mueven y se agrupan
3. Usa los controles del panel superior:
   - **⏯ Pausar/Reanudar**: Detiene/continúa la simulación
   - **🔄 Reiniciar**: Vuelve al estado inicial

### Paso 2: Entender el Código

1. Abre el archivo HTML en tu editor de código
2. Lee los comentarios extensivos que explican cada sección
3. Consulta `DOCUMENTACION-Y-REFLEXION.md` para la teoría

### Paso 3: Experimentar

1. Consulta `GUIA-EXPERIMENTACION.md`
2. Prueba las modificaciones sugeridas
3. Observa cómo cambia el comportamiento
4. Documenta tus descubrimientos

---

## 🎨 Características Implementadas

### ✨ Sistema de Física

- **Fuerzas tipo muelle**: Entre partículas del mismo tipo
- **Repulsión suave**: Entre partículas diferentes
- **Repulsión de seguridad**: Evita solapamiento
- **Fricción**: Estabiliza el sistema
- **Rebote en paredes**: Con amortiguación

### 🎯 Comportamiento Emergente

- **Agrupamiento automático**: Por similitud de atributos
- **Separación de grupos**: Los diferentes mantienen distancia
- **Estabilización progresiva**: Sistema tiende al equilibrio
- **Optimización dinámica**: Partículas estables dejan de calcular

### 📊 Interfaz y Visualización

- **Panel informativo**: Estadísticas en tiempo real
- **Indicadores visuales**: Color según estado (fijo/móvil)
- **Red de conexiones**: Líneas muestran proximidad
- **Controles interactivos**: Pausa y reinicio

---

## 🔑 Conceptos Clave Implementados

### 1. Física Computacional

```
Sistema de N-cuerpos:
- N = 250 partículas
- Cada una interactúa con todas las demás
- Complejidad: O(N²) por frame
```

### 2. Integración Numérica (Método de Euler)

```javascript
// Actualizar velocidad con aceleración
velocidad = velocidad + aceleración

// Actualizar posición con velocidad
posición = posición + velocidad
```

### 3. Fuerzas Físicas

```
F_muelle = k × (d - d₀)
F_repulsión = k × (d_max - d)
F_fricción = v × 0.93
```

### 4. Algoritmo de Agrupamiento

```
Para cada partícula:
  Para cada otra partícula:
    Si mismo_tipo Y distancia > objetivo:
      → ATRAER
    Si mismo_tipo Y distancia < objetivo:
      → REPELER suavemente
    Si diferente_tipo:
      → REPELER moderadamente
    Si muy_cerca (cualquier tipo):
      → REPELER fuertemente
```

---

## 📚 Guía de Estudio

### Para Principiantes

1. ✅ Lee el código HTML con atención a los comentarios
2. ✅ Consulta `DOCUMENTACION-Y-REFLEXION.md` sección "Introducción Teórica"
3. ✅ Prueba los Ejercicios 1-4 de `GUIA-EXPERIMENTACION.md`
4. ✅ Observa cómo cada parámetro afecta el comportamiento

### Para Nivel Intermedio

1. ✅ Estudia las funciones `interacciones()`, `mueve()` y `rebote()`
2. ✅ Lee la sección "Análisis de Funciones Clave" en la documentación
3. ✅ Completa Ejercicios 5-8
4. ✅ Implementa al menos una mejora visual (colores, tamaños)

### Para Nivel Avanzado

1. ✅ Analiza la complejidad algorítmica del sistema
2. ✅ Implementa Spatial Hashing (Ejercicio 9)
3. ✅ Prueba Verlet Integration (Ejercicio 10)
4. ✅ Añade interacción con mouse (Ejercicio 11)
5. ✅ Mide y compara el rendimiento de optimizaciones
6. ✅ Completa el Proyecto Final (Ejercicio 15)

---

## 🎓 Relación con el Temario

### Programación Multimedia y Dispositivos Móviles

- **Canvas API**: Renderizado 2D en tiempo real
- **requestAnimationFrame**: Animaciones fluidas
- **Event Handling**: Interactividad con el usuario

### Desarrollo de Juegos 2D y 3D

- **Sistemas de Partículas**: Base de efectos visuales
- **Física de Videojuegos**: Detección y respuesta a colisiones
- **Game Loop**: Bucle de actualización y renderizado
- **Optimización**: Técnicas para mejorar rendimiento

### Fases de Desarrollo

- **Diseño**: Planificación de clases y métodos
- **Implementación**: Codificación estructurada
- **Pruebas**: Experimentación con parámetros
- **Optimización**: Mejora del rendimiento
- **Documentación**: Comentarios y guías

---

## 💡 Preguntas Frecuentes

### ¿Por qué las partículas no se agrupan correctamente?

Posibles causas:
- Fricción muy alta → disminuye el movimiento
- Fuerzas muy débiles → aumenta las constantes k
- Distancia objetivo incorrecta → ajusta según el espacio

### ¿Por qué el rendimiento es bajo con muchas partículas?

- El algoritmo es O(N²): cada partícula comprueba todas las demás
- Soluciones:
  - Implementar Spatial Hashing (Ejercicio 9)
  - Sistema de partículas fijas (ya implementado)
  - Limitar rango de interacción

### ¿Cómo añado nuevas características?

1. Identifica dónde debe ir el código (constructor, método específico, bucle)
2. Mantén la estructura existente
3. Añade comentarios explicativos
4. Prueba con valores pequeños primero

### ¿Qué navegador es mejor para ejecutar esto?

- **Recomendado**: Google Chrome, Microsoft Edge (motor Chromium)
- **Alternativo**: Firefox
- Usa las "Developer Tools" (F12) para ver errores y rendimiento

---

## 🔧 Parámetros Principales (para experimentar)

Localiza y modifica estos valores en el código:

```javascript
// Número de entidades
let numeroparticulas = 250;

// Tipos de partículas
let nombres = ['Juan','Julia','Jorge','Jaime','Jose','Julian'];

// Distancias (en píxeles)
let distanciaObjetivo = 120;         // Separación ideal entre iguales
let distanciaMinima = 80;            // Distancia de seguridad
let distanciaRepulsionDistinto = 200; // Rango de repulsión diferentes

// Constantes de fuerza
let kAtraccionIgual = 0.0012;        // Fuerza del "muelle"
let kRepulsionDistinto = 0.001;      // Repulsión suave
let kRepulsionCorta = 0.06;          // Repulsión fuerte cerca

// Fricción
const friccion = 0.93;               // 0.93 = pierde 7% por frame

// Rebote
const reboteFactor = -0.5;           // -0.5 = invierte y reduce a la mitad
```

---

## 📈 Criterios de Evaluación (Referencia)

| Aspecto | Peso | Descripción |
|---------|------|-------------|
| **Comprensión** | 30% | Entendimiento de conceptos físicos y algorítmicos |
| **Implementación** | 25% | Corrección del código, funcionalidad completa |
| **Experimentación** | 20% | Pruebas realizadas, modificaciones exploradas |
| **Documentación** | 15% | Claridad de comentarios y explicaciones |
| **Optimización** | 10% | Mejoras de rendimiento implementadas |

---

## 🌟 Extensiones Sugeridas

Si quieres ir más allá:

1. **Modo 3D**: Usar Three.js para visualización 3D
2. **Diferentes tipos de fuerza**: Magnética, gravitacional, viento
3. **Editor visual**: Interfaz para cambiar parámetros en tiempo real
4. **Guardado de estados**: Exportar/importar configuraciones
5. **Simulaciones sociales**: Modelar comportamientos humanos
6. **Integración con datos reales**: Cargar datos desde JSON/API

---

## 📚 Referencias Adicionales

### Matemáticas y Física

- [Vectors in Game Development](https://www.khanacademy.org/computing/computer-programming/programming-natural-simulations/programming-vectors)
- [Numerical Integration Methods](https://en.wikipedia.org/wiki/Numerical_integration)

### Algoritmos

- [Boids Algorithm](https://en.wikipedia.org/wiki/Boids) - Comportamiento de bandadas
- [Spatial Hashing](https://matthias-research.github.io/pages/publications/tetraederCollision.pdf)

### Canvas y JavaScript

- [MDN Canvas Tutorial](https://developer.mozilla.org/es/docs/Web/API/Canvas_API/Tutorial)
- [requestAnimationFrame](https://developer.mozilla.org/es/docs/Web/API/window/requestAnimationFrame)

---

## 👨‍🏫 Información del Curso

**Asignatura**: Programación Multimedia y Dispositivos Móviles  
**Módulo**: Desarrollo de Juegos 2D y 3D  
**Tema**: Fases de Desarrollo  
**Tipo**: Actividad Evaluable  
**Fecha**: Febrero 2026

---

## 📝 Notas Finales

Este proyecto representa la culminación de los conceptos aprendidos en la carpeta `101-Ejercicios`, donde se exploraron progresivamente:

1. ✅ Redes de elementos
2. ✅ Líneas de conexión
3. ✅ Bucles de animación
4. ✅ Movimiento de partículas
5. ✅ Rebote en paredes
6. ✅ Física realista
7. ✅ Velocidades variables
8. ✅ Colores y estilos
9. ✅ Datos estructurados
10. ✅ Agrupamiento con animación
11. ✅ Movimiento inteligente
12. ✅ Búsqueda de estabilidad
13. ✅ **Libertad con criterios → ESTE PROYECTO**

---

## 🎯 ¡Comienza Ahora!

1. 🌐 Abre [actividad-particulas-interactivas.html](actividad-particulas-interactivas.html)
2. 📖 Lee [DOCUMENTACION-Y-REFLEXION.md](DOCUMENTACION-Y-REFLEXION.md)
3. 🧪 Experimenta con [GUIA-EXPERIMENTACION.md](GUIA-EXPERIMENTACION.md)

---

**¡Disfruta del aprendizaje y la experimentación!** 🚀✨

---

*Desarrollado como material educativo para el módulo de Desarrollo de Juegos 2D y 3D*