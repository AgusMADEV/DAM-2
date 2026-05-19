// ========================================
// PERSON.JS - Persona evacuando
// ========================================

class Person {
    constructor(position) {
        this.position = position.clone();
        this.velocity = new THREE.Vector3();
        this.speed = 2 + Math.random() * 2; // Velocidad variable (2-4 m/s)
        this.evacuated = false;
        this.evacuationTime = 0;
        this.mesh = null;
        this.targetExit = null;
        this.panicLevel = Math.random(); // 0-1, afecta comportamiento
        
        // Comportamiento del algoritmo genético
        this.behavior = {
            followCrowd: Math.random(),      // Tendencia a seguir a otros
            seekNearestExit: Math.random(),  // Tendencia a buscar salida más cercana
            avoidCrowds: Math.random(),      // Tendencia a evitar multitudes
            panicThreshold: Math.random()    // Nivel de pánico que activa comportamientos erráticos
        };
        
        this.createMesh();
    }
    
    createMesh() {
        // Geometría de persona simplificada (cilindro + esfera para cabeza)
        // CapsuleGeometry no existe en Three.js r128, usamos combinación de geometrías
        
        // Color basado en nivel de pánico
        const color = new THREE.Color();
        color.setHSL(0.3 - this.panicLevel * 0.3, 0.7, 0.5);
        
        const bodyMaterial = new THREE.MeshStandardMaterial({
            color: color,
            roughness: 0.7,
            metalness: 0.1
        });
        
        // Crear grupo para la persona
        this.mesh = new THREE.Group();
        
        // Cuerpo (cilindro)
        const bodyGeometry = new THREE.CylinderGeometry(0.25, 0.25, 1.0, 8);
        const bodyMesh = new THREE.Mesh(bodyGeometry, bodyMaterial);
        bodyMesh.position.y = 0.5;
        bodyMesh.castShadow = true;
        bodyMesh.receiveShadow = true;
        this.mesh.add(bodyMesh);
        
        // Cabeza (esfera)
        const headGeometry = new THREE.SphereGeometry(0.2, 8, 8);
        const headMesh = new THREE.Mesh(headGeometry, bodyMaterial);
        headMesh.position.y = 1.15;
        headMesh.castShadow = true;
        headMesh.receiveShadow = true;
        this.mesh.add(headMesh);
        
        this.mesh.position.copy(this.position);
    }
    
    addToScene(scene) {
        if (this.mesh) {
            scene.add(this.mesh);
        }
    }
    
    remove(scene) {
        if (this.mesh) {
            scene.remove(this.mesh);
        }
    }
    
    update(deltaTime, building, allPeople) {
        if (this.evacuated) return;
        
        this.evacuationTime += deltaTime;
        
        // Seleccionar salida objetivo
        if (!this.targetExit) {
            this.targetExit = this.selectExit(building);
        }
        
        // Calcular dirección hacia la salida
        const direction = new THREE.Vector3();
        direction.subVectors(this.targetExit.position, this.position);
        direction.y = 0; // Solo movimiento horizontal
        direction.normalize();
        
        // Aplicar comportamientos (evitación de obstáculos y personas)
        this.applyBehaviors(direction, building, allPeople);
        
        // Aplicar velocidad
        this.velocity.copy(direction);
        this.velocity.multiplyScalar(this.speed * deltaTime);
        
        // Guardar posición anterior para detección de colisiones
        const previousPosition = this.position.clone();
        
        // Actualizar posición
        this.position.add(this.velocity);
        
        // Verificar colisiones y revertir si es necesario
        if (this.checkCollisions(building, allPeople)) {
            this.position.copy(previousPosition);
            // Intentar movimiento lateral
            this.tryAlternativeMovement(deltaTime);
        }
        
        // Mantener dentro de límites
        this.clampPosition(building);
        
        // Actualizar mesh
        if (this.mesh) {
            this.mesh.position.copy(this.position);
            
            // Rotar hacia la dirección de movimiento
            if (this.velocity.length() > 0.01) {
                const angle = Math.atan2(this.velocity.x, this.velocity.z);
                this.mesh.rotation.y = angle;
            }
            
            // Animación simple de "caminar" (bobbing)
            // La persona ahora mide ~1.35 total (cuerpo + cabeza)
            this.mesh.position.y = 0.7 + Math.sin(this.evacuationTime * 10) * 0.05;
        }
    }
    
    selectExit(building) {
        // Estrategia basada en comportamiento
        const nearestExit = building.getNearestExit(this.position);
        
        if (Math.random() < this.behavior.seekNearestExit) {
            return nearestExit;
        } else {
            // Seleccionar salida aleatoria (menos óptimo)
            const randomIndex = Math.floor(Math.random() * building.exits.length);
            return building.exits[randomIndex];
        }
    }
    
    applyBehaviors(direction, building, allPeople) {
        // Vector de evitación
        const avoidance = new THREE.Vector3();
        
        // 1. Evitar otras personas
        const personalSpace = 1.0; // Radio de espacio personal
        allPeople.forEach(other => {
            if (other === this || other.evacuated) return;
            
            const distance = this.position.distanceTo(other.position);
            if (distance < personalSpace && distance > 0) {
                // Vector desde la otra persona hacia esta
                const away = new THREE.Vector3();
                away.subVectors(this.position, other.position);
                away.y = 0;
                away.normalize();
                
                // Fuerza inversamente proporcional a la distancia
                const force = (personalSpace - distance) / personalSpace;
                away.multiplyScalar(force * this.behavior.avoidCrowds);
                avoidance.add(away);
            }
        });
        
        // 2. Evitar paredes (steering behavior)
        const wallDistance = 2.0; // Distancia para anticipar paredes
        const halfWidth = building.width / 2;
        const halfDepth = building.depth / 2;
        
        // Pared derecha
        if (this.position.x > halfWidth - wallDistance) {
            avoidance.x -= (this.position.x - (halfWidth - wallDistance)) * 0.5;
        }
        // Pared izquierda
        if (this.position.x < -halfWidth + wallDistance) {
            avoidance.x += ((-halfWidth + wallDistance) - this.position.x) * 0.5;
        }
        // Pared frontal
        if (this.position.z > halfDepth - wallDistance) {
            avoidance.z -= (this.position.z - (halfDepth - wallDistance)) * 0.5;
        }
        // Pared trasera
        if (this.position.z < -halfDepth + wallDistance) {
            avoidance.z += ((-halfDepth + wallDistance) - this.position.z) * 0.5;
        }
        
        // 2b. Evitar obstáculos internos (columnas y paredes divisorias)
        const obstacleAvoidanceRadius = 2.5; // Radio de detección anticipada
        building.obstacles.forEach(obstacle => {
            if (obstacle.type === 'cylinder') {
                // Evitar columnas
                const dx = this.position.x - obstacle.position.x;
                const dz = this.position.z - obstacle.position.z;
                const distance = Math.sqrt(dx * dx + dz * dz);
                
                if (distance < obstacleAvoidanceRadius && distance > 0) {
                    const force = (obstacleAvoidanceRadius - distance) / obstacleAvoidanceRadius;
                    avoidance.x += (dx / distance) * force * 0.8;
                    avoidance.z += (dz / distance) * force * 0.8;
                }
            } 
            else if (obstacle.type === 'box') {
                // Evitar paredes divisorias
                const halfWidth = obstacle.size.width / 2;
                const halfDepth = obstacle.size.depth / 2;
                
                // Punto más cercano de la caja
                const closestX = Math.max(
                    obstacle.position.x - halfWidth,
                    Math.min(this.position.x, obstacle.position.x + halfWidth)
                );
                const closestZ = Math.max(
                    obstacle.position.z - halfDepth,
                    Math.min(this.position.z, obstacle.position.z + halfDepth)
                );
                
                const dx = this.position.x - closestX;
                const dz = this.position.z - closestZ;
                const distance = Math.sqrt(dx * dx + dz * dz);
                
                if (distance < obstacleAvoidanceRadius && distance > 0) {
                    const force = (obstacleAvoidanceRadius - distance) / obstacleAvoidanceRadius;
                    avoidance.x += (dx / distance) * force * 0.8;
                    avoidance.z += (dz / distance) * force * 0.8;
                }
            }
        });
        
        // 3. Aplicar evitación a la dirección
        if (avoidance.length() > 0) {
            avoidance.normalize();
            direction.add(avoidance.multiplyScalar(0.5));
            direction.normalize();
        }
        
        // 4. Comportamiento de seguir multitudes (si está activado)
        if (this.behavior.followCrowd > 0.5) {
            const crowdDirection = this.getFlockDirection(allPeople);
            if (crowdDirection.length() > 0) {
                direction.add(crowdDirection.multiplyScalar(0.2 * this.behavior.followCrowd));
                direction.normalize();
            }
        }
    }
    
    checkCollisions(building, allPeople) {
        // Radio de colisión de la persona
        const collisionRadius = 0.4;
        
        // 1. Verificar colisión con límites del edificio
        const halfWidth = building.width / 2 - 0.5;
        const halfDepth = building.depth / 2 - 0.5;
        
        if (Math.abs(this.position.x) > halfWidth || 
            Math.abs(this.position.z) > halfDepth) {
            return true; // Colisión con pared perimetral
        }
        
        // 2. Verificar colisión con obstáculos internos (columnas, paredes divisorias)
        if (building.checkObstacleCollision(this.position, collisionRadius)) {
            return true; // Colisión con obstáculo interno
        }
        
        // 3. Verificar colisión con otras personas
        for (let other of allPeople) {
            if (other === this || other.evacuated) continue;
            
            const distance = this.position.distanceTo(other.position);
            if (distance < collisionRadius * 2) {
                return true; // Colisión con otra persona
            }
        }
        
        return false; // Sin colisiones
    }
    
    tryAlternativeMovement(deltaTime) {
        // Intentar movimiento lateral cuando hay colisión
        const alternativeVelocity = new THREE.Vector3(
            -this.velocity.z,
            0,
            this.velocity.x
        );
        alternativeVelocity.multiplyScalar(0.5);
        this.position.add(alternativeVelocity);
    }
    
    getFlockDirection(allPeople) {
        // Calcular dirección promedio de personas cercanas
        const flockRadius = 3.0;
        const flockDirection = new THREE.Vector3();
        let count = 0;
        
        allPeople.forEach(other => {
            if (other === this || other.evacuated) return;
            
            const distance = this.position.distanceTo(other.position);
            if (distance < flockRadius) {
                flockDirection.add(other.velocity);
                count++;
            }
        });
        
        if (count > 0) {
            flockDirection.divideScalar(count);
            flockDirection.normalize();
        }
        
        return flockDirection;
    }
    
    clampPosition(building) {
        const halfWidth = building.width / 2 - 1;
        const halfDepth = building.depth / 2 - 1;
        
        this.position.x = Math.max(-halfWidth, Math.min(halfWidth, this.position.x));
        this.position.z = Math.max(-halfDepth, Math.min(halfDepth, this.position.z));
        this.position.y = 0.7; // Altura fija ajustada para nueva geometría
    }
    
    getFitness() {
        // Fitness para el algoritmo genético
        // Menor tiempo de evacuación = mejor fitness
        return this.evacuationTime > 0 ? 1 / this.evacuationTime : 0;
    }
    
    clone() {
        const newPerson = new Person(this.position);
        newPerson.behavior = { ...this.behavior };
        return newPerson;
    }
    
    mutate(mutationRate = 0.1) {
        // Mutación de comportamientos
        Object.keys(this.behavior).forEach(key => {
            if (Math.random() < mutationRate) {
                this.behavior[key] = Math.max(0, Math.min(1, 
                    this.behavior[key] + (Math.random() - 0.5) * 0.2
                ));
            }
        });
    }
}
