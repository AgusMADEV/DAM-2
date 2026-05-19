# 📚 Actividad Evaluable: Sistema de Partículas con Interacciones

## 🎯 Objetivo de la Actividad

Desarrollar un sistema de partículas interactivas que aplique conceptos de física computacional y programación orientada a objetos para simular comportamientos de agrupamiento basados en atributos compartidos.

---

## 📖 Introducción Teórica

### 1. Física Computacional Aplicada

Este proyecto implementa conceptos fundamentales de **simulación física**:

#### a) **Sistemas de N-cuerpos**
Un problema de N-cuerpos consiste en predecir el movimiento de múltiples objetos que interactúan entre sí. En nuestro caso:
- **N = 250 partículas**
- Cada partícula experimenta fuerzas de todas las demás
- Complejidad algorítmica: O(N²) por frame

#### b) **Integración Numérica**
Utilizamos el **Método de Euler** para resolver las ecuaciones de movimiento:

```
Ecuaciones de movimiento:
v(t+Δt) = v(t) + a(t)·Δt    [Velocidad]
x(t+Δt) = x(t) + v(t+Δt)·Δt [Posición]

Donde:
- x = posición
- v = velocidad
- a = aceleración (fuerza/masa, asumiendo masa=1)
- Δt = intervalo de tiempo (1 frame)
```

#### c) **Fuerzas Implementadas**

1. **Fuerza tipo Muelle (Ley de Hooke)**
   - Aplicada entre partículas del mismo tipo
   - F = k · (d - d₀)
   - d = distancia actual, d₀ = distancia objetivo, k = constante del muelle

2. **Fuerza de Repulsión**
   - Aplicada entre partículas de diferente tipo
   - F = k · (d_max - d) / d_max
   - Inversamente proporcional a la distancia

3. **Fricción**
   - v(t+1) = v(t) · α (donde α = 0.93)
   - Simula resistencia del medio
   - Estabiliza el sistema

---

## 🔬 Algoritmo de Agrupamiento

### Detección de Proximidad

La función `distance2D()` calcula la distancia euclidiana:

```javascript
d = √[(x₂-x₁)² + (y₂-y₁)²]
```

### Criterios de Agrupamiento

El algoritmo agrupa partículas basándose en:

1. **Identidad (texto)**: Partículas con el mismo nombre se atraen
2. **Distancia objetivo**: 120 píxeles (distancia ideal entre iguales)
3. **Zona de repulsión**: < 80 píxeles (evita solapamiento)
4. **Rango de interacción**: 200 píxeles para diferentes tipos

### Diagrama de Fuerzas

```
Distancia (d)     |  Fuerza aplicada
------------------|----------------------------------
d < 80px          |  REPULSIÓN FUERTE (seguridad)
80 < d < 120      |  ATRACCIÓN suave (mismo tipo)
d = 120px         |  EQUILIBRIO (mismo tipo)
120 < d < 200     |  ATRACCIÓN leve (mismo tipo)
d > 200           |  Sin interacción (diferente tipo)
```

---

## 💻 Implementación del Código

### Estructura de la Clase Particula

```
Particula {
  PROPIEDADES:
  - Posición: (x, y)
  - Velocidad: (vx, vy)
  - Aceleración: (ax, ay)
  - Identidad: texto
  - Estado: fija, estableFrames
  
  MÉTODOS:
  - interacciones() → Calcula fuerzas
  - mueve()         → Actualiza posición
  - rebote()        → Gestiona colisiones
  - dibuja()        → Renderiza visual
  - lineas()        → Muestra conexiones
}
```

### Ciclo de Simulación (60 FPS)

```
BUCLE PRINCIPAL:
1. Limpiar canvas
2. Para cada partícula:
   → Calcular fuerzas (interacciones)
3. Para cada partícula:
   → Aplicar movimiento
   → Detectar colisiones (rebote)
4. Renderizar todo:
   → Líneas de conexión
   → Partículas
5. requestAnimationFrame(bucle)
```

---

## 🔍 Análisis de Funciones Clave

### 1. Función `interacciones(particulas)`

**Propósito**: Calcula todas las fuerzas que actúan sobre una partícula

**Algoritmo**:
```
1. Si la partícula está fija → salir
2. Inicializar acumuladores de fuerza (fx, fy)
3. Para cada otra partícula p:
   a. Calcular distancia d
   b. Calcular vector unitario (ux, uy)
   c. Si d < distanciaMinima:
      → Aplicar repulsión fuerte
   d. Si mismo texto:
      → Aplicar fuerza tipo muelle
   e. Si diferente texto:
      → Aplicar repulsión suave
4. Limitar fuerza máxima (estabilidad)
5. Asignar fx → ax, fy → ay
```

**Conceptos Aplicados**:
- Vectores unitarios para direccionalidad
- Superposición de fuerzas
- Limitación para estabilidad numérica

### 2. Función `mueve()`

**Propósito**: Integra las ecuaciones de movimiento

**Pasos**:
1. **Actualizar velocidad**: v = v + a (Euler)
2. **Aplicar fricción**: v = v × 0.93
3. **Actualizar posición**: x = x + v
4. **Detectar estabilidad**: 
   - Si velocidad y fuerza son mínimas durante 60 frames
   - → Marcar como fija (optimización)

**Concepto**: Integración numérica de ecuaciones diferenciales

### 3. Función `rebote()`

**Propósito**: Gestionar colisiones con bordes

**Física**:
- **Colisión inelástica**: energía se pierde
- **Coeficiente de restitución**: e = -0.5
- Al colisionar: v_nueva = v_vieja × (-0.5)

**Implementación**:
```javascript
if (this.x > anchura) {
  this.x = anchura;      // Reposicionar
  this.vx *= -0.5;       // Invertir + amortiguar
}
```

---

## 🎨 Visualización

### Sistema de Colores

- **Partículas estables**: Fondo verde claro (#e8f5e9), borde verde (#4CAF50)
- **Partículas móviles**: Fondo blanco, borde negro
- **Líneas mismo tipo**: Verde semi-transparente (opacidad 0.6)
- **Líneas diferente tipo**: Gris transparente (opacidad 0.2)

### Información en Tiempo Real

El panel muestra:
- Total de partículas
- Partículas fijas (en equilibrio)
- Partículas en movimiento

---

## 🚀 Optimizaciones Implementadas

### 1. Sistema de Partículas Fijas

**Problema**: Calcular fuerzas para 250 partículas cada frame es costoso.

**Solución**:
```javascript
if (this.fija) {
  this.ax = 0;
  this.ay = 0;
  return; // No calcular fuerzas
}
```

**Resultado**: Reducción progresiva de cálculos a medida que el sistema se estabiliza.

### 2. Limitación de Fuerza Máxima

**Problema**: Fuerzas muy grandes causan inestabilidad numérica.

**Solución**:
```javascript
const maxForce = 0.05;
if (fuerza_total > maxForce) {
  fuerza = fuerza * (maxForce / fuerza_total);
}
```

**Resultado**: Sistema estable sin explosiones numéricas.

### 3. Fricción Adaptativa

**Concepto**: La fricción (0.93) hace que el sistema converja hacia equilibrio.

**Beneficio**: Las partículas se detienen naturalmente, permitiendo la detección de estabilidad.

---

## 📊 Optimizaciones Adicionales Posibles

### 1. **Spatial Hashing / Cuadrícula**

**Idea**: Dividir el espacio en celdas.

```javascript
// En lugar de comprobar todas las partículas:
for (let p of particulas) { ... }  // O(N²)

// Comprobar solo las de celdas cercanas:
for (let p of celdasCercanas) { ... }  // O(N)
```

**Beneficio**: Reducción de O(N²) a O(N) en casos óptimos.

### 2. **Web Workers**

**Idea**: Calcular fuerzas en un hilo separado.

```javascript
// Main thread: Renderizado
// Worker thread: Física
```

**Beneficio**: Mejor rendimiento en sistemas multiprocesador.

### 3. **Barnes-Hut Algorithm**

**Concepto**: Agrupar partículas distantes en "superpartículas".

**Beneficio**: Reducción de complejidad a O(N log N).

### 4. **Verlet Integration**

**Idea**: Método de integración más preciso que Euler.

```javascript
// Euler (actual):
x_nuevo = x + v*dt

// Verlet:
x_nuevo = 2*x_actual - x_antiguo + a*dt²
```

**Beneficio**: Mayor estabilidad numérica, permite timesteps más grandes.

---

## 🎓 Relación con Conceptos de Clase

### Programación Orientada a Objetos

- **Encapsulación**: La clase `Particula` agrupa datos y comportamiento
- **Cohesión**: Cada método tiene una responsabilidad clara
- **Reutilización**: La clase es instanciable múltiples veces

### Física para Videojuegos

- **Detección de colisiones**: Método `rebote()`
- **Sistemas de partículas**: Fundamento de efectos visuales
- **Simulación física**: Base de motores como Unity, Unreal

### Algoritmos y Estructuras de Datos

- **Búsqueda de vecinos**: Base de algoritmos espaciales
- **Optimización**: Trade-off entre precisión y rendimiento
- **Complejidad computacional**: Análisis de O(N²)

### Programación Interactiva

- **Animación con `requestAnimationFrame`**: Sincronización con monitor
- **Canvas API**: Gráficos 2D en tiempo real
- **Event Handling**: Controles de pausa/reinicio

---

## 🏆 Resultados Esperados

Al ejecutar la aplicación, deberías observar:

1. **Formación de grupos**: Partículas con el mismo nombre convergen
2. **Separación de grupos**: Grupos diferentes mantienen distancia
3. **Estabilización progresiva**: Las partículas se vuelven verdes al estabilizarse
4. **Red visual**: Líneas muestran las conexiones activas
5. **Información en tiempo real**: El panel muestra estadísticas

---

## 📝 Conclusiones

### Aprendizajes Clave

1. **Física computacional** es la base de simulaciones realistas
2. **Vectores y trigonometría** son esenciales para movimiento 2D
3. **Optimización** es crucial para sistemas con muchas entidades
4. **Integración numérica** permite resolver ecuaciones complejas
5. **POO** facilita la organización de sistemas complejos

### Aplicaciones Prácticas

Este tipo de sistema se utiliza en:
- **Videojuegos**: IA de multitudes, comportamiento de enjambres
- **Visualización de datos**: Gráficos de red, clustering
- **Simulaciones científicas**: Dinámica molecular, astronomía
- **Arte generativo**: Instalaciones interactivas

### Reflexión Personal

Este ejercicio demuestra cómo conceptos matemáticos y físicos abstractos cobran vida mediante código. La interacción emergente (grupos que se forman sin programación explícita) es un ejemplo de **comportamiento emergente**, un concepto clave en sistemas complejos.

La progresión desde partículas simples (ejercicio 001) hasta este sistema complejo de interacciones muestra la construcción incremental de funcionalidad, un principio fundamental del desarrollo de software.

---

## 🔗 Referencias y Recursos

### Conceptos Matemáticos
- Vectores en 2D
- Distancia euclidiana
- Integración numérica (Métodos de Euler y Verlet)
- Fuerzas centrales y leyes de potencia

### Algoritmos Relacionados
- Boids (Reynolds, 1987) - Comportamiento de bandadas
- Particle Swarm Optimization - Optimización inspirada en enjambres
- Force-Directed Graph Drawing - Visualización de grafos

### Técnicas de Optimización
- Spatial Hashing / Grid Partitioning
- Quadtrees / Octrees
- Barnes-Hut Algorithm
- Verlet Integration

---

## 📅 Información del Proyecto

**Asignatura**: Programación Multimedia y Dispositivos Móviles  
**Módulo**: Desarrollo de Juegos 2D y 3D  
**Tema**: Fases de Desarrollo  
**Tipo**: Actividad Evaluable  
**Fecha**: Febrero 2026

---

**🎮 ¡Experimenta con los parámetros y observa cómo cambia el comportamiento del sistema!**