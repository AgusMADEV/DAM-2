import os

carpeta = "/home/josevicente/Escritorio/muchosvideos"

archivos = os.listdir(carpeta)

for archivo in archivos:
  print(archivo)
