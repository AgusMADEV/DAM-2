class JETable extends JEComponent {
  init() {
    this.src = this.root.dataset.src;               // URL JSON
    this.captionText = this.root.dataset.caption || "";
    this.sortable = this.root.dataset.sortable === "true";

    if (!this.src) {
      this.setError("Falta el atributo data-src con la ruta al JSON.");
      return;
    }

    this.buildBase();
    this.loadData();
  }

  buildBase() {
    this.root.classList.add("je-table-wrapper");
    this.table = document.createElement("table");
    this.table.className = "je-table";

    if (this.captionText) {
      const cap = document.createElement("caption");
      cap.textContent = this.captionText;
      this.table.appendChild(cap);
    }

    this.thead = document.createElement("thead");
    this.tbody = document.createElement("tbody");
    this.table.appendChild(this.thead);
    this.table.appendChild(this.tbody);

    this.root.innerHTML = "";
    this.root.appendChild(this.table);
  }

  async loadData() {
    try {
      this.setLoading(true);
      this.setError(null);

      const res = await fetch(this.src);
      if (!res.ok) throw new Error("No se pudo cargar la tabla");
      const data = await res.json();

      if (!Array.isArray(data) || data.length === 0) {
        this.setError("No hay datos para mostrar.");
        return;
      }

      this.renderTable(data);
    } catch (err) {
      this.setError("Error al cargar datos.");
      console.error(err);
    } finally {
      this.setLoading(false);
    }
  }

  renderTable(data) {
    this.data = data;
    const keys = Object.keys(data[0]); // columnas por las claves del primer objeto

    // Cabecera
    this.thead.innerHTML = "";
    const trHead = document.createElement("tr");

    keys.forEach(key => {
      const th = document.createElement("th");
      th.textContent = key;
      if (this.sortable) {
        th.classList.add("je-sortable");
        th.addEventListener("click", () => this.sortBy(key, th));
      }
      trHead.appendChild(th);
    });

    this.thead.appendChild(trHead);

    // Cuerpo
    this.fillBody(this.data, keys);
  }

  fillBody(rows, keys) {
    this.tbody.innerHTML = "";

    rows.forEach(row => {
      const tr = document.createElement("tr");
      keys.forEach(key => {
        const td = document.createElement("td");
        td.textContent = row[key];
        tr.appendChild(td);
      });
      this.tbody.appendChild(tr);
    });
  }

  sortBy(key, th) {
    // Alternar orden
    const currentOrder = th.dataset.order || "none";
    const newOrder = currentOrder === "asc" ? "desc" : "asc";
    th.dataset.order = newOrder;

    // Reset visual de otros
    this.thead.querySelectorAll("th").forEach(h => {
      if (h !== th) h.dataset.order = "none";
    });

    const sorted = [...this.data].sort((a, b) => {
      if (a[key] < b[key]) return newOrder === "asc" ? -1 : 1;
      if (a[key] > b[key]) return newOrder === "asc" ? 1 : -1;
      return 0;
    });

    this.fillBody(sorted, Object.keys(this.data[0]));
  }
}

JERegistry.register(".je-table", JETable);
