En este proyecto he desarrollado **jEnterpriseUI**, una pequeña librería de componentes de interfaz de usuario reutilizables orientada a entornos empresariales.  
El objetivo principal ha sido comprender el funcionamiento de los **controles de formulario personalizados** y su integración con datos externos mediante JavaScript puro, sin usar librerías externas.  
Estos componentes son esenciales en aplicaciones de gestión (ERP, CRM o sistemas internos) donde se requiere **consistencia visual**, validaciones y componentes modulares.

Por ejemplo, el componente `je-select-remote` permite cargar datos desde archivos JSON, tal como se haría en una aplicación que obtiene información de clientes o pedidos desde una API:
```js
<div class="je-select-remote" 
     data-label="Cliente" 
     data-src="data/clientes.json" 
     data-value-field="id" 
     data-label-field="nombre"></div>
```

---

Cada componente hereda de una clase base `JEComponent`, que define métodos comunes como `setError()` o `setLoading()`.  
De esta manera, cualquier control nuevo mantiene un comportamiento coherente.

Ejemplo de definición base en `jenterpriseui.js`:
```js
class JEComponent {
  constructor(root) { this.root = root; }
  setError(msg) { ... }
  setLoading(isLoading) { ... }
}
```
Los componentes se registran en `JERegistry`, lo que permite inicializarlos automáticamente al cargar el DOM:
```js
JERegistry.register(".je-select-remote", JESelectRemote);
document.addEventListener("DOMContentLoaded", () => JERegistry.initAll());
```

Entre los componentes más destacados se encuentran:

## - **je-textfield:** campos con validaciones de longitud, patrón y contador de caracteres.  

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

## - **je-tag-input:** permite añadir etiquetas interactivas con validación de máximo.  

```js
class JETagInput extends JEComponent {
  init() {
    this.labelText = this.root.dataset.label || "Etiquetas";
    this.placeholder = this.root.dataset.placeholder || "Escribe y pulsa Enter";
    this.name = this.root.dataset.name || "tags";
    this.maxTags = this.root.dataset.max ? parseInt(this.root.dataset.max, 10) : null;

    this.tags = [];
    this.build();
  }

  build() {
    this.root.classList.add("je-field", "je-tag-input-wrapper");

    const label = document.createElement("label");
    label.className = "je-label";
    label.textContent = this.labelText;

    this.tagsContainer = document.createElement("div");
    this.tagsContainer.className = "je-tag-input";

    this.input = document.createElement("input");
    this.input.type = "text";
    this.input.className = "je-tag-input-field";
    this.input.placeholder = this.placeholder;

    this.hiddenInput = document.createElement("input");
    this.hiddenInput.type = "hidden";
    this.hiddenInput.name = this.name;

    this.tagsContainer.appendChild(this.input);

    this.root.innerHTML = "";
    this.root.appendChild(label);
    this.root.appendChild(this.tagsContainer);
    this.root.appendChild(this.hiddenInput);

    this.input.addEventListener("keydown", (e) => this.handleKeyDown(e));
    this.tagsContainer.addEventListener("click", () => this.input.focus());
  }

  handleKeyDown(e) {
    const value = this.input.value.trim();

    if (e.key === "Enter" && value) {
      e.preventDefault();
      this.addTag(value);
    }

    if (e.key === "Backspace" && !value && this.tags.length > 0) {
      e.preventDefault();
      this.removeTag(this.tags[this.tags.length - 1]);
    }
  }

  addTag(text) {
    if (this.maxTags && this.tags.length >= this.maxTags) {
      this.setError(`Máximo ${this.maxTags} etiquetas.`);
      return;
    }

    this.setError(null);

    if (this.tags.includes(text)) return;

    this.tags.push(text);

    const tagEl = document.createElement("span");
    tagEl.className = "je-tag";
    tagEl.textContent = text;

    const removeBtn = document.createElement("button");
    removeBtn.type = "button";
    removeBtn.className = "je-tag-remove";
    removeBtn.textContent = "×";
    removeBtn.addEventListener("click", () => this.removeTag(text));

    tagEl.appendChild(removeBtn);

    this.tagsContainer.insertBefore(tagEl, this.input);
    this.input.value = "";

    this.updateHidden();
    this.emitChange();
  }

  removeTag(text) {
    this.tags = this.tags.filter(t => t !== text);
    [...this.tagsContainer.querySelectorAll(".je-tag")].forEach(tagEl => {
      if (tagEl.firstChild.nodeValue === text) {
        tagEl.remove();
      }
    });
    this.updateHidden();
    this.emitChange();
  }

  updateHidden() {
    this.hiddenInput.value = this.tags.join(",");
  }

  emitChange() {
    this.root.dispatchEvent(new CustomEvent("je:change", {
      detail: { tags: this.tags },
      bubbles: true
    }));
  }

  getTags() {
    return [...this.tags];
  }
}

JERegistry.register(".je-tag-input", JETagInput);
```

## - **je-datepicker:** calendario interactivo para seleccionar fechas con límites mínimos y máximos.  

```js
class JEDatePicker extends JEComponent {
  init() {
    this.labelText = this.root.dataset.label || "Fecha";
    this.format = this.root.dataset.format || "dd/mm/yyyy";
    this.minDate = this.root.dataset.min || null;
    this.maxDate = this.root.dataset.max || null;
    this.required = this.root.dataset.required === "true";
    
    this.selectedDate = null;
    this.currentMonth = new Date();
    this.isOpen = false;
    
    this.build();
    this.attachEvents();
  }

  build() {
    this.root.classList.add("je-field", "je-datepicker-wrapper");
    
    // Label
    const label = document.createElement("label");
    label.className = "je-label";
    label.textContent = this.labelText + (this.required ? " *" : "");
    
    // Input contenedor
    this.inputContainer = document.createElement("div");
    this.inputContainer.className = "je-datepicker-input";
    
    this.display = document.createElement("input");
    this.display.type = "text";
    this.display.className = "je-input";
    this.display.placeholder = this.format;
    this.display.readOnly = true;
    
    this.calendarIcon = document.createElement("span");
    this.calendarIcon.className = "je-datepicker-icon";
    this.calendarIcon.innerHTML = "📅";
    
    this.inputContainer.appendChild(this.display);
    this.inputContainer.appendChild(this.calendarIcon);
    
    // Calendario desplegable
    this.calendar = document.createElement("div");
    this.calendar.className = "je-datepicker-calendar";
    this.calendar.style.display = "none";
    
    // Ensamblar
    this.root.innerHTML = "";
    this.root.appendChild(label);
    this.root.appendChild(this.inputContainer);
    this.root.appendChild(this.calendar);
    
    this.renderCalendar();
  }

  attachEvents() {
    // Abrir/cerrar calendario
    this.inputContainer.addEventListener("click", () => {
      this.toggleCalendar();
    });
    
    // Cerrar al hacer click fuera
    document.addEventListener("click", (e) => {
      if (!this.root.contains(e.target) && this.isOpen) {
        this.closeCalendar();
      }
    });
  }

  toggleCalendar() {
    if (this.isOpen) {
      this.closeCalendar();
    } else {
      this.openCalendar();
    }
  }

  openCalendar() {
    this.calendar.style.display = "block";
    this.isOpen = true;
    this.renderCalendar();
  }

  closeCalendar() {
    this.calendar.style.display = "none";
    this.isOpen = false;
  }

  renderCalendar() {
    const year = this.currentMonth.getFullYear();
    const month = this.currentMonth.getMonth();
    
    // Header del calendario
    const header = document.createElement("div");
    header.className = "je-datepicker-header";
    
    const prevBtn = document.createElement("button");
    prevBtn.type = "button";
    prevBtn.className = "je-datepicker-nav";
    prevBtn.innerHTML = "‹";
    prevBtn.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      this.currentMonth = new Date(year, month - 1, 1);
      this.renderCalendar();
    });
    
    const monthYear = document.createElement("span");
    monthYear.className = "je-datepicker-month";
    monthYear.textContent = this.getMonthName(month) + " " + year;
    
    const nextBtn = document.createElement("button");
    nextBtn.type = "button";
    nextBtn.className = "je-datepicker-nav";
    nextBtn.innerHTML = "›";
    nextBtn.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      this.currentMonth = new Date(year, month + 1, 1);
      this.renderCalendar();
    });
    
    header.appendChild(prevBtn);
    header.appendChild(monthYear);
    header.appendChild(nextBtn);
    
    // Días de la semana
    const weekdays = document.createElement("div");
    weekdays.className = "je-datepicker-weekdays";
    ["Lu", "Ma", "Mi", "Ju", "Vi", "Sá", "Do"].forEach(day => {
      const dayEl = document.createElement("div");
      dayEl.textContent = day;
      weekdays.appendChild(dayEl);
    });
    
    // Días del mes
    const days = document.createElement("div");
    days.className = "je-datepicker-days";
    
    // Primer día del mes
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    
    // Ajustar para que lunes sea 0
    const startDay = firstDay === 0 ? 6 : firstDay - 1;
    
    // Días vacíos al inicio
    for (let i = 0; i < startDay; i++) {
      const emptyDay = document.createElement("div");
      emptyDay.className = "je-datepicker-day je-datepicker-day-empty";
      days.appendChild(emptyDay);
    }
    
    // Días del mes
    for (let day = 1; day <= daysInMonth; day++) {
      const dayEl = document.createElement("div");
      dayEl.className = "je-datepicker-day";
      dayEl.textContent = day;
      
      const currentDate = new Date(year, month, day);
      
      // Verificar si es el día seleccionado
      if (this.selectedDate && this.isSameDay(currentDate, this.selectedDate)) {
        dayEl.classList.add("je-datepicker-day-selected");
      }
      
      // Verificar si es hoy
      if (this.isSameDay(currentDate, new Date())) {
        dayEl.classList.add("je-datepicker-day-today");
      }
      
      // Verificar si está fuera del rango
      if (this.isDateDisabled(currentDate)) {
        dayEl.classList.add("je-datepicker-day-disabled");
      } else {
        dayEl.addEventListener("click", (e) => {
          e.preventDefault();
          e.stopPropagation();
          this.selectDate(currentDate);
        });
      }
      
      days.appendChild(dayEl);
    }
    
    // Limpiar y renderizar (pero mantener display)
    const currentDisplay = this.calendar.style.display;
    this.calendar.innerHTML = "";
    this.calendar.appendChild(header);
    this.calendar.appendChild(weekdays);
    this.calendar.appendChild(days);
    this.calendar.style.display = currentDisplay;
  }

  selectDate(date) {
    this.selectedDate = date;
    this.display.value = this.formatDate(date);
    this.closeCalendar();
    
    this.root.dispatchEvent(new CustomEvent("je:date:change", {
      detail: { date: date, formatted: this.formatDate(date) },
      bubbles: true
    }));
  }

  formatDate(date) {
    const day = String(date.getDate()).padStart(2, "0");
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const year = date.getFullYear();
    
    return this.format
      .replace("dd", day)
      .replace("mm", month)
      .replace("yyyy", year);
  }

  isSameDay(date1, date2) {
    return date1.getDate() === date2.getDate() &&
           date1.getMonth() === date2.getMonth() &&
           date1.getFullYear() === date2.getFullYear();
  }

  isDateDisabled(date) {
    if (this.minDate) {
      const min = new Date(this.minDate);
      if (date < min) return true;
    }
    if (this.maxDate) {
      const max = new Date(this.maxDate);
      if (date > max) return true;
    }
    return false;
  }

  getMonthName(month) {
    const months = [
      "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
      "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ];
    return months[month];
  }

  getValue() {
    return this.selectedDate;
  }

  setValue(date) {
    if (date instanceof Date) {
      this.selectDate(date);
    } else if (typeof date === "string") {
      this.selectDate(new Date(date));
    }
  }
}

JERegistry.register(".je-datepicker", JEDatePicker);
```

## - **je-progress-bar:** barra de progreso animada y configurable.  

```js
class JEProgressBar extends JEComponent {
  init() {
    this.labelText = this.root.dataset.label || "";
    this.value = parseFloat(this.root.dataset.value || 0);
    this.max = parseFloat(this.root.dataset.max || 100);
    this.showPercentage = this.root.dataset.showPercentage === "true";
    this.color = this.root.dataset.color || "primary"; // primary, success, warning, danger
    this.striped = this.root.dataset.striped === "true";
    this.animated = this.root.dataset.animated === "true";
    
    this.build();
  }

  build() {
    this.root.classList.add("je-progress-wrapper");
    
    // Label y porcentaje
    if (this.labelText || this.showPercentage) {
      const header = document.createElement("div");
      header.className = "je-progress-header";
      
      if (this.labelText) {
        const label = document.createElement("span");
        label.className = "je-progress-label";
        label.textContent = this.labelText;
        header.appendChild(label);
      }
      
      if (this.showPercentage) {
        this.percentageEl = document.createElement("span");
        this.percentageEl.className = "je-progress-percentage";
        this.percentageEl.textContent = this.getPercentage() + "%";
        header.appendChild(this.percentageEl);
      }
      
      this.root.appendChild(header);
    }
    
    // Barra contenedora
    this.container = document.createElement("div");
    this.container.className = "je-progress-container";
    
    // Barra de progreso
    this.bar = document.createElement("div");
    this.bar.className = `je-progress-bar je-progress-${this.color}`;
    
    if (this.striped) {
      this.bar.classList.add("je-progress-striped");
    }
    
    if (this.animated) {
      this.bar.classList.add("je-progress-animated");
    }
    
    this.updateBar();
    
    this.container.appendChild(this.bar);
    this.root.appendChild(this.container);
  }

  updateBar() {
    const percentage = this.getPercentage();
    this.bar.style.width = percentage + "%";
    
    if (this.percentageEl) {
      this.percentageEl.textContent = percentage + "%";
    }
    
    // Actualizar atributo aria
    this.bar.setAttribute("role", "progressbar");
    this.bar.setAttribute("aria-valuenow", this.value);
    this.bar.setAttribute("aria-valuemin", "0");
    this.bar.setAttribute("aria-valuemax", this.max);
  }

  getPercentage() {
    return Math.round((this.value / this.max) * 100);
  }

  setValue(value) {
    this.value = Math.max(0, Math.min(value, this.max));
    this.updateBar();
    
    // Emitir evento
    this.root.dispatchEvent(new CustomEvent("je:progress:change", {
      detail: { value: this.value, percentage: this.getPercentage() },
      bubbles: true
    }));
  }

  increment(amount = 1) {
    this.setValue(this.value + amount);
  }

  decrement(amount = 1) {
    this.setValue(this.value - amount);
  }

  setMax(max) {
    this.max = max;
    this.updateBar();
  }

  setColor(color) {
    this.bar.classList.remove(`je-progress-${this.color}`);
    this.color = color;
    this.bar.classList.add(`je-progress-${this.color}`);
  }

  complete() {
    this.setValue(this.max);
  }

  reset() {
    this.setValue(0);
  }
}

JERegistry.register(".je-progress-bar", JEProgressBar);
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

Ejemplo del `je-progress-bar`:
```html
<div class="je-progress-bar" 
     data-value="65" 
     data-max="100" 
     data-label="Progreso del pedido"
     data-show-percentage="true"
     data-striped="true" 
     data-animated="true"></div>
```

---

```js
// Base para todos los componentes JE
class JEComponent {
  constructor(root) {
    this.root = root;
  }

  init() {
    // Implementar en cada componente
  }

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
}

// Registro de componentes
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

// Inicialización automática al cargar DOM
document.addEventListener("DOMContentLoaded", () => {
  JERegistry.initAll();
});
```

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>jEnterpriseUI - Demo librería</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/jenterpriseui.css">
</head>
<body>
  <div class="je-layout">
    <aside class="je-sidebar">
      <h1>jEnterpriseUI</h1>
      <nav>
        <a href="#formulario">Formulario de alta</a>
        <a href="#listado">Listado de pedidos</a>
        <a href="#componentes-extra">Componentes adicionales</a>
      </nav>
    </aside>

    <main class="je-main">
      <header class="je-header">
        <div>
          <div class="je-header-title">Librería de componentes UI empresariales</div>
          <div class="je-header-subtitle">
            Ejercicio final U1 · Controles avanzados + datos externos + reutilización
          </div>
        </div>
      </header>

      <section id="formulario" class="je-card">
        <h2>Formulario de alta de pedido</h2>
        <p style="font-size:0.85rem; color:#6b7280;">
          Ejemplo de uso de <code>.je-select-remote</code> enlazado a datos JSON.
        </p>
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

        <!-- Etiquetas internas -->
        <div class="je-tag-input"
            data-label="Etiquetas internas"
            data-placeholder="Añade etiquetas y pulsa Enter"
            data-name="tags"
            data-max="5">
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
      </section>

      <!-- NUEVOS COMPONENTES -->
      <section id="componentes-extra" class="je-card">
        <h2>Componentes adicionales</h2>
        <p style="font-size:0.85rem; color:#6b7280;">
          Nuevos componentes: DatePicker, CheckboxGroup, ProgressBar y Modal.
        </p>

        <!-- DatePicker -->
        <div class="je-datepicker"
             data-label="Fecha de entrega"
             data-format="dd/mm/yyyy"
             data-min="2025-01-01"
             data-max="2025-12-31"
             data-required="true">
        </div>

        <!-- CheckboxGroup -->
        <div class="je-checkbox-group"
             data-label="Opciones de envío"
             data-options='[{"value":"express","label":"Envío Express"},{"value":"normal","label":"Envío Normal"},{"value":"recogida","label":"Recogida en tienda"}]'
             data-name="envio"
             data-layout="vertical"
             data-min-checked="1">
        </div>

        <!-- ProgressBar -->
        <div class="je-progress-bar"
             data-value="65"
             data-max="100"
             data-label="Progreso del pedido"
             data-show-percentage="true"
             data-color="primary"
             data-striped="true"
             data-animated="true">
        </div>

        <!-- Botón para abrir modal -->
        <button onclick="document.querySelector('.je-modal').__jeInstance.open()" 
                class="je-btn je-btn-primary">
          🔔 Abrir Modal de confirmación
        </button>
      </section>
    </main>
  </div>

  <!-- MODAL (fuera del layout principal) -->
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
    <script src="js/je-tag-input.js"></script>
    <script src="js/je-table.js"></script>
    <script src="js/je-modal.js"></script>
    <script src="js/je-datepicker.js"></script>
    <script src="js/je-checkbox-group.js"></script>
    <script src="js/je-progress-bar.js"></script>
</body>
</html>
```

La librería se aplica en el archivo principal `index.html`, donde se crean formularios empresariales reutilizando los componentes definidos.  
Por ejemplo, el formulario de alta de pedido combina varios de ellos:

```html
<div class="je-textfield" data-label="Nombre del pedido" data-required="true"></div>
<div class="je-select-remote" data-label="Cliente" data-src="data/clientes.json"></div>
<div class="je-tag-input" data-label="Etiquetas internas"></div>
```

Además, se enlazaron los componentes a archivos JSON reales (`clientes.json` y `pedidos.json`) para simular la carga de datos desde un servidor, logrando así un flujo de trabajo similar al de una aplicación real.

---

Este ejercicio me ha permitido comprender cómo se construyen librerías de componentes de interfaz de usuario desde cero y cómo se aplican en un entorno empresarial.  
He aprendido la importancia de **estructurar el código en módulos reutilizables**, usar el **DOM de forma dinámica** y mantener la **coherencia visual y funcional** en todos los elementos.  
Estos conceptos se relacionan directamente con el contenido de la **Unidad 1 de Desarrollo de Interfaces**, centrada en la creación y reutilización de componentes visuales que optimizan la experiencia del usuario y facilitan el mantenimiento del software.
