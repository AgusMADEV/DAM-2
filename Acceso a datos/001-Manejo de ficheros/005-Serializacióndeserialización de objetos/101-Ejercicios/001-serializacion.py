import json

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

print(personas)
print(type(personas))
cadena = json.dumps(personas)
print(cadena)
print(type(cadena))

archivo = open("basededatos.dat",'w')
archivo.write(cadena)
archivo.close()




    
