clientes = [{
  "nombre":"Jose Vicente",
  "apellidos":"Carratala Sanchis",
  "emails":[
    {
      "tipo":"personal",
      "direcciones":[
        "info@josevicentecarratala.com",
        "jocarsa2@gmail.com"
       ]
    },
    {
      "tipo":"empresa",
      "direcciones":["info@jocarsa.com"]
    }
   ]
},{
  "nombre":"Jose Vicente",
  "apellidos":"Carratala Sanchis",
  "emails":[
    {
      "tipo":"personal",
      "direcciones":[
        "info@josevicentecarratala.com",
        "jocarsa2@gmail.com"
       ]
    },
    {
      "tipo":"empresa",
      "direcciones":["info@jocarsa.com"]
    }
   ]
}
]

muestra = clientes[0]
print(muestra)

for clave in muestra.keys():
  print(clave)
  print(type(muestra[clave]))
  if type(muestra[clave]) == str:
    print("Lo voy a convertir en una columna de SQL que sera de tipo varchar")
  elif type(muestra[clave]) == list:
    print("Lo voy a convertir en una tabla externa de SQL")
  elif type(muestra[clave]) == int:
    print("Lo voy a convertir en una columna de SQL que sera de tipo int ")
  elif:
    print("No me han programado para ese tipo de campo")










