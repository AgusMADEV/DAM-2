En este ejercicio, simulo una situación real en la que necesito **consultar datos de mis clientes o jugadores** desde una base de datos MySQL para una aplicación de **gestión deportiva digital**.  
Por ejemplo, podría querer mostrar una lista de participantes o usuarios registrados en un torneo.  
Para ello, aprendo a **establecer la conexión**, **ejecutar una consulta SQL** y **mostrar los resultados** usando Python.

---

El objetivo técnico es conectar Python con MySQL, realizar una consulta `SELECT` y recorrer los resultados con un bucle.  

```python
import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="accesoadatos2526",
    password="accesoadatos2526",
    database="accesoadatos2526"
)

cursor = conexion.cursor()

cursor.execute('''
  SELECT 
  nombre,
  apellidos,
  email
  FROM clientes;
''')

filas = cursor.fetchall()

for fila in filas:
  print(fila)

cursor.close()
conexion.close()
```

1. **Conexión:**  
   Se establece con `mysql.connector.connect()`, indicando el host, usuario, contraseña y base de datos.
2. **Creación del cursor:**  
   El objeto `cursor` permite ejecutar instrucciones SQL sobre la base de datos.
3. **Consulta SQL:**  
   Con `cursor.execute()` se lanza el comando `SELECT nombre, apellidos, email FROM clientes;` para obtener la información.
4. **Lectura de resultados:**  
   `fetchall()` recupera todas las filas resultantes de la consulta.
5. **Recorrido de filas:**  
   Un bucle `for` imprime cada registro de cliente.
6. **Cierre de recursos:**  
   Se cierran tanto el cursor como la conexión con `close()`.

---

Al ejecutar el código, se muestra una lista de tuplas con los datos de cada cliente.  
Por ejemplo, si en la base de datos están registrados algunos contactos relacionados con el ámbito deportivo, la salida puede ser:

```
('Agustin', 'Morcillo', 'info@agusmadev.es')
('Elena', 'Botezatu', 'info@elena.es')
('Lilo', 'Morcillo', 'info@lilo.es')
```

Esto demuestra que el programa lee correctamente los datos de la tabla `clientes` y los muestra en consola, algo muy útil para desarrollar paneles de control o listados dinámicos en aplicaciones deportivas o de gestión de eventos.

---

Este ejercicio me ha ayudado a entender cómo **recuperar y visualizar datos reales** desde una base de datos MySQL, conectando directamente con lo aprendido en la unidad de **acceso a datos**.  
En un contexto más práctico, como en una **aplicación de gestión deportiva**, esta técnica me permitiría mostrar listados de clientes, jugadores o usuarios conectados.  
Aprender a consultar y manejar resultados en Python me acerca un paso más al desarrollo de aplicaciones completas donde la información fluye desde la base de datos hasta la interfaz de usuario.
