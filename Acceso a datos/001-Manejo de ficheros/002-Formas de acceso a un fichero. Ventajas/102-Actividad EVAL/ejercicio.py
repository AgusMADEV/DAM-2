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
