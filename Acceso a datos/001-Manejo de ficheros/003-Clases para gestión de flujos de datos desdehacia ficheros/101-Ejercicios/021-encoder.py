from PIL import Image
import math
import argparse

parser = argparse.ArgumentParser(description="Convierte un texto en una imagen RGB")
parser.add_argument("-i", "--entrada", required=True, help="Texto de entrada (string)")
parser.add_argument("-o", "--salida", required=True, help="Archivo de salida (ej: salida.png)")
args = parser.parse_args()

# 1) Texto a bytes UTF-8
data = args.entrada.encode("utf-8")
length = len(data)

# 2) Cabecera de 4 bytes (longitud) en big-endian
header = length.to_bytes(4, byteorder="big")
payload = header + data

# 3) Relleno a múltiplo de 3
pad_len = (3 - (len(payload) % 3)) % 3
payload += b"\x00" * pad_len

# 4) Calcular tamaño de imagen (cuadrada)
num_pixels = len(payload) // 3
side = math.ceil(math.sqrt(num_pixels))

# 5) Crear imagen negra y volcar bytes
img = Image.new("RGB", size=(side, side), color=(0, 0, 0))
pixels = img.load()

for i in range(0, len(payload), 3):
    p = i // 3
    x = p % side
    y = p // side
    r = payload[i]
    g = payload[i + 1]
    b = payload[i + 2]
    pixels[x, y] = (r, g, b)

img.save(args.salida)
