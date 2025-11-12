/**
 * Componente CheckboxGroup (grupo de checkboxes)
 * 
 * Uso:
 * <div class="je-checkbox-group"
 *      data-label="Selecciona opciones"
 *      data-options='[{"value":"op1","label":"Opción 1"},{"value":"op2","label":"Opción 2"}]'
 *      data-name="opciones"
 *      data-layout="vertical">
 * </div>
 */
class JECheckboxGroup extends JEComponent {
  init() {
    this.labelText = this.root.dataset.label || "Opciones";
    this.name = this.root.dataset.name || "checkbox-group";
    this.layout = this.root.dataset.layout || "vertical"; // vertical, horizontal
    this.required = this.root.dataset.required === "true";
    this.minChecked = this.root.dataset.minChecked ? parseInt(this.root.dataset.minChecked, 10) : null;
    this.maxChecked = this.root.dataset.maxChecked ? parseInt(this.root.dataset.maxChecked, 10) : null;
    
    // Parsear opciones
    try {
      this.options = JSON.parse(this.root.dataset.options || "[]");
    } catch (e) {
      this.options = [];
      this.setError("Error al parsear opciones");
    }
    
    this.selectedValues = [];
    this.build();
  }

  build() {
    this.root.classList.add("je-field", "je-checkbox-group-wrapper");
    
    // Label principal
    const label = document.createElement("label");
    label.className = "je-label";
    label.textContent = this.labelText + (this.required ? " *" : "");
    
    // Contenedor de checkboxes
    this.container = document.createElement("div");
    this.container.className = `je-checkbox-group je-checkbox-group-${this.layout}`;
    
    // Crear checkboxes
    this.checkboxes = [];
    this.options.forEach((option, index) => {
      const itemWrapper = document.createElement("div");
      itemWrapper.className = "je-checkbox-item";
      
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.className = "je-checkbox";
      checkbox.id = `${this.name}-${index}`;
      checkbox.name = this.name;
      checkbox.value = option.value;
      
      const itemLabel = document.createElement("label");
      itemLabel.className = "je-checkbox-label";
      itemLabel.htmlFor = checkbox.id;
      itemLabel.textContent = option.label;
      
      checkbox.addEventListener("change", () => this.handleChange(checkbox));
      
      itemWrapper.appendChild(checkbox);
      itemWrapper.appendChild(itemLabel);
      this.container.appendChild(itemWrapper);
      
      this.checkboxes.push(checkbox);
    });
    
    // Ensamblar
    this.root.innerHTML = "";
    this.root.appendChild(label);
    this.root.appendChild(this.container);
  }

  handleChange(checkbox) {
    this.updateSelectedValues();
    
    // Validar límites
    if (this.maxChecked && this.selectedValues.length > this.maxChecked) {
      checkbox.checked = false;
      this.updateSelectedValues();
      this.setError(`Máximo ${this.maxChecked} opciones`);
      return;
    }
    
    this.setError(null);
    
    // Emitir evento
    this.root.dispatchEvent(new CustomEvent("je:checkbox:change", {
      detail: { values: this.selectedValues },
      bubbles: true
    }));
  }

  updateSelectedValues() {
    this.selectedValues = this.checkboxes
      .filter(cb => cb.checked)
      .map(cb => cb.value);
  }

  validate() {
    if (this.required && this.selectedValues.length === 0) {
      this.setError("Debes seleccionar al menos una opción");
      return false;
    }
    
    if (this.minChecked && this.selectedValues.length < this.minChecked) {
      this.setError(`Selecciona al menos ${this.minChecked} opciones`);
      return false;
    }
    
    this.setError(null);
    return true;
  }

  getValue() {
    return this.selectedValues;
  }

  setValue(values) {
    this.checkboxes.forEach(cb => {
      cb.checked = values.includes(cb.value);
    });
    this.updateSelectedValues();
  }
}

JERegistry.register(".je-checkbox-group", JECheckboxGroup);
