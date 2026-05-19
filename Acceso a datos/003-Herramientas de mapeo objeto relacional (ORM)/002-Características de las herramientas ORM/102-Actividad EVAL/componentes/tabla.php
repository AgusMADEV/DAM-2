<!-- componentes/tabla.php -->
<style>
  #tabla-contenedor {
    display: flex;
    flex-direction: column;
    min-height: 0;
    flex: 1;
  }

  #tabla {
    width: 100%;
    border-collapse: collapse;
    --tabla-velocidad: 30ms;
    font-size: 0.94em;
    flex: 1;
    table-layout: auto;
  }

  #tabla thead tr {
    background: var(--colorprincipal);
    color: white;
    position: sticky;
    top: 0;
    z-index: 10;
  }

  #tabla thead tr th:first-child {
    border-radius: 0;
  }

  #tabla thead tr th:last-child {
    border-radius: 0;
  }

  #tabla th {
    padding: 12px 10px;
    text-align: left;
    font-weight: 700;
    white-space: nowrap;
    font-size: 0.85em;
    text-transform: uppercase;
    letter-spacing: 0.4px;
    border-right: 1px solid rgba(255, 255, 255, 0.15);
    min-width: auto;
  }

  #tabla th:last-child {
    border-right: none;
  }

  #tabla td {
    padding: 11px 10px;
    text-align: left;
    color: #555;
    word-break: break-word;
    overflow-wrap: break-word;
  }

  #tabla tr {
    border-bottom: 1px solid #e8e8e8;
  }

  #tabla tbody tr:hover {
    background: #f8f9fa;
  }

  #tabla tbody tr:nth-child(even) {
    background: #fafbfc;
  }

  #tabla tbody tr:last-child {
    border-bottom: none;
  }

  /* Animación en cascada */
  #tabla.tabla-animada thead th,
  #tabla.tabla-animada tbody td {
    opacity: 0;
    transform: scale(0.4);
    transform-origin: center center;
    animation: tablaPopIn 0.3s ease-out forwards;
    animation-delay: calc(var(--delay-index, 0) * var(--tabla-velocidad));
  }

  @keyframes tablaPopIn {
    0% {
      opacity: 0;
      transform: scale(0.4);
    }
    70% {
      opacity: 1;
      transform: scale(1.02);
    }
    100% {
      opacity: 1;
      transform: scale(1);
    }
  }

  .cargando {
    text-align: center;
    padding: 30px;
    color: var(--color_accent);
    font-size: 1.05em;
    font-weight: 600;
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  #tabla-vacio {
    text-align: center;
    padding: 30px;
    color: #999;
    font-size: 1em;
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
  }
</style>

<div id="tabla-contenedor">
  <div class="cargando" id="cargando" style="display:none;">
    ⏳ Cargando datos...
  </div>

  <div id="tabla-vacio" style="display:none;">
    📊 Sin datos disponibles
  </div>

  <table id="tabla" class="tabla-animada">
    <thead>
      <tr></tr>
    </thead>
    <tbody></tbody>
  </table>
</div>

<script>
  window.velocidadTablaMs = 15;

  /**
   * CONTROLADOR: Carga una tabla desde el API
   */
  function seleccionarTabla(nombreTabla) {
    document.getElementById("cargando").style.display = "flex";
    document.getElementById("tabla-vacio").style.display = "none";
    document.getElementById("tabla").style.display = "none";

    const url = "api/index.php?action=seleccionar&tabla=" + encodeURIComponent(nombreTabla);

    fetch(url)
      .then(respuesta => {
        if (!respuesta.ok) {
          throw new Error("Error: " + nombreTabla);
        }
        return respuesta.json();
      })
      .then(datos => {
        construirTabla(datos);
        document.getElementById("cargando").style.display = "none";
        document.getElementById("tabla").style.display = "table";
      })
      .catch(error => {
        console.error(error);
        document.getElementById("tabla-vacio").innerHTML = 
          '❌ Error al cargar datos de: <strong>' + nombreTabla + '</strong>';
        document.getElementById("tabla-vacio").style.display = "flex";
        document.getElementById("cargando").style.display = "none";
        document.getElementById("tabla").style.display = "none";
      });
  }

  /**
   * VISTA: Construye la tabla HTML con animación
   */
  function construirTabla(datos, velocidadMs = window.velocidadTablaMs) {
    if (!Array.isArray(datos) || datos.length === 0) {
      document.getElementById("tabla-vacio").style.display = "flex";
      document.getElementById("tabla").style.display = "none";
      return;
    }

    const tabla = document.getElementById("tabla");
    const thead = tabla.querySelector("thead tr");
    const tbody = tabla.querySelector("tbody");

    thead.innerHTML = "";
    tbody.innerHTML = "";

    // Crear encabezados
    const columnas = Object.keys(datos[0]);
    columnas.forEach((columna, i) => {
      const th = document.createElement("th");
      th.textContent = columna.replace(/_/g, ' ');
      th.style.setProperty("--delay-index", i);
      thead.appendChild(th);
    });

    // Crear filas
    datos.forEach((fila, filaIndex) => {
      const tr = document.createElement("tr");

      columnas.forEach((columna, colIndex) => {
        const td = document.createElement("td");
        const valor = fila[columna];
        
        // Truncar valores muy largos
        if (valor && typeof valor === 'string' && valor.length > 50) {
          td.textContent = valor.substring(0, 47) + '...';
          td.title = valor;
        } else {
          td.textContent = valor || "";
        }
        
        td.style.setProperty("--delay-index", (filaIndex * columnas.length) + colIndex);
        tr.appendChild(td);
      });

      tbody.appendChild(tr);
    });

    // Forzar reflow para activar animación
    tabla.offsetHeight;
    tabla.classList.remove("tabla-animada");
    tabla.offsetHeight;
    tabla.classList.add("tabla-animada");
  }
</script>
