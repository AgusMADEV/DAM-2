// D:\xampp\htdocs\DAM-2\Desarrollo de interfaces\003-Creación de componentes visuales\004-Persistencia del componente\101-Ejercicios\boton-tooltip.js

const tpl = document.createElement('template');
tpl.innerHTML = `
  <style>
    :host{
      font-family: system-ui, sans-serif;
      display: inline-block;
      position: relative;
      --c-border: #ddd;
      --c-bg: #fff;
      --c-hover: #f6f6f6;
      --c-prim: #0078ff;
      --radius: .6rem;
      --shadow: 0 6px 18px rgba(0,0,0,.08);
      width: 320px;
    }
    .wrap{
      display: grid;
      gap: .5rem;
    }

    /* Buscador */
    .search{
      position: relative;
    }
    .search input{
      width: 100%;
      box-sizing: border-box;
      padding: .6rem .75rem;
      border: 1px solid var(--c-border);
      border-radius: var(--radius);
      outline: none;
      background: var(--c-bg);
    }
    .search input:focus{
      box-shadow: 0 0 0 3px rgba(0,120,255,.18);
    }

    /* Dropdown de opciones (filtrado) */
    .panel{
      position: absolute;
      left: 0; right: 0; top: calc(100% + .25rem);
      border: 1px solid var(--c-border);
      border-radius: var(--radius);
      background: var(--c-bg);
      max-height: 220px;
      overflow: auto;
      display: none;
      box-shadow: var(--shadow);
      z-index: 10;
    }
    .panel.open{ display:block; }
    .item{
      padding: .55rem .75rem;
      cursor: pointer;
      user-select: none;
      line-height: 1.2;
    }
    .item:hover, .item[aria-selected="true"]{ background: var(--c-hover); }
    .empty{ padding:.55rem .75rem; color:#666; }

    /* Botón */
    .actions{
      display: flex;
      gap: .5rem;
      align-items: center;
    }
    .btn{
      padding: .6rem 1rem;
      border: 1px solid var(--c-border);
      border-radius: var(--radius);
      background: var(--c-bg);
      cursor: pointer;
    }
    .btn-primary{
      background: var(--c-prim);
      color: #fff;
      border: none;
    }
    .label{
      font-size: .9rem;
      color: #555;
      min-height: 1.2em;
    }

    /* Tooltip */
    .tooltip{
      position: absolute;
      left: 0; right: 0;
      top: calc(100% + .5rem);
      background: #111;
      color: #fff;
      padding: .6rem .75rem;
      border-radius: .6rem;
      font-size: .9rem;
      display: none;
      box-shadow: var(--shadow);
      z-index: 20;
    }
    .tooltip.show{ display: block; }
  </style>

  <div class="wrap">
    <div class="search">
      <input type="search" placeholder="Busca tu juego…" aria-label="Buscar juego">
      <div class="panel" role="listbox" aria-label="Resultados de juegos"></div>
    </div>

    <div class="actions">
      <button class="btn btn-primary" type="button" data-action="show">Mostrar info</button>
      <button class="btn" type="button" data-action="clear" title="Limpiar selección">Limpiar</button>
    </div>

    <div class="label" data-label></div>
  </div>

  <div class="tooltip" role="tooltip"></div>
`;

class BotonTooltip extends HTMLElement {
  static get observedAttributes(){ return ['label', 'placeholder']; }

  constructor(){
    super();
    this.attachShadow({mode:'open'}).appendChild(tpl.content.cloneNode(true));

    // refs
    this.$input   = this.shadowRoot.querySelector('.search input');
    this.$panel   = this.shadowRoot.querySelector('.panel');
    this.$label   = this.shadowRoot.querySelector('[data-label]');
    this.$tooltip = this.shadowRoot.querySelector('.tooltip');
    this.$btnShow = this.shadowRoot.querySelector('[data-action="show"]');
    this.$btnClear= this.shadowRoot.querySelector('[data-action="clear"]');

    // estado
    this._items = [];        // [{text, desc}]
    this._filtered = [];
    this._activeIndex = -1;
    this._selected = null;
  }

  connectedCallback(){
    // 1) Cargar opciones desde light DOM (<option data-desc="...">Texto</option>)
    this._loadItemsFromLightDOM();

    // 2) Placeholder opcional por atributo
    if (this.hasAttribute('placeholder')){
      this.$input.placeholder = this.getAttribute('placeholder');
    }

    // 3) Label opcional del botón por atributo
    if (this.hasAttribute('label')){
      this.$btnShow.textContent = this.getAttribute('label');
    }

    // 4) Pintado inicial (todas)
    this._render(this._items);

    // Eventos
    this.$input.addEventListener('focus', () => this._open(true));
    this.$input.addEventListener('input', () => this._onFilter());
    this.$input.addEventListener('keydown', e => this._onKeys(e));

    this.$btnShow.addEventListener('click', () => this._toggleTooltip());
    this.$btnClear.addEventListener('click', () => this._clear());

    document.addEventListener('click', this._outsideClick);
  }

  disconnectedCallback(){
    document.removeEventListener('click', this._outsideClick);
  }

  attributeChangedCallback(name, _old, val){
    if (name === 'placeholder' && this.$input) this.$input.placeholder = val ?? 'Busca tu juego…';
    if (name === 'label' && this.$btnShow) this.$btnShow.textContent = val ?? 'Mostrar info';
  }

  /** Lee las <option> hijas con data-desc */
  _loadItemsFromLightDOM(){
    const opts = Array.from(this.querySelectorAll('option'));
    this._items = opts.map(o => ({
      text: (o.textContent || '').trim(),
      desc: (o.getAttribute('data-desc') || '').trim()
    })).filter(o => o.text);

    // ocultar el contenido light para no duplicar (queda como fuente de datos)
    this.style.visibility = 'visible';
  }

  /** Normaliza texto (sin acentos) */
  _norm(s){ return s.normalize('NFD').replace(/\p{Diacritic}/gu,'').toLowerCase(); }

  /** Filtrado */
  _onFilter(){
    const q = this._norm(this.$input.value);
    this._filtered = this._items.filter(it => this._norm(it.text).includes(q));
    this._activeIndex = -1;
    this._render(this._filtered.length || q ? this._filtered : this._items);
    this._open(true);
  }

  /** Navegación con teclado */
  _onKeys(e){
    const items = Array.from(this.$panel.querySelectorAll('.item'));
    if (!items.length) return;

    if (e.key === 'ArrowDown'){
      e.preventDefault();
      this._activeIndex = (this._activeIndex + 1) % items.length;
      this._mark(items);
    } else if (e.key === 'ArrowUp'){
      e.preventDefault();
      this._activeIndex = (this._activeIndex - 1 + items.length) % items.length;
      this._mark(items);
    } else if (e.key === 'Enter' && this._activeIndex >= 0){
      e.preventDefault();
      items[this._activeIndex].click();
    } else if (e.key === 'Escape'){
      this._open(false);
    }
  }

  /** Dibuja lista en panel */
  _render(list){
    this.$panel.innerHTML = '';
    const data = list && list.length ? list : [];
    if (!data.length){
      this.$panel.innerHTML = `<div class="empty">Sin coincidencias</div>`;
      return;
    }
    data.forEach((it, idx) => {
      const div = document.createElement('div');
      div.className = 'item';
      div.setAttribute('role','option');
      div.textContent = it.text;
      div.addEventListener('click', () => this._select(it));
      this.$panel.appendChild(div);
    });
  }

  _select(item){
    this._selected = item;
    this.$input.value = item.text;
    this.$label.textContent = `Seleccionado: ${item.text}`;
    // Al seleccionar, cerramos el dropdown
    this._open(false);
    // Si el tooltip estaba abierto, actualizar contenido
    if (this.$tooltip.classList.contains('show')) {
      this._showTooltip(true);
    }
  }

  _mark(items){
    items.forEach((el,i) => el.setAttribute('aria-selected', i === this._activeIndex ? 'true':'false'));
    if (this._activeIndex >= 0) items[this._activeIndex].scrollIntoView({block:'nearest'});
  }

  _toggleTooltip(){
    const show = !this.$tooltip.classList.contains('show');
    this._showTooltip(show);
  }

  _showTooltip(show){
    // Si no hay selección, enseñamos aviso breve
    if (!this._selected){
      this.$tooltip.textContent = 'Selecciona primero un juego.';
    } else {
      this.$tooltip.textContent = this._selected.desc || 'Sin descripción.';
    }
    this.$tooltip.classList.toggle('show', show);
  }

  _clear(){
    this._selected = null;
    this.$input.value = '';
    this.$label.textContent = '';
    this._render(this._items);
    this._open(false);
    this.$tooltip.classList.remove('show');
    this.$input.focus();
  }

  _open(v){ this.$panel.classList.toggle('open', !!v); }

  _outsideClick = (e) => {
    if (!this.isConnected) return;
    if (!this.shadowRoot) return;

    // Si clic fuera del componente => cierra panel y tooltip
    const path = e.composedPath();
    if (!path.includes(this)) {
      this._open(false);
      this.$tooltip.classList.remove('show');
    }
  }
}

customElements.define('boton-tooltip', BotonTooltip);
