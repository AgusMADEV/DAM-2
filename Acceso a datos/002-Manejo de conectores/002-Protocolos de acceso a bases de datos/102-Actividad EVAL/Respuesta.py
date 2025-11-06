import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="accesoadatos2526",
    password="accesoadatos2526",
    database="accesoadatos2526"
)

cursor = conexion.cursor()

cursor.execute('''
  CREATE TABLE `clientes` (
  `Identificador` INT NOT NULL , 
  `nombre` VARCHAR(255) NOT NULL , 
  `apellidos` VARCHAR(255) NOT NULL , 
  `email` VARCHAR(255) NOT NULL  
) ENGINE = InnoDB;
''')

conexion.commit()

cursor.close()
conexion.close()

##### COMPROBACIÓN CON SQL #####

'''
SHOW TABLES;

DESCRIBE clientes;
'''