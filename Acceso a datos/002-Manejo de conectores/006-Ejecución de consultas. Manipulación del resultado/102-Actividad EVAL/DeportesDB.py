import os

class DeportesDB:
    carpeta_bd = "db"

    @staticmethod
    def peticion(peticion):
        if peticion == "SHOW DATABASES;":
            carpetas = os.listdir(DeportesDB.carpeta_bd)
            for carpeta in carpetas:
                print(carpeta)
            return carpetas

DeportesDB.peticion("SHOW DATABASES;")

