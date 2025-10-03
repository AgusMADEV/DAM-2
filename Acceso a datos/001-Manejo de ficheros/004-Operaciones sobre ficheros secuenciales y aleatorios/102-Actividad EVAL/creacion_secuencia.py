import os
import hashlib
import json

try:
    os.mkdir("secuenciales")
except:
    pass

for i in range(0,50):
    archivo = open("secuenciales/0"+str(i)+"-cliente.json",'w')
    archivo.write("texto del cliente")
    archivo.close()
