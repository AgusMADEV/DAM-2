"""
Clasificador de Intenciones
Identifica qué tipo de consulta está haciendo el usuario
Solo con librerías estándar de Python
"""

import re
from ollama_client import get_ollama_client

class IntentClassifier:
    """Clasificador de intenciones del usuario"""
    
    # Definición de intenciones soportadas
    INTENTS = {
        'consulta_stock': {
            'keywords': ['stock', 'inventario', 'cantidad', 'cuántos', 'unidades', 'existencias', 'bajo stock'],
            'patterns': [
                r'\b(stock|inventario|unidades)\b.*\b(bajo|poco|mínimo|crítico)\b',
                r'\b(cuánto|cuántos|cantidad)\b.*\b(stock|inventario|quedan)\b',
                r'\b(productos|artículos)\b.*\b(stock|inventario)\b'
            ]
        },
        'consulta_ventas': {
            'keywords': ['ventas', 'vendido', 'facturas', 'ingresos', 'facturación', 'vendí'],
            'patterns': [
                r'\b(ventas|vendido)\b.*\b(hoy|semana|mes|año)\b',
                r'\b(cuánto|total)\b.*\b(vendido|ventas|ingresos)\b',
                r'\b(facturas?)\b.*\b(pendiente|pagada|vencida)\b'
            ]
        },
        'consulta_clientes': {
            'keywords': ['cliente', 'clientes', 'comprador', 'compradores'],
            'patterns': [
                r'\b(cliente|clientes)\b.*\b(mejor|top|más|inactivo)\b',
                r'\b(quién|cual)\b.*\b(cliente|comprado|compra)\b',
                r'\b(clientes?)\b.*\b(sin comprar|inactivos)\b'
            ]
        },
        'consulta_productos': {
            'keywords': ['producto', 'productos', 'artículo', 'artículos', 'catálogo'],
            'patterns': [
                r'\b(producto|productos)\b.*\b(más|mejor|top)\b',
                r'\b(cuáles?|qué)\b.*\b(productos?|artículos?)\b',
                r'\b(busca|encuentra|muestra)\b.*\b(producto)\b'
            ]
        },
        'generar_informe': {
            'keywords': ['informe', 'reporte', 'resumen', 'estadísticas', 'análisis', 'dame'],
            'patterns': [
                r'\b(dame|genera|crea|haz)\b.*\b(informe|reporte|resumen)\b',
                r'\b(informe|reporte)\b.*\b(de|sobre)\b',
                r'\b(estadísticas?)\b.*\b(de|sobre)\b'
            ]
        },
        'prediccion': {
            'keywords': ['predice', 'predicción', 'estimación', 'futuro', 'próximo', 'venderemos'],
            'patterns': [
                r'\b(cuánto|qué)\b.*\b(vender|venta)\b.*\b(próximo|siguiente|futuro)\b',
                r'\b(predice|predecir|estima)\b',
                r'\b(cuando|cuándo)\b.*\b(reabastecer|reponer|pedir)\b'
            ]
        },
        'alerta': {
            'keywords': ['alerta', 'alertas', 'problema', 'problemas', 'atención', 'crítico'],
            'patterns': [
                r'\b(hay|existe|tengo)\b.*\b(problema|alerta)\b',
                r'\b(alertas?|problemas?)\b.*\b(pendiente|sin resolver)\b',
                r'\b(qué debo|necesito)\b.*\b(atender|revisar)\b'
            ]
        },
        'automatizacion': {
            'keywords': ['envía', 'actualiza', 'cambia', 'modifica', 'automático'],
            'patterns': [
                r'\b(envía|enviar|manda)\b.*\b(email|correo|recordatorio)\b',
                r'\b(actualiza|cambia|modifica)\b.*\b(precio|stock)\b',
                r'\b(hacer|ejecutar)\b.*\b(automático|automatizar)\b'
            ]
        },
        'saludo': {
            'keywords': ['hola', 'buenos días', 'buenas tardes', 'buenas', 'hey', 'saludos'],
            'patterns': [
                r'^\s*(hola|buenos|buenas|hey)\b',
                r'\b(cómo estás|qué tal)\b'
            ]
        },
        'ayuda': {
            'keywords': ['ayuda', 'ayúdame', 'puedes', 'cómo', 'qué puedes'],
            'patterns': [
                r'\b(ayuda|ayúdame)\b',
                r'\b(qué puedes|cómo funciona)\b',
                r'\b(cómo)\b.*\b(hacer|funciona)\b'
            ]
        }
    }
    
    def __init__(self):
        self.ollama = get_ollama_client()
    
    def classify_with_rules(self, texto):
        """
        Clasificación basada en reglas (rápida, sin IA)
        
        Returns:
            tuple: (intencion, confianza)
        """
        texto_lower = texto.lower()
        scores = {}
        
        for intent, data in self.INTENTS.items():
            score = 0.0
            
            # Buscar keywords
            for keyword in data['keywords']:
                if keyword in texto_lower:
                    score += 1.0
            
            # Buscar patrones regex
            for pattern in data.get('patterns', []):
                if re.search(pattern, texto_lower):
                    score += 2.0  # Los patrones pesan más
            
            if score > 0:
                scores[intent] = score
        
        if not scores:
            return ('desconocido', 0.0)
        
        # Intención con mayor score
        best_intent = max(scores, key=scores.get)
        max_score = scores[best_intent]
        
        # Normalizar confianza a 0-100
        confidence = min(100.0, (max_score / 3.0) * 100)
        
        return (best_intent, confidence)
    
    def classify_with_ai(self, texto):
        """
        Clasificación usando IA (más precisa pero más lenta)
        
        Returns:
            tuple: (intencion, confianza)
        """
        system_prompt = """Eres un clasificador de intenciones para un sistema ERP.
Debes clasificar la consulta del usuario en UNA de estas categorías:
- consulta_stock: Preguntas sobre inventario, stock, unidades disponibles
- consulta_ventas: Preguntas sobre ventas, facturación, ingresos
- consulta_clientes: Preguntas sobre clientes, compradores
- consulta_productos: Preguntas sobre productos, catálogo
- generar_informe: Petición de informes, reportes, estadísticas
- prediccion: Preguntas sobre futuro, predicciones, estimaciones
- alerta: Preguntas sobre problemas, alertas, cosas urgentes
- automatizacion: Petición de ejecutar acciones automáticas
- saludo: Saludos, presentaciones
- ayuda: Pedir ayuda sobre el sistema
- desconocido: Si no encaja en ninguna categoría

Responde SOLO con el nombre de la categoría, sin explicaciones."""
        
        try:
            respuesta = self.ollama.generate(
                prompt=f"Clasifica esta consulta: {texto}",
                system_prompt=system_prompt,
                temperature=0.3,  # Baja temperatura para consistencia
                max_tokens=50
            )
            
            if respuesta:
                # Limpiar respuesta
                intent = respuesta.strip().lower()
                
                # Validar que sea una intención válida
                if intent in self.INTENTS or intent == 'desconocido':
                    return (intent, 85.0)  # Alta confianza con IA
                else:
                    logger.warning(f"IA devolvió intención no válida: {intent}")
                    return self.classify_with_rules(texto)
            else:
                # Fallback a reglas si IA falla
                    return self.classify_with_rules(texto)
                
        except Exception as e:
            print(f"[ERROR] Error en clasificación con IA: {e}")
            return self.classify_with_rules(texto)
    
    def classify(self, texto, use_ai=False):
        """
        Clasificar intención del usuario
        
        Returns:
            tuple: (intencion, confianza)
        """
        if use_ai:
            return self.classify_with_ai(texto)
        else:
            return self.classify_with_rules(texto)
    
    def get_intent_description(self, intent):
        """Obtener descripción de una intención"""
        descriptions = {
            'consulta_stock': 'Consulta sobre stock o inventario',
            'consulta_ventas': 'Consulta sobre ventas o facturación',
            'consulta_clientes': 'Consulta sobre clientes',
            'consulta_productos': 'Consulta sobre productos',
            'generar_informe': 'Generación de informes o reportes',
            'prediccion': 'Predicción o estimación futura',
            'alerta': 'Consulta sobre alertas o problemas',
            'automatizacion': 'Ejecución de acciones automáticas',
            'saludo': 'Saludo o presentación',
            'ayuda': 'Solicitud de ayuda',
            'desconocido': 'Intención no reconocida'
        }
        return descriptions.get(intent, 'Desconocido')


# Instancia global (patrón usado en clase)
_classifier = None

def get_classifier():
    """Obtener instancia global del clasificador"""
    global _classifier
    if _classifier is None:
        _classifier = IntentClassifier()
    return _classifier
