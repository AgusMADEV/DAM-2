import os
import hashlib
import json

try:
    os.mkdir("hash")
except:
    pass

# Lista de personas ficticias
personas = [
    {
        "nombre": "Carlos",
        "apellido": "Martínez",
        "edad": 28,
        "ciudad": "Madrid",
        "profesion": "Ingeniero"
    },
    {
        "nombre": "Lucía",
        "apellido": "Fernández",
        "edad": 34,
        "ciudad": "Barcelona",
        "profesion": "Doctora"
    },
    {
        "nombre": "Andrés",
        "apellido": "García",
        "edad": 22,
        "ciudad": "Valencia",
        "profesion": "Estudiante"
    },
    {
        "nombre": "María",
        "apellido": "López",
        "edad": 41,
        "ciudad": "Sevilla",
        "profesion": "Arquitecta"
    },
    {
        "nombre": "Javier",
        "apellido": "Sánchez",
        "edad": 30,
        "ciudad": "Bilbao",
        "profesion": "Profesor"
    }
]

for persona in personas:
    cadena = persona['nombre']+persona['apellido']+str(persona['edad'])
    picadillo = hashlib.md5(cadena.encode()).hexdigest()
    print(picadillo)
    archivo = open("hash/"+picadillo+".json",'w')
    json.dump(persona,archivo,indent=4)
    archivo.close()

# Ahora busco entre esos hashes

cadena = "Lucía"+"Fernández"+"34"
picadillo = hashlib.md5(cadena.encode()).hexdigest()
archivo = open("hash/"+picadillo+".json",'r')
contenido = json.load(archivo)
print(contenido)

    
