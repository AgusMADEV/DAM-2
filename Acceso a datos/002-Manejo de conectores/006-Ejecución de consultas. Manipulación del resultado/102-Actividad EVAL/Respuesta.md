En este ejercicio se aprende a **simular el funcionamiento de una base de datos** utilizando **carpetas y archivos CSV** en lugar de un sistema gestor real como MySQL o SQLite.  
La idea es imaginar que cada carpeta dentro de la carpeta principal `db` representa una **base de datos**, y cada archivo CSV dentro de esas carpetas sería una **tabla**.  
Como aficionado a los **deportes digitales**, me resulta interesante porque puedo organizar mis datos como si estuviera gestionando ligas, equipos o resultados sin necesidad de un servidor real.

---

El código implementa un método estático llamado `peticion` que interpreta la instrucción `"SHOW DATABASES;"`, igual que en MySQL, pero de forma simulada.  
El método lista las carpetas dentro del directorio `db` y las muestra como si fueran bases de datos existentes.

```python
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
```

1. **Definición de clase:**  
   `DeportesDB` representa un sistema de base de datos simulado.  
2. **Atributo estático:**  
   `carpeta_bd` contiene la ruta principal donde se almacenan las carpetas de bases de datos.  
3. **Método estático `peticion`:**  
   - Recibe un texto con la petición SQL simulada.  
   - Si la petición es `"SHOW DATABASES;"`, lista todas las carpetas dentro de `db`.  
   - Imprime y devuelve la lista de nombres de carpetas (bases de datos).  
4. **Uso de `os.listdir()`:**  
   Permite obtener el listado de directorios dentro de `db`, que equivalen a las bases de datos simuladas.  

**Ejemplo de estructura:**
```
db/
├── futbol
├── baloncesto
├── tenis
```
**Salida esperada en consola:**
```
futbol
baloncesto
tenis
```

---

```python
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
```

Para probar el código, he creado varias carpetas dentro del directorio `db`, por ejemplo:
```
db/
├── futbol
├── baloncesto
├── tenis
```
Al ejecutar el programa:
```bash
python deportesdb.py
```
La salida fue:
```
futbol
baloncesto
tenis
```
Esto demuestra que el método `peticion("SHOW DATABASES;")` funciona correctamente, mostrando todas las “bases de datos” disponibles.  
Es una forma práctica de **simular una consulta SQL real** sin depender de un motor de base de datos.

---

Este ejercicio me ayudó a entender cómo funcionan las **estructuras jerárquicas de datos** en una base de datos real.  
Simular consultas SQL con carpetas y archivos me permite visualizar de forma sencilla cómo **MySQL organiza sus bases, tablas y registros**.  
Además, es una base útil para proyectos futuros, donde podría ampliar la clase `DeportesDB` para incluir operaciones como `SHOW TABLES;` o `SELECT`, aplicándolo en pequeños sistemas de **gestión de información deportiva sin necesidad de un servidor**.
