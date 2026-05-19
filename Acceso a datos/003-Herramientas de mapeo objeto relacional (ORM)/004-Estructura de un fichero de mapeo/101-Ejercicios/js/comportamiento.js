// Variables globales

var inicio = 0;
var id_conversacion = 0;

function iniciarSesion(){
  let usuario = localStorage.getItem("jocarsachatusuario")
  if(usuario == null){
    let contienemodal = document.querySelector("#contienemodal")
    contienemodal.style.display = "flex";
  }
}

function bienvenida(){
  fetch("api/bienvenida.php")
  .then(function(respuesta){return respuesta.json()})
  .then(function(datos){
    let titulo = document.querySelector("main section h1")
    titulo.textContent = datos[0].frase
  })
}

function cargaConversaciones(usuario){
  fetch("api/conversaciones.php?idusuario="+usuario)
  .then(function(respuesta){return respuesta.json()})
  .then(function(datos){
    let contenedor = document.querySelector("#conversaciones")
    datos.forEach(function(dato){
      let articulo = document.createElement("article")
      articulo.classList.add("conversacion")
      articulo.textContent = dato.descripcion
      articulo.onclick = function(){cargaMensajes(dato.Identificador)}
      contenedor.appendChild(articulo)
    })
  })
}

function cargaMensajes(id){
  console.log("has hecho click en el id: "+id)
  fetch("api/mensajes.php?id="+id)
  .then(function(respuesta){return respuesta.json()})
  .then(function(datos){
    let contenedor = document.querySelector("main section")
    contenedor.innerHTML = "" // Vaciamos el contenedor antes de carga más
    datos.forEach(function(dato){
      let mensaje = document.createElement("article")
      mensaje.classList.add("mensaje")
      if(dato.es_usuario == "1"){mensaje.classList.add("usuario")}
      mensaje.textContent = dato.mensaje_md
      contenedor.appendChild(mensaje)
    })
  })
}

function nuevaConversacion(){
  let logo = document.querySelector("nav img")
  logo.onclick = function(){
  console.log("ok logo click")
    let contenedor = document.querySelector("main section")
    contenedor.innerHTML = "<h1></h1>"
    bienvenida()
  }
}

function enviaMensaje(){
  let entrada = document.querySelector("main footer input")
  entrada.onkeyup = function(tecla){
    if(tecla.code == "Enter"){
      console.log("iniciamos una nueva conversación")
      let contenedor = document.querySelector("main section")
      //contenedor.innerHTML = ""
      let articulo = document.createElement("article")
      articulo.classList.add("mensaje")
      articulo.classList.add("usuario")
      articulo.textContent = entrada.value
      if(inicio == 0){
        fetch("api/creaconversacion.php?titulo="+encodeURI(entrada.value))
        .then(function(respuesta){return respuesta.json()})
        .then(function(datos){
          console.log("el id generado es:"+datos.id)
          id_conversacion = datos.id
        })
        inicio = 1; 
      }
      fetch("api/creamensaje.php?titulo="+encodeURI(entrada.value)+"&id="+id_conversacion)
      entrada.value = ""
      contenedor.appendChild(articulo)
      contenedor.scrollTop = 100000000000000000000;
    }
  }
}

function login(){
  let botonlogin = document.querySelector("#enviar")
  botonlogin.onclick = function(){
    console.log("voy a logear")
    let usuario = document.querySelector("#usuario").value
    let contrasena = document.querySelector("#contrasena").value
    fetch("api/login.php?usuario="+usuario+"&contrasena="+contrasena)
      .then(function(respuesta){return respuesta.json()})
      .then(function(datos){
        console.log("ok")
        console.log(datos)
        localStorage.setItem("jocarsachatusuario",datos[0].usuario)
        localStorage.setItem("jocarsachatidusuario",datos[0].Identificador)
        window.location = window.location;
      })
  }
}
function logout(){
  let botonlogout = document.querySelector("#logout")
  botonlogout.onclick = function(){
    localStorage.removeItem("jocarsachatusuario");
    localStorage.removeItem("jocarsachatidusuario");
    window.location = window.location;
  }
}

bienvenida()
cargaConversaciones(localStorage.getItem("jocarsachatidusuario"))
nuevaConversacion()
enviaMensaje()
iniciarSesion()
login()
logout()
