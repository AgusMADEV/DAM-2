# Pintamos el píxel (0,0) de color rojo
from PIL import Image
import math
import argparse

img = Image.open("josevicente.jpeg")

pixels = img.load()
pixels[0, 0] = (255, 0, 0)

img.save("josevicente_roja.png") 

parser = argparse.ArgumentParser(description="Convierte texto en imagen o imagen en texto.")
parser.add_argument("-m","--modo", choices=["encode", "decode"], required=True, help="Modo de operación: encode o decode")
parser.add_argument("-i", "--entrada", required=True, help="Archivo de entrada o texto a codificar")
parser.add_argument("-o", "--salida", help="Archivo de salida (solo necesario para encode)")
args = parser.parse_args()

# ------------------ ENCODER ------------------
if args.modo == "encode":
    if not args.salida:
        raise ValueError("Debes indicar -o para guardar la imagen de salida.")

    data = args.entrada.encode("utf-8")
    length = len(data)
    header = length.to_bytes(4, byteorder="big")
    payload = header + data

    pad_len = (3 - (len(payload) % 3)) % 3
    payload += b"\x00" * pad_len

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

# ------------------ DECODER ------------------
elif args.modo == "decode":
    img = Image.open(args.entrada).convert("RGB")
    pixels = img.load()
    w, h = img.size

    byte_array = bytearray()
    for y in range(h):
        for x in range(w):
            r, g, b = pixels[x, y]
            byte_array.extend((r, g, b))

    if len(byte_array) < 4:
        raise ValueError("Imagen demasiado pequeña: no contiene cabecera de longitud.")

    length = int.from_bytes(byte_array[0:4], byteorder="big")
    data = bytes(byte_array[4:4 + length])

    texto = data.decode("utf-8")
    print("🧩 Texto decodificado:")
    print(texto)

