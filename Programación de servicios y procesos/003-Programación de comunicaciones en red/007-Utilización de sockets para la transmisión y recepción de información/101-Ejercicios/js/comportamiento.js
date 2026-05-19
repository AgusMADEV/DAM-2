import { mdToHtml } from "../lib/jocarsa-md.js";


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
  inicio = 1
  id_conversacion = id
  fetch("api/mensajes.php?id="+id)
  .then(function(respuesta){return respuesta.json()})
  .then(function(datos){
    let contenedor = document.querySelector("main section")
    contenedor.innerHTML = "" // Vaciamos el contenedor antes de carga más
    datos.forEach(function(dato){
      let mensaje = document.createElement("article")
      mensaje.classList.add("mensaje")
      if(dato.es_usuario == "1"){mensaje.classList.add("usuario")}
      mensaje.innerHTML = mdToHtml(dato.mensaje_md)
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
  let botonentrada = document.querySelector("main footer button")
  botonentrada.onclick = function(){
    enviaMensajeReal()
  }
  
  let entrada = document.querySelector("main footer input")
  entrada.onkeyup = function(tecla){
    if(tecla.code == "Enter"){
      enviaMensajeReal()
    }
  }
}

function enviaMensajeReal(){
  let entrada = document.querySelector("main footer input")
      let valorentrada = entrada.value
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
          guardaMensaje(valorentrada)
        })
        inicio = 1; 
      }else{
        guardaMensaje(valorentrada)
      }
      
      contenedor.appendChild(articulo)
      
      entrada.value = ""
      contenedor.scrollTop = 100000000000000000000;
}

function guardaMensaje(valor){
let contenedor = document.querySelector("main section")
  fetch("api/creamensaje.php?titulo="+encodeURI(valor)+"&id="+id_conversacion+"&usuario=1")
      let modeloseleccionado = document.querySelector("select").value
      
      
        
      fetch("api/consultaia.php?question="+encodeURI(valor)+"&model="+modeloseleccionado)
      .then(function(respuesta){return respuesta.json()})
      .then(function(datos){
      let articulo = document.createElement("article")
       articulo.classList.add("mensaje")
        articulo.innerHTML = "Cargando..."
        articulo.innerHTML = mdToHtml(datos.answer) 
        fetch("api/creamensaje.php?titulo="+encodeURI(datos.answer)+"&id="+id_conversacion+"&usuario=0")
        contenedor.appendChild(articulo)
        contenedor.scrollTop = 100000000000000000000;
      })
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

function cargaModelos(){
  fetch("api/modelos.php")
      .then(function(respuesta){return respuesta.json()})
      .then(function(datos){
        let contenedor = document.querySelector("select")
        datos.forEach(function(dato){
          let opcion = document.createElement("option")
          opcion.value = dato.modelo
          opcion.textContent = dato.modelo
          contenedor.appendChild(opcion)
        })
      })
}

bienvenida()
cargaConversaciones(localStorage.getItem("jocarsachatidusuario"))
nuevaConversacion()
enviaMensaje()
iniciarSesion()
login()
logout()
cargaModelos()
