En esta actividad he desarrollado un **mini clon de Minecraft en 3D** usando `Three.js` y `PointerLockControls`, siguiendo la progresión de los ejemplos trabajados en clase.  
El objetivo ha sido integrar en un único proyecto varios conceptos clave de la unidad:

- Creación de una **escena 3D** con cámara, luz y renderizador.
- Representación del mundo mediante **bloques cúbicos** (tipo Minecraft).
- Control en primera persona con teclado + ratón.
- Uso de **raycasting** para interactuar con los bloques (colocar y eliminar).
- Gestión básica de físicas y colisiones.

Todo ello se usa en el contexto del desarrollo de motores de juego y escenas interactivas, entendiendo cómo se construye desde cero un entorno jugable sencillo, pero completo.

**Ejemplo real del inicio del proyecto:**

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/PointerLockControls.min.js"></script>
```

```js
console.log('🎮 Iniciando Minecraft Clone Completo...');
const game = new MinecraftGame();
```

Con esto dejo claro que el ejercicio no es solo teórico: he montado un flujo completo de juego en el navegador.

---

En esta sección explico cómo he implementado técnicamente las partes principales, usando **código real** del archivo `Juego Completo.html`.

### Clase `Block` (bloques del mundo)

Cada bloque del escenario es un cubo que se añade a la escena:

```js
class Block {
    constructor(x, y, z, type = 'grass') {
        this.x = x;
        this.y = y;
        this.z = z;
        this.type = type;
        this.mesh = null;
        this.createMesh();
    }
    
    createMesh() {
        const geometry = new THREE.BoxGeometry(1, 1, 1);

        const colors = {
            'grass': 0x4CAF50,
            'dirt': 0x795548,
            'stone': 0x9E9E9E
        };
        
        const material = new THREE.MeshPhongMaterial({ 
            color: colors[this.type] || 0x4CAF50,
            flatShading: true
        });
        
        this.mesh = new THREE.Mesh(geometry, material);
        this.mesh.position.set(this.x, this.y, this.z);
        this.mesh.castShadow = true;
        this.mesh.receiveShadow = true;
    }

    addToScene(scene) {
        if (this.mesh) scene.add(this.mesh);
    }

    removeFromScene(scene) {
        if (this.mesh) scene.remove(this.mesh);
    }

    getBoundingBox() {
        return new THREE.Box3().setFromObject(this.mesh);
    }
}
```

Con esto cumplo la parte de **modelo de datos del mundo**: cada bloque sabe cómo se ve y dónde está.

### Inicialización del juego (`MinecraftGame`)

En el constructor preparo escena, cámara, renderizador y estructuras internas:

```js
class MinecraftGame {
    constructor() {
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x87CEEB);

        this.camera = new THREE.PerspectiveCamera(
            75,
            window.innerWidth / window.innerHeight,
            0.1,
            1000
        );
        this.camera.position.set(0, 2, 0);

        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        document.body.appendChild(this.renderer.domElement);
    }
```

Aquí se ve el uso correcto de:

- `THREE.Scene`, `THREE.PerspectiveCamera`, `THREE.WebGLRenderer`.
- Sombras activadas.
- Variables para físicas y movimiento.
- `Raycaster` para interacción.

### Creación del mundo (bloques iniciales)

Genero un suelo + una pequeña estructura para practicar construcción/destrucción:

```js
createWorld() {
    const gridSize = 20;

    for (let x = -gridSize/2; x < gridSize/2; x++) {
        for (let z = -gridSize/2; z < gridSize/2; z++) {
            let type = 'grass';
            const rand = Math.random();
            if (rand > 0.85) type = 'dirt';
            if (rand > 0.95) type = 'stone';

            const block = new Block(x, -0.5, z, type);
            block.addToScene(this.scene);
            this.blocks.push(block);
        }
    }
}
```

### Controles, raycasting e interacción real

**Controles FPS con PointerLock:**

```js
setupControls() {
    this.controls = new THREE.PointerLockControls(this.camera, document.body);
    const instructions = document.getElementById('instructions');
    instructions.addEventListener('click', () => this.controls.lock());
}
```

**Raycasting para eliminar bloques (click izquierdo):**

```js
removeBlockAtPointer() {
    this.raycaster.setFromCamera(new THREE.Vector2(0, 0), this.camera);
    const intersects = this.raycaster.intersectObjects(this.blocks.map(b => b.mesh));
    if (intersects.length > 0) {
        const block = this.blocks.find(b => b.mesh === intersects[0].object);
        if (block.y >= 0) {
            block.removeFromScene(this.scene);
            this.blocks = this.blocks.filter(b => b !== block);
        }
    }
}
```

---

```js
document.addEventListener('keydown', (event) => {
    switch (event.code) {
        case 'KeyW': this.moveState.forward = true; break;
        case 'KeyS': this.moveState.backward = true; break;
        case 'KeyA': this.moveState.left = true; break;
        case 'KeyD': this.moveState.right = true; break;
        case 'Space':
            if (this.onGround) this.moveState.jump = true;
            event.preventDefault();
            break;
    }
});
```

### Actualización de físicas

```js
updateMovement(delta) {
    const baseSpeed = 250.0;
    const dir = new THREE.Vector3();
    this.camera.getWorldDirection(dir);
    dir.y = 0;
    dir.normalize();

    this.velocity.add(dir.multiplyScalar(baseSpeed * delta));
    this.velocity.y += this.gravity * delta;
}
```

---

Con este proyecto he conseguido:

- Integrar **renderizado 3D, movimiento, interacción y colisiones** en un mismo entorno.
- Comprender cómo se estructuran internamente los motores de juegos voxel.
- Usar correctamente `Three.js` sin dependencias externas.
- Aplicar conceptos de **física básica, raycasting y control de cámara**.

Este ejercicio cierra la unidad sobre **Análisis y aplicación de motores de juegos**, mostrando que puedo construir desde cero un entorno jugable funcional y extensible a proyectos más complejos.
