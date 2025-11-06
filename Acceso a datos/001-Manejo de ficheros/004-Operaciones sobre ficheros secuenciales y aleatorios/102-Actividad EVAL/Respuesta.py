import os
import json
import hashlib

try:
    os.mkdir("secuenciales")
except:
    pass

clientes = [
    {"nombre": "Cristiano", "apellido": "Ronaldo", "edad": 38, "ciudad": "Madrid", "profesion": "Futbolista"},
    {"nombre": "Lionel", "apellido": "Messi", "edad": 36, "ciudad": "Barcelona", "profesion": "Futbolista"},
    {"nombre": "Mario", "apellido": "Bros", "edad": 35, "ciudad": "Valencia", "profesion": "Fontanero"},
    {"nombre": "Link", "apellido": "Hyrule", "edad": 25, "ciudad": "Sevilla", "profesion": "Héroe"},
    {"nombre": "Sonic", "apellido": "Hedgehog", "edad": 28, "ciudad": "Bilbao", "profesion": "Velocista"},
    {"nombre": "Lara", "apellido": "Croft", "edad": 32, "ciudad": "Málaga", "profesion": "Arqueóloga"},
    {"nombre": "Neymar", "apellido": "Junior", "edad": 31, "ciudad": "Zaragoza", "profesion": "Futbolista"},
    {"nombre": "Serena", "apellido": "Williams", "edad": 42, "ciudad": "Murcia", "profesion": "Tenista"},
    {"nombre": "Rafael", "apellido": "Nadal", "edad": 37, "ciudad": "Palma", "profesion": "Tenista"},
    {"nombre": "Cloud", "apellido": "Strife", "edad": 27, "ciudad": "Alicante", "profesion": "Mercenario"},
    {"nombre": "Kratos", "apellido": "Sparta", "edad": 45, "ciudad": "Córdoba", "profesion": "Guerrero"},
    {"nombre": "Nathan", "apellido": "Drake", "edad": 40, "ciudad": "Valladolid", "profesion": "Cazatesoros"},
    {"nombre": "Ellie", "apellido": "Williams", "edad": 19, "ciudad": "Vigo", "profesion": "Superviviente"},
    {"nombre": "Aloy", "apellido": "Sobeck", "edad": 26, "ciudad": "Gijón", "profesion": "Cazadora"},
    {"nombre": "Arthur", "apellido": "Morgan", "edad": 36, "ciudad": "Granada", "profesion": "Forajido"},
    {"nombre": "Fernando", "apellido": "Alonso", "edad": 42, "ciudad": "Santander", "profesion": "Piloto F1"},
    {"nombre": "Lewis", "apellido": "Hamilton", "edad": 39, "ciudad": "Pamplona", "profesion": "Piloto F1"},
    {"nombre": "Kobe", "apellido": "Bryant", "edad": 41, "ciudad": "Madrid", "profesion": "Baloncestista"},
    {"nombre": "Ash", "apellido": "Ketchum", "edad": 20, "ciudad": "Barcelona", "profesion": "Entrenador Pokémon"},
    {"nombre": "Geralt", "apellido": "Rivia", "edad": 95, "ciudad": "Valencia", "profesion": "Brujo"},
    {"nombre": "Samus", "apellido": "Aran", "edad": 32, "ciudad": "Sevilla", "profesion": "Cazarrecompensas"},
    {"nombre": "Master", "apellido": "Chief", "edad": 41, "ciudad": "Bilbao", "profesion": "Supersoldado"},
    {"nombre": "Zelda", "apellido": "Hyrule", "edad": 23, "ciudad": "Málaga", "profesion": "Princesa"},
    {"nombre": "Tom", "apellido": "Brady", "edad": 46, "ciudad": "Zaragoza", "profesion": "Quarterback"},
    {"nombre": "Megan", "apellido": "Rapinoe", "edad": 38, "ciudad": "Murcia", "profesion": "Futbolista"},
    {"nombre": "Jill", "apellido": "Valentine", "edad": 34, "ciudad": "Palma", "profesion": "Agente"},
    {"nombre": "Leon", "apellido": "Kennedy", "edad": 37, "ciudad": "Alicante", "profesion": "Agente"},
    {"nombre": "Chell", "apellido": "Johnson", "edad": 29, "ciudad": "Córdoba", "profesion": "Científica"},
    {"nombre": "Gordon", "apellido": "Freeman", "edad": 43, "ciudad": "Valladolid", "profesion": "Físico"},
    {"nombre": "Duke", "apellido": "Nukem", "edad": 50, "ciudad": "Vigo", "profesion": "Héroe"},
    {"nombre": "Sam", "apellido": "Porter", "edad": 35, "ciudad": "Gijón", "profesion": "Repartidor"},
    {"nombre": "Marcus", "apellido": "Fenix", "edad": 38, "ciudad": "Granada", "profesion": "Soldado"},
    {"nombre": "Cortana", "apellido": "AI", "edad": 8, "ciudad": "Santander", "profesion": "IA"},
    {"nombre": "Pikachu", "apellido": "Electric", "edad": 5, "ciudad": "Pamplona", "profesion": "Pokémon"},
    {"nombre": "Misty", "apellido": "Waterflower", "edad": 21, "ciudad": "Madrid", "profesion": "Entrenadora"},
    {"nombre": "Brock", "apellido": "Harrison", "edad": 24, "ciudad": "Barcelona", "profesion": "Criador"},
    {"nombre": "Joel", "apellido": "Miller", "edad": 52, "ciudad": "Valencia", "profesion": "Contrabandista"},
    {"nombre": "Tifa", "apellido": "Lockhart", "edad": 25, "ciudad": "Sevilla", "profesion": "Luchadora"},
    {"nombre": "Yuna", "apellido": "Braska", "edad": 22, "ciudad": "Bilbao", "profesion": "Invocadora"},
    {"nombre": "Ryu", "apellido": "Hayabusa", "edad": 30, "ciudad": "Málaga", "profesion": "Ninja"},
    {"nombre": "Cammy", "apellido": "White", "edad": 29, "ciudad": "Zaragoza", "profesion": "Agente"},
    {"nombre": "Dante", "apellido": "Sparda", "edad": 40, "ciudad": "Murcia", "profesion": "Cazademonios"},
    {"nombre": "Bayonetta", "apellido": "Umbra", "edad": 500, "ciudad": "Palma", "profesion": "Bruja"},
    {"nombre": "Solid", "apellido": "Snake", "edad": 42, "ciudad": "Alicante", "profesion": "Espía"},
    {"nombre": "Ezio", "apellido": "Auditore", "edad": 35, "ciudad": "Córdoba", "profesion": "Asesino"},
    {"nombre": "Altair", "apellido": "Ibn-La", "edad": 40, "ciudad": "Valladolid", "profesion": "Asesino"},
    {"nombre": "Raiden", "apellido": "Thunder", "edad": 33, "ciudad": "Vigo", "profesion": "Cyborg"},
    {"nombre": "Pac", "apellido": "Man", "edad": 42, "ciudad": "Gijón", "profesion": "Comecocos"},
    {"nombre": "Fox", "apellido": "McCloud", "edad": 28, "ciudad": "Granada", "profesion": "Piloto"},
    {"nombre": "Kirby", "apellido": "Star", "edad": 30, "ciudad": "Santander", "profesion": "Héroe"}
]

print("Creando 50 archivos secuenciales...")
for i, cliente in enumerate(clientes):
    archivo = open(f"secuenciales/cliente_{i+1:03d}.json", 'w')
    json.dump(cliente, archivo, indent=4)
    archivo.close()
print("✓ 50 archivos creados\n")

for cliente in clientes:
    inicial = cliente["nombre"][0].upper()
    archivo = f"secuenciales/cliente{inicial}.json"

    if os.path.exists(archivo):
        with open(archivo, 'r', encoding='utf-8') as f:
            lista = json.load(f)
    else:
        lista = []

    lista.append(cliente)

    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)

def buscar_cliente(nombre):
    inicial = nombre[0].upper()
    archivo = f"secuenciales/cliente{inicial}.json"

    if not os.path.exists(archivo):
        return None
    
    with open(archivo, encoding='utf-8') as f:
        for cliente in json.load(f):
            if cliente["nombre"].lower() == nombre.lower():
                return cliente
    return None
resultado = buscar_cliente("Cristiano")
print(resultado)
