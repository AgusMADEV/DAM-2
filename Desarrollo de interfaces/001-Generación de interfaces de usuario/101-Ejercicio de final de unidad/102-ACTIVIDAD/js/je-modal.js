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
