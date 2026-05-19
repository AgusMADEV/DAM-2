# modules/aprobar.py
"""
Nodo Aprobar: Aprueba o rechaza una orden según el monto
"""

TOOL = {
    "type": "aprobar",
    "label": "✅ Aprobar",
    "description": "Aprueba o rechaza una orden según criterios (ej: monto máximo)",
    "config": {
        "monto_maximo": {"type": "number", "label": "Monto Máximo (€)", "default": 1000}
    }
}


def execute(config, context):
    """
    Aprueba o rechaza una orden según el monto máximo configurado
    """
    monto_max = float(config.get("monto_maximo", 1000))
    inputs = context.get("inputs", [])
    
    # Obtener la orden del input
    orden = None
    for inp in inputs:
        if isinstance(inp, dict) and "numero" in inp:
            orden = inp
            break
    
    if not orden:
        return {
            "message": "⚠️ No se recibió ninguna orden para aprobar",
            "value": None
        }
    
    total = orden.get("total", 0)
    aprobada = total <= monto_max
    
    # Crear resultado
    resultado = dict(orden)  # copiar orden
    resultado["estado"] = "aprobada" if aprobada else "rechazada"
    resultado["razon"] = f"Total {total}€ {'≤' if aprobada else '>'} límite {monto_max}€"
    
    emoji = "✅" if aprobada else "❌"
    message = f"{emoji} Orden {orden.get('numero', 'N/A')}: {resultado['estado']} ({resultado['razon']})"
    
    return {
        "message": message,
        "value": resultado
    }
