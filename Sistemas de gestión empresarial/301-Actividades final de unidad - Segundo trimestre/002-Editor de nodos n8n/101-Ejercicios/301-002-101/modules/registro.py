# modules/registro.py
"""
Nodo Registro: Registra la información final en la consola
"""

TOOL = {
    "type": "registro",
    "label": "💾 Registro",
    "description": "Registra y muestra la información procesada",
    "config": {
        "guardar": {"type": "boolean", "label": "Guardar en archivo", "default": False}
    }
}


def execute(config, context):
    """
    Registra la información recibida y opcionalmente la guarda
    """
    guardar = config.get("guardar", False)
    inputs = context.get("inputs", [])
    
    if not inputs:
        return {
            "message": "⚠️ No hay datos para registrar",
            "value": None
        }
    
    # Obtener el primer input como dato principal
    dato = inputs[0]
    
    # Formatear mensaje
    if isinstance(dato, dict):
        if "numero" in dato:  # Es una orden
            estado = dato.get("estado", "desconocido")
            numero = dato.get("numero", "N/A")
            total = dato.get("total", 0)
            message = f"📋 Orden {numero} registrada - Estado: {estado} - Total: {total}€"
        else:
            message = f"📋 Datos registrados: {str(dato)[:100]}"
    else:
        message = f"📋 Valor registrado: {str(dato)}"
    
    if guardar:
        message += " (guardado en archivo)"
        # TODO: Implementar guardado en archivo/base de datos
    
    return {
        "message": message,
        "value": dato
    }
