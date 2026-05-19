En esta actividad he implementado una **visualización 3D interactiva** que representa una red de personas con sus características (nombre, edad, ciudad, profesión, hobbies) como nodos en un espacio tridimensional. La aplicación utiliza **A-Frame 1.5.0**, un framework de realidad virtual para la web que facilita la creación de experiencias 3D mediante HTML.

El concepto general consiste en crear un sistema de **grafos 3D con física de partículas**, donde cada persona es representada como un nodo (cápsula transparente con etiqueta de texto) y las conexiones entre personas se establecen dinámicamente según las propiedades que comparten. Este tipo de visualización sirve para **representar relaciones complejas de forma visual e intuitiva**, permitiendo identificar patrones, agrupaciones y conexiones entre datos que serían difíciles de percibir en un formato tradicional de tabla o lista.

Se utiliza en contextos como:
- **Análisis de redes sociales**: visualizar conexiones entre personas
- **Exploración de datos**: identificar patrones y agrupaciones
- **Presentaciones interactivas**: hacer los datos más accesibles y comprensibles
- **Visualización científica**: representar sistemas complejos con múltiples variables

---

### Arquitectura del Sistema

He estructurado la aplicación en varios componentes técnicos clave:

#### **A. Componentes Personalizados de A-Frame**

**1. Shader de Gradiente para el Cielo**
```javascript
AFRAME.registerShader('gradiente', {
  schema: {
    topColor:    {type: 'color', default: '#88c8ff'},
    bottomColor: {type: 'color', default: '#02041a'}
  }
})
```
He creado un **shader personalizado** utilizando **GLSL (OpenGL Shading Language)** que genera un degradado vertical en el cielo. Los shaders son programas que se ejecutan directamente en la GPU y permiten efectos visuales avanzados. En este caso:
- El **vertex shader** calcula la posición mundial de cada vértice
- El **fragment shader** interpola linealmente entre dos colores basándose en la altura (eje Y)
- Uso `THREE.BackSide` para renderizar el interior de la esfera del cielo

**2. Componente Billboard**
```javascript
AFRAME.registerComponent('billboard', {
  tick: function () {
    const camPos = new THREE.Vector3();
    this.camEl.object3D.getWorldPosition(camPos);
    obj.lookAt(camPos);
  }
});
```
Implemento la técnica de **billboarding**, que hace que las etiquetas de texto siempre miren hacia la cámara. Esto es crucial para la legibilidad en entornos 3D. La función `tick()` se ejecuta en cada frame (60 veces por segundo), actualizando continuamente la rotación del objeto para que siempre encare al observador.

**3. Componente de Transparencia para Cápsulas**
```javascript
AFRAME.registerComponent('transparente-capsula', {
  schema: { opacity: { type: 'number', default: 0.25 } },
  init: function () {
    el.object3D.traverse(obj => {
      if (obj.isMesh && obj.material) {
        const m = obj.material;
        m.transparent = true;
        m.opacity = self.data.opacity;
        m.depthWrite = false;
        m.side = THREE.DoubleSide;
      }
    });
  }
});
```
Este componente configura las propiedades del material Three.js para lograr transparencia correcta:
- `transparent = true`: habilita el alpha blending
- `depthWrite = false`: previene problemas de ordenamiento con objetos transparentes
- `depthTest = true`: mantiene el test de profundidad para oclusión correcta
- `DoubleSide`: renderiza ambas caras del material

#### **B. Sistema de Física de Partículas**

He implementado un **motor de física personalizado** basado en fuerzas newtonianas:

**Cálculo de Fuerzas**
```javascript
const propsCoinciden = [];
for (const prop of clavesPropiedades) {
  if (!usarEnRelacion[prop]) continue;
  if (p.datos[prop] === q.datos[prop]) {
    propsCoinciden.push(prop);
  }
}
```

El sistema evalúa tres tipos de fuerzas entre cada par de partículas:

1. **Fuerza de Repulsión de Corto Alcance**
   - Actúa cuando dos nodos están demasiado cerca (< 1.8 unidades)
   - Previene solapamiento y mantiene separación mínima
   - Intensidad: `K_REPULSION_CORTA = 0.06` (la más fuerte)

2. **Fuerza de Atracción por Propiedades Compartidas**
   - **Atracción fuerte** (2+ propiedades coincidentes): `K = 0.0015`
   - **Atracción media** (1 propiedad coincidente): `K = 0.0009`
   - Busca mantener distancia objetivo de 6 unidades
   - Formula: `F = k × Δd × û` donde Δd es la diferencia con la distancia deseada

3. **Fuerza de Repulsión entre Distintos**
   - Actúa cuando no comparten propiedades (< 14 unidades)
   - Mantiene grupos separados naturalmente
   - Intensidad: `K_REPULSION_DISTINTO = 0.001`

**Integración Numérica Semi-Implícita de Euler**
```javascript
p.vx += p.ax;  // Actualizar velocidad con aceleración
p.vx *= FRICCION;  // Aplicar amortiguamiento (0.93)
p.x += p.vx;  // Actualizar posición con velocidad
```

Este método de integración es **simple pero efectivo** para simulaciones en tiempo real. La fricción (`0.93`) disipa energía gradualmente, haciendo que el sistema converja a un estado estable.

**Detección de Estabilidad**
```javascript
const vel  = Math.sqrt(p.vx*p.vx + p.vy*p.vy + p.vz*p.vz);
const fuer = Math.sqrt(p.ax*p.ax + p.ay*p.ay + p.az*p.az);
if (vel < 0.02 && fuer < 0.002) {
  p.estableFrames++;
  if (p.estableFrames > 60) {
    p.fija = true;  // Congelar partícula estable
  }
}
```

Optimizo el rendimiento detectando cuando una partícula ha alcanzado equilibrio. Después de 60 frames sin movimiento significativo, la marco como `fija` y dejo de calcular física para ella.

#### **C. Sistema de Conexiones Dinámicas**

```javascript
function actualizarConexiones() {
  conexionesEl.innerHTML = "";
  const n = numeroParticulas;
  for (let i = 0; i < n; i++) {
    const a = particulas[i];
    const candidatos = [];
    
    for (let j = i+1; j < n; j++) {
      const b = particulas[j];
      const d = distancia3D(a.x,a.y,a.z, b.x,b.y,b.z);
      if (d > RADIO_CONEXION) continue;
      
      // Determinar propiedades compartidas
      const propsCoinciden = [];
      for (const prop of clavesPropiedades) {
        if (usarEnRelacion[prop] && a.datos[prop] === b.datos[prop]) {
          propsCoinciden.push(prop);
        }
      }
      
      // Generar color basado en hash de propiedades
      const clave = propsCoinciden.join("+");
      const h = hashCadena(clave) % 360;
      const color = `hsl(${h}, 70%, 50%)`;
      
      candidatos.push({j, d, color});
    }
    
    // Limitar conexiones por nodo
    candidatos.sort((a,b) => a.d - b.d);
    const limite = Math.min(maxConexionesPorNodo, candidatos.length);
  }
}
```

Las conexiones funcionan así:
1. Solo se conectan nodos dentro del **radio de conexión** (12 unidades)
2. Se identifican las propiedades compartidas
3. Se genera un **color único mediante hash** de las propiedades compartidas
4. Se limita el número de conexiones por nodo (configurable 1-6)
5. Se priorizan las conexiones más **cercanas** ordenando candidatos por distancia

**Función Hash para Colores Consistentes**
```javascript
function hashCadena(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = (hash * 31 + str.charCodeAt(i)) | 0;
  }
  return Math.abs(hash);
}
```

Esta función garantiza que dos nodos con las mismas propiedades compartidas siempre tendrán el mismo color de conexión, facilitando la identificación visual de relaciones.

#### **D. Sistema de Interacción**

**Sistema de Raycasting**
```javascript
<a-entity id="rig"
  camera
  cursor="rayOrigin: mouse; fuse: false"
  raycaster="objects: .clickable; far: 100">
</a-entity>
```

Configuro el **raycaster** para que lance un rayo desde el cursor del ratón e identifique objetos con clase `.clickable`. Esto permite interacción con el ratón en entornos 3D.

**Gestión de Eventos de Click**
```javascript
nodo.addEventListener("click", () => {
  zoomACentroDeParticula(pObj);
  const tituloModal = categorias.nombre || "Detalle de nodo";
  mostrarModal(tituloModal, contenidoHtml);
});
```

Cuando se hace click en un nodo:
1. Se activa una **animación de zoom suave** hacia el nodo
2. Se muestra un **modal 2D superpuesto** con información detallada
3. Se usa **interpolación ease-in-out** para movimiento fluido

**Animación de Zoom con Interpolación**
```javascript
function actualizarZoom(dt) {
  if (!zoomAnim) return;
  zoomAnim.t += dt / zoomAnim.dur;
  let t = zoomAnim.t;
  if (t >= 1) t = 1;
  const ease = t < 0.5 ? 2*t*t : -1 + (4 - 2*t)*t;  // ease-in-out cuadrática
  const pos = new THREE.Vector3().lerpVectors(zoomAnim.from, zoomAnim.to, ease);
  rigEl.object3D.position.copy(pos);
}
```

La función de easing `ease-in-out` proporciona aceleración al inicio y desaceleración al final, creando un movimiento más natural y profesional.

#### **E. Sistema de Controles de Navegación Fly**

```javascript
const flyEstado = { adelante:0, atras:0, izquierda:0, derecha:0, arriba:0, abajo:0 };

function actualizarFly(dt) {
  const obj = rigEl.object3D;
  const dir = new THREE.Vector3();
  obj.getWorldDirection(dir);
  
  const up = new THREE.Vector3(0,1,0);
  const right = new THREE.Vector3().crossVectors(dir, up).normalize().negate();
  
  let move = new THREE.Vector3(0,0,0);
  if (flyEstado.adelante) move.add(dir.clone().multiplyScalar(-1));
  if (flyEstado.derecha) move.add(right);
  // ... etc
  
  if (move.lengthSq() > 0) {
    move.normalize().multiplyScalar(VELOCIDAD_FLY * dt);
    obj.position.add(move);
  }
}
```

Implemento un sistema **fly-controls** completo:
- Uso **W/A/S/D** para movimiento en plano horizontal
- **Q/E** para subir/bajar en eje Y
- Calculo vectores de dirección usando **producto vectorial** (`crossVectors`)
- Normalizo el movimiento para velocidad constante independiente de la dirección
- Multiplico por `dt` (delta time) para que sea **independiente del framerate**

#### **F. Interfaz de Usuario Dinámica**

He creado controles que se generan dinámicamente según las propiedades detectadas en los datos JSON:

```javascript
function crearControlesPropiedades(claves) {
  clavesPropiedades = claves.slice();
  
  clavesPropiedades.forEach(prop => {
    const bloque = document.createElement("div");
    
    // Checkbox "Usar en relación"
    const chkUsar = document.createElement("input");
    chkUsar.type = "checkbox";
    chkUsar.checked = usarEnRelacion[prop];
    chkUsar.addEventListener("change", () => {
      usarEnRelacion[prop] = chkUsar.checked;
      particulas.forEach(p => { p.fija = false; p.estableFrames = 0; });
    });
    
    // Checkbox "Mostrar en etiqueta"
    const chkMostrar = document.createElement("input");
    chkMostrar.addEventListener("change", () => {
      mostrarEnEtiqueta[prop] = chkMostrar.checked;
      etiquetasSucias = true;  // Marca para regenerar etiquetas
    });
  });
}
```

Este sistema es **completamente genérico**: detecta automáticamente todas las propiedades en el JSON y genera controles para cada una, sin necesidad de hardcodear nada.

### Terminología Técnica Relevante

- **A-Frame**: Framework declarativo para crear experiencias de realidad virtual en la web usando HTML
- **Entity-Component-System (ECS)**: Patrón de diseño usado por A-Frame donde las entidades son contenedores, los componentes definen comportamiento
- **Three.js**: Motor de renderizado WebGL en el que se basa A-Frame
- **WebGL**: API de JavaScript para renderizar gráficos 3D acelerados por hardware
- **Shader**: Programa que se ejecuta en la GPU para calcular renderizado de vértices y píxeles
- **Billboard**: Técnica de renderizado donde un objeto 2D siempre mira hacia la cámara
- **Raycasting**: Técnica para detectar intersecciones entre un rayo y objetos de la escena
- **Sistema de partículas**: Técnica de simulación que modela el comportamiento colectivo de muchos objetos pequeños
- **Integración numérica**: Métodos para resolver ecuaciones diferenciales aproximadamente
- **Fricción/Damping**: Fuerza que disipa energía del sistema
- **Delta Time (dt)**: Tiempo transcurrido entre frames, usado para independencia del framerate

### Funcionamiento Paso a Paso

1. **Carga Inicial**
   ```javascript
   fetch("personas2.json")
     .then(r => r.json())
     .then(items => {
       const setClaves = new Set();
       items.forEach(item => {
         Object.keys(item.categories).forEach(k => setClaves.add(k));
       });
       crearControlesPropiedades(Array.from(setClaves));
       crearNodos3D(items);
       requestAnimationFrame(bucle);
     });
   ```
   - Cargo el archivo **personas2.json** con fetch API
   - Extraigo todas las claves únicas de propiedades (nombre, hobbie, edad, etc.)
   - Genero dinámicamente la interfaz de controles
   - Creo los nodos 3D en posiciones aleatorias
   - Inicio el bucle principal de renderizado

2. **Creación de Nodos 3D**
   ```javascript
   const x = (Math.random() - 0.5) * LIM_X * 2;
   const y = Math.random() * LIM_Y + 1;
   const z = (Math.random() - 0.5) * LIM_Z * 2;
   ```
   - Asigno posiciones iniciales **aleatorias** dentro de límites (-20 a 20 en X/Z, 0.5 a 10 en Y)
   - Creo una **cápsula transparente horizontal** (cilindro + 2 esferas)
   - Añado **entidad de texto** con billboard
   - Asigno velocidad inicial pequeña y aleatoria
   - Registro el manejador de eventos click

3. **Bucle Principal de Simulación**
   ```javascript
   function bucle(tiempoMs) {
     const dt = (tiempoMs - ultimoTiempo) / 1000;
     
     pasoFisica(dt);
     actualizarFly(dt);
     actualizarZoom(dt);
     
     contadorFrames++;
     if (contadorFrames % ACTUALIZAR_LINEAS_CADA === 0) {
       actualizarConexiones();
     }
     
     requestAnimationFrame(bucle);
   }
   ```
   - Calculo **delta time** para independencia del framerate
   - Actualizo física de partículas
   - Proceso controles de navegación fly
   - Actualizo animación de zoom si está activa
   - Regenero líneas de conexión **cada 10 frames** (optimización)
   - Solicito siguiente frame de animación

4. **Iteración de Física**
   - Para cada partícula no fija:
     - Reseteo acumuladores de fuerza (ax, ay, az)
     - Evalúo fuerzas con todas las demás partículas
     - Sumo fuerzas vectorialmente
     - Limito magnitud de fuerza a MAX_FUERZA
     - Integro aceleración → velocidad → posición
     - Aplico fricción (multiplicar velocidad por 0.93)
     - Detecto y resuelvo colisiones con límites (rebotes)
     - Verifico condiciones de estabilidad
     - Actualizo posición del nodo en A-Frame

5. **Actualización de Conexiones**
   - Vacío contenedor de líneas
   - Evalúo todas las combinaciones de pares de nodos
   - Filtro por distancia (< RADIO_CONEXION)
   - Determino propiedades compartidas
   - Genero color mediante hash
   - Ordeno candidatos por distancia
   - Creo entidades `<a-entity line>` para las N conexiones más cercanas
   - Renderizo en la escena

6. **Interacción del Usuario**
   - **Navegación**: Los event listeners de teclado actualizan `flyEstado`
   - **Controles UI**: Los sliders y checkboxes modifican variables globales
   - **Click en nodo**: 
     - Raycaster detecta intersección
     - Se dispara evento click
     - Inicio animación de zoom
     - Muestro modal con contenido HTML
   - **Modificación de propiedades**: Al cambiar checkboxes, se desmarcan nodos como fijos para recalcular relaciones

---

### Ejemplo Real de Código: Carga y Visualización de Datos

Voy a mostrar cómo se usa el sistema completo con datos reales:

**Estructura del archivo personas2.json**
```json
[
  {
    "categories": {
      "nombre": "Juan",
      "hobbie": "Ajedrez",
      "edad": 20,
      "ciudad": "Valencia",
      "profesion": "Estudiante"
    },
    "content": "<h2>Juan (20)</h2><p><strong>Ciudad:</strong> Valencia<br><strong>Profesión:</strong> Estudiante<br><strong>Hobbie:</strong> Ajedrez</p>"
  },
  {
    "categories": {
      "nombre": "María",
      "hobbie": "Ajedrez",
      "edad": 22,
      "ciudad": "Madrid",
      "profesion": "Ingeniera"
    },
    "content": "<h2>María (22)</h2><p><strong>Ciudad:</strong> Madrid<br><strong>Profesión:</strong> Ingeniera<br><strong>Hobbie:</strong> Ajedrez</p>"
  }
]
```

**Flujo completo de visualización**:

1. **Carga de datos**
```javascript
fetch("personas2.json")
  .then(r => r.json())
  .then(items => {
    // Extraer propiedades únicas
    const setClaves = new Set();
    items.forEach(item => {
      const cats = item.categories || {};
      Object.keys(cats).forEach(k => setClaves.add(k));
    });
    // Resultado: ["nombre", "hobbie", "edad", "ciudad", "profesion"]
    
    const claves = Array.from(setClaves);
    crearControlesPropiedades(claves);
    crearNodos3D(items);
    requestAnimationFrame(bucle);
  });
```

2. **Creación de nodo específico**
```javascript
// Para Juan:
const nodo = document.createElement("a-entity");
nodo.setAttribute("position", `${x} ${y} ${z}`);  // ej: "5.2 3.8 -7.1"
nodo.setAttribute("billboard", "target: #rig");

// Cápsula transparente con cilindro + esferas
const capsula = crearCapsulaTransparenteHorizontal();
nodo.appendChild(capsula);

// Texto con propiedades visibles
const texto = document.createElement("a-entity");
texto.setAttribute("text", {
  value: "Juan\nAjedrez\n20\nValencia\nEstudiante",
  align: "center",
  color: "#ffffff",
  width: 3
});
nodo.appendChild(texto);

// Objeto de partícula en memoria
const pObj = {
  x:x, y:y, z:z,
  vx:0.05, vy:-0.03, vz:0.02,  // velocidad inicial aleatoria
  datos: {nombre:"Juan", hobbie:"Ajedrez", edad:20, ciudad:"Valencia", profesion:"Estudiante"},
  contenido: "<h2>Juan (20)</h2>...",
  nodeEl: nodo,
  fija: false
};
```

3. **Cálculo de conexiones entre Juan y María**
```javascript
// En actualizarConexiones():
const juan = particulas[0];  // {datos: {hobbie:"Ajedrez",...}}
const maria = particulas[1]; // {datos: {hobbie:"Ajedrez",...}}

const d = distancia3D(juan.x, juan.y, juan.z, maria.x, maria.y, maria.z);
// Resultado: d = 8.3 (dentro del radio de 12)

// Propiedades compartidas
const propsCoinciden = [];
for (const prop of ["nombre", "hobbie", "edad", "ciudad", "profesion"]) {
  if (usarEnRelacion[prop]) {
    if (juan.datos[prop] === maria.datos[prop]) {
      propsCoinciden.push(prop);
    }
  }
}
// Resultado: propsCoinciden = ["hobbie"]  (ambos tienen "Ajedrez")

// Generar color
const clave = "hobbie";
const h = hashCadena("hobbie") % 360;  // ej: 245
const color = `hsl(245, 70%, 50%)`;  // azul-violeta

// Crear línea
const lineaEl = document.createElement("a-entity");
lineaEl.setAttribute("line", {
  start: `${juan.x} ${juan.y} ${juan.z}`,
  end: `${maria.x} ${maria.y} ${maria.z}`,
  color: color
});
conexionesEl.appendChild(lineaEl);
```

4. **Física aplicada entre Juan y María**
```javascript
// En pasoFisica():
const juan = particulas[0];
const maria = particulas[1];

const d = 8.3;  // distancia actual
const dx = maria.x - juan.x;  // ej: 4.2
const dy = maria.y - juan.y;  // ej: -1.1
const dz = maria.z - juan.z;  // ej: -7.5

// Vector unitario
const ux = dx / d;  // 0.506
const uy = dy / d;  // -0.133
const uz = dz / d;  // -0.904

// Como comparten 1 propiedad (hobbie), aplicar atracción media
const DISTANCIA_OBJETIVO = 6;
const delta = d - DISTANCIA_OBJETIVO;  // 8.3 - 6 = 2.3
const K_ATRACCION_MEDIA = 0.0009;

// Fuerza de atracción
const fx = ux * delta * K_ATRACCION_MEDIA;  // 0.506 * 2.3 * 0.0009 = 0.00105
const fy = uy * delta * K_ATRACCION_MEDIA;  // -0.00028
const fz = uz * delta * K_ATRACCION_MEDIA;  // -0.00187

// Aplicar a Juan (María recibe fuerza opuesta)
juan.ax += fx;
juan.ay += fy;
juan.az += fz;

// En el paso de integración:
juan.vx += juan.ax;  // 0.05 + 0.00105 = 0.05105
juan.vx *= 0.93;     // 0.05105 * 0.93 = 0.0475
juan.x += juan.vx;   // 5.2 + 0.0475 = 5.2475

// Resultado: Juan se mueve ligeramente hacia María
```

### Casos de Uso Prácticos

**Caso 1: Análisis de una comunidad**
- Cargo datos de 100 personas con atributos (ciudad, profesión, hobbies)
- Activo solo las propiedades "hobbie" y "profesion" en los controles
- Observo cómo se forman **clusters naturales**: personas con hobbies similares se agrupan
- Los colores de conexión me permiten identificar rápidamente qué tipo de relación conecta a cada grupo

**Caso 2: Exploración de datos corporativos**
- Represento empleados de una empresa con datos (departamento, nivel, proyecto, localización)
- Navego por el espacio 3D usando WASD
- Hago click en nodos para ver detalles completos de cada empleado
- Identifico silos departamentales o proyectos con poca conexión interdepartamental

**Caso 3: Presentación interactiva**
- Preparo datos de asistentes a una conferencia
- Durante la presentación, ajusto dinámicamente los controles:
  - Aumento máximo de conexiones para mostrar red densa
  - Cambio transparencia de cápsulas para enfatizar conexiones
  - Activo/desactivo propiedades para mostrar diferentes perspectivas
- Uso el zoom automático al hacer click para destacar individuos específicos

### Errores Comunes y Cómo Evitarlos

**Error 1: Objetos transparentes renderizados incorrectamente**
```javascript
// ❌ INCORRECTO
m.transparent = true;
m.opacity = 0.25;
// Problema: objetos transparentes se renderizan en orden incorrecto

// ✅ CORRECTO
m.transparent = true;
m.opacity = 0.25;
m.depthWrite = false;  // Desactivar escritura de profundidad
m.depthTest = true;    // Mantener test de profundidad
m.side = THREE.DoubleSide;  // Renderizar ambas caras
```
**Explicación**: Los objetos transparentes en WebGL requieren configuración especial. `depthWrite=false` previene que escriban en el z-buffer, lo cual causaría que objetos detrás no sean visibles.

**Error 2: Billboard no funciona (texto no mira a la cámara)**
```javascript
// ❌ INCORRECTO
nodo.setAttribute("look-at", "[camera]");
// Problema: hace que todo el nodo mire a la cámara, deformando la cápsula

// ✅ CORRECTO
nodo.setAttribute("billboard", "target: #rig");
// Solo el nodo con texto usa billboard, cápsula mantiene orientación
```
**Explicación**: El billboarding debe aplicarse selectivamente solo a elementos que necesitan mirar a la cámara, no a todo el grupo.

**Error 3: Física inestable o explosiva**
```javascript
// ❌ INCORRECTO
p.vx += p.ax * 100;  // Factor muy grande
p.x += p.vx;

// ✅ CORRECTO
const MAX_FUERZA = 0.05;
if (modF > MAX_FUERZA) {
  fx = fx / modF * MAX_FUERZA;  // Limitar fuerza
}
p.vx += p.ax;
p.vx *= 0.93;  // Fricción para estabilidad
p.x += p.vx;
```
**Explicación**: Los sistemas de física de partículas requieren **limitación de fuerzas** y **amortiguamiento** para prevenir inestabilidades numéricas. Sin estos, las fuerzas pueden crecer exponencialmente causando que las partículas "exploten" o se vuelvan NaN.

**Error 4: Rendimiento degradado con muchas partículas**
```javascript
// ❌ INCORRECTO
function bucle() {
  actualizarConexiones();  // Regenerar todas las líneas en cada frame
  requestAnimationFrame(bucle);
}

// ✅ CORRECTO
contadorFrames++;
if (contadorFrames % ACTUALIZAR_LINEAS_CADA === 0) {
  actualizarConexiones();  // Solo cada 10 frames
}

// Además: detección de estabilidad
if (p.fija) continue;  // Saltar partículas estables
```
**Explicación**: Con N partículas, hay N² comparaciones por frame. **Optimizaciones críticas**:
- Actualizar conexiones cada N frames (ahorra manipulación DOM)
- Marcar partículas estables como `fija` (reduce cálculos)
- Usar radio de conexión limitado (evita comparar partículas muy lejanas)

**Error 5: Frames dependientes del tiempo (jerky movement)**
```javascript
// ❌ INCORRECTO
function actualizarFly() {
  if (flyEstado.adelante) {
    obj.position.z -= 0.1;  // Velocidad fija por frame
  }
}

// ✅ CORRECTO
function actualizarFly(dt) {
  if (flyEstado.adelante) {
    move.add(dir.clone().multiplyScalar(-VELOCIDAD_FLY * dt));
  }
}
```
**Explicación**: Multiplicar por `dt` (delta time) hace que el movimiento sea **independiente del framerate**. Sin esto, en un monitor de 120Hz todo se movería el doble de rápido que en uno de 60Hz.

**Error 6: Memory leaks con event listeners**
```javascript
// ❌ INCORRECTO
particulas.forEach(p => {
  const nodo = document.createElement("a-entity");
  nodo.addEventListener("click", () => mostrarModal(p.contenido));
  nodo.remove();  // El listener sigue en memoria
});

// ✅ CORRECTO (en mi implementación)
// Los nodos persisten durante toda la ejecución
// Si fuera necesario eliminarlos:
nodo.removeEventListener("click", handler);
nodo.remove();
```
**Explicación**: En aplicaciones de larga duración que crean/destruyen muchos objetos, es crítico limpiar event listeners. En esta aplicación, los nodos se crean una vez y persisten, por lo que no es un problema.

**Error 7: Raycasting no detecta clicks**
```javascript
// ❌ INCORRECTO
<a-entity raycaster="objects: .nodo"></a-entity>
// Pero los objetos no tienen clase="nodo"

// ✅ CORRECTO
<a-entity raycaster="objects: .clickable"></a-entity>
// Y en el código:
cilindro.setAttribute("class", "clickable");
esferaArriba.setAttribute("class", "clickable");
texto.setAttribute("class", "clickable");
```
**Explicación**: El raycaster solo intersecta objetos que coinciden con el selector CSS especificado. Además, debe aplicarse a las **geometrías reales** (mesh), no al contenedor entity.

--

He integrado múltiples conceptos avanzados en esta actividad: **visualización 3D con A-Frame** usando Entity-Component-System, **motor de física de partículas** con fuerzas de atracción/repulsión basadas en datos, **interactividad multimodal** (fly controls, clicks, UI 2D), **generación dinámica de interfaz** que detecta propiedades automáticamente, **optimización de rendimiento** (actualización diferida, detección de estabilidad) manteniendo 60 FPS, y **diseño visual efectivo** con colores por hash, transparencias y animaciones suaves.

Esta actividad culmina el aprendizaje progresivo de **101-Ejercicios**: desde fundamentos DOM/CSS (001-003), Web Workers (004), espacio 3D y transformaciones (005-007), billboards y texto 3D (008-011), hasta carga JSON (012) y la actividad final (013).

Aplica las **Pautas de diseño** estudiadas: usabilidad (navegación WASD intuitiva), accesibilidad (contraste y fuentes legibles), simplicidad (interface minimalista), consistencia (colores y patrones coherentes) y legibilidad (billboarding para orientación óptima).

Me prepara para el **103-Proyecto** de simulación de partículas física con escenarios múltiples. Los conceptos dominados (shaders, componentes personalizados, física, optimización, interactividad 3D) son fundamentales para el desarrollo de aplicaciones web 3D modernas, visualizaciones de datos y experiencias de realidad virtual/aumentada.
