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
