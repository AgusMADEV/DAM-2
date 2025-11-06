tupla = ("Jose Vicente","Carratala","info@jocarsa.com")

archivo = open("clientes.csv",'a')
cadena = ""
for campo in tupla:
  cadena += campo+","
archivo.write(cadena)
archivo.close()
