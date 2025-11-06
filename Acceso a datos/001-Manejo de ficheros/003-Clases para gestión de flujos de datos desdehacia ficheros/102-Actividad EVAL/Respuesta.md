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
