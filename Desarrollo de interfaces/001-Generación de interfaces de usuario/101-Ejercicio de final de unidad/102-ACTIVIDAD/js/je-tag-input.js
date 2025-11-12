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
