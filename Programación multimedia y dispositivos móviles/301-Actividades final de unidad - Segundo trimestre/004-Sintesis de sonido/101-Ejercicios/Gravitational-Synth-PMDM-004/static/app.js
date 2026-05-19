// ==================== AUDIO SETUP ====================
let audioContext = null;
let masterGainNode = null;
let reverbNode = null;
let audioEnabled = false;

// Secuenciador state
const sequencer = {
    grid: Array(7).fill(null).map(() => Array(16).fill(false)),
    notes: ['C5', 'B4', 'A4', 'G4', 'F4', 'E4', 'D4'],
    isPlaying: false,
    currentStep: 0,
    bpm: 120,
    intervalId: null
};

// Notas musicales: C4 a C6 (2 octavas)
const notes = {
    'C4': 261.63, 'C#4': 277.18, 'D4': 293.66, 'D#4': 311.13,
    'E4': 329.63, 'F4': 349.23, 'F#4': 369.99, 'G4': 392.00,
    'G#4': 415.30, 'A4': 440.00, 'A#4': 466.16, 'B4': 493.88,
    'C5': 523.25, 'C#5': 554.37, 'D5': 587.33, 'D#5': 622.25,
    'E5': 659.25, 'F5': 698.46, 'F#5': 739.99, 'G5': 783.99,
    'G#5': 830.61, 'A5': 880.00, 'A#5': 932.33, 'B5': 987.77,
    'C6': 1046.50
};

const noteColors = {
    'C4': '#FF6B6B', 'C#4': '#FF8E8E', 'D4': '#FFA07A', 'D#4': '#FFB347',
    'E4': '#FFD700', 'F4': '#F0E68C', 'F#4': '#BDB76B', 'G4': '#90EE90',
    'G#4': '#7FFFD4', 'A4': '#87CEEB', 'A#4': '#6495ED', 'B4': '#4682B4',
    'C5': '#9370DB', 'C#5': '#BA55D3', 'D5': '#DA70D6', 'D#5': '#EE82EE',
    'E5': '#FF69B4', 'F5': '#FF1493', 'F#5': '#C71585', 'G5': '#DB7093',
    'G#5': '#FFB6C1', 'A5': '#FFC0CB', 'A#5': '#FFE4E1', 'B5': '#FFF0F5',
    'C6': '#FFFFFF'
};

function initAudio() {
    if (audioContext) return;
    
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    
    // Master gain
    masterGainNode = audioContext.createGain();
    masterGainNode.gain.value = 0.7;
    
    // Simple reverb using convolver
    reverbNode = audioContext.createGain();
    reverbNode.gain.value = 0.3;
    
    reverbNode.connect(audioContext.destination);
    masterGainNode.connect(reverbNode);
    masterGainNode.connect(audioContext.destination);
    
    audioEnabled = true;
    document.getElementById('startAudio').classList.add('active');
    document.getElementById('startAudio').textContent = '🔊 Audio Activo';
}

function playNote(frequency, duration, waveType) {
    if (!audioEnabled || !audioContext) return;
    
    const now = audioContext.currentTime;
    
    // Oscillator
    const osc = audioContext.createOscillator();
    osc.type = waveType;
    osc.frequency.setValueAtTime(frequency, now);
    
    // Envelope
    const envelope = audioContext.createGain();
    envelope.gain.setValueAtTime(0, now);
    envelope.gain.linearRampToValueAtTime(0.3, now + 0.01); // Attack
    envelope.gain.exponentialRampToValueAtTime(0.01, now + duration / 1000); // Decay
    
    osc.connect(envelope);
    envelope.connect(masterGainNode);
    
    osc.start(now);
    osc.stop(now + duration / 1000);
    
    stats.notesPlayed++;
}

// Wrapper function for sequencer compatibility
function playSound(frequency, note, velocity, duration) {
    if (!audioEnabled || !audioContext) {
        initAudio();
        if (!audioContext) return;
    }
    
    const durationMs = duration * 1000; // Convert to milliseconds
    playNote(frequency, durationMs, settings.waveType);
}

// ==================== CANVAS SETUP ====================
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

function resizeCanvas() {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

// ==================== PARTICLE SYSTEM ====================
class Particle {
    constructor(x, y, vx, vy, radius, note, mass) {
        this.x = x;
        this.y = y;
        this.vx = vx;
        this.vy = vy;
        this.radius = radius;
        this.note = note;
        this.frequency = notes[note];
        this.color = noteColors[note];
        this.mass = mass;
        this.trail = [];
        this.maxTrail = 20;
    }

    update() {
        // Apply gravity
        if (settings.gravityEnabled) {
            this.vy += settings.gravity;
        }

        // Update position
        this.x += this.vx;
        this.y += this.vy;

        // Trail effect
        this.trail.push({ x: this.x, y: this.y });
        if (this.trail.length > this.maxTrail) {
            this.trail.shift();
        }

        // Bounce off walls
        if (this.x - this.radius < 0 || this.x + this.radius > canvas.width) {
            this.vx *= -0.95;
            this.x = Math.max(this.radius, Math.min(canvas.width - this.radius, this.x));
            this.playSound();
            stats.collisionCount++;
        }

        if (this.y - this.radius < 0 || this.y + this.radius > canvas.height) {
            this.vy *= -0.95;
            this.y = Math.max(this.radius, Math.min(canvas.height - this.radius, this.y));
            this.playSound();
            stats.collisionCount++;
        }

        // Air resistance
        this.vx *= 0.999;
        this.vy *= 0.999;
    }

    draw() {
        // Draw trail
        ctx.strokeStyle = this.color;
        ctx.lineWidth = 2;
        ctx.globalAlpha = 0.3;
        ctx.beginPath();
        for (let i = 0; i < this.trail.length - 1; i++) {
            const alpha = i / this.trail.length;
            ctx.globalAlpha = alpha * 0.3;
            ctx.moveTo(this.trail[i].x, this.trail[i].y);
            ctx.lineTo(this.trail[i + 1].x, this.trail[i + 1].y);
        }
        ctx.stroke();

        // Draw particle
        ctx.globalAlpha = 1;
        const gradient = ctx.createRadialGradient(
            this.x - this.radius / 3,
            this.y - this.radius / 3,
            0,
            this.x,
            this.y,
            this.radius
        );
        gradient.addColorStop(0, 'white');
        gradient.addColorStop(0.4, this.color);
        gradient.addColorStop(1, this.color + '80');
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fill();

        // Glow effect
        ctx.shadowBlur = 20;
        ctx.shadowColor = this.color;
        ctx.fill();
        ctx.shadowBlur = 0;
    }

    playSound() {
        playNote(this.frequency, settings.noteDuration, settings.waveType);
    }

    checkCollision(other) {
        const dx = this.x - other.x;
        const dy = this.y - other.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        return distance < this.radius + other.radius;
    }

    resolveCollision(other) {
        const dx = other.x - this.x;
        const dy = other.y - this.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance === 0) return;

        // Normal vector
        const nx = dx / distance;
        const ny = dy / distance;

        // Relative velocity
        const dvx = other.vx - this.vx;
        const dvy = other.vy - this.vy;

        // Velocity along normal
        const dvn = dvx * nx + dvy * ny;

        // Do not resolve if velocities are separating
        if (dvn > 0) return;

        // Collision impulse
        const restitution = 0.9;
        const impulse = (2 * dvn) / (this.mass + other.mass);

        // Apply impulse
        this.vx += impulse * other.mass * nx * restitution;
        this.vy += impulse * other.mass * ny * restitution;
        other.vx -= impulse * this.mass * nx * restitution;
        other.vy -= impulse * this.mass * ny * restitution;

        // Separate particles
        const overlap = this.radius + other.radius - distance;
        const separationX = (overlap / 2) * nx;
        const separationY = (overlap / 2) * ny;
        this.x -= separationX;
        this.y -= separationY;
        other.x += separationX;
        other.y += separationY;

        // Play sounds
        this.playSound();
        other.playSound();
        stats.collisionCount++;
    }
}

// ==================== SEQUENCER VISUAL EFFECTS ====================
class SequencerVisual {
    constructor(x, y, note, color) {
        this.x = x;
        this.y = y;
        this.note = note;
        this.color = color;
        this.radius = 10;
        this.maxRadius = 120;
        this.alpha = 1.0;
        this.active = true;
    }

    update() {
        this.radius += 3;
        this.alpha = 1 - (this.radius / this.maxRadius);
        if (this.radius >= this.maxRadius) {
            this.active = false;
        }
    }

    draw(ctx) {
        ctx.save();
        ctx.globalAlpha = this.alpha;
        
        // Outer ring
        ctx.strokeStyle = this.color;
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.stroke();
        
        // Inner glow
        const gradient = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.radius);
        gradient.addColorStop(0, this.color + '80');
        gradient.addColorStop(1, this.color + '00');
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.restore();
    }
}

// ==================== GAME STATE ====================
const particles = [];
const sequencerVisuals = [];
const stats = {
    collisionCount: 0,
    notesPlayed: 0
};

const settings = {
    creationMode: 'single',
    selectedNote: 'A4',
    waveType: 'sine',
    particleRadius: 15,
    initialVelocity: 5,
    particleMass: 1.0,
    gravity: 0.2,
    gravityEnabled: true,
    masterVolume: 0.7,
    noteDuration: 200,
    reverbAmount: 0.3
};

// ==================== INPUT HANDLERS ====================
canvas.addEventListener('click', (e) => {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    switch (settings.creationMode) {
        case 'single':
            createParticle(x, y);
            break;
        case 'burst':
            createBurst(x, y, 5);
            break;
        case 'fountain':
            createFountain(x, y);
            break;
        case 'orbital':
            createOrbitalSystem(x, y);
            break;
    }
});

function createParticle(x, y, vx = null, vy = null) {
    if (vx === null) {
        const angle = Math.random() * Math.PI * 2;
        vx = Math.cos(angle) * settings.initialVelocity;
        vy = Math.sin(angle) * settings.initialVelocity;
    }

    const particle = new Particle(
        x, y, vx, vy,
        settings.particleRadius,
        settings.selectedNote,
        settings.particleMass
    );
    particles.push(particle);
}

function createBurst(x, y, count) {
    for (let i = 0; i < count; i++) {
        const angle = (Math.PI * 2 / count) * i;
        const vx = Math.cos(angle) * settings.initialVelocity;
        const vy = Math.sin(angle) * settings.initialVelocity;
        
        const noteKeys = Object.keys(notes);
        const randomNote = noteKeys[Math.floor(Math.random() * noteKeys.length)];
        settings.selectedNote = randomNote;
        
        createParticle(x, y, vx, vy);
    }
}

function createFountain(x, y) {
    const interval = setInterval(() => {
        if (particles.length > 100) {
            clearInterval(interval);
            return;
        }
        const vx = (Math.random() - 0.5) * settings.initialVelocity;
        const vy = -Math.random() * settings.initialVelocity * 2;
        createParticle(x, y, vx, vy);
    }, 100);
    
    setTimeout(() => clearInterval(interval), 2000);
}

function createOrbitalSystem(x, y) {
    const center = new Particle(x, y, 0, 0, 25, 'C5', 10);
    center.color = '#FFD700';
    particles.push(center);

    const orbits = 3;
    const particlesPerOrbit = 4;

    for (let orbit = 1; orbit <= orbits; orbit++) {
        const radius = orbit * 60;
        for (let i = 0; i < particlesPerOrbit; i++) {
            const angle = (Math.PI * 2 / particlesPerOrbit) * i;
            const px = x + Math.cos(angle) * radius;
            const py = y + Math.sin(angle) * radius;
            
            const speed = 2 - orbit * 0.3;
            const vx = -Math.sin(angle) * speed;
            const vy = Math.cos(angle) * speed;
            
            const noteKeys = Object.keys(notes);
            const randomNote = noteKeys[orbit * 5 + i];
            settings.selectedNote = randomNote;
            
            createParticle(px, py, vx, vy);
        }
    }
}

// ==================== UI CONTROLS ====================
document.getElementById('startAudio').addEventListener('click', initAudio);

document.getElementById('clearAll').addEventListener('click', () => {
    particles.length = 0;
    stats.collisionCount = 0;
    stats.notesPlayed = 0;
});

document.getElementById('toggleGravity').addEventListener('click', (e) => {
    settings.gravityEnabled = !settings.gravityEnabled;
    e.target.textContent = settings.gravityEnabled ? '🌍 Gravedad: ON' : '🌍 Gravedad: OFF';
    e.target.classList.toggle('active', settings.gravityEnabled);
});

// Create note selector buttons
const noteSelector = document.getElementById('noteSelector');
const notesToShow = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5'];
notesToShow.forEach(note => {
    const btn = document.createElement('button');
    btn.className = 'note-btn';
    btn.textContent = note;
    if (note === 'A4') btn.classList.add('selected');
    btn.addEventListener('click', () => {
        document.querySelectorAll('.note-btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        settings.selectedNote = note;
    });
    noteSelector.appendChild(btn);
});

// Range inputs with value display
const ranges = [
    { id: 'particleRadius', prop: 'particleRadius', display: 'radiusValue', suffix: '' },
    { id: 'initialVelocity', prop: 'initialVelocity', display: 'velocityValue', suffix: '' },
    { id: 'particleMass', prop: 'particleMass', display: 'massValue', suffix: '' },
    { id: 'gravityStrength', prop: 'gravity', display: 'gravityValue', suffix: '' },
    { id: 'masterVolume', prop: 'masterVolume', display: 'volumeValue', suffix: '%' },
    { id: 'noteDuration', prop: 'noteDuration', display: 'durationValue', suffix: 'ms' },
    { id: 'reverbAmount', prop: 'reverbAmount', display: 'reverbValue', suffix: '%' }
];

ranges.forEach(range => {
    const input = document.getElementById(range.id);
    const display = document.getElementById(range.display);
    
    input.addEventListener('input', (e) => {
        const value = parseFloat(e.target.value);
        settings[range.prop] = value;
        display.textContent = value + range.suffix;
        
        // Update audio settings
        if (range.id === 'masterVolume' && masterGainNode) {
            masterGainNode.gain.value = value / 100;
        }
        if (range.id === 'reverbAmount' && reverbNode) {
            reverbNode.gain.value = value / 100;
        }
    });
});

// Select inputs
document.getElementById('creationMode').addEventListener('change', (e) => {
    settings.creationMode = e.target.value;
});

document.getElementById('waveType').addEventListener('change', (e) => {
    settings.waveType = e.target.value;
});

// ==================== SEQUENCER ====================
function buildSequencerGrid() {
    const grid = document.getElementById('sequencerGrid');
    grid.innerHTML = '';
    
    // Header row (step numbers)
    grid.appendChild(document.createElement('div')); // Empty corner
    for (let col = 0; col < 16; col++) {
        const header = document.createElement('div');
        header.className = 'seq-label';
        header.textContent = col + 1;
        grid.appendChild(header);
    }
    
    // Rows with note labels and cells
    for (let row = 0; row < 7; row++) {
        // Note label
        const label = document.createElement('div');
        label.className = 'seq-label';
        label.textContent = sequencer.notes[row];
        grid.appendChild(label);
        
        // Cells
        for (let col = 0; col < 16; col++) {
            const cell = document.createElement('div');
            cell.className = 'seq-cell';
            cell.dataset.row = row;
            cell.dataset.col = col;
            
            cell.addEventListener('click', () => {
                sequencer.grid[row][col] = !sequencer.grid[row][col];
                cell.classList.toggle('active', sequencer.grid[row][col]);
            });
            
            grid.appendChild(cell);
        }
    }
}

function playSequencerStep() {
    const cells = document.querySelectorAll('.seq-cell');
    
    // Clear previous playing state
    cells.forEach(cell => cell.classList.remove('playing'));
    
    // Highlight current column and play active notes
    let notesThisStep = 0;
    for (let row = 0; row < 7; row++) {
        // querySelectorAll('.seq-cell') returns only cells (7 rows × 16 cols = 112 cells)
        const cellIndex = row * 16 + sequencer.currentStep;
        const cell = cells[cellIndex];
        
        if (cell) {
            cell.classList.add('playing');
            
            if (sequencer.grid[row][sequencer.currentStep]) {
                const note = sequencer.notes[row];
                const frequency = notes[note];
                playSound(frequency, note, 0.4, settings.noteDuration / 1000);
                
                // Create visual effect in canvas
                const spacing = canvas.height / 8;
                const y = spacing * (row + 1);
                const x = canvas.width * 0.25 + (notesThisStep * 80);
                const color = noteColors[note] || '#FFFFFF';
                sequencerVisuals.push(new SequencerVisual(x, y, note, color));
                notesThisStep++;
            }
        }
    }
    
    sequencer.currentStep = (sequencer.currentStep + 1) % 16;
}

function startSequencer() {
    if (sequencer.isPlaying) return;
    
    if (!audioEnabled) {
        initAudio();
    }
    
    sequencer.isPlaying = true;
    sequencer.currentStep = 0;
    
    const interval = (60000 / sequencer.bpm) / 4; // 16th notes
    sequencer.intervalId = setInterval(playSequencerStep, interval);
    
    document.getElementById('btnPlaySeq').classList.add('active');
    document.getElementById('btnStopSeq').classList.remove('active');
}

function stopSequencer() {
    if (!sequencer.isPlaying) return;
    
    sequencer.isPlaying = false;
    clearInterval(sequencer.intervalId);
    sequencer.intervalId = null;
    
    // Clear playing highlights
    document.querySelectorAll('.seq-cell').forEach(cell => {
        cell.classList.remove('playing');
    });
    
    document.getElementById('btnPlaySeq').classList.remove('active');
    document.getElementById('btnStopSeq').classList.add('active');
}

function clearSequencer() {
    stopSequencer();
    sequencer.grid = Array(7).fill(null).map(() => Array(16).fill(false));
    document.querySelectorAll('.seq-cell').forEach(cell => {
        cell.classList.remove('active');
    });
}

// Sequencer controls
document.getElementById('btnPlaySeq').addEventListener('click', startSequencer);
document.getElementById('btnStopSeq').addEventListener('click', stopSequencer);
document.getElementById('btnClearSeq').addEventListener('click', clearSequencer);

document.getElementById('bpmSlider').addEventListener('input', (e) => {
    sequencer.bpm = parseInt(e.target.value);
    document.getElementById('bpmValue').textContent = sequencer.bpm;
    
    // Restart sequencer with new BPM if playing
    if (sequencer.isPlaying) {
        stopSequencer();
        startSequencer();
    }
});

// Initialize sequencer grid
buildSequencerGrid();

// ==================== COMPOSITION MANAGEMENT ====================
const API_BASE = 'http://127.0.0.1:5000/api';
let selectedCompositionId = null;

async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            headers: { 'Content-Type': 'application/json' },
            ...options
        });
        const data = await response.json();
        if (!response.ok || !data.ok) {
            throw new Error(data.error || 'Error en la API');
        }
        return data;
    } catch (error) {
        console.error('API Error:', error);
        alert('Error: ' + error.message);
        throw error;
    }
}

async function saveComposition() {
    const title = document.getElementById('saveTitle').value.trim();
    if (!title) {
        alert('Por favor, ingresa un título para la composición');
        return;
    }

    const composition = {
        title: title,
        description: document.getElementById('saveDescription').value.trim(),
        bpm: sequencer.bpm,
        waveType: settings.waveType,
        sequencerGrid: sequencer.grid,
        settings: {
            particleRadius: settings.particleRadius,
            initialVelocity: settings.initialVelocity,
            particleMass: settings.particleMass,
            gravity: settings.gravity,
            gravityEnabled: settings.gravityEnabled,
            masterVolume: settings.masterVolume,
            noteDuration: settings.noteDuration,
            reverbAmount: settings.reverbAmount
        }
    };

    try {
        const result = await apiCall('/compositions', {
            method: 'POST',
            body: JSON.stringify(composition)
        });
        
        alert(`✅ ${result.message}`);
        document.getElementById('saveTitle').value = '';
        document.getElementById('saveDescription').value = '';
        await loadCompositions();
    } catch (error) {
        console.error('Error guardando:', error);
    }
}

async function loadCompositions() {
    const listContainer = document.getElementById('compositionList');
    
    try {
        const result = await apiCall('/compositions');
        const compositions = result.compositions;

        if (!compositions || compositions.length === 0) {
            listContainer.innerHTML = '<div class="compositions-empty">No hay composiciones guardadas</div>';
            return;
        }

        listContainer.innerHTML = compositions.map(comp => `
            <div class="composition-item" data-id="${comp.id}">
                <div class="composition-title">${comp.title}</div>
                <div class="composition-meta">
                    ${comp.bpm} BPM · ${comp.wave_type} · ${comp.author_name || 'Anónimo'}
                </div>
                ${comp.description ? `<div class="composition-meta" style="margin-top: 4px">${comp.description}</div>` : ''}
            </div>
        `).join('');

        // Click handlers
        document.querySelectorAll('.composition-item').forEach(item => {
            item.addEventListener('click', () => loadComposition(parseInt(item.dataset.id)));
        });
    } catch (error) {
        listContainer.innerHTML = '<div class="compositions-empty">⚠️ Error cargando composiciones.<br>Asegúrate de que el servidor Flask esté corriendo.</div>';
    }
}

async function loadComposition(compId) {
    try {
        const result = await apiCall(`/compositions/${compId}`);
        const comp = result.composition;

        // Stop sequencer if playing
        if (sequencer.isPlaying) {
            stopSequencer();
        }

        // Load sequencer grid
        sequencer.grid = comp.sequencer_grid;
        sequencer.bpm = comp.bpm;
        document.getElementById('bpmValue').textContent = comp.bpm;
        document.getElementById('bpmSlider').value = comp.bpm;

        // Load wave type
        settings.waveType = comp.wave_type;
        document.getElementById('waveType').value = comp.wave_type;

        // Load settings
        const loadedSettings = comp.settings_json;
        Object.keys(loadedSettings).forEach(key => {
            if (settings.hasOwnProperty(key)) {
                settings[key] = loadedSettings[key];
            }
        });

        // Update UI controls
        ranges.forEach(range => {
            const input = document.getElementById(range.id);
            const display = document.getElementById(range.display);
            if (input && display) {
                input.value = settings[range.prop];
                display.textContent = settings[range.prop] + range.suffix;
            }
        });

        // Rebuild grid with loaded data
        buildSequencerGrid();
        const cells = document.querySelectorAll('.seq-cell');
        cells.forEach(cell => {
            const row = parseInt(cell.dataset.row);
            const col = parseInt(cell.dataset.col);
            if (sequencer.grid[row][col]) {
                cell.classList.add('active');
            }
        });

        // Highlight selected composition
        document.querySelectorAll('.composition-item').forEach(item => {
            item.classList.toggle('selected', parseInt(item.dataset.id) === compId);
        });

        selectedCompositionId = compId;
        alert(`✅ Composición "${comp.title}" cargada`);
    } catch (error) {
        console.error('Error cargando composición:', error);
    }
}

// Composition controls
document.getElementById('btnSaveComposition').addEventListener('click', saveComposition);
document.getElementById('btnRefreshList').addEventListener('click', loadCompositions);

// Load compositions on startup
loadCompositions();

// ==================== ANIMATION LOOP ====================

let lastTime = performance.now();
let frames = 0;
let fpsTime = 0;

function animate(currentTime) {
    const deltaTime = currentTime - lastTime;
    lastTime = currentTime;

    // FPS counter
    frames++;
    fpsTime += deltaTime;
    if (fpsTime >= 1000) {
        document.getElementById('fps').textContent = frames;
        frames = 0;
        fpsTime = 0;
    }

    // Clear canvas with fade effect
    ctx.fillStyle = 'rgba(102, 126, 234, 0.1)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw sequencer progress bar
    if (sequencer.isPlaying) {
        const barHeight = 4;
        const barY = 10;
        const barWidth = canvas.width - 40;
        const barX = 20;
        
        // Background bar
        ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
        ctx.fillRect(barX, barY, barWidth, barHeight);
        
        // Progress
        const progress = sequencer.currentStep / 16;
        ctx.fillStyle = '#4CAF50';
        ctx.fillRect(barX, barY, barWidth * progress, barHeight);
        
        // Step markers
        for (let i = 0; i <= 16; i++) {
            const markerX = barX + (barWidth / 16) * i;
            ctx.fillStyle = i === sequencer.currentStep ? '#FFD700' : 'rgba(255, 255, 255, 0.4)';
            ctx.fillRect(markerX - 1, barY - 3, 2, barHeight + 6);
        }
        
        // BPM label
        ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
        ctx.font = '12px monospace';
        ctx.fillText(`${sequencer.bpm} BPM | Step ${sequencer.currentStep + 1}/16`, barX, barY - 8);
    }

    // Update and draw sequencer visuals
    for (let i = sequencerVisuals.length - 1; i >= 0; i--) {
        const visual = sequencerVisuals[i];
        visual.update();
        visual.draw(ctx);
        if (!visual.active) {
            sequencerVisuals.splice(i, 1);
        }
    }

    // Update and draw particles
    particles.forEach(particle => {
        particle.update();
        particle.draw();
    });

    // Check collisions
    for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
            if (particles[i].checkCollision(particles[j])) {
                particles[i].resolveCollision(particles[j]);
            }
        }
    }

    // Update stats
    document.getElementById('particleCount').textContent = particles.length;
    document.getElementById('collisionCount').textContent = stats.collisionCount;
    document.getElementById('notesPlayed').textContent = stats.notesPlayed;

    requestAnimationFrame(animate);
}

animate(performance.now());
