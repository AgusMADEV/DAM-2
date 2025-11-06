import pickle

# CREO ALGUNOS OBJETOS JUGADOR
class Jugador():
  def __init__(self,nombre,apellidos,emails):
    self.nombre = nombre
    self.apellidos = apellidos
    self.emails = emails
    
jugadores = []
for _ in range(0,10):
  jugadores.append(
    Jugador(
      "Agustín",
      "Morcillo Aguado",
      ["info@agus.es","info@agustin.com"]
      )
  )

print(jugadores)

# SERIALIZO LOS OBJETOS JUGADOR A UN FICHERO BINARIO

archivo = open("jugadores.bin",'wb')
pickle.dump(jugadores,archivo)
archivo.close()

# DESERIALIZO LOS OBJETOS JUGADOR DESDE EL FICHERO BINARIO

archivo = open("jugadores.bin",'rb')
jugadores = pickle.load(archivo)
archivo.close()

print(jugadores)
