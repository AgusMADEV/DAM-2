/**
 * Sistema de Gestión de Gimnasio - JavaScript Frontend
 * Desarrollo de Interfaces - Programación funcional y orientada a objetos
 */

// Estado global de la aplicación
const appState = {
    currentSection: 'dashboard',
    usuario: null,
    datos: {
        socios: [],
        entrenadores: [],
        clases: [],
        membresias: [],
        asistencias: []
    }
};

// Configuración de la API
const API_BASE = 'http://localhost:5000/api';

/**
 * Clase para gestionar la navegación del sistema
 */
class NavigationManager {
    constructor() {
        this.initEventListeners();
    }

    initEventListeners() {
        // Navegación por secciones
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const section = link.getAttribute('data-section');
                this.showSection(section);
            });
        });
    }

    showSection(sectionId) {
        // Ocultar todas las secciones
        document.querySelectorAll('.content-section').forEach(section => {
            section.classList.remove('active');
        });

        // Mostrar la sección seleccionada
        document.getElementById(sectionId).classList.add('active');

        // Actualizar navegación
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        document.querySelector(`[data-section="${sectionId}"]`).classList.add('active');

        // Actualizar estado
        appState.currentSection = sectionId;

        // Cargar datos según la sección
        this.loadSectionData(sectionId);
    }

    loadSectionData(sectionId) {
        switch (sectionId) {
            case 'dashboard':
                dashboardController.cargarDatos();
                break;
            case 'socios':
                sociosController.cargarSocios();
                break;
            case 'entrenadores':
                entrenadoresController.cargarEntrenadores();
                break;
            case 'clases':
                clasesController.cargarClases();
                break;
            case 'membresias':
                membresiasController.cargarMembresias();
                break;
            case 'asistencias':
                asistenciasController.cargarAsistencias();
                break;
            case 'informes':
                informesController.cargarInformes();
                break;
        }
    }
}

/**
 * Controlador del Dashboard
 */
class DashboardController {
    async cargarDatos() {
        try {
            const response = await fetch(`${API_BASE}/informes/dashboard`);
            const data = await response.json();
            
            if (data.success) {
                this.actualizarEstadisticas(data.data);
            }
        } catch (error) {
            console.error('Error al cargar dashboard:', error);
            // Datos de ejemplo si falla la API
            this.actualizarEstadisticas({
                total_socios: 4,
                socios_activos: 3,
                total_entrenadores: 3,
                total_clases: 5,
                ingresos_mes: 465.00
            });
        }
    }

    actualizarEstadisticas(stats) {
        document.getElementById('total-socios').textContent = stats.total_socios;
        document.getElementById('socios-activos').textContent = stats.socios_activos;
        document.getElementById('total-entrenadores').textContent = stats.total_entrenadores;
        document.getElementById('total-clases').textContent = stats.total_clases;
        
        this.cargarAlertas();
    }

    async cargarAlertas() {
        const alertasContainer = document.getElementById('alertas-sistema');
        
        try {
            const response = await fetch(`${API_BASE}/informes/membresias-vencer`);
            const data = await response.json();
            
            if (data.success && data.data.length > 0) {
                alertasContainer.innerHTML = `
                    <div class="alert alert-warning">
                        <i class="fas fa-exclamation-triangle"></i>
                        <span>${data.data.length} membresías próximas a vencer en los próximos 7 días</span>
                    </div>
                `;
            } else {
                alertasContainer.innerHTML = `
                    <div class="alert alert-success">
                        <i class="fas fa-check-circle"></i>
                        <span>No hay alertas pendientes. Todo funcionando correctamente.</span>
                    </div>
                `;
            }
        } catch (error) {
            alertasContainer.innerHTML = `
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i>
                    <span>Sistema operativo. Conectando con la base de datos...</span>
                </div>
            `;
        }
    }
}

/**
 * Controlador de Socios
 */
class SociosController {
    async cargarSocios() {
        const tbody = document.getElementById('tabla-socios');
        tbody.innerHTML = '<tr><td colspan="8" class="text-center">Cargando...</td></tr>';
        
        try {
            const response = await fetch(`${API_BASE}/socios`);
            const data = await response.json();
            
            if (data.success) {
                appState.datos.socios = data.data;
                this.renderizarSocios(data.data);
            }
        } catch (error) {
            console.error('Error al cargar socios:', error);
            tbody.innerHTML = '<tr><td colspan="8" class="text-center text-danger">Error al cargar socios</td></tr>';
        }
    }

    renderizarSocios(socios) {
        const tbody = document.getElementById('tabla-socios');
        tbody.innerHTML = '';

        if (socios.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="text-center">No hay socios registrados</td></tr>';
            return;
        }

        socios.forEach(socio => {
            const row = tbody.insertRow();
            const estadoBadge = socio.estado === 'activo' ? 'badge-success' : 'badge-danger';
            const membresiaBadge = socio.estado_membresia === 'Con membresía' ? 'badge-success' : 'badge-warning';
            
            row.innerHTML = `
                <td><strong>${socio.numero_socio}</strong></td>
                <td>${socio.nombre} ${socio.apellidos}</td>
                <td>${socio.email || '-'}</td>
                <td>${socio.telefono || '-'}</td>
                <td>${socio.ciudad || '-'}</td>
                <td><span class="badge ${membresiaBadge}">${socio.estado_membresia}</span></td>
                <td><span class="badge ${estadoBadge}">${socio.estado}</span></td>
                <td>
                    <button class="btn btn-sm btn-outline" onclick="sociosController.verDetalle(${socio.id})" title="Ver detalle">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-sm btn-warning" onclick="sociosController.editarSocio(${socio.id})" title="Editar">
                        <i class="fas fa-edit"></i>
                    </button>
                </td>
            `;
        });
    }

    verDetalle(id) {
        const socio = appState.datos.socios.find(s => s.id === id);
        if (socio) {
            modalManager.show('Detalle del Socio', `
                <div class="detalle-socio">
                    <h4><i class="fas fa-user"></i> ${socio.nombre} ${socio.apellidos}</h4>
                    <p><strong>Nº Socio:</strong> ${socio.numero_socio}</p>
                    <p><strong>Email:</strong> ${socio.email || 'No especificado'}</p>
                    <p><strong>Teléfono:</strong> ${socio.telefono || 'No especificado'}</p>
                    <p><strong>Ciudad:</strong> ${socio.ciudad || 'No especificada'}</p>
                    <p><strong>Estado Membresía:</strong> <span class="badge ${socio.estado_membresia === 'Con membresía' ? 'badge-success' : 'badge-warning'}">${socio.estado_membresia}</span></p>
                    <div class="form-actions">
                        <button class="btn btn-outline" onclick="modalManager.close()">Cerrar</button>
                    </div>
                </div>
            `);
        }
    }

    editarSocio(id) {
        notificationManager.show('Funcionalidad de edición en desarrollo', 'info');
    }
}

/**
 * Controlador de Entrenadores
 */
class EntrenadoresController {
    async cargarEntrenadores() {
        const tbody = document.getElementById('tabla-entrenadores');
        tbody.innerHTML = '<tr><td colspan="8" class="text-center">Cargando...</td></tr>';
        
        try {
            const response = await fetch(`${API_BASE}/entrenadores`);
            const data = await response.json();
            
            if (data.success) {
                appState.datos.entrenadores = data.data;
                this.renderizarEntrenadores(data.data);
            }
        } catch (error) {
            console.error('Error al cargar entrenadores:', error);
            tbody.innerHTML = '<tr><td colspan="8" class="text-center text-danger">Error al cargar entrenadores</td></tr>';
        }
    }

    renderizarEntrenadores(entrenadores) {
        const tbody = document.getElementById('tabla-entrenadores');
        tbody.innerHTML = '';

        if (entrenadores.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="text-center">No hay entrenadores registrados</td></tr>';
            return;
        }

        entrenadores.forEach(entrenador => {
            const row = tbody.insertRow();
            const estadoBadge = entrenador.estado === 'activo' ? 'badge-success' : 'badge-danger';
            
            row.innerHTML = `
                <td><strong>${entrenador.codigo_empleado}</strong></td>
                <td>${entrenador.nombre} ${entrenador.apellidos}</td>
                <td><span class="badge badge-info">${entrenador.especialidad}</span></td>
                <td>${entrenador.telefono || '-'}</td>
                <td>${entrenador.email || '-'}</td>
                <td><span class="badge badge-purple">${entrenador.total_clases} clases</span></td>
                <td><span class="badge ${estadoBadge}">${entrenador.estado}</span></td>
                <td>
                    <button class="btn btn-sm btn-outline" onclick="entrenadoresController.verDetalle(${entrenador.id})" title="Ver detalle">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            `;
        });
    }

    verDetalle(id) {
        const entrenador = appState.datos.entrenadores.find(e => e.id === id);
        if (entrenador) {
            modalManager.show('Detalle del Entrenador', `
                <div class="detalle-entrenador">
                    <h4><i class="fas fa-user-tie"></i> ${entrenador.nombre} ${entrenador.apellidos}</h4>
                    <p><strong>Código:</strong> ${entrenador.codigo_empleado}</p>
                    <p><strong>Especialidad:</strong> <span class="badge badge-info">${entrenador.especialidad}</span></p>
                    <p><strong>Email:</strong> ${entrenador.email || 'No especificado'}</p>
                    <p><strong>Teléfono:</strong> ${entrenador.telefono || 'No especificado'}</p>
                    <p><strong>Clases Asignadas:</strong> ${entrenador.total_clases}</p>
                    <div class="form-actions">
                        <button class="btn btn-outline" onclick="modalManager.close()">Cerrar</button>
                    </div>
                </div>
            `);
        }
    }
}

/**
 * Controlador de Clases
 */
class ClasesController {
    async cargarClases() {
        const tbody = document.getElementById('tabla-clases');
        tbody.innerHTML = '<tr><td colspan="9" class="text-center">Cargando...</td></tr>';
        
        try {
            const response = await fetch(`${API_BASE}/clases`);
            const data = await response.json();
            
            if (data.success) {
                appState.datos.clases = data.data;
                this.renderizarClases(data.data);
            }
        } catch (error) {
            console.error('Error al cargar clases:', error);
            tbody.innerHTML = '<tr><td colspan="9" class="text-center text-danger">Error al cargar clases</td></tr>';
        }
    }

    renderizarClases(clases) {
        const tbody = document.getElementById('tabla-clases');
        tbody.innerHTML = '';

        if (clases.length === 0) {
            tbody.innerHTML = '<tr><td colspan="9" class="text-center">No hay clases programadas</td></tr>';
            return;
        }

        clases.forEach(clase => {
            const row = tbody.insertRow();
            const nivelBadge = {
                'principiante': 'badge-success',
                'intermedio': 'badge-warning',
                'avanzado': 'badge-danger'
            }[clase.nivel] || 'badge-info';
            
            const disponibilidad = `${clase.plazas_disponibles}/${clase.capacidad_maxima}`;
            const disponibilidadClass = clase.plazas_disponibles === 0 ? 'text-danger' : 'text-success';
            
            row.innerHTML = `
                <td><strong>${clase.nombre}</strong></td>
                <td>${clase.dia_semana}</td>
                <td>${clase.hora_inicio}</td>
                <td>${clase.duracion_minutos} min</td>
                <td>${clase.entrenador}</td>
                <td>${clase.sala || '-'}</td>
                <td><span class="badge ${nivelBadge}">${clase.nivel}</span></td>
                <td class="${disponibilidadClass}"><strong>${disponibilidad}</strong></td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="clasesController.reservarClase(${clase.id})" title="Reservar plaza">
                        <i class="fas fa-calendar-plus"></i>
                    </button>
                </td>
            `;
        });
    }

    reservarClase(id) {
        notificationManager.show('Funcionalidad de reservas en desarrollo', 'info');
    }
}

/**
 * Controlador de Membresías
 */
class MembresiasController {
    async cargarMembresias() {
        const tbody = document.getElementById('tabla-membresias');
        tbody.innerHTML = '<tr><td colspan="8" class="text-center">Cargando...</td></tr>';
        
        try {
            const response = await fetch(`${API_BASE}/membresias`);
            const data = await response.json();
            
            if (data.success) {
                appState.datos.membresias = data.data;
                this.renderizarMembresias(data.data);
            }
        } catch (error) {
            console.error('Error al cargar membresías:', error);
            tbody.innerHTML = '<tr><td colspan="8" class="text-center text-danger">Error al cargar membresías</td></tr>';
        }
    }

    renderizarMembresias(membresias) {
        const tbody = document.getElementById('tabla-membresias');
        tbody.innerHTML = '';

        if (membresias.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="text-center">No hay membresías registradas</td></tr>';
            return;
        }

        membresias.forEach(membresia => {
            const row = tbody.insertRow();
            const vigenciaBadge = membresia.estado_vigencia === 'Vigente' ? 'badge-success' : 'badge-danger';
            
            row.innerHTML = `
                <td><strong>${membresia.numero_socio}</strong></td>
                <td>${membresia.socio}</td>
                <td><span class="badge badge-info">${membresia.tipo_membresia}</span></td>
                <td>${membresia.fecha_inicio}</td>
                <td>${membresia.fecha_fin}</td>
                <td><strong>${membresia.precio_pagado.toFixed(2)}€</strong></td>
                <td><span class="badge ${vigenciaBadge}">${membresia.estado_vigencia}</span></td>
                <td>
                    <button class="btn btn-sm btn-outline" onclick="membresiasController.verDetalle(${membresia.id})" title="Ver detalle">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            `;
        });
    }

    verDetalle(id) {
        const membresia = appState.datos.membresias.find(m => m.id === id);
        if (membresia) {
            modalManager.show('Detalle de Membresía', `
                <div class="detalle-membresia">
                    <h4><i class="fas fa-id-card"></i> Membresía #${membresia.id}</h4>
                    <p><strong>Socio:</strong> ${membresia.socio} (${membresia.numero_socio})</p>
                    <p><strong>Tipo:</strong> ${membresia.tipo_membresia}</p>
                    <p><strong>Período:</strong> ${membresia.fecha_inicio} - ${membresia.fecha_fin}</p>
                    <p><strong>Precio Pagado:</strong> ${membresia.precio_pagado.toFixed(2)}€</p>
                    <p><strong>Estado:</strong> <span class="badge ${membresia.estado_vigencia === 'Vigente' ? 'badge-success' : 'badge-danger'}">${membresia.estado_vigencia}</span></p>
                    <div class="form-actions">
                        <button class="btn btn-outline" onclick="modalManager.close()">Cerrar</button>
                    </div>
                </div>
            `);
        }
    }
}

/**
 * Controlador de Asistencias
 */
class AsistenciasController {
    async cargarAsistencias() {
        const tbody = document.getElementById('tabla-asistencias');
        tbody.innerHTML = '<tr><td colspan="5" class="text-center">Cargando...</td></tr>';
        
        try {
            const response = await fetch(`${API_BASE}/asistencias/hoy`);
            const data = await response.json();
            
            if (data.success) {
                appState.datos.asistencias = data.data;
                this.renderizarAsistencias(data.data);
            }
        } catch (error) {
            console.error('Error al cargar asistencias:', error);
            tbody.innerHTML = '<tr><td colspan="5" class="text-center text-danger">Error al cargar asistencias</td></tr>';
        }
    }

    renderizarAsistencias(asistencias) {
        const tbody = document.getElementById('tabla-asistencias');
        tbody.innerHTML = '';

        if (asistencias.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">No hay asistencias registradas hoy</td></tr>';
            return;
        }

        asistencias.forEach(asistencia => {
            const row = tbody.insertRow();
            const estado = asistencia.salida ? 'Completado' : 'En gimnasio';
            const estadoBadge = asistencia.salida ? 'badge-success' : 'badge-warning';
            
            row.innerHTML = `
                <td><strong>${asistencia.numero_socio}</strong></td>
                <td>${asistencia.socio}</td>
                <td>${asistencia.entrada}</td>
                <td>${asistencia.salida || '-'}</td>
                <td><span class="badge ${estadoBadge}">${estado}</span></td>
            `;
        });
    }
}

/**
 * Controlador de Informes
 */
class InformesController {
    async cargarInformes() {
        this.generarReporteIngresos();
        this.generarReporteMembresias();
        this.generarReporteClases();
    }

    async generarReporteIngresos() {
        const container = document.getElementById('reporte-ingresos-mes');
        container.innerHTML = '<p class="loading">Cargando...</p>';
        
        try {
            const response = await fetch(`${API_BASE}/informes/ingresos-mes`);
            const data = await response.json();
            
            if (data.success && data.data.length > 0) {
                container.innerHTML = data.data.map(item => `
                    <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #e2e8f0;">
                        <span>${item.mes}</span>
                        <span><strong>${item.total_ingresos.toFixed(2)}€</strong> (${item.total_membresias} membresías)</span>
                    </div>
                `).join('');
            } else {
                container.innerHTML = '<p>No hay datos de ingresos</p>';
            }
        } catch (error) {
            container.innerHTML = '<p class="text-danger">Error al cargar datos</p>';
        }
    }

    async generarReporteMembresias() {
        const container = document.getElementById('reporte-membresias-vencer');
        container.innerHTML = '<p class="loading">Cargando...</p>';
        
        try {
            const response = await fetch(`${API_BASE}/informes/membresias-vencer`);
            const data = await response.json();
            
            if (data.success && data.data.length > 0) {
                container.innerHTML = data.data.map(membresia => `
                    <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #e2e8f0;">
                        <span>${membresia.socio}</span>
                        <span class="badge badge-warning">Vence: ${membresia.fecha_fin}</span>
                    </div>
                `).join('');
            } else {
                container.innerHTML = '<p class="text-success">No hay membresías próximas a vencer</p>';
            }
        } catch (error) {
            container.innerHTML = '<p class="text-danger">Error al cargar datos</p>';
        }
    }

    async generarReporteClases() {
        const container = document.getElementById('reporte-clases-populares');
        container.innerHTML = '<p class="loading">Cargando...</p>';
        
        try {
            const response = await fetch(`${API_BASE}/informes/clases-populares`);
            const data = await response.json();
            
            if (data.success && data.data.length > 0) {
                container.innerHTML = data.data.slice(0, 5).map(clase => `
                    <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #e2e8f0;">
                        <span>${clase.clase}</span>
                        <span class="badge badge-info">${clase.porcentaje_ocupacion}% ocupación</span>
                    </div>
                `).join('');
            } else {
                container.innerHTML = '<p>No hay datos de clases</p>';
            }
        } catch (error) {
            container.innerHTML = '<p class="text-danger">Error al cargar datos</p>';
        }
    }
}

/**
 * Gestor de Modales
 */
class ModalManager {
    show(title, content) {
        document.getElementById('modal-title').textContent = title;
        document.getElementById('modal-body').innerHTML = content;
        document.getElementById('modal-overlay').classList.add('active');
    }

    close() {
        document.getElementById('modal-overlay').classList.remove('active');
    }
}

/**
 * Gestor de Notificaciones
 */
class NotificationManager {
    show(message, type = 'info', duration = 3000) {
        // Crear elemento de notificación
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas ${this.getIcon(type)}"></i>
                <span>${message}</span>
            </div>
        `;

        // Agregar estilos si no existen
        if (!document.querySelector('#notification-styles')) {
            const styles = document.createElement('style');
            styles.id = 'notification-styles';
            styles.textContent = `
                .notification {
                    position: fixed;
                    top: 90px;
                    right: 20px;
                    background: white;
                    border-radius: 0.5rem;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    border: 1px solid #e2e8f0;
                    z-index: 3000;
                    animation: slideIn 0.3s ease;
                    min-width: 300px;
                }
                .notification-content {
                    display: flex;
                    align-items: center;
                    padding: 1rem;
                    gap: 0.5rem;
                }
                .notification-success { border-left: 4px solid #10b981; }
                .notification-warning { border-left: 4px solid #f59e0b; }
                .notification-error { border-left: 4px solid #ef4444; }
                .notification-info { border-left: 4px solid #3b82f6; }
                @keyframes slideIn {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
            `;
            document.head.appendChild(styles);
        }

        // Agregar al DOM
        document.body.appendChild(notification);

        // Eliminar después del tiempo especificado
        setTimeout(() => {
            notification.style.animation = 'slideIn 0.3s ease reverse';
            setTimeout(() => notification.remove(), 300);
        }, duration);
    }

    getIcon(type) {
        switch (type) {
            case 'success': return 'fa-check-circle';
            case 'warning': return 'fa-exclamation-triangle';
            case 'error': return 'fa-times-circle';
            default: return 'fa-info-circle';
        }
    }
}

// Instancias globales
const navigationManager = new NavigationManager();
const dashboardController = new DashboardController();
const sociosController = new SociosController();
const entrenadoresController = new EntrenadoresController();
const clasesController = new ClasesController();
const membresiasController = new MembresiasController();
const asistenciasController = new AsistenciasController();
const informesController = new InformesController();
const modalManager = new ModalManager();
const notificationManager = new NotificationManager();

// Funciones globales para los botones
function mostrarFormularioSocio() {
    notificationManager.show('Funcionalidad de nuevo socio en desarrollo', 'info');
}

function mostrarFormularioEntrenador() {
    notificationManager.show('Funcionalidad de nuevo entrenador en desarrollo', 'info');
}

function mostrarFormularioClase() {
    notificationManager.show('Funcionalidad de nueva clase en desarrollo', 'info');
}

function mostrarFormularioMembresia() {
    notificationManager.show('Funcionalidad de nueva membresía en desarrollo', 'info');
}

function registrarEntrada() {
    notificationManager.show('Funcionalidad de registro de entrada en desarrollo', 'info');
}

function generarReporteIngresos() {
    informesController.generarReporteIngresos();
}

function generarReporteMembresias() {
    informesController.generarReporteMembresias();
}

function generarReporteClases() {
    informesController.generarReporteClases();
}

function cerrarModal() {
    modalManager.close();
}

// Inicialización al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    console.log('🏋️ Sistema de Gestión de Gimnasio cargado');
    
    // Cargar datos iniciales del dashboard
    dashboardController.cargarDatos();
    
    // Event listener para cerrar modal al hacer clic fuera
    document.getElementById('modal-overlay').addEventListener('click', function(e) {
        if (e.target === this) {
            modalManager.close();
        }
    });
    
    // Mostrar notificación de bienvenida
    setTimeout(() => {
        notificationManager.show('Sistema de Gestión de Gimnasio cargado correctamente', 'success');
    }, 500);
});