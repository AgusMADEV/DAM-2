/* static/jocarsaux.js
   jocarsa | ux – v14 UI kit (menu + dashboard + CRUD con FK)
   - puro JS, sin dependencias
   - estilos unificados para navegación y tablas
   - dashboard con gráficos SVG automáticos
   - CRUD (insertar/actualizar/borrar) con soporte FK si el backend expone /fk_options
*/

(() => {
  // -----------------------
  // Utilidades básicas
  // -----------------------
  const NS_PREFIX = "jux";
  const NS = (x) => `${NS_PREFIX}-${x}`;
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  function el(tag, cls, text) {
    const e = document.createElement(tag);
    if (cls) {
      if (Array.isArray(cls)) e.className = cls.join(" ");
      else e.className = cls;
    }
    if (text != null) e.textContent = text;
    return e;
  }

  async function getJSON(url) {
    const r = await fetch(url, { headers: { Accept: "application/json" } });
    if (!r.ok) throw new Error(`GET ${url} -> ${r.status}`);
    return r.json();
  }

  async function postJSON(url, data) {
    const r = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(data ?? {}),
    });
    if (!r.ok) throw new Error(`POST ${url} -> ${r.status}`);
    return r.json().catch(() => ({}));
  }

  function debounce(fn, ms = 250) {
    let t;
    return (...args) => {
      clearTimeout(t);
      t = setTimeout(() => fn(...args), ms);
    };
  }

  function guessIsNumericArray(arr) {
    if (!arr.length) return false;
    return arr.every((v) => {
      if (v == null || v === "") return true;
      if (typeof v === "number") return true;
      const n = parseFloat(v);
      return Number.isFinite(n);
    });
  }

  function collectColumns(rows) {
    const cols = new Set();
    rows.forEach((r) => Object.keys(r || {}).forEach((k) => cols.add(k)));
    return Array.from(cols);
  }

  function fmt(val) {
    if (val == null) return "";
    if (val instanceof Date) return val.toISOString().slice(0, 19).replace("T", " ");
    return String(val);
  }

  // -----------------------
  // Estilos (unificados)
  // -----------------------
  function ensureStyles() {
    if (document.getElementById(NS("styles"))) return;
    const css = `
:root{
  --jux-bg:#f6f7fb;
  --jux-panel:#ffffff;
  --jux-line:#e5e7eb;
  --jux-text:#0f172a;
  --jux-muted:#6b7280;
  --jux-accent:#dc143c;
  --jux-chip:#f1f5f9;
  --jux-focus: rgba(220,20,60,.12);
}
.${NS("root")} { color:var(--jux-text); }
.${NS("wrap")} { max-width:1200px; margin:0 auto; padding:12px; }
.${NS("title")} { margin:6px 2px 2px; font-size:20px; font-weight:800; text-transform:lowercase; }
.${NS("subtitle")} { margin:0 2px 18px; color:var(--jux-muted); }
.${NS("card")} { background:var(--jux-panel); border:1px solid var(--jux-line); border-radius:14px; margin:12px 0; overflow:hidden; box-shadow:0 1px 0 rgba(16,24,40,.02); }
.${NS("pad")} { padding:14px 14px 10px; }
.${NS("badge")} { display:inline-block; font-size:12px; color:var(--jux-muted); background:var(--jux-chip); border:1px solid var(--jux-line); border-radius:999px; padding:4px 8px; margin:2px 0 8px; }

 /* NAVIGATION uses the same table tokens */
.${NS("menu")} { display:flex; flex-direction:column; gap:10px; padding:16px; background:var(--jux-panel); border-right:1px solid var(--jux-line); }
.${NS("menu-title")} { font-size:12px; font-weight:800; color:var(--jux-muted); letter-spacing:.3px; text-transform:uppercase; }
.${NS("menu-section")} { display:flex; flex-direction:column; gap:6px; }
.${NS("menu-btn")} { background:var(--jux-panel); color:var(--jux-text); border:1px solid var(--jux-line); padding:10px 12px; border-radius:10px; cursor:pointer; text-align:left; transition:background .15s, border-color .15s; }
.${NS("menu-btn")}:hover { background:var(--jux-chip); }
.${NS("menu-btn-active")} { background:var(--jux-text); color:#fff; border-color:var(--jux-text); }

 /* TABLE */
.${NS("toolbar")} { display:flex; gap:8px; align-items:center; justify-content:space-between; padding:12px; border-bottom:1px solid var(--jux-line); background:var(--jux-panel); position:sticky; top:57px; z-index:5; }
.${NS("toolbar-left")}, .${NS("toolbar-right")} { display:flex; gap:8px; align-items:center; }
.${NS("btn")} { border:1px solid var(--jux-line); background:var(--jux-panel); padding:8px 10px; border-radius:10px; cursor:pointer; }
.${NS("btn-primary")} { background:var(--jux-text); color:#fff; border-color:var(--jux-text); }
.${NS("btn-danger")} { background:#991b1b; color:#fff; border-color:#991b1b; }
.${NS("search")} { display:flex; align-items:center; gap:6px; border:1px solid var(--jux-line); padding:6px 8px; border-radius:10px; background:#fff; }
.${NS("search")} input { border:none; outline:none; min-width:200px; }
.${NS("table-wrap")} { overflow:auto; }
.${NS("table")} { width:100%; border-collapse:separate; border-spacing:0; }
.${NS("th")}, .${NS("td")} { border-bottom:1px solid var(--jux-line); padding:10px 12px; text-align:left; background:#fff; }
.${NS("th")} { position:sticky; top: calc(57px + 48px); background:#fff; z-index:4; font-weight:700; font-size:13px; }
.${NS("tr")}:hover .${NS("td")} { background:#fcfcfd; }
.${NS("row-actions")} { display:flex; gap:6px; }
.${NS("pagination")} { display:flex; gap:8px; align-items:center; justify-content:flex-end; padding:10px 12px; border-top:1px solid var(--jux-line); background:#fff; }
.${NS("pill")} { border:1px solid var(--jux-line); background:var(--jux-chip); padding:4px 8px; border-radius:999px; font-size:12px; color:var(--jux-muted); }

 /* FORM */
.${NS("form")} { border-top:1px solid var(--jux-line); background:#fff; padding:12px; display:grid; grid-template-columns:repeat(2, minmax(220px, 1fr)); gap:10px; }
.${NS("form-row")} { display:flex; flex-direction:column; gap:6px; }
.${NS("label")} { font-size:12px; color:var(--jux-muted); }
.${NS("input")}, .${NS("select")}, .${NS("textarea")} {
  border:1px solid var(--jux-line); border-radius:10px; padding:8px 10px; outline:none; background:#fff;
}
.${NS("input")}:focus, .${NS("select")}:focus, .${NS("textarea")}:focus { box-shadow:0 0 0 3px var(--jux-focus); border-color: var(--jux-text); }
.${NS("form-actions")} { grid-column:1 / -1; display:flex; gap:8px; justify-content:flex-end; margin-top:6px; }

 /* BAD STATE */
.${NS("empty")} { padding:14px; margin:10px 12px; border:1px dashed var(--jux-line); background:#fff; border-radius:12px; color:var(--jux-muted); }
`;
    const style = document.createElement("style");
    style.id = NS("styles");
    style.textContent = css;
    document.head.appendChild(style);
  }

  // -----------------------
  // Gráficos mini (SVG)
  // -----------------------
  function svgEl(tag, attrs) {
    const e = document.createElementNS("http://www.w3.org/2000/svg", tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    return e;
  }

  function barChartSVG({ data = [], w = 300, h = 120, pad = 8 }) {
    const max = Math.max(...data.map((d) => d.v), 1);
    const svg = svgEl("svg", { viewBox: `0 0 ${w} ${h}`, width: "100%", height: h });
    const bw = (w - pad * 2) / Math.max(data.length, 1);
    svg.appendChild(svgEl("line", { x1: pad, y1: h - pad, x2: w - pad, y2: h - pad, stroke: "#e5e7eb" }));
    data.forEach((d, i) => {
      const bh = (d.v / max) * (h - pad * 2 - 16);
      const x = pad + i * bw, y = h - pad - bh;
      svg.appendChild(svgEl("rect", { x, y, width: bw * 0.8, height: bh, rx: 4, ry: 4, fill: "#94a3b8" }));
      const tx = svgEl("text", { x: x + bw * 0.4, y: h - 2, "text-anchor": "middle", "font-size": "10", fill: "#475569" });
      tx.append(document.createTextNode(String(d.k).slice(0, 10)));
      svg.appendChild(tx);
    });
    return svg;
  }

  // -----------------------
  // Clase principal
  // -----------------------
  class JocarsaUX {
    constructor() {
      ensureStyles();
      this._fkCache = new Map(); // key: `${tabla}:${col}` -> [{value,label}]
    }

    // --------- Navigation
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
          // FIXED: remove active using a valid selector
          const activeSel = `.${NS("menu-btn-active")}`;
          root.querySelectorAll(activeSel).forEach(n => n.classList.remove(NS("menu-btn-active")));
          b.classList.add(NS("menu-btn-active"));
          onItemClick && onItemClick(b.dataset.value);
        });
        list.appendChild(b);
      });
      root.append(h, list);
      host.appendChild(root);
    }

    // --------- Dashboard
    async dashboardRenderer({ target }) {
      const host = typeof target === "string" ? $(target) : target;
      if (!host) throw new Error("Target not found");
      host.classList.add(NS("root"));
      host.innerHTML = "";

      const wrap = el("div", NS("wrap"));
      wrap.append(el("h1", NS("title"), "dashboard"), el("p", NS("subtitle"), "Resumen automático por tabla y columna"));

      const tablas = await getJSON("/tablas").then((r) => (Array.isArray(r) ? r.map((x) => x.tabla || x) : [])).catch(() => []);
      if (!tablas.length) {
        wrap.append(el("div", NS("empty"), "No hay tablas."));
        host.append(wrap);
        return;
      }

      for (const tabla of tablas) {
        const card = el("div", NS("card"));
        const pad = el("div", NS("pad"));
        pad.append(el("h3", null, tabla));
        const rows = await getJSON(`/seleccionar/${encodeURIComponent(tabla)}`).then((r) => (Array.isArray(r) ? r : [])).catch(() => []);
        if (!rows.length) {
          pad.append(el("div", NS("badge"), "Tabla vacía"));
          card.append(pad);
          wrap.append(card);
          continue;
        }

        const cols = collectColumns(rows);
        const cat = [];
        const num = [];
        cols.forEach((c) => {
          const vals = rows.map((r) => r[c]).filter((v) => v != null && v !== "");
          if (!vals.length) return;
          if (guessIsNumericArray(vals)) num.push(c);
          else {
            const uniq = new Set(vals.map((v) => String(v))).size;
            if (uniq > 1 && uniq <= 10) cat.push(c);
          }
        });

        // hasta 2 categóricas
        cat.slice(0, 2).forEach((c) => {
          const freq = {};
          rows.forEach((r) => {
            const k = String(r[c] ?? "");
            freq[k] = (freq[k] || 0) + 1;
          });
          const data = Object.entries(freq)
            .map(([k, v]) => ({ k, v }))
            .sort((a, b) => b.v - a.v)
            .slice(0, 5);
          const block = el("div");
          block.style.margin = "10px 0";
          block.append(el("div", NS("badge"), `${c} (top ${data.length})`), barChartSVG({ data }));
          pad.append(block);
        });

        // 1 numérica (suma)
        if (num.length) {
          const c = num[0];
          const sum = rows.reduce((acc, r) => acc + (parseFloat(r[c]) || 0), 0);
          const block = el("div");
          block.style.margin = "10px 0";
          block.append(el("div", NS("badge"), `${c} (suma)`), barChartSVG({ data: [{ k: c, v: sum }] }));
          pad.append(block);
        }

        card.append(pad);
        wrap.append(card);
      }

      host.append(wrap);
    }

    // --------- Tablas
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

      // Form area (hidden by default)
      const form = el("div", NS("form"));
      form.style.display = "none";
      const formActions = el("div", NS("form-actions"));
      const saveBtn = el("button", [NS("btn"), NS("btn-primary")], "💾 Guardar");
      const cancelBtn = el("button", NS("btn"), "Cancelar");
      formActions.append(cancelBtn, saveBtn);
      form.append(formActions);
      card.append(form);

      host.append(wrap);

      // State
      let allRows = [];
      let filtered = [];
      let page = 1;
      let pageSize = rowsPerPage;
      let columns = [];
      let sortKey = null;
      let sortDir = 1; // 1 asc, -1 desc
      let editing = null; // null | {mode:'insert'|'edit', pkField, data}

      const load = async () => {
        try {
          allRows = await getJSON(`/seleccionar/${encodeURIComponent(tabla)}`).then((r) => (Array.isArray(r) ? r : []));
          columns = collectColumns(allRows);
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
              const va = a[c], vb = b[c];
              if (va == null && vb != null) return -1 * sortDir;
              if (vb == null && va != null) return 1 * sortDir;
              if (va == null && vb == null) return 0;
              if (typeof va === "number" && typeof vb === "number") return (va - vb) * sortDir;
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
            td.textContent = fmt(row[c]);
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

      const openInsert = () => {
        editing = { mode: "insert", pkField: inferPK(), data: {} };
        buildForm(editing.data);
        form.style.display = "";
      };

      const openEdit = (row) => {
        editing = { mode: "edit", pkField: inferPK(), data: { ...row } };
        buildForm(editing.data);
        form.style.display = "";
      };

      const inferPK = () => {
        // heurística: id, <tabla>_id, or first column
        if (columns.includes("id")) return "id";
        const guess = columns.find((c) => c === `${tabla}_id` || c.endsWith("_id"));
        return guess || columns[0];
      };

      const fetchFK = async (col) => {
        const key = `${tabla}:${col}`;
        if (this._fkCache.has(key)) return this._fkCache.get(key);
        try {
          const list = await getJSON(`/fk_options?tabla=${encodeURIComponent(tabla)}&col=${encodeURIComponent(col)}`);
          const options = Array.isArray(list)
            ? list.map((o) => ({ value: o.value ?? o.id ?? o[Object.keys(o)[0]], label: o.label ?? o.name ?? JSON.stringify(o) }))
            : [];
          this._fkCache.set(key, options);
          return options;
        } catch {
          this._fkCache.set(key, []);
          return [];
        }
      };

      const buildForm = async (data) => {
        // reset form (keep actions row)
        const prevActs = form.querySelector(`.${NS("form-actions")}`);
        form.innerHTML = "";
        const tmpActs = el("div", NS("form-actions"));
        form.append(tmpActs); // will move later

        for (const c of columns) {
          // skip PK on insert?
          if (editing.mode === "insert" && (c === editing.pkField)) continue;

          const row = el("div", NS("form-row"));
          row.append(el("label", NS("label"), c));

          let inputEl;
          const isFK = c.endsWith("_id");
          if (isFK) {
            inputEl = el("select", NS("select"));
            // load FK options (if any)
            const opts = await fetchFK(c);
            if (opts.length) {
              inputEl.append(el("option", null, "— seleccionar —"));
              opts.forEach((o) => {
                const op = document.createElement("option");
                op.value = o.value;
                op.textContent = o.label ?? o.value;
                inputEl.append(op);
              });
            } else {
              // si no hay endpoint FK, cae a input numeric
              inputEl = el("input", NS("input"));
              inputEl.type = "number";
            }
          } else {
            // elegir tipo por heurística
            inputEl = el("input", NS("input"));
            const val = data[c];
            if (typeof val === "number") inputEl.type = "number";
            else if (String(c).toLowerCase().includes("fecha")) inputEl.type = "datetime-local";
            else inputEl.type = "text";
          }

          inputEl.name = c;
          inputEl.value = data[c] ?? "";
          row.append(inputEl);
          form.insertBefore(row, tmpActs);
        }

        // actions row
        const actions = el("div", NS("form-actions"));
        const save = el("button", [NS("btn"), NS("btn-primary")], "💾 Guardar");
        const cancel = el("button", NS("btn"), "Cancelar");
        actions.append(cancel, save);
        form.append(actions);

        cancel.addEventListener("click", (e) => {
          e.preventDefault();
          form.style.display = "none";
          editing = null;
        });

        save.addEventListener("click", async (e) => {
          e.preventDefault();
          const payload = {};
          $$(`.${NS("form")} input, .${NS("form")} select, .${NS("form")} textarea`, form).forEach((inp) => {
            if (!inp.name) return;
            const raw = inp.value;
            const numLike = raw !== "" && !isNaN(Number(raw)) && !/^\s+$/.test(raw) && !isNaN(parseFloat(raw));
            payload[inp.name] = numLike ? Number(raw) : raw;
          });

          try {
            if (editing.mode === "insert") {
              await postJSON(`/insertar/${encodeURIComponent(tabla)}`, payload);
            } else {
              const pk = editing.pkField;
              const idv = editing.data[pk];
              await postJSON(`/actualizar/${encodeURIComponent(tabla)}`, { [pk]: idv, ...payload });
            }
            await load();
            form.style.display = "none";
            editing = null;
          } catch (err) {
            console.error(err);
            alert("Error guardando. Revisa la consola.");
          }
        });
      };

      const onDelete = async (row) => {
        const pk = inferPK();
        const idv = row[pk];
        if (!confirm(`¿Borrar registro ${pk}=${idv}?`)) return;
        try {
          await postJSON(`/borrar/${encodeURIComponent(tabla)}`, { [pk]: idv });
          await load();
        } catch (e) {
          console.error(e);
          alert("Error al borrar. Revisa la consola.");
        }
      };

      // eventos
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

      searchInput.addEventListener(
        "input",
        debounce(() => {
          const q = searchInput.value.trim().toLowerCase();
          if (!q) filtered = [...allRows];
          else {
            filtered = allRows.filter((r) => {
              return columns.some((c) => String(r[c] ?? "").toLowerCase().includes(q));
            });
          }
          page = 1;
          renderTable();
        }, 200)
      );

      // load initial
      await load();
    }
  }

  // Exponer a window
  window.JocarsaUX = JocarsaUX;
})();

