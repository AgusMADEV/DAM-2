En este proyecto he desarrollado un prototipo jugable inspirado en *Minecraft* con vista isométrica. El objetivo es demostrar los fundamentos de un motor gráfico ejecutándose en el navegador: **escena 3D**, **cámara**, **renderer WebGL**, **bucle de juego**, **gestión de entrada** (teclado/ratón), **detección por raycasting** y **lógica de mundo** (terreno por ruido, bloques, colisiones, inventario básico).  
Se usa **Three.js** para la capa de renderizado y utilidades 3D. El contexto de uso es docente: analizar la arquitectura mínima de un “motor” para juegos tipo *sandbox* en entorno web y dispositivos (por su compatibilidad con navegadores móviles/desktop).

---

### Definiciones y terminología
- **Escena (Scene):** contenedor de todos los objetos 3D.
- **Cámara (Camera):** define el punto de vista; uso `PerspectiveCamera` con posición isométrica.
- **Renderer:** traduce la escena+cámara a píxeles en un `<canvas>` con WebGL.
- **Game Loop (bucle de juego):** ciclo continuo que actualiza lógica y renderiza.
- **Raycaster:** calcula intersecciones ratón↔objetos 3D (apuntar bloques).
- **Ruido/perlin-like:** función pseudoaleatoria suave para alturas del terreno.
- **AABB/colisiones:** aquí se simplifica con consultas a bloques ocupados en grilla.
- **Inventario/ítems:** representación mínima de recolección y conteo por tipo.

### Arquitectura y flujo principal
1) **Inicialización**: crear escena, cámara, renderer, luces, geometrías, materiales, terreno y jugador; suscribir eventos.  
2) **Interacción**: teclado para mover/saltar y rotar cámara; ratón para destruir/colocar bloques mediante raycasting con límite de alcance.  
3) **Simulación**: actualización de jugador (gravedad, salto, colisiones) e ítems (animación y recogida).  
4) **Render**: se pinta cada frame en `animate()`.

**Configuración base** (constantes y tipos de bloque):
```js
const CONFIG = {
  WORLD_SIZE: 32, BLOCK_SIZE: 1, CAMERA_DISTANCE: 15,
  CAMERA_ANGLE: 45, CAMERA_HEIGHT: 12, ZOOM_SPEED: 2,
  ROTATION_SPEED: 2, PLAYER_SPEED: 0.1, PLAYER_HEIGHT: 1.8,
  TERRAIN_SCALE: 0.3, TERRAIN_HEIGHT: 4,
};

const BLOCK_TYPES = {
  grass: { color: 0x4CAF50, name: 'Grass' },
  dirt:  { color: 0x795548, name: 'Dirt' },
  stone: { color: 0x9E9E9E, name: 'Stone' }
};
```

**Luces** (ambiental + direccional con sombras):
```js
function setupLights() {
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
  scene.add(ambientLight);

  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.6);
  directionalLight.position.set(20, 30, 20);
  directionalLight.castShadow = true;
  directionalLight.shadow.camera.left = -40;
  directionalLight.shadow.camera.right = 40;
  directionalLight.shadow.camera.top = 40;
  directionalLight.shadow.camera.bottom = -40;
  directionalLight.shadow.mapSize.width = 2048;
  directionalLight.shadow.mapSize.height = 2048;
  scene.add(directionalLight);
}
```

**Terreno** (ruido 2D suavizado + biomas + capas de materiales):
```js
function getPerlinNoise(x, z) { /* ...interpolate + smoothNoise... */ }

function generateTerrain() {
  // ...construcción de heightMap y smoothedHeightMap...
  for (let x = 0; x < CONFIG.WORLD_SIZE; x++) {
    for (let z = 0; z < CONFIG.WORLD_SIZE; z++) {
      const height = smoothedHeightMap[x][z];
      for (let y = 0; y <= height; y++) {
        let blockType = y === height ? 'grass' : (y >= height - 2 ? 'dirt' : 'stone');
        placeBlock(x, y, z, blockType, false);
      }
    }
  }
}
```

**Colocación y eliminación de bloques + ítems**:
```js
function placeBlock(x, y, z, type, updateCount = true) {
  if (getBlockAt(x, y, z)) return;
  const material = blockMaterials[type].clone();
  const mesh = new THREE.Mesh(blockGeometry, material);
  mesh.position.set(x + 0.5, y + 0.5, z + 0.5);
  mesh.userData = { x, y, z, type };
  scene.add(mesh); blocks.push(mesh);
  if (updateCount) updateBlockCount();
}

function removeBlock(block) {
  createItem(block.userData.x + 0.5, block.userData.y + 0.5, block.userData.z + 0.5, block.userData.type);
  blocks.splice(blocks.indexOf(block), 1);
  scene.remove(block); updateBlockCount();
}
```

**Selección con ratón (raycasting + alcance)**:
```js
function onMouseDown(event) {
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(blocks);
  if (intersects.length > 0) {
    const clickedBlock = intersects[0].object;
    const dist = /* distancia jugador-bloque */;
    if (dist > 4.5) return;
    if (event.button === 0) removeBlock(clickedBlock);
    else if (event.button === 2) { /* calcular cara y placeBlock(...) */ }
  }
}
```

**Movimiento del jugador + gravedad + colisiones**:
```js
function updatePlayer() {
  // calcular desplazamiento relativo a la cámara (WASD)
  // colisiones sin “auto-step”: checkCollision(x,z) por diferencias de altura
  // gravedad y salto a 1 bloque exacto
  player.velocity.y -= 0.02;
  // suelo en getGroundHeight(x,z) y estado onGround
  // rotación del mesh según vector de movimiento
  updateCameraPosition();
}
```

**Bucle de juego**:
```js
function animate() {
  requestAnimationFrame(animate);
  if (!gameStarted) return;
  updatePlayer();
  updateItems();
  renderer.render(scene, camera);
}
```

### Ejemplos concretos del proyecto
- **Biomas y capas:** césped en superficie, tierra como subcapa y piedra en profundidad.
- **Inventario:** cada bloque destruido genera un ítem flotante con leve brillo; al acercarme, se añade al contador UI.
- **Cámara isométrica dinámica:** orbita con `Q/E` y zoom con rueda manteniendo el foco en el jugador.

---

### ¿Cómo se usa en juego?
- **Construcción/destrucción:** apunto con el ratón, **click izq.** destruye y **click der.** coloca el bloque seleccionado (1–3).
- **Movimiento:** **WASD** + **Espacio** para saltar exactamente un bloque (diseñado para evitar escalado “automático” e imponer timing).
- **Gestión de mundo:** el raycast limita el alcance a ~4.5 bloques, coherente con el género.

### Colocación respetando límites y cuerpo del jugador
```js
if (x >= 0 && x < CONFIG.WORLD_SIZE && z >= 0 && z < CONFIG.WORLD_SIZE && y >= 0 && y < 10) {
  const px = Math.floor(player.x), pz = Math.floor(player.z);
  const py1 = Math.floor(player.y - CONFIG.PLAYER_HEIGHT / 2);
  const py2 = Math.floor(player.y + CONFIG.PLAYER_HEIGHT / 2);
  if (!(x === px && z === pz && (y === py1 || y === py2))) {
    placeBlock(x, y, z, selectedBlockType);
  }
}
```

### Errores comunes y cómo los evité
- **Hover/selección “a través” de otros objetos:** uso `raycaster.intersectObjects(blocks)` y reseteo el emissive del bloque anterior para evitar artefactos visuales.
- **Físicas inestables al aterrizar:** fijo la altura del jugador al nivel del suelo calculado y anulo velocidad vertical al contactar (`player.velocity.y = 0`).
- **Auto-escalado indeseado en rampas:** bloqueo movimientos con `checkCollision` cuando la diferencia de altura objetivo > 1 o es 1 sin salto activo.
- **Colocar bloques dentro del jugador:** compruebo la celda del cuerpo antes de `placeBlock(...)`.
- **Rendimiento en terreno:** reutilizo geometrías/materiales base y clono solo el material por bloque para manipular `emissive` en hover.

---

He construido un “mini motor” jugable que integra **renderizado 3D**, **entrada**, **física simple**, **raycasting**, **generación procedural** y **UI in‑game**. Esto conecta con otros contenidos de la unidad:  
- **Motores de juegos y bucles de actualización**,  
- **Cámaras y proyección**,  
- **Sistemas de coordenadas y colisiones por grilla**,  
- **Gestión de recursos (geometrías/materiales) y rendimiento**.  

El resultado es una base sólida para extender a **optimización por *chunking***, **texturas/atlas**, **persistencia del mundo** o **portado a dispositivos** aprovechando la naturaleza web del proyecto.
