He desarrollado un **sistema de partículas con interacciones físicas** que simula el comportamiento de agrupamiento emergente basado en atributos compartidos. En concreto, mi implementación consiste en 250 partículas que navegan por un canvas HTML5, donde cada partícula tiene asignado un nombre aleatorio de un conjunto de 6 posibles valores.

El concepto general que aplico es el de **sistemas de N-cuerpos con fuerzas diferenciales**: las partículas con el mismo nombre se atraen entre sí mediante una fuerza tipo muelle (Ley de Hooke), mientras que las partículas con nombres diferentes se repelen mediante una fuerza inversamente proporcional a la distancia. Este comportamiento genera grupos o "clusters" de manera natural, sin necesidad de programar explícitamente la formación de estos grupos.

Este tipo de sistema se utiliza ampliamente en múltiples contextos:

- **Videojuegos**: Comportamiento de enjambres, multitudes, partículas mágicas, sistemas de efectos especiales
- **Visualización de datos**: Representación de redes sociales, clustering de información, grafos de relaciones
- **Simulaciones científicas**: Dinámica molecular, simulaciones astronómicas, estudios de comportamiento colectivo
- **Arte generativo**: Instalaciones interactivas, visualizaciones musicales

En mi caso, este ejercicio me ha permitido consolidar los conceptos trabajados progresivamente en clases, donde fui construyendo desde redes simples hasta este sistema complejo de interacciones.

---

### Fundamentos Teóricos

Mi implementación se basa en tres pilares fundamentales de la física computacional:

#### A) Sistemas de N-cuerpos

Un **problema de N-cuerpos** consiste en predecir el movimiento individual de un grupo de objetos que interactúan entre sí mediante fuerzas físicas. En mi caso:

- **N = 250** partículas
- Cada partícula calcula las fuerzas ejercidas por las **249 restantes**
- Complejidad algorítmica: **O(N²)** por cada frame

La ecuación general que gobierna el sistema es:

$$
\vec{F}_i = \sum_{j \neq i}^{N} \vec{F}_{ij}
$$

Donde $\vec{F}_i$ es la fuerza total sobre la partícula $i$, y $\vec{F}_{ij}$ es la fuerza que la partícula $j$ ejerce sobre $i$.

#### B) Integración Numérica - Método de Euler

Para resolver las ecuaciones de movimiento, he implementado el **Método de Euler**, que discretiza las ecuaciones diferenciales:

$$
\begin{align}
\vec{v}(t + \Delta t) &= \vec{v}(t) + \vec{a}(t) \cdot \Delta t \\
\vec{x}(t + \Delta t) &= \vec{x}(t) + \vec{v}(t + \Delta t) \cdot \Delta t
\end{align}
$$

Donde:
- $\vec{x}$ = posición (píxeles)
- $\vec{v}$ = velocidad (píxeles/frame)
- $\vec{a}$ = aceleración (asumiendo masa m=1, entonces $\vec{a} = \vec{F}$)
- $\Delta t$ = 1 frame (aprox. 16.67ms a 60 FPS)

#### C) Tipos de Fuerzas Implementadas

He implementado tres tipos de fuerzas diferenciadas:

**1. Fuerza tipo Muelle (Ley de Hooke)** - Entre partículas iguales:

$$
\vec{F}_{muelle} = k \cdot (d - d_0) \cdot \hat{u}
$$

Donde:
- $k = 0.0012$ (constante del muelle)
- $d$ = distancia actual entre partículas
- $d_0 = 120$ píxeles (distancia de equilibrio)
- $\hat{u}$ = vector unitario direccional

**2. Fuerza de Repulsión** - Entre partículas diferentes:

$$
\vec{F}_{repulsión} = -k_{rep} \cdot (d_{max} - d) \cdot \hat{u}
$$

Donde:
- $k_{rep} = 0.001$
- $d_{max} = 200$ píxeles (rango de repulsión)

**3. Fricción** - Disipación de energía:

$$
\vec{v}(t+1) = \vec{v}(t) \cdot \alpha \quad \text{donde } \alpha = 0.93
$$

Esto significa que cada frame, las partículas pierden el 7% de su velocidad, lo que estabiliza el sistema y evita movimiento perpetuo.

### Estructura de la Clase Particula

He diseñado la clase `Particula` siguiendo principios de **Programación Orientada a Objetos**, encapsulando tanto los datos como el comportamiento:

```javascript
class Particula {
  constructor(x, y, a) {
    // Propiedades de posición
    this.x = x;
    this.y = y;
    
    // Propiedades de velocidad (descompuesta en componentes)
    this.v = 0.5;
    this.vx = Math.cos(a) * this.v;  // Componente X
    this.vy = Math.sin(a) * this.v;  // Componente Y
    
    // Aceleración (resultado de fuerzas)
    this.ax = 0;
    this.ay = 0;
    
    // Identidad
    this.texto = nombres[Math.floor(Math.random()*nombres.length)];
    
    // Control de estabilidad (optimización)
    this.fija = false;
    this.estableFrames = 0;
  }
  
  // Métodos: interacciones(), mueve(), rebote(), dibuja(), lineas()
}
```

### Algoritmo de Interacciones - Paso a Paso

El método más crítico de mi implementación es `interacciones()`, que calcula todas las fuerzas sobre una partícula:

```javascript
interacciones(particulas) {
```

**PASO 1: Verificación de estado**
```javascript
  if (this.fija) {
    this.ax = 0;
    this.ay = 0;
    return;  // Optimización: partículas estables no calculan
  }
```

**PASO 2: Definición de parámetros**
```javascript
  let distanciaObjetivo = 120;         // Distancia ideal entre iguales
  let distanciaMinima = 80;            // Zona de seguridad
  let distanciaRepulsionDistinto = 200; // Rango de repulsión

  let kAtraccionIgual = 0.0012;
  let kRepulsionDistinto = 0.001;
  let kRepulsionCorta = 0.06;
```

**PASO 3: Inicializar acumuladores**
```javascript
  let fx = 0;  // Fuerza total en eje X
  let fy = 0;  // Fuerza total en eje Y
```

**PASO 4: Iterar sobre todas las demás partículas**
```javascript
  for (let p of particulas) {
    if (p === this) continue;  // No calcular fuerza sobre sí misma
    
    // Calcular distancia euclidiana
    let d = distance2D(this.x, this.y, p.x, p.y);
    if (d === 0) continue;
    
    // Calcular vector unitario (dirección de la fuerza)
    let dx = p.x - this.x;
    let dy = p.y - this.y;
    let ux = dx / d;  // Componente X normalizada
    let uy = dy / d;  // Componente Y normalizada
```

**PASO 5: Repulsión de seguridad (prioritaria)**
```javascript
    if (d < distanciaMinima) {
      let intensidad = (distanciaMinima - d) * kRepulsionCorta;
      fx -= ux * intensidad;  // Signo negativo = alejarse
      fy -= uy * intensidad;
      continue;  // No aplicar otras fuerzas
    }
```

**PASO 6: Fuerzas diferenciadas según tipo**
```javascript
    if (p.texto === this.texto) {
      // MISMO TIPO: Fuerza tipo muelle
      let delta = d - distanciaObjetivo;
      // Si d > objetivo → delta > 0 → atrae (acerca)
      // Si d < objetivo → delta < 0 → repele (aleja)
      fx += ux * delta * kAtraccionIgual;
      fy += uy * delta * kAtraccionIgual;
    } else {
      // DIFERENTE TIPO: Repulsión suave
      if (d < distanciaRepulsionDistinto) {
        let intensidad = (distanciaRepulsionDistinto - d) * kRepulsionDistinto;
        fx -= ux * intensidad;
        fy -= uy * intensidad;
      }
    }
  }
```

**PASO 7: Limitar fuerza máxima (estabilidad numérica)**
```javascript
  const maxForce = 0.05;
  let fmag = Math.sqrt(fx*fx + fy*fy);
  if (fmag > maxForce) {
    fx = fx / fmag * maxForce;
    fy = fy / fmag * maxForce;
  }
```

**PASO 8: Asignar fuerzas como aceleración**
```javascript
  this.ax = fx;
  this.ay = fy;
}
```

### Método de Movimiento

El método `mueve()` integra las ecuaciones de movimiento:

```javascript
mueve() {
  if (this.fija) return;
  
  // PASO 1: Actualizar velocidad con aceleración
  this.vx += this.ax;
  this.vy += this.ay;
  
  // PASO 2: Aplicar fricción
  const friccion = 0.93;
  this.vx *= friccion;
  this.vy *= friccion;
  
  // PASO 3: Actualizar posición con velocidad
  this.x += this.vx;
  this.y += this.vy;
  
  // PASO 4: Detectar estabilidad
  const speed = Math.sqrt(this.vx*this.vx + this.vy*this.vy);
  const fuerza = Math.sqrt(this.ax*this.ax + this.ay*this.ay);
  
  if (speed < 0.02 && fuerza < 0.002) {
    this.estableFrames++;
    if (this.estableFrames > 60) {  // 1 segundo estable
      this.fija = true;
      this.vx = 0;
      this.vy = 0;
    }
  } else {
    this.estableFrames = 0;
  }
}
```

### Gestión de Colisiones con Paredes

El método `rebote()` implementa colisiones inelásticas:

```javascript
rebote() {
  if (this.fija) return;
  
  const reboteFactor = -0.5;  // Coeficiente de restitución
  
  // Paredes verticales
  if (this.x > anchura) {
    this.x = anchura;
    this.vx *= reboteFactor;  // Invierte y reduce velocidad
  }
  if (this.x < 0) {
    this.x = 0;
    this.vx *= reboteFactor;
  }
  
  // Paredes horizontales
  if (this.y > altura) {
    this.y = altura;
    this.vy *= reboteFactor;
  }
  if (this.y < 0) {
    this.y = 0;
    this.vy *= reboteFactor;
  }
}
```

El factor de -0.5 significa:
- **Inversión de dirección** (signo negativo)
- **Pérdida del 50% de energía** (magnitud 0.5)

Esto simula un rebote **inelástico** realista.

### Ciclo Principal de Simulación

Mi bucle principal sigue el patrón estándar de **Game Loop**:

```javascript
function bucle() {
  if (!pausado) {
    // FASE 1: Limpiar canvas
    contexto.clearRect(0, 0, anchura, altura);
    
    // FASE 2: Calcular física
    for (let i = 0; i < particulas.length; i++) {
      particulas[i].interacciones(particulas);
    }
    
    // FASE 3: Actualizar posiciones
    for (let i = 0; i < particulas.length; i++) {
      particulas[i].mueve();
      particulas[i].rebote();
    }
    
    // FASE 4: Renderizar
    for (let i = 0; i < particulas.length; i++) {
      particulas[i].lineas();
    }
    for (let i = 0; i < particulas.length; i++) {
      particulas[i].dibuja();
    }
    
    // Actualizar estadísticas
    if (Math.random() < 0.1) {
      actualizarEstadisticas();
    }
  }
  
  requestAnimationFrame(bucle);
}
```

He separado claramente las fases de **cálculo** y **renderizado** para mantener la coherencia física.

### Terminología Técnica Utilizada

En mi implementación utilizo los siguientes conceptos técnicos:

- **Vector unitario** ($\hat{u}$): Vector de magnitud 1 que indica dirección
- **Distancia euclidiana**: $d = \sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}$
- **Integración numérica**: Método de Euler para resolver ecuaciones diferenciales
- **Coeficiente de restitución**: Fracción de energía conservada en colisión
- **Frame**: Unidad de tiempo en animación (1/60 segundo en mi caso)
- **Canvas API**: Interfaz de HTML5 para gráficos 2D
- **requestAnimationFrame**: API para sincronizar animaciones con el refresco del monitor

---

### Implementación Real del Sistema

He desarrollado el código completo en `actividad-particulas-interactivas.html`. A continuación muestro las secciones clave:

#### Función de Cálculo de Distancia

```javascript
function distance2D(x1, y1, x2, y2) {
  const dx = x2 - x1;
  const dy = y2 - y1;
  return Math.sqrt(dx * dx + dy * dy);
}
```

Esta función es la base de todo el sistema de detección de proximidad.

#### Inicialización del Sistema

```javascript
let particulas = [];
let numeroparticulas = 250;

function inicializarParticulas() {
  particulas = [];
  for(let i = 0; i < numeroparticulas; i++){
    particulas.push(
      new Particula(
        Math.random() * anchura,      // Posición X aleatoria
        Math.random() * altura,       // Posición Y aleatoria
        Math.random() * Math.PI * 2   // Ángulo aleatorio [0, 2π]
      )
    );
  }
}
```

Creo 250 partículas con posiciones y direcciones iniciales completamente aleatorias.

#### Visualización Mejorada

He implementado un sistema de visualización que diferencia el estado de las partículas:

```javascript
dibuja() {
  let anchopastilla = 20;
  let altopastilla = 10;
  
  contexto.beginPath();
  // ... dibujo de forma de pastilla ...
  
  // Color según estado
  contexto.fillStyle = this.fija ? "#e8f5e9" : "white";
  contexto.strokeStyle = this.fija ? "#4CAF50" : "black";
  contexto.lineWidth = this.fija ? 2 : 1;
  
  contexto.fill();
  contexto.stroke();
  
  // Texto identificador
  contexto.fillStyle = "black";
  contexto.fillText(this.texto, this.x, this.y);
}
```

Las partículas estables se muestran en **verde** para indicar que han alcanzado el equilibrio.

#### Sistema de Conexiones Visuales

```javascript
lineas() {
  for(let i = 0; i < particulas.length; i++){
    const p = particulas[i];
    if (p === this) continue;
    
    const d = distance2D(this.x, this.y, p.x, p.y);
    
    if(d < 160){
      // Diferente estilo según si son del mismo tipo
      let opacidad = (p.texto === this.texto) ? 0.6 : 0.2;
      let color = (p.texto === this.texto) ? "100,200,100" : "128,128,128";
      
      contexto.strokeStyle = `rgba(${color},${opacidad})`;
      contexto.lineWidth = (p.texto === this.texto) ? 1.5 : 0.5;
      contexto.beginPath();
      contexto.moveTo(this.x, this.y);
      contexto.lineTo(p.x, p.y);
      contexto.stroke();
    }
  }
}
```

Las líneas verdes más gruesas conectan partículas del mismo grupo, mientras que líneas grises finas muestran proximidad con diferentes tipos.

### Optimizaciones Implementadas

He incluido dos optimizaciones importantes:

#### A) Sistema de Partículas Fijas

```javascript
if (this.fija) {
  this.ax = 0;
  this.ay = 0;
  return;  // No calcular interacciones
}
```

Cuando una partícula ha estado estable durante 60 frames consecutivos, la marco como fija y deja de calcular fuerzas, reduciendo progresivamente la carga computacional.

#### B) Limitación de Fuerza Máxima

```javascript
const maxForce = 0.05;
let fmag = Math.sqrt(fx*fx + fy*fy);
if (fmag > maxForce) {
  fx = fx / fmag * maxForce;
  fy = fy / fmag * maxForce;
}
```

Esto evita **explosiones numéricas** que pueden ocurrir cuando múltiples partículas muy cercanas generan fuerzas extremadamente grandes.

### Interfaz de Usuario

He creado un panel informativo que muestra estadísticas en tiempo real:

```javascript
function actualizarEstadisticas() {
  let fijas = particulas.filter(p => p.fija).length;
  let movimiento = particulas.length - fijas;
  
  document.getElementById('total-particulas').textContent = particulas.length;
  document.getElementById('particulas-fijas').textContent = fijas;
  document.getElementById('particulas-movimiento').textContent = movimiento;
}
```

Y controles interactivos:

```javascript
function togglePause() {
  pausado = !pausado;
}

function reiniciar() {
  inicializarParticulas();
  pausado = false;
}
```

### Comportamiento Observado

Al ejecutar mi aplicación, observo estos patrones:

1. **Fase inicial (0-5 segundos)**: Caos total, partículas moviéndose rápidamente en todas direcciones
2. **Fase de agrupamiento (5-15 segundos)**: Las partículas con el mismo nombre comienzan a converger
3. **Fase de separación (15-30 segundos)**: Los grupos se separan entre sí
4. **Fase de estabilización (30-60 segundos)**: Las partículas alcanzan posiciones de equilibrio y se vuelven verdes
5. **Estado final**: 6 grupos claramente diferenciados, distribuidos por el canvas

### Errores Comunes y Soluciones

Durante el desarrollo encontré y resolví estos problemas:

#### Error 1: División por cero en vector unitario

**Problema:**
```javascript
let ux = (p.x - this.x) / d;  // Si d=0 → Infinity
```

**Solución:**
```javascript
if (d === 0) continue;  // Saltar si las partículas están exactamente en el mismo punto
```

#### Error 2: Partículas escapando del canvas

**Problema:** Sin rebote, las partículas desaparecían fuera de los límites.

**Solución:** Implementar el método `rebote()` con reposicionamiento:
```javascript
if (this.x > anchura) {
  this.x = anchura;  // Forzar dentro del borde
  this.vx *= -0.5;
}
```

#### Error 3: Inestabilidad numérica (partículas "explotando")

**Problema:** Fuerzas muy grandes causaban velocidades infinitas.

**Solución:** Limitar fuerza máxima:
```javascript
if (fmag > maxForce) {
  fx = fx / fmag * maxForce;
}
```

#### Error 4: Rendimiento degradado con 250 partículas

**Problema:** O(N²) = 62,500 cálculos por frame → lag visible.

**Solución:** Sistema de partículas fijas que reduce cálculos a medida que se estabiliza:
```javascript
if (speed < 0.02 && fuerza < 0.002) {
  this.estableFrames++;
  if (this.estableFrames > 60) {
    this.fija = true;  // Dejar de calcular
  }
}
```

#### Error 5: Grupos no se forman correctamente

**Problema:** Con `kAtraccionIgual` muy bajo, las partículas no se agrupaban.

**Solución:** Ajustar parámetros tras experimentación:
- `kAtraccionIgual = 0.0012` (suficientemente fuerte)
- `distanciaObjetivo = 120` (equilibrio adecuado)
- `friccion = 0.93` (permite convergencia)

### 3.6. Ejemplo de Uso en Contexto Real

Este tipo de sistema se puede aplicar en un videojuego de estrategia:

```javascript
// Ejemplo: Sistema de unidades que se agrupan por tipo
class Unidad extends Particula {
  constructor(x, y, tipo) {
    super(x, y, Math.random() * Math.PI * 2);
    this.tipo = tipo;  // "soldado", "arquero", "caballero"
    this.texto = tipo;
  }
  
  // Soldados se agrupan entre sí
  // Arqueros se agrupan entre sí
  // Se mantienen separados de otros tipos
  // Forma automática formaciones tácticas
}
```

O en visualización de datos:

```javascript
// Clustering de contenidos similares
class Documento extends Particula {
  constructor(x, y, categoria) {
    super(x, y, Math.random() * Math.PI * 2);
    this.categoria = categoria;
    this.texto = categoria;
  }
  
  // Documentos de la misma categoría se agrupan visualmente
  // Permite ver la estructura de un corpus de documentos
}
```

---

He implementado con éxito un **sistema de partículas con interacciones físicas** que integra:

- **Física computacional** (Método de Euler, sistemas de N-cuerpos)
- **Fuerzas diferenciadas** (atracción tipo muelle, repulsión)
- **Comportamiento emergente** (agrupamiento natural sin lógica explícita)
- **Optimización** (partículas fijas, limitación de fuerzas)

Este proyecto consolida conceptos de los ejercicios 101 (red de elementos, líneas, bucle animado, movimiento, rebote, agrupamiento y estabilidad) aplicando los principios de **Programación Multimedia** (Canvas API), **Desarrollo de Juegos** (Game Loop, física) y **Fases de Desarrollo** (diseño, implementación, optimización).

El aprendizaje más valioso ha sido comprender cómo **reglas locales simples** (atracción/repulsión) generan **patrones globales complejos** (grupos auto-organizados). También he entendido la importancia de la **estabilidad numérica** y el trade-off entre precisión y rendimiento en sistemas O(N²).

Las mejoras futuras incluyen Spatial Hashing para optimización, Verlet Integration para mejor estabilidad, y controles interactivos con el mouse. Este proyecto proporciona una base sólida para sistemas de partículas en videojuegos y visualización de datos.
