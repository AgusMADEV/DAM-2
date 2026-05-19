// ===== Sistema de Gestión Empresarial - Editor de Procesos =====
// Aplicación principal JavaScript (ES6 Module)

// Elementos del DOM
const centro = document.getElementById("centro");
const mundo = document.getElementById("mundo");
const edgesSvg = document.getElementById("edges");
const toolsList = document.getElementById("tools-list");
const playBtn = document.getElementById("play");
const delBtn = document.getElementById("deleteNode");
const clearAllBtn = document.getElementById("clearAll");
const clearLogBtn = document.getElementById("clearLog");
const logEl = document.getElementById("log");
const hint = document.getElementById("hint");

// Estado de la aplicación
const nodos = [];           // {id, x, y, el, type, config}
const conexiones = [];      // {from, to, fromPort, pathBg, path}
let nodoCounter = 1;
let TOOLS = [];
const frontModules = {};    // módulos frontend específicos (si existen)

// Selección
let selectedNodeId = null;

// Transform (zoom & pan)
let scale = 1;
let translateX = 0;
let translateY = 0;

// Conexión en curso
let conexionEnCurso = null; // {fromIdx, fromPort, line}


// ===== UTILIDADES =====

function log(msg) {
  const timestamp = new Date().toLocaleTimeString();
  logEl.textContent = `[${timestamp}] ${msg}\n` + logEl.textContent;
}

function aplicarTransform() {
  mundo.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
}

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function screenToWorld(screenX, screenY) {
  const rect = centro.getBoundingClientRect();
  return {
    x: (screenX - rect.left - translateX) / scale,
    y: (screenY - rect.top - translateY) / scale
  };
}

aplicarTransform();


// ===== SELECCIÓN Y ELIMINACIÓN =====

function setSelected(nodeId) {
  selectedNodeId = nodeId;
  nodos.forEach(n => {
    if (n.id === nodeId) n.el.classList.add("selected");
    else n.el.classList.remove("selected");
  });
}

function clearSelected() {
  setSelected(null);
}

function getSelectedNode() {
  if (!selectedNodeId) return null;
  return nodos.find(n => n.id === selectedNodeId) || null;
}

function eliminarNodoSeleccionado() {
  const nodo = getSelectedNode();
  if (!nodo) {
    log("⚠️ No hay ningún nodo seleccionado");
    return;
  }

  const idx = nodos.indexOf(nodo);
  if (idx < 0) return;

  // Eliminar conexiones asociadas
  for (let i = conexiones.length - 1; i >= 0; i--) {
    const c = conexiones[i];
    if (c.from === idx || c.to === idx) {
      c.pathBg?.remove();
      c.path?.remove();
      conexiones.splice(i, 1);
    }
  }

  // Eliminar nodo del DOM y array
  nodo.el.remove();
  nodos.splice(idx, 1);

  // Reindexar conexiones
  conexiones.forEach(c => {
    if (c.from > idx) c.from--;
    if (c.to > idx) c.to--;
  });

  selectedNodeId = null;
  log(`🗑️ Nodo ${nodo.id} eliminado`);
  
  // Mostrar hint si no quedan nodos
  if (nodos.length === 0) {
    hint.style.display = "block";
  }
}

function limpiarTodo() {
  if (!confirm("¿Seguro que quieres eliminar todos los nodos y conexiones?")) {
    return;
  }
  
  // Eliminar todos los nodos
  nodos.forEach(n => n.el.remove());
  nodos.length = 0;
  
  // Eliminar todas las conexiones
  conexiones.forEach(c => {
    c.pathBg?.remove();
    c.path?.remove();
  });
  conexiones.length = 0;
  
  selectedNodeId = null;
  nodoCounter = 1;
  
  hint.style.display = "block";
  log("🧹 Lienzo limpiado completamente");
}


// ===== EVENTOS DE BOTONES =====

delBtn?.addEventListener("click", eliminarNodoSeleccionado);
clearAllBtn?.addEventListener("click", limpiarTodo);
clearLogBtn?.addEventListener("click", () => {
  logEl.textContent = "Consola limpiada.\n";
});

window.addEventListener("keydown", (e) => {
  if (e.key === "Delete" || e.key === "Supr") {
    eliminarNodoSeleccionado();
  }
});

// Click en área vacía deselecciona (si no estamos conectando)
centro.addEventListener("pointerdown", (e) => {
  if (conexionEnCurso) return;
  if (!e.target.closest(".node")) {
    clearSelected();
  }
});


// ===== ZOOM & PAN =====

centro.addEventListener("wheel", (e) => {
  if (!e.ctrlKey) return;
  e.preventDefault();

  const delta = -Math.sign(e.deltaY);
  const factor = 1.1;
  const newScale = delta > 0 ? scale * factor : scale / factor;
  scale = clamp(newScale, 0.3, 3);

  aplicarTransform();
}, { passive: false });

let panActive = false;
let panStart = { x: 0, y: 0 };

centro.addEventListener("pointerdown", (e) => {
  if (e.ctrlKey && e.button === 0) {
    panActive = true;
    panStart = { x: e.clientX - translateX, y: e.clientY - translateY };
    e.preventDefault();
  }
});

window.addEventListener("pointermove", (e) => {
  if (panActive) {
    translateX = e.clientX - panStart.x;
    translateY = e.clientY - panStart.y;
    aplicarTransform();
  }
});

window.addEventListener("pointerup", () => {
  panActive = false;
});


// ===== CARGA DE HERRAMIENTAS =====

(async function cargarHerramientas() {
  try {
    const resp = await fetch("/api/tools");
    const data = await resp.json();
    TOOLS = data.tools || [];

    if (TOOLS.length === 0) {
      toolsList.innerHTML = '<div class="muted">No hay herramientas disponibles</div>';
      return;
    }

    toolsList.innerHTML = "";

    // Cargar módulos frontend (si existen)
    await Promise.all(TOOLS.map(async (tool) => {
      if (tool.front_module) {
        try {
          const mod = await import(tool.front_module);
          if (mod?.default?.type === tool.type) {
            frontModules[tool.type] = mod.default;
          }
        } catch (err) {
          console.warn("No se pudo cargar módulo frontend:", tool.type, err);
        }
      }
    }));

    // Crear botones de herramientas
    TOOLS.forEach(tool => {
      const btn = document.createElement("button");
      btn.className = "tool-btn";
      btn.type = "button";
      btn.title = tool.description || "";
      btn.textContent = tool.label || tool.type;
      btn.addEventListener("click", () => crearNodoDesdeHerramienta(tool));
      toolsList.appendChild(btn);
    });

    log(`✅ ${TOOLS.length} herramientas cargadas`);
  } catch (err) {
    log(`❌ Error cargando herramientas: ${err.message}`);
    toolsList.innerHTML = '<div class="muted">Error al cargar herramientas</div>';
  }
})();


// ===== CREACIÓN DE NODOS =====

function crearNodoBase(x, y, titulo) {
  const el = document.createElement("article");
  el.className = "node";
  el.style.left = x + "px";
  el.style.top = y + "px";

  el.innerHTML = `
    <div class="titlebar drag-handle"></div>
    <div class="title">${titulo}</div>
    <div class="body"></div>
    <div class="port in" title="Entrada"></div>
    <div class="port out" title="Salida"></div>
  `;

  mundo.appendChild(el);

  // Evento de selección
  el.addEventListener("pointerdown", (e) => {
    const id = el.dataset.nodeId;
    if (id) setSelected(id);
  }, true);

  // Puerto de salida (para iniciar conexión)
  const portOut = el.querySelector(".port.out");
  portOut?.addEventListener("pointerdown", (e) => {
    e.preventDefault();
    e.stopPropagation();
    iniciarConexion(e, el, portOut);
  });

  return el;
}

function crearNodoDesdeHerramienta(tool) {
  // Posición aleatoria cerca del centro
  const baseX = 200 + Math.random() * 300;
  const baseY = 150 + Math.random() * 200;
  const { x, y } = screenToWorld(baseX, baseY);

  const el = crearNodoBase(x, y, tool.label || tool.type);
  const nodeId = "n" + (nodoCounter++);
  el.dataset.nodeId = nodeId;
  el.dataset.type = tool.type;

  // Configuración inicial
  const config = {};
  if (tool.config) {
    Object.keys(tool.config).forEach(key => {
      const field = tool.config[key];
      config[key] = field.default !== undefined ? field.default : "";
    });
  }

  // Renderizar campos de configuración
  renderizarCamposNodo(el, tool, config);

  // Añadir a la lista de nodos
  nodos.push({ id: nodeId, x, y, el, type: tool.type, config });

  // Habilitar drag & drop
  habilitarDragNodo(el);

  // Ocultar hint
  hint.style.display = "none";

  log(`➕ Nodo creado: ${tool.label || tool.type}`);
}

function renderizarCamposNodo(el, tool, config) {
  const body = el.querySelector(".body");
  body.innerHTML = "";

  if (!tool.config) return;

  Object.keys(tool.config).forEach(key => {
    const field = tool.config[key];
    const fieldDiv = document.createElement("div");
    fieldDiv.className = "field";

    const label = document.createElement("label");
    label.textContent = field.label || key;

    let input;
    if (field.type === "number") {
      input = document.createElement("input");
      input.type = "number";
      input.value = config[key] || field.default || 0;
    } else if (field.type === "boolean") {
      input = document.createElement("input");
      input.type = "checkbox";
      input.checked = config[key] || field.default || false;
    } else {  // string por defecto
      input = document.createElement("input");
      input.type = "text";
      input.value = config[key] || field.default || "";
    }

    input.dataset.configKey = key;
    
    // Actualizar config cuando cambie el valor
    input.addEventListener("input", () => {
      const nodo = nodos.find(n => n.el === el);
      if (nodo) {
        if (field.type === "number") {
          nodo.config[key] = parseFloat(input.value) || 0;
        } else if (field.type === "boolean") {
          nodo.config[key] = input.checked;
        } else {
          nodo.config[key] = input.value;
        }
      }
    });

    fieldDiv.appendChild(label);
    fieldDiv.appendChild(input);
    body.appendChild(fieldDiv);
  });
}


// ===== DRAG & DROP DE NODOS =====

function habilitarDragNodo(el) {
  const handle = el.querySelector(".drag-handle");
  let dragging = false;
  let offsetX = 0, offsetY = 0;

  handle.addEventListener("pointerdown", (e) => {
    dragging = true;
    const rect = el.getBoundingClientRect();
    offsetX = (e.clientX - rect.left) / scale;
    offsetY = (e.clientY - rect.top) / scale;
    el.style.cursor = "grabbing";
    e.preventDefault();
  });

  window.addEventListener("pointermove", (e) => {
    if (!dragging) return;

    const mundo_rect = mundo.getBoundingClientRect();
    const x = (e.clientX - mundo_rect.left) / scale - offsetX;
    const y = (e.clientY - mundo_rect.top) / scale - offsetY;

    el.style.left = x + "px";
    el.style.top = y + "px";

    // Actualizar posición en el array
    const nodo = nodos.find(n => n.el === el);
    if (nodo) {
      nodo.x = x;
      nodo.y = y;
    }

    // Actualizar conexiones visuales
    actualizarConexiones();
  });

  window.addEventListener("pointerup", () => {
    if (dragging) {
      dragging = false;
      el.style.cursor = "move";
    }
  });
}


// ===== CONEXIONES =====

function iniciarConexion(e, fromEl, fromPort) {
  const fromIdx = nodos.findIndex(n => n.el === fromEl);
  if (fromIdx < 0) return;

  const portName = fromPort.dataset.port || "default";

  // Crear línea temporal
  const line = document.createElementNS("http://www.w3.org/2000/svg", "path");
  line.setAttribute("stroke", "#2563eb");
  line.setAttribute("stroke-width", "3");
  line.setAttribute("fill", "none");
  line.setAttribute("opacity", "0.6");
  edgesSvg.appendChild(line);

  conexionEnCurso = { fromIdx, fromPort: portName, line };

  const updateLine = (clientX, clientY) => {
    const fromRect = fromPort.getBoundingClientRect();
    const centroRect = centro.getBoundingClientRect();

    const x1 = (fromRect.left + fromRect.width / 2 - centroRect.left) / scale;
    const y1 = (fromRect.top + fromRect.height / 2 - centroRect.top) / scale;
    const x2 = (clientX - centroRect.left) / scale;
    const y2 = (clientY - centroRect.top) / scale;

    const path = generarPathCurva(x1, y1, x2, y2);
    line.setAttribute("d", path);
  };

  const onMove = (e) => updateLine(e.clientX, e.clientY);
  const onUp = (e) => {
    window.removeEventListener("pointermove", onMove);
    window.removeEventListener("pointerup", onUp);

    // Verificar si terminó en un puerto de entrada
    const target = document.elementFromPoint(e.clientX, e.clientY);
    if (target && target.classList.contains("port") && target.classList.contains("in")) {
      const toEl = target.closest(".node");
      const toIdx = nodos.findIndex(n => n.el === toEl);

      if (toIdx >= 0 && toIdx !== fromIdx) {
        crearConexion(fromIdx, toIdx, portName);
      }
    }

    // Eliminar línea temporal
    line.remove();
    conexionEnCurso = null;
  };

  updateLine(e.clientX, e.clientY);
  window.addEventListener("pointermove", onMove);
  window.addEventListener("pointerup", onUp);
}

function crearConexion(fromIdx, toIdx, fromPort = "default") {
  // Verificar si ya existe esta conexión
  const existe = conexiones.some(c =>
    c.from === fromIdx && c.to === toIdx && c.fromPort === fromPort
  );

  if (existe) {
    log("⚠️ Ya existe esta conexión");
    return;
  }

  // Crear paths SVG para la conexión
  const pathBg = document.createElementNS("http://www.w3.org/2000/svg", "path");
  pathBg.classList.add("edge-bg");

  const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
  path.classList.add("edge");

  edgesSvg.appendChild(pathBg);
  edgesSvg.appendChild(path);

  conexiones.push({ from: fromIdx, to: toIdx, fromPort, pathBg, path });

  actualizarConexiones();

  const fromNode = nodos[fromIdx];
  const toNode = nodos[toIdx];
  log(`🔗 Conexión creada: ${fromNode.id} → ${toNode.id}`);
}

function actualizarConexiones() {
  conexiones.forEach(c => {
    const fromNode = nodos[c.from];
    const toNode = nodos[c.to];

    if (!fromNode || !toNode) return;

    const fromPort = fromNode.el.querySelector(".port.out");
    const toPort = toNode.el.querySelector(".port.in");

    if (!fromPort || !toPort) return;

    const fromRect = fromPort.getBoundingClientRect();
    const toRect = toPort.getBoundingClientRect();
    const centroRect = centro.getBoundingClientRect();

    const x1 = (fromRect.left + fromRect.width / 2 - centroRect.left) / scale;
    const y1 = (fromRect.top + fromRect.height / 2 - centroRect.top) / scale;
    const x2 = (toRect.left + toRect.width / 2 - centroRect.left) / scale;
    const y2 = (toRect.top + toRect.height / 2 - centroRect.top) / scale;

    const pathStr = generarPathCurva(x1, y1, x2, y2);
    c.pathBg.setAttribute("d", pathStr);
    c.path.setAttribute("d", pathStr);
  });
}

function generarPathCurva(x1, y1, x2, y2) {
  const dx = Math.abs(x2 - x1);
  const offset = Math.min(dx * 0.5, 100);
  return `M ${x1} ${y1} C ${x1 + offset} ${y1}, ${x2 - offset} ${y2}, ${x2} ${y2}`;
}


// ===== EJECUCIÓN DEL FLUJO =====

playBtn?.addEventListener("click", async () => {
  if (nodos.length === 0) {
    log("⚠️ No hay nodos para ejecutar");
    return;
  }

  log("\n🚀 ===== EJECUTANDO FLUJO =====");
  playBtn.disabled = true;
  playBtn.textContent = "⏳ Ejecutando...";

  try {
    // Preparar datos para el backend
    const nodes_data = nodos.map(n => ({
      id: n.id,
      type: n.type,
      config: n.config
    }));

    const edges_data = conexiones.map(c => ({
      from: nodos[c.from].id,
      to: nodos[c.to].id,
      fromPort: c.fromPort
    }));

    // Ejecutar en el backend
    const resp = await fetch("/api/execute", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        nodes: nodes_data,
        edges: edges_data
      })
    });

    const result = await resp.json();

    if (result.success) {
      result.logs.forEach(msg => log(msg));
      log("\n✅ Ejecución completada con éxito");
    } else {
      log(`\n❌ Error: ${result.error}`);
      result.logs?.forEach(msg => log(msg));
    }

  } catch (err) {
    log(`❌ Error al ejecutar: ${err.message}`);
  } finally {
    playBtn.disabled = false;
    playBtn.textContent = "▶ Ejecutar Flujo";
  }
});


// Actualizar conexiones cuando cambie el zoom/pan
window.addEventListener("resize", actualizarConexiones);

// Log inicial
log("✨ Sistema de Gestión Empresarial iniciado");
log("👉 Arrastra nodos desde el panel izquierdo para comenzar");
