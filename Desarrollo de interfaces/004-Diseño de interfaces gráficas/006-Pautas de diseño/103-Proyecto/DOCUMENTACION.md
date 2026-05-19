# 📚 Documentación - Simulación de Partículas 3D con Física Interactiva

## 📋 Índice
1. [Introducción](#introducción)
2. [Conceptos de Física 3D Aplicados](#conceptos-de-física-3d-aplicados)
3. [Características del Proyecto](#características-del-proyecto)
4. [Escenarios Implementados](#escenarios-implementados)
5. [Parámetros Físicos](#parámetros-físicos)
6. [Guía de Uso](#guía-de-uso)
7. [Modificaciones Realizadas](#modificaciones-realizadas)
8. [Experimentos Sugeridos](#experimentos-sugeridos)
9. [Recursos de Aprendizaje](#recursos-de-aprendizaje)

---

## 🎯 Introducción

Este proyecto es una **simulación avanzada de partículas en 3D** que implementa múltiples conceptos de física para crear un entorno interactivo y educativo. Está basado en los ejemplos de clase (carpeta 101) pero extendido con nuevas características y escenarios.

### Objetivos del Proyecto
- Practicar conceptos de **física 3D** (gravedad, fuerzas, colisiones)
- Implementar un **sistema de partículas** configurable
- Crear **escenarios interactivos** que demuestren diferentes fenómenos físicos
- Proporcionar **controles en tiempo real** para experimentar con los parámetros

### Tecnologías Utilizadas
- **A-Frame 1.5.0**: Framework para realidad virtual y 3D en web
- **Three.js**: Motor 3D subyacente (incluido con A-Frame)
- **JavaScript ES6+**: Lógica de simulación y física
- **HTML5/CSS3**: Interfaz y controles

---

## ⚛️ Conceptos de Física 3D Aplicados

### 1. **Sistema de Coordenadas 3D**
```javascript
// Cada partícula tiene posición en 3 ejes
x, y, z  // Posición en metros
```
- **Eje Y**: Vertical (arriba/abajo)
- **Eje X**: Horizontal (izquierda/derecha)
- **Eje Z**: Profundidad (adelante/atrás)

### 2. **Cinemática**
El movimiento se calcula usando las ecuaciones fundamentales:

```javascript
// Velocidad
vx += ax * dt
vy += ay * dt
vz += az * dt

// Posición
x += vx * dt
y += vy * dt
z += vz * dt
```

donde:
- `v` = velocidad (m/s)
- `a` = aceleración (m/s²)
- `dt` = delta de tiempo (s)

### 3. **Fuerzas Aplicadas**

#### a) **Gravedad**
```javascript
ay = gravedad  // Típicamente -0.01 (hacia abajo)
```
La gravedad es una **aceleración constante** hacia abajo que afecta a todas las partículas.

**Efecto**: Las partículas caen continuamente, simulando el comportamiento real.

#### b) **Viento**
```javascript
ax += viento   // Fuerza horizontal constante
az += vientoZ  // Fuerza en profundidad
```
El viento aplica una **fuerza constante** en direcciones horizontales.

**Efecto**: Desplaza las partículas lateralmente, como el viento real.

#### c) **Fuerza Central (Centrípeta)**
```javascript
// Vector hacia el centro
dx = centroX - x
dy = centroY - y
dz = centroZ - z
distancia = sqrt(dx² + dy² + dz²)

// Fuerza normalizada
ax += (dx / distancia) * fuerzaCentral
ay += (dy / distancia) * fuerzaCentral
az += (dz / distancia) * fuerzaCentral
```

La fuerza central atrae todas las partículas hacia un punto central.

**Efecto**: Crea órbitas o espirales, simula gravedad de un cuerpo central.

### 4. **Fricción**
```javascript
vx *= friccion  // Típicamente 0.98 (2% de pérdida)
vy *= friccion
vz *= friccion
```

La fricción **reduce la velocidad** multiplicándola por un factor < 1.

**Efecto**: Las partículas se ralentizan gradualmente, simulando resistencia del aire.

### 5. **Colisiones con Límites (Rebotes)**
```javascript
if (y < radioParticula) {
  y = radioParticula
  vy *= -coeficienteRebote  // Invertir velocidad
  vx *= 0.95  // Pérdida de energía lateral
  vz *= 0.95
}
```

Cuando una partícula alcanza un límite:
1. Se reposiciona en el límite
2. La velocidad perpendicular se invierte
3. Se aplica un coeficiente de rebote (pérdida de energía)

**Coeficiente de rebote**:
- `1.0` = Rebote perfectamente elástico (sin pérdida)
- `0.5` = Pierde 50% de energía
- `0.0` = Sin rebote (se queda pegado)

### 6. **Colisiones Entre Partículas**

Se implementa una **colisión elástica simplificada**:

```javascript
// 1. Detectar colisión
distancia = sqrt(dx² + dy² + dz²)
if (distancia < radio1 + radio2) {
  // COLISIÓN
  
  // 2. Vector normal de colisión
  nx = dx / distancia
  ny = dy / distancia
  nz = dz / distancia
  
  // 3. Velocidad relativa en dirección normal
  velocidadRelativa = (v1x - v2x)*nx + (v1y - v2y)*ny + (v1z - v2z)*nz
  
  // 4. Intercambio de momento (simplificado)
  v1x -= velocidadRelativa * nx
  v1y -= velocidadRelativa * ny
  v1z -= velocidadRelativa * nz
  v2x += velocidadRelativa * nx
  v2y += velocidadRelativa * ny
  v2z += velocidadRelativa * nz
}
```

**Efecto**: Las partículas rebotan entre sí de forma realista.

### 7. **Conservación y Pérdida de Energía**

En un sistema físico real, la energía se conserva o se disipa:

- **Energía Cinética**: $E_k = \frac{1}{2}mv^2$
- **Energía Potencial Gravitatoria**: $E_p = mgh$

En nuestra simulación:
- La **fricción** disipa energía continuamente
- Los **rebotes** (coef < 1) disipan energía en colisiones
- Sin estas pérdidas, las partículas se moverían infinitamente

---

## ✨ Características del Proyecto

### 🎮 Sistema de Partículas Avanzado
- ✅ Hasta 500 partículas simultáneas
- ✅ Propiedades físicas individuales (masa, radio, color)
- ✅ Sistema de vida útil (partículas que desaparecen)
- ✅ Generación dinámica de partículas

### ⚡ Múltiples Fuerzas Físicas
- ✅ Gravedad variable (puede ser negativa o cero)
- ✅ Viento en dos dimensiones horizontales
- ✅ Fuerza centrípeta hacia el centro
- ✅ Fricción configurable
- ✅ Colisiones elásticas

### 🎨 Efectos Visuales
- ✅ Colores dinámicos basados en velocidad
- ✅ Emisividad variable (brillo)
- ✅ Sistema de estelas (trails) opcional
- ✅ Iluminación realista (ambiente, direccional, puntual)
- ✅ Niebla exponencial para profundidad

### 🎯 Interactividad
- ✅ 6 escenarios predefinidos
- ✅ Controles en tiempo real para todos los parámetros
- ✅ Click para crear mini-explosiones
- ✅ Pausa/Reanudar simulación
- ✅ Regeneración y limpieza de partículas
- ✅ Estadísticas en vivo (FPS, número de partículas)

### 🎥 Navegación 3D
- ✅ Movimiento WASD (plano horizontal)
- ✅ Q/E para subir/bajar
- ✅ Ratón para mirar alrededor (360°)
- ✅ Posición inicial optimizada

---

## 🎬 Escenarios Implementados

### 1. 🌧️ Lluvia
**Concepto físico**: Caída libre con resistencia del aire

**Parámetros**:
- Gravedad: -0.02 (fuerte)
- Viento: 0.002 (ligero)
- Fricción: 0.995 (alta resistencia)
- Rebote: 0.1 (baja elasticidad)

**Comportamiento**:
- Las partículas caen desde arriba
- Ligero movimiento lateral por viento
- Al tocar el suelo, apenas rebotan (como gotas de agua)
- Se dispersan lateralmente al impactar

**Aplicación real**: Simulación de lluvia, granizo, o partículas cayendo

---

### 2. 💥 Explosión
**Concepto físico**: Expansión radial desde un punto

**Parámetros**:
- Gravedad: -0.008 (media)
- Sin viento
- Fricción: 0.985 (media)
- Rebote: 0.6 (media elasticidad)

**Comportamiento**:
- Todas las partículas se generan en el centro
- Velocidades iniciales en direcciones aleatorias uniformemente distribuidas
- Expansión esférica simétrica
- Gradualmente caen por gravedad
- Rebotan con las paredes

**Aplicación real**: Fuegos artificiales, explosiones, dispersión de material

---

### 3. ⛲ Fuente
**Concepto físico**: Trayectoria parabólica continua

**Parámetros**:
- Gravedad: -0.015 (fuerte)
- Sin viento
- Fricción: 0.99 (baja)
- Rebote: 0.4 (bajo)

**Comportamiento especial**:
- **Generación continua** de partículas (5 cada 200ms)
- Velocidad inicial hacia arriba
- Dispersión horizontal aleatoria
- Vida útil limitada (8 segundos)
- Forma parabólica clásica

**Aplicación real**: Fuentes de agua, géiseres, chorros

---

### 4. 🛸 Sistema Orbital
**Concepto físico**: Movimiento orbital por fuerza centrípeta

**Parámetros**:
- Gravedad: 0 (ingravidez)
- Sin viento
- Fricción: 0.999 (muy baja)
- Rebote: 0.8 (alto)
- Fuerza central: 0.002 (moderada)

**Comportamiento**:
- Partículas distribuidas en diferentes radios
- Velocidad tangencial inicial
- La fuerza central simula gravedad del cuerpo central
- Crean órbitas elípticas y circulares
- Sin fricción atmosférica, las órbitas son estables

**Física subyacente**:
```
Fuerza centrípeta = m * v² / r
```

**Aplicación real**: Sistemas solares, satélites, partículas en campos gravitatorios

---

### 5. 🌪️ Vórtice (Remolino)
**Concepto físico**: Movimiento circular con componente descendente

**Parámetros**:
- Gravedad: -0.005 (ligera)
- Sin viento externo
- Fricción: 0.995 (media)
- Rebote: 0.3 (bajo)
- Fuerza central: 0.001 (ligera)

**Comportamiento**:
- Velocidad tangencial inicial (circular)
- Gravedad leve que hace descender
- Fuerza central que atrae hacia el eje
- Crea espiral descendente
- Al tocar el suelo, se dispersan

**Aplicación real**: Tornados, remolinos de agua, vórtices atmosféricos

---

### 6. 🎲 Caos
**Concepto físico**: Sistema dinámico con parámetros aleatorios

**Parámetros**:
- **Todos los parámetros son aleatorios**
- Gravedad: [-0.01, +0.01]
- Viento: [-0.01, +0.01] en X y Z
- Fricción: [0.97, 0.99]
- Rebote: [0.3, 0.8]
- Fuerza central: [0, 0.003]

**Comportamiento**:
- Totalmente impredecible
- Cada ejecución es diferente
- Explora el espacio de parámetros
- Puede producir patrones emergentes

**Aplicación didáctica**: Demuestra cómo pequeños cambios en parámetros generan comportamientos muy diferentes (teoría del caos)

---

## 🔧 Parámetros Físicos

### Parámetros Modificables en Tiempo Real

| Parámetro | Rango | Unidad | Descripción |
|-----------|-------|--------|-------------|
| **Gravedad** | -0.05 a +0.05 | m/s² | Aceleración vertical. Negativo = hacia abajo |
| **Viento X** | -0.02 a +0.02 | m/s² | Fuerza horizontal (izq/der) |
| **Viento Z** | -0.02 a +0.02 | m/s² | Fuerza en profundidad (adelante/atrás) |
| **Fuerza Central** | 0 a 0.005 | m/s² | Atracción hacia el centro (0,10,0) |
| **Fricción** | 0.8 a 0.999 | adimensional | Factor de reducción de velocidad |
| **Coef. Rebote** | 0 a 1 | adimensional | Elasticidad de colisiones con límites |
| **Radio Partícula** | 0.1 a 0.5 | m | Tamaño visual y colisión |
| **Num. Partículas** | 50 a 500 | unidades | Cantidad de partículas activas |

### Límites del Espacio 3D

```javascript
limX = 20 metros  // ±20 en X
limY = 20 metros  // 0 a 40 en Y (doble altura)
limZ = 20 metros  // ±20 en Z
```

**Volumen total**: 40 × 40 × 40 = 64,000 m³

---

## 📖 Guía de Uso

### Inicio Rápido

1. **Abrir el archivo**: `simulacion-particulas.html` en un navegador moderno
2. **Esperar a que cargue**: La escena 3D se inicializa automáticamente
3. **Elegir un escenario**: Click en cualquier botón de escenario
4. **Experimentar**: Modificar los controles deslizantes

### Controles de Navegación

| Tecla/Acción | Efecto |
|--------------|--------|
| **W** | Avanzar |
| **S** | Retroceder |
| **A** | Izquierda |
| **D** | Derecha |
| **Q** | Subir |
| **E** | Bajar |
| **Ratón** | Mirar alrededor (arrastra) |
| **Click** | Crear mini-explosión en dirección de la mirada |

### Controles de Simulación

- **Pausar/Reanudar**: Congela la física pero mantiene la navegación
- **Reiniciar**: Regenera partículas con parámetros actuales
- **Limpiar**: Elimina todas las partículas
- **Regenerar Partículas**: Crea nuevas partículas aleatorias

### Opciones Visuales

- **Activar estelas**: Deja rastro del movimiento (afecta rendimiento)
- **Colores dinámicos**: El brillo varía con la velocidad
- **Detectar colisiones**: Activa/desactiva colisiones entre partículas

---

## 🔄 Modificaciones Realizadas (respecto a ejemplos de clase)

### Basado en los ejercicios 005-008 de la carpeta 101

#### ➕ Nuevas Características

1. **Sistema de Escenarios Predefinidos**
   - 6 escenarios completos con parámetros optimizados
   - Botones de acceso rápido
   - Actualización automática de controles

2. **Física Mejorada**
   - Fuerza central/centrípeta añadida
   - Colisiones elásticas entre partículas
   - Múltiples componentes de viento (X y Z)
   - Sistema de vida útil de partículas

3. **Controles Expandidos**
   - 8 parámetros ajustables en tiempo real
   - Rangos optimizados para cada parámetro
   - Feedback visual inmediato
   - Valores numéricos precisos

4. **Efectos Visuales**
   - Colores dinámicos basados en velocidad
   - Iluminación mejorada (3 fuentes de luz)
   - Niebla exponencial para profundidad
   - Sistema de estelas opcional
   - Efectos de emisividad en colisiones

5. **Interactividad**
   - Click para crear explosiones localizadas
   - Pausa sin perder el estado
   - Regeneración dinámica
   - Estadísticas en tiempo real (FPS, conteo)

6. **Arquitectura del Código**
   - Clase `Particula` orientada a objetos
   - Separación clara de responsabilidades
   - Código documentado y estructurado
   - Fácil de extender

#### 🔧 Mejoras Técnicas

1. **Rendimiento**
   - Detección de colisiones optimizada
   - Actualización condicional de efectos visuales
   - Gestión eficiente de memoria (eliminación de partículas muertas)

2. **Usabilidad**
   - Interfaz más intuitiva y clara
   - Ayuda contextual siempre visible
   - Valores numéricos con precisión adecuada
   - Diseño responsive del panel de control

3. **Escalabilidad**
   - Fácil añadir nuevos escenarios
   - Parámetros centralizados
   - Sistema modular de fuerzas

---

## 🧪 Experimentos Sugeridos

### Experimento 1: Encontrar la Órbita Perfecta
**Objetivo**: Conseguir órbitas circulares estables

1. Iniciar escenario "Sistema Orbital"
2. Ajustar `Fuerza Central` hasta que las órbitas sean circulares
3. Modificar `Fricción` a 0.999 para máxima estabilidad
4. Observar cómo diferentes partículas tienen órbitas distintas

**Pregunta**: ¿Por qué las partículas más alejadas necesitan menos velocidad?

---

### Experimento 2: Gravedad Inversa
**Objetivo**: Ver qué pasa con gravedad positiva (hacia arriba)

1. Iniciar cualquier escenario
2. Cambiar `Gravedad` a +0.02 (máximo positivo)
3. Observar el comportamiento

**Pregunta**: ¿Por qué las partículas se acumulan en el techo y no caen?

---

### Experimento 3: Fricción Cero vs. Máxima
**Objetivo**: Entender el efecto de la fricción

1. Escenario "Explosión"
2. **Experimento A**: Fricción = 0.8
   - Observar cuánto duran las partículas en movimiento
3. **Experimento B**: Fricción = 0.999
   - Observar la diferencia

**Pregunta**: ¿Qué representa la fricción en el mundo real?

---

### Experimento 4: Colisiones Sin Rebote
**Objetivo**: Ver efecto del coeficiente de restitución

1. Escenario "Lluvia"
2. Cambiar `Coef. Rebote` a 0
3. Observar cómo las partículas no rebotan

**Pregunta**: ¿Qué materiales reales tienen rebote cercano a 0?

---

### Experimento 5: Crear un Huracán
**Objetivo**: Simular un vórtice atmosférico

1. Escenario "Vórtice"
2. Aumentar `Fuerza Central` a 0.003
3. Reducir `Gravedad` a -0.002
4. Añadir `Viento X` = 0.01

**Pregunta**: ¿Cómo cambia el patrón de movimiento?

---

### Experimento 6: Máximo Caos
**Objetivo**: Explorar comportamientos complejos

1. Escenario "Caos" (ejecutar varias veces)
2. Buscar configuraciones interesantes
3. Intentar replicarlas manualmente

**Pregunta**: ¿Puedes predecir el comportamiento observando los parámetros?

---

## 📚 Recursos de Aprendizaje

### Conceptos de Física Aplicada

#### 1. **Mecánica Newtoniana**
- Segunda Ley de Newton: F = ma
- [Khan Academy - Newton's Laws](https://www.khanacademy.org/science/physics/forces-newtons-laws)
- [Physics Classroom - Kinematics](https://www.physicsclassroom.com/class/1DKin)

#### 2. **Colisiones y Conservación de Momento**
- Colisiones elásticas e inelásticas
- [Elastic Collisions](https://en.wikipedia.org/wiki/Elastic_collision)
- Conservación de energía y momento

#### 3. **Movimiento Orbital**
- Fuerza centrípeta: Fc = mv²/r
- Velocidad orbital: v = √(GM/r)
- [Orbital Mechanics Basics](https://www.youtube.com/watch?v=xdoiRgV02is)

#### 4. **Sistemas de Partículas**
- [Nature of Code - Particle Systems](https://natureofcode.com/book/chapter-4-particle-systems/)
- [Three.js Particle System Tutorial](https://threejs.org/docs/#manual/en/introduction/Creating-a-scene)

### Tutoriales de A-Frame y Three.js

#### A-Frame (Framework 3D/VR)
- [A-Frame School](https://aframe.io/aframe-school/)
- [A-Frame Documentation](https://aframe.io/docs/1.5.0/introduction/)
- [A-Frame Examples](https://aframe.io/examples/showcase/)

#### Three.js (Motor 3D)
- [Three.js Journey](https://threejs-journey.com/)
- [Three.js Fundamentals](https://threejsfundamentals.org/)
- [Three.js Examples](https://threejs.org/examples/)

### Matemáticas para Gráficos 3D

#### Vectores y Álgebra Lineal
- [3Blue1Brown - Essence of Linear Algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab)
- Operaciones vectoriales (suma, producto escalar, cruz)
- Normalización de vectores

#### Trigonometría Aplicada
- Coordenadas esféricas: (r, θ, φ)
- Conversión esférica ↔ cartesiana
- [Math is Fun - Spherical Coordinates](https://www.mathsisfun.com/geometry/spherical-coordinates.html)

### Cursos Online Recomendados

1. **Physics Simulations in JavaScript**
   - Coursera / Udemy
   - Implementación de física en código

2. **Game Physics Programming**
   - Colisiones, cinemática, dinámica
   - Optimización de simulaciones

3. **Computer Graphics**
   - MIT OpenCourseWare
   - Fundamentos de renderizado 3D

---

## 🎓 Conceptos Técnicos Avanzados

### 1. Integración Numérica
Nuestro código usa **Integración de Euler** (el método más simple):

```javascript
v = v + a * dt
x = x + v * dt
```

**Ventajas**: Simple, rápido
**Desventajas**: Puede ser inestable con dt grande

**Métodos más avanzados**:
- **Verlet Integration**: Más estable, conserva energía mejor
- **Runge-Kutta (RK4)**: Muy preciso, usado en simulaciones científicas

### 2. Detección de Colisiones
Usamos **Broad Phase** simplificada:

```javascript
// Solo chequeamos partículas cercanas
if (distancia < radio1 + radio2) {
  // COLISIÓN
}
```

**Optimizaciones posibles**:
- **Spatial Hashing**: Dividir espacio en celdas
- **Quadtree/Octree**: Estructura de datos jerárquica
- **Sweep and Prune**: Ordenar por ejes

Complejidad actual: O(n²)
Con optimización: O(n log n) o mejor

### 3. Renderizado Condicional
```javascript
// Solo actualizar visual cada N frames
if (frameCount % 3 === 0) {
  actualizarEstela();
}
```

Reduce llamadas al DOM, mejora rendimiento.

### 4. Pool de Objetos
Para mejor rendimiento, se podría implementar:

```javascript
// En vez de crear/destruir partículas
// Reutilizar objetos de un pool
class ParticlePool {
  constructor(size) {
    this.pool = [];
    for (let i = 0; i < size; i++) {
      this.pool.push(new Particula());
    }
  }
  
  get() {
    return this.pool.find(p => !p.activa);
  }
  
  release(particula) {
    particula.reset();
    particula.activa = false;
  }
}
```

---

## 💡 Ideas para Extensiones

### Extensiones Físicas
1. **Campos de Fuerza Variables**
   - Zonas con diferente gravedad
   - Viento turbulento (variación temporal)

2. **Fluidos Básicos**
   - Simulación SPH (Smoothed Particle Hydrodynamics)
   - Viscosidad entre partículas

3. **Electromagnetismo**
   - Partículas con carga (+/-)
   - Fuerza de Coulomb

4. **Física de Telas**
   - Conectar partículas con resortes
   - Simular banderas o ropa

### Extensiones Visuales
1. **Partículas con Texturas**
   - Sprites para fuego, humo
   - Partículas con forma

2. **Iluminación Dinámica**
   - Partículas que emiten luz
   - Sombras en tiempo real

3. **Post-Procesado**
   - Bloom (brillo)
   - Motion blur
   - Color grading

### Extensiones Interactivas
1. **Editor de Escenarios**
   - Guardar/cargar configuraciones
   - Exportar parámetros a JSON

2. **Modo Sandbox**
   - Crear partículas con click
   - Pintar con partículas
   - Arrastrar para aplicar fuerzas

3. **Modo Educativo**
   - Visualizar vectores de fuerza
   - Mostrar ecuaciones en tiempo real
   - Gráficas de energía

---

## 🐛 Resolución de Problemas

### Problema: Baja tasa de FPS
**Soluciones**:
1. Reducir número de partículas
2. Desactivar colisiones entre partículas
3. Desactivar estelas
4. Cerrar otras pestañas del navegador

### Problema: Las partículas "explotan" (velocidades infinitas)
**Causa**: Paso de tiempo (dt) muy grande o fuerzas mal configuradas

**Solución**:
1. Reducir valores de fuerzas
2. Aumentar fricción
3. Implementar límite de velocidad máxima

### Problema: No se ven las partículas
**Soluciones**:
1. Verificar que la escena haya cargado
2. Navegar hacia el centro (0, 10, 0)
3. Regenerar partículas
4. Verificar consola del navegador para errores

---

## 📝 Registro de Modificaciones

### Versión 1.0 (Fecha: 8 de febrero de 2026)

#### Cambios respecto a ejercicios base (101):

**Del ejercicio 005-espacio en 3D.html:**
- ✅ Mantenido: Sistema de coordenadas 3D, física básica
- ➕ Añadido: Múltiples escenarios, más fuerzas físicas
- 🔧 Mejorado: Controles más completos, mejor UI

**Del ejercicio 006-espacio en 3D mejorado.html:**
- ✅ Mantenido: Controles de zoom, etiquetas
- ➕ Añadido: Colisiones entre partículas, efectos visuales
- 🔧 Mejorado: Navegación más fluida

**Del ejercicio 008-billboards y mas cosas.html:**
- ✅ Mantenido: Estética visual, iluminación
- ➕ Añadido: Más tipos de iluminación, niebla
- 🔧 Mejorado: Shader custom eliminado (simplificado)

#### Parámetros Modificados:

| Parámetro Original | Valor Original | Nuevo Rango | Justificación |
|-------------------|----------------|-------------|---------------|
| Gravedad | Fijo (-0.01) | -0.05 a +0.05 | Permitir gravedad inversa y cero |
| Fricción | 0.93 | 0.8 a 0.999 | Mayor control sobre disipación |
| Rebote | -0.5 (invertido) | 0 a 1 | Más intuitivo y realista |
| Num. Partículas | Variable | 50 a 500 | Rango optimizado para rendimiento |

#### Nuevas Funcionalidades:

1. **6 Escenarios Completos** (0 → 6)
2. **Fuerza Central** (no existía)
3. **Viento en 2 ejes** (1 → 2)
4. **Colisiones entre partículas** (nueva)
5. **Sistema de vida útil** (nuevo)
6. **Generación continua** (Fuente) (nueva)
7. **Click interactivo** (explosiones localizadas) (nuevo)
8. **Estadísticas en vivo** (nueva)

---

## 🎯 Conclusiones

Este proyecto demuestra cómo conceptos fundamentales de física pueden implementarse en código para crear simulaciones interactivas y educativas. Los principales aprendizajes incluyen:

1. **Física 3D**: Vectores, fuerzas, cinemática
2. **Integración numérica**: Euler, manejo de tiempo
3. **Detección de colisiones**: Espacial, entre partículas
4. **Optimización**: Rendimiento con múltiples objetos
5. **Diseño de interacción**: Controles intuitivos en tiempo real

Las posibilidades de extensión son infinitas, desde simulaciones científicas hasta videojuegos, visualizaciones artísticas o herramientas educativas.

**¡Experimenta, modifica y aprende!** 🚀

---

## 📄 Licencia y Créditos

**Proyecto Educativo** - Desarrollo de Interfaces Gráficas
**Curso**: DAM-2
**Basado en**: Ejercicios 101 (carpeta de ejemplos de clase)
**Tecnologías**: A-Frame, Three.js, WebGL

**Autor**: [Tu nombre]
**Fecha**: 8 de febrero de 2026

---

## 📞 Contacto y Soporte

Para dudas, sugerencias o reportar problemas:
- Consultar con el profesor
- Revisar documentación de [A-Frame](https://aframe.io)
- Comunidad de [Three.js](https://discourse.threejs.org)

---

**🎓 ¡Sigue experimentando y aprendiendo!**
