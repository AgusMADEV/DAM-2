let rootRef = null;

export function init({ root, navigate, state }) {
  rootRef = root;

  const btn = root.querySelector("#btn-volver");
  if (btn) {
    btn.addEventListener("click", () => navigate("principal"));
  }

  // Optional: render once in case you land here first
  render(state);
}

export function onShow({ state }) {
  render(state);
}

function render(state) {
  if (!rootRef) return;

  const portada = rootRef.querySelector("#portada-detalle");
  const titulo = rootRef.querySelector("#titulo-detalle");
  const artista = rootRef.querySelector("#artista-detalle");
  const lista = rootRef.querySelector("#lista-canciones");

  if (portada) portada.src = state.album.portada || "https://via.placeholder.com/200";
  if (titulo) titulo.textContent = state.album.titulo || "Título del Álbum";
  if (artista) artista.textContent = state.album.artista || "Artista";

  const canciones = Array.isArray(state.album.canciones) ? state.album.canciones : [];
  const cancionesHtml = canciones.map(c => `
    <div class="cancion">
      <span>${c.nombre}</span>
      <span>${c.duracion}</span>
    </div>
  `).join("");

  if (lista) {
    lista.innerHTML = `<h3>Canciones</h3>${cancionesHtml}`;
  }
}

