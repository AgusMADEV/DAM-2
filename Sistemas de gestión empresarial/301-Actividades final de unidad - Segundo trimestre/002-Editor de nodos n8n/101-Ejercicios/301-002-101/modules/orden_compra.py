# modules/orden_compra.py
"""
Nodo Orden de Compra: Crea una orden combinando cliente y productos
"""

TOOL = {
    "type": "orden_compra",
    "label": "📝 Orden de Compra",
    "description": "Crea una orden de compra combinando clientes y productos",
    "config": {
        "numero_orden": {"type": "string", "label": "Número de Orden", "default": "ORD-001"}
    }
}


def execute(config, context):
    """
    Crea una orden de compra a partir de los inputs (cliente y productos)
    """
    numero = config.get("numero_orden", "ORD-001")
    inputs = context.get("inputs", [])
    
    # Separar clientes y productos de los inputs
    clientes = []
    productos = []
    total_orden = 0
    
    for inp in inputs:
        if isinstance(inp, dict):
            if "email" in inp:  # Es un cliente
                clientes.append(inp)
            elif "precio" in inp:  # Es un producto
                productos.append(inp)
                total_orden += inp.get("total", 0)
    
    orden_data = {
        "numero": numero,
        "clientes": clientes,
        "productos": productos,
        "total": total_orden,
        "estado": "pendiente"
    }
    
    cliente_info = clientes[0]["nombre"] if clientes else "Sin cliente"
    productos_info = f"{len(productos)} producto(s)"
    
    message = f"Orden {numero}: {cliente_info} - {productos_info} - Total: {total_orden}€"
    
    return {
        "message": message,
        "value": orden_data
    }
