// ========================================
// HAND-CONTROLS.JS - Control por gestos
// ========================================

class HandControls {
    constructor(camera, gestureCallback) {
        this.camera = camera;
        this.gestureCallback = gestureCallback;
        this.hands = null;
        this.videoElement = document.getElementById('webcam');
        this.canvasElement = document.getElementById('hand-canvas');
        this.canvasCtx = this.canvasElement.getContext('2d');
        
        // Estado de las manos
        this.leftHand = null;
        this.rightHand = null;
        this.previousLeftHand = null;
        this.previousRightHand = null;
        
        // Estado del gesto actual
        this.currentGesture = 'idle';
        
        // Parámetros de control
        this.panSensitivity = 0.5;
        this.rotateSensitivity = 0.01;
        this.zoomSensitivity = 0.1;
        
        // Posición inicial de la cámara (para reset)
        this.initialCameraPosition = this.camera.position.clone();
        
        this.initMediaPipe();
    }
    
    async initMediaPipe() {
        console.log('👋 Inicializando detección de manos...');
        
        try {
            // Configurar MediaPipe Hands
            this.hands = new Hands({
                locateFile: (file) => {
                    return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
                }
            });
            
            this.hands.setOptions({
                maxNumHands: 2,
                modelComplexity: 1,
                minDetectionConfidence: 0.5,
                minTrackingConfidence: 0.5
            });
            
            this.hands.onResults((results) => this.onResults(results));
            
            // Iniciar webcam
            const stream = await navigator.mediaDevices.getUserMedia({ 
                video: { 
                    width: 640, 
                    height: 480,
                    facingMode: 'user'
                } 
            });
            
            this.videoElement.srcObject = stream;
            
            // Ajustar tamaño del canvas
            this.canvasElement.width = this.videoElement.videoWidth || 640;
            this.canvasElement.height = this.videoElement.videoHeight || 480;
            
            console.log('✅ Webcam iniciada correctamente');
            
        } catch (error) {
            console.error('❌ Error al inicializar webcam:', error);
            this.gestureCallback('error');
        }
    }
    
    onResults(results) {
        // Limpiar canvas
        this.canvasCtx.save();
        this.canvasCtx.clearRect(0, 0, this.canvasElement.width, this.canvasElement.height);
        
        // Dibujar landmarks si hay manos detectadas
        if (results.multiHandLandmarks && results.multiHandedness) {
            this.leftHand = null;
            this.rightHand = null;
            
            for (let i = 0; i < results.multiHandLandmarks.length; i++) {
                const landmarks = results.multiHandLandmarks[i];
                const handedness = results.multiHandedness[i].label; // "Left" o "Right"
                
                // Dibujar skeleton de la mano
                this.drawHand(landmarks);
                
                // Guardar datos de la mano
                if (handedness === 'Left') {
                    this.leftHand = landmarks;
                } else {
                    this.rightHand = landmarks;
                }
            }
            
            // Detectar y aplicar gestos
            this.detectAndApplyGesture();
        } else {
            this.currentGesture = 'idle';
            this.gestureCallback('idle');
        }
        
        this.canvasCtx.restore();
        
        // Guardar estado anterior
        this.previousLeftHand = this.leftHand;
        this.previousRightHand = this.rightHand;
    }
    
    drawHand(landmarks) {
        // Dibujar puntos de los dedos
        landmarks.forEach(landmark => {
            const x = landmark.x * this.canvasElement.width;
            const y = landmark.y * this.canvasElement.height;
            
            this.canvasCtx.beginPath();
            this.canvasCtx.arc(x, y, 5, 0, 2 * Math.PI);
            this.canvasCtx.fillStyle = '#00ff00';
            this.canvasCtx.fill();
        });
        
        // Dibujar conexiones
        const connections = [
            [0, 1], [1, 2], [2, 3], [3, 4],      // Pulgar
            [0, 5], [5, 6], [6, 7], [7, 8],      // Índice
            [0, 9], [9, 10], [10, 11], [11, 12], // Medio
            [0, 13], [13, 14], [14, 15], [15, 16], // Anular
            [0, 17], [17, 18], [18, 19], [19, 20], // Meñique
            [5, 9], [9, 13], [13, 17]            // Palma
        ];
        
        connections.forEach(([start, end]) => {
            const startPoint = landmarks[start];
            const endPoint = landmarks[end];
            
            this.canvasCtx.beginPath();
            this.canvasCtx.moveTo(
                startPoint.x * this.canvasElement.width,
                startPoint.y * this.canvasElement.height
            );
            this.canvasCtx.lineTo(
                endPoint.x * this.canvasElement.width,
                endPoint.y * this.canvasElement.height
            );
            this.canvasCtx.strokeStyle = '#00ff00';
            this.canvasCtx.lineWidth = 2;
            this.canvasCtx.stroke();
        });
    }
    
    detectAndApplyGesture() {
        // GESTO 1: Una mano abierta = PAN (mover cámara)
        if ((this.leftHand && !this.rightHand) || (!this.leftHand && this.rightHand)) {
            const hand = this.leftHand || this.rightHand;
            const previousHand = this.previousLeftHand || this.previousRightHand;
            
            if (this.isHandOpen(hand) && previousHand) {
                this.applyPan(hand, previousHand);
                this.currentGesture = 'pan';
                this.gestureCallback('pan');
                return;
            }
        }
        
        // GESTO 2: Pinch (índice y pulgar juntos) = ROTATE
        if (this.leftHand || this.rightHand) {
            const hand = this.leftHand || this.rightHand;
            const previousHand = this.previousLeftHand || this.previousRightHand;
            
            if (this.isPinching(hand) && previousHand) {
                this.applyRotate(hand, previousHand);
                this.currentGesture = 'rotate';
                this.gestureCallback('rotate');
                return;
            }
        }
        
        // GESTO 3: Dos manos abiertas = ZOOM
        if (this.leftHand && this.rightHand && this.previousLeftHand && this.previousRightHand) {
            if (this.isHandOpen(this.leftHand) && this.isHandOpen(this.rightHand)) {
                this.applyZoom();
                this.currentGesture = 'zoom';
                this.gestureCallback('zoom');
                return;
            }
        }
        
        this.currentGesture = 'idle';
    }
    
    isHandOpen(hand) {
        // Verificar si la mano está abierta comparando distancias
        const wrist = hand[0];
        const indexTip = hand[8];
        const middleTip = hand[12];
        const ringTip = hand[16];
        const pinkyTip = hand[20];
        
        const avgDistance = (
            this.distance2D(wrist, indexTip) +
            this.distance2D(wrist, middleTip) +
            this.distance2D(wrist, ringTip) +
            this.distance2D(wrist, pinkyTip)
        ) / 4;
        
        return avgDistance > 0.25; // Threshold para mano abierta
    }
    
    isPinching(hand) {
        // Verificar si índice y pulgar están juntos
        const thumbTip = hand[4];
        const indexTip = hand[8];
        
        const distance = this.distance2D(thumbTip, indexTip);
        return distance < 0.08; // Threshold para pinch
    }
    
    distance2D(point1, point2) {
        const dx = point1.x - point2.x;
        const dy = point1.y - point2.y;
        return Math.sqrt(dx * dx + dy * dy);
    }
    
    applyPan(hand, previousHand) {
        // Obtener el punto central de la palma
        const currentPalm = hand[9]; // Punto medio de la palma
        const previousPalm = previousHand[9];
        
        const deltaX = (currentPalm.x - previousPalm.x) * this.panSensitivity;
        const deltaY = (currentPalm.y - previousPalm.y) * this.panSensitivity;
        
        // Mover cámara
        this.camera.position.x -= deltaX * 50;
        this.camera.position.z += deltaY * 50;
    }
    
    applyRotate(hand, previousHand) {
        const currentIndex = hand[8];
        const previousIndex = previousHand[8];
        
        const deltaX = (currentIndex.x - previousIndex.x) * this.rotateSensitivity;
        
        // Rotar cámara alrededor del centro
        const radius = Math.sqrt(
            this.camera.position.x ** 2 + 
            this.camera.position.z ** 2
        );
        
        const currentAngle = Math.atan2(this.camera.position.z, this.camera.position.x);
        const newAngle = currentAngle + deltaX * 10;
        
        this.camera.position.x = radius * Math.cos(newAngle);
        this.camera.position.z = radius * Math.sin(newAngle);
        this.camera.lookAt(0, 0, 0);
    }
    
    applyZoom() {
        // Calcular distancia entre las dos manos
        const leftPalm = this.leftHand[9];
        const rightPalm = this.rightHand[9];
        const currentDistance = this.distance2D(leftPalm, rightPalm);
        
        if (this.previousLeftHand && this.previousRightHand) {
            const prevLeftPalm = this.previousLeftHand[9];
            const prevRightPalm = this.previousRightHand[9];
            const previousDistance = this.distance2D(prevLeftPalm, prevRightPalm);
            
            const deltaDistance = currentDistance - previousDistance;
            
            // Zoom in/out
            const zoomFactor = 1 + deltaDistance * this.zoomSensitivity * 10;
            this.camera.position.multiplyScalar(zoomFactor);
            
            // Limitar zoom
            const distance = this.camera.position.length();
            if (distance < 15) {
                this.camera.position.normalize().multiplyScalar(15);
            } else if (distance > 100) {
                this.camera.position.normalize().multiplyScalar(100);
            }
        }
    }
    
    update() {
        // Enviar frame a MediaPipe si está disponible
        if (this.hands && this.videoElement.readyState >= 2) {
            this.hands.send({ image: this.videoElement });
        }
    }
    
    reset() {
        this.camera.position.copy(this.initialCameraPosition);
        this.camera.lookAt(0, 0, 0);
    }
}
