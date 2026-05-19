// ========================================
// HYBRID-CONTROLS.JS - Sistema de Control Híbrido
// ========================================

class HybridControls {
    constructor(camera, renderer, updateControlUI) {
        this.camera = camera;
        this.renderer = renderer;
        this.updateControlUI = updateControlUI;
        
        // Modos de control disponibles
        this.modes = {
            GESTURES: 'gestures',
            KEYBOARD: 'keyboard',
            MOUSE: 'mouse'
        };
        
        this.currentMode = this.modes.KEYBOARD;
        
        // Estado de teclas presionadas
        this.keys = {};
        
        // Estado del ratón
        this.mouse = {
            isDragging: false,
            lastX: 0,
            lastY: 0
        };
        
        // Parámetros de cámara
        this.cameraTarget = new THREE.Vector3(0, 0, 0);
        this.cameraDistance = 50;
        this.cameraAngleY = Math.PI / 6;  // Ángulo vertical (30°)
        this.cameraAngleX = Math.PI / 4;  // Ángulo horizontal (45°)
        
        // Velocidades
        this.moveSpeed = 0.5;
        this.rotateSpeed = 0.02;
        this.zoomSpeed = 2;
        
        // Controles por gestos (MediaPipe)
        this.handControls = null;
        
        // Inicializar event listeners
        this.initEventListeners();
        
        // Actualizar posición inicial
        this.updateCameraPosition();
        
        console.log('🎮 Sistema de controles híbridos inicializado');
    }
    
    initEventListeners() {
        // Teclado
        window.addEventListener('keydown', (e) => this.onKeyDown(e));
        window.addEventListener('keyup', (e) => this.onKeyUp(e));
        
        // Ratón
        const canvas = this.renderer.domElement;
        canvas.addEventListener('mousedown', (e) => this.onMouseDown(e));
        canvas.addEventListener('mousemove', (e) => this.onMouseMove(e));
        canvas.addEventListener('mouseup', (e) => this.onMouseUp(e));
        canvas.addEventListener('wheel', (e) => this.onMouseWheel(e));
        
        // Prevenir menú contextual en el canvas
        canvas.addEventListener('contextmenu', (e) => e.preventDefault());
    }
    
    // ========================================
    // CONTROLES DE TECLADO
    // ========================================
    
    onKeyDown(e) {
        this.keys[e.key.toLowerCase()] = true;
        
        // Cambio rápido de modo con tecla Tab
        if (e.key === 'Tab') {
            e.preventDefault();
            this.cycleControlMode();
        }
    }
    
    onKeyUp(e) {
        this.keys[e.key.toLowerCase()] = false;
    }
    
    updateKeyboardControls() {
        if (this.currentMode !== this.modes.KEYBOARD) return;
        
        let moved = false;
        
        // Calcular vectores de dirección basados en la rotación actual de la cámara
        // Importante: usar la misma convención que updateCameraPosition()
        // en coordenadas esféricas: angleX es azimut, angleY es elevación
        
        // Forward: dirección hacia donde apunta la cámara (proyectado en plano horizontal)
        // La cámara mira HACIA el target, así que el forward es -gradiente de posición
        const forward = new THREE.Vector3(
            -Math.cos(this.cameraAngleX),  // componente X
            0,                              // no mover en Y con WASD
            -Math.sin(this.cameraAngleX)   // componente Z
        ).normalize();
        
        // Right: perpendicular al forward, 90° a la derecha en plano horizontal
        const right = new THREE.Vector3(
            Math.sin(this.cameraAngleX),   // cos(angle - 90°) = sin(angle)
            0,
            -Math.cos(this.cameraAngleX)   // sin(angle - 90°) = -cos(angle)
        ).normalize();
        
        // Movimiento de cámara (WASD) - Relativo a la orientación
        if (this.keys['w']) {
            this.cameraTarget.add(forward.clone().multiplyScalar(this.moveSpeed));
            moved = true;
        }
        if (this.keys['s']) {
            this.cameraTarget.add(forward.clone().multiplyScalar(-this.moveSpeed));
            moved = true;
        }
        if (this.keys['a']) {
            this.cameraTarget.add(right.clone().multiplyScalar(-this.moveSpeed));
            moved = true;
        }
        if (this.keys['d']) {
            this.cameraTarget.add(right.clone().multiplyScalar(this.moveSpeed));
            moved = true;
        }
        
        // Rotación (Q/E)
        if (this.keys['q']) {
            this.cameraAngleX -= this.rotateSpeed;
            moved = true;
        }
        if (this.keys['e']) {
            this.cameraAngleX += this.rotateSpeed;
            moved = true;
        }
        
        // Zoom (R/F)
        if (this.keys['r']) {
            this.cameraDistance = Math.max(10, this.cameraDistance - this.zoomSpeed);
            moved = true;
        }
        if (this.keys['f']) {
            this.cameraDistance = Math.min(100, this.cameraDistance + this.zoomSpeed);
            moved = true;
        }
        
        if (moved) {
            this.updateCameraPosition();
        }
    }
    
    // ========================================
    // CONTROLES DE RATÓN
    // ========================================
    
    onMouseDown(e) {
        if (this.currentMode !== this.modes.MOUSE) return;
        
        this.mouse.isDragging = true;
        this.mouse.lastX = e.clientX;
        this.mouse.lastY = e.clientY;
    }
    
    onMouseMove(e) {
        if (!this.mouse.isDragging || this.currentMode !== this.modes.MOUSE) return;
        
        const deltaX = e.clientX - this.mouse.lastX;
        const deltaY = e.clientY - this.mouse.lastY;
        
        // Rotar cámara
        this.cameraAngleX += deltaX * 0.005;
        this.cameraAngleY = Math.max(0.1, Math.min(Math.PI / 2 - 0.1, this.cameraAngleY - deltaY * 0.005));
        
        this.updateCameraPosition();
        
        this.mouse.lastX = e.clientX;
        this.mouse.lastY = e.clientY;
    }
    
    onMouseUp(e) {
        this.mouse.isDragging = false;
    }
    
    onMouseWheel(e) {
        if (this.currentMode !== this.modes.MOUSE) return;
        
        e.preventDefault();
        
        const delta = e.deltaY > 0 ? 1 : -1;
        this.cameraDistance = Math.max(10, Math.min(100, this.cameraDistance + delta * 2));
        
        this.updateCameraPosition();
    }
    
    // ========================================
    // CONTROLES POR GESTOS (MediaPipe)
    // ========================================
    
    initGestureControls(updateGestureUI) {
        this.handControls = new HandControls(this.camera, updateGestureUI);
        console.log('✋ Controles por gestos activados');
    }
    
    updateGestureControls() {
        if (this.currentMode !== this.modes.GESTURES || !this.handControls) return;
        
        this.handControls.update();
    }
    
    // ========================================
    // GESTIÓN DE MODOS
    // ========================================
    
    setMode(mode) {
        if (!Object.values(this.modes).includes(mode)) {
            console.warn(`Modo de control desconocido: ${mode}`);
            return;
        }
        
        this.currentMode = mode;
        
        // Notificar cambio de modo
        const modeNames = {
            [this.modes.GESTURES]: '✋ Gestos',
            [this.modes.KEYBOARD]: '⌨️ Teclado',
            [this.modes.MOUSE]: '🖱️ Ratón'
        };
        
        if (this.updateControlUI) {
            this.updateControlUI(modeNames[mode]);
        }
        
        console.log(`🎮 Modo de control: ${modeNames[mode]}`);
    }
    
    cycleControlMode() {
        const modes = Object.values(this.modes);
        const currentIndex = modes.indexOf(this.currentMode);
        const nextIndex = (currentIndex + 1) % modes.length;
        
        // Saltar gestos si MediaPipe no está disponible
        if (modes[nextIndex] === this.modes.GESTURES && !this.handControls) {
            this.setMode(modes[(nextIndex + 1) % modes.length]);
        } else {
            this.setMode(modes[nextIndex]);
        }
    }
    
    // ========================================
    // ACTUALIZACIÓN DE CÁMARA
    // ========================================
    
    updateCameraPosition() {
        // Calcular posición de cámara en coordenadas esféricas
        const x = this.cameraTarget.x + this.cameraDistance * Math.sin(this.cameraAngleY) * Math.cos(this.cameraAngleX);
        const y = this.cameraTarget.y + this.cameraDistance * Math.cos(this.cameraAngleY);
        const z = this.cameraTarget.z + this.cameraDistance * Math.sin(this.cameraAngleY) * Math.sin(this.cameraAngleX);
        
        this.camera.position.set(x, y, z);
        this.camera.lookAt(this.cameraTarget);
    }
    
    // ========================================
    // BUCLE PRINCIPAL
    // ========================================
    
    update() {
        switch(this.currentMode) {
            case this.modes.KEYBOARD:
                this.updateKeyboardControls();
                break;
            case this.modes.GESTURES:
                this.updateGestureControls();
                break;
            case this.modes.MOUSE:
                // El ratón se actualiza con eventos, no necesita update continuo
                break;
        }
    }
    
    // ========================================
    // UTILIDADES
    // ========================================
    
    getControlsHelp() {
        return {
            keyboard: [
                'WASD - Mover cámara',
                'Q/E - Rotar',
                'R/F - Zoom',
                'Tab - Cambiar modo'
            ],
            mouse: [
                'Click + Arrastrar - Rotar',
                'Scroll - Zoom',
                'Tab - Cambiar modo'
            ],
            gestures: [
                'Palma abierta - Mover',
                'Pinza - Rotar',
                'Dos manos - Zoom',
                'Tab - Cambiar modo'
            ]
        };
    }
    
    reset() {
        this.cameraTarget.set(0, 0, 0);
        this.cameraDistance = 50;
        this.cameraAngleY = Math.PI / 6;
        this.cameraAngleX = Math.PI / 4;
        this.updateCameraPosition();
    }
}
