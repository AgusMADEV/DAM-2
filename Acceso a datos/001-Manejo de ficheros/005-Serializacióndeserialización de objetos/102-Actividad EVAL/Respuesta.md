En este ejercicio práctico, trabajo con un archivo que contiene información en formato **JSON** para reforzar lo aprendido sobre **acceso a datos**.  
El objetivo es entender cómo **leer** un fichero con datos serializados (guardados como texto JSON) y **convertirlo** de nuevo en un objeto Python con `json.loads()`.  
Así puedo ver cómo un programa transforma información guardada en texto (por ejemplo, una base de datos o una API) en estructuras que el lenguaje puede manipular.

---

El código completo es el siguiente:

```python
import json

# Abrimos el archivo con datos en formato JSON
archivo = open("basededatos.dat", 'r')

# Leemos la primera línea
linea = archivo.readlines()[0]
print(linea)
print(type(linea))
archivo.close()

# Deserializamos el contenido (de texto JSON a objeto Python)
devuelta = json.loads(linea)
print(devuelta)
print(type(devuelta))
```

1. **Apertura del archivo**  
   Se abre el archivo `basededatos.dat` en modo lectura (`'r'`).

2. **Lectura de línea**  
   `readlines()[0]` toma la primera línea del archivo, que contiene el JSON.

3. **Visualización del contenido original**  
   El programa imprime la línea leída (en formato texto) y su tipo (`str`).

4. **Deserialización con `json.loads()`**  
   Convierte la cadena JSON en un **diccionario Python**, lo que permite acceder a los datos con sus claves.

5. **Comprobación final**  
   Se imprime el objeto resultante y su tipo (`dict`) para confirmar la transformación.

---

Supongamos que el archivo `basededatos.dat` contiene la siguiente línea:

```json
{"nombre": "Mario", "edad": 30, "ciudad": "Valencia"}
```

```
{"nombre": "Mario", "edad": 30, "ciudad": "Valencia"}
<class 'str'>
{'nombre': 'Mario', 'edad': 30, 'ciudad': 'Valencia'}
<class 'dict'>
```

🔹 **Antes de la deserialización:**  
El contenido es texto (tipo `str`).  

🔹 **Después de la deserialización:**  
El contenido se convierte en un diccionario Python (`dict`), lo que permite hacer cosas como:

```python
print(devuelta["nombre"])
# Resultado: Mario
```

✅ Esto demuestra de forma práctica cómo un texto JSON puede transformarse en un objeto Python para trabajar fácilmente con los datos.

---

Con este ejercicio comprendí cómo los datos pueden viajar como texto (JSON) y luego convertirse en estructuras manipulables dentro del programa.  
Es una base importante del **acceso a datos**, ya que el mismo proceso se utiliza en APIs, ficheros o bases de datos modernas.  
Entender cómo **serializar y deserializar** información me permite conectar programas con fuentes de datos reales de manera segura y eficiente.
