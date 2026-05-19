# modules/producto.py
"""
Nodo Producto: Representa información de un producto
"""

TOOL = {
    "type": "producto",
    "label": "📦 Producto",
    "description": "Información de producto para órdenes de compra/venta",
    "config": {
        "nombre": {"type": "string", "label": "Nombre", "default": ""},
        "precio": {"type": "number", "label": "Precio (€)", "default": 0},
        "cantidad": {"type": "number", "label": "Cantidad", "default": 1}
    }
}


def execute(config, context):
    """
    Ejecuta el nodo producto, calculando el total
    """
    nombre = config.get("nombre", "Producto")
    precio = float(config.get("precio", 0))
    cantidad = int(config.get("cantidad", 1))
    
    total = precio * cantidad
    
    producto_data = {
        "nombre": nombre,
        "precio": precio,
        "cantidad": cantidad,
        "total": total
    }
    
    message = f"Producto: {nombre} - {cantidad} uds. × {precio}€ = {total}€"
    
    return {
        "message": message,
        "value": producto_data
    }
