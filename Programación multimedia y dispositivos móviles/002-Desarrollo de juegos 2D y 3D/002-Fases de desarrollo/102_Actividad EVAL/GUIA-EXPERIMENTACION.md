# 🧪 Guía de Experimentación y Ejercicios Prácticos

## 📋 Introducción

Esta guía proporciona ejercicios prácticos para profundizar en el entendimiento del sistema de partículas. Cada ejercicio está diseñado para explorar un concepto específico y desarrollar habilidades de programación experimental.

---

## 🎯 Ejercicios Básicos

### Ejercicio 1: Modificar el Número de Partículas

**Objetivo**: Entender el impacto de N en el rendimiento.

**Instrucciones**:
1. Abre el archivo HTML en un editor
2. Localiza la línea: `let numeroparticulas = 250;`
3. Prueba con diferentes valores: 50, 100, 500, 1000
4. Observa y anota:
   - Tiempo hasta la estabilización
   - Rendimiento (FPS) en cada caso
   - Calidad de los grupos formados

**Pregunta reflexiva**: ¿Por qué el rendimiento disminuye cuadráticamente con N?

---

### Ejercicio 2: Cambiar los Nombres

**Objetivo**: Experimentar con diferentes números de grupos.

**Instrucciones**:
1. Localiza: `let nombres = ['Juan','Julia','Jorge','Jaime','Jose','Julian'];`
2. Prueba combinaciones:
   ```javascript
   // 2 grupos
   let nombres = ['Grupo1', 'Grupo2'];
   
   // 10 grupos
   let nombres = ['A','B','C','D','E','F','G','H','I','J'];
   
   // 1 grupo (todas iguales)
   let nombres = ['Todas'];
   ```
3. Observa los patrones de agrupamiento

**Pregunta reflexiva**: ¿Cómo afecta el número de grupos a la estructura final?

---

### Ejercicio 3: Ajustar la Distancia Objetivo

**Objetivo**: Comprender el parámetro de equilibrio.

**Instrucciones**:
1. En el método `interacciones()`, localiza:
   ```javascript
   let distanciaObjetivo = 120;
   ```
2. Prueba valores: 50, 80, 150, 200
3. Observa:
   - Densidad de los grupos
   - Tamaño de los grupos
   - Tiempo de estabilización

**Pregunta reflexiva**: ¿Qué valor produce la organización más clara?

---

### Ejercicio 4: Modificar la Fricción

**Objetivo**: Entender la amortiguación del sistema.

**Instrucciones**:
1. En el método `mueve()`, localiza:
   ```javascript
   const friccion = 0.93;
   ```
2. Prueba valores:
   - 0.99 (poca fricción)
   - 0.90 (fricción moderada)
   - 0.80 (mucha fricción)
   - 1.00 (sin fricción) ⚠️
3. Observa el comportamiento

**Pregunta reflexiva**: ¿Qué sucede sin fricción? ¿Por qué?

---

## 🚀 Ejercicios Intermedios

### Ejercicio 5: Añadir Gravedad

**Objetivo**: Incorporar una fuerza constante.

**Instrucciones**:
1. En el método `mueve()`, después de aplicar fuerzas:
   ```javascript
   // Añadir gravedad
   this.ay += 0.005; // Fuerza hacia abajo
   ```
2. Ajusta el rebote del suelo para compensar:
   ```javascript
   const reboteFactor = -0.7; // Más elástico
   ```
3. Observa cómo los grupos tienden a caer

**Desafío**: Implementa una "anti-gravedad" que active al presionar una tecla.

---

### Ejercicio 6: Colores por Grupo

**Objetivo**: Mejorar la visualización diferenciando grupos.

**Instrucciones**:
1. Crea un objeto de colores:
   ```javascript
   const coloresPorNombre = {
     'Juan': '#FF6B6B',
     'Julia': '#4ECDC4',
     'Jorge': '#FFD93D',
     'Jaime': '#95E1D3',
     'Jose': '#F38181',
     'Julian': '#AA96DA'
   };
   ```
2. En el método `dibuja()`, usa:
   ```javascript
   contexto.fillStyle = this.fija ? coloresPorNombre[this.texto] : "white";
   ```

**Desafío**: Haz que el color cambie gradualmente según la velocidad.

---

### Ejercicio 7: Sistema de Tamaños Variables

**Objetivo**: Añadir más diversidad a las partículas.

**Instrucciones**:
1. En el constructor, añade:
   ```javascript
   this.tamaño = 0.5 + Math.random() * 1.5; // 0.5 a 2.0
   ```
2. Modifica `dibuja()` para usar el tamaño:
   ```javascript
   let anchopastilla = 20 * this.tamaño;
   let altopastilla = 10 * this.tamaño;
   ```
3. Ajusta las fuerzas considerando el tamaño:
   ```javascript
   // En interacciones(), la masa afecta la inercia
   this.ax = fx / this.tamaño; // Partículas grandes son más "pesadas"
   ```

**Pregunta reflexiva**: ¿Cómo cambia la dinámica del sistema?

---

### Ejercicio 8: Detección de Clústeres

**Objetivo**: Identificar y contar grupos formados.

**Instrucciones**:
1. Implementa una función de análisis:
   ```javascript
   function analizarClusters() {
     let clusters = {};
     
     for (let p of particulas) {
       if (!clusters[p.texto]) {
         clusters[p.texto] = [];
       }
       clusters[p.texto].push(p);
     }
     
     // Calcular centro de masa de cada cluster
     for (let nombre in clusters) {
       let grupo = clusters[nombre];
       let cx = 0, cy = 0;
       for (let p of grupo) {
         cx += p.x;
         cy += p.y;
       }
       cx /= grupo.length;
       cy /= grupo.length;
       
       console.log(`${nombre}: ${grupo.length} partículas en (${cx.toFixed(0)}, ${cy.toFixed(0)})`);
     }
   }
   ```
2. Llámala periódicamente desde el bucle principal

**Desafío**: Dibuja círculos alrededor de cada clúster identificado.

---

## 🎨 Ejercicios Avanzados

### Ejercicio 9: Implementar Spatial Hashing

**Objetivo**: Optimizar el algoritmo de O(N²) a O(N).

**Instrucciones**:
1. Crea una estructura de cuadrícula:
   ```javascript
   class Grid {
     constructor(cellSize) {
       this.cellSize = cellSize;
       this.cells = {};
     }
     
     getKey(x, y) {
       let cx = Math.floor(x / this.cellSize);
       let cy = Math.floor(y / this.cellSize);
       return `${cx},${cy}`;
     }
     
     insert(particle) {
       let key = this.getKey(particle.x, particle.y);
       if (!this.cells[key]) this.cells[key] = [];
       this.cells[key].push(particle);
     }
     
     getNearby(particle) {
       let nearby = [];
       let cx = Math.floor(particle.x / this.cellSize);
       let cy = Math.floor(particle.y / this.cellSize);
       
       // Buscar en 9 celdas (3x3 alrededor)
       for (let dx = -1; dx <= 1; dx++) {
         for (let dy = -1; dy <= 1; dy++) {
           let key = `${cx+dx},${cy+dy}`;
           if (this.cells[key]) {
             nearby.push(...this.cells[key]);
           }
         }
       }
       return nearby;
     }
     
     clear() {
       this.cells = {};
     }
   }
   ```

2. Úsala en el bucle principal:
   ```javascript
   let grid = new Grid(200); // Tamaño de celda
   
   function bucle() {
     // ... limpiar canvas ...
     
     // Construir grid
     grid.clear();
     for (let p of particulas) {
       grid.insert(p);
     }
     
     // Calcular fuerzas solo con vecinos
     for (let p of particulas) {
       let vecinos = grid.getNearby(p);
       p.interacciones(vecinos); // Modificar para aceptar subconjunto
     }
     
     // ... resto del bucle ...
   }
   ```

**Medición**: Compara el rendimiento antes y después con 1000 partículas.

---

### Ejercicio 10: Integración Verlet

**Objetivo**: Implementar un método de integración más estable.

**Instrucciones**:
1. Modifica el constructor:
   ```javascript
   this.x_anterior = x;
   this.y_anterior = y;
   ```

2. Reemplaza el método `mueve()`:
   ```javascript
   mueve() {
     if (this.fija) return;
     
     // Método Verlet
     let x_temp = this.x;
     let y_temp = this.y;
     
     // x_nuevo = 2*x_actual - x_anterior + a*dt²
     this.x = 2 * this.x - this.x_anterior + this.ax;
     this.y = 2 * this.y - this.y_anterior + this.ay;
     
     // Aplicar fricción (amortiguación)
     const damping = 0.98;
     this.x = this.x * damping + (1 - damping) * x_temp;
     this.y = this.y * damping + (1 - damping) * y_temp;
     
     this.x_anterior = x_temp;
     this.y_anterior = y_temp;
     
     // Detección de estabilidad (calcular velocidad implícita)
     let vx_implicito = this.x - this.x_anterior;
     let vy_implicito = this.y - this.y_anterior;
     let speed = Math.sqrt(vx_implicito*vx_implicito + vy_implicito*vy_implicito);
     
     // ... resto de la detección de estabilidad ...
   }
   ```

**Comparación**: ¿Es el sistema más estable? ¿Puedes usar fuerzas más grandes?

---

### Ejercicio 11: Interacción con el Mouse

**Objetivo**: Añadir interactividad directa.

**Instrucciones**:
1. Añade un "atractor" controlado por el mouse:
   ```javascript
   let mouseX = 0;
   let mouseY = 0;
   let mouseDown = false;
   
   lienzo.addEventListener('mousemove', (e) => {
     mouseX = e.clientX;
     mouseY = e.clientY;
   });
   
   lienzo.addEventListener('mousedown', () => {
     mouseDown = true;
   });
   
   lienzo.addEventListener('mouseup', () => {
     mouseDown = false;
   });
   ```

2. En el método `interacciones()`, añade:
   ```javascript
   if (mouseDown) {
     let d = distance2D(this.x, this.y, mouseX, mouseY);
     if (d > 10) { // Evitar división por cero
       let ux = (mouseX - this.x) / d;
       let uy = (mouseY - this.y) / d;
       let fuerza = 0.02; // Intensidad de atracción
       fx += ux * fuerza;
       fy += uy * fuerza;
     }
   }
   ```

3. Dibuja el cursor:
   ```javascript
   if (mouseDown) {
     contexto.beginPath();
     contexto.arc(mouseX, mouseY, 15, 0, Math.PI * 2);
     contexto.fillStyle = "rgba(255, 100, 100, 0.5)";
     contexto.fill();
   }
   ```

**Variación**: Implementa repulsión cuando se presiona la tecla Shift.

---

### Ejercicio 12: Física de Colisiones entre Partículas

**Objetivo**: Implementar colisiones realistas.

**Instrucciones**:
1. En el método `interacciones()`, detecta colisiones:
   ```javascript
   for (let p of particulas) {
     if (p === this) continue;
     
     let d = distance2D(this.x, this.y, p.x, p.y);
     let radioTotal = 25 + 25; // Radio de ambas partículas
     
     if (d < radioTotal && d > 0) {
       // COLISIÓN DETECTADA
       
       // Separar partículas
       let overlap = radioTotal - d;
       let dx = p.x - this.x;
       let dy = p.y - this.y;
       let ux = dx / d;
       let uy = dy / d;
       
       this.x -= ux * overlap * 0.5;
       this.y -= uy * overlap * 0.5;
       p.x += ux * overlap * 0.5;
       p.y += uy * overlap * 0.5;
       
       // Intercambio de momento (colisión elástica simplificada)
       let vx_rel = this.vx - p.vx;
       let vy_rel = this.vy - p.vy;
       let velocidadRelativa = vx_rel * ux + vy_rel * uy;
       
       if (velocidadRelativa < 0) continue; // Ya se están alejando
       
       let coeficiente = 0.8; // Elasticidad
       let impulso = -(1 + coeficiente) * velocidadRelativa;
       
       this.vx += impulso * ux * 0.5;
       this.vy += impulso * uy * 0.5;
       p.vx -= impulso * ux * 0.5;
       p.vy -= impulso * uy * 0.5;
     }
   }
   ```

**Nota**: Este código debe ejecutarse en una fase separada para evitar inconsistencias.

---

## 📊 Ejercicios de Análisis

### Ejercicio 13: Medición de Rendimiento

**Objetivo**: Cuantificar el impacto de optimizaciones.

**Instrucciones**:
1. Añade medición de tiempo:
   ```javascript
   let tiempoTotal = 0;
   let frames = 0;
   
   function bucle() {
     let inicio = performance.now();
     
     // ... código del bucle ...
     
     let fin = performance.now();
     tiempoTotal += (fin - inicio);
     frames++;
     
     if (frames % 60 === 0) {
       let promedio = tiempoTotal / frames;
       console.log(`Tiempo promedio por frame: ${promedio.toFixed(2)}ms`);
       console.log(`FPS estimados: ${(1000/promedio).toFixed(0)}`);
     }
     
     requestAnimationFrame(bucle);
   }
   ```

2. Compara:
   - Sin optimizaciones (N² completo)
   - Con partículas fijas
   - Con spatial hashing

**Objetivo**: Crear una tabla comparativa.

---

### Ejercicio 14: Visualización de Fuerzas

**Objetivo**: Entender las fuerzas actuantes.

**Instrucciones**:
1. Dibuja vectores de fuerza:
   ```javascript
   dibujaFuerzas() {
     if (this.fija) return;
     
     let escala = 500; // Factor de escala para visualizar
     let fx_visual = this.ax * escala;
     let fy_visual = this.ay * escala;
     
     contexto.strokeStyle = "rgba(255, 0, 0, 0.6)";
     contexto.lineWidth = 2;
     contexto.beginPath();
     contexto.moveTo(this.x, this.y);
     contexto.lineTo(this.x + fx_visual, this.y + fy_visual);
     contexto.stroke();
     
     // Punta de flecha
     let angulo = Math.atan2(fy_visual, fx_visual);
     let longitud = 8;
     contexto.beginPath();
     contexto.moveTo(this.x + fx_visual, this.y + fy_visual);
     contexto.lineTo(
       this.x + fx_visual - longitud * Math.cos(angulo - Math.PI/6),
       this.y + fy_visual - longitud * Math.sin(angulo - Math.PI/6)
     );
     contexto.lineTo(
       this.x + fx_visual - longitud * Math.cos(angulo + Math.PI/6),
       this.y + fy_visual - longitud * Math.sin(angulo + Math.PI/6)
     );
     contexto.closePath();
     contexto.fill();
   }
   ```

2. Llama a este método en el bucle de renderizado.

**Pregunta**: ¿Qué patrones observas en las fuerzas?

---

## 🎯 Proyecto Final: Sistema Completo

### Ejercicio 15: Simulador de Opiniones/Polarización

**Objetivo**: Crear una aplicación completa basada en los conceptos aprendidos.

**Descripción**:
Simula la polarización de opiniones en una sociedad:
- Cada partícula representa una persona con una opinión (1-10)
- Personas con opiniones similares se atraen
- Personas con opiniones opuestas se repelen
- Las opiniones pueden cambiar ligeramente con las interacciones

**Instrucciones**:
1. Modifica el constructor:
   ```javascript
   this.opinion = 1 + Math.random() * 9; // 1 a 10
   this.color = this.getColorFromOpinion();
   ```

2. Implementa el color basado en opinión:
   ```javascript
   getColorFromOpinion() {
     // Gradiente de azul (1) a rojo (10)
     let ratio = (this.opinion - 1) / 9;
     let r = Math.floor(255 * ratio);
     let b = Math.floor(255 * (1 - ratio));
     return `rgb(${r}, 100, ${b})`;
   }
   ```

3. Modifica las interacciones:
   ```javascript
   let diferenciaOpinion = Math.abs(this.opinion - p.opinion);
   
   if (diferenciaOpinion < 2) {
     // Opiniones similares: atracción
     let delta = d - distanciaObjetivo;
     fx += ux * delta * kAtraccion;
     fy += uy * delta * kAtraccion;
     
     // Convergencia de opiniones
     if (d < 100 && Math.random() < 0.001) {
       this.opinion = (this.opinion + p.opinion) / 2;
       this.color = this.getColorFromOpinion();
     }
   } else if (diferenciaOpinion > 5) {
     // Opiniones opuestas: repulsión
     fx -= ux * kRepulsion;
     fy -= uy * kRepulsion;
   }
   ```

4. Añade controles para:
   - "Introducir un influencer" (partícula especial fuerte)
   - "Evento polarizante" (empujar opiniones a extremos)
   - Medir la "polarización total" del sistema

**Entregable**: Documento explicando los resultados y patrones observados.

---

## 📈 Tabla de Seguimiento

| Ejercicio | Completado | Dificultad | Notas |
|-----------|------------|------------|-------|
| 1. Número de partículas | ⬜ | ⭐ | |
| 2. Cambiar nombres | ⬜ | ⭐ | |
| 3. Distancia objetivo | ⬜ | ⭐ | |
| 4. Fricción | ⬜ | ⭐⭐ | |
| 5. Gravedad | ⬜ | ⭐⭐ | |
| 6. Colores por grupo | ⬜ | ⭐⭐ | |
| 7. Tamaños variables | ⬜ | ⭐⭐⭐ | |
| 8. Detección de clústeres | ⬜ | ⭐⭐⭐ | |
| 9. Spatial Hashing | ⬜ | ⭐⭐⭐⭐ | |
| 10. Verlet Integration | ⬜ | ⭐⭐⭐⭐ | |
| 11. Mouse Interaction | ⬜ | ⭐⭐⭐ | |
| 12. Colisiones | ⬜ | ⭐⭐⭐⭐ | |
| 13. Medición rendimiento | ⬜ | ⭐⭐ | |
| 14. Visualización fuerzas | ⬜ | ⭐⭐⭐ | |
| 15. Proyecto final | ⬜ | ⭐⭐⭐⭐⭐ | |

---

## 💡 Consejos Generales

1. **Cambia un parámetro a la vez**: Así entenderás el efecto de cada variable
2. **Usa console.log()**: Para depurar y entender el flujo
3. **Guarda versiones**: Copia el archivo antes de hacer cambios grandes
4. **Experimenta**: No tengas miedo de romper cosas, ¡aprenderás más!
5. **Documenta tus observaciones**: Lleva un registro de lo que descubres

---

## 🎓 Criterios de Evaluación

Si esta fuera una actividad evaluable, se valoraría:

- **Experimentación (30%)**: Número y profundidad de ejercicios completados
- **Comprensión (25%)**: Respuestas a preguntas reflexivas
- **Creatividad (20%)**: Implementaciones originales o mejoras propuestas
- **Documentación (15%)**: Claridad en la explicación de cambios
- **Optimización (10%)**: Mejoras medibles en rendimiento

---

**¡Disfruta experimentando y descubriendo los principios que gobiernan los sistemas complejos!** 🚀