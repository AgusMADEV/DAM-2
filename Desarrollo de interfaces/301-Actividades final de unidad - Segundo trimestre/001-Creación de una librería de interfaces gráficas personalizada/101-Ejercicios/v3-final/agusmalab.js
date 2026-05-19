/*!
 * AgusmaLab - Librería de Componentes UI v3.0 (Premium)
 * Con Glassmorphism, Iconos SVG, Animaciones y Tipografía Mejorada
 * Búsqueda, Ordenamiento, Paginación y Gráficos
 * Autor: Agust�n Mateo
 * Fecha: 17 de febrero de 2026
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.AgusmaLab = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  /* ========================================
     UTILIDADES
     ======================================== */
  
  const crearElemento = (tag, className = '', content = '') => {
    const elemento = document.createElement(tag);
    if (className) elemento.className = className;
    if (content) elemento.textContent = content;
    return elemento;
  };

  const obtenerElemento = (selector) => {
    return typeof selector === 'string' ? document.querySelector(selector) : selector;
  };

  const normalizar = (str) => {
    return str.normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase();
  };

  /* ========================================
     ICONOS SVG PROFESIONALES
     ======================================== */
  const Iconos = {
    usuarios: `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
        <circle cx="9" cy="7" r="4"></circle>
        <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
        <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
      </svg>
    `,
    dinero: `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="12" y1="1" x2="12" y2="23"></line>
        <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
      </svg>
    `,
    pedidos: `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
        <polyline points="14 2 14 8 20 8"></polyline>
        <line x1="16" y1="13" x2="8" y2="13"></line>
        <line x1="16" y1="17" x2="8" y2="17"></line>
        <polyline points="10 9 9 9 8 9"></polyline>
      </svg>
    `,
    estadisticas: `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="18" y1="20" x2="18" y2="10"></line>
        <line x1="12" y1="20" x2="12" y2="4"></line>
        <line x1="6" y1="20" x2="6" y2="14"></line>
      </svg>
    `,
    tendencia: `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>
        <polyline points="17 6 23 6 23 12"></polyline>
      </svg>
    `,
    productos: `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
        <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
        <line x1="12" y1="22.08" x2="12" y2="12"></line>
      </svg>
    `,
    ventas: `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="9" cy="21" r="1"></circle>
        <circle cx="20" cy="21" r="1"></circle>
        <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
      </svg>
    `,
    objetivo: `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <circle cx="12" cy="12" r="6"></circle>
        <circle cx="12" cy="12" r="2"></circle>
      </svg>
    `
  };

  const obtenerIconoSVG = (nombreIcono) => {
    return Iconos[nombreIcono] || Iconos.estadisticas;
  };

  /* ========================================
     COMPONENTE: StatsCard (Premium con SVG)
     ======================================== */
  class StatsCard {
    constructor(contenedor, opciones = {}) {
      this.contenedor = obtenerElemento(contenedor);
      
      if (!this.contenedor) {
        throw new Error('AgusmaLab.StatsCard: contenedor no encontrado');
      }

      this.opciones = {
        titulo: opciones.titulo || 'Estadística',
        valor: opciones.valor || '0',
        icono: opciones.icono || 'estadisticas',
        colorIcono: opciones.colorIcono || 'primary',
        descripcion: opciones.descripcion || '',
        cambio: opciones.cambio || null,
        tipoCambio: opciones.tipoCambio || 'neutral',
        ...opciones
      };

      this.renderizar();
    }

    renderizar() {
      this.contenedor.innerHTML = '';
      this.contenedor.className = 'agl-container agl-animate-in';

      const tarjeta = crearElemento('div', 'agl-stats-card');

      // Header
      const header = crearElemento('div', 'agl-stats-card-header');
      const titulo = crearElemento('div', 'agl-stats-card-title', this.opciones.titulo);
      
      // Icono SVG
      const icono = document.createElement('div');
      icono.className = `agl-stats-card-icon ${this.opciones.colorIcono}`;
      icono.innerHTML = obtenerIconoSVG(this.opciones.icono);
      
      header.appendChild(titulo);
      header.appendChild(icono);
      tarjeta.appendChild(header);

      // Valor
      const valor = crearElemento('div', 'agl-stats-card-value', this.opciones.valor);
      tarjeta.appendChild(valor);

      // Footer
      if (this.opciones.descripcion || this.opciones.cambio) {
        const footer = crearElemento('div', 'agl-stats-card-footer');
        
        if (this.opciones.descripcion) {
          const desc = crearElemento('div', 'agl-stats-card-description', this.opciones.descripcion);
          footer.appendChild(desc);
        }
        
        if (this.opciones.cambio) {
          const cambio = crearElemento('div', `agl-stats-card-change ${this.opciones.tipoCambio}`, this.opciones.cambio);
          footer.appendChild(cambio);
        }
        
        tarjeta.appendChild(footer);
      }

      this.contenedor.appendChild(tarjeta);
      
      // Guardar referencias
      this.elementoValor = valor;
      this.elementoCambio = this.contenedor.querySelector('.agl-stats-card-change');
    }

    actualizarValor(nuevoValor, animar = true) {
      this.opciones.valor = nuevoValor;
      if (this.elementoValor) {
        if (animar) {
          this.elementoValor.classList.add('animating');
          setTimeout(() => this.elementoValor.classList.remove('animating'), 400);
        }
        this.elementoValor.textContent = nuevoValor;
      }
    }

    mostrarCambio(cambio, tipo = 'neutral') {
      this.opciones.cambio = cambio;
      this.opciones.tipoCambio = tipo;
      
      if (this.elementoCambio) {
        this.elementoCambio.textContent = cambio;
        this.elementoCambio.className = `agl-stats-card-change ${tipo}`;
      } else {
        this.renderizar();
      }
    }
  }

  /* ========================================
     COMPONENTE: DataTable (Mejorada)
     ======================================== */
  class DataTable {
    constructor(contenedor, opciones = {}) {
      this.contenedor = obtenerElemento(contenedor);
      
      if (!this.contenedor) {
        throw new Error('AgusmaLab.DataTable: contenedor no encontrado');
      }

      this.opciones = {
        titulo: opciones.titulo || 'Tabla de Datos',
        columnas: opciones.columnas || [],
        datos: opciones.datos || [],
        busqueda: opciones.busqueda !== false,
        ordenamiento: opciones.ordenamiento !== false,
        paginacion: opciones.paginacion !== false,
        filasPorPagina: opciones.filasPorPagina || 10,
        ...opciones
      };

      this.paginaActual = 1;
      this.columnaOrden = null;
      this.direccionOrden = 'asc';
      this.terminoBusqueda = '';
      this.datosFiltrados = [...this.opciones.datos];

      this.renderizar();
    }

    renderizar() {
      this.contenedor.innerHTML = '';
      this.contenedor.className = 'agl-container';

      const wrapper = crearElemento('div', 'agl-table-wrapper');

      // Header con título y búsqueda
      const header = crearElemento('div', 'agl-table-header');
      const titulo = crearElemento('h3', 'agl-table-title', this.opciones.titulo);
      header.appendChild(titulo);

      if (this.opciones.busqueda) {
        this.inputBusqueda = crearElemento('input', 'agl-table-search');
        this.inputBusqueda.type = 'search';
        this.inputBusqueda.placeholder = 'Buscar...';
        this.inputBusqueda.value = this.terminoBusqueda;
        header.appendChild(this.inputBusqueda);
      }

      wrapper.appendChild(header);

      // Tabla
      const tabla = crearElemento('table', 'agl-table');
      
      // Thead
      const thead = document.createElement('thead');
      const filaHeader = document.createElement('tr');
      
      this.opciones.columnas.forEach((col, index) => {
        const campo = col.campo || col;
        const etiqueta = col.etiqueta || col;
        const ordenable = col.ordenable !== false && this.opciones.ordenamiento;
        
        const th = crearElemento('th', '', etiqueta);
        
        if (ordenable) {
          th.classList.add('sortable');
          th.dataset.campo = campo;
          
          if (this.columnaOrden === campo) {
            th.classList.add(this.direccionOrden === 'asc' ? 'sorted-asc' : 'sorted-desc');
          }
        }
        
        filaHeader.appendChild(th);
      });
      
      thead.appendChild(filaHeader);
      tabla.appendChild(thead);

      // Tbody
      const tbody = document.createElement('tbody');
      const datosPaginados = this._obtenerDatosPaginados();
      
      if (datosPaginados.length === 0) {
        const filaVacia = document.createElement('tr');
        const celdaVacia = crearElemento('td', '', 'No hay datos para mostrar');
        celdaVacia.colSpan = this.opciones.columnas.length;
        celdaVacia.style.textAlign = 'center';
        celdaVacia.style.padding = '2rem';
        celdaVacia.style.color = 'var(--agl-text-muted)';
        filaVacia.appendChild(celdaVacia);
        tbody.appendChild(filaVacia);
      } else {
        datosPaginados.forEach(fila => {
          const tr = document.createElement('tr');
          
          this.opciones.columnas.forEach(col => {
            const campo = col.campo || col;
            const td = crearElemento('td');
            
            // Si la fila es un array, usar índice
            const valor = Array.isArray(fila) ? 
              fila[this.opciones.columnas.indexOf(col)] : 
              fila[campo];
            
            td.textContent = valor !== null && valor !== undefined ? valor : '';
            tr.appendChild(td);
          });
          
          tbody.appendChild(tr);
        });
      }
      
      tabla.appendChild(tbody);
      wrapper.appendChild(tabla);

      // Footer con paginación
      if (this.opciones.paginacion) {
        this._renderizarPaginacion(wrapper);
      }

      this.contenedor.appendChild(wrapper);
      
      // Guardar referencias para actualizaciones parciales
      this.wrapper = wrapper;
      this.tabla = tabla;
      
      this._adjuntarEventos();
    }

    _actualizarContenido() {
      // Actualizar solo tbody y footer sin tocar el header
      if (!this.tabla) return;
      
      // Actualizar tbody
      const tbody = this.tabla.querySelector('tbody');
      if (tbody) {
        tbody.innerHTML = '';
        const datosPaginados = this._obtenerDatosPaginados();
        
        if (datosPaginados.length === 0) {
          const filaVacia = document.createElement('tr');
          const celdaVacia = crearElemento('td', '', 'No hay datos para mostrar');
          celdaVacia.colSpan = this.opciones.columnas.length;
          celdaVacia.style.textAlign = 'center';
          celdaVacia.style.padding = '2rem';
          celdaVacia.style.color = 'var(--agl-text-muted)';
          filaVacia.appendChild(celdaVacia);
          tbody.appendChild(filaVacia);
        } else {
          datosPaginados.forEach(fila => {
            const tr = document.createElement('tr');
            
            this.opciones.columnas.forEach(col => {
              const campo = col.campo || col;
              const td = crearElemento('td');
              
              const valor = Array.isArray(fila) ? 
                fila[this.opciones.columnas.indexOf(col)] : 
                fila[campo];
              
              td.textContent = valor !== null && valor !== undefined ? valor : '';
              tr.appendChild(td);
            });
            
            tbody.appendChild(tr);
          });
        }
      }
      
      // Actualizar thead (para indicadores de ordenamiento)
      const headers = this.tabla.querySelectorAll('th.sortable');
      headers.forEach(th => {
        th.classList.remove('sorted-asc', 'sorted-desc');
        const campo = th.dataset.campo;
        if (this.columnaOrden === campo) {
          th.classList.add(this.direccionOrden === 'asc' ? 'sorted-asc' : 'sorted-desc');
        }
      });
      
      // Actualizar footer de paginación
      if (this.opciones.paginacion) {
        const footerAntiguo = this.wrapper.querySelector('.agl-table-footer');
        if (footerAntiguo) {
          footerAntiguo.remove();
        }
        this._renderizarPaginacion(this.wrapper);
        this._adjuntarEventosPaginacion();
      }
    }

    _renderizarPaginacion(wrapper) {
      const footer = crearElemento('div', 'agl-table-footer');
      
      // Info
      const totalFilas = this.datosFiltrados.length;
      const inicio = (this.paginaActual - 1) * this.opciones.filasPorPagina + 1;
      const fin = Math.min(this.paginaActual * this.opciones.filasPorPagina, totalFilas);
      const info = crearElemento('div', 'agl-table-info', 
        `Mostrando ${inicio}-${fin} de ${totalFilas} registros`);
      footer.appendChild(info);

      // Paginación
      const paginacion = crearElemento('div', 'agl-table-pagination');
      const totalPaginas = Math.ceil(totalFilas / this.opciones.filasPorPagina);

      // Botón anterior
      const btnAnterior = crearElemento('button', '', '← Anterior');
      btnAnterior.disabled = this.paginaActual === 1;
      paginacion.appendChild(btnAnterior);

      // Números de página
      const maxPaginasVisibles = 5;
      let paginaInicio = Math.max(1, this.paginaActual - Math.floor(maxPaginasVisibles / 2));
      let paginaFin = Math.min(totalPaginas, paginaInicio + maxPaginasVisibles - 1);
      
      if (paginaFin - paginaInicio < maxPaginasVisibles - 1) {
        paginaInicio = Math.max(1, paginaFin - maxPaginasVisibles + 1);
      }

      for (let i = paginaInicio; i <= paginaFin; i++) {
        const btnPagina = crearElemento('button', '', i.toString());
        if (i === this.paginaActual) {
          btnPagina.classList.add('active');
        }
        btnPagina.dataset.pagina = i;
        paginacion.appendChild(btnPagina);
      }

      // Botón siguiente
      const btnSiguiente = crearElemento('button', '', 'Siguiente →');
      btnSiguiente.disabled = this.paginaActual === totalPaginas || totalPaginas === 0;
      paginacion.appendChild(btnSiguiente);

      footer.appendChild(paginacion);
      wrapper.appendChild(footer);
    }

    _adjuntarEventos() {
      // Búsqueda
      if (this.inputBusqueda) {
        this.inputBusqueda.addEventListener('input', (e) => {
          this.terminoBusqueda = e.target.value;
          this._filtrarDatos();
          this.paginaActual = 1;
          this._actualizarContenido();
        });
      }

      // Ordenamiento
      const headers = this.contenedor.querySelectorAll('th.sortable');
      headers.forEach(th => {
        th.addEventListener('click', () => {
          const campo = th.dataset.campo;
          if (this.columnaOrden === campo) {
            this.direccionOrden = this.direccionOrden === 'asc' ? 'desc' : 'asc';
          } else {
            this.columnaOrden = campo;
            this.direccionOrden = 'asc';
          }
          this._ordenarDatos();
          this._actualizarContenido();
        });
      });

      this._adjuntarEventosPaginacion();
    }

    _adjuntarEventosPaginacion() {
      // Paginación
      const btnAnterior = this.contenedor.querySelector('.agl-table-pagination button:first-child');
      const btnSiguiente = this.contenedor.querySelector('.agl-table-pagination button:last-child');
      const btnsPagina = this.contenedor.querySelectorAll('.agl-table-pagination button[data-pagina]');

      if (btnAnterior) {
        btnAnterior.addEventListener('click', () => this.paginaAnterior());
      }

      if (btnSiguiente) {
        btnSiguiente.addEventListener('click', () => this.paginaSiguiente());
      }

      btnsPagina.forEach(btn => {
        btn.addEventListener('click', () => {
          this.irAPagina(parseInt(btn.dataset.pagina));
        });
      });
    }

    _filtrarDatos() {
      if (!this.terminoBusqueda) {
        this.datosFiltrados = [...this.opciones.datos];
        return;
      }

      const termino = normalizar(this.terminoBusqueda);
      this.datosFiltrados = this.opciones.datos.filter(fila => {
        return this.opciones.columnas.some((col, index) => {
          const valor = Array.isArray(fila) ? fila[index] : fila[col.campo || col];
          if (valor === null || valor === undefined) return false;
          return normalizar(String(valor)).includes(termino);
        });
      });
    }

    _ordenarDatos() {
      if (!this.columnaOrden) return;

      const indiceColumna = this.opciones.columnas.findIndex(col => 
        (col.campo || col) === this.columnaOrden
      );

      this.datosFiltrados.sort((a, b) => {
        const valorA = Array.isArray(a) ? a[indiceColumna] : a[this.columnaOrden];
        const valorB = Array.isArray(b) ? b[indiceColumna] : b[this.columnaOrden];
        
        if (valorA === null || valorA === undefined) return 1;
        if (valorB === null || valorB === undefined) return -1;
        
        let comparacion = 0;
        if (typeof valorA === 'number' && typeof valorB === 'number') {
          comparacion = valorA - valorB;
        } else {
          comparacion = String(valorA).localeCompare(String(valorB));
        }
        
        return this.direccionOrden === 'asc' ? comparacion : -comparacion;
      });
    }

    _obtenerDatosPaginados() {
      if (!this.opciones.paginacion) {
        return this.datosFiltrados;
      }

      const inicio = (this.paginaActual - 1) * this.opciones.filasPorPagina;
      const fin = inicio + this.opciones.filasPorPagina;
      return this.datosFiltrados.slice(inicio, fin);
    }

    paginaSiguiente() {
      const totalPaginas = Math.ceil(this.datosFiltrados.length / this.opciones.filasPorPagina);
      if (this.paginaActual < totalPaginas) {
        this.paginaActual++;
        this._actualizarContenido();
      }
    }

    paginaAnterior() {
      if (this.paginaActual > 1) {
        this.paginaActual--;
        this._actualizarContenido();
      }
    }

    irAPagina(pagina) {
      const totalPaginas = Math.ceil(this.datosFiltrados.length / this.opciones.filasPorPagina);
      if (pagina >= 1 && pagina <= totalPaginas) {
        this.paginaActual = pagina;
        this._actualizarContenido();
      }
    }

    actualizarDatos(nuevosDatos) {
      this.opciones.datos = nuevosDatos;
      this.datosFiltrados = [...nuevosDatos];
      this.paginaActual = 1;
      this.renderizar();
    }
  }

  /* ========================================
     COMPONENTE: BarChart
     ======================================== */
  class BarChart {
    constructor(contenedor, opciones = {}) {
      this.contenedor = obtenerElemento(contenedor);
      
      if (!this.contenedor) {
        throw new Error('AgusmaLab.BarChart: contenedor no encontrado');
      }

      this.opciones = {
        titulo: opciones.titulo || 'Gráfico de Barras',
        etiquetas: opciones.etiquetas || [],
        datos: opciones.datos || [],
        color: opciones.color || '#3b82f6',
        ancho: opciones.ancho || 600,
        alto: opciones.alto || 300,
        ...opciones
      };

      this.renderizar();
    }

    renderizar() {
      this.contenedor.innerHTML = '';
      this.contenedor.className = 'agl-container';

      const wrapper = crearElemento('div', 'agl-chart-wrapper');

      // Título
      if (this.opciones.titulo) {
        const titulo = crearElemento('h3', 'agl-chart-title', this.opciones.titulo);
        wrapper.appendChild(titulo);
      }

      // Canvas
      const canvas = document.createElement('canvas');
      canvas.className = 'agl-chart-canvas';
      canvas.width = this.opciones.ancho;
      canvas.height = this.opciones.alto;
      wrapper.appendChild(canvas);

      this.contenedor.appendChild(wrapper);

      // Dibujar gráfico
      this._dibujarGrafico(canvas);
    }

    _dibujarGrafico(canvas) {
      const ctx = canvas.getContext('2d');
      const padding = 50;
      const ancho = canvas.width - padding * 2;
      const alto = canvas.height - padding * 2;

      // Limpiar canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Configurar fuente
      ctx.font = '12px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';

      // Encontrar valor máximo
      const valorMax = Math.max(...this.opciones.datos);
      const escalaY = alto / valorMax;

      // Calcular ancho de barras
      const numBarras = this.opciones.datos.length;
      const anchoBarra = (ancho / numBarras) * 0.7;
      const espacioBarra = (ancho / numBarras) * 0.3;

      // Dibujar barras
      this.opciones.datos.forEach((valor, i) => {
        const x = padding + (i * (anchoBarra + espacioBarra)) + espacioBarra / 2;
        const alturaBarra = valor * escalaY;
        const y = canvas.height - padding - alturaBarra;

        // Barra
        ctx.fillStyle = this.opciones.color;
        ctx.fillRect(x, y, anchoBarra, alturaBarra);

        // Valor encima de la barra
        ctx.fillStyle = '#1e293b';
        ctx.textAlign = 'center';
        ctx.fillText(valor, x + anchoBarra / 2, y - 5);

        // Etiqueta debajo
        if (this.opciones.etiquetas[i]) {
          ctx.fillText(this.opciones.etiquetas[i], x + anchoBarra / 2, canvas.height - padding + 20);
        }
      });

      // Eje Y (línea)
      ctx.strokeStyle = '#e2e8f0';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(padding, padding);
      ctx.lineTo(padding, canvas.height - padding);
      ctx.lineTo(canvas.width - padding, canvas.height - padding);
      ctx.stroke();
    }

    actualizarDatos(nuevosDatos, nuevasEtiquetas = null) {
      this.opciones.datos = nuevosDatos;
      if (nuevasEtiquetas) {
        this.opciones.etiquetas = nuevasEtiquetas;
      }
      this.renderizar();
    }
  }

  /* ========================================
     EXPORTAR LIBRERÍA
     ======================================== */
  return {
    StatsCard: StatsCard,
    DataTable: DataTable,
    BarChart: BarChart,
    Iconos: Iconos,
    version: '3.0.0'
  };
}));

