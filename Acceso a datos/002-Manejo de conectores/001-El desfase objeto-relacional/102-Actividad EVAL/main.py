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