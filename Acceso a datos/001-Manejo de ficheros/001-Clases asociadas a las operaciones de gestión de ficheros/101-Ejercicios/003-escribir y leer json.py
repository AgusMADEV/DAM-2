import json

agenda = [
        {
            "nombre":"Agustín",
            "telefono":["543534","543534","543534"],
            "email":"info@agusmadev.com",
            },
        {
            "nombre":"Elena",
            "telefono":["543534","543534","543534"],
            "email":"info@evoluciona.com",
            },
    ]

archivo = open("agenda.json",'w')
json.dump(agenda,archivo,indent=4)
archivo.close()

archivo = open("agenda.json", "r")
datos = json.load(archivo)   # Cargar el contenido del JSON en una variable Python
print("Datos completos de los clientes:\n")
for dato in datos:
    print(f"Nombre: {dato['nombre']}, Telefono: {dato['telefono']}, email: {dato['email']}")

archivo.close()
