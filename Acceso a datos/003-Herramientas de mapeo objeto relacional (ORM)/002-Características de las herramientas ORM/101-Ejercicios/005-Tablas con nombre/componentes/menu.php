<!-- componentes/menu.php -->
<style>
  #menu{
    display:flex;
    flex-direction:column;
    gap:var(--hueco);
  }
  #menu button{
    background:var(--colorprincipal_claro2);
    border:none;
  }
</style>

<div id="menu"></div>

<script>
  fetch("api/menu")
    .then(response => response.json())
    .then(datos => {
      const menu = document.querySelector("#menu");

      datos.forEach(nombreTabla => {
        const boton = document.createElement("button");
        boton.textContent = nombreTabla;
        boton.dataset.tabla = nombreTabla;

        boton.addEventListener("click", () => {
          // >>> Aquí llamas al controlador de la vista tabla
          if (typeof seleccionarTabla === "function") {
            seleccionarTabla(nombreTabla);
          } else {
            console.error("Controlador seleccionarTabla no está definido todavía");
          }
        });

        menu.appendChild(boton);
      });

      // Opcional: cargar automáticamente la primera tabla
      const primero = menu.querySelector("button");
      if (primero && typeof seleccionarTabla === "function") {
        seleccionarTabla(primero.dataset.tabla);
      }
    });
</script>

