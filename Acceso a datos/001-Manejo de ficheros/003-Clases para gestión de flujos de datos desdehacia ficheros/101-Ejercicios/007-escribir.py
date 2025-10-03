from PIL import Image

img = Image.open("agustin.png")

pixels = img.load()
pixels[0, 0] = (0, 0, 0)

img.save("agustin2.jpeg")       # .jpeg pierde información de conversión