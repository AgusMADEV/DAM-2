/**
 * Aplicación principal del Procesador de Imágenes Multinúcleo
 * Gestiona la interfaz web y la comunicación con el servidor WebSocket
 */

class AplicacionProcesadorImagenes {
    constructor() {
        this.ws = null;
        this.conectado = false;
        this.filtrosDisponibles = [];
        this.filtrosSeleccionados = new Set();
        this.procesando = false;
        
        // Worker para tareas en segundo plano
        this.worker = null;
        
        // Estadísticas
        this.estadisticas = {
            inicio: null,
            imagenesProcesadas: 0,
            imagenesTotal: 0
        };
        
        this.inicializar();
    }
    
    inicializar() {
        console.log('🚀 Inicializando aplicación...');
        this.conectarWebSocket();
        this.inicializarEventos();
        this.inicializarWorker();
    }
    
    // ==================== WEBSOCKET ====================
    
    conectarWebSocket() {
        this.log('Conectando al servidor WebSocket...', 'info');
        
        try {
            this.ws = new WebSocket('ws://localhost:8765');
            
            this.ws.onopen = () => this.alConectar();
            this.ws.onmessage = (event) => this.alRecibirMensaje(event);
            this.ws.onerror = (error) => this.alError(error);
            this.ws.onclose = () => this.alDesconectar();
            
        } catch (error) {
            this.log(`Error al conectar: ${error.message}`, 'error');
            this.actualizarEstadoConexion(false);
        }
    }
    
    alConectar() {
        this.conectado = true;
        this.actualizarEstadoConexion(true);
        this.log('✅ Conectado al servidor exitosamente', 'success');
        
        // Solicitar información inicial
        this.solicitarFiltros();
        this.solicitarImagenes();
    }
    
    alRecibirMensaje(event) {
        try {
            const mensaje = JSON.parse(event.data);
            this.procesarMensaje(mensaje);
        } catch (error) {
            this.log(`Error al procesar mensaje: ${error.message}`, 'error');
        }
    }
    
    alError(error) {
        this.log(`Error de WebSocket: ${error.message}`, 'error');
        this.actualizarEstadoConexion(false);
    }
    
    alDesconectar() {
        this.conectado = false;
        this.actualizarEstadoConexion(false);
        this.log('❌ Desconectado del servidor', 'error');
        
        // Intentar reconectar después de 3 segundos
        setTimeout(() => {
            if (!this.conectado) {
                this.log('Intentando reconectar...', 'info');
                this.conectarWebSocket();
            }
        }, 3000);
    }
    
    enviarComando(comando) {
        if (!this.conectado || !this.ws) {
            this.log('No hay conexión con el servidor', 'error');
            return;
        }
        
        try {
            this.ws.send(JSON.stringify(comando));
        } catch (error) {
            this.log(`Error al enviar comando: ${error.message}`, 'error');
        }
    }
    
    // ==================== PROCESAMIENTO DE MENSAJES ====================
    
    procesarMensaje(mensaje) {
        const tipo = mensaje.tipo;
        
        switch (tipo) {
            case 'conexion':
                this.log(mensaje.mensaje, 'success');
                break;
                
            case 'filtros':
                this.actualizarFiltros(mensaje.datos);
                break;
                
            case 'imagenes':
                this.actualizarImagenes(mensaje.datos);
                break;
                
            case 'inicio_procesamiento':
                this.iniciarProcesamientoUI(mensaje.datos);
                break;
                
            case 'progreso':
                this.actualizarProgreso(mensaje.datos);
                break;
                
            case 'finalizado':
                this.finalizarProcesamiento(mensaje.datos);
                break;
                
            case 'error':
                this.log(`❌ Error: ${mensaje.mensaje}`, 'error');
                this.procesando = false;
                this.actualizarBotones();
                break;
                
            case 'aceptado':
                this.log(mensaje.mensaje, 'success');
                break;
                
            default:
                console.log('Mensaje desconocido:', mensaje);
        }
    }
    
    // ==================== UI - FILTROS ====================
    
    solicitarFiltros() {
        this.enviarComando({ tipo: 'listar_filtros' });
    }
    
    actualizarFiltros(filtros) {
        this.filtrosDisponibles = filtros;
        const container = document.getElementById('filtros-container');
        container.innerHTML = '';
        
        const descripciones = {
            'invertir': '🔄 Invertir Colores',
            'grises': '⬜ Escala de Grises',
            'blur': '🌫️ Desenfocar (Blur)',
            'nitidez': '✨ Aumentar Nitidez',
            'brillo': '💡 Ajustar Brillo',
            'contraste': '🎚️ Ajustar Contraste',
            'sepia': '📜 Efecto Sepia',
            'bordes': '🔲 Detectar Bordes',
            'relieve': '🗻 Efecto Relieve',
            'posterizar': '🎨 Posterizar',
            'redimensionar': '📏 Redimensionar',
            'marca_agua': '©️ Marca de Agua'
        };
        
        filtros.forEach(filtro => {
            const div = document.createElement('div');
            div.className = 'filtro-item';
            div.dataset.filtro = filtro;
            
            div.innerHTML = `
                <input type="checkbox" class="filtro-checkbox" id="filtro-${filtro}">
                <label for="filtro-${filtro}">${descripciones[filtro] || filtro}</label>
            `;
            
            div.addEventListener('click', (e) => {
                if (e.target.tagName !== 'INPUT') {
                    const checkbox = div.querySelector('input');
                    checkbox.checked = !checkbox.checked;
                }
                this.toggleFiltro(filtro, div.querySelector('input').checked);
                div.classList.toggle('seleccionado');
            });
            
            container.appendChild(div);
        });
        
        this.log(`📋 Cargados ${filtros.length} filtros disponibles`, 'info');
    }
    
    toggleFiltro(filtro, seleccionado) {
        if (seleccionado) {
            this.filtrosSeleccionados.add(filtro);
        } else {
            this.filtrosSeleccionados.delete(filtro);
        }
        this.actualizarBotones();
    }
    
    // ==================== UI - IMÁGENES ====================
    
    solicitarImagenes() {
        this.enviarComando({ tipo: 'listar_imagenes' });
    }
    
    actualizarImagenes(datos) {
        const container = document.getElementById('lista-imagenes');
        
        if (datos.cantidad === 0) {
            container.innerHTML = '<p class="mensaje-placeholder">⚠️ No hay imágenes en el directorio input_images</p>';
            this.log('No se encontraron imágenes para procesar', 'warning');
            return;
        }
        
        container.innerHTML = '';
        datos.imagenes.forEach(imagen => {
            const div = document.createElement('div');
            div.className = 'imagen-item';
            div.innerHTML = `
                <span>📷</span>
                <span>${imagen}</span>
            `;
            container.appendChild(div);
        });
        
        this.log(`✅ Encontradas ${datos.cantidad} imágenes`, 'success');
        this.actualizarBotones();
    }
    
    // ==================== UI - PROCESAMIENTO ====================
    
    iniciarProcesamiento() {
        if (this.filtrosSeleccionados.size === 0) {
            this.log('⚠️ Selecciona al menos un filtro', 'warning');
            return;
        }
        
        const modo = document.getElementById('modo-procesamiento').value;
        const filtros = Array.from(this.filtrosSeleccionados);
        
        this.enviarComando({
            tipo: 'procesar',
            filtros: filtros,
            modo: modo
        });
        
        this.procesando = true;
        this.actualizarBotones();
    }
    
    iniciarProcesamientoUI(datos) {
        this.estadisticas.inicio = Date.now();
        this.estadisticas.imagenesProcesadas = 0;
        this.estadisticas.imagenesTotal = datos.imagenes;
        
        const panel = document.getElementById('progreso-general');
        panel.classList.remove('oculto');
        
        document.getElementById('imagenes-total').textContent = datos.imagenes;
        document.getElementById('imagenes-procesadas').textContent = '0';
        document.getElementById('progreso-porcentaje').textContent = '0%';
        document.getElementById('barra-progreso-fill').style.width = '0%';
        
        this.log(`🚀 Iniciando procesamiento: ${datos.imagenes} imágenes, ${datos.filtros.length} filtros, modo: ${datos.modo}`, 'info');
        
        // Ocultar resultados anteriores
        document.getElementById('panel-resultados').classList.add('oculto');
    }
    
    actualizarProgreso(info) {
        // Actualizar estadísticas
        document.getElementById('imagenes-procesadas').textContent = info.procesadas;
        document.getElementById('progreso-porcentaje').textContent = `${info.porcentaje}%`;
        document.getElementById('barra-progreso-fill').style.width = `${info.porcentaje}%`;
        document.getElementById('tiempo-transcurrido').textContent = `${info.tiempo_transcurrido}s`;
        
        // Calcular velocidad
        if (info.tiempo_transcurrido > 0) {
            const velocidad = (info.procesadas / info.tiempo_transcurrido).toFixed(2);
            document.getElementById('velocidad').textContent = velocidad;
        }
        
        // Actualizar texto de progreso
        const estados = {
            'procesando': '⏳',
            'completado': '✅',
            'error': '❌'
        };
        
        const emoji = estados[info.estado] || '📁';
        document.getElementById('progreso-texto').textContent = `${emoji} ${info.imagen}`;
        
        // Log del progreso
        const clase = info.estado === 'completado' ? 'success' : (info.estado === 'error' ? 'error' : 'info');
        this.log(`[${info.porcentaje.toFixed(1)}%] ${info.imagen} - ${info.mensaje}`, clase);
        
        // Enviar datos al worker para análisis
        if (this.worker) {
            this.worker.postMessage({
                tipo: 'actualizar_stats',
                datos: info
            });
        }
    }
    
    finalizarProcesamiento(datos) {
        this.procesando = false;
        this.actualizarBotones();
        
        this.log('🎉 Procesamiento completado exitosamente', 'success');
        
        // Mostrar resultados
        this.mostrarResultados(datos.resultados);
        
        // Actualizar barra a 100%
        document.getElementById('progreso-porcentaje').textContent = '100%';
        document.getElementById('barra-progreso-fill').style.width = '100%';
        document.getElementById('progreso-texto').textContent = '✅ Procesamiento completado';
    }
    
    mostrarResultados(resultados) {
        const panel = document.getElementById('panel-resultados');
        const content = document.getElementById('resultados-content');
        
        panel.classList.remove('oculto');
        content.innerHTML = '';
        
        resultados.forEach(resultado => {
            const div = document.createElement('div');
            div.className = 'resultado-item fade-in';
            
            const tiempoPorImagen = (resultado.tiempo_total / resultado.exitosas).toFixed(2);
            
            div.innerHTML = `
                <h3>🎨 ${resultado.filtro.toUpperCase()}</h3>
                <div class="resultado-stats">
                    <div class="stat-row">
                        <span>⏱️ Tiempo Total:</span>
                        <strong>${resultado.tiempo_total.toFixed(2)}s</strong>
                    </div>
                    <div class="stat-row">
                        <span>✅ Exitosas:</span>
                        <strong>${resultado.exitosas}</strong>
                    </div>
                    <div class="stat-row">
                        <span>❌ Fallidas:</span>
                        <strong>${resultado.fallidas}</strong>
                    </div>
                    <div class="stat-row">
                        <span>⚡ Tiempo/Imagen:</span>
                        <strong>${tiempoPorImagen}s</strong>
                    </div>
                    <div class="stat-row">
                        <span>🖥️ Núcleos Usados:</span>
                        <strong>${resultado.nucleos_usados}</strong>
                    </div>
                </div>
            `;
            
            content.appendChild(div);
        });
        
        // Scroll suave al panel de resultados
        panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    
    // ==================== UI - CONTROLES ====================
    
    actualizarEstadoConexion(conectado) {
        const elemento = document.getElementById('conexion-estado');
        elemento.textContent = conectado ? '● Conectado' : '● Desconectado';
        elemento.className = `estado ${conectado ? 'conectado' : 'desconectado'}`;
        
        this.actualizarBotones();
    }
    
    actualizarBotones() {
        const btnProcesar = document.getElementById('btn-procesar');
        const btnCancelar = document.getElementById('btn-cancelar');
        
        const hayImagenes = document.querySelectorAll('.imagen-item').length > 0;
        const hayFiltros = this.filtrosSeleccionados.size > 0;
        
        btnProcesar.disabled = !this.conectado || this.procesando || !hayImagenes || !hayFiltros;
        btnCancelar.disabled = !this.procesando;
    }
    
    // ==================== EVENTOS ====================
    
    inicializarEventos() {
        // Botón procesar
        document.getElementById('btn-procesar').addEventListener('click', () => {
            this.iniciarProcesamiento();
        });
        
        // Botón cancelar
        document.getElementById('btn-cancelar').addEventListener('click', () => {
            this.enviarComando({ tipo: 'cancelar' });
        });
        
        // Actualizar imágenes
        document.getElementById('btn-actualizar-imagenes').addEventListener('click', () => {
            this.solicitarImagenes();
        });
        
        // Seleccionar/deseleccionar todos los filtros
        document.getElementById('btn-seleccionar-todos').addEventListener('click', () => {
            document.querySelectorAll('.filtro-item input').forEach(checkbox => {
                checkbox.checked = true;
                const filtro = checkbox.closest('.filtro-item').dataset.filtro;
                this.filtrosSeleccionados.add(filtro);
                checkbox.closest('.filtro-item').classList.add('seleccionado');
            });
            this.actualizarBotones();
        });
        
        document.getElementById('btn-deseleccionar-todos').addEventListener('click', () => {
            document.querySelectorAll('.filtro-item input').forEach(checkbox => {
                checkbox.checked = false;
                checkbox.closest('.filtro-item').classList.remove('seleccionado');
            });
            this.filtrosSeleccionados.clear();
            this.actualizarBotones();
        });
        
        // Limpiar log
        document.getElementById('btn-limpiar-log').addEventListener('click', () => {
            document.getElementById('log-content').innerHTML = '';
        });
    }
    
    // ==================== WEB WORKER ====================
    
    inicializarWorker() {
        try {
            this.worker = new Worker('workers/monitor.js');
            
            this.worker.onmessage = (e) => {
                if (e.data.tipo === 'stats') {
                    // Actualizar información de núcleos si está disponible
                    if (e.data.nucleos) {
                        document.getElementById('nucleos-info').textContent = `🖥️ Núcleos: ${e.data.nucleos}`;
                    }
                }
            };
            
            this.log('✅ Worker inicializado para monitorización', 'info');
        } catch (error) {
            this.log('⚠️ No se pudo inicializar el worker', 'warning');
        }
    }
    
    // ==================== UTILIDADES ====================
    
    log(mensaje, tipo = 'info') {
        const logContent = document.getElementById('log-content');
        const logItem = document.createElement('p');
        logItem.className = `log-item ${tipo}`;
        
        const timestamp = new Date().toLocaleTimeString();
        logItem.textContent = `[${timestamp}] ${mensaje}`;
        
        logContent.appendChild(logItem);
        logContent.scrollTop = logContent.scrollHeight;
        
        // Limitar número de logs
        if (logContent.children.length > 100) {
            logContent.removeChild(logContent.firstChild);
        }
    }
}

// Inicializar aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.app = new AplicacionProcesadorImagenes();
});
