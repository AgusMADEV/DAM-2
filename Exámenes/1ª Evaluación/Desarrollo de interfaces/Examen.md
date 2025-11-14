El proyecto que he elegido para exponer en el exámen de Desarrollo de interfaces es la actividad de la unida 001-Generación de interfaces de usuario. En este proyecto, lo que he buscado es desarrollar una pequeña librería de componentes de interfaz de usuario que se puedan reutilizar y que tienen un enfoque empresarial. La librería se llama **jEnterpriseUI**, y su objetivo principal es comprender el funcionamiento de los **controles de formulario ''personalizados''** y la fácil integraciíon con datos externos mediante JavaScript, puro, sin usar librerías ecternas.
Para  mi, estos componentes son fundamentales y esenciales en aplicaciones de gestión, ya sean ERP, CRM, etc, que requeiran una **consistencia visual**, validaciones y componentes modulares.

---

En este proyecto, cada componente hereda de una clase base `JEComponent`, que define los métodos comunes como `setError()` o `setLoading()`.

Aquí tenemos la definición base en `jenterpriseui.js`:

```js
class JEComponent {
  constructor(root) {
    this.root = root;
  }

  init() {}
  setLoading(isLoading) {
    if (isLoading) {
      this.root.classList.add("je-loading");
    } else {
      this.root.classList.remove("je-loading");
    }
  }
  setError(message) {
    if (!message) {
      this.root.classList.remove("je-error");
      const msg = this.root.querySelector(".je-error-message");
      if (msg) msg.remove();
      return;
    }
    this.root.classList.add("je-error");
    let msg = this.root.querySelector(".je-error-message");
    if (!msg) {
      msg = document.createElement("div");
      msg.className = "je-error-message";
      this.root.appendChild(msg);
    }
    msg.textContent = message;
  }
```

También hemos creado el método de registro de componentes, lo que nos permite inicializar automáticamente al cargar el DOM:

```js
const JERegistry = {
  components: {},

  register(selector, ComponentClass) {
    this.components[selector] = ComponentClass;
  },

  initAll() {
    Object.entries(this.components).forEach(([selector, ComponentClass]) => {
      const elements = document.querySelectorAll(selector);
      elements.forEach(el => {
        if (!el.__jeInstance) {
          const instance = new ComponentClass(el);
          el.__jeInstance = instance;
          instance.init();
        }
      });
    });
  }
};

document.addEventListener("DOMContentLoaded", () => {
  JERegistry.initAll();
});
```

Luego, en cada componente para registrarlo lo hacemos de la siguiente forma:

```js
JERegistry.register(".je-select-remote", JESelectRemote);
```

Ahora vamos a ver los componentes más destacados de mi proyecto:

## - **je-textfield:** campos con validación de longitud, patrón y contador de carácteres.

```js
class JETextField extends JEComponent {
  init() {
    this.labelText = this.root.dataset.label || "Campo de texto";
    this.type = this.root.dataset.type || "text";
    this.required = this.root.dataset.required === "true";
    this.pattern = this.root.dataset.pattern || null;
    this.minLength = this.root.dataset.minlength ? parseInt(this.root.dataset.minlength, 10) : null;
    this.maxLength = this.root.dataset.maxlength ? parseInt(this.root.dataset.maxlength, 10) : null;
    this.helper = this.root.dataset.helper || "";
    this.showCounter = this.root.dataset.counter === "true";

    this.build();
  }

  build() {
    this.root.classList.add("je-field");

    const label = document.createElement("label");
    label.className = "je-label";
    label.textContent = this.labelText + (this.required ? " *" : "");

    this.input = document.createElement("input");
    this.input.className = "je-input";
    this.input.type = this.type;

    if (this.maxLength) this.input.maxLength = this.maxLength;

    if (this.helper) {
      this.helperEl = document.createElement("div");
      this.helperEl.className = "je-helper";
      this.helperEl.textContent = this.helper;
    }

    if (this.showCounter && this.maxLength) {
      this.counterEl = document.createElement("div");
      this.counterEl.className = "je-counter";
      this.updateCounter();
    }

    this.root.innerHTML = "";
    this.root.appendChild(label);
    this.root.appendChild(this.input);
    if (this.helperEl) this.root.appendChild(this.helperEl);
    if (this.counterEl) this.root.appendChild(this.counterEl);

    this.input.addEventListener("input", () => {
      if (this.showCounter && this.maxLength) this.updateCounter();
      this.clearError();
    });

    this.input.addEventListener("blur", () => {
      this.validate();
    });
  }

  updateCounter() {
    const length = this.input.value.length;
    this.counterEl.textContent = `${length}/${this.maxLength}`;
  }

  clearError() {
    this.setError(null);
  }

  validate() {
    const value = this.input.value.trim();

    if (this.required && !value) {
      this.setError("Este campo es obligatorio.");
      return false;
    }

    if (this.minLength && value.length < this.minLength) {
      this.setError(`Mínimo ${this.minLength} caracteres.`);
      return false;
    }

    if (this.pattern) {
      const regex = new RegExp(this.pattern);
      if (value && !regex.test(value)) {
        this.setError("El formato introducido no es válido.");
        return false;
      }
    }

    this.setError(null);

    // Evento de cambio válido
    this.root.dispatchEvent(new CustomEvent("je:valid", {
      detail: { value },
      bubbles: true
    }));

    return true;
  }

  getValue() {
    return this.input.value.trim();
  }
}

JERegistry.register(".je-textfield", JETextField);
```

## -**je-select-remote:** carga dinámica de datos externos en menús desplegables.  

```js
class JESelectRemote extends JEComponent {
  init() {
    this.labelText = this.root.dataset.label || "Selecciona una opción";
    this.src = this.root.dataset.src;                 // URL del JSON
    this.valueField = this.root.dataset.valueField || "id";
    this.labelField = this.root.dataset.labelField || "nombre";
    this.placeholder = this.root.dataset.placeholder || "Cargando...";
    this.required = this.root.dataset.required === "true";

    this.build();
    if (!this.src) {
      this.setError("Falta el atributo data-src con la ruta al JSON.");
      return;
    }
    this.loadOptions();
  }

  build() {
    this.root.classList.add("je-field");

    const label = document.createElement("label");
    label.className = "je-label";
    label.textContent = this.labelText;

    this.select = document.createElement("select");
    this.select.className = "je-select";
    if (this.required) this.select.required = true;

    const optPlaceholder = document.createElement("option");
    optPlaceholder.textContent = this.placeholder;
    optPlaceholder.value = "";
    optPlaceholder.disabled = true;
    optPlaceholder.selected = true;
    this.select.appendChild(optPlaceholder);

    this.root.innerHTML = "";
    this.root.appendChild(label);
    this.root.appendChild(this.select);

    this.select.addEventListener("change", () => {
      this.root.dispatchEvent(new CustomEvent("je:change", {
        detail: { value: this.select.value },
        bubbles: true
      }));
    });
  }

  async loadOptions() {
    try {
      this.setLoading(true);
      this.setError(null);

      const res = await fetch(this.src);
      if (!res.ok) throw new Error("No se pudo cargar el origen de datos");
      const data = await res.json();

      // Asumimos array de objetos
      this.populate(data);
    } catch (err) {
      this.setError("Error al cargar opciones.");
      console.error(err);
    } finally {
      this.setLoading(false);
    }
  }

  populate(items) {
    // Elimina placeholder anterior
    this.select.innerHTML = "";

    const emptyOpt = document.createElement("option");
    emptyOpt.textContent = "Selecciona una opción";
    emptyOpt.value = "";
    emptyOpt.disabled = true;
    emptyOpt.selected = true;
    this.select.appendChild(emptyOpt);

    items.forEach(item => {
      const opt = document.createElement("option");
      opt.value = item[this.valueField];
      opt.textContent = item[this.labelField];
      this.select.appendChild(opt);
    });
  }
}

// Registrar en el sistema
JERegistry.register(".je-select-remote", JESelectRemote);
```

## - **je-modal:** ventana emergente reutilizable con eventos personalizados.  

```js
class JEModal extends JEComponent {
  init() {
    this.title = this.root.dataset.title || "Modal";
    this.size = this.root.dataset.size || "medium"; // small, medium, large
    this.closeOnBackdrop = this.root.dataset.closeOnBackdrop !== "false";
    this.closeOnEscape = this.root.dataset.closeOnEscape !== "false";
    
    // Guardar contenido original
    this.originalContent = this.root.innerHTML;
    
    this.isOpen = false;
    this.build();
    this.attachEvents();
  }

  build() {
    // Crear estructura del modal
    this.backdrop = document.createElement("div");
    this.backdrop.className = "je-modal-backdrop";
    
    this.dialog = document.createElement("div");
    this.dialog.className = `je-modal-dialog je-modal-${this.size}`;
    
    // Header
    this.header = document.createElement("div");
    this.header.className = "je-modal-header";
    
    this.titleEl = document.createElement("h3");
    this.titleEl.className = "je-modal-title";
    this.titleEl.textContent = this.title;
    
    this.closeBtn = document.createElement("button");
    this.closeBtn.className = "je-modal-close";
    this.closeBtn.innerHTML = "&times;";
    this.closeBtn.type = "button";
    
    this.header.appendChild(this.titleEl);
    this.header.appendChild(this.closeBtn);
    
    // Body
    this.body = document.createElement("div");
    this.body.className = "je-modal-body";
    this.body.innerHTML = this.originalContent;
    
    // Footer (opcional)
    this.footer = document.createElement("div");
    this.footer.className = "je-modal-footer";
    
    // Ensamblar
    this.dialog.appendChild(this.header);
    this.dialog.appendChild(this.body);
    this.dialog.appendChild(this.footer);
    
    this.backdrop.appendChild(this.dialog);
    
    // Reemplazar contenido original con contenedor oculto
    this.root.innerHTML = "";
    this.root.classList.add("je-modal-container");
    this.root.style.display = "none";
  }

  attachEvents() {
    // Cerrar con botón X
    this.closeBtn.addEventListener("click", () => this.close());
    
    // Cerrar con backdrop
    if (this.closeOnBackdrop) {
      this.backdrop.addEventListener("click", (e) => {
        if (e.target === this.backdrop) {
          this.close();
        }
      });
    }
    
    // Cerrar con ESC
    if (this.closeOnEscape) {
      this.escapeHandler = (e) => {
        if (e.key === "Escape" && this.isOpen) {
          this.close();
        }
      };
      document.addEventListener("keydown", this.escapeHandler);
    }
  }

  open() {
    if (this.isOpen) return;
    
    this.isOpen = true;
    document.body.appendChild(this.backdrop);
    
    // Animación
    setTimeout(() => {
      this.backdrop.classList.add("je-modal-open");
    }, 10);
    
    // Prevenir scroll del body
    document.body.style.overflow = "hidden";
    
    // Emitir evento
    this.root.dispatchEvent(new CustomEvent("je:modal:open", {
      bubbles: true
    }));
  }

  close() {
    if (!this.isOpen) return;
    
    this.backdrop.classList.remove("je-modal-open");
    
    setTimeout(() => {
      if (this.backdrop.parentNode) {
        this.backdrop.parentNode.removeChild(this.backdrop);
      }
      this.isOpen = false;
      document.body.style.overflow = "";
      
      // Emitir evento
      this.root.dispatchEvent(new CustomEvent("je:modal:close", {
        bubbles: true
      }));
    }, 300);
  }

  setContent(html) {
    this.body.innerHTML = html;
  }

  setFooter(html) {
    this.footer.innerHTML = html;
  }

  destroy() {
    if (this.isOpen) {
      this.close();
    }
    if (this.escapeHandler) {
      document.removeEventListener("keydown", this.escapeHandler);
    }
  }
}

JERegistry.register(".je-modal", JEModal);
```

Aquí dejo un ejemplo de como darles funcionamiento a los modales en nuestro HTML:

**Ejemplo de `je-texfield.js`** 
```html
    <div class="je-textfield"
        data-label="Nombre del pedido"
        data-required="true"
        data-minlength="3"
        data-maxlength="50"
        data-helper="Introduce un nombre descriptivo."
        data-counter="true">
    </div>
```

**Ejemplo de `je-select-remote.js`**
```html
    <div class="je-select-remote"
            data-label="Cliente"
            data-src="data/clientes.json"
            data-value-field="id"
            data-label-field="nombre"
            data-required="true">
    </div>
```

**Ejemplo de `je-table.js`**
```html
    <div class="je-table"
            data-src="data/pedidos.json"
            data-caption="Pedidos recientes"
            data-sortable="true">
    </div>
```

Cada uno de los componentes pueden ser personalizados como el usuario deseé, modificando la información que recoge cada modal, y cambiando el texto que se necesite.

---

Voy a mostrar un pequeño ejemplo de un proyecto, que integre mi libreria `jenterpriceui`, y se genere la información de forma correcta y reutilizable:
En este caso lo importaremos desde la misma carpeta del proyecto, pero también podría importarse desde GitHub.

### Árbol del proyecto en cuestión.

├── data
│   ├── clientes.json
│   └── pedidos.json
├── index.html
└── js
   ├── je-checkbox-group.js
   ├── je-datepicker.js
   ├── je-modal.js
   ├── je-progress-bar.js
   ├── je-select-remote.js
   ├── je-table.js
   ├── je-tag-input.js
   ├── je-textfield.js
   └── jenterpriseui.js

**index.html**
```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>jEnterpriseUI - Demo librería</title>
  <link rel="stylesheet" href="css/jenterpriseui.css">
</head>
<body>
  <div class="je-layout">
    <aside class="je-sidebar">
      <h1>jEnterpriseUI</h1>
      <nav>
        <a href="#formulario">Formulario de alta</a>
        <a href="#listado">Listado de pedidos</a>
      </nav>
    </aside>
    <main class="je-main">
      <header class="je-header">
        <div>
          <div class="je-header-title">Librería de componentes UI empresariales</div>
          <div class="je-header-subtitle">
            Ejercicio final U1 · jEnterpriseUI
          </div>
        </div>
      </header>

      <section id="formulario" class="je-card">
        <h2>Formulario de alta de pedido</h2>
        <!-- Nombre del pedido -->
        <div class="je-textfield"
            data-label="Nombre del pedido"
            data-required="true"
            data-minlength="3"
            data-maxlength="50"
            data-helper="Introduce un nombre descriptivo."
            data-counter="true">
        </div>
        <!-- Selector de cliente desde JSON -->
        <div class="je-select-remote"
             data-label="Cliente"
             data-src="data/clientes.json"
             data-value-field="id"
             data-label-field="nombre"
             data-required="true">
        </div>
      </section>
      <section id="listado" class="je-card">
        <h2>Listado de pedidos</h2>
        <p style="font-size:0.85rem; color:#6b7280;">
          Ejemplo de <code>.je-table</code> generada desde <code>pedidos.json</code>, con ordenación.
        </p>

        <div class="je-table"
             data-src="data/pedidos.json"
             data-caption="Pedidos recientes"
             data-sortable="true">
        </div>
        <!-- DatePicker -->
        <div class="je-datepicker"
             data-label="Fecha de entrega"
             data-format="dd/mm/yyyy"
             data-min="2025-01-01"
             data-max="2025-12-31"
             data-required="true">
        </div>
      </section>
        <!-- Botón para abrir modal -->
        <button onclick="document.querySelector('.je-modal').__jeInstance.open()" 
                class="je-btn je-btn-primary">
          🔔 Abrir Modal de confirmación
        </button>
      </section>
    </main>
  </div>

  <!-- MODAL-->
  <div class="je-modal" 
       data-title="Confirmar pedido"
       data-size="medium"
       data-close-on-backdrop="true">
    <p>¿Estás seguro de que deseas confirmar este pedido?</p>
    <p style="color:#6b7280; font-size:0.85rem;">Esta acción no se puede deshacer.</p>
    <div style="display:flex; gap:0.75rem; justify-content:flex-end; margin-top:1.5rem;">
      <button onclick="document.querySelector('.je-modal').__jeInstance.close()" 
              class="je-btn je-btn-secondary">
        Cancelar
      </button>
      <button onclick="alert('Pedido confirmado'); document.querySelector('.je-modal').__jeInstance.close()" 
              class="je-btn je-btn-success">
        ✓ Confirmar
      </button>
    </div>
  </div>
    <script src="js/jenterpriseui.js"></script>
    <script src="js/je-textfield.js"></script>
    <script src="js/je-select-remote.js"></script>
    <script src="js/je-table.js"></script>
    <script src="js/je-modal.js"></script>
    <script src="js/je-datepicker.js"></script>
</body>
</html>
```
La librería se aplica en el archivo principal `index.html`, donde se crean formularios empresariales reutilizando los componentes definidos.  
Por ejemplo, el formulario de alta de pedido combina varios de ellos:

```html
<div class="je-textfield" data-label="Nombre del pedido" data-required="true"></div>
<div class="je-select-remote" data-label="Cliente" data-src="data/clientes.json"></div>
```

Además, la información es enlazada a los componentes a archivos JSON reales (`clientes.json` y `pedidos.json`), simulamos así la carga de datos desde u nservidor, logrando que el flujo de trabajo sea el apropiado y similar al de una aplicación real.

**Ejemplo de los JSON:**
(`clientes.json`)
```json
[
  { "id": "C001", "nombre": "Acme S.A." },
  { "id": "C002", "nombre": "Tecnologías Norte" },
  { "id": "C003", "nombre": "Grupo Logístico Sur" }
]
````
(`pedidos.json`)
```json
[
  { "id": "P-1001", "cliente": "Acme S.A.", "importe": 1250.50, "nombre_pedido": "Pan", "estado": "Pendiente" },
  { "id": "P-1002", "cliente": "Tecnologías Norte", "importe": 980.00,"nombre_pedido": "Salami", "estado": "Enviado" },
  { "id": "P-1003", "cliente": "Grupo Logístico Sur", "importe": 430.75, "nombre_pedido": "Cartón","estado": "Entregado" },
  { "id": "P-1004", "cliente": "Grupo 2", "importe": 400.75,"nombre_pedido": "Auriculares", "estado": "Entregado" },
  { "id": "P-1005", "cliente": "Tecnologías Norte", "importe": 1500.00,"nombre_pedido": "Jamón Ibérico", "estado": "Pendiente" }
]
```

---

Este ejercicio, ha conseguido que comprenda mejor cómo se distribuyen librerías de componentes de interfaz de usuario desde cero y cómo poder aplicarlas en un entorno real empresarial.
He aprendido lo importante que es **estructurar el código en módulos reutilizables**, usar el **DOM de forma dinámica** y también a mantener una **coherencia visual y funcional** en todos lo elementos.
Los conceptos que he aplicado en este ejercicio se relacionan directamente con todo el contenido dado en clase en la **Uninda 1 de Desarrollo de Interfaces**, que ha sido centrada en la creación y reutilización de componentes visuales que optimizan y mejoran la experiencia del usuario, facilitando así también el mantenimiento del software.