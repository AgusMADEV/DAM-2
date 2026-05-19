/*!
 * static/jocarsaux.js
 * FK-aware CRUD table + left nav
 *
 * Expected backend routes:
 *  GET  /tablas                           -> [{tabla:"clientes"}, ...]
 *  GET  /seleccionar_humano/:tabla        -> { rows:[{...}], meta:{ pk:"id", fks:[{col,ref_table,ref_column,label_column}] } }
 *  GET  /fk_options/:tabla                -> { fkcol: [ {value, label}, ... ], ... }
 *  POST /insertar/:tabla                  -> body JSON {col: value, ...}
 *  PUT  /actualizar/:tabla/:pk            -> body JSON {col: value, ...} (supports single-field)
 *  DELETE /eliminar/:tabla/:pk
 */

(function (global) {
  "use strict";

  const NAMESPACE = "jux";
  const NS = (name) => `${NAMESPACE}-${name}`;

  // ---------------- Styles ----------------
  function ensureStyles() {
    const id = `${NAMESPACE}-styles`;
    if (document.getElementById(id)) return;

    const css = `
:root { --jux-bg:#ffffff; --jux-text:#0f172a; --jux-muted:#475569; --jux-line:#e2e8f0; --jux-chip:#f8fafc; --jux-accent:#dc143c; }
.${NS("root")} { font:14px/1.5 system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Cantarell,Noto Sans,Arial; color:var(--jux-text); }
.${NS("wrap")} { max-width:1000px; margin:32px auto; padding:0 16px; }
.${NS("title")} { margin:0 0 6px; font-size:clamp(18px,3.5vw,26px); }
.${NS("subtitle")} { margin:0 0 14px; color:var(--jux-muted); }
.${NS("card")} { border:1px solid var(--jux-line); border-radius:12px; overflow:hidden; background:#fff }
.${NS("pad")} { padding:14px }
.${NS("toolbar")} { display:flex; gap:10px; align-items:center; justify-content:space-between; flex-wrap:wrap }
.${NS("badge")} { display:inline-block; background:var(--jux-chip); padding:2px 8px; border:1px solid var(--jux-line); border-radius:999px; font-size:12px; color:var(--jux-muted) }
.${NS("search")} { display:flex; gap:8px; align-items:center }
.${NS("search")} input { border:1px solid var(--jux-line); border-radius:10px; padding:8px 10px; min-width:220px }
.${NS("count")} { font-size:12px; color:var(--jux-muted) }
.${NS("scroll")} { max-height:70vh; overflow:auto; border-top:1px solid var(--jux-line) }
.${NS("table")} { width:100%; border-collapse:separate; border-spacing:0; font-size:14px }
.${NS("thead")} th { position:sticky; top:0; background:linear-gradient(0deg,#f8fafc,#ffffff); border-bottom:1px solid var(--jux-line); text-align:left; font-weight:700; padding:10px 12px; white-space:nowrap }
.${NS("th-sortable")} { cursor:pointer; user-select:none }
.${NS("th-sortable")} .${NS("dir")} { margin-left:6px; font-size:11px; color:var(--jux-muted) }
.${NS("tbody")} td { border-bottom:1px solid var(--jux-line); padding:10px 12px; vertical-align:top }
.${NS("row-odd")} { background:#fafafa }
.${NS("pagination")} { display:flex; gap:8px; align-items:center; justify-content:center; padding:16px; border-top:1px solid var(--jux-line) }
.${NS("page-btn")} { padding:6px 12px; border:1px solid var(--jux-line); border-radius:6px; background:#fff; cursor:pointer; font:inherit; transition:all 0.2s }
.${NS("page-btn")}:hover:not(:disabled) { background:var(--jux-chip) }
.${NS("page-btn")}:disabled { opacity:0.5; cursor:not-allowed }
.${NS("page-btn-active")} { background:var(--jux-text); color:#fff; border-color:var(--jux-text) }
.${NS("page-info")} { font-size:13px; color:var(--jux-muted); margin:0 8px }
.${NS("table-area")} {}
.${NS("form-area")} { padding:16px; }
.${NS("form")} { padding:20px }
.${NS("form-grid")} { display:grid; gap:20px; grid-template-columns:repeat(2, minmax(0, 1fr)); }
.${NS("field")} { margin:0 }
.${NS("label")} { display:block; margin-bottom:6px; font-weight:600; color:var(--jux-text); font-size:13px }
.${NS("input")}, .${NS("textarea")}, .${NS("select")} { width:100%; border:1px solid var(--jux-line); border-radius:8px; padding:10px 12px; font:inherit; color:var(--jux-text); transition:border-color 0.2s }
.${NS("input")}:focus, .${NS("textarea")}:focus, .${NS("select")}:focus { outline:none; border-color:#94a3b8 }
.${NS("textarea")} { min-height:100px; resize:vertical; font-family:inherit }
.${NS("select")} { cursor:pointer }
.${NS("btn-group")} { display:flex; gap:10px; margin-top:24px; padding-top:20px; border-top:1px solid var(--jux-line); grid-column:1/-1 }
.${NS("btn")} { padding:10px 20px; border:1px solid var(--jux-line); border-radius:8px; font:inherit; cursor:pointer; transition:all 0.2s }
.${NS("btn-primary")} { background:var(--jux-text); color:#fff; border-color:var(--jux-text) }
.${NS("btn-primary")}:hover { background:#1e293b }
.${NS("btn-secondary")} { background:#fff; color:var(--jux-text) }
.${NS("btn-secondary")}:hover { background:var(--jux-chip) }
.${NS("cell-editable")} { cursor:text; border-bottom:1px dashed #ddd; }
.${NS("readonly")} { background:#f5f5f5; }
.${NS("menu")} { display:flex; flex-direction:column; gap:10px; padding:20px; background:var(--jux-accent); color:#fff; }
.${NS("menu-title")} { font-size:18px; font-weight:700; margin-bottom:10px; }
.${NS("menu-section")} { display:flex; flex-direction:column; gap:8px }
.${NS("menu-btn")} { background:#fff; color:#000; border:none; padding:10px 16px; border-radius:999px; cursor:pointer; text-align:left; }
.${NS("menu-btn")}:hover { background:rgba(255,255,255,.85); }
.${NS("menu-btn-active")} { background:#000; color:#fff; }
`;
    const style = document.createElement("style");
    style.id = id;
    style.textContent = css;
    document.head.appendChild(style);
  }

  // ---------------- Helpers ----------------
  const el = (tag, className, text) => {
    const x = document.createElement(tag);
    if (className) x.className = className;
    if (text != null) x.textContent = text;
    return x;
  };
  const isPlain = (v) => Object.prototype.toString.call(v) === "[object Object]";
  const normalizeTop = (data) => (Array.isArray(data) ? data : (isPlain(data) ? [data] : []));
  const collectColumns = (rows) => {
    const s = new Set();
    rows.forEach((r) => Object.keys(r).forEach((k) => s.add(k)));
    return [...s];
  };

  const getJSON = (url) =>
    fetch(url, { headers: { Accept: "application/json" } }).then((r) => r.json().catch(() => ({})));
  const sendJSON = (url, method, bodyObj) =>
    fetch(url, {
      method,
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: bodyObj ? JSON.stringify(bodyObj) : undefined,
    }).then((r) => r.json().catch(() => ({})).then((json) => ({ ok: r.ok, status: r.status, json })));

  // ---------------- JocarsaUX ----------------
  class JocarsaUX {
    constructor() {
      ensureStyles();
      this.state = {
        columns: [],
        rows: [],
        view: [],
        sort: { key: null, dir: 1 },
        query: "",
        page: 1,
        rowsPerPage: 10,
        currentTable: null,
        meta: { pk: null, fks: [] },
        fkOptions: {},
      };
      this._els = {};
    }

    // -------- Left nav --------
    menuRenderer({ target, items = [], title = "Tablas", onItemClick = null } = {}) {
      const host = typeof target === "string" ? document.querySelector(target) : target;
      if (!host) throw new Error("Target not found");
      host.className = NS("menu");
      host.innerHTML = "";
      if (title) host.appendChild(el("div", NS("menu-title"), title));
      const section = el("div", NS("menu-section"));
      items.forEach((item) => {
        const label = typeof item === "string" ? item : (item.label ?? item.value ?? "");
        const value = typeof item === "string" ? item : (item.value ?? item.label ?? "");
        const btn = el("button", NS("menu-btn"), label);
        btn.onclick = () => {
          host.querySelectorAll(`.${NS("menu-btn")}`).forEach((b) => b.classList.remove(NS("menu-btn-active")));
          btn.classList.add(NS("menu-btn-active"));
          if (onItemClick) onItemClick(value, item);
        };
        section.appendChild(btn);
      });
      host.appendChild(section);
      return this;
    }

    async loadTablesMenu({ target, title = "Tablas", onItemClick }) {
      const j = await getJSON("/tablas");
      const items = Array.isArray(j) ? j.map((x) => x.tabla || x) : [];
      return this.menuRenderer({ target, items, title, onItemClick });
    }

    // -------- Load humanized table + FK options then render --------
    async openTable({ target, tabla, rowsPerPage = 10, subtitle = "Table renderer (search + sort + CRUD)" }) {
      const host = typeof target === "string" ? document.querySelector(target) : target;
      if (!host) throw new Error("Target not found");

      const [human, options] = await Promise.all([
        getJSON(`/seleccionar_humano/${encodeURIComponent(tabla)}`),
        getJSON(`/fk_options/${encodeURIComponent(tabla)}`),
      ]);

      const rows = normalizeTop(human?.rows || []);
      this.state.meta = human?.meta || { pk: null, fks: [] };
      this.state.fkOptions = options || {};
      this.state.currentTable = tabla;

      this.tableRenderer({
        target: host,
        data: rows,
        title: `${tabla} - Table View`,
        subtitle,
        rowsPerPage,
      });
    }

    // -------- Main table renderer with CRUD + FK awareness --------
    tableRenderer({ target, data, title = "jocarsa|ux", subtitle = "Table renderer (search + sort + CRUD)", rowsPerPage = 10 } = {}) {
      const host = typeof target === "string" ? document.querySelector(target) : target;
      if (!host) throw new Error("Target not found");
      host.classList.add(NS("root"));
      host.innerHTML = "";

      // Layout
      const wrap = el("div", NS("wrap"));
      const h1 = el("h1", NS("title"), title);
      const p = el("p", NS("subtitle"), subtitle);
      const card = el("div", NS("card"));
      const pad = el("div", NS("pad"));
      const toolbar = el("div", NS("toolbar"));
      const leftTools = el("div");
      leftTools.style.display = "flex";
      leftTools.style.gap = "8px";
      const addBtn = el("button", `${NS("btn")} ${NS("btn-primary")}`, "+ Add");
      addBtn.type = "button";
      leftTools.append(addBtn);

      const searchBox = el("div", NS("search"));
      const label = el("label", null, "Search");
      label.htmlFor = NS("search-input");
      const input = el("input");
      input.id = NS("search-input");
      const count = el("span", NS("count"));
      searchBox.append(label, input, count);

      toolbar.append(leftTools, searchBox);
      pad.append(toolbar);

      const tableArea = el("div", NS("table-area"));
      const formArea = el("div", NS("form-area"));
      formArea.style.display = "none";

      const scroll = el("div", NS("scroll"));
      const table = el("table", NS("table"));
      const thead = el("thead", NS("thead"));
      const tbody = el("tbody", NS("tbody"));
      table.append(thead, tbody);
      scroll.append(table);

      const paginationDiv = el("div", NS("pagination"));
      tableArea.append(pad, scroll, paginationDiv);

      card.append(tableArea, formArea);
      wrap.append(h1, p, card);
      host.append(wrap);

      // Bind elements
      this._els = {
        host,
        table,
        thead,
        tbody,
        search: input,
        count,
        pagination: paginationDiv,
        tableArea,
        formArea,
      };

      // Data
      const arr = normalizeTop(data);
      this.state.columns = collectColumns(arr);
      this._preferLabelColumns();
      this.state.rows = arr.slice();
      this.state.view = arr.slice();
      this.state.sort = { key: null, dir: 1 };
      this.state.query = "";
      this.state.page = 1;
      this.state.rowsPerPage = rowsPerPage;

      // Handlers
      input.value = "";
      input.oninput = () => this.setFilter(input.value);
      addBtn.onclick = () => this._renderInsertForm();

      // Paint
      this._renderPagination();
      this._renderHead();
      this._renderBody();
      return this;
    }

    _preferLabelColumns() {
      const cols = new Set(this.state.columns);
      for (const c of [...cols]) {
        if (c.endsWith("__label")) {
          const raw = c.replace(/__label$/, "");
          if (cols.has(raw)) cols.delete(raw);
        }
      }
      this.state.columns = [...cols];
    }

    // -------- Filtering / Sorting / Paging --------
    setFilter(q) {
      const query = (q || "").toLowerCase();
      this.state.query = query;
      if (!query) {
        this.state.view = this.state.rows.slice();
      } else {
        this.state.view = this.state.rows.filter((r) =>
          this.state.columns.some((c) => (r[c] ?? "").toString().toLowerCase().includes(query))
        );
      }
      this.state.page = 1;
      this._renderBody();
      if (this._els.count) this._els.count.textContent = `${this.state.view.length} row(s)`;
    }

    sortBy(key) {
      const s = this.state.sort;
      if (s.key === key) s.dir = -s.dir;
      else {
        s.key = key;
        s.dir = 1;
      }
      const dir = s.dir;
      this.state.view.sort((a, b) => {
        const va = a[key];
        const vb = b[key];
        if (va == null && vb == null) return 0;
        if (va == null) return 1;
        if (vb == null) return -1;
        return String(va).localeCompare(String(vb), undefined, { numeric: true }) * dir;
      });
      this._renderBody();
    }

    _renderPagination() {
      const p = this._els.pagination;
      p.innerHTML = "";
      const { view, page, rowsPerPage } = this.state;
      const totalPages = Math.max(1, Math.ceil(view.length / rowsPerPage));
      const prev = el("button", NS("page-btn"), "← Previous");
      const next = el("button", NS("page-btn"), "Next →");
      const info = el("span", NS("page-info"), `Page ${page} of ${totalPages}`);
      prev.disabled = page <= 1;
      next.disabled = page >= totalPages;
      prev.onclick = () => {
        if (this.state.page > 1) {
          this.state.page--;
          this._renderBody();
        }
      };
      next.onclick = () => {
        if (this.state.page < totalPages) {
          this.state.page++;
          this._renderBody();
        }
      };
      p.append(prev, info, next);
      this._els.pageInfo = info;
    }

    _renderHead() {
      const { columns, sort } = this.state;
      const thead = this._els.thead;
      thead.innerHTML = "";
      const tr = document.createElement("tr");
      columns.forEach((c) => {
        const th = document.createElement("th");
        th.className = NS("th-sortable");
        th.textContent = c;
        const dir = el("span", NS("dir"), sort.key === c ? (sort.dir === 1 ? "▲" : "▼") : "");
        th.append(dir);
        th.addEventListener("click", () => this.sortBy(c));
        tr.append(th);
      });
      const thActions = document.createElement("th");
      thActions.textContent = "Actions";
      tr.append(thActions);
      thead.append(tr);
    }

    _renderBody() {
      const { columns, view, page, rowsPerPage } = this.state;
      const tbody = this._els.tbody;
      tbody.innerHTML = "";
      const start = (page - 1) * rowsPerPage;
      const end = start + rowsPerPage;
      const pageData = view.slice(start, end);

      const pk = this.state.meta?.pk || (columns.includes("id") ? "id" : columns[0]);
      const tabla = this.state.currentTable;

      const frag = document.createDocumentFragment();
      pageData.forEach((r, idx) => {
        const tr = document.createElement("tr");
        if (idx % 2 === 0) tr.classList.add(NS("row-odd"));

        columns.forEach((c) => {
          const td = document.createElement("td");
          td.textContent = r[c] ?? "";
          if (c !== pk) {
            td.classList.add(NS("cell-editable"));
            td.title = "Double-click to edit";
            td.ondblclick = () => {
              if (td.querySelector("input,textarea,select")) return;

              if (this._isFkLabelCol(c)) {
                // FK label -> edit raw FK with a select
                const rawCol = c.replace(/__label$/, "");
                const options = this.state.fkOptions?.[rawCol] || [];
                const currentId = r[rawCol];
                const select = document.createElement("select");
                select.className = NS("select");
                const empty = document.createElement("option");
                empty.value = "";
                empty.textContent = "-- Selecciona --";
                select.appendChild(empty);
                options.forEach((o) => {
                  const opt = document.createElement("option");
                  opt.value = o.value;
                  opt.textContent = o.label;
                  if (String(o.value) === String(currentId)) opt.selected = true;
                  select.appendChild(opt);
                });
                td.innerHTML = "";
                td.append(select);
                select.focus();

                const commit = () => {
                  const newId = select.value === "" ? null : select.value;
                  if (String(newId) === String(currentId)) {
                    td.textContent = r[c] ?? "";
                    return;
                  }
                  const pkValue = r[pk];
                  const body = {};
                  body[rawCol] = newId;
                  sendJSON(`/actualizar/${encodeURIComponent(tabla)}/${encodeURIComponent(pkValue)}`, "PUT", body)
                    .then(({ ok, status, json }) => {
                      if (ok && !json.error) {
                        r[rawCol] = newId;
                        const chosen = options.find((o) => String(o.value) === String(newId));
                        r[c] = chosen ? chosen.label : "";
                        td.textContent = r[c] ?? "";
                      } else {
                        alert(`Error (${status}): ${json?.mensaje || "FK update failed"}`);
                        td.textContent = r[c] ?? "";
                      }
                    })
                    .catch(() => {
                      alert("Network error");
                      td.textContent = r[c] ?? "";
                    });
                };
                select.addEventListener("blur", commit);
                select.addEventListener("keydown", (ev) => {
                  if (ev.key === "Enter") commit();
                  if (ev.key === "Escape") td.textContent = r[c] ?? "";
                });
              } else {
                const original = r[c] ?? "";
                const isNumber = original !== "" && !isNaN(Number(original));
                const input = document.createElement("input");
                input.type = isNumber ? "number" : "text";
                input.value = original;
                input.style.width = "98%";
                td.innerHTML = "";
                td.append(input);
                input.focus();
                input.select();

                const commit = () => {
                  const newValRaw = input.value;
                  const newVal = newValRaw.trim() === "" ? null : newValRaw;
                  if (String(original ?? "") === String(newValRaw ?? "")) {
                    td.textContent = original ?? "";
                    return;
                  }
                  const pkValue = r[pk];
                  const body = {};
                  body[c] = newVal;
                  sendJSON(`/actualizar/${encodeURIComponent(tabla)}/${encodeURIComponent(pkValue)}`, "PUT", body)
                    .then(({ ok, status, json }) => {
                      if (ok && !json.error) {
                        r[c] = newVal;
                        td.textContent = newValRaw ?? "";
                      } else {
                        alert(`Error (${status}): ${json?.mensaje || "Cell update failed"}`);
                        td.textContent = original ?? "";
                      }
                    })
                    .catch(() => {
                      alert("Network error on cell update");
                      td.textContent = original ?? "";
                    });
                };
                input.addEventListener("blur", commit);
                input.addEventListener("keydown", (ev) => {
                  if (ev.key === "Enter") {
                    ev.preventDefault();
                    commit();
                  }
                  if (ev.key === "Escape") {
                    ev.preventDefault();
                    td.textContent = original ?? "";
                  }
                });
              }
            };
          }
          tr.append(td);
        });

        // Actions
        const tdActions = document.createElement("td");
        const editBtn = el("button", NS("btn"), "Edit");
        editBtn.type = "button";
        editBtn.onclick = () => this._renderEditForm(r);
        const delBtn = el("button", `${NS("btn")} ${NS("btn-secondary")}`, "Delete");
        delBtn.type = "button";
        delBtn.onclick = () => {
          if (!confirm("¿Eliminar este registro?")) return;
          const pkValue = r[pk];
          sendJSON(`/eliminar/${encodeURIComponent(tabla)}/${encodeURIComponent(pkValue)}`, "DELETE")
            .then(({ ok, status, json }) => {
              if (ok && !json.error) {
                this.state.rows = this.state.rows.filter((x) => String(x[pk]) !== String(pkValue));
                this.setFilter(this.state.query || "");
              } else {
                alert(`Error (${status}): ${json?.mensaje || "Delete failed"}`);
              }
            })
            .catch(() => alert("Network error on delete"));
        };
        tdActions.append(editBtn, delBtn);
        tr.append(tdActions);

        frag.append(tr);
      });
      tbody.append(frag);

      const total = this.state.view.length;
      const maxp = Math.max(1, Math.ceil(total / this.state.rowsPerPage));
      if (this._els.pageInfo) this._els.pageInfo.textContent = `Page ${this.state.page} / ${maxp}`;
      if (this._els.count) this._els.count.textContent = `${total} row(s)`;
    }

    // -------- Forms that replace the table --------
    _showForm() { this._els.tableArea.style.display = "none"; this._els.formArea.style.display = "block"; }
    _showTable() { this._els.formArea.style.display = "none"; this._els.tableArea.style.display = "block"; }

    _columnsForForms() {
      const cols = new Set(this.state.columns);
      for (const c of [...cols]) if (c.endsWith("__label")) cols.delete(c);
      return [...cols];
    }

    _renderInsertForm() {
      const tabla = this.state.currentTable;
      const cols = this._columnsForForms();
      const formArea = this._els.formArea;
      formArea.innerHTML = "";

      const frm = el("form", NS("form"));
      const grid = el("div", NS("form-grid"));

      cols.forEach((col) => {
        if (col.toLowerCase() === (this.state.meta?.pk || "").toLowerCase()) return; // skip auto PK
        const f = el("div", NS("field"));
        const lab = el("label", NS("label"), col);
        lab.htmlFor = `${NAMESPACE}-ins-${col}`;

        let input;
        if (this.state.fkOptions && this.state.fkOptions[col]) {
          const sel = document.createElement("select");
          sel.className = NS("select");
          const empty = document.createElement("option");
          empty.value = "";
          empty.textContent = "-- Selecciona --";
          sel.appendChild(empty);
          this.state.fkOptions[col].forEach((o) => {
            const opt = document.createElement("option");
            opt.value = o.value;
            opt.textContent = o.label;
            sel.appendChild(opt);
          });
          input = sel;
        } else {
          input = el("input", NS("input"));
          input.type = "text";
        }
        input.id = `${NAMESPACE}-ins-${col}`;
        input.name = col;

        f.append(lab, input);
        grid.append(f);
      });

      const btns = el("div", NS("btn-group"));
      const saveBtn = el("button", `${NS("btn")} ${NS("btn-primary")}`, "Insert");
      saveBtn.type = "submit";
      const cancelBtn = el("button", `${NS("btn")} ${NS("btn-secondary")}`, "Cancel");
      cancelBtn.type = "button";
      cancelBtn.onclick = () => { this._showTable(); formArea.innerHTML = ""; };
      btns.append(saveBtn, cancelBtn);

      frm.append(grid, btns);
      formArea.append(frm);
      this._showForm();

      frm.onsubmit = (e) => {
        e.preventDefault();
        const payload = {};
        Array.from(frm.elements).forEach((elm) => {
          if (!elm.name) return;
          const v = (typeof elm.value === "string" && elm.value.trim() === "") ? null : elm.value;
          payload[elm.name] = v;
        });
        sendJSON(`/insertar/${encodeURIComponent(tabla)}`, "POST", payload)
          .then(({ ok, status, json }) => {
            if (ok && !json.error) { this._showTable(); this._refreshFromServer(); }
            else { alert(`Error (${status}): ${json?.mensaje || "Insert failed"}`); }
          })
          .catch(() => alert("Network error on insert"));
      };
    }

    _renderEditForm(row) {
      const tabla = this.state.currentTable;
      const pkCol = this.state.meta?.pk || "id";
      const pkValue = row[pkCol];
      const cols = this._columnsForForms();
      const formArea = this._els.formArea;
      formArea.innerHTML = "";

      const frm = el("form", NS("form"));
      const grid = el("div", NS("form-grid"));

      cols.forEach((col) => {
        const f = el("div", NS("field"));
        const lab = el("label", NS("label"), col);
        lab.htmlFor = `${NAMESPACE}-upd-${col}`;

        let input;
        if (this.state.fkOptions && this.state.fkOptions[col]) {
          const sel = document.createElement("select");
          sel.className = NS("select");
          const empty = document.createElement("option");
          empty.value = "";
          empty.textContent = "-- Selecciona --";
          sel.appendChild(empty);
          const currentId = row[col];
          this.state.fkOptions[col].forEach((o) => {
            const opt = document.createElement("option");
            opt.value = o.value;
            opt.textContent = o.label;
            if (String(o.value) === String(currentId)) opt.selected = true;
            sel.appendChild(opt);
          });
          input = sel;
        } else {
          input = el("input", NS("input"));
          input.type = "text";
          input.value = row[col] ?? "";
        }

        input.id = `${NAMESPACE}-upd-${col}`;
        input.name = col;
        if (col === pkCol) { input.readOnly = true; input.classList.add(NS("readonly")); }
        f.append(lab, input);
        grid.append(f);
      });

      const btns = el("div", NS("btn-group"));
      const saveBtn = el("button", `${NS("btn")} ${NS("btn-primary")}`, "Save");
      saveBtn.type = "submit";
      const cancelBtn = el("button", `${NS("btn")} ${NS("btn-secondary")}`, "Cancel");
      cancelBtn.type = "button";
      cancelBtn.onclick = () => { this._showTable(); formArea.innerHTML = ""; };
      btns.append(saveBtn, cancelBtn);

      frm.append(grid, btns);
      formArea.append(frm);
      this._showForm();

      frm.onsubmit = (e) => {
        e.preventDefault();
        const cambios = {};
        Array.from(frm.elements).forEach((elm) => {
          if (!elm.name || elm.readOnly) return;
          const v = (typeof elm.value === "string" && elm.value.trim() === "") ? null : elm.value;
          cambios[elm.name] = v;
        });
        sendJSON(`/actualizar/${encodeURIComponent(tabla)}/${encodeURIComponent(pkValue)}`, "PUT", cambios)
          .then(({ ok, status, json }) => {
            if (ok && !json.error) { this._showTable(); this._refreshFromServer(); }
            else { alert(`Error (${status}): ${json?.mensaje || "Update failed"}`); }
          })
          .catch(() => alert("Network error on update"));
      };
    }

    _isFkLabelCol(c) {
      return c.endsWith("__label") && !!this.state.fkOptions?.[c.replace(/__label$/, "")];
    }

    _refreshFromServer() {
      const tabla = this.state.currentTable;
      Promise.all([
        getJSON(`/seleccionar_humano/${encodeURIComponent(tabla)}`),
        getJSON(`/fk_options/${encodeURIComponent(tabla)}`),
      ])
        .then(([human, options]) => {
          const rows = normalizeTop(human?.rows || []);
          this.state.meta = human?.meta || { pk: null, fks: [] };
          this.state.fkOptions = options || {};
          this.tableRenderer({
            target: this._els.host,
            data: rows,
            title: `${tabla} - Table View`,
            subtitle: "Table renderer (search + sort + CRUD)",
            rowsPerPage: this.state.rowsPerPage,
          });
        })
        .catch(() => alert("Network error refreshing table"));
    }
  }

  // Expose
  global.JocarsaUX = JocarsaUX;       // use: const ux = new JocarsaUX();
  global.jocarsaux = new JocarsaUX(); // or: jocarsaux.openTable({ target:'#main', tabla:'clientes' });

})(window);

