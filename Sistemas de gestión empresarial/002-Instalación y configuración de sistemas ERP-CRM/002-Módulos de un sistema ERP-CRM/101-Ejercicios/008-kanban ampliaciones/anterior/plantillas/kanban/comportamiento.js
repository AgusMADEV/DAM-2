/*
  Kanban ampliado + edición inline + modal
  (c) 2025 Jose Vicente Carratala
*/

let estado = null;
let dragged = null;
const CONT = document.querySelector("#kanban");

// ==== Carga inicial ====
(function init() {
  const cache = localStorage.getItem("kanbanJSON");
  if (cache) {
    try { estado = JSON.parse(cache); renderKanban(estado); return; }
    catch(e){ console.warn("LocalStorage inválido, cargo kanban.json"); }
  }
  fetch("kanban.json")
    .then(r => r.json())
    .then(data => { estado = data; renderKanban(estado); })
    .catch(err => console.error("No pude cargar kanban.json:", err));
})();

// ==== Render ====
function renderKanban(datos) {
  CONT.innerHTML = "";
  (datos.columnas || []).forEach((col, idx) => {
    CONT.appendChild(creaColumna(col.nombre, col.tarjetas || [], idx));
  });
  CONT.appendChild(creaTileAddColumna());
}

// Columna
function creaColumna(nombre, tarjetas, colIndex) {
  const col = document.createElement("div");
  col.className = "columna";
  col.dataset.title = nombre;

  const head = document.createElement("div");
  head.className = "col-head";

  const title = document.createElement("div");
  title.className = "col-title";
  title.contentEditable = "true";
  title.textContent = nombre;
  title.spellcheck = false;
  title.addEventListener("keydown", (e) => {
    if (e.key === "Enter") { e.preventDefault(); title.blur(); }
  });
  title.addEventListener("blur", () => {
    const nuevo = title.textContent.trim() || "Sin nombre";
    col.dataset.title = nuevo;
    guardar();
  });

  const actions = document.createElement("div");
  actions.className = "col-actions";

  const btnAddCard = document.createElement("button");
  btnAddCard.className = "icon-btn";
  btnAddCard.title = "Añadir tarjeta";
  btnAddCard.textContent = "＋";
  btnAddCard.onclick = (e)=>{ e.stopPropagation(); promptNuevaTarjeta(col); };

  const btnDelCol = document.createElement("button");
  btnDelCol.className = "icon-btn";
  btnDelCol.title = "Borrar columna";
  btnDelCol.textContent = "🗑";
  btnDelCol.onclick = (e)=>{ e.stopPropagation(); borrarColumna(col); };

  actions.append(btnAddCard, btnDelCol);
  head.append(title, actions);
  col.appendChild(head);

  // DnD columna
  col.addEventListener("dragover", e => e.preventDefault());
  col.addEventListener("dragenter", () => col.classList.add("over"));
  col.addEventListener("dragleave", () => col.classList.remove("over"));
  col.addEventListener("drop", (e) => {
    e.preventDefault();
    col.classList.remove("over");
    if (dragged) { col.appendChild(dragged); guardar(); }
  });

  // Tarjetas
  tarjetas.forEach(t => col.appendChild(creaTarjeta(t.texto, t.color)));

  return col;
}

// Tarjeta
function creaTarjeta(texto, color = "#FFF59D") {
  const card = document.createElement("div");
  card.className = "tarjeta";
  card.draggable = true;

  // Botón borrar
  const del = document.createElement("button");
  del.className = "del";
  del.title = "Borrar tarjeta";
  del.textContent = "✖";
  del.onclick = (e)=>{ e.stopPropagation(); card.remove(); guardar(); };

  // Texto editable
  const p = document.createElement("p");
  p.className = "txt";
  p.textContent = texto || "Nueva tarjeta";
  p.setAttribute("contenteditable","false");
  p.spellcheck = false;

  // Doble clic: activar edición inline
  card.addEventListener("dblclick", () => {
    enableInlineEdit(p);
  });

  // Botón ver (modal)
  const view = document.createElement("button");
  view.className = "view";
  view.title = "Ver/editar en modal";
  view.textContent = "👁️";
  view.onclick = (e)=>{ e.stopPropagation(); openModalFromCard(card); };

  // Color picker
  const picker = document.createElement("input");
  picker.type = "color";
  picker.value = normalizaColor(color);
  picker.onchange = () => { card.style.background = picker.value; guardar(); };

  card.style.background = picker.value;

  // DnD tarjeta
  card.addEventListener("dragstart", e => { dragged = card; e.dataTransfer.effectAllowed = "move"; });
  card.addEventListener("dragend",   () => { dragged = null; });

  // Evita que botones/inputs inicien drag
  [del, view, picker, p].forEach(el=>{
    el.addEventListener("mousedown", e=> e.stopPropagation());
  });

  card.append(del, view, p, picker);
  return card;
}

// Inline edit helpers
function enableInlineEdit(el){
  if (el.getAttribute("contenteditable")==="true") return;
  el.setAttribute("contenteditable","true");
  el.focus();
  // Coloca cursor al final
  document.execCommand && document.execCommand("selectAll", false, null);
  window.getSelection().collapseToEnd();
  const finish = ()=>{
    el.setAttribute("contenteditable","false");
    el.textContent = el.textContent.trim();
    guardar();
  };
  el.addEventListener("blur", finish, { once:true });
  el.addEventListener("keydown", (e)=>{
    if(e.key==="Enter"){ e.preventDefault(); el.blur(); }
    if((e.metaKey||e.ctrlKey) && e.key.toLowerCase()==="s"){ e.preventDefault(); el.blur(); }
  });
}

// Tile “Añadir columna”
function creaTileAddColumna() {
  const wrap = document.createElement("div");
  wrap.className = "add-col-tile";
  const btn = document.createElement("button");
  btn.textContent = "＋ Añadir columna";
  btn.onclick = () => {
    const nombre = (prompt("Nombre de la nueva columna:", "Nueva columna") || "Nueva columna").trim();
    const nueva = creaColumna(nombre, [], (estado?.columnas?.length || 0));
    CONT.insertBefore(nueva, wrap);
    guardar();
  };
  wrap.appendChild(btn);
  return wrap;
}

// Acciones
function promptNuevaTarjeta(columnaEl) {
  const t = prompt("Texto de la tarjeta:", "Nueva tarea");
  if (t === null) return;
  const card = creaTarjeta(t.trim() || "Nueva tarea");
  columnaEl.appendChild(card);
  guardar();
}

function borrarColumna(columnaEl) {
  const nombre = columnaEl.dataset.title || "esta columna";
  if (!confirm(`¿Borrar "${nombre}" y todas sus tarjetas?`)) return;
  columnaEl.remove();
  guardar();
}

// ==== Persistencia ====
function guardar() {
  const nuevo = reconstruyeDesdeDOM(CONT);
  estado = nuevo;
  localStorage.setItem("kanbanJSON", JSON.stringify(nuevo));
  fetch("../../../posterior/savekanban.php", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ source: "kanban-ui", timestamp: Date.now(), data: nuevo })
  })
  .then(r => r.json())
  .then(res => console.log("Guardado:", res))
  .catch(err => console.error("Error guardando:", err));
}

function reconstruyeDesdeDOM(contenedor) {
  const resultado = { columnas: [] };
  const cols = [...contenedor.querySelectorAll(".columna")];
  cols.forEach(col => {
    const nombre = (col.dataset.title || "").trim() || "Sin nombre";
    const tarjetas = [...col.querySelectorAll(".tarjeta")].map(card => {
      const texto = (card.querySelector(".txt")?.textContent || "").trim();
      const inputColor = card.querySelector('input[type="color"]');
      let color = getComputedStyle(card).backgroundColor;
      if (inputColor) color = inputColor.value || color;
      return { texto, color: rgbToHex(color) };
    });
    resultado.columnas.push({ nombre, tarjetas });
  });
  return resultado;
}

// ==== Modal con animación desde la tarjeta ====
function openModalFromCard(card){
  // Colores y estilo desde la tarjeta
  const cardBg = getComputedStyle(card).backgroundColor;
  const cardBorder = getComputedStyle(card).borderColor || "transparent";

  // Crear overlay + shell
  const overlay = document.createElement("div");
  overlay.className = "erp-modal-overlay";
  const shell = document.createElement("div");
  shell.className = "erp-modal-shell";

  // Estilo inicial: clon de la tarjeta
  const rect = card.getBoundingClientRect();
  shell.style.top    = rect.top + "px";
  shell.style.left   = rect.left + "px";
  shell.style.width  = rect.width + "px";
  shell.style.height = rect.height + "px";

  // Inyecta modal con fondo de la tarjeta
  shell.innerHTML = `
    <div class="erp-modal" style="--modal-bg:${cardBg}; --modal-border:${cardBorder};">
      <header>
        <h3>Tarjeta</h3>
        <button class="close" title="Cerrar">✖</button>
      </header>
      <section>
        <textarea class="editor" rows="8">${(card.querySelector(".txt")?.textContent || "").trim()}</textarea>
      </section>
      <footer>
        <button class="primary save">💾 Guardar</button>
        <button class="muted cancel">Cancelar</button>
      </footer>
    </div>
  `;

  overlay.appendChild(shell);
  document.body.appendChild(overlay);

  // Animación: crecer al centro (80% de pantalla)
  requestAnimationFrame(()=>{ shell.classList.add("grow"); });

  // Cerrar con animación inversa hasta la tarjeta
  const close = ()=> {
    shell.classList.remove("grow");              // vuelve a su rect original
    shell.addEventListener("transitionend", ()=> overlay.remove(), { once:true });
  };

  // Acciones
  shell.querySelector(".close").onclick = close;
  shell.querySelector(".cancel").onclick = close;

  shell.querySelector(".save").onclick = ()=>{
    const text = shell.querySelector(".editor").value.trim();
    const p = card.querySelector(".txt");
    p.textContent = text || "Nueva tarjeta";
    guardar();
    close();
  };

  // Teclado
  overlay.addEventListener("keydown", (e)=>{
    if(e.key==="Escape"){ e.preventDefault(); close(); }
    if((e.metaKey||e.ctrlKey) && e.key.toLowerCase()==="s"){ e.preventDefault(); shell.querySelector(".save").click(); }
  });

  shell.querySelector(".editor").focus();
}


// ==== Utils ====
function rgbToHex(rgb) {
  if (typeof rgb !== "string") return rgb;
  const m = rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/i);
  if (!m) return rgb;
  const toHex = n => Number(n).toString(16).padStart(2, "0");
  return `#${toHex(m[1])}${toHex(m[2])}${toHex(m[3])}`;
}
function normalizaColor(c) {
  if (!c) return "#FFA500";
  if (c.startsWith("#")) return c;
  const tmp = document.createElement("div");
  tmp.style.color = c;
  document.body.appendChild(tmp);
  const rgb = getComputedStyle(tmp).color;
  document.body.removeChild(tmp);
  return rgbToHex(rgb);
}

