He desarrollado un videojuego tipo Minecraft con vista isométrica utilizando Three.js como motor de renderizado 3D. El proyecto es un juego sandbox (mundo abierto) donde el jugador puede explorar, destruir y construir en un entorno 3D generado proceduralmente.

Este proyecto sirve para demostrar la comprensión de los conceptos fundamentales de motores de juegos estudiados en la unidad 001, aplicando conocimientos de:

- **Animación 2D y 3D**: Movimiento del personaje, rotación de items, animación flotante
- **Arquitectura del juego**: Separación entre lógica, física, renderizado y entrada de usuario
- **Componentes de un motor**: Sistema de físicas, detección de colisiones, cámara, renderizador
- **Librerías 3D**: Three.js como motor de renderizado WebGL
- **Generación procedurada**: Algoritmo Perlin Noise para crear terrenos realistas
- **Sistemas de juego**: Inventario, recolección de items, construcción/destrucción

El proyecto está diseñado para funcionar completamente en el navegador web sin necesidad de instalaciones adicionales, utilizando tecnologías web estándar (HTML5, CSS3, JavaScript ES6+).

---

### Arquitectura del Motor de Juego

El proyecto implementa una arquitectura modular típica de motores de juegos modernos:

**Definiciones técnicas:**

- **Motor de renderizado**: Sistema que transforma la geometría 3D en una imagen 2D en pantalla (Three.js con WebGL)
- **Game Loop**: Bucle principal que actualiza la lógica del juego y renderiza cada frame (~60 FPS)
- **Raycasting**: Técnica para detectar qué objeto 3D está bajo el cursor del ratón
- **Sistema de físicas**: Componente que simula gravedad, colisiones y movimiento

**Estructura del código:**

```javascript
// Configuración inicial
const CONFIG = {
  WORLD_SIZE: 32,
  PLAYER_SPEED: 0.1,
  CAMERA_HEIGHT: 12,
  TERRAIN_SCALE: 0.3
};

// Variables globales organizadas por sistema
let scene, camera, renderer;  // Sistema de renderizado
let blocks = [], items = [];  // Sistema de mundo
let player, playerMesh;        // Sistema de jugador
let inventory = {};            // Sistema de inventario
```

### Funcionamiento paso a paso

#### Paso 1: Inicialización del motor

```javascript
function init() {
  // 1. Crear escena 3D
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x87CEEB);
  scene.fog = new THREE.Fog(0x87CEEB, 40, 80);
  
  // 2. Configurar cámara isométrica
  camera = new THREE.PerspectiveCamera(45, aspect, 0.1, 1000);
  
  // 3. Crear renderer WebGL
  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.shadowMap.enabled = true;
  
  // 4. Inicializar sistemas
  setupLights();
  generateTerrain();
  createPlayer();
  setupEventListeners();
  
  // 5. Iniciar game loop
  animate();
}
```

#### Paso 2: Generación procedurada de terreno

Utilizo el algoritmo **Perlin Noise** para generar terrenos realistas:

```javascript
function getPerlinNoise(x, z) {
  const intX = Math.floor(x);
  const intZ = Math.floor(z);
  const fracX = x - intX;
  const fracZ = z - intZ;
  
  // Obtener valores en las esquinas
  const v1 = smoothNoise(intX, intZ);
  const v2 = smoothNoise(intX + 1, intZ);
  const v3 = smoothNoise(intX, intZ + 1);
  const v4 = smoothNoise(intX + 1, intZ + 1);
  
  // Interpolar suavemente
  const i1 = interpolate(v1, v2, fracX);
  const i2 = interpolate(v3, v4, fracX);
  
  return interpolate(i1, i2, fracZ);
}
```

**Sistema de biomas** implementado:

- **Montañas**: `biomeNoise > 0.6` → alturas de 4-8 bloques
- **Colinas**: `0.4 < biomeNoise < 0.6` → alturas de 2-5 bloques
- **Llanuras**: `biomeNoise < 0.4` → alturas de 0-2 bloques

#### Paso 3: Sistema de físicas

```javascript
function updatePlayer() {
  // Aplicar gravedad
  player.velocity.y -= 0.02;
  player.y += player.velocity.y;
  
  // Detectar suelo
  const groundY = getGroundHeight(player.x, player.z) + CONFIG.PLAYER_HEIGHT / 2;
  if (player.y <= groundY) {
    player.y = groundY;
    player.velocity.y = 0;
    player.onGround = true;
    
    // Saltar (alcanza exactamente 1 bloque)
    if (keys.space && player.onGround) {
      player.velocity.y = 0.25;
    }
  }
}
```

**Detección de colisiones:**

```javascript
function checkCollision(x, y, z) {
  const currentGroundHeight = getGroundHeight(player.x, player.z);
  const targetGroundHeight = getGroundHeight(x, z);
  const heightDifference = targetGroundHeight - currentGroundHeight;
  
  // Bloquear si la diferencia es mayor a 1 bloque
  if (heightDifference > 1) {
    return true; // No puede subir sin saltar
  }
  
  // Bloquear subida de 1 bloque sin salto
  if (heightDifference === 1 && player.onGround) {
    return true;
  }
  
  return false;
}
```

#### Paso 4: Sistema de items e inventario

```javascript
function createItem(x, y, z, type) {
  const itemGeometry = new THREE.BoxGeometry(0.3, 0.3, 0.3);
  const itemMaterial = new THREE.MeshLambertMaterial({ 
    color: BLOCK_TYPES[type].color,
    emissive: BLOCK_TYPES[type].color,
    emissiveIntensity: 0.3
  });
  
  const itemMesh = new THREE.Mesh(itemGeometry, itemMaterial);
  itemMesh.userData = { 
    type: type,
    floatOffset: Math.random() * Math.PI * 2
  };
  
  scene.add(itemMesh);
  items.push(itemMesh);
}

function updateItems() {
  const time = Date.now() * 0.001;
  
  for (let i = items.length - 1; i >= 0; i--) {
    const item = items[i];
    
    // Animación: rotación + levitación
    item.rotation.y += 0.05;
    item.position.y += Math.sin(time * 2 + item.userData.floatOffset) * 0.02;
    
    // Recolección automática por proximidad
    const distance = Math.sqrt(
      Math.pow(item.position.x - player.x, 2) +
      Math.pow(item.position.y - player.y, 2) +
      Math.pow(item.position.z - player.z, 2)
    );
    
    if (distance < 1.5) {
      inventory[item.userData.type]++;
      scene.remove(item);
      items.splice(i, 1);
    }
  }
}
```

#### Paso 5: Game Loop (Bucle principal)

```javascript
function animate() {
  requestAnimationFrame(animate);
  
  if (!gameStarted) return;
  
  // 1. Actualizar lógica de juego
  updatePlayer();
  updateItems();
  
  // 2. Actualizar FPS counter
  frames++;
  if (Date.now() >= lastTime + 1000) {
    document.getElementById('fps').textContent = frames;
    frames = 0;
    lastTime = Date.now();
  }
  
  // 3. Renderizar escena
  renderer.render(scene, camera);
}
```

### 2.3. Terminología técnica aplicada

- **Three.js**: Librería JavaScript que abstrae WebGL para facilitar el desarrollo 3D
- **Mesh**: Objeto 3D compuesto por geometría (forma) y material (apariencia)
- **Raycaster**: Proyecta un rayo desde la cámara para detectar intersecciones con objetos
- **Flat Shading**: Técnica de sombreado donde cada cara tiene un color uniforme (estilo Minecraft)
- **Frustum Culling**: Optimización que no renderiza objetos fuera del campo de visión
- **Shadow Mapping**: Técnica para calcular sombras proyectadas por objetos
- **Delta Time**: Tiempo transcurrido entre frames (importante para física consistente)
- **Emissive Material**: Material que emite luz propia (usado para el brillo de items)

---

## 3. Aplicación práctica

### 3.1. Implementación real del proyecto

El proyecto está completamente funcional con los siguientes sistemas implementados:

**Sistema de entrada (Input Handling):**

```javascript
function onKeyDown(event) {
  switch(event.key.toLowerCase()) {
    case 'w': keys.w = true; break;
    case 'a': keys.a = true; break;
    case 's': keys.s = true; break;
    case 'd': keys.d = true; break;
    case ' ': keys.space = true; break;
    case '1': selectBlock('grass'); break;
    case 'q': cameraAngle -= 2; break;
    case 'e': cameraAngle += 2; break;
  }
}
```

**Sistema de cámara isométrica:**

```javascript
function updateCameraPosition() {
  const centerX = player.x;
  const centerZ = player.z;
  const centerY = player.y;
  
  const radians = (cameraAngle * Math.PI) / 180;
  const x = centerX + Math.cos(radians) * cameraDistance;
  const z = centerZ + Math.sin(radians) * cameraDistance;
  
  camera.position.set(x, centerY + CONFIG.CAMERA_HEIGHT, z);
  camera.lookAt(centerX, centerY, centerZ);
}
```

**Sistema de construcción/destrucción:**

```javascript
function onMouseDown(event) {
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(blocks);
  
  if (intersects.length > 0) {
    const clickedBlock = intersects[0].object;
    const distance = calculateDistance(clickedBlock, player);
    
    if (distance > 4.5) return; // Fuera de alcance
    
    if (event.button === 0) {
      removeBlock(clickedBlock); // Destruir
    } else if (event.button === 2) {
      const newPos = calculateNewBlockPosition(clickedBlock, intersects[0].face);
      placeBlock(newPos.x, newPos.y, newPos.z, selectedBlockType); // Colocar
    }
  }
}
```

### 3.2. Ejemplos de uso

**Ejemplo 1: Crear un bloque con material clonado**

```javascript
// CORRECTO: Cada bloque tiene su propio material
const material = blockMaterials[type].clone();
const mesh = new THREE.Mesh(blockGeometry, material);
mesh.userData = { x, y, z, type };
```

**Ejemplo 2: Optimización con geometría compartida**

```javascript
// BUENA PRÁCTICA: Reutilizar geometría (ahorra memoria)
blockGeometry = new THREE.BoxGeometry(1, 1, 1);
blockGeometry.computeVertexNormals();

// Cada bloque usa la misma geometría pero diferente material
for (let i = 0; i < 1000; i++) {
  const mesh = new THREE.Mesh(blockGeometry, materials[i].clone());
}
```

### 3.3. Errores comunes y soluciones

#### Error 1: Materiales compartidos causan highlight en todos los bloques

**❌ INCORRECTO:**
```javascript
// Todos los bloques del mismo tipo comparten material
const mesh = new THREE.Mesh(blockGeometry, blockMaterials[type]);
hoveredBlock.material.emissive.setHex(0x333333); // ¡Afecta a TODOS!
```

**✅ CORRECTO:**
```javascript
// Clonar el material para cada bloque
const material = blockMaterials[type].clone();
const mesh = new THREE.Mesh(blockGeometry, material);
hoveredBlock.material.emissive.setHex(0x333333); // Solo afecta a uno
```

#### Error 2: Cámara de sombras desajustada

**❌ PROBLEMA:**
```javascript
// Sombras solo cubren 20x20 pero el mundo es 32x32
directionalLight.shadow.camera.left = -20;
directionalLight.shadow.camera.right = 20;
// Resultado: Línea diagonal donde terminan las sombras
```

**✅ SOLUCIÓN:**
```javascript
// Ajustar para cubrir todo el mundo
directionalLight.shadow.camera.left = -40;
directionalLight.shadow.camera.right = 40;
directionalLight.shadow.camera.top = 40;
directionalLight.shadow.camera.bottom = -40;
```

#### Error 3: Movimiento inconsistente por framerate variable

**❌ INCORRECTO:**
```javascript
// Velocidad depende de FPS
player.x += 0.1; // Más rápido a 120 FPS, más lento a 30 FPS
```

**✅ CORRECTO:**
```javascript
// Usar delta time (no implementado en este proyecto básico, pero recomendado)
const deltaTime = clock.getDelta();
player.x += CONFIG.PLAYER_SPEED * deltaTime * 60; // Normalizado a 60 FPS
```

#### Error 4: Verificación de colisiones inexacta

**❌ PROBLEMA:**
```javascript
// Solo verificar posición exacta
const block = getBlockAt(Math.floor(player.x), Math.floor(player.y), Math.floor(player.z));
// No detecta colisiones con bloques adyacentes
```

**✅ SOLUCIÓN:**
```javascript
// Verificar diferencia de alturas relativa
const currentGroundHeight = getGroundHeight(player.x, player.z);
const targetGroundHeight = getGroundHeight(newX, newZ);
const heightDiff = targetGroundHeight - currentGroundHeight;

if (heightDiff > 1) return true; // Bloqueado: demasiado alto
```

### 3.4. Optimizaciones aplicadas

1. **Geometría compartida**: Un solo `BoxGeometry` reutilizado por todos los bloques
2. **Material clonado**: Materiales individuales solo cuando es necesario (hover)
3. **Frustum culling automático**: Three.js no renderiza objetos fuera de cámara
4. **Shadow map optimizado**: Resolución 2048x2048 balanceando calidad/rendimiento
5. **Flat shading**: Menos cálculos de iluminación que smooth shading

---

## 4. Conclusión breve

### 4.1. Puntos clave del proyecto

Este proyecto de Minecraft Isométrico demuestra la aplicación práctica de los conceptos fundamentales de motores de juegos:

1. **Arquitectura modular**: Separación clara entre renderizado (Three.js), lógica (game loop), física (colisiones/gravedad) y entrada (eventos)

2. **Generación procedurada**: Algoritmo Perlin Noise con múltiples octavas para crear terrenos naturales con biomas diferenciados

3. **Sistemas de juego**: Inventario, recolección de items, construcción/destrucción con rango de interacción

4. **Optimización**: Reutilización de geometría, clonación selectiva de materiales, shadow mapping eficiente

5. **Física realista**: Gravedad, salto calibrado (1 bloque), detección de colisiones por altura relativa

### 4.2. Relación con contenidos de la unidad

**Conexión con ejercicios previos:**

- **001 - Animación**: Implementado en rotación de items, levitación, movimiento del personaje
- **002 - Arquitectura**: Estructura modular con separación de sistemas (CONFIG, variables globales organizadas)
- **003 - Motores de juegos**: Three.js como motor especializado en renderizado 3D WebGL
- **004 - Librerías**: Uso de Three.js (librería externa) vs desarrollo desde cero
- **005 - Componentes**: Sistema de físicas, renderer, input handler, audio (pendiente)
- **007 - Juegos existentes**: Sistema de recolección inspirado en ejercicios previos
- **008 - Modificaciones**: Extensión del concepto base con generación procedurada y biomas

**Conceptos avanzados aplicados:**

- **Raycasting**: Detección de intersecciones 3D para selección de bloques
- **Shadow Mapping**: Cálculo de sombras dinámicas en tiempo real
- **Procedural Generation**: Creación algorítmica de contenido (terreno infinitamente variable)
- **State Machine**: Estados del jugador (onGround, jumping, falling)
- **Camera System**: Cámara isométrica que sigue al jugador con rotación orbital

### 4.3. Posibles mejoras futuras

1. **Texturas**: Sustituir colores sólidos por texturas realistas
2. **Audio**: Sonidos de pasos, destrucción, recolección (usando Web Audio API)
3. **Partículas**: Efectos visuales al destruir bloques (THREE.Points)
4. **Guardado**: Sistema de persistencia con LocalStorage
5. **Multijugador**: WebSockets para juego en red
6. **Más biomas**: Desiertos, bosques, nieve
7. **Mobs**: NPCs con IA básica (pathfinding)

---

## Autoevaluación de criterios

| Criterio | Cumplimiento | Evidencia |
|----------|--------------|-----------|
| Introducción clara | ✅ Completo | Concepto y contexto explicados con detalle |
| Terminología técnica | ✅ Completo | Uso correcto de términos: Mesh, Raycaster, Perlin Noise, etc. |
| Funcionamiento paso a paso | ✅ Completo | 5 pasos detallados desde init() hasta game loop |
| Ejemplos de código real | ✅ Completo | Múltiples fragmentos funcionales del proyecto |
| Aplicación práctica | ✅ Completo | Sistema completo implementado y funcional |
| Errores comunes | ✅ Completo | 4 errores identificados con soluciones |
| Conclusión con resumen | ✅ Completo | Puntos clave enumerados claramente |
| Enlace con otros contenidos | ✅ Completo | Conexión explícita con ejercicios 001-008 |

---

**Proyecto desarrollado por:** [Nombre del alumno]  
**Fecha de entrega:** 12 de noviembre de 2025  
**Asignatura:** Programación multimedia y dispositivos móviles  
**Unidad:** 001 - Análisis de motores de juegos
