// public/main.js

const ROOT_PATH = "/";

const treeContainer = document.getElementById("tree");
const tabsContainer = document.getElementById("tabs");
const sidebar = document.getElementById("sidebar");
const divider = document.getElementById("divider");
const editorHost = document.getElementById("editor");
const contextMenu = document.getElementById("context-menu");

const menuEnter     = contextMenu.querySelector('[data-action="enter-folder"]');
const menuNewFolder = contextMenu.querySelector('[data-action="new-folder"]');
const menuNewFile   = contextMenu.querySelector('[data-action="new-file"]');
const menuGoUp      = contextMenu.querySelector('[data-action="go-up"]');
const menuGoRoot    = contextMenu.querySelector('[data-action="go-root"]');

let cmEditor = null;

let openTabs = []; // { path, name, content, dirty }
let activeIndex = -1;
let editingProgrammatically = false;

// estado del árbol
let expandedPaths = new Set();      // carpetas desplegadas
let pathToNode = new Map();         // path -> .tree-node
let configLoaded = false;

// carpeta raíz actual en el panel izquierdo
let currentRootPath = ROOT_PATH;

// contexto del menú
let contextTargetDirPath = null;       // para crear fichero/carpeta
let contextClickedFolderPath = null;   // para "Entrar en la carpeta"

let saveConfigTimer = null;

// ==== STREAMING: profesor → servidor remoto PHP ====
const STREAM_URL = "https://editor.jocarsa.com/api/stream.php";
const STREAM_INTERVAL_MS = 2000; // cada 2 segundos
let streamTimer = null;
// ==================================================

// ----------------- Utilidades básicas -----------------

function log(msg) {
  console.log("[jocarsa|editor]", msg);
}

async function fetchJSON(url, options) {
  const resp = await fetch(url, options);
  const data = await resp.json();
  if (!data.ok) {
    throw new Error(data.error || "Error en la petición");
  }
  return data;
}

function detectarModo(path) {
  if (!path) return "text/plain";
  const lower = path.toLowerCase();

  if (
    lower.endsWith(".js") ||
    lower.endsWith(".cjs") ||
    lower.endsWith(".mjs") ||
    lower.endsWith(".json")
  ) {
    return "javascript";
  }
  if (lower.endsWith(".ts")) {
    return "javascript";
  }
  if (lower.endsWith(".py")) {
    return "python";
  }
  if (lower.endsWith(".html") || lower.endsWith(".htm")) {
    return "htmlmixed";
  }
  if (lower.endsWith(".css")) {
    return "css";
  }
  if (lower.endsWith(".md") || lower.endsWith(".markdown")) {
    return "markdown";
  }
  if (lower.endsWith(".sh") || lower.endsWith(".bash")) {
    return "shell";
  }
  if (lower.endsWith(".xml")) {
    return "xml";
  }
  return "text/plain";
}

function aplicarModoEditor(tab) {
  if (!cmEditor || !tab) return;
  const modo = detectarModo(tab.path || tab.name);
  cmEditor.setOption("mode", modo);
}

// dirname simple para rutas tipo Unix
function pathDirname(p) {
  if (!p) return ROOT_PATH;
  const parts = p.split("/");
  parts.pop();
  const d = parts.join("/") || "/";
  return d;
}

// ----------------- Configuración (estado persistente) -----------------

async function cargarConfig() {
  try {
    const data = await fetchJSON("/api/config");
    const cfg = data.config || {};
    if (Array.isArray(cfg.expanded)) {
      expandedPaths = new Set(cfg.expanded);
    }
    if (typeof cfg.currentRoot === "string") {
      currentRootPath = cfg.currentRoot || ROOT_PATH;
    }
  } catch (e) {
    console.warn("No se pudo cargar config:", e.message);
  } finally {
    configLoaded = true;
  }
}

function guardarConfig() {
  const payload = {
    config: {
      expanded: Array.from(expandedPaths),
      currentRoot: currentRootPath,
    },
  };
  fetch("/api/config", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  }).catch((e) => console.warn("No se pudo guardar config:", e.message));
}

function planificarGuardarConfig() {
  if (!configLoaded) return;
  clearTimeout(saveConfigTimer);
  saveConfigTimer = setTimeout(guardarConfig, 500);
}

// ==== STREAMING: construir y enviar snapshot de pestañas abiertas ====

function construirPayloadStream() {
  let cursorInfo = null;
  if (cmEditor && activeIndex >= 0) {
    const cur = cmEditor.getCursor();
    cursorInfo = {
      index: activeIndex,
      line: cur.line,
      ch: cur.ch,
    };
  }
  return {
    tabs: openTabs.map((t, i) => ({
      index: i,
      path: t.path || "",
      name: t.name || "",
      content: t.content || "",
    })),
    activeIndex: activeIndex,
    cursor: cursorInfo,
  };
}

function enviarStream() {
  if (!STREAM_URL) return;
  const payload = construirPayloadStream();
  fetch(STREAM_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  }).catch((e) =>
    console.warn("No se pudo enviar stream al servidor remoto:", e.message)
  );
}

function planificarStream() {
  clearTimeout(streamTimer);
  streamTimer = setTimeout(enviarStream, STREAM_INTERVAL_MS);
}

// ======================================================

// ----------------- Árbol de directorios -----------------

function crearNodoArbol(entry) {
  const node = document.createElement("div");
  node.className = "tree-node";
  node.dataset.path = entry.relpath;

  const row = document.createElement("div");
  row.className = "tree-row";
  row.dataset.path = entry.relpath;
  row.dataset.type = entry.type;

  const twisty = document.createElement("span");
  twisty.className = "twisty";
  twisty.textContent = entry.type === "dir" ? "▸" : "";
  row.appendChild(twisty);

  const icon = document.createElement("span");
  icon.className = "icon";
  icon.textContent = entry.type === "dir" ? "📁" : "📄";
  row.appendChild(icon);

  const label = document.createElement("span");
  label.className = "label";
  label.textContent = entry.name;
  row.appendChild(label);

  const children = document.createElement("div");
  children.className = "tree-children";
  children.style.display = "none";

  node.appendChild(row);
  node.appendChild(children);

  pathToNode.set(entry.relpath, node);

  row.addEventListener("click", async (ev) => {
    ev.stopPropagation();
    const type = row.dataset.type;
    const dirPath = row.dataset.path;

    const targetEsControlDir =
      ev.target === twisty || ev.target === icon || (type === "dir" && ev.target === label);

    if (type === "dir" && targetEsControlDir) {
      const estaAbierta = children.style.display !== "none";
      if (estaAbierta) {
        children.style.display = "none";
        twisty.textContent = "▸";
        expandedPaths.delete(dirPath);
        planificarGuardarConfig();
      } else {
        await expandirDirectorio(dirPath, node);
        expandedPaths.add(dirPath);
        planificarGuardarConfig();
      }
    } else if (type === "file") {
      abrirFichero(dirPath, entry.name);
    }
  });

  return node;
}

async function cargarDirEn(container, dirPath) {
  try {
    const data = await fetchJSON("/api/tree?path=" + encodeURIComponent(dirPath));
    container.innerHTML = "";
    data.entries.forEach((entry) => {
      const node = crearNodoArbol(entry);
      container.appendChild(node);
    });

    for (const entry of data.entries) {
      if (entry.type === "dir" && expandedPaths.has(entry.relpath)) {
        const node = pathToNode.get(entry.relpath);
        if (node) {
          await expandirDirectorio(entry.relpath, node);
        }
      }
    }
  } catch (err) {
    container.textContent = "Error al cargar el árbol: " + err.message;
  }
}

async function expandirDirectorio(dirPath, node) {
  const children = node.querySelector(":scope > .tree-children");
  const row = node.querySelector(":scope > .tree-row");
  const twisty = row.querySelector(".twisty");

  await cargarDirEn(children, dirPath);
  children.style.display = "block";
  if (twisty) twisty.textContent = "▾";
}

async function cargarArbolRaiz() {
  treeContainer.innerHTML = "";
  pathToNode.clear();
  await cargarDirEn(treeContainer, currentRootPath);
}

async function recargarDirectorio(dirPath) {
  if (!dirPath) dirPath = currentRootPath;
  if (dirPath === currentRootPath) {
    await cargarArbolRaiz();
    return;
  }
  const node = pathToNode.get(dirPath);
  if (!node) {
    await cargarArbolRaiz();
    return;
  }
  expandedPaths.add(dirPath);
  planificarGuardarConfig();
  await expandirDirectorio(dirPath, node);
}

// ----------------- Pestañas + editor -----------------

function indiceTabPorRuta(path) {
  return openTabs.findIndex((t) => t.path === path);
}

function actualizarUI_Tabs() {
  tabsContainer.innerHTML = "";
  openTabs.forEach((tab, index) => {
    const tabEl = document.createElement("div");
    tabEl.className = "tab" + (index === activeIndex ? " active" : "");
    tabEl.dataset.index = index;
    tabEl.title = tab.path || "";

    const nameSpan = document.createElement("span");
    nameSpan.className = "tab-name";
    nameSpan.textContent = tab.name + (tab.dirty ? "*" : "");
    tabEl.appendChild(nameSpan);

    const closeSpan = document.createElement("span");
    closeSpan.className = "tab-close";
    closeSpan.textContent = "×";
    closeSpan.title = "Cerrar";
    closeSpan.addEventListener("click", (ev) => {
      ev.stopPropagation();
      cerrarTab(index);
    });
    tabEl.appendChild(closeSpan);

    tabEl.addEventListener("click", () => {
      activarTab(index);
    });

    tabsContainer.appendChild(tabEl);
  });
}

function activarTab(index) {
  if (index < 0 || index >= openTabs.length) {
    activeIndex = -1;
    if (cmEditor) {
      editingProgrammatically = true;
      cmEditor.setValue("");
      editingProgrammatically = false;
    }
    actualizarUI_Tabs();
    planificarStream();
    return;
  }

  activeIndex = index;
  const tab = openTabs[index];

  if (cmEditor) {
    editingProgrammatically = true;
    cmEditor.setValue(tab.content);
    editingProgrammatically = false;
    aplicarModoEditor(tab);
  }

  actualizarUI_Tabs();
  planificarStream();
}

function cerrarTab(index) {
  if (index < 0 || index >= openTabs.length) return;
  const tab = openTabs[index];
  if (tab.dirty) {
    const ok = confirm("Este archivo tiene cambios sin guardar. ¿Cerrar igualmente?");
    if (!ok) return;
  }

  openTabs.splice(index, 1);
  if (activeIndex === index) {
    activeIndex = Math.min(index, openTabs.length - 1);
  } else if (activeIndex > index) {
    activeIndex -= 1;
  }
  actualizarUI_Tabs();
  activarTab(activeIndex);
  planificarStream();
}

async function abrirFichero(ruta, nombreVisible) {
  const existente = indiceTabPorRuta(ruta);
  if (existente !== -1) {
    activarTab(existente);
    return;
  }

  try {
    const data = await fetchJSON("/api/file?path=" + encodeURIComponent(ruta));
    const tab = {
      path: data.path,
      name: nombreVisible || data.path.split(/[\\/]/).pop(),
      content: data.content,
      dirty: false,
    };
    openTabs.push(tab);
    activarTab(openTabs.length - 1);
    log("Abierto " + tab.name);
    planificarStream();
  } catch (err) {
    alert("Error al abrir el fichero: " + err.message);
    console.error(err);
  }
}

async function guardarActual() {
  if (activeIndex < 0) return;
  const tab = openTabs[activeIndex];
  if (!tab.path) {
    alert("Este ejemplo asume ficheros existentes. Usa Ctrl+Shift+S para 'Guardar como'.");
    return;
  }
  try {
    const body = JSON.stringify({
      path: tab.path,
      content: tab.content,
    });
    await fetchJSON("/api/file", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body,
    });
    tab.dirty = false;
    actualizarUI_Tabs();
    log("Guardado " + tab.name);
    planificarStream();
  } catch (err) {
    alert("Error al guardar: " + err.message);
    console.error(err);
  }
}

async function guardarActualComo() {
  if (activeIndex < 0) return;
  const tab = openTabs[activeIndex];
  const antiguaRuta = tab.path;
  let carpetaBase;
  let nombrePorDefecto;

  if (antiguaRuta) {
    carpetaBase = pathDirname(antiguaRuta);
    nombrePorDefecto = antiguaRuta.split("/").pop();
  } else {
    carpetaBase = currentRootPath;
    nombrePorDefecto = tab.name || "sin_nombre.txt";
  }

  const nuevoNombre = prompt("Guardar como (nombre de archivo):", nombrePorDefecto);
  if (!nuevoNombre) return;

  const separador = carpetaBase.endsWith("/") ? "" : "/";
  const nuevaRuta = carpetaBase + separador + nuevoNombre;

  try {
    const body = JSON.stringify({
      path: nuevaRuta,
      content: tab.content,
    });
    await fetchJSON("/api/file", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body,
    });
    tab.path = nuevaRuta;
    tab.name = nuevoNombre;
    tab.dirty = false;
    actualizarUI_Tabs();
    log("Guardado como " + nuevoNombre);
    await recargarDirectorio(carpetaBase);
    planificarStream();
  } catch (err) {
    alert("Error al guardar como: " + err.message);
    console.error(err);
  }
}

// ----------------- Editor CodeMirror -----------------

function configurarEditor() {
  cmEditor = CodeMirror(editorHost, {
    value: "",
    lineNumbers: true,
    theme: "darcula",
    mode: "text/plain",
    indentUnit: 4,
    tabSize: 4,
    indentWithTabs: false,
    lineWrapping: false,
  });

  cmEditor.on("change", () => {
    if (editingProgrammatically) return;
    if (activeIndex < 0) return;
    const tab = openTabs[activeIndex];
    tab.content = cmEditor.getValue();
    if (!tab.dirty) {
      tab.dirty = true;
      actualizarUI_Tabs();
    }
    planificarStream();
  });
}

// ----------------- Atajos de teclado -----------------

document.addEventListener("keydown", (ev) => {
  if ((ev.ctrlKey || ev.metaKey) && ev.key.toLowerCase() === "s") {
    ev.preventDefault();
    if (ev.shiftKey) {
      guardarActualComo();  // Ctrl+Shift+S
    } else {
      guardarActual();      // Ctrl+S
    }
  }
  if ((ev.ctrlKey || ev.metaKey) && ev.key.toLowerCase() === "w") {
    ev.preventDefault();
    if (activeIndex >= 0) {
      cerrarTab(activeIndex);
    }
  }
});

// ----------------- Redimensionar panel izquierdo -----------------

let redimensionando = false;
let startX = 0;
let anchoInicial = 0;

divider.addEventListener("mousedown", (e) => {
  redimensionando = true;
  startX = e.clientX;
  anchoInicial = sidebar.getBoundingClientRect().width;
  document.body.classList.add("resizing");
});

document.addEventListener("mousemove", (e) => {
  if (!redimensionando) return;
  const dx = e.clientX - startX;
  let nuevoAncho = anchoInicial + dx;
  const min = 140;
  const max = 600;
  if (nuevoAncho < min) nuevoAncho = min;
  if (nuevoAncho > max) nuevoAncho = max;
  sidebar.style.width = nuevoAncho + "px";
});

document.addEventListener("mouseup", () => {
  if (redimensionando) {
    redimensionando = false;
    document.body.classList.remove("resizing");
  }
});

// ----------------- Menú contextual -----------------

function ocultarMenuContextual() {
  contextMenu.classList.remove("visible");
}

function mostrarMenuContextual(x, y) {
  contextMenu.style.left = x + "px";
  contextMenu.style.top = y + "px";
  contextMenu.classList.add("visible");
}

treeContainer.addEventListener("contextmenu", (e) => {
  e.preventDefault();
  const row = e.target.closest(".tree-row");
  contextClickedFolderPath = null;

  if (row) {
    const tipo = row.dataset.type;
    const ruta = row.dataset.path;
    if (tipo === "file") {
      contextTargetDirPath = pathDirname(ruta);
    } else {
      contextTargetDirPath = ruta;
      contextClickedFolderPath = ruta;
    }
  } else {
    contextTargetDirPath = currentRootPath;
  }

  menuEnter.style.display = contextClickedFolderPath ? "block" : "none";
  menuGoUp.style.display = currentRootPath !== ROOT_PATH ? "block" : "none";
  mostrarMenuContextual(e.clientX, e.clientY);
});

document.addEventListener("click", () => {
  ocultarMenuContextual();
});

contextMenu.addEventListener("click", async (e) => {
  const item = e.target.closest(".context-item");
  if (!item) return;
  const accion = item.dataset.action;
  ocultarMenuContextual();
  if (!contextTargetDirPath) contextTargetDirPath = currentRootPath;

  try {
    if (accion === "new-folder" || accion === "new-file") {
      const etiqueta = accion === "new-folder" ? "Nombre de la carpeta" : "Nombre del archivo";
      const nombre = prompt(etiqueta + ":");
      if (!nombre) return;

      const endpoint = accion === "new-folder" ? "/api/new-folder" : "/api/new-file";

      await fetchJSON(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          parentPath: contextTargetDirPath,
          name: nombre,
        }),
      });
      log("Creado " + nombre);
      await recargarDirectorio(contextTargetDirPath);
    } else if (accion === "enter-folder" && contextClickedFolderPath) {
      currentRootPath = contextClickedFolderPath;
      planificarGuardarConfig();
      await cargarArbolRaiz();
    } else if (accion === "go-up") {
      if (currentRootPath !== ROOT_PATH) {
        currentRootPath = pathDirname(currentRootPath);
        planificarGuardarConfig();
        await cargarArbolRaiz();
      }
    } else if (accion === "go-root") {
      currentRootPath = ROOT_PATH;
      planificarGuardarConfig();
      await cargarArbolRaiz();
    }
  } catch (err) {
    alert("Error: " + err.message);
    console.error(err);
  }

  e.stopPropagation();
});

// ----------------- Init -----------------

window.addEventListener("load", async () => {
  configurarEditor();
  await cargarConfig();
  await cargarArbolRaiz();

  openTabs.push({
    path: "",
    name: "Sin título",
    content: "",
    dirty: false,
  });
  activarTab(0);
  planificarStream(); // primer envío
});

