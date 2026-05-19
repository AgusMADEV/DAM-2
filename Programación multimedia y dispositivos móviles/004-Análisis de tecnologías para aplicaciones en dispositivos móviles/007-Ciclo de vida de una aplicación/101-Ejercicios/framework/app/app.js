const grid = document.getElementById("grid");

const state = {
  album: {
    titulo: "Título del Álbum",
    artista: "Artista",
    canciones: [
      { nombre: "Canción 1", duracion: "3:45" },
      { nombre: "Canción 2", duracion: "4:20" },
      { nombre: "Canción 3", duracion: "3:10" },
    ],
    portada: "https://via.placeholder.com/200",
  },
};

const routes = {
  principal: { x: 0, y: 0, path: "screens/principal" },
  album:     { x: 1, y: 0, path: "screens/album" },
  config:    { x: 0, y: 1, path: "screens/config" },
  // (x:1,y:1) free slot if you want later
};

const loaded = new Map();

function moveTo(routeName) {
  const r = routes[routeName];
  if (!r) throw new Error(`Unknown route: ${routeName}`);
  const xPx = window.innerWidth * r.x;
  const yPx = window.innerHeight * r.y;
  grid.style.transform = `translate(${-xPx}px, ${-yPx}px)`;
}

function ensureSlotElements() {
  // build the 2x2 slots once
  if (grid.children.length) return;
  for (let i = 0; i < 4; i++) {
    const slot = document.createElement("div");
    slot.className = "screen-slot";
    slot.dataset.slot = String(i);
    grid.appendChild(slot);
  }
}

function slotIndexForRoute(routeName) {
  const r = routes[routeName];
  // 2 cols: index = y*2 + x
  return r.y * 2 + r.x;
}

async function loadScreen(routeName) {
  if (loaded.has(routeName)) return;

  const r = routes[routeName];
  const slot = grid.children[slotIndexForRoute(routeName)];

  // 1) HTML
  const html = await fetch(`${r.path}/screen.html`).then(res => res.text());
  slot.innerHTML = html;

  // 2) CSS (inject once per screen)
  const cssId = `css-${routeName}`;
  if (!document.getElementById(cssId)) {
    const css = await fetch(`${r.path}/screen.css`).then(res => res.text());
    const style = document.createElement("style");
    style.id = cssId;
    style.textContent = css;
    document.head.appendChild(style);
  }

  // 3) JS (module import)
  const mod = await import(`../${r.path}/screen.js`);
  if (typeof mod.init === "function") {
    mod.init({
      route: routeName,
      root: slot,
      navigate,
      state,
      setState: (patch) => Object.assign(state, patch),
    });
  }

  loaded.set(routeName, true);
}

async function navigate(routeName, params = {}) {
  await loadScreen(routeName);

  // If screen module exposes onShow, call it
  const r = routes[routeName];
  const mod = await import(`../${r.path}/screen.js`);
  if (typeof mod.onShow === "function") {
    mod.onShow({ route: routeName, params, state });
  }

  moveTo(routeName);
}

// Boot
ensureSlotElements();
await loadScreen("principal");
await loadScreen("album");
await loadScreen("config");
navigate("principal");

// Keep movement correct on resize
window.addEventListener("resize", () => {
  // Re-apply current transform by reading last route from hash (or track it)
  // Minimal approach: go back to principal; you can improve this.
  navigate("principal");
});

