/**
 * AGENTE IA AUTÓNOMO - APLICACIÓN FRONTEND
 * Gestión de la interfaz y comunicación con la API
 */

const API_BASE = 'api/api.php';

// Estado global de la aplicación
const AppState = {
    misiones: [],
    misionActual: null,
    config: {},
    stats: {}
};

// ==========================================
// INICIALIZACIÓN
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Agente IA Autónomo iniciado');
    
    // Configurar navegación
    setupNavigation();
    
    // Cargar datos iniciales
    cargarDashboard();
    
    // Auto-refresh cada 30 segundos
    setInterval(() => {
        if (document.querySelector('#view-dashboard').classList.contains('active')) {
            cargarDashboard();
        }
    }, 30000);
});

// ==========================================
// NAVEGACIÓN
// ==========================================

function setupNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    
    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const view = btn.dataset.view;
            cambiarVista(view);
            
            // Actualizar botón activo
            navButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });
}

function cambiarVista(viewName) {
    // Ocultar todas las vistas
    document.querySelectorAll('.view').forEach(view => {
        view.classList.remove('active');
    });
    
    // Mostrar vista seleccionada
    const targetView = document.getElementById(`view-${viewName}`);
    if (targetView) {
        targetView.classList.add('active');
        
        // Cargar datos según la vista
        switch(viewName) {
            case 'dashboard':
                cargarDashboard();
                break;
            case 'misiones':
                cargarMisiones();
                break;
            case 'logs':
                cargarLogs();
                break;
            case 'config':
                cargarConfiguracion();
                break;
        }
    }
}

// ==========================================
// DASHBOARD
// ==========================================

async function cargarDashboard() {
    try {
        // Cargar estadísticas
        const stats = await apiRequest('stats');
        if (stats.exito) {
            actualizarEstadisticas(stats.estadisticas);
        }
        
        // Cargar misiones recientes
        const misiones = await apiRequest('listar_misiones');
        if (misiones.exito) {
            AppState.misiones = misiones.misiones;
            renderMisionesRecientes(misiones.misiones.slice(0, 5));
        }
    } catch (error) {
        console.error('Error cargando dashboard:', error);
        mostrarToast('Error al cargar el dashboard', 'error');
    }
}

function actualizarEstadisticas(stats) {
    const estadoMisiones = stats.misiones_por_estado || {};
    
    document.getElementById('stat-completadas').textContent = estadoMisiones.completada || 0;
    document.getElementById('stat-proceso').textContent = estadoMisiones.en_proceso || 0;
    document.getElementById('stat-pendientes').textContent = estadoMisiones.pendiente || 0;
    document.getElementById('stat-iteraciones').textContent = stats.total_iteraciones || 0;
}

function renderMisionesRecientes(misiones) {
    const container = document.getElementById('misiones-recientes');
    
    if (misiones.length === 0) {
        container.innerHTML = `
            <div style="text-align: center; padding: 40px; color: #64748b;">
                <i class="fas fa-inbox" style="font-size: 48px; margin-bottom: 16px;"></i>
                <p>No hay misiones todavía</p>
                <button class="btn btn-primary" onclick="mostrarCrearMision()" style="margin-top: 16px;">
                    Crear Primera Misión
                </button>
            </div>
        `;
        return;
    }
    
    container.innerHTML = misiones.map(mision => crearMisionHTML(mision)).join('');
}

// ==========================================
// MISIONES
// ==========================================

async function cargarMisiones() {
    try {
        const response = await apiRequest('listar_misiones');
        if (response.exito) {
            AppState.misiones = response.misiones;
            renderListaMisiones(response.misiones);
        }
    } catch (error) {
        console.error('Error cargando misiones:', error);
        mostrarToast('Error al cargar misiones', 'error');
    }
}

function renderListaMisiones(misiones) {
    const container = document.getElementById('lista-misiones');
    
    if (misiones.length === 0) {
        container.innerHTML = `
            <div style="text-align: center; padding: 60px; color: #64748b;">
                <i class="fas fa-robot" style="font-size: 64px; margin-bottom: 20px; opacity: 0.5;"></i>
                <h3 style="margin-bottom: 8px;">No hay misiones</h3>
                <p>Crea tu primera misión para que el agente empiece a trabajar</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = misiones.map(mision => crearMisionHTML(mision)).join('');
}

function crearMisionHTML(mision) {
    const estadoClass = `estado-${mision.estado}`;
    const estadoTexto = mision.estado.replace('_', ' ');
    const progreso = mision.progreso || 0;
    
    return `
        <div class="mision-item" onclick="verDetalleMision(${mision.id})">
            <div class="mision-header">
                <div>
                    <div class="mision-titulo">${escapeHtml(mision.titulo)}</div>
                    <div class="mision-descripcion">${escapeHtml(mision.descripcion || mision.objetivo_final).substring(0, 150)}...</div>
                </div>
                <span class="mision-estado ${estadoClass}">${estadoTexto}</span>
            </div>
            
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${progreso}%"></div>
            </div>
            
            <div class="mision-footer">
                <div class="mision-info">
                    <span><i class="fas fa-calendar"></i> ${formatearFecha(mision.fecha_creacion)}</span>
                    <span><i class="fas fa-sync"></i> ${mision.total_iteraciones || 0} iteraciones</span>
                    <span><i class="fas fa-flag"></i> ${mision.prioridad}</span>
                </div>
                <div class="mision-actions" onclick="event.stopPropagation()">
                    ${mision.estado === 'pendiente' ? 
                        `<button class="btn btn-success btn-sm" onclick="ejecutarMision(${mision.id})">
                            <i class="fas fa-play"></i> Ejecutar
                        </button>` : ''
                    }
                    ${mision.estado === 'en_proceso' ? 
                        `<button class="btn btn-warning btn-sm">
                            <i class="fas fa-spinner fa-spin"></i> En proceso
                        </button>` : ''
                    }
                    ${(mision.estado === 'completada' || mision.estado === 'fallida') ? 
                        `<button class="btn btn-info btn-sm" onclick="reiniciarMision(${mision.id})" title="Reiniciar misión">
                            <i class="fas fa-redo"></i> Reiniciar
                        </button>` : ''
                    }
                    <button class="btn btn-danger btn-sm" onclick="eliminarMision(${mision.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        </div>
    `;
}

function mostrarCrearMision() {
    document.getElementById('modal-crear-mision').classList.add('active');
}

function cerrarModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

async function crearMision(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    const datos = {
        titulo: formData.get('titulo'),
        descripcion: formData.get('descripcion'),
        objetivo_final: formData.get('objetivo_final'),
        prioridad: formData.get('prioridad')
    };
    
    try {
        const response = await apiRequest('crear_mision', 'POST', datos);
        
        if (response.exito) {
            mostrarToast('Misión creada exitosamente', 'success');
            cerrarModal('modal-crear-mision');
            form.reset();
            cargarMisiones();
            cargarDashboard();
        }
    } catch (error) {
        console.error('Error creando misión:', error);
        mostrarToast('Error al crear la misión', 'error');
    }
}

async function ejecutarMision(misionId) {
    if (!confirm('¿Iniciar la ejecución del agente para esta misión?')) {
        return;
    }
    
    mostrarToast('Iniciando agente IA...', 'info');
    
    try {
        const response = await apiRequest('ejecutar_mision', 'POST', { id: misionId });
        
        if (response.exito) {
            mostrarToast('Agente ejecutado exitosamente', 'success');
            cargarMisiones();
            cargarDashboard();
        }
    } catch (error) {
        console.error('Error ejecutando misión:', error);
        mostrarToast('Error al ejecutar la misión', 'error');
    }
}

async function eliminarMision(misionId) {
    if (!confirm('¿Estás seguro de eliminar esta misión?')) {
        return;
    }
    
    try {
        const response = await apiRequest('eliminar_mision', 'POST', { id: misionId });
        
        if (response.exito) {
            mostrarToast('Misión eliminada', 'success');
            cargarMisiones();
            cargarDashboard();
        }
    } catch (error) {
        console.error('Error eliminando misión:', error);
        mostrarToast('Error al eliminar la misión', 'error');
    }
}

async function reiniciarMision(misionId) {
    if (!confirm('¿Reiniciar esta misión? Se eliminarán todas las iteraciones anteriores.')) {
        return;
    }
    
    try {
        const response = await apiRequest('reiniciar_mision', 'POST', { id: misionId });
        
        if (response.exito) {
            mostrarToast('Misión reiniciada correctamente', 'success');
            cargarMisiones();
            cargarDashboard();
        }
    } catch (error) {
        console.error('Error reiniciando misión:', error);
        mostrarToast('Error al reiniciar la misión', 'error');
    }
}

async function verDetalleMision(misionId) {
    try {
        console.log('Cargando misión:', misionId);
        const response = await apiRequest('obtener_mision', 'GET', null, { id: misionId });
        console.log('Respuesta completa de la API:', response);
        
        if (response.exito) {
            mostrarDetalleModal(response.mision, response.iteraciones);
        } else {
            console.error('La API devolvió exito=false:', response);
            mostrarToast(response.error || 'Error al cargar detalles', 'error');
        }
    } catch (error) {
        console.error('Error capturado en verDetalleMision:', error);
        mostrarToast(`Error: ${error.message || 'Error al cargar detalles'}`, 'error');
    }
}

function mostrarDetalleModal(mision, iteraciones) {
    document.getElementById('detalle-titulo').textContent = mision.titulo;
    
    const estadoClass = `estado-${mision.estado}`;
    const estadoTexto = mision.estado.replace('_', ' ');
    
    let html = `
        <div style="margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                <span class="mision-estado ${estadoClass}">${estadoTexto}</span>
                <div style="display: flex; gap: 8px; align-items: center;">
                    ${(mision.estado === 'completada' || mision.estado === 'fallida') ? 
                        `<button class="btn btn-info btn-sm" onclick="reiniciarMision(${mision.id}); cerrarModal('modal-detalle-mision');" title="Reiniciar misión">
                            <i class="fas fa-redo"></i> Reiniciar
                        </button>` : ''
                    }
                    <span style="color: #64748b;"><i class="fas fa-calendar"></i> ${formatearFecha(mision.fecha_creacion)}</span>
                </div>
            </div>
            
            <h4 style="margin-bottom: 8px;">Objetivo:</h4>
            <p style="color: #64748b; margin-bottom: 16px;">${escapeHtml(mision.objetivo_final)}</p>
            
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${mision.progreso}%"></div>
            </div>
            <p style="text-align: center; margin-top: 8px; color: #64748b;">Progreso: ${mision.progreso}%</p>
        </div>
        
        <h4 style="margin-bottom: 12px;">Iteraciones (${iteraciones.length}):</h4>
    `;
    
    if (iteraciones.length === 0) {
        html += '<p style="color: #64748b; text-align: center; padding: 20px;">No hay iteraciones todavía</p>';
    } else {
        html += '<div style="max-height: 400px; overflow-y: auto;">';
        iteraciones.forEach(iter => {
            const resultadoIcon = iter.resultado === 'exito' ? '✓' : 
                                 iter.resultado === 'fallo' ? '✗' : '⋯';
            const resultadoColor = iter.resultado === 'exito' ? '#10b981' : 
                                  iter.resultado === 'fallo' ? '#ef4444' : '#f59e0b';
            
            html += `
                <div style="border-left: 3px solid ${resultadoColor}; padding: 12px; margin-bottom: 12px; background: #f8fafc; border-radius: 4px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <strong>Iteración ${iter.numero_iteracion} - ${iter.tipo_accion}</strong>
                        <span style="color: ${resultadoColor};">${resultadoIcon} ${iter.resultado}</span>
                    </div>
                    <p style="color: #64748b; font-size: 14px;">${escapeHtml(iter.descripcion)}</p>
                    ${iter.duracion_segundos ? `<small style="color: #94a3b8;">Duración: ${iter.duracion_segundos}s</small>` : ''}
                </div>
            `;
        });
        html += '</div>';
    }
    
    document.getElementById('detalle-contenido').innerHTML = html;
    document.getElementById('modal-detalle-mision').classList.add('active');
}

// ==========================================
// LOGS
// ==========================================

async function cargarLogs() {
    try {
        const nivel = document.getElementById('filter-nivel').value;
        const params = nivel ? { nivel } : {};
        
        const response = await apiRequest('logs', 'POST', params);
        
        if (response.exito) {
            renderLogs(response.logs);
        }
    } catch (error) {
        console.error('Error cargando logs:', error);
        mostrarToast('Error al cargar logs', 'error');
    }
}

function renderLogs(logs) {
    const container = document.getElementById('logs-container');
    
    if (logs.length === 0) {
        container.innerHTML = '<p style="color: #64748b; text-align: center;">No hay logs</p>';
        return;
    }
    
    container.innerHTML = logs.map(log => {
        const contexto = log.contexto ? JSON.parse(log.contexto) : null;
        return `
            <div class="log-entry log-${log.nivel}">
                <span class="log-timestamp">[${formatearFechaHora(log.timestamp)}]</span>
                <strong>[${log.nivel.toUpperCase()}]</strong>
                ${escapeHtml(log.mensaje)}
                ${contexto ? `<br><small style="opacity: 0.7;">${JSON.stringify(contexto)}</small>` : ''}
            </div>
        `;
    }).join('');
}

// ==========================================
// CONFIGURACIÓN
// ==========================================

async function cargarConfiguracion() {
    try {
        const response = await apiRequest('obtener_config');
        
        if (response.exito) {
            renderConfiguracion(response.configuracion);
        }
    } catch (error) {
        console.error('Error cargando configuración:', error);
        mostrarToast('Error al cargar configuración', 'error');
    }
}

function renderConfiguracion(config) {
    const form = document.getElementById('form-config');
    
    form.innerHTML = config.map(item => {
        const inputType = item.tipo === 'integer' ? 'number' : 
                         item.tipo === 'boolean' ? 'checkbox' : 'text';
        const value = item.tipo === 'boolean' ? 
                     (item.valor === 'true' ? 'checked' : '') : 
                     `value="${escapeHtml(item.valor)}"`;
        
        return `
            <div class="form-group">
                <label for="config-${item.clave}">${item.clave}</label>
                ${item.descripcion ? `<small style="color: #64748b; display: block; margin-bottom: 8px;">${item.descripcion}</small>` : ''}
                <input type="${inputType}" 
                       id="config-${item.clave}" 
                       name="${item.clave}" 
                       ${value}>
            </div>
        `;
    }).join('');
}

async function guardarConfiguracion() {
    const form = document.getElementById('form-config');
    const formData = new FormData(form);
    const datos = {};
    
    for (let [key, value] of formData.entries()) {
        datos[key] = value;
    }
    
    try {
        const response = await apiRequest('actualizar_config', 'POST', datos);
        
        if (response.exito) {
            mostrarToast('Configuración guardada', 'success');
        }
    } catch (error) {
        console.error('Error guardando configuración:', error);
        mostrarToast('Error al guardar configuración', 'error');
    }
}

// ==========================================
// API UTILITIES
// ==========================================

async function apiRequest(action, method = 'GET', data = null, params = null) {
    // Construir URL con parámetros
    let url = `${API_BASE}?action=${action}`;
    
    // Añadir parámetros adicionales si existen
    if (params) {
        for (let [key, value] of Object.entries(params)) {
            url += `&${key}=${encodeURIComponent(value)}`;
        }
    }
    
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    if (data && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(data);
    }
    
    const response = await fetch(url, options);
    
    // Intentar leer el cuerpo de la respuesta
    let responseData;
    const contentType = response.headers.get('content-type');
    
    if (contentType && contentType.includes('application/json')) {
        try {
            responseData = await response.json();
        } catch (e) {
            responseData = { error: 'Respuesta JSON inválida' };
        }
    } else {
        // Si no es JSON, leer como texto
        const text = await response.text();
        console.error('Respuesta no-JSON del servidor:', text);
        responseData = { error: 'El servidor no devolvió JSON', respuesta: text.substring(0, 500) };
    }
    
    if (!response.ok) {
        console.error('Error del servidor:', responseData);
        throw new Error(responseData.error || `HTTP error! status: ${response.status}`);
    }
    
    return responseData;
}

// ==========================================
// UTILIDADES
// ==========================================

function mostrarToast(mensaje, tipo = 'info') {
    const container = document.getElementById('toast-container');
    
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };
    
    const toast = document.createElement('div');
    toast.className = `toast ${tipo}`;
    toast.innerHTML = `
        <i class="fas ${icons[tipo]} toast-icon"></i>
        <span>${mensaje}</span>
    `;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease-in-out';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function formatearFecha(fecha) {
    if (!fecha) return '-';
    const d = new Date(fecha);
    return d.toLocaleDateString('es-ES');
}

function formatearFechaHora(fecha) {
    if (!fecha) return '-';
    const d = new Date(fecha);
    return d.toLocaleString('es-ES');
}

function escapeHtml(text) {
    if (!text) return '';
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Cerrar modales al hacer clic fuera
window.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('active');
    }
});

// ==========================================
// EXPONER FUNCIONES AL SCOPE GLOBAL
// (necesarias para onclick en HTML dinámico)
// ==========================================
window.verDetalleMision = verDetalleMision;
window.mostrarCrearMision = mostrarCrearMision;
window.crearMision = crearMision;
window.ejecutarMision = ejecutarMision;
window.eliminarMision = eliminarMision;
window.reiniciarMision = reiniciarMision;
window.cerrarModal = cerrarModal;
window.cargarLogs = cargarLogs;
window.guardarConfiguracion = guardarConfiguracion;
