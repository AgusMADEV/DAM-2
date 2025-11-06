He integrado una situación real de **deportes**: necesito listar los **partidos de fútbol** almacenados en mi BD para mostrarlos en una app/tabla.  
Para eso creo una clase `JVDB` que encapsula la **conexión MySQL** y un método que **consulta la tabla** y devuelve el resultado en **JSON**, ideal para APIs o frontends.

---

### Clase `JVDB` e instanciación
```python
import mysql.connector
import json

class JVDB():
  def __init__(self,host,usuario,contrasena,basedatos):
    self.host = host
    self.usuario = usuario
    self.contrasena = contrasena
    self.basedatos = basedatos

    self.conexion = mysql.connector.connect(
        host=self.host,
        user=self.usuario,
        password=self.contrasena,
        database=self.basedatos
    )

    self.cursor = self.conexion.cursor()
```
- El constructor guarda la **config** y abre la **conexión**.  
- `self.cursor` permite ejecutar SQL.

### Método `seleccionar_partidos`
```python
  def seleccionar_partidos(self, tabla):
    self.cursor.execute(f"SELECT * FROM {tabla}")
    columnas = self.cursor.column_names
    filas = self.cursor.fetchall()
    datos = [dict(zip(columnas, fila)) for fila in filas]
    return json.dumps(datos, ensure_ascii=False, indent=2, default=str)
```
- Ejecuta `SELECT * FROM {tabla}`.  
- Recupera `column_names` y `fetchall()` para obtener todas las filas.  
- **Mapea** cada fila a diccionario `columna → valor` y lo **serializa a JSON** con `json.dumps` (soporta fechas con `default=str`).

### Creación de instancia y uso
```python
conexion = JVDB("localhost","futbol_amadev","futbol_amadev","futbol_amadev")
```

---

### Consulta real: obtener y mostrar partidos
```python
print(conexion.seleccionar_partidos("partidos"))
```
**Salida esperada (ejemplo):**
```json
[
  {
    "id": 101,
    "local": "Agus United",
    "visitante": "Rival CF",
    "goles_local": 2,
    "goles_visitante": 1,
    "fecha": "2025-10-12 18:00:00"
  },
  {
    "id": 102,
    "local": "Agus United",
    "visitante": "Devs FC",
    "goles_local": 0,
    "goles_visitante": 0,
    "fecha": "2025-10-19 17:30:00"
  }
]
```
Con esto puedo **pintar la lista de partidos** en un frontend, alimentar una **API** o exportar a ficheros.

---

Esta actividad me ha ayudado a entender mejor el **acceso a datos con Python**: abrir conexión, lanzar consultas, **formatear resultados** y exponerlos en **JSON**.  
Aplicado a mi caso (deportes), ahora puedo listar **partidos jugados**, estadísticas o clasificaciones desde la base de datos y mostrarlos en mi app. Es la base para construir **paneles**, **endpoints** y flujos de análisis de cara a futuras sesiones.
