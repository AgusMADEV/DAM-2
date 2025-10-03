from PIL import Image

img = Image.new("RGB", size=(200, 200), color="white")
pixels = img.load()

# <- solo añado encoding para que no falle en Windows
texto = open("texto.txt", 'r', encoding="latin-1", errors="strict")
lineas = texto.readlines()
# opcional: texto.close() (no uso with para mantener tu estructura)
letras = []
for linea in lineas:
  for letra in linea:
    letras.append(letra)

contador = 0
ancho, alto = img.size

for i in range(0, len(letras), 3):
  try:
    r = ord(letras[i])
    g = ord(letras[i+1]) if i+1 < len(letras) else 0
    b = ord(letras[i+2]) if i+2 < len(letras) else 0

    print("r:", letras[i], r)
    print("g:", letras[i+1] if i+1 < len(letras) else "\\x00", g)
    print("b:", letras[i+2] if i+2 < len(letras) else "\\x00", b)

    # un pixel por cada 3 letras (mantengo tu idea, solo corrigo //)
    idx_pixel = i // 3
    # coloco en (x,y) recorriendo por filas
    x = idx_pixel % ancho
    y = idx_pixel // ancho
    if y >= alto:
      break  # imagen llena

    pixels[x, y] = (r & 255, g & 255, b & 255)  # por seguridad, 0-255

    print("siguiente pixel")
  except Exception as e:
    # mantengo tu try/except, pero si quieres ver el error:
    # print("Error en i=", i, e)
    pass

img.save("mensaje.png")
