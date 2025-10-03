import csv

# Primero escribo datos

datos = [
    ['nombre','apellidos','telefono'],
    ['Agustín','Morcillo','123456789'],
    ['Elena','Botezatu','987654321'],
    ['Lilo','Morcillo','123654789'],
    ['Dipsy','Botezatu','987456321'],
]

archivo = open("datos.csv",'w')
escritor = csv.writer(archivo)
escritor.writerows(datos)
archivo.close()

# Ahora leo los datos

archivo = open("datos.csv",'r')
lector = csv.reader(archivo)
for linea in lector:
    print(linea)
