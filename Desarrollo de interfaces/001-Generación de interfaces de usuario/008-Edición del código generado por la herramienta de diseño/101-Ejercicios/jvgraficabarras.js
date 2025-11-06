function graficaBarras(selector,misdatos,color){
      
  let grafica = document.querySelector(selector);
  
  let tabla = document.createElement("table");
  tabla.classList.add("jvgraficabarras")
  grafica.appendChild(tabla)
  
  let cabecera = document.createElement("thead");
  tabla.appendChild(cabecera)
  
  let filacabecera = document.createElement("tr");
  filacabecera.innerHTML = "<th>Valor</th><th>Gráfica</th>"
  cabecera.appendChild(filacabecera)
  
  let cuerpo = document.createElement("tbody");
  tabla.appendChild(cuerpo);
  
  misdatos.forEach(function(dato){
  console.log("hola")
 
    let fila = document.createElement("tr")
    cuerpo.appendChild(fila);
     
    let valor = document.createElement("td")
    valor.textContent = dato.Valor
    fila.appendChild(valor)
    
    let contienebarra = document.createElement("td")
    let barra = document.createElement("div")
    barra.classList.add("barra")
    barra.textContent = dato.Etiqueta
    barra.style.width = dato.Valor+"px"
    barra.style.backgroundColor = color
    contienebarra.appendChild(barra)
    
    fila.appendChild(contienebarra)
    
  })
}
