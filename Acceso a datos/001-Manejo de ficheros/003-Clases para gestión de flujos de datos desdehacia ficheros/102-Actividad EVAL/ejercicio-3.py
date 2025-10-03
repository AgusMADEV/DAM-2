from PIL import Image
import argparse

parser = argparse.ArgumentParser(description="Decodifica una imagen RGB a texto")
parser.add_argument("-i", "--entrada", required=True, help="Archivo de imagen de entrada (png/jpg)")
args = parser.parse_args()

# 1) Leer todos los bytes (R,G,B) en el mismo orden de escritura
img = Image.open(args.entrada).convert("RGB")
pixels = img.load()
w, h = img.size

byte_array = bytearray()
for y in range(h):
    for x in range(w):
        r, g, b = pixels[x, y]
        byte_array.extend((r, g, b))

# 2) Extraer longitud (4 bytes big-endian) y recuperar exactamente esos bytes
if len(byte_array) < 4:
    raise ValueError("Imagen demasiado pequeña: no contiene cabecera de longitud.")

length = int.from_bytes(byte_array[0:4], byteorder="big")
data = bytes(byte_array[4:4 + length])

# 3) Decodificar UTF-8 y mostrar
texto = data.decode("utf-8")
print(texto)
