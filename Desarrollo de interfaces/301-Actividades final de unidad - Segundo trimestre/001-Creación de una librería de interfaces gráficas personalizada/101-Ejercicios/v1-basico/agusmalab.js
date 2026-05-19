/*!
 * AgusmaLab - Librería de Componentes UI v1.0 (Básica)
 * Librería personal de componentes reutilizables
 * Autor: Agustín Mateo
 * Fecha: 17 de febrero de 2026
 */

(function (root, factory) {
  // Patrón UMD para compatibilidad con diferentes sistemas de módulos
  if (typeof define === 'function' && define.amd) {
    // AMD
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    // CommonJS
    module.exports = factory();
  } else {
    // Browser global
    root.AgusmaLab = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  /* ========================================
     UTILIDADES
     ======================================== */
  
  /**
   * Crea un elemento HTML con clase y contenido opcional
   * @param {string} tag - Etiqueta HTML
   * @param {string} className - Clase CSS
   * @param {string} content - Contenido de texto
   * @returns {HTMLElement}
   */
  const crearElemento = (tag, className = '', content = '') => {
    const elemento = document.createElement(tag);
    if (className) elemento.className = className;
    if (content) elemento.textContent = content;
    return elemento;
  };

  /**
   * Obtiene un elemento del DOM
   * @param {string|HTMLElement} selector - Selector CSS o elemento
   * @returns {HTMLElement}
   */
  const obtenerElemento = (selector) => {
    if (typeof selector === 'string') {
      return document.querySelector(selector);
    }
    return selector;
  };

  /* ========================================
     COMPONENTE: StatsCard
     Tarjeta de estadísticas visual
     ======================================== */
  class StatsCard {
    /**
     * Constructor de tarjeta de estadísticas
     * @param {string|HTMLElement} contenedor - Selector o elemento contenedor
     * @param {Object} opciones - Configuración de la tarjeta
     */
    constructor(contenedor, opciones = {}) {
      this.contenedor = obtenerElemento(contenedor);
      
      if (!this.contenedor) {
        throw new Error('AgusmaLab.StatsCard: contenedor no encontrado');
      }

      // Configuración por defecto
      this.opciones = {
        titulo: opciones.titulo || 'Estadística',
        valor: opciones.valor || '0',
        icono: opciones.icono || '📊',
        colorIcono: opciones.colorIcono || 'primary',
        descripcion: opciones.descripcion || '',
        ...opciones
      };

      this.renderizar();
    }

    /**
     * Renderiza la tarjeta de estadísticas
     */
    renderizar() {
      // Limpiar contenedor
      this.contenedor.innerHTML = '';
      this.contenedor.className = 'agl-container';

      // Crear tarjeta
      const tarjeta = crearElemento('div', 'agl-stats-card');

      // Header con título e icono
      const header = crearElemento('div', 'agl-stats-card-header');
      const titulo = crearElemento('div', 'agl-stats-card-title', this.opciones.titulo);
      const icono = crearElemento('div', `agl-stats-card-icon ${this.opciones.colorIcono}`, this.opciones.icono);
      
      header.appendChild(titulo);
      header.appendChild(icono);
      tarjeta.appendChild(header);

      // Valor principal
      const valor = crearElemento('div', 'agl-stats-card-value', this.opciones.valor);
      tarjeta.appendChild(valor);

      // Footer con descripción (si existe)
      if (this.opciones.descripcion) {
        const footer = crearElemento('div', 'agl-stats-card-footer', this.opciones.descripcion);
        tarjeta.appendChild(footer);
      }

      this.contenedor.appendChild(tarjeta);
    }

    /**
     * Actualiza el valor de la tarjeta
     * @param {string} nuevoValor - Nuevo valor a mostrar
     */
    actualizarValor(nuevoValor) {
      this.opciones.valor = nuevoValor;
      const valorElement = this.contenedor.querySelector('.ml-stats-card-value');
      if (valorElement) {
        valorElement.textContent = nuevoValor;
      }
    }

    /**
     * Actualiza el título de la tarjeta
     * @param {string} nuevoTitulo - Nuevo título
     */
    actualizarTitulo(nuevoTitulo) {
      this.opciones.titulo = nuevoTitulo;
      const tituloElement = this.contenedor.querySelector('.ml-stats-card-title');
      if (tituloElement) {
        tituloElement.textContent = nuevoTitulo;
      }
    }
  }

  /* ========================================
     COMPONENTE: SimpleTable
     Tabla HTML mejorada con estilos
     ======================================== */
  class SimpleTable {
    /**
     * Constructor de tabla simple
     * @param {string|HTMLElement} contenedor - Selector o elemento contenedor
     * @param {Object} opciones - Configuración de la tabla
     */
    constructor(contenedor, opciones = {}) {
      this.contenedor = obtenerElemento(contenedor);
      
      if (!this.contenedor) {
        throw new Error('AgusmaLab.SimpleTable: contenedor no encontrado');
      }

      // Configuración por defecto
      this.opciones = {
        titulo: opciones.titulo || 'Tabla de Datos',
        columnas: opciones.columnas || [],
        datos: opciones.datos || [],
        ...opciones
      };

      this.renderizar();
    }

    /**
     * Renderiza la tabla
     */
    renderizar() {
      // Limpiar contenedor
      this.contenedor.innerHTML = '';
      this.contenedor.className = 'agl-container';

      // Crear wrapper
      const wrapper = crearElemento('div', 'agl-table-wrapper');

      // Header con título
      const header = crearElemento('div', 'agl-table-header');
      const titulo = crearElemento('h3', 'agl-table-title', this.opciones.titulo);
      header.appendChild(titulo);
      wrapper.appendChild(header);

      // Crear tabla
      const tabla = crearElemento('table', 'agl-table');

      // Thead - Cabeceras
      const thead = document.createElement('thead');
      const filaHeader = document.createElement('tr');
      
      this.opciones.columnas.forEach(columna => {
        const th = crearElemento('th', '', columna);
        filaHeader.appendChild(th);
      });
      
      thead.appendChild(filaHeader);
      tabla.appendChild(thead);

      // Tbody - Datos
      const tbody = document.createElement('tbody');
      
      if (this.opciones.datos.length === 0) {
        // Mensaje si no hay datos
        const filaVacia = document.createElement('tr');
        const celdaVacia = crearElemento('td', '', 'No hay datos disponibles');
        celdaVacia.colSpan = this.opciones.columnas.length;
        celdaVacia.style.textAlign = 'center';
        celdaVacia.style.padding = '2rem';
        celdaVacia.style.color = 'var(--ml-text-muted)';
        filaVacia.appendChild(celdaVacia);
        tbody.appendChild(filaVacia);
      } else {
        // Renderizar datos
        this.opciones.datos.forEach(fila => {
          const tr = document.createElement('tr');
          
          fila.forEach(celda => {
            const td = crearElemento('td', '', celda);
            tr.appendChild(td);
          });
          
          tbody.appendChild(tr);
        });
      }
      
      tabla.appendChild(tbody);
      wrapper.appendChild(tabla);
      this.contenedor.appendChild(wrapper);
    }

    /**
     * Agrega una nueva fila a la tabla
     * @param {Array} nuevaFila - Array con los datos de la nueva fila
     */
    agregarFila(nuevaFila) {
      this.opciones.datos.push(nuevaFila);
      this.renderizar();
    }

    /**
     * Actualiza los datos completos de la tabla
     * @param {Array} nuevosDatos - Array bidimensional con los nuevos datos
     */
    actualizarDatos(nuevosDatos) {
      this.opciones.datos = nuevosDatos;
      this.renderizar();
    }

    /**
     * Limpia todos los datos de la tabla
     */
    limpiarDatos() {
      this.opciones.datos = [];
      this.renderizar();
    }
  }

  /* ========================================
     EXPORTAR LIBRERÍA
     ======================================== */
  return {
    StatsCard: StatsCard,
    SimpleTable: SimpleTable,
    version: '1.0.0'
  };
}));

