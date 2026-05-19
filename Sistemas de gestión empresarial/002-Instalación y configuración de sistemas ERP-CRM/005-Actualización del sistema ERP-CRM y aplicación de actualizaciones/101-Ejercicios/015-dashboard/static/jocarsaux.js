/* static/jocarsaux.js
   jocarsa | ux – v16 (dashboard + CRUD con FK human-readable)
   - Tables show labels for *_id using fkcol__label or FK maps
   - Forms render FK fields as <select> with option.value = PK, text = label
   - Opening a form hides the table/pager/toolbar; closing restores them
*/

(() => {
  // -----------------------
  // Utils
  // -----------------------
  const NS_PREFIX = "jux";
  const NS = (x) => `${NS_PREFIX}-${x}`;
  const $ = (sel, root = document) => root.querySelector(sel);

  function el(tag, cls, text) {
    const e = document.createElement(tag);
    if (cls) e.className = Array.isArray(cls) ? cls.join(" ") : cls;
    if (text != null) e.textContent = text;
    return e;
  }

  async function getJSON(url, init = {}) {
    const r = await fetch(url, { headers: { Accept: "application/json" }, ...init });
    if (!r.ok) throw new Error(`${init.method || "GET"} ${url} -> ${r.status}`);
    return r.json();
  }

  async function sendJSON(url, method, data) {
    const r = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: data == null ? null : JSON.stringify(data),
    });
    if (!r.ok) throw new Error(`${method} ${url} -> ${r.status}`);
    return r.json().catch(() => ({}));
  }
  const postJSON = (url, data) => sendJSON(url, "POST", data);
  const putJSON = (url, data) => sendJSON(url, "PUT", data);
  const delJSON = (url) => sendJSON(url, "DELETE", null);

  const debounce = (fn, ms = 250) => {
    let t;
    return (...args) => {
      clearTimeout(t);
      t = setTimeout(() => fn(...args), ms);
    };
  };

  const collectColumns = (rows) => {
    const s = new Set();
    rows.forEach((r) => Object.keys(r || {}).forEach((k) => s.add(k)));
    return Array.from(s);
  };

  // -----------------------
  // Styles (minimal)
  // -----------------------
  function ensureStyles() {
    if (document.getElementById(NS("styles"))) return;
    const css = `
:root{
  --bg:#f6f7fb; --panel:#fff; --line:#e5e7eb; --text:#0f172a; --muted:#6b7280; --accent:#dc143c;
}
.${NS("root")} { padding: 12px; color: var(--text); }
.${NS("wrap")} { max-width: 1200px; margin: 0 auto; }
.${NS("title")} { margin: 8px 4px 12px; font: 600 20px/1.2 system-ui; }
.${NS("subtitle")} { margin: 0 4px 18px; color: var(--muted); }
.${NS("card")} { background: var(--panel); border: 1px solid var(--line); border-radius: 12px; overflow: hidden; }
.${NS("toolbar")} { display:flex; justify-content:space-between; align-items:center; padding:8px; gap:8px; border-bottom:1px solid var(--line); }
.${NS("toolbar-left")}, .${NS("toolbar-right")} { display:flex; gap:8px; align-items:center; }
.${NS("btn")} { appearance:none; border:1px solid var(--line); background:#fff; padding:6px 10px; border-radius:8px; cursor:pointer; }
.${NS("btn")}:hover { background:#fafafa; }
.${NS("btn-primary")} { border-color: transparent; background: var(--accent); color:#fff; }
.${NS("btn-danger")} { border-color: transparent; background: #ef4444; color:#fff; }
.${NS("search")} { display:flex; gap:6px; align-items:center; padding:4px 8px; border:1px solid var(--line); border-radius:8px; }
.${NS("table-wrap")} { overflow:auto; }
.${NS("table")} { border-collapse:collapse; width:100%; }
.${NS("th")}, .${NS("td")} { border-bottom:1px solid var(--line); padding:8px 10px; white-space:nowrap; }
.${NS("pagination")} { display:flex; gap:8px; align-items:center; padding:8px; border-top:1px solid var(--line); }
.${NS("pill")} { padding:2px 8px; border:1px solid var(--line); border-radius:999px; color:var(--muted); }
.${NS("row-actions")} { display:flex; gap:6px; }
.${NS("form")} { padding:10px; border-top:1px solid var(--line); background:#fcfcfd; }
.${NS("form-row")} { display:grid; grid-template-columns:220px 1fr; gap:8px; align-items:center; padding:6px 0; }
.${NS("label")} { color:var(--muted); }
.${NS("input")}, .${NS("select")}, textarea { width:100%; padding:8px; border:1px solid var(--line); border-radius:8px; }
.${NS("empty")} { margin:16px; padding:18px; border:1px dashed var(--line); border-radius:12px; color:var(--muted); background:#fff; }
.${NS("menu")} { padding:10px; }
.${NS("menu-title")} { margin:10px 6px; color:var(--muted); font-weight:600; }
.${NS("menu-section")} { display:flex; flex-direction:column; gap:6px; }
.${NS("menu-btn")} { width:100%; text-align:left; padding:8px 10px; border:1px solid var(--line); border-radius:8px; background:#fff; cursor:pointer; }
.${NS("menu-btn-active")} { background:#111827; color:#fff; border-color:#111827; }
.${NS("grid")} { display:grid; grid-template-columns: repeat(auto-fill,minmax(260px,1fr)); gap:12px; padding:12px; }
.${NS("tile")} { background:#fff; border:1px solid var(--line); border-radius:12px; padding:12px; }
.${NS("tile-head")} { display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; }
.${NS("tile-title")} { font-weight:600; }
.${NS("badge")} { font-size:12px; padding:2px 8px; border:1px solid var(--line); border-radius:999px; color:var(--muted); }
.${NS("legend")} { display:grid; gap:4px; margin-top:6px; }
.${NS("legend-item")} { display:flex; align-items:center; gap:8px; font-size:12px; color:#334155; }
.${NS("legend-swatch")} { width:10px; height:10px; border-radius:2px; border:1px solid rgba(0,0,0,.05); }
    `;
    const s = document.createElement("style");
    s.id = NS("styles");
    s.textContent = css;
    document.head.appendChild(s);
  }

  // -----------------------
  // Charts (lightweight SVGs for dashboard)
  // -----------------------
  const PALETTE = [
    "#a78bfa",
    "#60a5fa",
    "#34d399",
    "#f59e0b",
    "#f472b6",
    "#94a3b8",
    "#fca5a5",
    "#4ade80",
  ];

  const svgEl = (name, attrs = {}) => {
    const n = document.createElementNS("http://www.w3.org/2000/svg", name);
    Object.entries(attrs).forEach(([k, v]) => n.setAttribute(k, String(v)));
    return n;
  };

  function pieChartSVG({ data = [], w = 240, h = 160, r = 55, cx = 80, cy = 80 }) {
    const total = data.reduce((a, d) => a + (d.v || 0), 0) || 1;
    const svg = svgEl("svg", { viewBox: `0 0 ${w} ${h}`, width: "100%", height: h });
    let a0 = -Math.PI / 2;
    data.forEach((d, i) => {
      const frac = (d.v || 0) / total;
      const a1 = a0 + frac * Math.PI * 2;
      const x0 = cx + r * Math.cos(a0),
        y0 = cy + r * Math.sin(a0);
      const x1 = cx + r * Math.cos(a1),
        y1 = cy + r * Math.sin(a1);
      const large = a1 - a0 > Math.PI ? 1 : 0;
      svg.appendChild(
        svgEl("path", {
          d: `M ${cx} ${cy} L ${x0} ${y0} A ${r} ${r} 0 ${large} 1 ${x1} ${y1} Z`,
          fill: PALETTE[i % PALETTE.length],
          stroke: "rgba(0,0,0,.05)",
        })
      );
      a0 = a1;
    });
    return svg;
  }

  function barChartSVG({ data = [], w = 240, h = 120, pad = 10 }) {
    const max = Math.max(...data.map((d) => d.v || 0), 1);
    const svg = svgEl("svg", { viewBox: `0 0 ${w} ${h}`, width: "100%", height: h });
    const bw = (w - pad * 2) / Math.max(data.length, 1);
    svg.appendChild(svgEl("line", { x1: pad, y1: h - pad, x2: w - pad, y2: h - pad, stroke: "#e5e7eb" }));
    data.forEach((d, i) => {
      const bh = (d.v / max) * (h - pad * 2 - 16);
      const x = pad + i * bw,
        y = h - pad - bh;
      svg.appendChild(svgEl("rect", { x, y, width: bw * 0.8, height: bh, rx: 4, ry: 4, fill: "#94a3b8" }));
      const tx = svgEl("text", {
        x: x + bw * 0.4,
        y: h - 2,
        "text-anchor": "middle",
        "font-size": "10",
        fill: "#475569",
      });
      tx.append(document.createTextNode(String(d.k).slice(0, 10)));
      svg.appendChild(tx);
    });
    return svg;
  }

  // -----------------------
  // Main class
  // -----------------------
  class JocarsaUX {
    constructor() {
      ensureStyles();
      this._fkCache = new Map(); // table-level dict cache: FKCOL -> [{value,label}]
      this._fkLabelMap = {}; // per-open-table: col -> Map(value->label)
    }

    // ---------- Navigation
    menuRenderer({ target, title = "Navegación", items = [], onItemClick }) {
      const host = typeof target === "string" ? $(target) : target;
      if (!host) throw new Error("Menu target not found");
      host.innerHTML = "";

      const root = el("div", NS("menu"));
      const h = el("div", NS("menu-title"), title);
      const list = el("div", NS("menu-section"));

      items.forEach((it, idx) => {
        const b = el("button", NS("menu-btn"));
        b.type = "button";
        b.textContent = it.label ?? it.value ?? String(idx);
        b.dataset.value = it.value ?? it.label;
        b.addEventListener("click", () => {
          root.querySelectorAll(`.${NS("menu-btn-active")}`).forEach((n) => n.classList.remove(NS("menu-btn-active")));
          b.classList.add(NS("menu-btn-active"));
          onItemClick && onItemClick(b.dataset.value);
        });
        list.appendChild(b);
      });
      root.append(h, list);
      host.appendChild(root);
    }

    // ---------- Dashboard (auto-summary)
    async dashboardRenderer({ target }) {
      const host = typeof target === "string" ? $(target) : target;
      if (!host) throw new Error("Target not found");
      host.classList.add(NS("root"));
      host.innerHTML = "";

      const wrap = el("div", NS("wrap"));
      const card = el("div", NS("card"));
      wrap.append(el("h1", NS("title"), "dashboard"), el("p", NS("subtitle"), "Resumen automático por tabla y columna"), card);

      const tablas = await getJSON("/tablas")
        .then((r) => (Array.isArray(r) ? r.map((x) => x.tabla || x) : []))
        .catch(() => []);
      if (!tablas.length) {
        wrap.append(el("div", NS("empty"), "No hay tablas."));
        host.append(wrap);
        return;
      }

      const grid = el("div", NS("grid"));

      for (const t of tablas) {
        const res = await getJSON(`/seleccionar_humano/${encodeURIComponent(t)}`).catch(() => null); // uses joined labels
        const rows = Array.isArray(res?.rows) ? res.rows : [];
        const cols = collectColumns(rows).filter((c) => !c.endsWith("__label"));

        const sample = rows.slice(0, 300);
        const textCols = cols.filter((c) => typeof sample.find((r) => r[c] != null)?.[c] === "string");
        const numCols = cols.filter((c) => Number.isFinite(parseFloat(sample.find((r) => r[c] != null)?.[c])));
        if (!textCols.length && !numCols.length) continue;

        const tile = el("div", NS("tile"));
        const head = el("div", NS("tile-head"));
        head.append(el("div", NS("tile-title"), t));
        tile.append(head);

        if (textCols.length) {
          const c = textCols[0];
          const freq = new Map();
          sample.forEach((r) => {
            const k = (r[`${c}__label`] ?? r[c]) ?? "";
            const s = String(k).slice(0, 30);
            freq.set(s, (freq.get(s) || 0) + 1);
          });
          const data = Array.from(freq.entries())
            .slice(0, 6)
            .map(([k, v]) => ({ k, v }));
          tile.append(pieChartSVG({ data }));
          const legend = el("div", NS("legend"));
          data.forEach((d, i) => {
            const li = el("div", NS("legend-item"));
            const sw = el("span", NS("legend-swatch"));
            sw.style.background = PALETTE[i % PALETTE.length];
            li.append(sw, document.createTextNode(`${d.k} (${d.v})`));
            legend.append(li);
          });
          tile.append(legend);
        }

        if (numCols.length) {
          const c = numCols[0];
          const sum = sample.reduce((acc, r) => acc + (parseFloat(r[c]) || 0), 0);
          const head2 = el("div", NS("tile-head"));
          head2.append(el("div", NS("tile-title"), `${c} · suma`), el("div", NS("badge"), String(sum)));
          tile.append(head2, barChartSVG({ data: [{ k: c, v: sum }] }));
        }

        grid.append(tile);
      }

      card.append(grid);
      host.append(wrap);
    }

    // ---------- FK helpers
    async _ensureFKDict(tabla) {
      const key = `FKDICT:${tabla}`;
      if (this._fkCache.has(key)) return this._fkCache.get(key);
      const dict = await getJSON(`/fk_options/${encodeURIComponent(tabla)}`).catch(() => ({}));
      this._fkCache.set(key, dict || {});
      return dict || {};
    }

    async _fetchFKOptions(tabla, col) {
      // returns [{value,label}] for a given FK column, based on table-level dict
      const dict = await this._ensureFKDict(tabla);
      const list = Array.isArray(dict[col]) ? dict[col] : [];
      return list.map((o) => ({
        value: o.value ?? o.id ?? o[Object.keys(o)[0]],
        label: o.label ?? o.name ?? JSON.stringify(o),
      }));
    }

    async _buildFKLabelMaps(tabla, columns) {
      // Build per-column Map(value -> label) for *_id columns
      this._fkLabelMap = {};
      const fkCols = columns.filter((c) => c.endsWith("_id"));
      await Promise.all(
        fkCols.map(async (c) => {
          const opts = await this._fetchFKOptions(tabla, c);
          const m = new Map();
          opts.forEach((o) =>
            m.set(typeof o.value === "number" ? o.value : String(o.value), String(o.label ?? o.value))
          );
          this._fkLabelMap[c] = m;
        })
      );
    }

    _displayVal(col, rawVal, row) {
      // Prefer server-provided label (fkcol__label), else map lookup
      if (row && row[`${col}__label`] != null) return String(row[`${col}__label`]);
      if (rawVal == null) return "";
      const map = this._fkLabelMap[col];
      if (!map) return String(rawVal);
      const key = typeof rawVal === "number" ? rawVal : String(rawVal);
      return map.get(key) ?? String(rawVal);
    }

    // ---------- Tables (CRUD + FK human display)
    async openTable({ target, tabla, rowsPerPage = 10 }) {
      const host = typeof target === "string" ? $(target) : target;
      if (!host) throw new Error("Target not found");
      host.classList.add(NS("root"));
      host.innerHTML = "";

      const wrap = el("div", NS("wrap"));
      const card = el("div", NS("card"));
      wrap.append(el("h1", NS("title"), tabla), card);

      // Toolbar
      const toolbar = el("div", NS("toolbar"));
      const left = el("div", NS("toolbar-left"));
      const right = el("div", NS("toolbar-right"));

      const addBtn = el("button", [NS("btn"), NS("btn-primary")], "➕ Añadir");
      const reloadBtn = el("button", NS("btn"), "↻ Recargar");
      left.append(addBtn, reloadBtn);

      const search = el("div", NS("search"));
      const searchIcon = el("span", null, "🔎");
      const searchInput = document.createElement("input");
      searchInput.type = "search";
      searchInput.placeholder = "Buscar…";
      search.append(searchIcon, searchInput);
      right.append(search);

      toolbar.append(left, right);
      card.append(toolbar);

      // Data area
      const tableWrap = el("div", NS("table-wrap"));
      const table = el("table", NS("table"));
      tableWrap.append(table);
      card.append(tableWrap);

      // Pagination
      const pager = el("div", NS("pagination"));
      const prevBtn = el("button", NS("btn"), "◀");
      const nextBtn = el("button", NS("btn"), "▶");
      const pagePill = el("span", NS("pill"), "Página 1");
      pager.append(prevBtn, nextBtn, pagePill);
      card.append(pager);

      // Form area
      const form = el("div", NS("form"));
      form.style.display = "none";
      card.append(form);

      host.append(wrap);

      // State
      let allRows = [];
      let filtered = [];
      let page = 1;
      let pageSize = rowsPerPage;
      let columns = [];
      let sortKey = null;
      let sortDir = 1;
      let editing = null; // { mode:'insert'|'edit', pkField, data }
      let fkCols = new Set(); // FK columns (drive <select> rendering)

      const inferPK = () => {
        if (columns.includes("id")) return "id";
        const guess = columns.find((c) => c === `${tabla}_id` || c.endsWith("_id"));
        return guess || columns[0];
      };

      const showForm = (show) => {
        form.style.display = show ? "" : "none";
        tableWrap.style.display = show ? "none" : "";
        pager.style.display = show ? "none" : "";
        // Also hide parts of the toolbar for focus
        search.style.display = show ? "none" : "";
        addBtn.style.display = show ? "none" : "";
        reloadBtn.style.display = show ? "none" : "";
      };

      const load = async () => {
        try {
          // Prefer joined (human) endpoint
          const resp = await getJSON(`/seleccionar_humano/${encodeURIComponent(tabla)}`); // rows + meta + fkcol__label
          allRows = Array.isArray(resp?.rows) ? resp.rows : [];
          columns = collectColumns(allRows);

          // Detect FK columns:
          // - name endsWith('_id') OR there is a sibling '<col>__label'
          fkCols = new Set(
            columns.filter((c) => c.endsWith("_id") || columns.includes(`${c}__label`))
          );

          // Build FK label maps for fallback + form selects
          await this._buildFKLabelMaps(tabla, columns);

          filtered = [...allRows];
          page = 1;
          renderTable();
        } catch (e) {
          console.error(e);
          card.append(el("div", NS("empty"), "Error cargando datos."));
        }
      };

      const renderTable = () => {
        table.innerHTML = "";
        if (!columns.length) {
          table.replaceWith(el("div", NS("empty"), "Sin columnas."));
          return;
        }
        // header
        const thead = document.createElement("thead");
        const trh = document.createElement("tr");
        columns.forEach((c) => {
          const th = el("th", NS("th"));
          const btn = el("button", NS("btn"));
          btn.textContent = c + (sortKey === c ? (sortDir === 1 ? " ⬆" : " ⬇") : "");
          btn.addEventListener("click", () => {
            if (sortKey === c) sortDir = -sortDir;
            else {
              sortKey = c;
              sortDir = 1;
            }
            filtered.sort((a, b) => {
              const va = this._displayVal(c, a[c], a);
              const vb = this._displayVal(c, b[c], b);
              if (va == null && vb != null) return -1 * sortDir;
              if (vb == null && va != null) return 1 * sortDir;
              if (va == null && vb == null) return 0;
              const na = parseFloat(va),
                nb = parseFloat(vb);
              if (!Number.isNaN(na) && !Number.isNaN(nb)) return (na - nb) * sortDir;
              return String(va).localeCompare(String(vb)) * sortDir;
            });
            page = 1;
            renderTable();
          });
          th.append(btn);
          trh.append(th);
        });
        trh.append(el("th", NS("th"), "Acciones"));
        thead.append(trh);
        table.append(thead);

        // body
        const tbody = document.createElement("tbody");
        const total = filtered.length;
        const totalPages = Math.max(Math.ceil(total / pageSize), 1);
        page = Math.max(1, Math.min(page, totalPages));
        const start = (page - 1) * pageSize;
        const rows = filtered.slice(start, start + pageSize);

        rows.forEach((row) => {
          const tr = document.createElement("tr");
          tr.className = NS("tr");
          columns.forEach((c) => {
            const td = el("td", NS("td"));
            td.textContent = this._displayVal(c, row[c], row);
            tr.append(td);
          });
          // actions
          const act = el("td", NS("td"));
          const box = el("div", NS("row-actions"));
          const edit = el("button", NS("btn"), "✏️");
          const del = el("button", [NS("btn"), NS("btn-danger")], "🗑️");
          edit.title = "Editar";
          del.title = "Borrar";
          edit.addEventListener("click", () => openEdit(row));
          del.addEventListener("click", () => onDelete(row));
          box.append(edit, del);
          act.append(box);
          tr.append(act);
          tbody.append(tr);
        });

        table.append(tbody);
        pagePill.textContent = `Página ${page}/${Math.max(Math.ceil(total / pageSize), 1)} · ${total} filas`;
      };

      const buildForm = async (data) => {
        form.innerHTML = "";
        const pkField = inferPK();

        // Columns to show in form
        const editableCols = columns.filter((c) => {
          if (c.endsWith("__label")) return false; // helper labels never editable
          if (editing?.mode === "insert" && c === pkField) return false; // skip PK when inserting
          return true;
        });

        // Placeholder to keep actions at the end
        const tmpActs = el("div", NS("form-actions"));
        form.append(tmpActs);

        for (const c of editableCols) {
          const row = el("div", NS("form-row"));
          row.append(el("label", NS("label"), c));

          const isFK = fkCols.has(c);
          let inputEl;

          if (isFK) {
            // FK -> <select>
            inputEl = el("select", NS("select"));
            inputEl.name = c;

            const placeholder = document.createElement("option");
            placeholder.value = "";
            placeholder.textContent = "— seleccionar —";
            inputEl.append(placeholder);

            const opts = await this._fetchFKOptions(tabla, c);
            opts.forEach((o) => {
              const op = document.createElement("option");
              op.value = String(o.value);
              op.textContent = o.label ?? String(o.value);
              inputEl.append(op);
            });

            // Preselect current value if exists
            const currentVal = data[c];
            if (currentVal != null && currentVal !== "") {
              const targetValue = String(currentVal);
              const exists = Array.from(inputEl.options).some((op) => op.value === targetValue);
              if (!exists) {
                const missing = document.createElement("option");
                missing.value = targetValue;
                const label = data[`${c}__label`] ?? String(currentVal);
                missing.textContent = `${label} (actual)`;
                inputEl.append(missing);
              }
              inputEl.value = targetValue;
            } else {
              inputEl.value = "";
            }
          } else {
            // Non-FK -> infer simple input
            inputEl = el("input", NS("input"));
            inputEl.name = c;
            const val = data[c];
            if (typeof val === "number") inputEl.type = "number";
            else if (String(c).toLowerCase().includes("fecha")) inputEl.type = "datetime-local";
            else inputEl.type = "text";
            if (val != null) inputEl.value = val;
          }

          row.append(inputEl);
          form.insertBefore(row, tmpActs);
        }

        // Actions
        const actions = el("div", NS("form-actions"));
        const save = el("button", [NS("btn"), NS("btn-primary")], "💾 Guardar");
        const cancel = el("button", NS("btn"), "Cancelar");
        actions.append(cancel, save);
        form.append(actions);

        cancel.addEventListener("click", (e) => {
          e.preventDefault();
          showForm(false);
          editing = null;
        });

        save.addEventListener("click", async (e) => {
          e.preventDefault();
          const payload = {};

          form.querySelectorAll("input, select, textarea").forEach((inp) => {
            if (!inp.name) return;
            let raw = inp.value;

            // Empty select → null
            if (inp.tagName === "SELECT" && raw === "") {
              payload[inp.name] = null;
              return;
            }

            // Force numeric for *_id when possible
            if (inp.name.endsWith("_id")) {
              const n = Number(raw);
              payload[inp.name] = Number.isFinite(n) ? n : raw === "" ? null : raw;
              return;
            }

            // Generic numeric detection
            const numLike =
              raw !== "" &&
              !isNaN(Number(raw)) &&
              !/^\s+$/.test(raw) &&
              !isNaN(parseFloat(raw));
            payload[inp.name] = numLike ? Number(raw) : raw;
          });

          try {
            if (editing.mode === "insert") {
              await postJSON(`/insertar/${encodeURIComponent(tabla)}`, payload);
            } else {
              const pk = editing.pkField;
              const idv = editing.data[pk];
              await putJSON(`/actualizar/${encodeURIComponent(tabla)}/${encodeURIComponent(idv)}`, payload);
            }
            await load();
            showForm(false);
            editing = null;
          } catch (err) {
            console.error(err);
            alert("Error guardando. Revisa la consola.");
          }
        });
      };

      const openInsert = () => {
        editing = { mode: "insert", pkField: inferPK(), data: {} };
        buildForm(editing.data);
        showForm(true);
      };

      const openEdit = (row) => {
        editing = { mode: "edit", pkField: inferPK(), data: { ...row } };
        buildForm(editing.data);
        showForm(true);
      };

      const onDelete = async (row) => {
        const pk = inferPK();
        const idv = row[pk];
        if (!confirm(`¿Borrar registro ${pk}=${idv}?`)) return;
        try {
          await delJSON(`/eliminar/${encodeURIComponent(tabla)}/${encodeURIComponent(idv)}`);
          await load();
        } catch (e) {
          console.error(e);
          alert("Error al borrar. Revisa la consola.");
        }
      };

      // events
      addBtn.addEventListener("click", openInsert);
      reloadBtn.addEventListener("click", load);

      prevBtn.addEventListener("click", () => {
        page = Math.max(1, page - 1);
        renderTable();
      });
      nextBtn.addEventListener("click", () => {
        const total = filtered.length;
        const totalPages = Math.max(Math.ceil(total / pageSize), 1);
        page = Math.min(totalPages, page + 1);
        renderTable();
      });

      const onSearch = () => {
        const q = searchInput.value.trim().toLowerCase();
        if (!q) filtered = [...allRows];
        else {
          filtered = allRows.filter((r) =>
            collectColumns([r]).some((c) =>
              String(this._displayVal(c, r[c], r) ?? "").toLowerCase().includes(q)
            )
          );
        }
        page = 1;
        renderTable();
      };
      searchInput.addEventListener("input", debounce(onSearch, 200));

      await load();
    }
  }

  // Expose
  window.JocarsaUX = JocarsaUX;
})();

