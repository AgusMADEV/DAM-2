// ========================================
// MAIN.JS - Sistema de Evacuación
// ========================================

// Variables globales de la escena Three.js
let scene, camera, renderer;
let building;
let people = [];
let geneticAlgorithm;
let hybridControls;
let dataManager;

// Estado de la simulación
let simulationRunning = false;
let showHeatmap = false;
let config = {
    numPeople: 50,
    numExits: 2,
    evolutionSpeed: 5
};

// Estadísticas
let stats = {
    evacuated: 0,
    generation: 1,
    avgTime: 0,
    totalTime: 0
};

// Datos de evolución y records
let evolutionData = [];
let bestTimeEver = Infinity;
let bestGenerationEver = 0;

// Canvas del gráfico
let evolutionCanvas = null;
let evolutionCtx = null;

// Inicialización cuando carga la página
window.addEventListener('load', init);

function init() {
    console.log('🚀 Inicializando SecurePath...');
    
    // Inicializar gestor de datos
    dataManager = new DataManager();
    
    // Cargar records desde localStorage
    loadRecordsFromStorage();
    
    // Cargar presets
    loadPresetsUI();
    
    // Inicializar canvas del gráfico
    evolutionCanvas = document.getElementById('evolution-chart');
    evolutionCtx = evolutionCanvas.getContext('2d');
    evolutionCanvas.width = evolutionCanvas.offsetWidth;
    evolutionCanvas.height = evolutionCanvas.offsetHeight;
    
    // Configurar la escena Three.js
    initThreeJS();
    
    // Crear el edificio
    building = new Building(scene);
    
    // Inicializar sistema de controles híbridos
    hybridControls = new HybridControls(camera, renderer, updateControlModeUI);
    
    // Intentar inicializar controles por gestos (MediaPipe)
    try {
        hybridControls.initGestureControls(updateGestureUI);
    } catch (error) {
        console.warn('⚠️ MediaPipe no disponible, usando solo teclado/ratón');
    }
    
    // Inicializar algoritmo genético
    geneticAlgorithm = new GeneticAlgorithm(config);
    
    // Event listeners para los controles
    setupEventListeners();
    
    // Dibujar gráfico inicial vacío
    drawEvolutionChart();
    
    // Iniciar el bucle de animación
    animate();
    
    console.log('✅ SecurePath inicializado correctamente');
}

function initThreeJS() {
    // Crear la escena
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0e27);
    scene.fog = new THREE.Fog(0x0a0e27, 50, 200);
    
    // Configurar la cámara
    const container = document.getElementById('scene-container');
    camera = new THREE.PerspectiveCamera(
        60,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
    );
    camera.position.set(30, 25, 30);
    camera.lookAt(0, 0, 0);
    
    // Crear el renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    container.appendChild(renderer.domElement);
    
    // Iluminación
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(20, 40, 10);
    directionalLight.castShadow = true;
    directionalLight.shadow.mapSize.width = 2048;
    directionalLight.shadow.mapSize.height = 2048;
    directionalLight.shadow.camera.far = 100;
    scene.add(directionalLight);
    
    // Luz de emergencia roja parpadeante
    const emergencyLight = new THREE.PointLight(0xff0000, 0.5, 50);
    emergencyLight.position.set(0, 15, 0);
    scene.add(emergencyLight);
    
    // Hacer parpadear la luz de emergencia
    let emergencyIntensity = 0.5;
    let emergencyDirection = 0.02;
    setInterval(() => {
        emergencyIntensity += emergencyDirection;
        if (emergencyIntensity > 1 || emergencyIntensity < 0.3) {
            emergencyDirection *= -1;
        }
        emergencyLight.intensity = emergencyIntensity;
    }, 50);
    
    // Responsive
    window.addEventListener('resize', onWindowResize);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function setupEventListeners() {
    // Sliders de configuración
    document.getElementById('num-people').addEventListener('input', (e) => {
        config.numPeople = parseInt(e.target.value);
        document.getElementById('num-people-value').textContent = config.numPeople;
    });
    
    document.getElementById('num-exits').addEventListener('input', (e) => {
        config.numExits = parseInt(e.target.value);
        document.getElementById('num-exits-value').textContent = config.numExits;
        building.updateExits(config.numExits);
    });
    
    document.getElementById('evolution-speed').addEventListener('input', (e) => {
        config.evolutionSpeed = parseInt(e.target.value);
        document.getElementById('evolution-speed-value').textContent = config.evolutionSpeed;
    });
    
    // Botones
    document.getElementById('start-simulation').addEventListener('click', toggleSimulation);
    document.getElementById('reset-simulation').addEventListener('click', resetSimulation);
    document.getElementById('toggle-heatmap').addEventListener('click', toggleHeatmap);
    document.getElementById('reset-history').addEventListener('click', resetEvolutionHistory);
    document.getElementById('cycle-mode').addEventListener('click', () => hybridControls.cycleControlMode());
    
    // Botones de gestión de datos
    document.getElementById('start-experiment').addEventListener('click', startNewExperiment);
    document.getElementById('save-experiment').addEventListener('click', saveCurrentExperiment);
    document.getElementById('save-preset').addEventListener('click', saveConfigPreset);
    document.getElementById('load-preset').addEventListener('click', loadConfigPreset);
    document.getElementById('delete-preset').addEventListener('click', deleteConfigPreset);
    document.getElementById('export-current').addEventListener('click', () => dataManager.downloadCurrentExperiment());
    document.getElementById('export-all').addEventListener('click', () => dataManager.downloadAllExperiments());
    document.getElementById('import-data').addEventListener('click', () => document.getElementById('import-file').click());
    document.getElementById('import-file').addEventListener('change', importDataFile);
    
    // Sistema de pestañas
    setupTabs();
}

// Sistema de pestañas para el panel de datos
function setupTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.dataset.tab;
            
            // Desactivar todas las pestañas
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Activar la pestaña seleccionada
            button.classList.add('active');
            document.getElementById(targetTab + '-tab').classList.add('active');
        });
    });
}

// Iniciar nuevo experimento
function startNewExperiment() {
    const name = document.getElementById('experiment-name').value || 'Experimento_' + Date.now();
    dataManager.startExperiment(name, config);
    
    document.getElementById('save-experiment').disabled = false;
    document.getElementById('start-experiment').disabled = true;
    
    console.log(`🔬 Experimento iniciado: ${name}`);
    alert(`Experimento "${name}" iniciado. Los datos se guardarán automáticamente.`);
}

// Guardar experimento actual
function saveCurrentExperiment() {
    const saved = dataManager.saveCurrentExperiment();
    
    if (saved) {
        document.getElementById('save-experiment').disabled = true;
        document.getElementById('start-experiment').disabled = false;
        updateStorageInfo();
        alert(`Experimento "${saved.name}" guardado exitosamente con ${saved.generations.length} generaciones.`);
    }
}

// Guardar preset de configuración
function saveConfigPreset() {
    const name = document.getElementById('preset-name').value.trim();
    
    if (!name) {
        alert('Por favor, ingresa un nombre para el preset.');
        return;
    }
    
    dataManager.savePreset(name, config);
    loadPresetsUI();
    document.getElementById('preset-name').value = '';
    alert(`Preset "${name}" guardado exitosamente.`);
}

// Cargar preset de configuración
function loadConfigPreset() {
    const select = document.getElementById('preset-list');
    const name = select.value;
    
    if (!name) {
        alert('Por favor, selecciona un preset.');
        return;
    }
    
    const preset = dataManager.loadPreset(name);
    
    if (preset) {
        config.numPeople = preset.config.numPeople;
        config.numExits = preset.config.numExits;
        config.evolutionSpeed = preset.config.evolutionSpeed;
        
        document.getElementById('num-people').value = config.numPeople;
        document.getElementById('num-people-value').textContent = config.numPeople;
        document.getElementById('num-exits').value = config.numExits;
        document.getElementById('num-exits-value').textContent = config.numExits;
        document.getElementById('evolution-speed').value = config.evolutionSpeed;
        document.getElementById('evolution-speed-value').textContent = config.evolutionSpeed;
        
        building.updateExits(config.numExits);
        
        console.log(`📂 Preset "${name}" cargado`);
        alert(`Preset "${name}" cargado exitosamente.`);
    }
}

// Eliminar preset de configuración
function deleteConfigPreset() {
    const select = document.getElementById('preset-list');
    const name = select.value;
    
    if (!name) {
        alert('Por favor, selecciona un preset.');
        return;
    }
    
    if (confirm(`¿Estás seguro de eliminar el preset "${name}"?`)) {
        dataManager.deletePreset(name);
        loadPresetsUI();
        alert(`Preset "${name}" eliminado.`);
    }
}

// Importar archivo de datos
function importDataFile(event) {
    const file = event.target.files[0];
    
    if (!file) return;
    
    const reader = new FileReader();
    
    reader.onload = (e) => {
        const experiment = dataManager.importExperiment(e.target.result);
        
        if (experiment) {
            updateStorageInfo();
            alert(`Experimento "${experiment.name}" importado exitosamente.`);
        } else {
            alert('Error al importar el archivo. Verifica que sea un archivo válido.');
        }
    };
    
    reader.readAsText(file);
    event.target.value = ''; // Reset input
}

function toggleSimulation() {
    const button = document.getElementById('start-simulation');
    
    if (!simulationRunning) {
        // Iniciar simulación
        simulationRunning = true;
        button.textContent = '⏸️ Pausar Simulación';
        button.style.background = 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)';
        
        // Crear personas si no existen
        if (people.length === 0) {
            createPeople();
        }
        
        console.log('▶️ Simulación iniciada');
    } else {
        // Pausar simulación
        simulationRunning = false;
        button.textContent = '▶️ Continuar Simulación';
        button.style.background = 'linear-gradient(135deg, #4ade80 0%, #22c55e 100%)';
        
        console.log('⏸️ Simulación pausada');
    }
}

function resetSimulation() {
    // Limpiar personas de la escena
    people.forEach(person => person.remove(scene));
    people = [];
    
    // Reiniciar estadísticas
    stats.evacuated = 0;
    stats.generation = 1;
    stats.avgTime = 0;
    stats.totalTime = 0;
    
    updateStatsUI();
    
    // Pausar simulación
    simulationRunning = false;
    const button = document.getElementById('start-simulation');
    button.textContent = '▶️ Iniciar Simulación';
    button.style.background = 'linear-gradient(135deg, #4ade80 0%, #22c55e 100%)';
    
    console.log('🔄 Simulación reiniciada');
}

function toggleHeatmap() {
    showHeatmap = !showHeatmap;
    building.toggleHeatmap(showHeatmap);
    
    const button = document.getElementById('toggle-heatmap');
    if (showHeatmap) {
        button.textContent = '❄️ Ocultar Mapa de Calor';
    } else {
        button.textContent = '🔥 Mapa de Calor';
    }
}

function createPeople() {
    for (let i = 0; i < config.numPeople; i++) {
        const person = new Person(building.getRandomPosition());
        people.push(person);
        person.addToScene(scene);
    }
    
    console.log(`👥 Creadas ${config.numPeople} personas`);
}

function updateSimulation(deltaTime) {
    if (!simulationRunning) return;
    
    // Actualizar cada persona
    let allEvacuated = true;
    
    people.forEach(person => {
        if (!person.evacuated) {
            allEvacuated = false;
            person.update(deltaTime, building, people);
            
            // Verificar si alcanzó una salida
            if (building.isAtExit(person.position)) {
                person.evacuated = true;
                person.remove(scene);
                stats.evacuated++;
                stats.totalTime += person.evacuationTime;
                updateStatsUI();
            }
        }
    });
    
    // Si todos evacuaron, nueva generación
    if (allEvacuated && people.length > 0) {
        nextGeneration();
    }
    
    // Actualizar mapa de calor
    if (showHeatmap) {
        building.updateHeatmap(people);
    }
}

function nextGeneration() {
    console.log(`🧬 Generación ${stats.generation} completada`);
    
    // Calcular tiempo promedio
    stats.avgTime = stats.totalTime / stats.evacuated;
    
    // Obtener estadísticas del algoritmo genético
    const gaStats = geneticAlgorithm.getStats(people);
    
    // Guardar datos de evolución para el gráfico
    evolutionData.push({
        generation: stats.generation,
        best: gaStats.min,      // Mejor tiempo (menor)
        avg: gaStats.avg,        // Tiempo promedio
        worst: gaStats.max       // Peor tiempo (mayor)
    });
    
    // Mantener solo las últimas 50 generaciones en el gráfico
    if (evolutionData.length > 50) {
        evolutionData.shift();
    }
    
    // Verificar si hay nuevo récord
    if (stats.avgTime < bestTimeEver) {
        bestTimeEver = stats.avgTime;
        bestGenerationEver = stats.generation;
        saveRecordsToStorage();
        console.log(`🏆 ¡Nuevo récord! Tiempo: ${bestTimeEver.toFixed(1)}s en generación ${bestGenerationEver}`);
    }
    
    // Registrar datos en experimento activo (si existe)
    if (dataManager && dataManager.currentExperiment) {
        dataManager.recordGeneration({
            generation: stats.generation,
            evacuated: stats.evacuated,
            avgTime: stats.avgTime,
            best: gaStats.min,
            worst: gaStats.max,
            totalTime: stats.totalTime
        });
    }
    
    // Algoritmo genético: evolucionar comportamientos
    const newBehaviors = geneticAlgorithm.evolve(people);
    
    // Incrementar generación
    stats.generation++;
    
    // Reiniciar personas con nuevos comportamientos
    people.forEach(person => person.remove(scene));
    people = [];
    
    for (let i = 0; i < config.numPeople; i++) {
        const person = new Person(building.getRandomPosition());
        person.behavior = newBehaviors[i % newBehaviors.length];
        people.push(person);
        person.addToScene(scene);
    }
    
    // Reiniciar contadores
    stats.evacuated = 0;
    stats.totalTime = 0;
    
    updateStatsUI();
    drawEvolutionChart();
}

function updateStatsUI() {
    document.getElementById('evacuated-count').textContent = stats.evacuated;
    document.getElementById('avg-time').textContent = stats.avgTime.toFixed(1) + 's';
    document.getElementById('generation').textContent = stats.generation;
    
    // Actualizar records
    if (bestTimeEver !== Infinity) {
        document.getElementById('best-time').textContent = bestTimeEver.toFixed(1) + 's';
        document.getElementById('best-generation').textContent = bestGenerationEver;
    } else {
        document.getElementById('best-time').textContent = '--';
        document.getElementById('best-generation').textContent = '--';
    }
}

function updateGestureUI(gesture) {
    const gestureText = document.getElementById('gesture-text');
    
    switch(gesture) {
        case 'pan':
            gestureText.textContent = '👋 Moviendo cámara';
            gestureText.style.color = '#4ade80';
            break;
        case 'rotate':
            gestureText.textContent = '🤏 Rotando cámara';
            gestureText.style.color = '#60a5fa';
            break;
        case 'zoom':
            gestureText.textContent = '✌️ Zoom';
            gestureText.style.color = '#f59e0b';
            break;
        case 'idle':
            gestureText.textContent = '👋 Muestra tus manos';
            gestureText.style.color = '#9ca3af';
            break;
        default:
            gestureText.textContent = '❓ Gesto no reconocido';
            gestureText.style.color = '#ef4444';
    }
}

function updateControlModeUI(modeName) {
    const currentModeElement = document.getElementById('current-mode');
    
    // Actualizar solo el icono y nombre del modo
    let displayText = '';
    if (modeName.includes('Teclado')) displayText = '⌨️ Teclado';
    else if (modeName.includes('Ratón')) displayText = '🖱️ Ratón';
    else if (modeName.includes('Gestos')) displayText = '✋ Gestos';
    
    currentModeElement.textContent = displayText;
}

// Bucle de animación principal
let lastTime = Date.now();

function animate() {
    requestAnimationFrame(animate);
    
    const currentTime = Date.now();
    const deltaTime = (currentTime - lastTime) / 1000; // en segundos
    lastTime = currentTime;
    
    // Actualizar simulación
    updateSimulation(deltaTime);
    
    // Actualizar controles híbridos
    if (hybridControls) {
        hybridControls.update();
    }
    
    // Renderizar
    renderer.render(scene, camera);
}

// ========================================
// GESTIÓN DE RECORDS Y VISUALIZACIÓN
// ========================================

// Cargar records desde localStorage
function loadRecordsFromStorage() {
    const savedBestTime = localStorage.getItem('securepath_best_time');
    const savedBestGen = localStorage.getItem('securepath_best_generation');
    
    if (savedBestTime) {
        bestTimeEver = parseFloat(savedBestTime);
        bestGenerationEver = parseInt(savedBestGen) || 0;
        console.log(`📂 Records cargados: ${bestTimeEver.toFixed(1)}s (gen ${bestGenerationEver})`);
    }
}

// Guardar records en localStorage
function saveRecordsToStorage() {
    localStorage.setItem('securepath_best_time', bestTimeEver.toString());
    localStorage.setItem('securepath_best_generation', bestGenerationEver.toString());
}

// Resetear historial de evolución
function resetEvolutionHistory() {
    if (confirm('¿Seguro que quieres borrar el historial de records?')) {
        evolutionData = [];
        bestTimeEver = Infinity;
        bestGenerationEver = 0;
        localStorage.removeItem('securepath_best_time');
        localStorage.removeItem('securepath_best_generation');
        updateStatsUI();
        drawEvolutionChart();
        console.log('🗑️ Historial borrado');
    }
}

// Dibujar gráfico de evolución
function drawEvolutionChart() {
    if (!evolutionCtx) return;
    
    const width = evolutionCanvas.width;
    const height = evolutionCanvas.height;
    const padding = 40;
    
    // Limpiar canvas
    evolutionCtx.fillStyle = 'rgba(0, 0, 0, 0.9)';
    evolutionCtx.fillRect(0, 0, width, height);
    
    if (evolutionData.length === 0) {
        // Mostrar mensaje si no hay datos
        evolutionCtx.fillStyle = '#9ca3af';
        evolutionCtx.font = '14px Arial';
        evolutionCtx.textAlign = 'center';
        evolutionCtx.fillText('Esperando datos de evolución...', width / 2, height / 2);
        return;
    }
    
    // Encontrar rangos
    let minFitness = Infinity;
    let maxFitness = -Infinity;
    
    evolutionData.forEach(data => {
        minFitness = Math.min(minFitness, data.worst);
        maxFitness = Math.max(maxFitness, data.best);
    });
    
    // Añadir margen al rango
    const range = maxFitness - minFitness || 1;
    minFitness -= range * 0.1;
    maxFitness += range * 0.1;
    
    // Función para escalar coordenadas
    const scaleX = (index) => padding + (index / (evolutionData.length - 1 || 1)) * (width - padding * 2);
    const scaleY = (fitness) => height - padding - ((fitness - minFitness) / (maxFitness - minFitness)) * (height - padding * 2);
    
    // Dibujar grid
    evolutionCtx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
    evolutionCtx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
        const y = padding + (i / 4) * (height - padding * 2);
        evolutionCtx.beginPath();
        evolutionCtx.moveTo(padding, y);
        evolutionCtx.lineTo(width - padding, y);
        evolutionCtx.stroke();
    }
    
    // Dibujar ejes
    evolutionCtx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
    evolutionCtx.lineWidth = 2;
    evolutionCtx.beginPath();
    evolutionCtx.moveTo(padding, padding);
    evolutionCtx.lineTo(padding, height - padding);
    evolutionCtx.lineTo(width - padding, height - padding);
    evolutionCtx.stroke();
    
    // Dibujar líneas
    const drawLine = (color, dataKey) => {
        evolutionCtx.strokeStyle = color;
        evolutionCtx.lineWidth = 2;
        evolutionCtx.beginPath();
        
        evolutionData.forEach((data, index) => {
            const x = scaleX(index);
            const y = scaleY(data[dataKey]);
            
            if (index === 0) {
                evolutionCtx.moveTo(x, y);
            } else {
                evolutionCtx.lineTo(x, y);
            }
        });
        
        evolutionCtx.stroke();
    };
    
    // Dibujar peor (rojo)
    drawLine('#ef4444', 'worst');
    
    // Dibujar promedio (amarillo)
    drawLine('#f59e0b', 'avg');
    
    // Dibujar mejor (verde)
    drawLine('#4ade80', 'best');
    
    // Etiquetas de ejes
    evolutionCtx.fillStyle = '#9ca3af';
    evolutionCtx.font = '11px Arial';
    evolutionCtx.textAlign = 'center';
    
    // Etiqueta eje X
    evolutionCtx.fillText('Generaciones', width / 2, height - 10);
    
    // Etiqueta eje Y (rotada)
    evolutionCtx.save();
    evolutionCtx.translate(12, height / 2);
    evolutionCtx.rotate(-Math.PI / 2);
    evolutionCtx.fillText('Fitness', 0, 0);
    evolutionCtx.restore();
    
    // Valores en ejes
    evolutionCtx.textAlign = 'right';
    for (let i = 0; i <= 4; i++) {
        const fitness = minFitness + (i / 4) * (maxFitness - minFitness);
        const y = scaleY(fitness);
        evolutionCtx.fillText(fitness.toFixed(1), padding - 8, y + 4);
    }
}

// ========================================
// GESTIÓN DE DATOS Y PERSISTENCIA
// ========================================

// Cargar presets en la UI
function loadPresetsUI() {
    const presets = dataManager.loadPresets();
    const select = document.getElementById('preset-list');
    
    select.innerHTML = '';
    
    const presetNames = Object.keys(presets);
    if (presetNames.length === 0) {
        select.innerHTML = '<option value="">No hay presets guardados</option>';
    } else {
        presetNames.forEach(name => {
            const option = document.createElement('option');
            option.value = name;
            option.textContent = name;
            select.appendChild(option);
        });
    }
    
    updateStorageInfo();
}

// Actualizar información de almacenamiento
function updateStorageInfo() {
    const storageSize = dataManager.getStorageSize();
    document.getElementById('storage-info').textContent = 
        `Almacenamiento: ${storageSize.kb} KB`;
}

// Exportar para debugging
window.debugInfo = () => {
    console.log('📊 Estado del sistema:', {
        scene,
        camera,
        building,
        people: people.length,
        stats,
        config,
        simulationRunning
    });
};
