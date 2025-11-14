En esta actividad he desarrollado una pequeña aplicación web que genera dinámicamente una **interfaz de formulario** a partir de un archivo XML (`interfaz.xml`) y guarda la información introducida por la persona usuaria en una base de datos **SQLite** (`odoo.db`).

Aunque el ejemplo está orientado a la gestión de **clientes**, la misma idea se puede aplicar fácilmente a otros contextos que conozco, como la gestión de **jugadores de un equipo**, listas de **personajes de un videojuego online** o control de **estadísticas de partidos**. En todos estos casos necesito:

- Una interfaz web sencilla donde introducir datos (nombre, apellidos, email, alias de jugador, equipo, etc.).
- Un sistema que **guarde la información de forma estructurada** en una base de datos para poder consultarla después.

El objetivo principal ha sido **automatizar la creación del formulario** a partir del XML y garantizar que **todos los datos introducidos se almacenan correctamente en SQLite**, utilizando únicamente las herramientas vistas en clase (Python, Flask, XML y SQLite).

---

### Generación de la interfaz desde el archivo XML

La función principal para generar la interfaz es `miInterfaz(destino)` dentro de `mifuncion.py`. Esta función:

1. **Carga y analiza el XML** usando `xml.etree.ElementTree`:

```python
tree = ET.parse(destino)
root = tree.getroot()
```

2. **Recorre los elementos del XML** y, según la etiqueta (`campotexto` o `areadetexto`), genera los campos HTML correspondientes:

```python
for campo in root:
    if campo.tag == "campotexto":
        cadena += f"<label for='{campo.get('nombre')}'>{campo.get('nombre').title()}:</label>"
        cadena += f"<input type='text' name='{campo.get('nombre')}' placeholder='{campo.get('nombre')}'><br>"
    elif campo.tag == "areadetexto":
        cadena += f"<label for='{campo.get('nombre')}'>{campo.get('nombre').title()}:</label>"
        cadena += f"<textarea name='{campo.get('nombre')}'></textarea><br>"
```

3. Cierra el formulario añadiendo un botón de envío:

```python
cadena += "<input type='submit' value='Guardar'></form>"
```

De esta forma, **si mañana cambio el XML** (por ejemplo, añadiendo un nuevo campo para “equipo” o “posición en el juego”), el formulario web se actualizará automáticamente sin tocar el código HTML a mano.

###  Creación y uso de la base de datos SQLite

En la misma función `miInterfaz`, después de leer el XML, se construye dinámicamente la sentencia SQL de creación de la tabla `interfaz`:

```python
campos_sql = []
for campo in root:
    if campo.tag == "campotexto":
        campos_sql.append(f'"{campo.get("nombre")}" TEXT')
    elif campo.tag == "areadetexto":
        campos_sql.append(f'"{campo.get("nombre")}" TEXT')
```

Si hay campos definidos en el XML, se genera la tabla con esos nombres de columna y un **Identificador autoincremental**:

```python
peticion = f'''
CREATE TABLE IF NOT EXISTS "interfaz" (
      "Identificador" INTEGER,
      {', '.join(campos_sql)},
      PRIMARY KEY("Identificador" AUTOINCREMENT)
);
'''
```

La conexión se realiza con SQLite usando solo la librería estándar:

```python
conexion = sqlite3.connect("odoo.db")
cursor = conexion.cursor()
cursor.execute(peticion)
conexion.commit()
conexion.close()
```

### Inserción de datos en la base de datos

La función `guardarDatos(datos)` se encarga de guardar la información enviada desde el formulario:

1. Se conecta a la base de datos `odoo.db`.
2. Filtra los datos vacíos para no insertar campos sin contenido:

```python
datos_filtrados = {k: v for k, v in datos.items() if v.strip()}
```

3. Construye la sentencia `INSERT` de forma dinámica, utilizando **placeholders** para evitar errores:

```python
campos = list(datos_filtrados.keys())
valores = list(datos_filtrados.values())
campos_escapados = [f'"{campo}"' for campo in campos]

query = f"INSERT INTO interfaz ({', '.join(campos_escapados)}) VALUES ({', '.join(['?' for _ in valores])})"
cursor.execute(query, valores)
```

4. Se hace `commit` y se cierra la conexión.

Con esto se cumple el criterio de que **los datos introducidos en la interfaz web se almacenen correctamente en la base de datos SQLite**.

### Lógica del servidor web (servidor.py)

En `servidor.py` se usa **Flask** para gestionar las peticiones:

- En una petición **GET**, simplemente se llama a `miInterfaz("interfaz.xml")` y se devuelve el formulario generado.
- En una petición **POST**, se leen los campos desde el XML para saber qué nombres buscar en `request.form`, se construye un diccionario `datos` y se llama a `guardarDatos(datos)`:

```python
tree = ET.parse("interfaz.xml")
root = tree.getroot()

datos = {}
for campo in root:
    nombre_campo = campo.get('nombre')
    if nombre_campo:
        datos[nombre_campo] = request.form.get(nombre_campo, '')
```

Después de guardar los datos, se muestra un mensaje de confirmación con los valores almacenados.

En resumen, **el flujo completo funciona sin errores**: el formulario se genera desde el XML, se muestran los campos en la web, y al enviar el formulario los datos se guardan en SQLite.

---

Para comprobar que todo funcionaba correctamente, he seguido estos pasos:

1. He ejecutado el servidor con:

   ```bash
   python servidor.py
   ```

2. He accedido desde el navegador a `http://localhost:5000/` y he visto el formulario generado automáticamente a partir de `interfaz.xml` (por ejemplo, con campos como `nombre`, `apellidos`, `email`).

3. He rellenado el formulario con datos de prueba, simulando que fueran datos de un **jugador de e-sports** o de un **cliente**:

   - nombre: `Laura`
   - apellidos: `Gómez`
   - email: `laura@example.com`

4. Al pulsar en **“Guardar”**, la aplicación ha mostrado un mensaje:

   > “Datos guardados correctamente”  
   > y una lista con los valores enviados.

5. Finalmente, he comprobado en la base de datos SQLite (`odoo.db`) que se había creado la tabla `interfaz` y que el registro con los datos de `Laura` estaba almacenado correctamente.

Este ejemplo práctico demuestra que:

- La **interfaz web** se genera a partir del XML.
- El **código Python** es claro, se entiende bien la separación entre la generación de interfaz (`mifuncion.py`) y la lógica del servidor (`servidor.py`).
- Los **datos recorren todo el ciclo**: formulario → servidor → función de guardado → base de datos SQLite.

---

Este proyecto me ha ayudado a entender cómo se combinan varios conceptos clave de la unidad de **Sistemas de gestión empresarial**:

- **Definición de interfaces desde XML**: permite que el diseño del formulario sea flexible y fácil de modificar sin cambiar el código fuente. Esto es muy útil en entornos empresariales donde los formularios cambian con frecuencia (nuevos campos, nuevos procesos).
- **Uso de una base de datos** (en este caso SQLite) para **persistir la información**, igual que hacen los sistemas ERP/CRM reales cuando guardan datos de clientes, jugadores, pedidos o inventario.
- **Separación por capas**:
  - Capa de presentación: formulario HTML generado dinámicamente.
  - Capa lógica: servidor Flask que recibe las peticiones.
  - Capa de datos: SQLite gestionando la tabla `interfaz`.

En un contexto real de gestión empresarial, algo tan sencillo como este formulario podría crecer hasta convertirse en un **módulo de altas de clientes** dentro de un sistema ERP: cada vez que alguien introduce un nuevo cliente, sus datos se guardan en la base de datos y luego pueden consultarse, modificarse o relacionarse con pedidos, facturas, etc.

Además, el hecho de haber trabajado con tecnologías básicas (Python, XML, SQLite, HTML) sin librerías externas me ha permitido **entender mejor lo que hacen los frameworks más grandes por debajo**, y cómo se relaciona todo con los contenidos de la unidad sobre **identificación de sistemas ERP-CRM y su instalación/configuración**.

En resumen, esta actividad me ha servido para:

- Practicar la **generación dinámica de interfaces**.
- Asegurar el **almacenamiento correcto de datos** en una base de datos.
- Relacionar el ejercicio con la realidad de los **sistemas de gestión empresarial**, tanto en empresas tradicionales como en entornos de deportes y videojuegos donde también se gestionan “clientes”, “jugadores” o “equipos” de forma muy similar.
