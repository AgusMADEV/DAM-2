Como aficionado a los **videojuegos** y a compartir partidas con mis amigos, este ejercicio me ayuda a entender cómo se puede **almacenar y gestionar información compleja de jugadores y sus compras** de una forma ordenada y reutilizable.  
Con **Python y `amadevorm` (mi implementación de `jvorm`)**, puedo **conectar una base de datos MySQL, cargar datos desde un JSON y procesarlos** sin tener que escribir manualmente consultas complicadas.  
Así aprendo a manejar datos reales —como historiales de compra, preferencias o contacto de los jugadores— de forma estructurada y persistente.

---

El ejercicio consiste en **establecer la conexión con MySQL mediante la clase `JsonMySQLBridge`**, recuperar los datos en formato JSON, **procesar la información** para obtener estadísticas como el número total de compras y el gasto total por jugador, y **visualizar un informe final** con los resultados.

### Código base del ejercicio:
```python
from amadevorm import JsonMySQLBridge

bridge = JsonMySQLBridge(
    host="localhost",
    user="desfase",
    password="desfase",
    database="desfase",
    json_path_default="./datos.json"
)

# 1) Conexión y recuperación
# bridge.load_from_json()  # (solo si queremos cargar el JSON a la BD)
recovered = bridge.dump_to_json("./dump_recuperado.json")

# 2) Procesamiento y visualización
jugadores = recovered.get("jugadores", [])
for j in jugadores:
    usuario = j.get("nombre_usuario")
    compras = j.get("historial_compras", [])
    total = sum([c.get("total", 0) for c in compras if isinstance(c, dict)])
    print(usuario, "→", len(compras), "compras •", f"{total:.2f} €")
```

### Explicación técnica:
1. **Conexión con MySQL:** la clase `JsonMySQLBridge` actúa como un puente entre JSON y MySQL, configurando la conexión sin librerías externas.  
2. **Recuperación de datos:** se utiliza `dump_to_json()` para reconstruir todos los datos de la base de datos en formato JSON.  
3. **Procesamiento:** se recorren los jugadores y su historial de compras, calculando el número total de compras y el importe gastado.  
4. **Visualización:** se muestra un informe simple en consola con los datos procesados.  

Este proceso demuestra el uso correcto de las herramientas del conector `jvorm`, aplicando un mapeo objeto-relacional sin necesidad de escribir SQL manual.

### Ejemplo de salida en consola:
```
Informe de compras por jugador
Usuario                    #Compras   #Items      € Total
---------------------------------------------------------
AgusmaDEV                        2        3        309.97
ElenaBotezatu03                  1        1         59.99
---------------------------------------------------------
TOTAL                            3        4        369.96
```

---

Este ejercicio muestra cómo un programa puede **leer datos jerárquicos complejos**, almacenarlos en una base de datos relacional y luego **reconstruirlos y analizarlos fácilmente**.  
Es un ejemplo claro de cómo se aplican los principios del **mapeo objeto-relacional (ORM)** y la **persistencia de datos** en un contexto práctico.

**Ejemplo práctico:**  
Una tienda de videojuegos podría usar este mismo enfoque para gestionar clientes, sus historiales de compra, y generar informes automáticos sobre ventas o preferencias de plataformas.  

```python
from amadevorm import JsonMySQLBridge

bridge = JsonMySQLBridge(
    host="localhost",
    user="desfase",
    password="desfase",
    database="desfase",
    json_path_default="./datos.json"
)

# --- Si necesitas cargar/recrear la BD desde el JSON, descomenta:
# bridge.load_from_json()

# 2) Recuperación: leemos toda la BD y reconstruimos JSON
recovered = bridge.dump_to_json("./dump_recuperado.json")

# 3) Procesamiento: nº de compras y gasto total por jugador
jugadores = recovered.get("jugadores", [])
res = []
total_global = 0.0
compras_globales = 0
items_globales = 0

def as_list(x):
    if isinstance(x, list):
        return x
    if isinstance(x, dict):
        return [x]
    return []

for j in jugadores:
    if not isinstance(j, dict):
        continue
    usuario = j.get("nombre_usuario", "(sin nombre)")

    # historial_compras puede ser lista o dict (si solo hay 1)
    compras = as_list(j.get("historial_compras", []))

    num_compras = 0
    total_gastado = 0.0
    num_items = 0

    for compra in compras:
        if not isinstance(compra, dict):
            continue

        num_compras += 1
        total_compra = compra.get("total", None)

        # productos puede ser lista o dict (si solo hay 1)
        productos = as_list(compra.get("productos", []))

        if total_compra is None:
            subtotal = 0.0
            for p in productos:
                if not isinstance(p, dict):
                    continue
                try:
                    cantidad = int(p.get("cantidad", 0) or 0)
                    precio = float(p.get("precio_unitario", 0) or 0.0)
                except (TypeError, ValueError):
                    cantidad, precio = 0, 0.0
                subtotal += cantidad * precio
                num_items += cantidad
            total_compra = subtotal
        else:
            # contamos items aunque venga 'total'
            for p in productos:
                if not isinstance(p, dict):
                    continue
                try:
                    num_items += int(p.get("cantidad", 0) or 0)
                except (TypeError, ValueError):
                    pass

        try:
            total_gastado += float(total_compra or 0.0)
        except (TypeError, ValueError):
            pass

    res.append({
        "usuario": usuario,
        "num_compras": num_compras,
        "total_gastado": total_gastado,
        "num_items": num_items
    })

    total_global += total_gastado
    compras_globales += num_compras
    items_globales += num_items

# 4) Visualización: informe simple
print("Informe de compras por jugador")
print(f"{'Usuario':25} {'#Compras':>8} {'#Items':>8} {'€ Total':>12}")
print("-" * 57)
for r in sorted(res, key=lambda x: x["usuario"].lower()):
    print(f"{r['usuario']:25} {r['num_compras']:>8} {r['num_items']:>8} {r['total_gastado']:>12.2f}")
print("-" * 57)
print(f"{'TOTAL':25} {compras_globales:>8} {items_globales:>8} {total_global:>12.2f}")
```

---

Con este ejercicio he aprendido a **conectar Python con MySQL**, convertir datos entre JSON y tablas relacionales, y **procesar información útil para generar informes**.  
Esto se relaciona directamente con la unidad de **acceso a datos y manejo de conectores**, ya que combina el uso de bases de datos, estructuras JSON y persistencia.  
Comprender este flujo me prepara para trabajar con **ORMs más avanzados** y para **automatizar el análisis de datos reales en proyectos profesionales**.
