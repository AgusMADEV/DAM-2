Como **administrador de deportes digitales**, es clave poder gestionar datos de forma estructurada: jugadores, equipos, clientes o incluso estadísticas.  
Este ejercicio muestra cómo **conectarse a una base de datos MySQL** desde Python para **crear una tabla** donde guardar información de clientes.  
Aprender esto me permite entender cómo funcionan las conexiones entre una aplicación y su base de datos, algo fundamental en el desarrollo de software deportivo, donde los datos cambian constantemente (inscripciones, usuarios, resultados, etc.).

---

El ejercicio se basa en establecer una **conexión MySQL**, ejecutar una instrucción **SQL de creación de tabla** y cerrar la conexión correctamente.

### Código utilizado:
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
```

1. **Conexión:** `mysql.connector.connect()` abre una conexión al servidor MySQL usando las credenciales indicadas.  
2. **Cursor:** el objeto `cursor` se utiliza para ejecutar sentencias SQL.  
3. **Creación de tabla:** el comando `CREATE TABLE` define los campos necesarios para los clientes: un `Identificador` numérico y datos personales básicos.  
4. **Commit:** guarda los cambios de forma definitiva en la base de datos.  
5. **Cierre:** se cierran correctamente tanto el cursor como la conexión para liberar recursos.

Después de ejecutar el programa, se puede comprobar la creación de la tabla con:
```sql
SHOW TABLES;
DESCRIBE clientes;
```
Esto muestra la lista de tablas y la estructura del campo de cada columna.

---

Al probar el código, la salida esperada en MySQL debe incluir la tabla recién creada:
```
+--------------------------+
| Tables_in_accesoadatos2526 |
+--------------------------+
| clientes                 |
+--------------------------+
```
Y al ejecutar `DESCRIBE clientes;`:
```
+---------------+--------------+------+-----+---------+-------+
| Field         | Type         | Null | Key | Default | Extra |
+---------------+--------------+------+-----+---------+-------+
| Identificador | int(11)      | NO   |     | NULL    |       |
| nombre        | varchar(255) | NO   |     | NULL    |       |
| apellidos     | varchar(255) | NO   |     | NULL    |       |
| email         | varchar(255) | NO   |     | NULL    |       |
+---------------+--------------+------+-----+---------+-------+
```
Esto confirma que la tabla se ha creado correctamente.

---

Este ejercicio me ha servido para ver cómo **Python puede comunicarse directamente con una base de datos MySQL**, algo esencial en el desarrollo de cualquier aplicación real.  
En mi futuro como **administrador o desarrollador de sistemas deportivos digitales**, podré usar esta misma base para guardar y consultar información sobre **usuarios, equipos o torneos**.  
Dominar la conexión y gestión de datos es clave para crear aplicaciones funcionales y seguras que respalden la organización y análisis de la información en el ámbito deportivo.
