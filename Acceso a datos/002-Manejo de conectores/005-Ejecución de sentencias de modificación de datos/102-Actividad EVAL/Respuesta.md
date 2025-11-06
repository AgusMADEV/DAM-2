En este ejercicio práctico utilizo mi base de datos para **gestionar información relacionada con mis equipos favoritos**, igual que haría un gestor deportivo digital.  
Por ejemplo, si tengo una tabla `clientes` que almacena distintos usuarios o equipos, puedo **actualizar los nombres o datos** fácilmente usando sentencias SQL desde Python.  
Este tipo de operación es muy útil cuando se necesita **modificar registros existentes** sin volver a crearlos, como al cambiar el nombre de un equipo, su contacto o sus estadísticas.

---

Para realizar la actualización, establezco la conexión con la base de datos y ejecuto la sentencia `UPDATE` sobre la tabla `clientes`.  
La sentencia `UPDATE` en MySQL permite modificar uno o varios campos de un registro existente según una condición (`WHERE`).

```python
import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="accesoadatos2526",
    password="accesoadatos2526",
    database="accesoadatos2526"
)

cursor = conexion.cursor(dictionary=True)

cursor.execute('''
  UPDATE clientes SET nombre = "River Plate" WHERE Identificador = 3;
''')

conexion.commit()

cursor.close()
conexion.close()
```

### Explicación técnica:
1. **Conexión:** Se establece con el servidor MySQL mediante `mysql.connector.connect()`.  
2. **Cursor:** Se crea un cursor con `dictionary=True` para poder manejar resultados como diccionarios si fuera necesario.  
3. **Sentencia `UPDATE`:**  
   La línea principal `UPDATE clientes SET nombre = "River Plate" WHERE Identificador = 3;` cambia el valor del campo `nombre` en el registro cuyo identificador es 3.  
4. **Confirmación:** `conexion.commit()` guarda el cambio de forma definitiva en la base de datos.  
5. **Cierre:** Se cierran el cursor y la conexión para liberar recursos.

---

Si antes del cambio el registro 3 tenía el valor:
```
+---------------+-----------+-----------+-------------------+
| Identificador | nombre    | apellidos | email             |
+---------------+-----------+-----------+-------------------+
| 3             | Agustin   | Morcillo  | info@agusmadev.es |
+---------------+-----------+-----------+-------------------+
```

Después de ejecutar el programa, el resultado sería:
```
+---------------+--------------+-----------+-------------------+
| Identificador | nombre       | apellidos | email             |
+---------------+--------------+-----------+-------------------+
| 3             | River Plate  | Morcillo  | info@agusmadev.es |
+---------------+--------------+-----------+-------------------+
```

Esto demuestra el funcionamiento correcto de la sentencia `UPDATE`, aplicable tanto a la gestión de clientes como al mantenimiento de **equipos o usuarios deportivos** dentro de una base de datos.

---

Con esta práctica he comprendido cómo usar `UPDATE` desde Python para **editar registros en bases de datos MySQL**.  
Esto se conecta con el tema de **acceso y manipulación de datos**, donde el objetivo es aprender a modificar información de manera segura y controlada.  
En mi futuro como desarrollador o administrador de sistemas deportivos, esta técnica me servirá para actualizar **datos de equipos, resultados o usuarios** sin tener que recrear registros, lo que mejora la eficiencia en la gestión de información.
