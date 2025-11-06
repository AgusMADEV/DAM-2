import mysql.connector

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
  else:
    print("No me han programado para ese tipo de campo")

conn = mysql.connector.connect(
    host="localhost",
    user="desfase",
    password="desfase",
    database="desfase"
)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE `desfase`.`clientes` (`Identificador` INT NOT NULL AUTO_INCREMENT , `nombre` VARCHAR(255) NOT NULL , `apellidos` VARCHAR(255) NOT NULL , `email` VARCHAR(255) NOT NULL , PRIMARY KEY (`Identificador`)) ENGINE = InnoDB;
''')  







