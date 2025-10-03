Un fichero es digamos como una caja donde guardamos datos (texto, imagenes, código, etc) en el disco duro para que no se pierdan al apagar el ordenador. Es útil porque nos permite almacenar la información de forma permanente para poder acceder a ella cuando haga falta.

Para crear en primer lugar el archivo .txt lo que hago es crear una variable para guardar la referencia al archivo que voy a abrir (puede llamarse de cualquier forma), seguido del operador de asignación de Puthon que es el = y luego uso la palabra reservada open junto a ("nombre del archivo.txt","w") para abrir o crear en caso de que no existiera ese archivo, en modo escritura (`"w"`).

'''
archivo = open("jugadores.txt","w")
'''

Para escribir la información en el .txt lo que hago es llamar a la variable (archivo en mi caso) que representa el archivo que hemos abierto y uso el metodo write() que sirve para escribir dentro del archivo.

'''
archivo.write("Kylian Mbappe\nCristiano Ronaldo\nAgustin")
'''

Y para acabar con el .txt, uso el metodo .close() que tiene la función de cerrar el archivo y de guardar todos los datos que hemos escrito con el write().

'''
archivo.close()
'''

En cuanto al archivo .json, lo primero que hago es importar json para poder trabajar con información en este formato, luego, defino una lista [] dentro de una variable, en el que hay varios elementos que son diccionarios{} que en mi caso son tres y cada diccionario tiene 3 claves ("nombre","edad",Posicion preferida")

'''
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
'''

Aquí estoy creando una lista de tres jugadores, y de cada uno de los jugadores guardosu nombre, su edad y su posición preferida.
A continuación, para abrir el archivo JSON, uso el mismo método que con el .txt, pero en vez de "nombre del archivo.txt" acabará en ".json".
'''
archivo = open("info_jugadores.json","w")
'''
Y para guardar la lista en formato JSON uso la función de json.dump() que me permite escribir datos de Python en JSON. Dentro del () pondré los datos que quiero guardar, en mi caso la lista de diccionarios, luego el archivo que está abierto donde quiero guardar esa información, y luego con indent= puedo decirle la sangría que quiero que tenga el JSON para que quede bien formateado.

'''
archivo = open("info_jugadores.json","w")
json.dump(info_jugadores,archivo,indent=4)
'''
Y cierro el archivo con 

'''
archivo.close()
'''

Para leer la información del archivo jugadores.txt lo primero que hago es abrir con la misma palabra reservada open, el archivo pero en modo lectura (`"r"`).

'''
archivo = open("jugadores.txt",'r')
'''

Luego, asigno una variable que será el resultado de usar el método readlines(), que es el encargado de leer todo el contenido del archivo.

'''
lineas = archivo.readlines()
'''

Y para mostrarlo en pantalla lo que hago es crear un bucle for en el que creamos una variable temporal, en mi caso linea, para que en cada vuelta del bucle sobre la lista que hemos obtenido con readlines() guarde una de las líneas del archivo. Y mostramos en pantalla con print() el contenido de la variable linea.

'''
for linea in lineas:
    print(linea)
'''
Con el JSON empezamos igual, abrimos el archivo en modo lectura (`"r"`) y creamos una variable que contenga la lista de diccionarios que obtenemos con json.load() del archivo .json. Obtenemos la misma estructura uqe teníamos al principio en la lista creada.

'''
archivo = open("info_jugadores.json", "r")
datos = json.load(archivo)
'''

Para mostrarlo en pantalla recorremos la lista con un bucle for, y accedemos a cada dato usando la clave del diccionario (['nombre'], ['edad'], ['posicion preferida']).  mostramos en pantalla con print() el contenido de la variable temporal, en mi caso, jugador.

'''
print("Datos completos de los jugadores:\n")
for jugador in datos:
    print("Nombre:", jugador["nombre"])
    print("Edad:", jugador["edad"])
    print("Posición:", jugador["posicion preferida"],"\n")
archivo.close()
'''
Por lo tanto, el código del programa completo es este:

'''
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

'''

Como hemos podido ver, Python nos permite guardar y leer datos en archivos de texto y JSON, uno nos puede servir para tener un listado más sencillo y con .json podemos guardar ya datos más competo y complejos.
Si lo pienso bien, en un caso real podría aplicarse perfectamente para la organización de un torne deportivo, en el que con el .txt registremos de forma rápida a quien se apunta, y con el .json tengamos la información mas estructurada.