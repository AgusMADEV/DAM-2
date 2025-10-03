Gracias a los métodos de acceso a ficheros que tenemos en Python, podemos organizar nuestro tiempo libre usando archivos. Este ejercicio va de eso, de acceder a ficheros para organizar información sencilla de mi tiempo libre.
Trabajar con archivos de texto me permite mantener datos sin necesidad de una base de datos y puedo escribir, leer y añadir contenido a un archivo.

Para crear el archivo .txt lo que hago es declarar una variable para guardar la referencia al archivo que voy a abrir, seguido de un = y luego usamos la palabra reservada open, entre parentesis ponemos el nombre del archivo y el modo de apertura del mismo, para abrir o crear en caso de que no existiera ese archivo, en modo escritura (`"w"` crea el archivo si no existe y lo vacía si ya existía).
Para la información que quiero escribir, llamamos a la variable y con .write() envío una cadena al buffer y en mi caso, concateno tres partidos.
Por último, cerramos el archivo para que se guarde con close()

```
archivo = open("partidos.txt","w")
archivo.write("Real Madrid CF vs FC Barcelona\nValencia CF vs Real Madrid CF\nReal Madrid CF vs CD Denia")
archivo.close()
```

Para añadir contenido sin tener que reescribirlo de nuevo y sin tener que descartar el contenido que teniamos ya en el archivo, utilizamos el modo de apertura del archivo de apendizar (`"a"` abre para añadir al final; crea el archivo si no existe). El resto es igual que antes, usamos el write() para poner la información que queremos añadir y cerramos para guardar con close()

```
archivo = open("partidos.txt",'a')
archivo.write("\nReal Madrid CF vs Liverpool FC")
archivo.close()
```
Y para poder leer la información que tiene el archivo, lo abrimos en modo lectura (`"r"`). 
Luego, asigno una variable que será el resultado de usar el método readlines(), que es el encargado de leer todo el contenido del archivo. 
Para imprimirla en pantalla utilizamos un bucle for para gaurdar cada línea y con print(linea) la enviamos a la salida.

```
archivo = open("partidos.txt",'r')
lineas = archivo.readlines()
print("Siguientes partidos del Real Madrid CF:\n")
for linea in lineas:
    print(linea)
```

Para mostrar este concepto de una forma consistente, aquí presento un ejercicio completo, en el que podemos organizar nuestro tiempo libre usando archivos con el uso de metodos de acceso en python. 

```
archivo = open("partidos.txt","w")
archivo.write("Real Madrid CF vs FC Barcelona\nValencia CF vs Real Madrid CF\nReal Madrid CF vs CD Denia")
archivo.close()

archivo = open("partidos.txt",'r')
lineas = archivo.readlines()
print("Siguientes partidos del Real Madrid CF:\n")
for linea in lineas:
    print(linea)

archivo = open("partidos.txt",'a')
archivo.write("\nReal Madrid CF vs Liverpool FC")
archivo.close()
```

El manejo de archivos nos permite almacenar y recuperar información de forma sencilla en nuestros programas.

Para usar correctamente archivos debemos comprender los modos de apertura y cierre, ya que son la base para trabajar después con sistemas de almacenamiento más complejos como las bases de datos.