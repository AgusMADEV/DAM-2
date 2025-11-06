En este ejercicio creo **50 archivos JSON** (uno por cliente) dentro de la carpeta `secuenciales/` y construyo una **hash table simple** basada en la **primera letra del nombre** para acceder rápidamente a los datos.  
La idea es practicar dos enfoques de almacenamiento que se ven en clase:
- **Archivo secuencial**: guardo registros en ficheros numerados (`cliente_001.json`, `cliente_002.json`, …). Útil para persistir datos discretos y comprobar estructura.
- **Hash table por inicial**: agrupo clientes por inicial en `clienteA.json`, `clienteB.json`, … Esto reduce el espacio de búsqueda a un subconjunto, emulando el acceso **O(1) esperado** de una tabla hash mediante **partición por clave**.

Además, integro uno de mis hobbies (los **deportes**): antes de codificar hago un **calentamiento breve** (3–4 minutos de movilidad de hombros, cadera y tobillos + 10 sentadillas suaves). Esto me ayuda a empezar la sesión más concentrado y con menos tensión postural.

---

### Estructura de la solución
- **Creación de la carpeta y ficheros secuenciales**
  ```py
  try:
      os.mkdir("secuenciales")
  except:
      pass

  print("Creando 50 archivos secuenciales...")
  for i, cliente in enumerate(clientes):
      with open(f"secuenciales/cliente_{i+1:03d}.json", "w", encoding="utf-8") as f:
          json.dump(cliente, f, indent=4, ensure_ascii=False)
  print("✓ 50 archivos creados\n")
  ```
  *Por qué*: cada registro queda en su propio archivo, con nombre **correlativo** y contenido **JSON identado** para legibilidad.

- **Construcción de la hash table basada en la inicial**
  ```py
  for cliente in clientes:
      inicial = cliente["nombre"][0].upper()
      archivo = f"secuenciales/cliente{inicial}.json"

      if os.path.exists(archivo):
          with open(archivo, "r", encoding="utf-8") as f:
              lista = json.load(f)
      else:
          lista = []

      lista.append(cliente)
      with open(archivo, "w", encoding="utf-8") as f:
          json.dump(lista, f, indent=4, ensure_ascii=False)
  ```
  *Qué hace*: genera un **bucket** por inicial (A..Z). Esto actúa como una **función hash h(nombre)=nombre[0]** y almacena colisiones (múltiples clientes con la misma inicial) en una **lista** dentro del mismo archivo.

- **Búsqueda por nombre a través de la hash table**
  ```py
  def buscar_cliente(nombre):
      inicial = nombre[0].upper()
      archivo = f"secuenciales/cliente{inicial}.json"

      if not os.path.exists(archivo):
          return None

      with open(archivo, encoding="utf-8") as f:
          for cliente in json.load(f):
              if cliente["nombre"].lower() == nombre.lower():
                  return cliente
      return None

  resultado = buscar_cliente("Cristiano")
  print(resultado)
  ```
  *Cómo funciona*: abre solo el **bucket** correspondiente a la inicial y **filtra** por coincidencia exacta de nombre (case-insensitive). Si no existe el bucket, devuelve `None`.

> **Restricciones cumplidas**: no uso librerías externas; solo `os` y `json` de la biblioteca estándar, manejo de ficheros con `with`, y estructuras vistas (listas, diccionarios, bucles, funciones).

---

**Codificación**:
   - Ejecuto el script para **crear los 50 ficheros**: `secuenciales/cliente_001.json` … `secuenciales/cliente_050.json`.
   - En el mismo proceso se generan los **buckets**: por ejemplo `secuenciales/clienteC.json`, `secuenciales/clienteL.json`, etc.
   - Verifico la búsqueda:
     ```py
    resultado = buscar_cliente("Cristiano")
    print(resultado)
     #Salida esperada (ejemplo):
     #{'nombre': 'Cristiano', 'apellido': 'Ronaldo', 'edad': 38, 'ciudad': 'Madrid', 'profesion': 'Futbolista'}
     ```

---

Este ejercicio me ha ayudado a entender cómo guardar y buscar datos de forma ordenada usando archivos y una tabla hash sencilla. Es una base práctica para sistemas de almacenamiento más grandes.
El aprendizaje es aplicable a situaciones reales de **gestión de datos** en proyectos de desarrollo: creación de **herramientas de import/export**, **mocks persistentes** para tests, prototipos de **indexación** por claves y preparación para migrar a soluciones más avanzadas (B‑Trees, bases de datos clave‑valor o índices secundarios). Integrar un **hábito de calentamiento** antes de programar me ha ayudado a mantener la concentración y reducir fatiga, conectando el ejercicio técnico con una rutina saludable.
