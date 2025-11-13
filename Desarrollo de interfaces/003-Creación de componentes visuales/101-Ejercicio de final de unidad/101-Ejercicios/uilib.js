/*!
 * UILib – Librería de Componentes UI v1.0.0
 * Componentes JavaScript reutilizables
 * Siguiendo los patrones vistos en clase (003, 004, 007)
 * Author: [Tu Nombre]
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.UILib = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  /* ========================================
     UTILIDADES
     ======================================== */
  
  const normalize = (str) => {
    return str.normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase();
  };

  const createElement = (tag, className, content) => {
    const el = document.createElement(tag);
    if (className) el.className = className;
    if (content) el.textContent = content;
    return el;
  };

  /* ========================================
     COMPONENTE: DataTable
     Tabla con ordenamiento, búsqueda y paginación
     ======================================== */
  class DataTable {
    constructor(container, options = {}) {
      this.container = typeof container === 'string' 
        ? document.querySelector(container) 
        : container;
      
      if (!this.container) {
        throw new Error('UILib.DataTable: contenedor no encontrado');
      }

      this.options = {
        title: options.title || 'Tabla de datos',
        columns: options.columns || [],
        data: options.data || [],
        searchable: options.searchable !== false,
        sortable: options.sortable !== false,
        pagination: options.pagination !== false,
        rowsPerPage: options.rowsPerPage || 10,
        ...options
      };

      this.currentPage = 1;
      this.sortColumn = null;
      this.sortDirection = 'asc';
      this.searchTerm = '';
      this.filteredData = [...this.options.data];

      this._render();
      this._attachEvents();
    }

    _render() {
      // Limpiar contenedor
      this.container.innerHTML = '';
      this.container.className = 'uil-table-wrapper uil-container';

      // Header con título y búsqueda
      const header = createElement('div', 'uil-table-header');
      const title = createElement('h3', 'uil-table-title', this.options.title);
      header.appendChild(title);

      if (this.options.searchable) {
        this.searchInput = createElement('input', 'uil-table-search');
        this.searchInput.type = 'search';
        this.searchInput.placeholder = 'Buscar...';
        this.searchInput.value = this.searchTerm;
        header.appendChild(this.searchInput);
      }

      this.container.appendChild(header);

      // Tabla
      const table = createElement('table', 'uil-table');
      
      // Thead
      const thead = document.createElement('thead');
      const headerRow = document.createElement('tr');
      
      this.options.columns.forEach((col, index) => {
        const th = createElement('th', '', col.label || col.field);
        if (this.options.sortable && col.sortable !== false) {
          th.classList.add('sortable');
          th.dataset.field = col.field;
          th.dataset.index = index;
          
          if (this.sortColumn === col.field) {
            th.classList.add(this.sortDirection === 'asc' ? 'sorted-asc' : 'sorted-desc');
          }
        }
        headerRow.appendChild(th);
      });
      
      thead.appendChild(headerRow);
      table.appendChild(thead);

      // Tbody
      const tbody = document.createElement('tbody');
      const paginatedData = this._getPaginatedData();
      
      if (paginatedData.length === 0) {
        const emptyRow = document.createElement('tr');
        const emptyCell = createElement('td', '', 'No hay datos para mostrar');
        emptyCell.colSpan = this.options.columns.length;
        emptyCell.style.textAlign = 'center';
        emptyCell.style.padding = '2rem';
        emptyRow.appendChild(emptyCell);
        tbody.appendChild(emptyRow);
      } else {
        paginatedData.forEach(row => {
          const tr = document.createElement('tr');
          this.options.columns.forEach(col => {
            const td = createElement('td');
            const value = row[col.field];
            
            if (col.render) {
              const rendered = col.render(value, row);
              if (typeof rendered === 'string') {
                td.innerHTML = rendered;
              } else {
                td.appendChild(rendered);
              }
            } else {
              td.textContent = value !== null && value !== undefined ? value : '';
            }
            
            tr.appendChild(td);
          });
          tbody.appendChild(tr);
        });
      }
      
      table.appendChild(tbody);
      this.container.appendChild(table);

      // Footer con paginación
      if (this.options.pagination) {
        this._renderPagination();
      }
    }

    _renderPagination() {
      const footer = createElement('div', 'uil-table-footer');
      
      // Info
      const totalRows = this.filteredData.length;
      const start = (this.currentPage - 1) * this.options.rowsPerPage + 1;
      const end = Math.min(this.currentPage * this.options.rowsPerPage, totalRows);
      const info = createElement('div', 'uil-table-info', 
        `Mostrando ${start}-${end} de ${totalRows} registros`);
      footer.appendChild(info);

      // Controles de paginación
      const pagination = createElement('div', 'uil-table-pagination');
      const totalPages = Math.ceil(totalRows / this.options.rowsPerPage);

      // Botón anterior
      const prevBtn = createElement('button', '', '← Anterior');
      prevBtn.disabled = this.currentPage === 1;
      prevBtn.addEventListener('click', () => this.previousPage());
      pagination.appendChild(prevBtn);

      // Números de página
      const maxVisiblePages = 5;
      let startPage = Math.max(1, this.currentPage - Math.floor(maxVisiblePages / 2));
      let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);
      
      if (endPage - startPage < maxVisiblePages - 1) {
        startPage = Math.max(1, endPage - maxVisiblePages + 1);
      }

      for (let i = startPage; i <= endPage; i++) {
        const pageBtn = createElement('button', 'page-number', i.toString());
        if (i === this.currentPage) {
          pageBtn.classList.add('active');
        }
        pageBtn.addEventListener('click', () => this.goToPage(i));
        pagination.appendChild(pageBtn);
      }

      // Botón siguiente
      const nextBtn = createElement('button', '', 'Siguiente →');
      nextBtn.disabled = this.currentPage === totalPages || totalPages === 0;
      nextBtn.addEventListener('click', () => this.nextPage());
      pagination.appendChild(nextBtn);

      footer.appendChild(pagination);
      this.container.appendChild(footer);
    }

    _attachEvents() {
      if (this.searchInput) {
        this.searchInput.addEventListener('input', (e) => {
          this.searchTerm = e.target.value;
          this._filterData();
          this.currentPage = 1;
          this._render();
          this._attachEvents();
        });
      }

      // Eventos de ordenamiento
      if (this.options.sortable) {
        const headers = this.container.querySelectorAll('th.sortable');
        headers.forEach(th => {
          th.addEventListener('click', () => {
            const field = th.dataset.field;
            if (this.sortColumn === field) {
              this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
            } else {
              this.sortColumn = field;
              this.sortDirection = 'asc';
            }
            this._sortData();
            this._render();
            this._attachEvents();
          });
        });
      }
    }

    _filterData() {
      if (!this.searchTerm) {
        this.filteredData = [...this.options.data];
        return;
      }

      const term = normalize(this.searchTerm);
      this.filteredData = this.options.data.filter(row => {
        return this.options.columns.some(col => {
          const value = row[col.field];
          if (value === null || value === undefined) return false;
          return normalize(String(value)).includes(term);
        });
      });
    }

    _sortData() {
      if (!this.sortColumn) return;

      this.filteredData.sort((a, b) => {
        const aVal = a[this.sortColumn];
        const bVal = b[this.sortColumn];
        
        if (aVal === null || aVal === undefined) return 1;
        if (bVal === null || bVal === undefined) return -1;
        
        let comparison = 0;
        if (typeof aVal === 'number' && typeof bVal === 'number') {
          comparison = aVal - bVal;
        } else {
          comparison = String(aVal).localeCompare(String(bVal));
        }
        
        return this.sortDirection === 'asc' ? comparison : -comparison;
      });
    }

    _getPaginatedData() {
      if (!this.options.pagination) {
        return this.filteredData;
      }

      const start = (this.currentPage - 1) * this.options.rowsPerPage;
      const end = start + this.options.rowsPerPage;
      return this.filteredData.slice(start, end);
    }

    nextPage() {
      const totalPages = Math.ceil(this.filteredData.length / this.options.rowsPerPage);
      if (this.currentPage < totalPages) {
        this.currentPage++;
        this._render();
        this._attachEvents();
      }
    }

    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this._render();
        this._attachEvents();
      }
    }

    goToPage(page) {
      const totalPages = Math.ceil(this.filteredData.length / this.options.rowsPerPage);
      if (page >= 1 && page <= totalPages) {
        this.currentPage = page;
        this._render();
        this._attachEvents();
      }
    }

    updateData(newData) {
      this.options.data = newData;
      this.filteredData = [...newData];
      this.currentPage = 1;
      this._filterData();
      this._sortData();
      this._render();
      this._attachEvents();
    }
  }

  /* ========================================
     COMPONENTE: SearchableSelect
     Select con búsqueda (basado en jocarsaui)
     ======================================== */
  class SearchableSelect {
    constructor(selectEl, options = {}) {
      if (!selectEl || selectEl.tagName !== 'SELECT') {
        throw new Error('UILib.SearchableSelect: debe recibir un elemento <select>');
      }

      this.select = selectEl;
      this.options = {
        placeholder: options.placeholder || 'Escribe para buscar...',
        diacriticsInsensitive: options.diacriticsInsensitive !== false,
        closeOnSelect: options.closeOnSelect !== false,
        ...options
      };

      this.isOpen = false;
      this.activeIndex = -1;
      this.items = [];

      this._setup();
      this._bind();
    }

    _setup() {
      // Crear contenedor
      this.root = createElement('div', 'uil-select uil-container');
      this.select.parentNode.insertBefore(this.root, this.select);
      this.root.appendChild(this.select);

      // Ocultar select nativo
      this.select.classList.add('uil-select-native');

      // Input de búsqueda
      this.input = createElement('input', 'uil-select-input');
      this.input.type = 'search';
      this.input.placeholder = this.options.placeholder;
      this.root.appendChild(this.input);

      // Panel de opciones
      this.panel = createElement('div', 'uil-select-panel');
      this.panel.setAttribute('role', 'listbox');
      this.root.appendChild(this.panel);

      // Extraer opciones
      this.allItems = Array.from(this.select.options)
        .filter(opt => opt.value && opt.text.trim())
        .map(opt => ({
          text: opt.text.trim(),
          value: opt.value
        }));

      this._renderItems(this.allItems);
      
      // Establecer valor inicial
      if (this.select.value) {
        this.input.value = this.select.options[this.select.selectedIndex]?.text || '';
      }
    }

    _bind() {
      this.input.addEventListener('focus', () => this.open());
      this.input.addEventListener('input', () => this._filter());
      this.input.addEventListener('keydown', (e) => this._handleKeys(e));

      // Click fuera para cerrar
      document.addEventListener('click', (e) => {
        if (!this.root.contains(e.target)) {
          this.close();
        }
      });
    }

    _renderItems(items) {
      this.panel.innerHTML = '';
      this.items = items;

      if (items.length === 0) {
        const empty = createElement('div', 'uil-select-empty', 'No se encontraron resultados');
        this.panel.appendChild(empty);
        return;
      }

      items.forEach((item, index) => {
        const div = createElement('div', 'uil-select-item', item.text);
        div.dataset.value = item.value;
        div.dataset.index = index;
        div.setAttribute('role', 'option');
        
        if (item.value === this.select.value) {
          div.classList.add('active');
        }

        div.addEventListener('click', () => this._selectItem(item));
        this.panel.appendChild(div);
      });
    }

    _filter() {
      const query = this.input.value.trim();
      
      if (!query) {
        this._renderItems(this.allItems);
        return;
      }

      const normalizedQuery = this.options.diacriticsInsensitive 
        ? normalize(query) 
        : query.toLowerCase();

      const filtered = this.allItems.filter(item => {
        const text = this.options.diacriticsInsensitive 
          ? normalize(item.text) 
          : item.text.toLowerCase();
        return text.includes(normalizedQuery);
      });

      this._renderItems(filtered);
      this.activeIndex = -1;
    }

    _selectItem(item) {
      this.select.value = item.value;
      this.input.value = item.text;
      
      // Disparar evento change
      const event = new Event('change', { bubbles: true });
      this.select.dispatchEvent(event);

      if (this.options.closeOnSelect) {
        this.close();
      }

      this._renderItems(this.items);
    }

    _handleKeys(e) {
      const itemElements = this.panel.querySelectorAll('.uil-select-item');
      
      switch(e.key) {
        case 'ArrowDown':
          e.preventDefault();
          this.activeIndex = Math.min(this.activeIndex + 1, itemElements.length - 1);
          this._highlightItem();
          break;
        
        case 'ArrowUp':
          e.preventDefault();
          this.activeIndex = Math.max(this.activeIndex - 1, 0);
          this._highlightItem();
          break;
        
        case 'Enter':
          e.preventDefault();
          if (this.activeIndex >= 0 && itemElements[this.activeIndex]) {
            const value = itemElements[this.activeIndex].dataset.value;
            const item = this.items.find(i => i.value === value);
            if (item) this._selectItem(item);
          }
          break;
        
        case 'Escape':
          this.close();
          break;
      }
    }

    _highlightItem() {
      const items = this.panel.querySelectorAll('.uil-select-item');
      items.forEach((item, index) => {
        item.setAttribute('aria-selected', index === this.activeIndex ? 'true' : 'false');
      });
      
      if (items[this.activeIndex]) {
        items[this.activeIndex].scrollIntoView({ block: 'nearest' });
      }
    }

    open() {
      this.isOpen = true;
      this.root.classList.add('uil-select--open');
      this._filter();
    }

    close() {
      this.isOpen = false;
      this.root.classList.remove('uil-select--open');
      this.activeIndex = -1;
      
      // Restaurar valor si input está vacío
      if (!this.input.value && this.select.value) {
        const selected = this.allItems.find(i => i.value === this.select.value);
        if (selected) this.input.value = selected.text;
      }
    }
  }

  /* ========================================
     COMPONENTE: BarChart
     Gráfico de barras simple con Canvas
     ======================================== */
  class BarChart {
    constructor(container, options = {}) {
      this.container = typeof container === 'string' 
        ? document.querySelector(container) 
        : container;
      
      if (!this.container) {
        throw new Error('UILib.BarChart: contenedor no encontrado');
      }

      this.options = {
        title: options.title || 'Gráfico de barras',
        labels: options.labels || [],
        data: options.data || [],
        color: options.color || '#2563eb',
        width: options.width || 600,
        height: options.height || 400,
        showValues: options.showValues !== false,
        ...options
      };

      this._render();
    }

    _render() {
      this.container.innerHTML = '';
      this.container.className = 'uil-chart-wrapper uil-container';

      // Título
      const title = createElement('div', 'uil-chart-title', this.options.title);
      this.container.appendChild(title);

      // Canvas
      this.canvas = document.createElement('canvas');
      this.canvas.className = 'uil-chart-canvas';
      this.canvas.width = this.options.width;
      this.canvas.height = this.options.height;
      this.container.appendChild(this.canvas);

      this._draw();
    }

    _draw() {
      const ctx = this.canvas.getContext('2d');
      const padding = 60;
      const chartWidth = this.canvas.width - padding * 2;
      const chartHeight = this.canvas.height - padding * 2;

      // Limpiar canvas
      ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

      // Encontrar valor máximo
      const maxValue = Math.max(...this.options.data, 0);
      const barCount = this.options.data.length;
      const barWidth = chartWidth / barCount * 0.8;
      const barSpacing = chartWidth / barCount * 0.2;

      // Dibujar ejes
      ctx.strokeStyle = '#e2e8f0';
      ctx.lineWidth = 2;
      
      // Eje Y
      ctx.beginPath();
      ctx.moveTo(padding, padding);
      ctx.lineTo(padding, this.canvas.height - padding);
      ctx.stroke();
      
      // Eje X
      ctx.beginPath();
      ctx.moveTo(padding, this.canvas.height - padding);
      ctx.lineTo(this.canvas.width - padding, this.canvas.height - padding);
      ctx.stroke();

      // Dibujar barras
      this.options.data.forEach((value, index) => {
        const barHeight = (value / maxValue) * chartHeight;
        const x = padding + index * (barWidth + barSpacing) + barSpacing / 2;
        const y = this.canvas.height - padding - barHeight;

        // Barra
        ctx.fillStyle = this.options.color;
        ctx.fillRect(x, y, barWidth, barHeight);

        // Valor sobre la barra
        if (this.options.showValues) {
          ctx.fillStyle = '#0f172a';
          ctx.font = '12px system-ui';
          ctx.textAlign = 'center';
          ctx.fillText(value, x + barWidth / 2, y - 5);
        }

        // Etiqueta debajo de la barra
        ctx.fillStyle = '#64748b';
        ctx.font = '12px system-ui';
        ctx.textAlign = 'center';
        ctx.fillText(
          this.options.labels[index] || '',
          x + barWidth / 2,
          this.canvas.height - padding + 20
        );
      });

      // Escala Y
      ctx.fillStyle = '#64748b';
      ctx.font = '12px system-ui';
      ctx.textAlign = 'right';
      
      for (let i = 0; i <= 5; i++) {
        const value = (maxValue / 5) * i;
        const y = this.canvas.height - padding - (chartHeight / 5) * i;
        ctx.fillText(Math.round(value), padding - 10, y + 5);
        
        // Líneas de guía
        ctx.strokeStyle = '#f1f5f9';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(padding, y);
        ctx.lineTo(this.canvas.width - padding, y);
        ctx.stroke();
      }
    }

    update(newData) {
      this.options.data = newData;
      this._draw();
    }
  }

  /* ========================================
     COMPONENTE: StatsCard
     Tarjeta de estadísticas para informes
     ======================================== */
  class StatsCard {
    constructor(container, options = {}) {
      this.container = typeof container === 'string' 
        ? document.querySelector(container) 
        : container;
      
      if (!this.container) {
        throw new Error('UILib.StatsCard: contenedor no encontrado');
      }

      this.options = {
        label: options.label || 'Estadística',
        value: options.value || '0',
        change: options.change || null,
        changeType: options.changeType || 'positive', // 'positive' | 'negative'
        icon: options.icon || '📊',
        iconType: options.iconType || 'primary', // 'primary' | 'success' | 'warning' | 'danger' | 'info'
        ...options
      };

      this._render();
    }

    _render() {
      this.container.innerHTML = '';
      this.container.className = 'uil-stats-card uil-container';

      // Header
      const header = createElement('div', 'uil-stats-header');
      
      const label = createElement('div', 'uil-stats-label', this.options.label);
      header.appendChild(label);

      const icon = createElement('div', `uil-stats-icon ${this.options.iconType}`, this.options.icon);
      header.appendChild(icon);

      this.container.appendChild(header);

      // Value
      const value = createElement('div', 'uil-stats-value', this.options.value);
      this.container.appendChild(value);

      // Change (opcional)
      if (this.options.change !== null) {
        const change = createElement('div', `uil-stats-change ${this.options.changeType}`, 
          `${this.options.change}%`);
        this.container.appendChild(change);
      }
    }

    update(newOptions) {
      this.options = { ...this.options, ...newOptions };
      this._render();
    }
  }

  /* ========================================
     COMPONENTE: ReportPanel
     Panel de informe con header, body y footer
     ======================================== */
  class ReportPanel {
    constructor(container, options = {}) {
      this.container = typeof container === 'string' 
        ? document.querySelector(container) 
        : container;
      
      if (!this.container) {
        throw new Error('UILib.ReportPanel: contenedor no encontrado');
      }

      this.options = {
        title: options.title || 'Informe',
        subtitle: options.subtitle || '',
        footer: options.footer || '',
        content: options.content || null,
        ...options
      };

      this._render();
    }

    _render() {
      this.container.innerHTML = '';
      this.container.className = 'uil-report uil-container';

      // Header
      const header = createElement('div', 'uil-report-header');
      const title = createElement('h3', 'uil-report-title', this.options.title);
      header.appendChild(title);

      if (this.options.subtitle) {
        const subtitle = createElement('div', 'uil-report-subtitle', this.options.subtitle);
        header.appendChild(subtitle);
      }

      this.container.appendChild(header);

      // Body
      const body = createElement('div', 'uil-report-body');
      if (this.options.content) {
        if (typeof this.options.content === 'string') {
          body.innerHTML = this.options.content;
        } else {
          body.appendChild(this.options.content);
        }
      }
      this.container.appendChild(body);

      // Footer
      if (this.options.footer) {
        const footer = createElement('div', 'uil-report-footer', this.options.footer);
        this.container.appendChild(footer);
      }
    }

    setContent(content) {
      const body = this.container.querySelector('.uil-report-body');
      if (body) {
        body.innerHTML = '';
        if (typeof content === 'string') {
          body.innerHTML = content;
        } else {
          body.appendChild(content);
        }
      }
    }
  }

  /* ========================================
     EXPORTAR API PÚBLICA
     ======================================== */
  return {
    DataTable,
    SearchableSelect,
    BarChart,
    StatsCard,
    ReportPanel,
    version: '1.0.0'
  };

}));
