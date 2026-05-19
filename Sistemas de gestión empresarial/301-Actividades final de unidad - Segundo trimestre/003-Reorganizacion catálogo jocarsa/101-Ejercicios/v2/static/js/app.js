/**
 * Jocarsa Suite - JavaScript principal
 * Gestiona la interacción con los módulos y el dashboard
 */

// Estado de la aplicación
const state = {
    modules: [],
    currentModule: null,
    dashboardData: null
};

// Sistema de modales
let currentModal = null;

// Sistema de validación
const validators = {
    required: (value) => value && value.trim() !== '',
    email: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
    phone: (value) => /^[+\d\s()-]+$/.test(value),
    number: (value) => !isNaN(value) && value !== '',
    min: (value, min) => parseFloat(value) >= min,
    max: (value, max) => parseFloat(value) <= max
};

// Inicializar aplicación
document.addEventListener("DOMContentLoaded", () => {
    console.log("Jocarsa Suite - Inicializando...");
    
    loadModules();
    loadDashboard();
    
    // Event listener para el botón dashboard
    document.getElementById("btn-dashboard").addEventListener("click", () => {
        showDashboard();
    });
});

/**
 * Carga la lista de módulos disponibles
 */
async function loadModules() {
    try {
        const response = await fetch("/api/modules");
        const data = await response.json();
        
        state.modules = data.modules;
        renderModules();
        
        console.log(`✅ ${state.modules.length} módulos cargados`);
    } catch (error) {
        console.error("Error cargando módulos:", error);
        showError("No se pudieron cargar los módulos");
    }
}

/**
 * Renderiza la lista de módulos en el sidebar
 */
function renderModules() {
    const container = document.getElementById("modules-list");
    
    if (state.modules.length === 0) {
        container.innerHTML = '<div class="loading">No hay módulos disponibles</div>';
        return;
    }
    
    // Agrupar módulos por categoría
    const modulesByCategory = {};
    state.modules.forEach(mod => {
        const category = mod.category || 'general';
        if (!modulesByCategory[category]) {
            modulesByCategory[category] = [];
        }
        modulesByCategory[category].push(mod);
    });
    
    // Renderizar módulos
    let html = '';
    
    for (const [category, modules] of Object.entries(modulesByCategory)) {
        modules.forEach(mod => {
            html += `
                <div class="module-card" data-module="${mod.type}" onclick="selectModule('${mod.type}')">
                    <h3>${mod.icon} ${mod.name}</h3>
                    <p>${mod.description}</p>
                    <div class="module-category">${category}</div>
                </div>
            `;
        });
    }
    
    container.innerHTML = html;
}

/**
 * Selecciona un módulo
 */
async function selectModule(moduleType) {
    console.log(`Seleccionando módulo: ${moduleType}`);
    
    state.currentModule = moduleType;
    
    // Actualizar UI
    document.querySelectorAll('.module-card').forEach(card => {
        card.classList.remove('active');
    });
    
    const selectedCard = document.querySelector(`[data-module="${moduleType}"]`);
    if (selectedCard) {
        selectedCard.classList.add('active');
    }
    
    // Ocultar dashboard, mostrar módulo
    document.getElementById("dashboard-section").classList.remove("active");
    document.getElementById("module-section").classList.add("active");
    
    // Cargar datos del módulo
    await loadModuleData(moduleType);
}

/**
 * Carga los datos de un módulo específico
 */
async function loadModuleData(moduleType) {
    const container = document.getElementById("module-content");
    container.innerHTML = '<div class="loading">Cargando datos del módulo...</div>';
    
    try {
        const response = await fetch(`/api/module/${moduleType}`);
        const result = await response.json();
        
        if (result.ok) {
            renderModuleContent(moduleType, result.data);
        } else {
            showError(result.error || "Error cargando módulo");
        }
    } catch (error) {
        console.error("Error:", error);
        showError("Error de conexión con el servidor");
    }
}

/**
 * Renderiza el contenido de un módulo
 */
function renderModuleContent(moduleType, data) {
    const container = document.getElementById("module-content");
    const module = state.modules.find(m => m.type === moduleType);
    
    let html = `
        <div class="module-content-card">
            <h3>${module.icon} ${module.name}</h3>
            <p>${module.description}</p>
        </div>
    `;
    
    // Renderizar según el tipo de módulo
    if (moduleType === 'crm') {
        html += renderCRMContent(data);
    } else if (moduleType === 'proyectos') {
        html += renderProyectosContent(data);
    } else if (moduleType === 'formularios') {
        html += renderFormulariosContent(data);
    } else if (moduleType === 'informes') {
        html += renderInformesContent(data);
    } else {
        html += `<div class="module-content-card">
            <pre>${JSON.stringify(data, null, 2)}</pre>
        </div>`;
    }
    
    container.innerHTML = html;
}

/**
 * Renderiza el contenido del módulo CRM
 */
function renderCRMContent(data) {
    const clientes = data.clientes || [];
    const oportunidades = data.oportunidades || [];
    
    let html = `
        <div class="module-content-card">
            <h3>👥 Clientes (${clientes.length})</h3>
            <button class="btn" onclick="addCliente()">➕ Nuevo Cliente</button>
            <div style="margin-top: 1rem;">
    `;
    
    if (clientes.length === 0) {
        html += '<p>No hay clientes registrados. Crea el primero para comenzar.</p>';
    } else {
        clientes.forEach(cliente => {
            html += `
                <div style="padding: 1rem; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>${cliente.nombre}</strong> - ${cliente.empresa}<br>
                        <small>📧 ${cliente.email} | 📱 ${cliente.telefono}</small>
                    </div>
                    <div class="action-buttons">
                        <button class="btn-action btn-edit" onclick='editCliente(${JSON.stringify(cliente)})' title="Editar">✏️</button>
                        <button class="btn-action btn-delete" onclick="deleteCliente(${cliente.id})" title="Eliminar">🗑️</button>
                    </div>
                </div>
            `;
        });
    }
    
    html += `
            </div>
        </div>
        
        <div class="module-content-card">
            <h3>💼 Oportunidades de Venta (${oportunidades.length})</h3>
            <button class="btn" onclick="addOportunidad()">➕ Nueva Oportunidad</button>
            <div style="margin-top: 1rem;">
    `;
    
    if (oportunidades.length === 0) {
        html += '<p>No hay oportunidades registradas.</p>';
    } else {
        oportunidades.forEach(op => {
            const estadoColor = {
                'abierta': '#10b981',
                'en_proceso': '#f59e0b',
                'ganada': '#2563eb',
                'perdida': '#ef4444'
            }[op.estado] || '#64748b';
            
            html += `
                <div style="padding: 1rem; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>${op.titulo}</strong> - ${op.valor}€<br>
                        <small>Probabilidad: ${op.probabilidad}%</small>
                        <span style="background: ${estadoColor}; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem; margin-left: 0.5rem;">${op.estado}</span>
                    </div>
                    <div class="action-buttons">
                        <button class="btn-action btn-edit" onclick='editOportunidad(${JSON.stringify(op)})' title="Editar">✏️</button>
                        <button class="btn-action btn-delete" onclick="deleteOportunidad(${op.id})" title="Eliminar">🗑️</button>
                    </div>
                </div>
            `;
        });
    }
    
    html += '</div></div>';
    
    return html;
}

/**
 * Renderiza el contenido del módulo de Proyectos
 */
function renderProyectosContent(data) {
    const proyectos = data.proyectos || [];
    const tareas = data.tareas || [];
    
    let html = `
        <div class="module-content-card">
            <h3>📋 Proyectos (${proyectos.length})</h3>
            <button class="btn" onclick="addProyecto()">➕ Nuevo Proyecto</button>
            <div style="margin-top: 1rem;">
    `;
    
    if (proyectos.length === 0) {
        html += '<p>No hay proyectos. Crea el primero para comenzar.</p>';
    } else {
        proyectos.forEach(proyecto => {
            const tareasProyecto = tareas.filter(t => t.proyecto_id === proyecto.id).length;
            html += `
                <div style="padding: 1rem; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>${proyecto.nombre}</strong><br>
                        <small>${proyecto.descripcion}</small><br>
                        <small>📊 Estado: ${proyecto.estado} | 📋 Tareas: ${tareasProyecto}</small>
                    </div>
                    <div class="action-buttons">
                        <button class="btn-action btn-edit" onclick='editProyecto(${JSON.stringify(proyecto)})' title="Editar">✏️</button>
                        <button class="btn-action btn-delete" onclick="deleteProyecto(${proyecto.id})" title="Eliminar">🗑️</button>
                    </div>
                </div>
            `;
        });
    }
    
    html += `</div></div>`;
    
    return html;
}

/**
 * Renderiza el contenido del módulo de Formularios
 */
function renderFormulariosContent(data) {
    const formularios = data.formularios || [];
    
    let html = `
        <div class="module-content-card">
            <h3>📝 Formularios (${formularios.length})</h3>
            <button class="btn" onclick="createFormulario()">➕ Nuevo Formulario</button>
            <div style="margin-top: 1rem;">
    `;
    
    if (formularios.length === 0) {
        html += '<p>No hay formularios creados.</p>';
    } else {
        formularios.forEach(form => {
            html += `
                <div style="padding: 1rem; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>${form.titulo}</strong><br>
                        <small>${form.descripcion}</small><br>
                        <small>📊 Respuestas: ${form.respuestas_count || 0} | Estado: ${form.activo ? '✅ Activo' : '❌ Inactivo'}</small>
                    </div>
                    <div class="action-buttons">
                        <button class="btn-action btn-edit" onclick='editFormulario(${JSON.stringify(form)})' title="Editar">✏️</button>
                        <button class="btn-action btn-delete" onclick="deleteFormulario(${form.id})" title="Eliminar">🗑️</button>
                    </div>
                </div>
            `;
        });
    }
    
    html += `</div></div>`;
    
    return html;
}

/**
 * Renderiza el contenido del módulo de Informes
 */
function renderInformesContent(data) {
    const informes = data.informes_generados || [];
    
    let html = `
        <div class="module-content-card">
            <h3>📊 Informes Generados (${informes.length})</h3>
            <div style="display: flex; gap: 1rem; margin: 1rem 0;">
                <button class="btn" onclick="generarInforme('general')">📄 Informe General</button>
                <button class="btn" onclick="generarInforme('ventas')">💰 Informe de Ventas</button>
                <button class="btn" onclick="generarInforme('proyectos')">📋 Informe de Proyectos</button>
                <button class="btn" onclick="generarInforme('integracion')">🔗 Informe de Integración</button>
            </div>
            <div style="margin-top: 1rem;">
    `;
    
    if (informes.length === 0) {
        html += '<p>No hay informes generados. Genera el primero con los botones de arriba.</p>';
    } else {
        informes.slice().reverse().forEach(informe => {
            html += `
                <div style="padding: 1rem; border: 1px solid #e2e8f0; border-radius: 8px; margin-bottom: 1rem;">
                    <strong>${informe.contenido.tipo}</strong><br>
                    <small>📅 ${new Date(informe.fecha_generacion).toLocaleString('es-ES')}</small>
                    <pre style="background: #f8fafc; padding: 1rem; margin-top: 0.5rem; border-radius: 4px; font-size: 0.85rem;">${JSON.stringify(informe.contenido, null, 2)}</pre>
                </div>
            `;
        });
    }
    
    html += `</div></div>`;
    
    return html;
}

/**
 * Carga los datos del dashboard
 */
async function loadDashboard() {
    try {
        const response = await fetch("/api/dashboard");
        const data = await response.json();
        
        state.dashboardData = data;
        renderDashboard();
        
        console.log("✅ Dashboard cargado");
    } catch (error) {
        console.error("Error cargando dashboard:", error);
    }
}

/**
 * Renderiza el dashboard
 */
function renderDashboard() {
    const container = document.getElementById("dashboard-cards");
    
    if (!state.dashboardData || !state.dashboardData.modules_summary) {
        container.innerHTML = '<div class="loading">No hay datos disponibles</div>';
        return;
    }
    
    let html = '';
    
    state.dashboardData.modules_summary.forEach(modSummary => {
        const module = state.modules.find(m => m.type === modSummary.module);
        if (!module) return;
        
        html += `
            <div class="dashboard-card">
                <h3>${module.icon} ${module.name}</h3>
        `;
        
        // Renderizar estadísticas del módulo
        const summary = modSummary.summary;
        for (const [key, value] of Object.entries(summary)) {
            const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            html += `
                <div class="dashboard-stat">
                    <span class="label">${label}</span>
                    <span class="value">${value}</span>
                </div>
            `;
        }
        
        html += '</div>';
    });
    
    container.innerHTML = html;
}

/**
 * Muestra el dashboard
 */
function showDashboard() {
    document.getElementById("module-section").classList.remove("active");
    document.getElementById("dashboard-section").classList.add("active");
    
    // Desactivar módulo seleccionado
    document.querySelectorAll('.module-card').forEach(card => {
        card.classList.remove('active');
    });
    
    state.currentModule = null;
    
    // Recargar datos del dashboard
    loadDashboard();
}

/**
 * Muestra un error
 */
function showError(message) {
    alert("❌ Error: " + message);
}

// ===== Funciones de acciones de módulos =====

function addCliente() {
    const nombre = prompt("Nombre del cliente:");
    if (!nombre) return;
    
    const email = prompt("Email:");
    const telefono = prompt("Teléfono:");
    const empresa = prompt("Empresa:");
    
    executeModuleAction('crm', 'add_cliente', {
        nombre, email, telefono, empresa
    });
}

function addOportunidad() {
    const titulo = prompt("Título de la oportunidad:");
    if (!titulo) return;
    
    const valor = parseFloat(prompt("Valor estimado (€):") || "0");
    const probabilidad = parseInt(prompt("Probabilidad (0-100):") || "50");
    
    executeModuleAction('crm', 'add_oportunidad', {
        titulo, valor, probabilidad, cliente_id: 1
    });
}

function addProyecto() {
    const nombre = prompt("Nombre del proyecto:");
    if (!nombre) return;
    
    const descripcion = prompt("Descripción:");
    
    executeModuleAction('proyectos', 'add_proyecto', {
        nombre, descripcion
    });
}

function createFormulario() {
    const titulo = prompt("Título del formulario:");
    if (!titulo) return;
    
    const descripcion = prompt("Descripción:");
    
    executeModuleAction('formularios', 'create_formulario', {
        titulo, descripcion,
        campos: [
            {name: "nombre", label: "Nombre", type: "text", required: true},
            {name: "email", label: "Email", type: "email", required: true},
            {name: "comentario", label: "Comentario", type: "textarea", required: false}
        ]
    });
}

async function generarInforme(tipo) {
    await executeModuleAction('informes', 'generar_informe', { tipo });
}

/**
 * Ejecuta una acción en un módulo
 */
async function executeModuleAction(moduleType, action, params) {
    try {
        const response = await fetch(`/api/module/${moduleType}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action, params })
        });
        
        const result = await response.json();
        
        if (result.ok) {
            console.log("✅ Acción ejecutada:", result.result);
            showToast(result.result.message || "Acción completada", "success");
            
            // Recargar datos del módulo actual
            if (state.currentModule === moduleType) {
                loadModuleData(moduleType);
            }
            
            // Recargar dashboard
            loadDashboard();
        } else {
            showToast(result.error, "error");
        }
    } catch (error) {
        console.error("Error ejecutando acción:", error);
        showToast("Error de conexión", "error");
    }
}

// ===== Sistema de Modales =====

/**
 * Muestra un modal de confirmación
 */
function showConfirmModal(title, message, onConfirm) {
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay active';
    overlay.innerHTML = `
        <div class="modal">
            <h3>${title}</h3>
            <p>${message}</p>
            <div class="modal-buttons">
                <button class="btn btn-cancel" onclick="closeModal()">Cancelar</button>
                <button class="btn btn-confirm" id="confirm-btn">Confirmar</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(overlay);
    currentModal = overlay;
    
    // Event listener para confirmar
    document.getElementById('confirm-btn').addEventListener('click', () => {
        onConfirm();
        closeModal();
    });
    
    // Cerrar al hacer click fuera del modal
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            closeModal();
        }
    });
}

/**
 * Muestra un modal de edición
 */
function showEditModal(title, fields, data, onSave) {
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay active';
    
    let fieldsHTML = '';
    fields.forEach(field => {
        const value = data[field.name] || '';
        const required = field.required ? 'required' : '';
        const type = field.type || 'text';
        
        if (type === 'textarea') {
            fieldsHTML += `
                <div class="form-group">
                    <label for="edit-${field.name}">${field.label}</label>
                    <textarea id="edit-${field.name}" ${required}>${value}</textarea>
                    <span class="form-error">Este campo es requerido</span>
                </div>
            `;
        } else if (type === 'select' && field.options) {
            let optionsHTML = '';
            field.options.forEach(opt => {
                const selected = opt === value ? 'selected' : '';
                optionsHTML += `<option value="${opt}" ${selected}>${opt}</option>`;
            });
            fieldsHTML += `
                <div class="form-group">
                    <label for="edit-${field.name}">${field.label}</label>
                    <select id="edit-${field.name}" ${required}>
                        ${optionsHTML}
                    </select>
                    <span class="form-error">Este campo es requerido</span>
                </div>
            `;
        } else {
            fieldsHTML += `
                <div class="form-group">
                    <label for="edit-${field.name}">${field.label}</label>
                    <input type="${type}" id="edit-${field.name}" value="${value}" ${required}>
                    <span class="form-error">Este campo es requerido</span>
                </div>
            `;
        }
    });
    
    overlay.innerHTML = `
        <div class="modal">
            <h3>${title}</h3>
            <form class="edit-form" id="edit-form">
                ${fieldsHTML}
                <div class="modal-buttons">
                    <button type="button" class="btn btn-cancel" onclick="closeModal()">Cancelar</button>
                    <button type="submit" class="btn btn-confirm" style="background: var(--color-exito)">Guardar</button>
                </div>
            </form>
        </div>
    `;
    
    document.body.appendChild(overlay);
    currentModal = overlay;
    
    // Event listener para el formulario
    document.getElementById('edit-form').addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Validar formulario
        if (!validateForm('edit-form', fields)) {
            return;
        }
        
        // Recopilar datos
        const formData = {};
        fields.forEach(field => {
            const input = document.getElementById(`edit-${field.name}`);
            formData[field.name] = input.value;
        });
        
        onSave(formData);
        closeModal();
    });
    
    // Cerrar al hacer click fuera
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            closeModal();
        }
    });
}

/**
 * Cierra el modal actual
 */
function closeModal() {
    if (currentModal) {
        currentModal.remove();
        currentModal = null;
    }
}

// ===== Sistema de Validación =====

/**
 * Valida un formulario
 */
function validateForm(formId, fields) {
    const form = document.getElementById(formId);
    let isValid = true;
    
    fields.forEach(field => {
        if (!field.required && !field.validation) return;
        
        const input = document.getElementById(`edit-${field.name}`) || 
                     document.getElementById(field.name);
        
        if (!input) return;
        
        const group = input.closest('.form-group');
        const value = input.value;
        
        // Validar campo requerido
        if (field.required && !validators.required(value)) {
            group.classList.add('error');
            isValid = false;
            return;
        }
        
        // Validaciones específicas
        if (field.validation) {
            if (field.validation === 'email' && !validators.email(value)) {
                group.classList.add('error');
                group.querySelector('.form-error').textContent = 'Email inválido';
                isValid = false;
                return;
            }
            
            if (field.validation === 'phone' && value && !validators.phone(value)) {
                group.classList.add('error');
                group.querySelector('.form-error').textContent = 'Teléfono inválido';
                isValid = false;
                return;
            }
            
            if (field.validation === 'number' && !validators.number(value)) {
                group.classList.add('error');
                group.querySelector('.form-error').textContent = 'Debe ser un número';
                isValid = false;
                return;
            }
        }
        
        // Limpiar error si pasa validación
        group.classList.remove('error');
    });
    
    return isValid;
}

// ===== Sistema de Toast Notifications =====

/**
 * Muestra una notificación toast
 */
function showToast(message, type = 'success') {
    const icons = {
        success: '✓',
        error: '✗',
        warning: '⚠'
    };
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <span class="toast-icon">${icons[type] || '●'}</span>
        <span>${message}</span>
        <button class="toast-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto-eliminar después de 3 segundos
    setTimeout(() => {
        if (toast.parentElement) {
            toast.remove();
        }
    }, 3000);
}

// ===== Funciones de CRM: Editar y Eliminar =====

/**
 * Edita un cliente
 */
function editCliente(cliente) {
    const fields = [
        { name: 'nombre', label: 'Nombre', required: true },
        { name: 'email', label: 'Email', required: true, validation: 'email' },
        { name: 'telefono', label: 'Teléfono', required: true, validation: 'phone' },
        { name: 'empresa', label: 'Empresa' },
        { name: 'notas', label: 'Notas', type: 'textarea' }
    ];
    
    showEditModal('Editar Cliente', fields, cliente, (formData) => {
        executeModuleAction('crm', 'update_cliente', {
            cliente_id: cliente.id,
            ...formData
        });
    });
}

/**
 * Elimina un cliente
 */
function deleteCliente(clienteId) {
    showConfirmModal(
        'Confirmar eliminación',
        '¿Estás seguro de que deseas eliminar este cliente?',
        () => {
            executeModuleAction('crm', 'delete_cliente', { cliente_id: clienteId });
        }
    );
}

/**
 * Edita una oportunidad
 */
function editOportunidad(oportunidad) {
    const fields = [
        { name: 'titulo', label: 'Título', required: true },
        { name: 'valor', label: 'Valor (€)', type: 'number', required: true, validation: 'number' },
        { name: 'probabilidad', label: 'Probabilidad (%)', type: 'number', required: true, validation: 'number' },
        { 
            name: 'estado', 
            label: 'Estado', 
            type: 'select', 
            required: true,
            options: ['abierta', 'en_proceso', 'ganada', 'perdida']
        },
        { name: 'descripcion', label: 'Descripción', type: 'textarea' }
    ];
    
    showEditModal('Editar Oportunidad', fields, oportunidad, (formData) => {
        executeModuleAction('crm', 'update_oportunidad', {
            oportunidad_id: oportunidad.id,
            ...formData
        });
    });
}

/**
 * Elimina una oportunidad
 */
function deleteOportunidad(oportunidadId) {
    showConfirmModal(
        'Confirmar eliminación',
        '¿Estás seguro de que deseas eliminar esta oportunidad?',
        () => {
            executeModuleAction('crm', 'delete_oportunidad', { oportunidad_id: oportunidadId });
        }
    );
}

// ===== Funciones de Proyectos: Editar y Eliminar =====

/**
 * Edita un proyecto
 */
function editProyecto(proyecto) {
    const fields = [
        { name: 'nombre', label: 'Nombre', required: true },
        { name: 'descripcion', label: 'Descripción', type: 'textarea' },
        { 
            name: 'estado', 
            label: 'Estado', 
            type: 'select', 
            required: true,
            options: ['planificacion', 'en_curso', 'pausado', 'completado', 'cancelado']
        },
        { name: 'fecha_inicio', label: 'Fecha Inicio', type: 'date' },
        { name: 'fecha_fin', label: 'Fecha Fin', type: 'date' }
    ];
    
    showEditModal('Editar Proyecto', fields, proyecto, (formData) => {
        executeModuleAction('proyectos', 'update_proyecto', {
            proyecto_id: proyecto.id,
            ...formData
        });
    });
}

/**
 * Elimina un proyecto
 */
function deleteProyecto(proyectoId) {
    showConfirmModal(
        'Confirmar eliminación',
        '¿Estás seguro de que deseas eliminar este proyecto? Se eliminarán también todas sus tareas.',
        () => {
            executeModuleAction('proyectos', 'delete_proyecto', { proyecto_id: proyectoId });
        }
    );
}

// ===== Funciones de Formularios: Editar y Eliminar =====

/**
 * Edita un formulario
 */
function editFormulario(formulario) {
    const fields = [
        { name: 'titulo', label: 'Título', required: true },
        { name: 'descripcion', label: 'Descripción', type: 'textarea' },
        { 
            name: 'activo', 
            label: 'Estado', 
            type: 'select', 
            required: true,
            options: ['true', 'false']
        }
    ];
    
    // Convertir activo a string para el selector
    const formularioEdit = { ...formulario, activo: formulario.activo.toString() };
    
    showEditModal('Editar Formulario', fields, formularioEdit, (formData) => {
        // Convertir 'activo' de vuelta a booleano
        formData.activo = formData.activo === 'true';
        
        executeModuleAction('formularios', 'update_formulario', {
            formulario_id: formulario.id,
            ...formData,
            campos: formulario.campos // Mantener los campos originales
        });
    });
}

/**
 * Elimina un formulario
 */
function deleteFormulario(formularioId) {
    showConfirmModal(
        'Confirmar eliminación',
        '¿Estás seguro de que deseas eliminar este formulario? Se eliminarán también todas sus respuestas.',
        () => {
            executeModuleAction('formularios', 'delete_formulario', { formulario_id: formularioId });
        }
    );
}
