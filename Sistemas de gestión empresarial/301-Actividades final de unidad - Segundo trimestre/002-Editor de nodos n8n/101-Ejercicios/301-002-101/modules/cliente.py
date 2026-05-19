# modules/cliente.py
"""
Nodo Cliente: Representa información de un cliente
"""

TOOL = {
    "type": "cliente",
    "label": "👤 Cliente",
    "description": "Información de cliente para procesos empresariales",
    "config": {
        "nombre": {"type": "string", "label": "Nombre", "default": ""},
        "email": {"type": "string", "label": "Email", "default": ""},
        "telefono": {"type": "string", "label": "Teléfono", "default": ""}
    }
}


def execute(config, context):
    """
    Ejecuta el nodo cliente, devolviendo la información del cliente
    """
    nombre = config.get("nombre", "Cliente Anónimo")
    email = config.get("email", "")
    telefono = config.get("telefono", "")
    
    cliente_data = {
        "nombre": nombre,
        "email": email,
        "telefono": telefono
    }
    
    message = f"Cliente: {nombre}"
    if email:
        message += f" ({email})"
    
    return {
        "message": message,
        "value": cliente_data
    }
