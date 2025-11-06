En este ejercicio partimos de una situación cercana: alguien que disfruta del deporte, los videojuegos y los viajes quiere organizar sus actividades diarias.  
Para eso, aprendemos a **trabajar con archivos CSV en Python**, un formato muy común para guardar información estructurada.  
La idea es ver cómo escribir y leer datos desde un archivo de texto, entendiendo el flujo completo de guardar una actividad y recuperarla más tarde.

---

El programa implementa una clase llamada **`Actividades`** que permite registrar y consultar actividades guardadas en un archivo CSV.

### Código principal:
```python
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
```

1. **Inicialización:** el constructor define el nombre del archivo (`actividades.csv`).  
2. **Escritura:** el método `escribir_actividad()` toma una tupla, la convierte en texto separado por comas y la guarda en el archivo.  
3. **Lectura:** el método `leer_actividad()` abre el archivo, lee la primera línea y la devuelve como una tupla con `split(',')`.  
4. **Prueba final:** se escribe una actividad y luego se lee para comprobar que los datos se guardaron correctamente.

---

### Contenido guardado en `actividades.csv`:
```
Jugar un partido de Baloncesto,2023-10-05,Deporte
```

### Resultado en la consola:
```
Actividad leída: ('Jugar un partido de Baloncesto', '2023-10-05', 'Deporte')
```

Esto muestra claramente el proceso de **guardar** información en formato CSV y luego **leerla** como una estructura Python.  
De esta forma, el código permite manejar pequeñas bases de datos de actividades sin depender de herramientas externas.

---

Has aprendido cómo manejar **archivos CSV** en Python, una habilidad clave dentro del tema de **acceso a datos**.  
Este tipo de archivos es ideal para guardar listas de tareas o actividades de forma simple y reutilizable.  
Con este mismo enfoque podrías crear una app más completa para planificar tus entrenamientos, registrar tus partidas o programar tus viajes.  
La práctica con ficheros te acerca un paso más a la gestión real de datos en proyectos de software.
