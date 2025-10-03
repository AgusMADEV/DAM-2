from PIL import Image
import time

nucleos = 6

inicio = int(time.time())
img = Image.open("agustin.png")
tamanio = img.size

bloquealtura = int(tamanio[1]/nucleos)

box = (0, 0, tamanio[0], bloquealtura)
recortado = img.crop(box)


pixels = recortado.load()
for x in range(0,tamanio[0]):
  for y in range(0,bloquealtura):
    pixel = recortado.getpixel((x, y))
    pixels[x, y] = (255-pixel[0], 255-pixel[1], 255-pixel[2])
    
recortado.save("agustin3.png")
final = int(time.time())
print((final-inicio),"segundos")