<style>
  #pantalla_favoritos{
    display:none;
  }
  #pantalla_favoritos header{
    display:flex;
    align-items:center;
    gap:20px;
    margin-bottom:20px;
  }
  #pantalla_favoritos header button{
    background:#333;
    color:white;
    border:none;
    border-radius:50%;
    width:40px;
    height:40px;
    font-size:20px;
    cursor:pointer;
  }
  #pantalla_favoritos header h2{
    margin:0;
  }
  #lista_favoritos{
    display:grid;
    grid-template-columns:1fr;
    gap:15px;
  }
  #lista_favoritos article{
    display:flex;
    align-items:center;
    gap:15px;
    background:#1a1a1a;
    padding:10px;
    border-radius:10px;
    cursor:pointer;
    transition:background 0.3s;
  }
  #lista_favoritos article:hover{
    background:#282828;
  }
  #lista_favoritos article img{
    width:80px;
    height:80px;
    border-radius:5px;
    object-fit:cover;
  }
  #lista_favoritos article p{
    font-size:16px;
    font-weight:bold;
    margin:0;
  }
</style>

<div id="pantalla_favoritos">
  <header>
    <button id="btn_volver">←</button>
    <h2>Favoritos</h2>
  </header>
  <section id="lista_favoritos">
    
  </section>
</div>

<script>
  let contenedor_favoritos = document.querySelector("#lista_favoritos")
  let btn_volver = document.querySelector("#btn_volver")
  
  // Botón para volver a la pantalla de inicio
  btn_volver.onclick = function(){
    document.querySelector("#pantalla_favoritos").style.display = "none"
    document.querySelector("#pantalla_inicio").style.display = "flex"
  }
  
  // Cargar artistas favoritos desde la API
  fetch("api/favoritos.json")
  .then(function(respuesta){return respuesta.json()})
  .then(function(datos){
    datos.favorites.forEach(function(dato){
      let plantilla = document.querySelector("#elemento_lista")
      let instancia = plantilla.content.cloneNode(true)
      let articulo = instancia.querySelector("article")
      articulo.querySelector("p").textContent = dato.artist
      articulo.querySelector("img").setAttribute("src",dato.image)
      contenedor_favoritos.appendChild(instancia)
      
      // Al hacer clic en un artista, mostrar la pantalla de lista
      articulo.onclick = function(){
        document.querySelector("#pantalla_favoritos").style.display = "none"
        document.querySelector("#pantalla_lista").style.display = "block"
      }
    })
  })
</script>
