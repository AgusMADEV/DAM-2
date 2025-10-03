from PIL import Image

img = Image.new("RGB", size=(200, 200), color="white")

with open("texto.txt", "r", encoding="utf-8") as texto:
    print(texto.readlines())

img.save("mensaje.png")