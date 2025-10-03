from PIL import Image

img = Image.open("agustin.png")

pixel = img.getpixel((0, 0))

print(pixel) 