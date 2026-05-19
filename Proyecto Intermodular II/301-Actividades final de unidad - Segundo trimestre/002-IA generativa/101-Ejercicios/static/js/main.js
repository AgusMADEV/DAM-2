// ========================================
// INMOWEB AI - JAVASCRIPT PRINCIPAL
// ========================================

document.addEventListener("DOMContentLoaded", () => {
    // Referencias del DOM
    const navItems = document.querySelectorAll(".nav-item");
    const views = document.querySelectorAll(".view");
    const form = document.getElementById("generator-form");
    const promptInput = document.getElementById("prompt");
    const tipoSelect = document.getElementById("tipo-propiedad");
    const precioSelect = document.getElementById("precio");
    const ubicacionInput = document.getElementById("ubicacion");
    const caracteristicasInput = document.getElementById("caracteristicas");
    const btnGenerate = document.getElementById("btn-generate");
    const statusMessage = document.getElementById("status-message");
    const formActions = document.getElementById("form-actions");
    const previewFrame = document.getElementById("preview-frame");
    
    // Botones de acciones
    const btnSave = document.getElementById("btn-save");
    const btnCopy = document.getElementById("btn-copy");
    const btnDownload = document.getElementById("btn-download");
    
    // Controles de dispositivo
    const deviceBtns = document.querySelectorAll(".device-btn");
    const iframeWrapper = document.querySelector(".iframe-wrapper");
    
    // Templates
    const templateCards = document.querySelectorAll(".template-card");
    const useTemplateButtons = document.querySelectorAll(".btn-use-template");
    
    // Modal
    const saveModal = document.getElementById("save-modal");
    const modalClose = document.getElementById("modal-close");
    const modalCancel = document.getElementById("modal-cancel");
    const modalSave = document.getElementById("modal-save");
    const proyectoNombreInput = document.getElementById("proyecto-nombre");
    const proyectoDescripcionInput = document.getElementById("proyecto-descripcion");
    
    // Estado
    let currentHTML = "";
    let totalGeneraciones = 0;
    let totalGuardados = 0;

    // ========================================
    // NAVEGACIÓN ENTRE VISTAS
    // ========================================
    
    navItems.forEach(item => {
        item.addEventListener("click", () => {
            const viewId = item.getAttribute("data-view");
            
            // Actualizar nav activo
            navItems.forEach(nav => nav.classList.remove("active"));
            item.classList.add("active");
            
            // Mostrar vista correspondiente
            views.forEach(view => view.classList.remove("active"));
            document.getElementById(`view-${viewId}`).classList.add("active");
            
            // Si es la vista de proyectos, cargarlos
            if (viewId === "proyectos") {
                loadProyectos();
            }
        });
    });

    // ========================================
    // PLANTILLAS PREDEFINIDAS
    // ========================================
    
    const templates = {
        luxury: {
            prompt: "Sitio web elegante para inmobiliaria de lujo con diseño sofisticado, galería de villas premium, filtros avanzados y formulario de contacto exclusivo",
            tipo: "villas",
            precio: "1M+",
            ubicacion: "Costa mediterránea",
            caracteristicas: "piscina infinita, vistas al mar, acabados de lujo, domótica"
        },
        modern: {
            prompt: "Landing page moderna y minimalista para agencia inmobiliaria, con hero impactante, grid de propiedades, sección de servicios y contacto",
            tipo: "mixto",
            precio: "300k-500k",
            ubicacion: "Centros urbanos",
            caracteristicas: "diseño contemporáneo, espacios abiertos, eficiencia energética"
        },
        vacation: {
            prompt: "Web atractiva para alquiler vacacional con calendario de disponibilidad, galería de fotos, mapa de ubicación y sistema de reservas",
            tipo: "apartamentos",
            precio: "150k-300k",
            ubicacion: "Zonas turísticas",
            caracteristicas: "cerca de la playa, piscina comunitaria, wifi, parking"
        },
        commercial: {
            prompt: "Sitio profesional para inmobiliaria comercial especializada en locales y oficinas, con búsqueda avanzada y tours virtuales",
            tipo: "locales",
            precio: "300k-500k",
            ubicacion: "Zonas comerciales",
            caracteristicas: "alto tránsito, escaparates amplios, accesibilidad"
        }
    };

    // Cargar template desde tarjetas rápidas
    templateCards.forEach(card => {
        card.addEventListener("click", () => {
            const templateId = card.getAttribute("data-template");
            loadTemplate(templateId);
        });
    });

    // Cargar template desde vista de plantillas
    useTemplateButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const templateId = btn.getAttribute("data-template");
            loadTemplate(templateId);
            
            // Cambiar a la vista del generador
            navItems.forEach(nav => nav.classList.remove("active"));
            navItems[0].classList.add("active");
            views.forEach(view => view.classList.remove("active"));
            views[0].classList.add("active");
        });
    });

    function loadTemplate(templateId) {
        const template = templates[templateId];
        if (!template) return;
        
        promptInput.value = template.prompt;
        tipoSelect.value = template.tipo;
        precioSelect.value = template.precio;
        ubicacionInput.value = template.ubicacion;
        caracteristicasInput.value = template.caracteristicas;
        
        showStatus("Plantilla cargada. Puedes personalizarla antes de generar.", "success");
    }

    // ========================================
    // GENERACIÓN DE PÁGINAS
    // ========================================
    
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        const prompt = promptInput.value.trim();
        const tipo = tipoSelect.value;
        const precio = precioSelect.value;
        const ubicacion = ubicacionInput.value.trim();
        const caracteristicas = caracteristicasInput.value.trim();
        
        if (!prompt) {
            showStatus("Por favor, describe el sitio web que deseas crear", "error");
            promptInput.focus();
            return;
        }
        
        if (prompt.length < 10) {
            showStatus("La descripción es muy corta. Sé más específico (mínimo 10 caracteres)", "error");
            promptInput.focus();
            return;
        }
        
        // Generar página
        await generatePage(prompt, tipo, precio, ubicacion, caracteristicas);
    });

    async function generatePage(prompt, tipo, precio, ubicacion, caracteristicas) {
        showStatus("⏳ Generando tu sitio web inmobiliario... Esto puede tardar unos segundos", "loading");
        setLoadingState(true);
        
        try {
            const response = await fetch(GENERATE_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    prompt,
                    tipo_propiedad: tipo,
                    precio,
                    ubicacion,
                    caracteristicas
                })
            });
            
            if (!response.ok) {
                const error = await response.json().catch(() => ({}));
                throw new Error(error.error || `Error HTTP ${response.status}`);
            }
            
            const data = await response.json();
            currentHTML = data.html || "<h1>No se recibió HTML</h1>";
            
            // Renderizar en iframe
            previewFrame.srcdoc = currentHTML;
            
            // Mostrar acciones
            formActions.hidden = false;
            
            // Actualizar estadísticas
            totalGeneraciones++;
            updateStats();
            
            showStatus("✅ ¡Sitio web generado correctamente! Revisa la vista previa.", "success");
        } catch (error) {
            console.error(error);
            showStatus(`❌ Error al generar: ${error.message}`, "error");
        } finally {
            setLoadingState(false);
        }
    }

    function showStatus(message, type) {
        statusMessage.textContent = message;
        statusMessage.className = `status-message show ${type}`;
        
        // Auto-ocultar mensajes de éxito después de 5 segundos
        if (type === "success") {
            setTimeout(() => {
                statusMessage.classList.remove("show");
            }, 5000);
        }
    }

    function setLoadingState(isLoading) {
        if (isLoading) {
            btnGenerate.disabled = true;
            const btnText = btnGenerate.querySelector(".btn-text");
            btnText.textContent = "Generando...";
        } else {
            btnGenerate.disabled = false;
            const btnText = btnGenerate.querySelector(".btn-text");
            btnText.textContent = "Generar Sitio Web";
        }
    }

    // ========================================
    // CONTROLES DE DISPOSITIVO
    // ========================================
    
    deviceBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            const device = btn.getAttribute("data-device");
            
            // Actualizar botón activo
            deviceBtns.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            
            // Cambiar clase del wrapper
            iframeWrapper.className = `iframe-wrapper ${device}`;
        });
    });

    // ========================================
    // ACCIONES: GUARDAR, COPIAR, DESCARGAR
    // ========================================
    
    btnSave.addEventListener("click", () => {
        if (!currentHTML) {
            showStatus("No hay contenido para guardar", "error");
            return;
        }
        
        // Abrir modal
        proyectoNombreInput.value = "";
        proyectoDescripcionInput.value = promptInput.value;
        saveModal.hidden = false;
    });

    btnCopy.addEventListener("click", async () => {
        if (!currentHTML) {
            showStatus("No hay contenido para copiar", "error");
            return;
        }
        
        try {
            await navigator.clipboard.writeText(currentHTML);
            showStatus("✅ HTML copiado al portapapeles", "success");
        } catch (error) {
            console.error(error);
            showStatus("❌ Error al copiar al portapapeles", "error");
        }
    });

    btnDownload.addEventListener("click", () => {
        if (!currentHTML) {
            showStatus("No hay contenido para descargar", "error");
            return;
        }
        
        const blob = new Blob([currentHTML], { type: "text/html" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `inmoweb-${Date.now()}.html`;
        a.click();
        URL.revokeObjectURL(url);
        
        showStatus("✅ Archivo descargado", "success");
    });

    // ========================================
    // MODAL: GUARDAR PROYECTO
    // ========================================
    
    modalClose.addEventListener("click", () => {
        saveModal.hidden = true;
    });

    modalCancel.addEventListener("click", () => {
        saveModal.hidden = true;
    });

    modalSave.addEventListener("click", async () => {
        const nombre = proyectoNombreInput.value.trim();
        
        if (!nombre) {
            alert("Por favor, ingresa un nombre para el proyecto");
            proyectoNombreInput.focus();
            return;
        }
        
        const descripcion = proyectoDescripcionInput.value.trim();
        const tipo = tipoSelect.value;
        const precio = precioSelect.value;
        const ubicacion = ubicacionInput.value.trim();
        const caracteristicas = caracteristicasInput.value.trim();
        
        try {
            const response = await fetch(SAVE_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    nombre,
                    descripcion,
                    tipo_propiedad: tipo,
                    precio,
                    ubicacion,
                    caracteristicas,
                    html: currentHTML
                })
            });
            
            if (!response.ok) {
                const error = await response.json().catch(() => ({}));
                throw new Error(error.error || `Error HTTP ${response.status}`);
            }
            
            const data = await response.json();
            
            // Cerrar modal
            saveModal.hidden = true;
            
            // Actualizar estadísticas
            totalGuardados++;
            updateStats();
            
            showStatus(`✅ Proyecto "${nombre}" guardado correctamente`, "success");
        } catch (error) {
            console.error(error);
            alert(`Error al guardar: ${error.message}`);
        }
    });

    // ========================================
    // PROYECTOS: LISTADO Y GESTIÓN
    // ========================================
    
    async function loadProyectos() {
        const proyectosList = document.getElementById("proyectos-list");
        proyectosList.innerHTML = '<p style="text-align:center; color: var(--gray-500);">Cargando proyectos...</p>';
        
        try {
            const response = await fetch(PROYECTOS_URL);
            
            if (!response.ok) {
                throw new Error(`Error HTTP ${response.status}`);
            }
            
            const data = await response.json();
            const proyectos = data.proyectos || [];
            
            if (proyectos.length === 0) {
                proyectosList.innerHTML = `
                    <div style="text-align: center; padding: 3rem; color: var(--gray-500);">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">📁</div>
                        <h3 style="margin-bottom: 0.5rem;">No hay proyectos guardados</h3>
                        <p>Los proyectos que guardes aparecerán aquí</p>
                    </div>
                `;
                return;
            }
            
            proyectosList.innerHTML = "";
            
            proyectos.forEach(proyecto => {
                const card = createProyectoCard(proyecto);
                proyectosList.appendChild(card);
            });
            
            // Actualizar contador
            document.getElementById("proyectos-count").textContent = proyectos.length;
            totalGuardados = proyectos.length;
            updateStats();
        } catch (error) {
            console.error(error);
            proyectosList.innerHTML = `
                <div style="text-align: center; padding: 2rem; color: var(--error);">
                    <p>❌ Error al cargar proyectos</p>
                    <p style="font-size: 0.875rem; margin-top: 0.5rem;">${error.message}</p>
                </div>
            `;
        }
    }

    function createProyectoCard(proyecto) {
        const card = document.createElement("div");
        card.className = "proyecto-card";
        
        const fecha = new Date(proyecto.fecha_creacion).toLocaleDateString("es-ES", {
            day: "2-digit",
            month: "short",
            year: "numeric"
        });
        
        card.innerHTML = `
            <div class="proyecto-preview">
                <div style="padding: 2rem; text-align: center; color: var(--gray-400); font-size: 3rem;">
                    🏠
                </div>
            </div>
            <div class="proyecto-info">
                <h3 class="proyecto-title">${proyecto.nombre}</h3>
                <div class="proyecto-meta">
                    <span>📅 ${fecha}</span>
                    ${proyecto.tipo_propiedad ? `<span>🏢 ${proyecto.tipo_propiedad}</span>` : ""}
                </div>
                ${proyecto.descripcion ? `<p style="font-size: 0.875rem; color: var(--gray-600); margin-bottom: 1rem;">${proyecto.descripcion}</p>` : ""}
                <div class="proyecto-actions">
                    <button class="btn-secondary" onclick="viewProyecto(${proyecto.id})" style="flex: 1;">
                        👁️ Ver
                    </button>
                    <button class="btn-secondary" onclick="exportProyecto(${proyecto.id})">
                        ⬇️
                    </button>
                    <button class="btn-secondary" onclick="deleteProyecto(${proyecto.id})">
                        🗑️
                    </button>
                </div>
            </div>
        `;
        
        return card;
    }

    // Funciones globales para los botones de proyecto
    window.viewProyecto = async function(id) {
        try {
            const response = await fetch(`/proyecto/${id}`);
            if (!response.ok) throw new Error(`Error HTTP ${response.status}`);
            
            const data = await response.json();
            const proyecto = data.proyecto;
            
            // Cargar en el generador
            promptInput.value = proyecto.descripcion || "";
            tipoSelect.value = proyecto.tipo_propiedad || "";
            precioSelect.value = proyecto.precio || "";
            ubicacionInput.value = proyecto.ubicacion || "";
            caracteristicasInput.value = proyecto.caracteristicas || "";
            currentHTML = proyecto.html_generado;
            
            // Renderizar
            previewFrame.srcdoc = currentHTML;
            formActions.hidden = false;
            
            // Cambiar a vista generador
            navItems.forEach(nav => nav.classList.remove("active"));
            navItems[0].classList.add("active");
            views.forEach(view => view.classList.remove("active"));
            views[0].classList.add("active");
            
            showStatus(`✅ Proyecto "${proyecto.nombre}" cargado`, "success");
        } catch (error) {
            alert(`Error al cargar proyecto: ${error.message}`);
        }
    };

    window.exportProyecto = function(id) {
        window.location.href = `/exportar/${id}`;
    };

    window.deleteProyecto = async function(id) {
        if (!confirm("¿Estás seguro de que deseas eliminar este proyecto?")) {
            return;
        }
        
        try {
            const response = await fetch(`/proyecto/${id}`, {
                method: "DELETE"
            });
            
            if (!response.ok) throw new Error(`Error HTTP ${response.status}`);
            
            // Recargar lista
            loadProyectos();
            showStatus("✅ Proyecto eliminado", "success");
        } catch (error) {
            alert(`Error al eliminar: ${error.message}`);
        }
    };

    // ========================================
    // ESTADÍSTICAS
    // ========================================
    
    function updateStats() {
        document.getElementById("total-generaciones").textContent = totalGeneraciones;
        document.getElementById("total-guardados").textContent = totalGuardados;
    }

    // ========================================
    // INICIALIZACIÓN
    // ========================================
    
    // Cargar proyectos al inicio para obtener el contador
    fetch(PROYECTOS_URL)
        .then(r => r.json())
        .then(data => {
            const count = data.proyectos?.length || 0;
            document.getElementById("proyectos-count").textContent = count;
            totalGuardados = count;
            updateStats();
        })
        .catch(err => console.error("Error al cargar contador de proyectos:", err));
});
