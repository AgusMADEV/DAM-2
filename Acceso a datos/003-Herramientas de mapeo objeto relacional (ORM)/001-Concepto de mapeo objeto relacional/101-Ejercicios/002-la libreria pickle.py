class Cliente():
  def __init__(self,nombre,apellidos,emails):
    self.nombre = nombre
    self.apellidos = apellidos
    self.emails = emails
    
clientes = []
for _ in range(0,10):
  clientes.append(
    Cliente(
      "Jose Vicente",
      "Carratala",
      ["info@jocarsa.com","info@josevicentecarratala.com"]
      )
  )

print(clientes)

