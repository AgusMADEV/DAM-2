from PIL import Image

img = Image.new("RGB", size=(200, 200), color="white")

texto = open("texto.txt",'r')
lineas = texto.readlines()
letras = []
for linea in lineas:
  for letra in linea:
    letras.append(letra)

contador = 0    
for letra in letras:
  print(letra)
  contador += 1
  if contador > 3:
    contador = 0
    print("Vamos con el siguiente pixel")

img.save("mensaje.png")