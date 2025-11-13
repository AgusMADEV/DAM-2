// Librería Simple de Componentes UI
// Basada en patrones vistos en clase

// ============================================
// COMPONENTE 1: TABLA CON BÚSQUEDA
// ============================================
function crearTabla(contenedorId, opciones) {
  const contenedor = document.getElementById(contenedorId);
  const { titulo, columnas, datos } = opciones;
  
  let datosFiltrados = [...datos];
  
  // Crear estructura HTML
  contenedor.innerHTML = `
    <div class="tabla-contenedor">
      <div class="tabla-header">
        <h3>${titulo}</h3>
        <input type="search" class="tabla-buscar" placeholder="Buscar...">
      </div>
      <table class="tabla">
        <thead>
          <tr>${columnas.map(col => `<th>${col.label}</th>`).join('')}</tr>
        </thead>
        <tbody class="tabla-body"></tbody>
      </table>
    </div>
  `;
  
  const buscarInput = contenedor.querySelector('.tabla-buscar');
  const tbody = contenedor.querySelector('.tabla-body');
  
  // Función para renderizar filas
  function renderizar(datos) {
    tbody.innerHTML = datos.map(fila => `
      <tr>
        ${columnas.map(col => `<td>${fila[col.campo]}</td>`).join('')}
      </tr>
    `).join('');
  }
  
  // Búsqueda
  buscarInput.addEventListener('input', (e) => {
    const termino = e.target.value.toLowerCase();
    datosFiltrados = datos.filter(fila => 
      columnas.some(col => 
        String(fila[col.campo]).toLowerCase().includes(termino)
      )
    );
    renderizar(datosFiltrados);
  });
  
  // Renderizar inicial
  renderizar(datosFiltrados);
}

// ============================================
// COMPONENTE 2: SELECT CON BÚSQUEDA
// ============================================
function crearSelectBuscable(selectId) {
  const select = document.getElementById(selectId);
  const opciones = Array.from(select.options).map(opt => ({
    valor: opt.value,
    texto: opt.text
  }));
  
  // Crear contenedor
  const contenedor = document.createElement('div');
  contenedor.className = 'select-buscable';
  select.parentNode.insertBefore(contenedor, select);
  contenedor.appendChild(select);
  select.style.display = 'none';
  
  // Crear input
  const input = document.createElement('input');
  input.type = 'text';
  input.className = 'select-input';
  input.placeholder = 'Buscar...';
  contenedor.appendChild(input);
  
  // Crear panel de opciones
  const panel = document.createElement('div');
  panel.className = 'select-panel';
  contenedor.appendChild(panel);
  
  // Renderizar opciones
  function mostrarOpciones(filtro = '') {
    const opcionesFiltradas = opciones.filter(opt => 
      opt.texto.toLowerCase().includes(filtro.toLowerCase())
    );
    
    panel.innerHTML = opcionesFiltradas.map(opt => `
      <div class="select-opcion" data-valor="${opt.valor}">${opt.texto}</div>
    `).join('');
    
    // Click en opción
    panel.querySelectorAll('.select-opcion').forEach(opcion => {
      opcion.addEventListener('click', () => {
        select.value = opcion.dataset.valor;
        input.value = opcion.textContent;
        panel.style.display = 'none';
      });
    });
  }
  
  // Eventos
  input.addEventListener('focus', () => {
    panel.style.display = 'block';
    mostrarOpciones();
  });
  
  input.addEventListener('input', (e) => {
    mostrarOpciones(e.target.value);
  });
  
  document.addEventListener('click', (e) => {
    if (!contenedor.contains(e.target)) {
      panel.style.display = 'none';
    }
  });
}

// ============================================
// COMPONENTE 3: GRÁFICO DE BARRAS
// ============================================
function crearGrafico(canvasId, opciones) {
  const canvas = document.getElementById(canvasId);
  const ctx = canvas.getContext('2d');
  const { titulo, etiquetas, valores } = opciones;
  
  // Configuración
  const padding = 50;
  const ancho = canvas.width - padding * 2;
  const alto = canvas.height - padding * 2;
  const maxValor = Math.max(...valores);
  const anchoBar = ancho / valores.length * 0.7;
  
  // Limpiar
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  // Título
  ctx.fillStyle = '#333';
  ctx.font = 'bold 16px Arial';
  ctx.textAlign = 'center';
  ctx.fillText(titulo, canvas.width / 2, 30);
  
  // Dibujar barras
  valores.forEach((valor, i) => {
    const altoBarra = (valor / maxValor) * alto;
    const x = padding + i * (ancho / valores.length);
    const y = canvas.height - padding - altoBarra;
    
    // Barra
    ctx.fillStyle = '#3b82f6';
    ctx.fillRect(x, y, anchoBar, altoBarra);
    
    // Valor
    ctx.fillStyle = '#333';
    ctx.font = '12px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(valor, x + anchoBar / 2, y - 5);
    
    // Etiqueta
    ctx.fillText(etiquetas[i], x + anchoBar / 2, canvas.height - padding + 20);
  });
}

// ============================================
// COMPONENTE 4: TARJETA DE ESTADÍSTICA
// ============================================
function crearTarjeta(contenedorId, opciones) {
  const contenedor = document.getElementById(contenedorId);
  const { titulo, valor, icono, color } = opciones;
  
  contenedor.innerHTML = `
    <div class="tarjeta-stat" style="border-left: 4px solid ${color || '#3b82f6'}">
      <div class="tarjeta-icono">${icono || '📊'}</div>
      <div class="tarjeta-info">
        <div class="tarjeta-titulo">${titulo}</div>
        <div class="tarjeta-valor">${valor}</div>
      </div>
    </div>
  `;
}

// ============================================
// COMPONENTE 5: PANEL DE INFORME
// ============================================
function crearInforme(contenedorId, opciones) {
  const contenedor = document.getElementById(contenedorId);
  const { titulo, contenido } = opciones;
  
  contenedor.innerHTML = `
    <div class="informe-panel">
      <div class="informe-header">
        <h3>${titulo}</h3>
      </div>
      <div class="informe-body">
        ${contenido}
      </div>
    </div>
  `;
}
