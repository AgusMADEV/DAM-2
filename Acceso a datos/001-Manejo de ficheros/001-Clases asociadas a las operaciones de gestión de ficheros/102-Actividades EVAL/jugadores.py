import json

# Creo un .txt

archivo = open("jugadores.txt","w")
archivo.write("Kylian Mbappe\nCristiano Ronaldo\nAgustin")
archivo.close()

# Ahora vamos a leer archivos

archivo = open("jugadores.txt",'r')
lineas = archivo.readlines()
print("En el torneo ahora mismo están inscritos:\n")
for linea in lineas:
    print(linea)
archivo.close()

# Creación de la lista

info_jugadores = [
    {
        "nombre":"Kylian Mbappe",
        "edad":"26",
        "posicion preferida":"Delantero"
    },
    {
        "nombre":"Cristiano Ronaldo",
        "edad":"40",
        "posicion preferida":"Delantero"
    },
    {
        "nombre":"Agustin",
        "edad":"25",
        "posicion preferida":"Extremo izquierdo"
    },
]

# Creación del .json

archivo = open("info_jugadores.json","w")
json.dump(info_jugadores,archivo,indent=4)
archivo.close()    

# Ahora vamos a leer archivos

archivo = open("info_jugadores.json", "r")
datos = json.load(archivo)
print("Datos completos de los jugadores:\n")
for jugador in datos:
    print("Nombre:", jugador["nombre"])
    print("Edad:", jugador["edad"])
    print("Posición:", jugador["posicion preferida"],"\n")
archivo.close()
