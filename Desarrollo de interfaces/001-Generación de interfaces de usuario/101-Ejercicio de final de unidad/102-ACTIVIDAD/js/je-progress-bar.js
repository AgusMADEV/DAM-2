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
