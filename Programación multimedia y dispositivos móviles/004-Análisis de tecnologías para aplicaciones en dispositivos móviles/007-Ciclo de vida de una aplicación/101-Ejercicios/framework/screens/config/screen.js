export function init({ root, navigate, state }) {
  const inputTitulo = root.querySelector("#titulo-album");
  const inputArtista = root.querySelector("#artista-album");
  const inputCanciones = root.querySelector("#canciones");

  // Pre-fill from state
  inputTitulo.value = state.album.titulo ?? "";
  inputArtista.value = state.album.artista ?? "";
  inputCanciones.value = (state.album.canciones ?? []).map(c => c.nombre).join(", ");

  root.querySelector("#btn-volver").addEventListener("click", () => navigate("principal"));

  root.querySelector("#btn-guardar").addEventListener("click", () => {
    state.album.titulo = inputTitulo.value.trim() || "Sin título";
    state.album.artista = inputArtista.value.trim() || "Sin artista";

    const nombres = inputCanciones.value
      .split(",")
      .map(s => s.trim())
      .filter(Boolean);

    state.album.canciones = nombres.length
      ? nombres.map((n, i) => ({ nombre: n, duracion: ["3:45","4:20","3:10"][i % 3] }))
      : [];

    alert("Mockup guardado");
    navigate("principal");
  });
}

