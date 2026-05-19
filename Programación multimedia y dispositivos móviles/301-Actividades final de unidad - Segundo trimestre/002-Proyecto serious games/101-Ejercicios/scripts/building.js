// ========================================
// BUILDING.JS - Edificio con salidas
// ========================================

class Building {
    constructor(scene) {
        this.scene = scene;
        this.width = 40;
        this.depth = 30;
        this.height = 3;
        this.exits = [];
        this.walls = [];
        this.obstacles = []; // Array de obstáculos internos
        this.heatmapData = [];
        this.heatmapPlane = null;
        
        this.createFloor();
        this.createWalls();
        this.createExits(2); // Por defecto 2 salidas
        this.createInternalLayout();
    }
    
    createFloor() {
        const floorGeometry = new THREE.BoxGeometry(this.width, 0.2, this.depth);
        const floorMaterial = new THREE.MeshStandardMaterial({
            color: 0x2a2a3a,
            roughness: 0.8,
            metalness: 0.2
        });
        
        this.floor = new THREE.Mesh(floorGeometry, floorMaterial);
        this.floor.receiveShadow = true;
        this.floor.position.y = -0.1;
        this.scene.add(this.floor);
        
        // Grid para referencia
        const gridHelper = new THREE.GridHelper(this.width, 20, 0x444466, 0x222233);
        gridHelper.position.y = 0;
        this.scene.add(gridHelper);
    }
    
    createWalls() {
        const wallHeight = this.height;
        const wallThickness = 0.5;
        const wallMaterial = new THREE.MeshStandardMaterial({
            color: 0x3a4a5a,
            roughness: 0.7,
            metalness: 0.3
        });
        
        // Pared Norte
        const northWall = this.createWall(
            this.width, wallHeight, wallThickness,
            0, wallHeight/2, -this.depth/2,
            wallMaterial
        );
        
        // Pared Sur
        const southWall = this.createWall(
            this.width, wallHeight, wallThickness,
            0, wallHeight/2, this.depth/2,
            wallMaterial
        );
        
        // Pared Este
        const eastWall = this.createWall(
            wallThickness, wallHeight, this.depth,
            this.width/2, wallHeight/2, 0,
            wallMaterial
        );
        
        // Pared Oeste
        const westWall = this.createWall(
            wallThickness, wallHeight, this.depth,
            -this.width/2, wallHeight/2, 0,
            wallMaterial
        );
        
        this.walls = [northWall, southWall, eastWall, westWall];
    }
    
    createWall(width, height, depth, x, y, z, material) {
        const geometry = new THREE.BoxGeometry(width, height, depth);
        const mesh = new THREE.Mesh(geometry, material);
        mesh.position.set(x, y, z);
        mesh.castShadow = true;
        mesh.receiveShadow = true;
        this.scene.add(mesh);
        return mesh;
    }
    
    createExits(numExits) {
        // Limpiar salidas anteriores
        this.exits.forEach(exit => {
            this.scene.remove(exit.mesh);
            this.scene.remove(exit.sign);
        });
        this.exits = [];
        
        const exitWidth = 3;
        const exitHeight = 2.5;
        const positions = this.calculateExitPositions(numExits);
        
        positions.forEach((pos, index) => {
            const exitMaterial = new THREE.MeshStandardMaterial({
                color: 0x00ff00,
                emissive: 0x00ff00,
                emissiveIntensity: 0.5,
                transparent: true,
                opacity: 0.7
            });
            
            const exitGeometry = new THREE.BoxGeometry(exitWidth, exitHeight, 0.3);
            const exitMesh = new THREE.Mesh(exitGeometry, exitMaterial);
            exitMesh.position.copy(pos.position);
            exitMesh.castShadow = false;
            exitMesh.receiveShadow = false;
            this.scene.add(exitMesh);
            
            // Señal de salida de emergencia
            const signGeometry = new THREE.BoxGeometry(2, 0.8, 0.1);
            const signMaterial = new THREE.MeshStandardMaterial({
                color: 0xff0000,
                emissive: 0xff0000,
                emissiveIntensity: 0.8
            });
            const signMesh = new THREE.Mesh(signGeometry, signMaterial);
            signMesh.position.copy(pos.position);
            signMesh.position.y = exitHeight + 0.8;
            this.scene.add(signMesh);
            
            // Luz de la salida
            const exitLight = new THREE.PointLight(0x00ff00, 1, 10);
            exitLight.position.copy(pos.position);
            exitLight.position.y = exitHeight;
            this.scene.add(exitLight);
            
            this.exits.push({
                mesh: exitMesh,
                sign: signMesh,
                light: exitLight,
                position: pos.position.clone(),
                direction: pos.direction,
                width: exitWidth
            });
        });
        
        console.log(`🚪 Creadas ${numExits} salidas de emergencia`);
    }
    
    calculateExitPositions(numExits) {
        const positions = [];
        const walls = ['north', 'south', 'east', 'west'];
        
        for (let i = 0; i < numExits; i++) {
            const wallIndex = i % walls.length;
            const wall = walls[wallIndex];
            
            let pos = new THREE.Vector3();
            let direction = new THREE.Vector3();
            
            switch(wall) {
                case 'north':
                    pos.set(
                        (i - numExits/2) * 8, 
                        1.25, 
                        -this.depth/2
                    );
                    direction.set(0, 0, -1);
                    break;
                case 'south':
                    pos.set(
                        (i - numExits/2) * 8,
                        1.25,
                        this.depth/2
                    );
                    direction.set(0, 0, 1);
                    break;
                case 'east':
                    pos.set(
                        this.width/2,
                        1.25,
                        (i - numExits/2) * 6
                    );
                    direction.set(1, 0, 0);
                    break;
                case 'west':
                    pos.set(
                        -this.width/2,
                        1.25,
                        (i - numExits/2) * 6
                    );
                    direction.set(-1, 0, 0);
                    break;
            }
            
            positions.push({ position: pos, direction });
        }
        
        return positions;
    }
    
    createInternalLayout() {
        // Crear algunas divisiones internas (obstáculos)
        const obstacleMaterial = new THREE.MeshStandardMaterial({
            color: 0x4a5a6a,
            roughness: 0.6
        });
        
        // Obstáculo central 1 (pared horizontal)
        this.createWall(
            10, 2.5, 0.3,
            -5, 1.25, 0,
            obstacleMaterial
        );
        this.obstacles.push({
            type: 'box',
            position: { x: -5, y: 1.25, z: 0 },
            size: { width: 10, height: 2.5, depth: 0.3 }
        });
        
        // Obstáculo central 2 (pared vertical)
        this.createWall(
            0.3, 2.5, 8,
            5, 1.25, 5,
            obstacleMaterial
        );
        this.obstacles.push({
            type: 'box',
            position: { x: 5, y: 1.25, z: 5 },
            size: { width: 0.3, height: 2.5, depth: 8 }
        });
        
        // Columnas estructurales
        for (let i = -1; i <= 1; i++) {
            for (let j = -1; j <= 1; j++) {
                if (i === 0 && j === 0) continue; // Evitar el centro
                const columnGeometry = new THREE.CylinderGeometry(0.3, 0.3, 2.5, 8);
                const columnMesh = new THREE.Mesh(columnGeometry, obstacleMaterial);
                const posX = i * 10;
                const posZ = j * 8;
                columnMesh.position.set(posX, 1.25, posZ);
                columnMesh.castShadow = true;
                this.scene.add(columnMesh);
                
                // Guardar en array de obstáculos
                this.obstacles.push({
                    type: 'cylinder',
                    position: { x: posX, y: 1.25, z: posZ },
                    radius: 0.3
                });
            }
        }
    }
    
    getRandomPosition() {
        // Generar posición aleatoria dentro del edificio, evitando paredes
        return new THREE.Vector3(
            (Math.random() - 0.5) * (this.width - 4),
            0.7, // Altura ajustada para nueva geometría de personas
            (Math.random() - 0.5) * (this.depth - 4)
        );
    }
    
    isAtExit(position) {
        return this.exits.some(exit => {
            const distance = position.distanceTo(exit.position);
            return distance < exit.width;
        });
    }
    
    getNearestExit(position) {
        let nearest = null;
        let minDistance = Infinity;
        
        this.exits.forEach(exit => {
            const distance = position.distanceTo(exit.position);
            if (distance < minDistance) {
                minDistance = distance;
                nearest = exit;
            }
        });
        
        return nearest;
    }
    
    updateExits(numExits) {
        this.createExits(numExits);
    }
    
    toggleHeatmap(show) {
        if (show && !this.heatmapPlane) {
            this.createHeatmapPlane();
        } else if (!show && this.heatmapPlane) {
            this.scene.remove(this.heatmapPlane);
            this.heatmapPlane = null;
        }
    }
    
    createHeatmapPlane() {
        const canvas = document.createElement('canvas');
        canvas.width = 256;
        canvas.height = 256;
        const context = canvas.getContext('2d');
        
        const texture = new THREE.CanvasTexture(canvas);
        const material = new THREE.MeshBasicMaterial({
            map: texture,
            transparent: true,
            opacity: 0.6
        });
        
        const geometry = new THREE.PlaneGeometry(this.width, this.depth);
        this.heatmapPlane = new THREE.Mesh(geometry, material);
        this.heatmapPlane.rotation.x = -Math.PI / 2;
        this.heatmapPlane.position.y = 0.1;
        
        this.scene.add(this.heatmapPlane);
        this.heatmapCanvas = canvas;
        this.heatmapContext = context;
    }
    
    updateHeatmap(people) {
        if (!this.heatmapPlane) return;
        
        const context = this.heatmapContext;
        const canvas = this.heatmapCanvas;
        
        // Limpiar canvas
        context.clearRect(0, 0, canvas.width, canvas.height);
        
        // Crear gradiente de calor basado en densidad de personas
        const gridSize = 16;
        const grid = Array(gridSize).fill().map(() => Array(gridSize).fill(0));
        
        people.forEach(person => {
            if (person.evacuated) return;
            
            const gridX = Math.floor(((person.position.x + this.width/2) / this.width) * gridSize);
            const gridZ = Math.floor(((person.position.z + this.depth/2) / this.depth) * gridSize);
            
            if (gridX >= 0 && gridX < gridSize && gridZ >= 0 && gridZ < gridSize) {
                grid[gridZ][gridX]++;
            }
        });
        
        // Dibujar heatmap
        const cellWidth = canvas.width / gridSize;
        const cellHeight = canvas.height / gridSize;
        
        for (let i = 0; i < gridSize; i++) {
            for (let j = 0; j < gridSize; j++) {
                const value = grid[i][j];
                if (value > 0) {
                    const intensity = Math.min(value / 5, 1);
                    context.fillStyle = `rgba(255, ${255 - intensity * 255}, 0, ${intensity * 0.8})`;
                    context.fillRect(j * cellWidth, i * cellHeight, cellWidth, cellHeight);
                }
            }
        }
        
        // Actualizar textura
        this.heatmapPlane.material.map.needsUpdate = true;
    }
    
    /**
     * Verificar colisión con obstáculos internos
     * @param {THREE.Vector3} position - Posición a verificar
     * @param {number} radius - Radio de colisión
     * @returns {boolean} - true si hay colisión
     */
    checkObstacleCollision(position, radius) {
        for (let obstacle of this.obstacles) {
            if (obstacle.type === 'box') {
                // Colisión con caja (pared)
                const halfWidth = obstacle.size.width / 2;
                const halfDepth = obstacle.size.depth / 2;
                
                // Punto más cercano de la caja a la posición
                const closestX = Math.max(
                    obstacle.position.x - halfWidth,
                    Math.min(position.x, obstacle.position.x + halfWidth)
                );
                const closestZ = Math.max(
                    obstacle.position.z - halfDepth,
                    Math.min(position.z, obstacle.position.z + halfDepth)
                );
                
                // Distancia del punto más cercano a la posición
                const distanceX = position.x - closestX;
                const distanceZ = position.z - closestZ;
                const distanceSquared = distanceX * distanceX + distanceZ * distanceZ;
                
                // Hay colisión si la distancia es menor que el radio
                if (distanceSquared < radius * radius) {
                    return true;
                }
            } 
            else if (obstacle.type === 'cylinder') {
                // Colisión con cilindro (columna)
                const dx = position.x - obstacle.position.x;
                const dz = position.z - obstacle.position.z;
                const distanceSquared = dx * dx + dz * dz;
                const totalRadius = radius + obstacle.radius;
                
                // Hay colisión si la distancia es menor que la suma de radios
                if (distanceSquared < totalRadius * totalRadius) {
                    return true;
                }
            }
        }
        
        return false; // Sin colisiones
    }
}
