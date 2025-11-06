Un fichero es digamos como una caja donde guardamos datos (texto, imagenes, código, etc) en el disco duro para que no se pierdan al apagar el ordenador. Es útil porque nos permite almacenar la información de forma permanente para poder acceder a ella cuando haga falta.

Para crear en primer lugar el archivo .txt lo que hago es crear una variable para guardar la referencia al archivo que voy a abrir (puede llamarse de cualquier forma), seguido del operador de asignación de Puthon que es el = y luego uso la palabra reservada open junto a ("nombre del archivo.txt","w") para abrir o crear en caso de que no existiera ese archivo, en modo escritura (`"w"`).

'''
archivo = open("jugadores.txt","w")
'''

Para escribir la información en el .txt lo que hago es llamar a la variable (archivo en mi caso) que representa el archivo que hemos abierto y uso el metodo write() que sirve para escribir dentro del archivo.

'''
archivo.write("Kylian Mbappe\nCristiano Ronaldo\nAgustin")
'''

Y para acabar con el .txt, uso el metodo .close() que tiene la función de cerrar el archivo y de guardar todos los datos que hemos escrito con el write().

'''
archivo.close()
'''

En cuanto al archivo .json, lo primero que hago es importar json para poder trabajar con información en este formato, luego, defino una lista [] dentro de una variable, en el que hay varios elementos que son diccionarios{} que en mi caso son tres y cada diccionario tiene 3 claves ("nombre","edad",Posicion preferida")

'''
info_jugadores = [
    {
        "nombre":"Kylian Mbappe",
        "edad":"26",
        "posicion preferida":"Delantero"
    },
    {
        "nombre":"Cristiano Ronaldo",
        "edad":"40",
        "posicion preferida":"Delantero"
    },
    {
        "nombre":"Agustin",
        "edad":"25",
        "posicion preferida":"Extremo izquierdo"
    },
]
'''

Aquí estoy creando una lista de tres jugadores, y de cada uno de los jugadores guardosu nombre, su edad y su posición preferida.
A continuación, para abrir el archivo JSON, uso el mismo método que con el .txt, pero en vez de "nombre del archivo.txt" acabará en ".json".
'''
archivo = open("info_jugadores.json","w")
'''
Y para guardar la lista en formato JSON uso la función de json.dump() que me permite escribir datos de Python en JSON. Dentro del () pondré los datos que quiero guardar, en mi caso la lista de diccionarios, luego el archivo que está abierto donde quiero guardar esa información, y luego con indent= puedo decirle la sangría que quiero que tenga el JSON para que quede bien formateado.

'''
archivo = open("info_jugadores.json","w")
json.dump(info_jugadores,archivo,indent=4)
'''
Y cierro el archivo con 

'''
archivo.close()
'''

Para leer la información del archivo jugadores.txt lo primero que hago es abrir con la misma palabra reservada open, el archivo pero en modo lectura (`"r"`).

'''
archivo = open("jugadores.txt",'r')
'''

Luego, asigno una variable que será el resultado de usar el método readlines(), que es el encargado de leer todo el contenido del archivo.

'''
lineas = archivo.readlines()
'''

Y para mostrarlo en pantalla lo que hago es crear un bucle for en el que creamos una variable temporal, en mi caso linea, para que en cada vuelta del bucle sobre la lista que hemos obtenido con readlines() guarde una de las líneas del archivo. Y mostramos en pantalla con print() el contenido de la variable linea.

'''
for linea in lineas:
    print(linea)
'''
Con el JSON empezamos igual, abrimos el archivo en modo lectura (`"r"`) y creamos una variable que contenga la lista de diccionarios que obtenemos con json.load() del archivo .json. Obtenemos la misma estructura uqe teníamos al principio en la lista creada.

'''
archivo = open("info_jugadores.json", "r")
datos = json.load(archivo)
'''

Para mostrarlo en pantalla recorremos la lista con un bucle for, y accedemos a cada dato usando la clave del diccionario (['nombre'], ['edad'], ['posicion preferida']).  mostramos en pantalla con print() el contenido de la variable temporal, en mi caso, jugador.

'''
print("Datos completos de los jugadores:\n")
for jugador in datos:
    print("Nombre:", jugador["nombre"])
    print("Edad:", jugador["edad"])
    print("Posición:", jugador["posicion preferida"],"\n")
archivo.close()
'''
Por lo tanto, el código del programa completo es este:

'''
import json

# Creo un .txt

archivo = open("jugadores.txt","w")
archivo.write("Kylian Mbappe\nCristiano Ronaldo\nAgustin")
archivo.close()

# Ahora vamos a leer archivos

archivo = open("jugadores.txt",'r')
lineas = archivo.readlines()
print("En el torneo ahora mismo están inscritos:\n")
for linea in lineas:
    print(linea)
archivo.close()

# Creación de la lista

info_jugadores = [
    {
        "nombre":"Kylian Mbappe",
        "edad":"26",
        "posicion preferida":"Delantero"
    },
    {
        "nombre":"Cristiano Ronaldo",
        "edad":"40",
        "posicion preferida":"Delantero"
    },
    {
        "nombre":"Agustin",
        "edad":"25",
        "posicion preferida":"Extremo izquierdo"
    },
]

# Creación del .json

archivo = open("info_jugadores.json","w")
json.dump(info_jugadores,archivo,indent=4)
archivo.close()    

# Ahora vamos a leer archivos

archivo = open("info_jugadores.json", "r")
datos = json.load(archivo)
print("Datos completos de los jugadores:\n")
for jugador in datos:
    print("Nombre:", jugador["nombre"])
    print("Edad:", jugador["edad"])
    print("Posición:", jugador["posicion preferida"],"\n")
archivo.close()

'''

Como hemos podido ver, Python nos permite guardar y leer datos en archivos de texto y JSON, uno nos puede servir para tener un listado más sencillo y con .json podemos guardar ya datos más competo y complejos.
Si lo pienso bien, en un caso real podría aplicarse perfectamente para la organización de un torne deportivo, en el que con el .txt registremos de forma rápida a quien se apunta, y con el .json tengamos la información mas estructurada.

------------------------------------------

Gracias a los métodos de acceso a ficheros que tenemos en Python, podemos organizar nuestro tiempo libre usando archivos. Este ejercicio va de eso, de acceder a ficheros para organizar información sencilla de mi tiempo libre.
Trabajar con archivos de texto me permite mantener datos sin necesidad de una base de datos y puedo escribir, leer y añadir contenido a un archivo.

Para crear el archivo .txt lo que hago es declarar una variable para guardar la referencia al archivo que voy a abrir, seguido de un = y luego usamos la palabra reservada open, entre parentesis ponemos el nombre del archivo y el modo de apertura del mismo, para abrir o crear en caso de que no existiera ese archivo, en modo escritura (`"w"` crea el archivo si no existe y lo vacía si ya existía).
Para la información que quiero escribir, llamamos a la variable y con .write() envío una cadena al buffer y en mi caso, concateno tres partidos.
Por último, cerramos el archivo para que se guarde con close()

```
archivo = open("partidos.txt","w")
archivo.write("Real Madrid CF vs FC Barcelona\nValencia CF vs Real Madrid CF\nReal Madrid CF vs CD Denia")
archivo.close()
```

Para añadir contenido sin tener que reescribirlo de nuevo y sin tener que descartar el contenido que teniamos ya en el archivo, utilizamos el modo de apertura del archivo de apendizar (`"a"` abre para añadir al final; crea el archivo si no existe). El resto es igual que antes, usamos el write() para poner la información que queremos añadir y cerramos para guardar con close()

```
archivo = open("partidos.txt",'a')
archivo.write("\nReal Madrid CF vs Liverpool FC")
archivo.close()
```
Y para poder leer la información que tiene el archivo, lo abrimos en modo lectura (`"r"`). 
Luego, asigno una variable que será el resultado de usar el método readlines(), que es el encargado de leer todo el contenido del archivo. 
Para imprimirla en pantalla utilizamos un bucle for para gaurdar cada línea y con print(linea) la enviamos a la salida.

```
archivo = open("partidos.txt",'r')
lineas = archivo.readlines()
print("Siguientes partidos del Real Madrid CF:\n")
for linea in lineas:
    print(linea)
```

Para mostrar este concepto de una forma consistente, aquí presento un ejercicio completo, en el que podemos organizar nuestro tiempo libre usando archivos con el uso de metodos de acceso en python. 

```
archivo = open("partidos.txt","w")
archivo.write("Real Madrid CF vs FC Barcelona\nValencia CF vs Real Madrid CF\nReal Madrid CF vs CD Denia")
archivo.close()

archivo = open("partidos.txt",'r')
lineas = archivo.readlines()
print("Siguientes partidos del Real Madrid CF:\n")
for linea in lineas:
    print(linea)

archivo = open("partidos.txt",'a')
archivo.write("\nReal Madrid CF vs Liverpool FC")
archivo.close()
```

El manejo de archivos nos permite almacenar y recuperar información de forma sencilla en nuestros programas.

Para usar correctamente archivos debemos comprender los modos de apertura y cierre, ya que son la base para trabajar después con sistemas de almacenamiento más complejos como las bases de datos.

------------------------------------------

Una imagen en Python es como un contenedor donde se guardan datos de color y forma en píxeles, que son los puntos que forman la imagen. Con la biblioteca **PIL (Python Imaging Library)** podemos abrir, crear y modificar imágenes fácilmente, algo que hemos estado viendo en clase dentro del tema de **Acceso a Datos**. En este ejercicio, además, he combinado el trabajo con imágenes con el uso de **argumentos limpios** usando el módulo `argparse`.

Para empezar, importo las librerías necesarias: `PIL.Image` para manejar las imágenes, `math` para cálculos del tamaño, y `argparse` para leer los parámetros del programa.

```python
from PIL import Image
import math
import argparse
```

Lo primero que hago es abrir una imagen con `Image.open()` y modificar un píxel concreto usando el método `load()`, que permite acceder a los datos de color. En este caso, cambio el píxel (0,0) por el color rojo y guardo la nueva imagen con `save()`.

```python
img = Image.open("josevicente.jpeg")
pixels = img.load()
pixels[0, 0] = (255, 0, 0)
img.save("josevicente_roja.png")
```

Luego, defino los argumentos que podrá recibir el programa con `argparse`. Estos argumentos permiten elegir si quiero codificar o decodificar, y qué archivos usar:

```python
parser = argparse.ArgumentParser(description="Convierte texto en imagen o imagen en texto.")
parser.add_argument("-m","--modo", choices=["encode", "decode"], required=True, help="Modo de operación: encode o decode")
parser.add_argument("-i", "--entrada", required=True, help="Archivo de entrada o texto a codificar")
parser.add_argument("-o", "--salida", help="Archivo de salida (solo necesario para encode)")
args = parser.parse_args()
```

En el **modo encode**, convierto un texto en una imagen. Primero, transformo el texto en bytes y guardo su longitud para saber cuánto ocupa. Luego, los datos se reparten entre los valores RGB de los píxeles:

```python
if args.modo == "encode":
    if not args.salida:
        raise ValueError("Debes indicar -o para guardar la imagen de salida.")

    data = args.entrada.encode("utf-8")
    length = len(data)
    header = length.to_bytes(4, byteorder="big")
    payload = header + data
```

Después calculo el tamaño de la imagen según los datos que haya que guardar, creo una nueva imagen en negro y empiezo a escribir los valores RGB de cada píxel con un bucle.

```python
    num_pixels = len(payload) // 3
    side = math.ceil(math.sqrt(num_pixels))

    img = Image.new("RGB", size=(side, side), color=(0, 0, 0))
    pixels = img.load()

    for i in range(0, len(payload), 3):
        p = i // 3
        x = p % side
        y = p // side
        r, g, b = payload[i], payload[i + 1], payload[i + 2]
        pixels[x, y] = (r, g, b)

    img.save(args.salida)
    print(f"✅ Texto codificado y guardado en {args.salida}")
```

En el **modo decode**, el proceso es al revés: abro la imagen, leo cada píxel y reconstruyo el texto original.

```python
elif args.modo == "decode":
    img = Image.open(args.entrada).convert("RGB")
    pixels = img.load()
    w, h = img.size

    byte_array = bytearray()
    for y in range(h):
        for x in range(w):
            r, g, b = pixels[x, y]
            byte_array.extend((r, g, b))

    length = int.from_bytes(byte_array[0:4], byteorder="big")
    data = bytes(byte_array[4:4 + length])

    texto = data.decode("utf-8")
    print("🧩 Texto decodificado:")
    print(texto)
```

De esta forma, el programa puede convertir texto en imagen y luego recuperarlo sin errores.

Para probarlo, se puede ejecutar desde la terminal así:

```bash
python encode_decode.py -m encode -i "Hola mundo" -o salida.png
python encode_decode.py -m decode -i salida.png
```

Al hacerlo, el texto “Hola mundo” se guarda dentro de la imagen `salida.png`, y al decodificarla vuelve a aparecer correctamente en pantalla.

En conclusión, este ejercicio me ha servido para entender cómo **trabajar con píxeles y flujos binarios en imágenes** usando PIL, y también cómo hacer que un script de Python sea **más profesional y flexible** usando `argparse` para los argumentos limpios.  
Esta práctica está directamente relacionada con el tema de **acceso a datos**, ya que implica leer, modificar y guardar información desde un archivo externo (en este caso una imagen).  
En proyectos futuros, este tipo de técnica podría aplicarse para cosas como **ocultar mensajes en imágenes (esteganografía)**, **almacenar datos visualmente** o incluso **procesar archivos multimedia de forma automatizada**.

------------------------------------------

En este ejercicio creo **50 archivos JSON** (uno por cliente) dentro de la carpeta `secuenciales/` y construyo una **hash table simple** basada en la **primera letra del nombre** para acceder rápidamente a los datos.  
La idea es practicar dos enfoques de almacenamiento que se ven en clase:
- **Archivo secuencial**: guardo registros en ficheros numerados (`cliente_001.json`, `cliente_002.json`, …). Útil para persistir datos discretos y comprobar estructura.
- **Hash table por inicial**: agrupo clientes por inicial en `clienteA.json`, `clienteB.json`, … Esto reduce el espacio de búsqueda a un subconjunto, emulando el acceso **O(1) esperado** de una tabla hash mediante **partición por clave**.

Además, integro uno de mis hobbies (los **deportes**): antes de codificar hago un **calentamiento breve** (3–4 minutos de movilidad de hombros, cadera y tobillos + 10 sentadillas suaves). Esto me ayuda a empezar la sesión más concentrado y con menos tensión postural.

---

### Estructura de la solución
- **Creación de la carpeta y ficheros secuenciales**
  ```py
  try:
      os.mkdir("secuenciales")
  except:
      pass

  print("Creando 50 archivos secuenciales...")
  for i, cliente in enumerate(clientes):
      with open(f"secuenciales/cliente_{i+1:03d}.json", "w", encoding="utf-8") as f:
          json.dump(cliente, f, indent=4, ensure_ascii=False)
  print("✓ 50 archivos creados\n")
  ```
  *Por qué*: cada registro queda en su propio archivo, con nombre **correlativo** y contenido **JSON identado** para legibilidad.

- **Construcción de la hash table basada en la inicial**
  ```py
  for cliente in clientes:
      inicial = cliente["nombre"][0].upper()
      archivo = f"secuenciales/cliente{inicial}.json"

      if os.path.exists(archivo):
          with open(archivo, "r", encoding="utf-8") as f:
              lista = json.load(f)
      else:
          lista = []

      lista.append(cliente)
      with open(archivo, "w", encoding="utf-8") as f:
          json.dump(lista, f, indent=4, ensure_ascii=False)
  ```
  *Qué hace*: genera un **bucket** por inicial (A..Z). Esto actúa como una **función hash h(nombre)=nombre[0]** y almacena colisiones (múltiples clientes con la misma inicial) en una **lista** dentro del mismo archivo.

- **Búsqueda por nombre a través de la hash table**
  ```py
  def buscar_cliente(nombre):
      inicial = nombre[0].upper()
      archivo = f"secuenciales/cliente{inicial}.json"

      if not os.path.exists(archivo):
          return None

      with open(archivo, encoding="utf-8") as f:
          for cliente in json.load(f):
              if cliente["nombre"].lower() == nombre.lower():
                  return cliente
      return None

  resultado = buscar_cliente("Cristiano")
  print(resultado)
  ```
  *Cómo funciona*: abre solo el **bucket** correspondiente a la inicial y **filtra** por coincidencia exacta de nombre (case-insensitive). Si no existe el bucket, devuelve `None`.

> **Restricciones cumplidas**: no uso librerías externas; solo `os` y `json` de la biblioteca estándar, manejo de ficheros con `with`, y estructuras vistas (listas, diccionarios, bucles, funciones).

---

**Codificación**:
   - Ejecuto el script para **crear los 50 ficheros**: `secuenciales/cliente_001.json` … `secuenciales/cliente_050.json`.
   - En el mismo proceso se generan los **buckets**: por ejemplo `secuenciales/clienteC.json`, `secuenciales/clienteL.json`, etc.
   - Verifico la búsqueda:
     ```py
    resultado = buscar_cliente("Cristiano")
    print(resultado)
     #Salida esperada (ejemplo):
     #{'nombre': 'Cristiano', 'apellido': 'Ronaldo', 'edad': 38, 'ciudad': 'Madrid', 'profesion': 'Futbolista'}
     ```

---

Este ejercicio me ha ayudado a entender cómo guardar y buscar datos de forma ordenada usando archivos y una tabla hash sencilla. Es una base práctica para sistemas de almacenamiento más grandes.
El aprendizaje es aplicable a situaciones reales de **gestión de datos** en proyectos de desarrollo: creación de **herramientas de import/export**, **mocks persistentes** para tests, prototipos de **indexación** por claves y preparación para migrar a soluciones más avanzadas (B‑Trees, bases de datos clave‑valor o índices secundarios). Integrar un **hábito de calentamiento** antes de programar me ha ayudado a mantener la concentración y reducir fatiga, conectando el ejercicio técnico con una rutina saludable.

------------------------------------------

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

------------------------------------------

En este ejercicio partimos de una situación cercana: alguien que disfruta del deporte, los videojuegos y los viajes quiere organizar sus actividades diarias.  
Para eso, aprendemos a **trabajar con archivos CSV en Python**, un formato muy común para guardar información estructurada.  
La idea es ver cómo escribir y leer datos desde un archivo de texto, entendiendo el flujo completo de guardar una actividad y recuperarla más tarde.

---

El programa implementa una clase llamada **`Actividades`** que permite registrar y consultar actividades guardadas en un archivo CSV.

### Código principal:
```python
class Actividades:
    def __init__(self, archivo="actividades.csv"):
        self.archivo = archivo

    def escribir_actividad(self, tupla):
        with open(self.archivo, 'a') as f:
            cadena = ",".join(tupla) + "\n"
            f.write(cadena)

    def leer_actividad(self):
        with open(self.archivo, 'r') as f:
            linea = f.readline().strip()
            if linea:
                return tuple(linea.split(","))
            else:
                return None
            
actividades = Actividades()
tupla_actividad = ("Jugar un partido de Baloncesto", "2023-10-05", "Deporte")
actividades.escribir_actividad(tupla_actividad)

actividad_leida = actividades.leer_actividad()
if actividad_leida:
    print(f"Actividad leída: {actividad_leida}")
else:
    print("No hay actividades registradas.")
```

1. **Inicialización:** el constructor define el nombre del archivo (`actividades.csv`).  
2. **Escritura:** el método `escribir_actividad()` toma una tupla, la convierte en texto separado por comas y la guarda en el archivo.  
3. **Lectura:** el método `leer_actividad()` abre el archivo, lee la primera línea y la devuelve como una tupla con `split(',')`.  
4. **Prueba final:** se escribe una actividad y luego se lee para comprobar que los datos se guardaron correctamente.

---

### Contenido guardado en `actividades.csv`:
```
Jugar un partido de Baloncesto,2023-10-05,Deporte
```

### Resultado en la consola:
```
Actividad leída: ('Jugar un partido de Baloncesto', '2023-10-05', 'Deporte')
```

Esto muestra claramente el proceso de **guardar** información en formato CSV y luego **leerla** como una estructura Python.  
De esta forma, el código permite manejar pequeñas bases de datos de actividades sin depender de herramientas externas.

---

Has aprendido cómo manejar **archivos CSV** en Python, una habilidad clave dentro del tema de **acceso a datos**.  
Este tipo de archivos es ideal para guardar listas de tareas o actividades de forma simple y reutilizable.  
Con este mismo enfoque podrías crear una app más completa para planificar tus entrenamientos, registrar tus partidas o programar tus viajes.  
La práctica con ficheros te acerca un paso más a la gestión real de datos en proyectos de software.