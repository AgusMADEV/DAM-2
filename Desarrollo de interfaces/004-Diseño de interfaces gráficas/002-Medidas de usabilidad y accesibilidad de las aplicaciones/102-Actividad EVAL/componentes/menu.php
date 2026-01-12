<style>
  #menu{
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  #menu button{
    padding: 14px 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s;
    text-align: left;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  }
  #menu button:hover{
    transform: translateX(5px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  }
  #menu button.active{
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
  }
  #menu h3{
    color: white;
    margin-bottom: 15px;
    font-size: 18px;
    text-align: center;
  }
</style>

<div id="menu">
  <h3>Menú Principal</h3>
  <button onclick="cargarSeccion('dashboard')">📊 Dashboard</button>
  <button onclick="cargarSeccion('clientes')">👥 Clientes</button>
  <button onclick="cargarSeccion('productos')">📦 Productos</button>
  <button onclick="cargarSeccion('ventas')">💰 Ventas</button>
  <button onclick="cargarSeccion('informes')">📈 Informes</button>
  <button onclick="cargarSeccion('configuracion')">⚙️ Configuración</button>
  <button onclick="cargarSeccion('usuarios')">👤 Usuarios</button>
  <button onclick="cerrarSesion()">🚪 Cerrar Sesión</button>
</div>

<script>
  function cargarSeccion(seccion){
    // Remover clase active de todos los botones
    let botones = document.querySelectorAll("#menu button");
    botones.forEach(btn => btn.classList.remove("active"));
    
    // Agregar clase active al botón clickeado
    event.target.classList.add("active");
    
    // Cargar contenido de la sección
    console.log("Cargando sección:", seccion);
    
    // Actualizar la URL con el parámetro de sección
    let urlActual = new URL(window.location);
    urlActual.searchParams.set('seccion', seccion);
    window.history.pushState({}, '', urlActual);
    
    // Aquí se puede cargar dinámicamente el contenido
    let contenido = document.querySelector("#principal section");
    if(contenido){
      contenido.innerHTML = `<h2>Sección: ${seccion.charAt(0).toUpperCase() + seccion.slice(1)}</h2>
                             <p>Contenido de la sección ${seccion}...</p>`;
    }
  }
  
  function cerrarSesion(){
    if(confirm("¿Está seguro que desea cerrar sesión?")){
      window.location.href = "login.php";
    }
  }
</script>
