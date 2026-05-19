// =============================================
// TOTALKIT ERP - SISTEMA DE BÚSQUEDA PROFESIONAL
// JavaScript para búsqueda de productos con filtros
// =============================================

class BuscadorProductos {
    constructor() {
        this.filtros = {
            q: '',
            equipo: '',
            liga: '',
            marca: '',
            temporada: '',
            tipo: '',
            talla: '',
            precio_min: '',
            precio_max: '',
            solo_stock: false,
            destacados: false,
            es_seleccion: ''
        };
        
        this.orden = 'p.fecha_creacion';
        this.dir = 'DESC';
        this.pagina = 1;
        this.por_pagina = 12;
        
        this.timeoutBusqueda = null;
        this.vistaActual = 'grid'; // grid o lista
        
        this.init();
    }
    
    /**
     * Inicializar el buscador
     */
    init() {
        this.cargarOpcionesFiltros();
        this.configurarEventos();
        this.realizarBusqueda();
    }
    
    /**
     * Cargar opciones para los filtros (equipos, marcas, etc.)
     */
    async cargarOpcionesFiltros() {
        try {
            const response = await fetch('buscar_productos.php?accion=filtros');
            const data = await response.json();
            
            if (data.success) {
                this.llenarSelectFiltros(data.opciones);
            }
        } catch (error) {
            console.error('Error al cargar filtros:', error);
        }
    }
    
    /**
     * Llenar los selectores con opciones
     */
    llenarSelectFiltros(opciones) {
        // Equipos
        const selectEquipo = document.getElementById('filtro-equipo');
        if (selectEquipo && opciones.equipos) {
            selectEquipo.innerHTML = '<option value="">Todos los equipos</option>';
            opciones.equipos.forEach(equipo => {
                const icono = equipo.es_seleccion == 1 ? '🌍' : '⚽';
                selectEquipo.innerHTML += `<option value="${equipo.id_equipo}">${icono} ${equipo.nombre_equipo}</option>`;
            });
        }
        
        // Ligas
        const selectLiga = document.getElementById('filtro-liga');
        if (selectLiga && opciones.ligas) {
            selectLiga.innerHTML = '<option value="">Todas las ligas</option>';
            opciones.ligas.forEach(liga => {
                selectLiga.innerHTML += `<option value="${liga.id_liga}">${liga.nombre_liga}</option>`;
            });
        }
        
        // Marcas
        const selectMarca = document.getElementById('filtro-marca');
        if (selectMarca && opciones.marcas) {
            selectMarca.innerHTML = '<option value="">Todas las marcas</option>';
            opciones.marcas.forEach(marca => {
                selectMarca.innerHTML += `<option value="${marca.id_marca}">${marca.nombre_marca}</option>`;
            });
        }
        
        // Temporadas
        const selectTemporada = document.getElementById('filtro-temporada');
        if (selectTemporada && opciones.temporadas) {
            selectTemporada.innerHTML = '<option value="">Todas las temporadas</option>';
            opciones.temporadas.forEach(temp => {
                selectTemporada.innerHTML += `<option value="${temp.id_temporada}">${temp.nombre_temporada}</option>`;
            });
        }
        
        // Tipos de camiseta
        const selectTipo = document.getElementById('filtro-tipo');
        if (selectTipo && opciones.tipos) {
            selectTipo.innerHTML = '<option value="">Todos los tipos</option>';
            opciones.tipos.forEach(tipo => {
                selectTipo.innerHTML += `<option value="${tipo.id_tipo_camiseta}">${tipo.nombre_tipo}</option>`;
            });
        }
        
        // Tallas
        const selectTalla = document.getElementById('filtro-talla');
        if (selectTalla && opciones.tallas) {
            selectTalla.innerHTML = '<option value="">Todas las tallas</option>';
            opciones.tallas.forEach(talla => {
                selectTalla.innerHTML += `<option value="${talla.id_talla}">${talla.nombre_talla}</option>`;
            });
        }
        
        // Rango de precios
        const inputPrecioMin = document.getElementById('filtro-precio-min');
        const inputPrecioMax = document.getElementById('filtro-precio-max');
        if (inputPrecioMin && opciones.precio_min !== undefined) {
            inputPrecioMin.placeholder = `Desde ${opciones.precio_min.toFixed(2)}€`;
        }
        if (inputPrecioMax && opciones.precio_max !== undefined) {
            inputPrecioMax.placeholder = `Hasta ${opciones.precio_max.toFixed(2)}€`;
        }
    }
    
    /**
     * Configurar eventos de los controles
     */
    configurarEventos() {
        // Búsqueda de texto
        const inputBusqueda = document.getElementById('busqueda-texto');
        if (inputBusqueda) {
            inputBusqueda.addEventListener('input', (e) => {
                this.filtros.q = e.target.value;
                this.busquedaConDelay();
            });
        }
        
        // Todos los filtros select
        const filtrosSelect = [
            'filtro-equipo', 'filtro-liga', 'filtro-marca',
            'filtro-temporada', 'filtro-tipo', 'filtro-talla'
        ];
        
        filtrosSelect.forEach(id => {
            const elemento = document.getElementById(id);
            if (elemento) {
                elemento.addEventListener('change', (e) => {
                    const campo = id.replace('filtro-', '');
                    this.filtros[campo] = e.target.value;
                    this.pagina = 1;
                    this.realizarBusqueda();
                });
            }
        });
        
        // Filtros de precio
        const inputPrecioMin = document.getElementById('filtro-precio-min');
        const inputPrecioMax = document.getElementById('filtro-precio-max');
        
        if (inputPrecioMin) {
            inputPrecioMin.addEventListener('change', (e) => {
                this.filtros.precio_min = e.target.value;
                this.pagina = 1;
                this.realizarBusqueda();
            });
        }
        
        if (inputPrecioMax) {
            inputPrecioMax.addEventListener('change', (e) => {
                this.filtros.precio_max = e.target.value;
                this.pagina = 1;
                this.realizarBusqueda();
            });
        }
        
        // Checkboxes
        const checkSoloStock = document.getElementById('filtro-solo-stock');
        const checkDestacados = document.getElementById('filtro-destacados');
        
        if (checkSoloStock) {
            checkSoloStock.addEventListener('change', (e) => {
                this.filtros.solo_stock = e.target.checked;
                this.pagina = 1;
                this.realizarBusqueda();
            });
        }
        
        if (checkDestacados) {
            checkDestacados.addEventListener('change', (e) => {
                this.filtros.destacados = e.target.checked;
                this.pagina = 1;
                this.realizarBusqueda();
            });
        }
        
        // Radio buttons para tipo de equipo
        const radiosSeleccion = document.getElementsByName('tipo-equipo');
        radiosSeleccion.forEach(radio => {
            radio.addEventListener('change', (e) => {
                this.filtros.es_seleccion = e.target.value;
                this.pagina = 1;
                this.realizarBusqueda();
            });
        });
        
        // Botón limpiar filtros
        const btnLimpiar = document.getElementById('btn-limpiar-filtros');
        if (btnLimpiar) {
            btnLimpiar.addEventListener('click', () => {
                this.limpiarFiltros();
            });
        }
        
        // Cambio de vista
        const btnVistaGrid = document.getElementById('btn-vista-grid');
        const btnVistaLista = document.getElementById('btn-vista-lista');
        
        if (btnVistaGrid) {
            btnVistaGrid.addEventListener('click', () => {
                this.cambiarVista('grid');
            });
        }
        
        if (btnVistaLista) {
            btnVistaLista.addEventListener('click', () => {
                this.cambiarVista('lista');
            });
        }
        
        // Ordenamiento
        const selectOrden = document.getElementById('select-orden');
        if (selectOrden) {
            selectOrden.addEventListener('change', (e) => {
                const valor = e.target.value.split('|');
                this.orden = valor[0];
                this.dir = valor[1] || 'DESC';
                this.realizarBusqueda();
            });
        }
    }
    
    /**
     * Búsqueda con delay (para texto)
     */
    busquedaConDelay() {
        if (this.timeoutBusqueda) {
            clearTimeout(this.timeoutBusqueda);
        }
        
        this.timeoutBusqueda = setTimeout(() => {
            this.pagina = 1;
            this.realizarBusqueda();
        }, 300);
    }
    
    /**
     * Realizar búsqueda principal
     */
    async realizarBusqueda() {
        const contenedorResultados = document.getElementById('resultados-busqueda');
        if (!contenedorResultados) return;
        
        // Mostrar indicador de carga
        contenedorResultados.innerHTML = `
            <div class="loading-search">
                <div class="spinner"></div>
                <p>Buscando productos...</p>
            </div>
        `;
        
        try {
            const params = new URLSearchParams({
                accion: 'buscar',
                ...this.filtros,
                orden: this.orden,
                dir: this.dir,
                pagina: this.pagina,
                por_pagina: this.por_pagina
            });
            
            // Eliminar parámetros vacíos
            for (let [key, value] of params.entries()) {
                if (value === '' || value === 'false') {
                    params.delete(key);
                }
            }
            
            const response = await fetch(`buscar_productos.php?${params.toString()}`);
            const data = await response.json();
            
            if (data.success) {
                this.mostrarResultados(data);
            } else {
                contenedorResultados.innerHTML = `
                    <div class="error-search">
                        <p>❌ Error: ${data.error || 'Error desconocido'}</p>
                    </div>
                `;
            }
        } catch (error) {
            console.error('Error en la búsqueda:', error);
            contenedorResultados.innerHTML = `
                <div class="error-search">
                    <p>❌ Error al realizar la búsqueda</p>
                </div>
            `;
        }
    }
    
    /**
     * Mostrar resultados de la búsqueda
     */
    mostrarResultados(data) {
        const contenedorResultados = document.getElementById('resultados-busqueda');
        const contenedorEstadisticas = document.getElementById('estadisticas-busqueda');
        
        // Actualizar estadísticas
        if (contenedorEstadisticas && data.estadisticas) {
            const stats = data.estadisticas;
            contenedorEstadisticas.innerHTML = `
                <div class="stat-item">
                    <span class="stat-icon">📦</span>
                    <span class="stat-label">Productos:</span>
                    <span class="stat-value">${stats.total}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-icon">💰</span>
                    <span class="stat-label">Precio promedio:</span>
                    <span class="stat-value">${stats.precio_promedio.toFixed(2)}€</span>
                </div>
                <div class="stat-item">
                    <span class="stat-icon">📊</span>
                    <span class="stat-label">Stock total:</span>
                    <span class="stat-value">${stats.stock_total}</span>
                </div>
            `;
        }
        
        // Mostrar productos
        if (data.productos.length === 0) {
            contenedorResultados.innerHTML = `
                <div class="no-results">
                    <div class="no-results-icon">🔍</div>
                    <h3>No se encontraron productos</h3>
                    <p>Intenta ajustar los filtros de búsqueda</p>
                </div>
            `;
            return;
        }
        
        const htmlProductos = data.productos.map(p => this.renderProducto(p)).join('');
        
        contenedorResultados.innerHTML = `
            <div class="productos-grid vista-${this.vistaActual}">
                ${htmlProductos}
            </div>
        `;
        
        // Mostrar paginación
        if (data.total_paginas > 1) {
            contenedorResultados.innerHTML += this.renderPaginacion(data);
        }
    }
    
    /**
     * Renderizar un producto
     */
    renderProducto(producto) {
        const stockClass = producto.stock > 10 ? 'stock-alto' : (producto.stock > 0 ? 'stock-medio' : 'stock-bajo');
        const stockTexto = producto.stock > 0 ? `${producto.stock} disponibles` : 'Sin stock';
        const destacado = producto.destacado == 1 ? '<span class="badge-destacado">⭐ Destacado</span>' : '';
        const tipoEquipo = producto.es_seleccion == 1 ? '🌍 Selección' : '⚽ Club';
        const jugadorInfo = producto.jugador ? `<div class="producto-jugador">👤 ${producto.jugador} ${producto.numero_dorsal ? '#' + producto.numero_dorsal : ''}</div>` : '';
        
        return `
            <div class="producto-card">
                <div class="producto-header">
                    ${destacado}
                    <span class="badge-tipo">${tipoEquipo}</span>
                </div>
                <div class="producto-body">
                    <h3 class="producto-nombre">${this.resaltarTexto(producto.nombre_producto)}</h3>
                    <div class="producto-equipo">${this.resaltarTexto(producto.nombre_equipo)}</div>
                    ${jugadorInfo}
                    <div class="producto-detalles">
                        <span class="detalle-item">🏷️ ${producto.tipo_camiseta}</span>
                        <span class="detalle-item">📏 ${producto.nombre_talla}</span>
                        <span class="detalle-item">📅 ${producto.nombre_temporada}</span>
                    </div>
                    <div class="producto-marca">Por ${producto.nombre_marca}</div>
                </div>
                <div class="producto-footer">
                    <div class="producto-precio">
                        <span class="precio-valor">${parseFloat(producto.precio).toFixed(2)}€</span>
                    </div>
                    <div class="producto-stock ${stockClass}">
                        ${stockTexto}
                    </div>
                </div>
                <div class="producto-acciones">
                    <button class="btn-ver-detalle" onclick="verDetalleProducto(${producto.id_producto})">
                        👁️ Ver detalle
                    </button>
                </div>
            </div>
        `;
    }
    
    /**
     * Resaltar texto de búsqueda en resultados
     */
    resaltarTexto(texto) {
        if (!this.filtros.q || this.filtros.q.length < 2) {
            return texto;
        }
        
        const regex = new RegExp(`(${this.filtros.q})`, 'gi');
        return texto.replace(regex, '<mark>$1</mark>');
    }
    
    /**
     * Renderizar paginación
     */
    renderPaginacion(data) {
        let html = '<div class="paginacion">';
        
        // Botón anterior
        if (this.pagina > 1) {
            html += `<button class="btn-paginacion" onclick="buscador.irAPagina(${this.pagina - 1})">« Anterior</button>`;
        }
        
        // Páginas
        const inicio = Math.max(1, this.pagina - 2);
        const fin = Math.min(data.total_paginas, this.pagina + 2);
        
        if (inicio > 1) {
            html += `<button class="btn-paginacion" onclick="buscador.irAPagina(1)">1</button>`;
            if (inicio > 2) {
                html += `<span class="paginacion-ellipsis">...</span>`;
            }
        }
        
        for (let i = inicio; i <= fin; i++) {
            const activeClass = i === this.pagina ? 'active' : '';
            html += `<button class="btn-paginacion ${activeClass}" onclick="buscador.irAPagina(${i})">${i}</button>`;
        }
        
        if (fin < data.total_paginas) {
            if (fin < data.total_paginas - 1) {
                html += `<span class="paginacion-ellipsis">...</span>`;
            }
            html += `<button class="btn-paginacion" onclick="buscador.irAPagina(${data.total_paginas})">${data.total_paginas}</button>`;
        }
        
        // Botón siguiente
        if (this.pagina < data.total_paginas) {
            html += `<button class="btn-paginacion" onclick="buscador.irAPagina(${this.pagina + 1})">Siguiente »</button>`;
        }
        
        html += '</div>';
        
        // Info de paginación
        const desde = (this.pagina - 1) * this.por_pagina + 1;
        const hasta = Math.min(this.pagina * this.por_pagina, data.total_resultados);
        
        html += `
            <div class="paginacion-info">
                Mostrando ${desde}-${hasta} de ${data.total_resultados} productos
            </div>
        `;
        
        return html;
    }
    
    /**
     * Ir a una página específica
     */
    irAPagina(pagina) {
        this.pagina = pagina;
        this.realizarBusqueda();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    /**
     * Cambiar vista (grid/lista)
     */
    cambiarVista(vista) {
        this.vistaActual = vista;
        
        const btnGrid = document.getElementById('btn-vista-grid');
        const btnLista = document.getElementById('btn-vista-lista');
        
        if (btnGrid && btnLista) {
            btnGrid.classList.toggle('active', vista === 'grid');
            btnLista.classList.toggle('active', vista === 'lista');
        }
        
        const contenedorGrid = document.querySelector('.productos-grid');
        if (contenedorGrid) {
            contenedorGrid.className = `productos-grid vista-${vista}`;
        }
    }
    
    /**
     * Limpiar todos los filtros
     */
    limpiarFiltros() {
        // Resetear objeto de filtros
        this.filtros = {
            q: '',
            equipo: '',
            liga: '',
            marca: '',
            temporada: '',
            tipo: '',
            talla: '',
            precio_min: '',
            precio_max: '',
            solo_stock: false,
            destacados: false,
            es_seleccion: ''
        };
        
        // Limpiar inputs de texto
        const inputBusqueda = document.getElementById('busqueda-texto');
        if (inputBusqueda) inputBusqueda.value = '';
        
        const inputPrecioMin = document.getElementById('filtro-precio-min');
        if (inputPrecioMin) inputPrecioMin.value = '';
        
        const inputPrecioMax = document.getElementById('filtro-precio-max');
        if (inputPrecioMax) inputPrecioMax.value = '';
        
        // Limpiar selects
        document.querySelectorAll('.filtros-container select').forEach(select => {
            select.selectedIndex = 0;
        });
        
        // Limpiar checkboxes
        const checkSoloStock = document.getElementById('filtro-solo-stock');
        const checkDestacados = document.getElementById('filtro-destacados');
        if (checkSoloStock) checkSoloStock.checked = false;
        if (checkDestacados) checkDestacados.checked = false;
        
        // Limpiar radios
        const radioTodos = document.getElementById('radio-todos-equipos');
        if (radioTodos) radioTodos.checked = true;
        
        this.pagina = 1;
        this.realizarBusqueda();
    }
}

// =============================================
// FUNCIONES AUXILIARES
// =============================================

/**
 * Ver detalle de producto (modal o página)
 */
function verDetalleProducto(idProducto) {
    alert(`Ver detalle del producto ${idProducto}\n\nAquí puedes implementar un modal con la información completa del producto.`);
}

/**
 * Inicializar buscador cuando se carga la página
 */
let buscador;

document.addEventListener('DOMContentLoaded', () => {
    // Solo inicializar si estamos en la página de búsqueda
    if (document.getElementById('busqueda-texto')) {
        buscador = new BuscadorProductos();
    }
});
