<!-- componentes/menu.php -->
<style>
  #menu {
    display: flex;
    flex-direction: column;
    gap: calc(var(--hueco) / 2);
  }

  #menu button {
    background: var(--colorprincipal_claro2);
    border: 2px solid var(--colorprincipal);
    color: var(--colorprincipal);
    padding: var(--hueco);
    border-radius: calc(var(--radio_empalme) / 2);
    cursor: pointer;
    font-size: 1em;
    font-weight: 600;
    transition: all 0.3s ease;
  }

  #menu button:hover {
    background: var(--colorprincipal);
    color: white;
    transform: translateX(5px);
  }

  #menu button.activo {
    background: var(--colorprincipal);
    color: white;
  }

  #menu h3 {
    color: var(--colorprincipal);
    margin-bottom: calc(var(--hueco) / 2);
    font-size: 1.1em;
  }
</style>

<h3>📊 Tablas</h3>
<div id="menu"></div>

<script>
  // Cargar menú dinámicamente desde API
  fetch("api/index.php?action=tablas")
    .then(response => response.json())
    .then(datos => {
      const menu = document.querySelector("#menu");
      menu.innerHTML = '';

      if (Array.isArray(datos)) {
        datos.forEach(nombreTabla => {
          const boton = document.createElement("button");
          boton.textContent = nombreTabla;
          boton.dataset.tabla = nombreTabla;

          boton.addEventListener("click", () => {
            // Actualizar estado activo
            document.querySelectorAll("#menu button").forEach(b => {
              b.classList.remove("activo");
            });
            boton.classList.add("activo");

            // Cargar tabla
            if (typeof seleccionarTabla === "function") {
              seleccionarTabla(nombreTabla);
            }
          });

          menu.appendChild(boton);
        });

        // Cargar primera tabla automáticamente
        const primero = menu.querySelector("button");
        if (primero) {
          primero.click();
        }
      }
    })
    .catch(error => {
      console.error("Error cargando menú:", error);
      document.querySelector("#menu").innerHTML = 
        '<p style="color: red;">Error al cargar tablas</p>';
    });
</script>
