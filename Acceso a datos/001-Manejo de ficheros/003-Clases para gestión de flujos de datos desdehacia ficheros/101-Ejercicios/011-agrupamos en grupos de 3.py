from PIL import Image

img = Image.new("RGB", size=(200, 200), color="white")

# Abre como texto pero con latin-1 para que todos los bytes 0-255 sean válidos
texto = open("texto.txt", 'r', encoding='latin-1')

lineas = texto.readlines()
letras = []
for linea in lineas:
    for letra in linea:
        # convierte cada carácter a su valor 0-255
        letras.append(ord(letra))

contador = 0
pix = img.load()
W, H = img.size

for i in range(0, len(letras), 3):
    # Evita IndexError si no hay múltiplo de 3
    r = letras[i]
    g = letras[i+1] if i+1 < len(letras) else 0
    b = letras[i+2] if i+2 < len(letras) else 0

    # Mismos prints que tenías
    print("r:", r)
    print("g:", g)
    print("b:", b)
    print("siguiente pixel")

    # Pinta el pixel correspondiente con el contador
    x = contador % W
    y = contador // W
    if y >= H:
        break
    pix[x, y] = (r, g, b)
    contador += 1

img.save("mensaje.png")
