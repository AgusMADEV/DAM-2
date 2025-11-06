En esta actividad conecto una app de **gestión de deportes** (mi hobby) con una base de datos **MySQL** para preparar la tabla `clientes` y poder **insertar registros** desde Python. El flujo que voy a realizar es:
1) Abrir conexión con `mysql.connector`.2) Asegurar la **clave primaria** de `clientes`.3) Convertir `Identificador` en **AUTO_INCREMENT**.4) **Insertar** un cliente de ejemplo y confirmar con `commit()`.5) Cerrar recursos (cursor/conexión).

---

```python
import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="accesoadatos2526",
    password="accesoadatos2526",
    database="accesoadatos2526"
)

cursor = conexion.cursor()

# 1) Añadir PK si no existía
cursor.execute('''
  ALTER TABLE clientes
  ADD PRIMARY KEY (`Identificador`);
''')

# 2) Poner AUTO_INCREMENT en la PK
cursor.execute('''
  ALTER TABLE clientes
  MODIFY COLUMN Identificador INT NOT NULL AUTO_INCREMENT;
''')

# 3) Inserción de un cliente
cursor.execute('''
  INSERT INTO clientes
  VALUES(
    NULL,                -- Identificador (AUTO_INCREMENT)
    "Agustin",           -- nombre
    "Morcillo",          -- apellidos
    "info@agusmadev.es"  -- email
  );
''')

conexion.commit()
cursor.close()
conexion.close()
```

**Notas técnicas rápidas**
- La **PK** garantiza **unicidad** y acelera búsquedas.
- `AUTO_INCREMENT` evita tener que calcular IDs manualmente.

---

Para validar que todo va bien:
1) **Ejecuto** el script anterior.
2) En MySQL, **compruebo** la tabla y su estructura:
   ```sql
   SHOW TABLES;
   DESCRIBE clientes;
   ```
3) Verifico que el registro existe:
   ```sql
   SELECT * FROM clientes;
   ```

**Salida esperada (ejemplo):**
```
+---------------+--------------------+-----------+-------------------+
| Identificador | nombre             | apellidos | email             |
+---------------+--------------------+-----------+-------------------+
| 1             | Agustin (Viajar)   | Morcillo  | info@agusmadev.es |
+---------------+--------------------+-----------+-------------------+
```

---

El objetivo se cumple: dejo `clientes` con **PK + AUTO_INCREMENT** y probé una **inserción real** desde Python. Esto encaja con la unidad de **acceso a datos**: conecto la capa de aplicación con la base de datos y aplico buenas prácticas (transacciones, claves, parametrización).Como futuro **administrador de deportes digitales**, este patrón me sirve para guardar **usuarios, socios, staff o atletas** y ampliar después con altas/bajas, validaciones y paneles de gestión.
