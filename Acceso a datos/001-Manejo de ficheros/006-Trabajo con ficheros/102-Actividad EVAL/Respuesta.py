class Actividades:
    def __init__(self, archivo="actividades.csv"):
        self.archivo = archivo

    def escribir_actividad(self, tupla):
        with open(self.archivo, 'a') as f:
            cadena = ",".join(tupla) + "\n"
            f.write(cadena)

    def leer_actividad(self):
        with open(self.archivo, 'r') as f:
            linea = f.readline().strip()
            if linea:
                return tuple(linea.split(","))
            else:
                return None
            
actividades = Actividades()
tupla_actividad = ("Jugar un partido de Baloncesto", "2023-10-05", "Deporte")
actividades.escribir_actividad(tupla_actividad)

actividad_leida = actividades.leer_actividad()
if actividad_leida:
    print(f"Actividad leída: {actividad_leida}")
else:
    print("No hay actividades registradas.")