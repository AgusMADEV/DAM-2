const albumsDemo = [
  { titulo: "Álbum 1", artista: "Artista 1", portada: "https://via.placeholder.com/60" },
  { titulo: "Álbum 2", artista: "Artista 2", portada: "https://via.placeholder.com/60" },
  { titulo: "Álbum 3", artista: "Artista 3", portada: "https://via.placeholder.com/60" },
];

export function init({ root, navigate, state }) {
  const lista = root.querySelector("#lista-albumes");
  const btnConfig = root.querySelector("#btn-config");

  lista.innerHTML = albumsDemo.map(a => `
    <div class="album" data-titulo="${a.titulo}" data-artista="${a.artista}" data-portada="${a.portada}">
      <img src="${a.portada}" class="portada-album">
      <div class="info-album">
        <h3>${a.titulo}</h3>
        <p>${a.artista}</p>
      </div>
    </div>
  `).join("");

  lista.addEventListener("click", (e) => {
    const item = e.target.closest(".album");
    if (!item) return;

    state.album.titulo = item.dataset.titulo;
    state.album.artista = item.dataset.artista;
    state.album.portada = item.dataset.portada;

    navigate("album", { from: "principal" });
  });

  btnConfig.addEventListener("click", () => navigate("config"));
}

