import os
import zipfile

carpeta = "/home/josevicente/Escritorio/muchosvideos"

archivos = os.listdir(carpeta)

for archivo in archivos:
  archivozip = zipfile.ZipFile(os.path.join(carpeta,archivo+".zip"), 'w')
  archivozip.write(os.path.join(carpeta,archivo))
  
