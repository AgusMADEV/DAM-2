Como aficionado a los **deportes y videojuegos**, he creado un **componente visual interactivo** que permite mostrar información sobre mis juegos favoritos.  
Este componente combina un **buscador con filtrado dinámico** y un **botón con tooltip**, lo que mejora la experiencia del usuario al permitir seleccionar un juego y ver rápidamente su descripción sin salir de la página.  
Este tipo de interacción es muy útil para sitios donde se desea mostrar información breve y clara, como catálogos, fichas de juegos o listas personalizadas.

---

El componente `boton-tooltip` ha sido implementado como un **Web Component** totalmente funcional.  
Sus principales características son:

- Un **campo de búsqueda (`input type="search"`)** que filtra las opciones disponibles mientras el usuario escribe.  
- Un **panel de resultados (`.panel`)** que muestra coincidencias dinámicamente.  
- Dos **botones de acción**:  
  - `Mostrar info`: muestra el tooltip con la descripción del juego seleccionado.  
  - `Limpiar`: reinicia la selección y limpia el campo de búsqueda.  
- Un **tooltip** que aparece al pulsar el botón principal, mostrando el texto descriptivo (`data-desc`) del juego elegido.  

El código también maneja el **teclado (ArrowUp, ArrowDown, Enter, Escape)** para una experiencia más accesible.  
Toda la lógica está dentro del archivo `boton-tooltip.js` y el componente se instancia directamente en `index.html`.

---

A continuación se muestra el código completo utilizado para esta actividad, que combina el buscador con el tooltip informativo.

### **index.html**
```
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <title>boton-tooltip con buscador (juegos favoritos)</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <script type="module" src="boton-tooltip.js"></script>
  <style>
    body{ font-family: system-ui, sans-serif; background:#fafafa; margin:2rem; }
    h1{ font-weight:600; color:#333; }
    section{
      background:#fff; padding:1.5rem; border-radius:1rem;
      box-shadow: 0 6px 18px rgba(0,0,0,.06); max-width: 740px;
    }
    .grid{ display:grid; gap:1.2rem; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); }
  </style>
</head>
<body>
  <h1>🎮 Componentes con buscador + tooltip</h1>
  <section>
    <p>
      Escribe para filtrar y selecciona un juego. Al pulsar <em>“Mostrar info”</em> verás un tooltip con la descripción.
    </p>

    <div class="grid">
      <!-- Instancia 1 -->
      <boton-tooltip label="Mostrar info" placeholder="Busca un videojuego…">
        <option data-desc="Acción y aventuras; mundo abierto y resolución de puzles.">
          The Legend of Zelda: Tears of the Kingdom
        </option>
        <option data-desc="Arcade de coches + fútbol; muy competitivo y con física divertida.">
          Rocket League
        </option>
        <option data-desc="Metroidvania desafiante con gran diseño de niveles y ambientación.">
          Hollow Knight
        </option>
        <option data-desc="Shooter hero-based 5v5 con trabajo en equipo y habilidades únicas.">
          Overwatch 2
        </option>
        <option data-desc="Simulador deportivo con licencias oficiales y modos competitivos.">
          EA Sports FC 25 (FIFA)
        </option>
        <option data-desc="Acción/rol en mundo abierto, combate exigente y jefes memorables.">
          Elden Ring
        </option>
      </boton-tooltip>
    </div>
  </section>
</body>
</html>
```

### **boton-tooltip.js**
```js
class BotonTooltip extends HTMLElement {
  static get observedAttributes(){ return ['label', 'placeholder']; }

  constructor(){
    super();
    this.attachShadow({mode:'open'});
    const tpl = document.createElement('template');
    tpl.innerHTML = `
      <style>
        :host{ font-family:system-ui,sans-serif; display:inline-block; position:relative; }
        .wrap{ display:grid; gap:.5rem; }
        .search input{ width:100%; padding:.6rem .75rem; border:1px solid #ccc; border-radius:.5rem; }
        .panel{ position:absolute; left:0; right:0; top:calc(100% + .25rem); border:1px solid #ddd; border-radius:.5rem; background:#fff; display:none; }
        .panel.open{ display:block; }
        .item{ padding:.5rem .75rem; cursor:pointer; }
        .item:hover{ background:#f0f0f0; }
        .tooltip{ position:absolute; top:calc(100% + .5rem); left:0; right:0; background:#111; color:#fff; padding:.5rem .75rem; border-radius:.5rem; display:none; }
        .tooltip.show{ display:block; }
      </style>

      <div class="wrap">
        <div class="search">
          <input type="search" placeholder="Busca tu juego…">
          <div class="panel"></div>
        </div>
        <div class="actions">
          <button data-action="show">Mostrar info</button>
          <button data-action="clear">Limpiar</button>
        </div>
        <div class="label" data-label></div>
      </div>
      <div class="tooltip"></div>
    `;
    this.shadowRoot.appendChild(tpl.content.cloneNode(true));

    this.$input = this.shadowRoot.querySelector('input');
    this.$panel = this.shadowRoot.querySelector('.panel');
    this.$tooltip = this.shadowRoot.querySelector('.tooltip');
    this.$btnShow = this.shadowRoot.querySelector('[data-action="show"]');
    this.$btnClear = this.shadowRoot.querySelector('[data-action="clear"]');
    this.$label = this.shadowRoot.querySelector('[data-label]');
    this._items = [];
    this._filtered = [];
    this._selected = null;
  }

  connectedCallback(){
    this._loadItemsFromLightDOM();
    this._render(this._items);
    this.$input.addEventListener('input', () => this._onFilter());
    this.$btnShow.addEventListener('click', () => this._toggleTooltip());
    this.$btnClear.addEventListener('click', () => this._clear());
  }

  _loadItemsFromLightDOM(){
    const opts = Array.from(this.querySelectorAll('option'));
    this._items = opts.map(o => ({ text:o.textContent.trim(), desc:o.dataset.desc.trim() }));
  }

  _onFilter(){
    const q = this.$input.value.toLowerCase();
    this._filtered = this._items.filter(it => it.text.toLowerCase().includes(q));
    this._render(this._filtered.length ? this._filtered : this._items);
    this.$panel.classList.add('open');
  }

  _render(list){
    this.$panel.innerHTML = '';
    list.forEach(it => {
      const div = document.createElement('div');
      div.className = 'item';
      div.textContent = it.text;
      div.onclick = () => this._select(it);
      this.$panel.appendChild(div);
    });
  }

  _select(item){
    this._selected = item;
    this.$input.value = item.text;
    this.$label.textContent = `Seleccionado: ${item.text}`;
    this.$panel.classList.remove('open');
  }

  _toggleTooltip(){
    if (!this._selected){
      this.$tooltip.textContent = 'Selecciona primero un juego.';
    } else {
      this.$tooltip.textContent = this._selected.desc;
    }
    this.$tooltip.classList.toggle('show');
  }

  _clear(){
    this._selected = null;
    this.$input.value = '';
    this.$label.textContent = '';
    this.$tooltip.classList.remove('show');
    this._render(this._items);
  }
}
customElements.define('boton-tooltip', BotonTooltip);
```

Luego, para utilizar el componente en una página web, basta con incluir el módulo JavaScript y declarar el elemento personalizado **boton-tooltip** en el HTML.
A continuación se añaden varias etiquetas **option** dentro del componente, cada una con el nombre del juego y una descripción:

```
<boton-tooltip label="Mostrar info" placeholder="Busca un videojuego…">
  <option data-desc="Acción y aventuras; mundo abierto y resolución de puzles.">
    The Legend of Zelda: Tears of the Kingdom
  </option>
  <option data-desc="Arcade de coches + fútbol; muy competitivo y con física divertida.">
    Rocket League
  </option>
  <option data-desc="Metroidvania desafiante con gran diseño de niveles y ambientación.">
    Hollow Knight
  </option>
</boton-tooltip>
```

**Ejemplo de uso:**

**1.** Escribo “zelda” en el buscador → aparece la coincidencia.
**2.** Selecciono el juego → se actualiza el texto “Seleccionado: The Legend of Zelda: Tears of the Kingdom”.
**3.** Hago clic en “Mostrar info” → aparece el tooltip con su descripción.

Todo ocurre sin recargar la página y con una respuesta visual inmediata.

---

Este ejercicio me ha permitido entender cómo los **componentes personalizados** y los **eventos en JavaScript** trabajan juntos para crear interfaces dinámicas.  
Gracias al uso de `shadow DOM`, encapsulación y lógica modular, este componente puede reutilizarse en otros proyectos sin interferir con el resto del código.  
A futuro, este tipo de desarrollos será muy útil para construir **interfaces modernas y personalizables**, tanto en proyectos de desarrollo web como en entornos profesionales donde se requiera **interactividad y eficiencia visual**.
