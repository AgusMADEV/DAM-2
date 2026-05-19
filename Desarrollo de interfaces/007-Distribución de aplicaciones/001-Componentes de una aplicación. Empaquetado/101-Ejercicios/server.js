// server.js
const express = require("express");
const path = require("path");
const fs = require("fs").promises;
const fsSync = require("fs");

const app = express();

// Raíz del sistema de archivos ("/" en Linux)
const ROOT_DIR = path.parse(process.cwd()).root; // p.ej. "/"

// Fichero de configuración para estado de la UI
const CONFIG_PATH = path.join(__dirname, "config.json");

function resolvePath(p) {
  if (!p) p = ROOT_DIR;
  let full;

  if (path.isAbsolute(p)) {
    full = p;
  } else {
    full = path.join(ROOT_DIR, p);
  }

  full = path.resolve(full);

  // mantenerse dentro de ROOT_DIR
  if (!full.startsWith(ROOT_DIR)) {
    throw new Error("Ruta no válida");
  }
  return full;
}

async function readConfig() {
  try {
    const txt = await fs.readFile(CONFIG_PATH, "utf8");
    const cfg = JSON.parse(txt);
    if (!cfg || typeof cfg !== "object") {
      return { expanded: [], currentRoot: ROOT_DIR };
    }
    if (!Array.isArray(cfg.expanded)) cfg.expanded = [];
    if (typeof cfg.currentRoot !== "string") cfg.currentRoot = ROOT_DIR;
    return cfg;
  } catch (e) {
    // primera ejecución: no existe
    return { expanded: [], currentRoot: ROOT_DIR };
  }
}

async function writeConfig(cfg) {
  const safe = {
    expanded: Array.isArray(cfg.expanded) ? cfg.expanded : [],
    currentRoot: typeof cfg.currentRoot === "string" ? cfg.currentRoot : ROOT_DIR,
  };
  await fs.writeFile(CONFIG_PATH, JSON.stringify(safe, null, 2), "utf8");
}

app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

// ------------------- API: árbol de directorios -------------------

app.get("/api/tree", async (req, res) => {
  const requested = req.query.path || ROOT_DIR;
  let base;
  try {
    base = resolvePath(requested);
  } catch (e) {
    return res.status(400).json({ ok: false, error: "Ruta no válida" });
  }

  try {
    const stat = await fs.stat(base);
    if (!stat.isDirectory()) {
      return res.status(400).json({ ok: false, error: "No es un directorio" });
    }
  } catch (e) {
    return res.status(400).json({ ok: false, error: "No es un directorio" });
  }

  try {
    const items = await fs.readdir(base);
    const entries = [];
    items.sort().forEach((name) => {
      const full = path.join(base, name);
      const type = fsSync.statSync(full).isDirectory() ? "dir" : "file";
      entries.push({
        name,
        relpath: full, // ruta absoluta
        type,
      });
    });
    res.json({ ok: true, path: base, entries });
  } catch (e) {
    res.status(500).json({ ok: false, error: e.message });
  }
});

// ------------------- API: leer fichero -------------------

app.get("/api/file", async (req, res) => {
  const p = req.query.path;
  if (!p) {
    return res.status(400).json({ ok: false, error: "Falta la ruta" });
  }

  let full;
  try {
    full = resolvePath(p);
  } catch (e) {
    return res.status(400).json({ ok: false, error: "Ruta no válida" });
  }

  try {
    const stat = await fs.stat(full);
    if (!stat.isFile()) {
      return res.status(404).json({ ok: false, error: "Fichero no encontrado" });
    }
  } catch (e) {
    return res.status(404).json({ ok: false, error: "Fichero no encontrado" });
  }

  try {
    const content = await fs.readFile(full, "utf8");
    res.json({ ok: true, path: full, content });
  } catch (e) {
    res.status(500).json({ ok: false, error: e.message });
  }
});

// ------------------- API: guardar fichero -------------------

app.post("/api/file", async (req, res) => {
  const p = req.body.path;
  const content = req.body.content || "";

  if (!p) {
    return res.status(400).json({ ok: false, error: "Falta la ruta" });
  }

  let full;
  try {
    full = resolvePath(p);
  } catch (e) {
    return res.status(400).json({ ok: false, error: "Ruta no válida" });
  }

  try {
    const dir = path.dirname(full);
    await fs.mkdir(dir, { recursive: true });
    await fs.writeFile(full, content, "utf8");
    res.json({ ok: true, path: full });
  } catch (e) {
    res.status(500).json({ ok: false, error: e.message });
  }
});

// ------------------- API: crear carpeta -------------------

app.post("/api/new-folder", async (req, res) => {
  const parentPath = req.body.parentPath;
  const name = (req.body.name || "").trim();

  if (!parentPath || !name) {
    return res
      .status(400)
      .json({ ok: false, error: "Faltan la carpeta padre o el nombre" });
  }

  let parentFull;
  try {
    parentFull = resolvePath(parentPath);
  } catch (e) {
    return res.status(400).json({ ok: false, error: "Carpeta padre no válida" });
  }

  try {
    const parentStat = await fs.stat(parentFull);
    if (!parentStat.isDirectory()) {
      return res.status(400).json({ ok: false, error: "La carpeta padre no es un directorio" });
    }
  } catch (e) {
    return res.status(400).json({ ok: false, error: "La carpeta padre no es un directorio" });
  }

  const newDir = path.join(parentFull, name);

  try {
    await fs.mkdir(newDir);
    res.json({ ok: true, path: newDir });
  } catch (e) {
    res.status(500).json({ ok: false, error: e.message });
  }
});

// ------------------- API: crear fichero vacío -------------------

app.post("/api/new-file", async (req, res) => {
  const parentPath = req.body.parentPath;
  const name = (req.body.name || "").trim();

  if (!parentPath || !name) {
    return res
      .status(400)
      .json({ ok: false, error: "Faltan la carpeta padre o el nombre" });
  }

  let parentFull;
  try {
    parentFull = resolvePath(parentPath);
  } catch (e) {
    return res.status(400).json({ ok: false, error: "Carpeta padre no válida" });
  }

  try {
    const parentStat = await fs.stat(parentFull);
    if (!parentStat.isDirectory()) {
      return res.status(400).json({ ok: false, error: "La carpeta padre no es un directorio" });
    }
  } catch (e) {
    return res.status(400).json({ ok: false, error: "La carpeta padre no es un directorio" });
  }

  const newFile = path.join(parentFull, name);

  try {
    await fs.writeFile(newFile, "", { flag: "wx" }); // falla si existe
    res.json({ ok: true, path: newFile });
  } catch (e) {
    res.status(500).json({ ok: false, error: e.message });
  }
});

// ------------------- API: configuración (estado árbol) -------------------

app.get("/api/config", async (req, res) => {
  try {
    const cfg = await readConfig();
    res.json({ ok: true, config: cfg });
  } catch (e) {
    res.status(500).json({ ok: false, error: e.message });
  }
});

app.post("/api/config", async (req, res) => {
  const cfg = (req.body && req.body.config) || {};
  try {
    await writeConfig(cfg);
    res.json({ ok: true });
  } catch (e) {
    res.status(500).json({ ok: false, error: e.message });
  }
});

// ------------------- Inicio -------------------

const PORT = process.env.PORT || 3000;

function startServer() {
  return new Promise((resolve, reject) => {
    const server = app.listen(PORT, () => {
      console.log(`jocarsa | editor escuchando en http://localhost:${PORT}`);
      console.log(`Raíz del sistema de ficheros: ${ROOT_DIR}`);
      resolve(server);
    });
    server.on("error", reject);
  });
}

// Si se ejecuta directamente con "node server.js"
if (require.main === module) {
  startServer().catch((err) => {
    console.error("Error al arrancar el servidor:", err);
  });
}

module.exports = { startServer, PORT };


