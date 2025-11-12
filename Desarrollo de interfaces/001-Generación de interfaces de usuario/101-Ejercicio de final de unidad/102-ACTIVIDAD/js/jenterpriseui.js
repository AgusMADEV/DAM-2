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
