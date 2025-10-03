from PIL import Image

img = Image.open("agustin.png")
tamanio = img.size
print(tamanio)
pixel = img.getpixel((0, 0))

print(pixel) 