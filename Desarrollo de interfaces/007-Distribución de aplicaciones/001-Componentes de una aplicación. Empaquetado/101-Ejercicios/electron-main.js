// electron-main.js
const { app, BrowserWindow, nativeImage } = require("electron");
const path = require("path");
const { startServer, PORT } = require("./server");

let mainWindow = null;
let serverInstance = null;

async function createWindow() {
  // Start Express server
  try {
    serverInstance = await startServer();
  } catch (err) {
    console.error("No se pudo arrancar el servidor Express:", err);
    app.quit();
    return;
  }

  // Build icon
  const iconPath = path.join(__dirname, "build", "icon.png");
  const appIcon = nativeImage.createFromPath(iconPath);

  if (appIcon.isEmpty()) {
    console.error("No se pudo cargar el icono:", iconPath);
  } else {
    console.log("Icono cargado correctamente:", iconPath);
  }

  // Create Electron window
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    icon: appIcon,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false
    },
    title: "jocarsa | editor"
  });

  mainWindow.loadURL(`http://localhost:${PORT}`);

  mainWindow.on("closed", () => {
    mainWindow = null;
  });
}

app.whenReady().then(createWindow);

app.on("activate", () => {
  if (mainWindow === null) {
    createWindow();
  }
});

app.on("window-all-closed", () => {
  if (serverInstance && serverInstance.close) {
    serverInstance.close(() => {
      console.log("Servidor Express detenido.");
    });
  }
  app.quit();
});

