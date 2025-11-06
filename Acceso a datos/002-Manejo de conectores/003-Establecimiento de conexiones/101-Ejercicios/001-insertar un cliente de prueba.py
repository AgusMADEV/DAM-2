import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="accesoadatos2526",
    password="Accesoadatos2526$",
    database="accesoadatos2526"
)

cursor = conexion.cursor()

cursor.execute('''
  INSERT INTO clientes
  VALUES(
    1,
    "Jose Vicente",
    "Carratala Sanchis",
    "info@jocarsa.com"
  );
''')

conexion.commit()

cursor.close()
conexion.close()
