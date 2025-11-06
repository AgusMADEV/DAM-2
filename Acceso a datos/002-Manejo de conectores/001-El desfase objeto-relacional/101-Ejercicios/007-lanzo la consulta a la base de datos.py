import mysql.connector

clientes = {
  "nombre":"Jose Vicente",
  "apellidos":"Carratala Sanchis",
  "dni":"45325345G",
  "edad":47,
  "emails":[
    {
      "tipo":"personal",
      "direccion":
        "info@josevicentecarratala.com",
        
    },
    {
      "tipo":"empresa",
      "direcciones":["info@jocarsa.com"]
    }
   ]
},{
  "nombre":"Jose Vicente",
  "apellidos":"Carratala Sanchis",
  "dni":"45325345G",
  "edad":45,
  "emails":[
    {
      "tipo":"personal",
      "direccion":
        "info@josevicentecarratala.com",
    },
    {
      "tipo":"empresa",
      "direcciones":["info@jocarsa.com"]
    }
   ]
}

muestra = clientes[0]
print(muestra)

campos = []

for clave in muestra.keys():
  print(clave)
  print(type(muestra[clave]))
  if type(muestra[clave]) == str:
    print("Lo voy a convertir en una columna de SQL que sera de tipo varchar")
    campos.append(clave)
  elif type(muestra[clave]) == list:
    print("Lo voy a convertir en una tabla externa de SQL")
  elif type(muestra[clave]) == int:
    print("Lo voy a convertir en una columna de SQL que sera de tipo int ")
    campos.append(clave)
  else:
    print("No me han programado para ese tipo de campo")

conn = mysql.connector.connect(
    host="localhost",
    user="desfase",
    password="desfase",
    database="desfase"
)

cadena = '''
CREATE TABLE `desfase`.`clientes` (
  `Identificador` INT NOT NULL AUTO_INCREMENT ,
  '''
for campo in campos:
  if type(campo) is str:
    cadena += ''' 
    `'''+campo+'''` VARCHAR(255) NOT NULL , 
    '''
  elif type(campo) is int:
    cadena += ''' 
    `'''+campo+'''` INT(255) NOT NULL , 
    '''
    
cadena += '''
  
  PRIMARY KEY (`Identificador`)
) ENGINE = InnoDB;
'''

print(cadena)
cursor = conn.cursor()
cursor.execute("DROP TABLE clientes;")  
cursor.execute(cadena)







