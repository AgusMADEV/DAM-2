<!-- componentes/tabla.php -->
<style>
  #tabla{
    width:100%;
    border-collapse:collapse;
    /* velocidad por defecto entre celdas (puedes cambiarla también aquí) */
    --tabla-velocidad: 40ms;
  }
  #tabla thead tr{
    background:var(--colorprincipal);
    border-radius:40px;
  }
  #tabla thead tr th:first-child{
    border-radius:var(--radio_empalme) 0px 0px var(--radio_empalme);
  }
  #tabla thead tr th:last-child{
    border-radius:0px var(--radio_empalme) var(--radio_empalme) 0px;
  }
  #tabla td, #tabla th{
    padding:calc(var(--hueco)/2);
  }
  #tabla tr{
    border-bottom:1px solid var(--colorprincipal);
  }

  /* Estado inicial para animación en cascada */
  #tabla.tabla-animada thead th,
  #tabla.tabla-animada tbody td{
    opacity:0;
    /* ESCALA DESDE EL CENTRO */
    transform:scale(0.4);
    transform-origin:center center;
    animation: tablaPopIn 0.4s ease-out forwards;
    /* cada celda tiene un índice y se multiplica por la velocidad */
    animation-delay: calc(var(--delay-index, 0) * var(--tabla-velocidad));
  }

  @keyframes tablaPopIn{
    0%{
      opacity:0;
      transform:scale(0.4);
    }
    60%{
      opacity:1;
      transform:scale(1.03); /* pequeño overshoot para dar “punch” */
    }
    100%{
      opacity:1;
      transform:scale(1);
    }
  }
</style>

<table id="tabla">
  <thead></thead>
  <tbody></tbody>
</table>

<script>
  /**
   * Parámetro global de velocidad (ms entre celdas).
   * Cambia este valor para hacer la cascada más rápida o más lenta.
   * Ejemplo: window.velocidadTablaMs = 100;
   */
  window.velocidadTablaMs = 15;

  /**
   * CONTROLADOR de interfaz:
   * Dado un nombre de tabla, pide los datos al API y llama a la vista.
   */
  function seleccionarTabla(nombreTabla) {
    const url = "api/tabla?tabla=" + encodeURIComponent(nombreTabla);

    fetch(url)
      .then(respuesta => {
        if (!respuesta.ok) {
          throw new Error("Error al cargar la tabla: " + nombreTabla);
        }
        return respuesta.json();
      })
      .then(datos => {
        construirTabla(datos);
      })
      .catch(error => {
        console.error(error);
      });
  }

  /**
   * VISTA:
   * Construye la tabla HTML a partir de un array de objetos.
   * Añade animación en cascada a las celdas.
   */
  function construirTabla(datos, velocidadMs = window.velocidadTablaMs) {
    const tabla = document.getElementById('tabla');
    const thead = tabla.querySelector('thead');
    const tbody = tabla.querySelector('tbody');

    // Limpiar antes de pintar de nuevo
    thead.innerHTML = '';
    tbody.innerHTML = '';

    // quitar clase de animación para poder re-aplicarla
    tabla.classList.remove('tabla-animada');

    if (!Array.isArray(datos) || datos.length === 0) {
      const trVacio = document.createElement('tr');
      const tdVacio = document.createElement('td');
      tdVacio.colSpan = 6;
      tdVacio.textContent = 'No hay datos';
      trVacio.appendChild(tdVacio);
      tbody.appendChild(trVacio);
      return;
    }

    const columnas = Object.keys(datos[0]);

    // Índice global para el retraso en cascada
    let indiceDelay = 0;

    // Cabecera
    const trHead = document.createElement('tr');
    columnas.forEach(col => {
      const th = document.createElement('th');
      th.textContent = col;
      th.style.setProperty('--delay-index', indiceDelay++);
      trHead.appendChild(th);
    });
    thead.appendChild(trHead);

    // Cuerpo
    datos.forEach(fila => {
      const tr = document.createElement('tr');
      columnas.forEach(col => {
        const td = document.createElement('td');
        td.textContent = fila[col];
        td.style.setProperty('--delay-index', indiceDelay++);
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });

    // Pasar velocidad a CSS (ms entre celdas)
    tabla.style.setProperty('--tabla-velocidad', velocidadMs + 'ms');

    // Forzar reflow para reiniciar la animación
    void tabla.offsetWidth;

    // Activar animación
    tabla.classList.add('tabla-animada');
  }

  // El menú seguirá llamando a seleccionarTabla(nombreTabla)
  // y cada carga disparará la animación en cascada.
</script>

