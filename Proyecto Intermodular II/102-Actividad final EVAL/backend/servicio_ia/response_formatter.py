def format_response(intencion, resultados, pregunta_original):
    if not resultados or len(resultados) == 0:
        return _respuesta_sin_datos(intencion)
    
    # Formatear según intención
    if intencion == 'consulta_stock':
        return _format_stock(resultados, pregunta_original)
    elif intencion == 'consulta_ventas':
        return _format_ventas(resultados, pregunta_original)
    elif intencion == 'consulta_clientes':
        return _format_clientes(resultados, pregunta_original)
    elif intencion == 'consulta_productos':
        return _format_productos(resultados, pregunta_original)
    elif intencion == 'alerta':
        return _format_alertas(resultados)
    else:
        return _format_generico(resultados)

def _respuesta_sin_datos(intencion):
    """Respuesta cuando no hay datos"""
    respuestas = {
        'consulta_stock': 'No encontré productos con esos criterios.',
        'consulta_ventas': 'No hay ventas registradas para ese período.',
        'consulta_clientes': 'No encontré clientes con esos criterios.',
        'consulta_productos': 'No hay productos que coincidan.',
        'alerta': '¡Genial! No hay alertas pendientes.'
    }
    return respuestas.get(intencion, 'No encontré información.')

def _format_stock(resultados, pregunta):
    """Formatear respuestas de stock"""
    if 'bajo' in pregunta.lower() or 'poco' in pregunta.lower():
        num_productos = len(resultados)
        respuesta = f"📦 He encontrado {num_productos} producto(s) con stock bajo:\n\n"
        
        for i, row in enumerate(resultados[:10], 1):  # Máximo 10
            nombre = row.get('nombre', 'Sin nombre')
            codigo = row.get('codigo', '')
            stock = row.get('stock_actual', 0)
            minimo = row.get('stock_minimo', 0)
            faltante = row.get('faltante', 0)
            
            respuesta += f"{i}. {nombre} (#{codigo})\n"
            respuesta += f"   Stock actual: {stock} unidades (mínimo: {minimo})\n"
            respuesta += f"   Faltan: {faltante} unidades\n\n"
        
        if num_productos > 10:
            respuesta += f"... y {num_productos - 10} producto(s) más.\n"
        
        respuesta += "¿Quieres que te ayude con algo más?"
        return respuesta
    
    else:
        # Listado general de stock
        respuesta = f"📦 Stock de productos ({len(resultados)} encontrados):\n\n"
        for i, row in enumerate(resultados[:15], 1):
            nombre = row.get('nombre', 'Sin nombre')
            stock = row.get('stock_actual', 0)
            respuesta += f"{i}. {nombre}: {stock} unidades\n"
        
        if len(resultados) > 15:
            respuesta += f"... y {len(resultados) - 15} más.\n"
        
        return respuesta

def _format_ventas(resultados, pregunta):
    """Formatear respuestas de ventas"""
    pregunta_lower = pregunta.lower()
    
    # Ventas diarias/semanales
    if 'fecha' in resultados[0] and 'num_ventas' in resultados[0]:
        respuesta = "📊 Resumen de ventas:\n\n"
        total_general = 0
        
        for row in resultados:
            fecha = row.get('fecha', '')
            num = row.get('num_ventas', 0)
            total = row.get('total_ingresos', 0)
            total_general += total
            
            respuesta += f"📅 {fecha}: {num} ventas - €{total:,.2f}\n"
        
        respuesta += f"\n💰 Total: €{total_general:,.2f}"
        return respuesta
    
    # Resumen del mes
    elif 'num_ventas' in resultados[0] and 'ticket_promedio' in resultados[0]:
        row = resultados[0]
        num_ventas = row.get('num_ventas', 0)
        total = row.get('total_ingresos', 0)
        promedio = row.get('ticket_promedio', 0)
        
        respuesta = "📊 Ventas del mes:\n\n"
        respuesta += f"• Número de ventas: {num_ventas}\n"
        respuesta += f"• Total ingresado: €{total:,.2f}\n"
        respuesta += f"• Ticket promedio: €{promedio:,.2f}\n"
        return respuesta
    
    # Facturas pendientes
    elif 'dias_vencido' in resultados[0]:
        num_facturas = len(resultados)
        total_pendiente = sum(row.get('total', 0) for row in resultados)
        
        respuesta = f"⚠️  Hay {num_facturas} factura(s) vencida(s):\n\n"
        
        for i, row in enumerate(resultados[:10], 1):
            factura = row.get('numero_factura', '')
            cliente = row.get('cliente', 'Sin nombre')
            total = row.get('total', 0)
            dias = row.get('dias_vencido', 0)
            
            respuesta += f"{i}. Factura {factura} - {cliente}\n"
            respuesta += f"   Importe: €{total:,.2f} | Vencida hace {dias} días\n\n"
        
        respuesta += f"💰 Total pendiente de cobro: €{total_pendiente:,.2f}"
        return respuesta
    
    # Listado de ventas
    else:
        respuesta = f"💳 Últimas ventas ({len(resultados)}):\n\n"
        for i, row in enumerate(resultados[:10], 1):
            factura = row.get('numero_factura', '')
            cliente = row.get('cliente', 'Sin nombre')
            total = row.get('total', 0)
            estado = row.get('estado', '')
            
            respuesta += f"{i}. {factura} - {cliente}: €{total:,.2f} ({estado})\n"
        
        return respuesta

def _format_clientes(resultados, pregunta):
    """Formatear respuestas de clientes"""
    pregunta_lower = pregunta.lower()
    
    # Top clientes
    if 'mejor' in pregunta_lower or 'top' in pregunta_lower:
        respuesta = "🏆 Top 10 Mejores Clientes:\n\n"
        
        for i, row in enumerate(resultados, 1):
            nombre = row.get('nombre', 'Sin nombre')
            total = row.get('total_compras', 0)
            ciudad = row.get('ciudad', '')
            
            respuesta += f"{i}. {nombre}"
            if ciudad:
                respuesta += f" ({ciudad})"
            respuesta += f"\n   Total compras: €{total:,.2f}\n\n"
        
        return respuesta
    
    # Clientes inactivos
    elif 'inactivo' in pregunta_lower or 'sin comprar' in pregunta_lower:
        num_clientes = len(resultados)
        respuesta = f"😴 {num_clientes} cliente(s) inactivo(s):\n\n"
        
        for i, row in enumerate(resultados[:10], 1):
            nombre = row.get('nombre', 'Sin nombre')
            dias = row.get('dias_inactivo', 0)
            email = row.get('email', '')
            telefono = row.get('telefono', '')
            
            respuesta += f"{i}. {nombre}\n"
            respuesta += f"   Sin comprar hace {dias} días\n"
            if email:
                respuesta += f"   📧 {email}\n"
            if telefono:
                respuesta += f"   📱 {telefono}\n"
            respuesta += "\n"
        
        respuesta += "💡 Sugerencia: Podrías enviarles un email con una oferta especial."
        return respuesta
    
    # Listado general
    else:
        respuesta = f"👥 Clientes ({len(resultados)}):\n\n"
        for i, row in enumerate(resultados[:15], 1):
            nombre = row.get('nombre', 'Sin nombre')
            ciudad = row.get('ciudad', '')
            total = row.get('total_compras', 0)
            
            respuesta += f"{i}. {nombre}"
            if ciudad:
                respuesta += f" - {ciudad}"
            if total > 0:
                respuesta += f" (€{total:,.2f})"
            respuesta += "\n"
        
        return respuesta

def _format_productos(resultados, pregunta):
    """Formatear respuestas de productos"""
    pregunta_lower = pregunta.lower()
    
    # Top productos vendidos
    if 'vendidos' in pregunta_lower or 'top' in pregunta_lower:
        respuesta = "🏆 Top 10 Productos Más Vendidos:\n\n"
        
        for i, row in enumerate(resultados, 1):
            nombre = row.get('nombre', 'Sin nombre')
            unidades = row.get('unidades_vendidas', 0)
            precio = row.get('precio_venta', 0)
            stock = row.get('stock_actual', 0)
            
            respuesta += f"{i}. {nombre}\n"
            respuesta += f"   Vendidas: {unidades} unidades\n"
            respuesta += f"   Precio: €{precio:,.2f} | Stock: {stock}\n\n"
        
        return respuesta
    
    # Listado general
    else:
        respuesta = f"📦 Productos ({len(resultados)}):\n\n"
        for i, row in enumerate(resultados[:15], 1):
            codigo = row.get('codigo', '')
            nombre = row.get('nombre', 'Sin nombre')
            precio = row.get('precio_venta', 0)
            stock = row.get('stock_actual', 0)
            
            respuesta += f"{i}. {nombre} (#{codigo})\n"
            respuesta += f"   €{precio:,.2f} | Stock: {stock}\n"
        
        if len(resultados) > 15:
            respuesta += f"... y {len(resultados) - 15} más.\n"
        
        return respuesta

def _format_alertas(resultados):
    """Formatear alertas"""
    num_alertas = len(resultados)
    
    # Contar por severidad
    criticas = sum(1 for r in resultados if r.get('severidad') == 'critical')
    warnings = sum(1 for r in resultados if r.get('severidad') == 'warning')
    
    respuesta = f"🚨 Tienes {num_alertas} alerta(s) pendiente(s):\n"
    if criticas > 0:
        respuesta += f"   • {criticas} crítica(s)\n"
    if warnings > 0:
        respuesta += f"   • {warnings} aviso(s)\n"
    respuesta += "\n"
    
    for i, row in enumerate(resultados[:10], 1):
        severidad = row.get('severidad', 'info')
        titulo = row.get('titulo', 'Sin título')
        descripcion = row.get('descripcion', '')
        
        # Icono según severidad
        icono = '🔴' if severidad == 'critical' else '🟡' if severidad == 'warning' else '🔵'
        
        respuesta += f"{icono} {titulo}\n"
        if descripcion:
            respuesta += f"   {descripcion}\n"
        respuesta += "\n"
    
    if num_alertas > 10:
        respuesta += f"... y {num_alertas - 10} alerta(s) más.\n"
    
    return respuesta

def _format_generico(resultados):
    """Formato genérico para otros casos"""
    respuesta = f"He encontrado {len(resultados)} resultado(s):\n\n"
    
    for i, row in enumerate(resultados[:10], 1):
        respuesta += f"{i}. "
        # Mostrar todos los campos
        campos = [f"{k}: {v}" for k, v in row.items() if v is not None]
        respuesta += " | ".join(campos[:3])  # Máximo 3 campos
        respuesta += "\n"
    
    return respuesta
