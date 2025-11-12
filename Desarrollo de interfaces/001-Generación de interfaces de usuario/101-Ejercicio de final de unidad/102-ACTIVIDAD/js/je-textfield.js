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
