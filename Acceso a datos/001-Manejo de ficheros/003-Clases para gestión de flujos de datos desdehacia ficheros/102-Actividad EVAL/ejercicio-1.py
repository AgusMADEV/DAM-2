# Pintamos el píxel (0,0) de color rojo

from PIL import Image

img = Image.open("josevicente.jpeg")

pixels = img.load()
pixels[0, 0] = (255, 0, 0)

img.save("josevicente_roja.png") 
