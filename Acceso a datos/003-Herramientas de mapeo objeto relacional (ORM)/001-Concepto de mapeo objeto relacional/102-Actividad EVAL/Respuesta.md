Como aficionado al **deporte** y a pasar tiempo con mi gente, este ejercicio me ayuda a ver cómo podría guardar información de mis compañeros de equipo o amigos de forma sencilla.  
Con **Python y `pickle`**, puedo **guardar y recuperar objetos completos** (como jugadores) en un archivo binario, sin tener que escribir ni leer cada dato manualmente.  
Así aprendo a mantener la información persistente, incluso cuando el programa se cierra.

---

El ejercicio consiste en **crear objetos `Jugador`**, guardarlos en un fichero binario con `pickle.dump()` y volver a cargarlos con `pickle.load()`.

### Código base del ejercicio:
```python
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
```

### Explicación técnica:
1. **Definición de la clase `Jugador`:** contiene nombre, apellidos y una lista de emails.  
2. **Creación de objetos:** se generan 10 instancias con los mismos datos.  
3. **Serialización:** con `pickle.dump(jugadores, archivo)` se guardan todos los objetos en el fichero binario `jugadores.bin`.  
4. **Deserialización:** con `pickle.load(archivo)` se recuperan exactamente los mismos objetos desde el archivo.  
5. **Verificación:** se imprime la lista antes y después de la carga para comprobar que los objetos se mantienen intactos.

### Ejemplo de salida en consola:
```
[<__main__.Jugador object at 0x0000021F...>, <__main__.Jugador object at 0x0000021F...>, ...]
[<__main__.Jugador object at 0x0000021F...>, <__main__.Jugador object at 0x0000021F...>, ...]
```

---

Este proceso es muy útil en situaciones reales donde se necesita **guardar el estado de un programa o una lista de objetos**.  
Por ejemplo, una aplicación deportiva podría guardar la plantilla de un equipo, sus estadísticas o los contactos de los jugadores en un fichero binario, y luego recuperarlos al iniciar el programa.

**Ejemplo práctico:**  
Guardar los datos de los jugadores al final del día y cargarlos en la siguiente sesión del programa sin perder información.  
Esto demuestra la aplicación directa de la **serialización de objetos** como paso previo a trabajar con bases de datos u otros formatos más complejos.

---

Con este ejercicio he aprendido a **guardar y recuperar objetos** en Python usando `pickle`, lo que forma parte de los conceptos de **persistencia de datos**.  
Es una base muy útil dentro de la unidad de **acceso a datos**, ya que me permite entender cómo se conserva la información entre ejecuciones.  
Este conocimiento es el primer paso antes de pasar a formatos como **JSON** o **bases de datos** más avanzadas, donde se aplica el mismo principio de guardar información estructurada para reutilizarla.
