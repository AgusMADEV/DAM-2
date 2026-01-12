"""
Servicio de IA con Ollama - ERP Inteligente
Basado en el patrón Flask visto en clase (servidor.py)
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import json
from datetime import datetime

# Importar nuestros módulos
from ollama_client import get_ollama_client
from intent_classifier import get_classifier
from query_generator import get_query_generator
from response_formatter import format_response

app = Flask(__name__)
CORS(app)  # Habilitar CORS para permitir peticiones desde el frontend

# Configuración de BD (como en vuestros proyectos)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'erp_inteligente',
    'charset': 'utf8mb4'
}

def get_db_connection():
    """Obtener conexión a BD - Patrón visto en clase"""
    try:
        return pymysql.connect(**DB_CONFIG)
    except Exception as e:
        print(f"[ERROR] Conexión BD: {e}")
        return None

def ejecutar_consulta(sql, params=None):
    """
    Ejecutar consulta SQL y devolver resultados
    Basado en el patrón de vuestros proyectos
    """
    conexion = get_db_connection()
    if not conexion:
        return None
    
    try:
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        
        resultados = cursor.fetchall()
        conexion.close()
        return resultados
        
    except Exception as e:
        print(f"[ERROR] Ejecutando consulta: {e}")
        if conexion:
            conexion.close()
        return None

def guardar_conversacion(usuario_id, mensaje, respuesta, intencion, confianza, sql_generado=None):
    """Guardar conversación en BD para historial"""
    conexion = get_db_connection()
    if not conexion:
        return
    
    try:
        cursor = conexion.cursor()
        sql = """
            INSERT INTO conversaciones_ia 
            (usuario_id, session_id, mensaje_usuario, respuesta_ia, intencion, confianza, consulta_sql)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            usuario_id,
            f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            mensaje,
            respuesta,
            intencion,
            confianza,
            sql_generado
        ))
        conexion.commit()
        conexion.close()
    except Exception as e:
        print(f"[ERROR] Guardando conversación: {e}")
        if conexion:
            conexion.close()

@app.route('/', methods=['GET'])
def home():
    """Página de inicio del servicio"""
    return jsonify({
        'servicio': 'ERP Inteligente - Servicio IA',
        'estado': 'activo',
        'ollama_disponible': get_ollama_client().check_connection(),
        'version': '1.0'
    })

@app.route('/chat', methods=['POST'])
def chat():
    """
    Endpoint principal del chat con IA
    Recibe mensaje del usuario y devuelve respuesta
    """
    try:
        # Obtener datos del request (como en Flask visto en clase)
        data = request.get_json() if request.is_json else request.form.to_dict()
        
        mensaje_usuario = data.get('mensaje', '').strip()
        usuario_id = data.get('usuario_id', 1)
        usar_ia = data.get('usar_ia', False)
        
        if not mensaje_usuario:
            return jsonify({
                'error': 'Mensaje vacío'
            }), 400
        
        print(f"\n[USUARIO] {mensaje_usuario}")
        
        # 1. Clasificar intención
        classifier = get_classifier()
        intencion, confianza = classifier.classify(mensaje_usuario, use_ai=usar_ia)
        
        print(f"[IA] Intención: {intencion} (confianza: {confianza}%)")
        
        # 2. Procesar según intención
        if intencion in ['saludo', 'ayuda']:
            # Respuestas predefinidas (no necesitan BD)
            respuesta = procesar_intenciones_simples(intencion, mensaje_usuario)
            sql_generado = None
            
        elif intencion == 'desconocido':
            # Intentar responder con IA general
            respuesta = "Lo siento, no estoy seguro de cómo ayudarte con eso. ¿Podrías reformular tu pregunta? Puedo ayudarte con consultas sobre stock, ventas, clientes, productos o generar informes."
            sql_generado = None
            
        else:
            # Consultas que requieren acceso a BD
            query_gen = get_query_generator()
            sql, params = query_gen.generate(intencion, mensaje_usuario)
            
            if sql:
                print(f"[SQL] {sql}")
                resultados = ejecutar_consulta(sql, params)
                
                if resultados is not None:
                    # Formatear respuesta con los datos
                    respuesta = format_response(intencion, resultados, mensaje_usuario)
                    sql_generado = sql
                else:
                    respuesta = "Hubo un error al consultar la base de datos. Por favor, intenta de nuevo."
                    sql_generado = None
            else:
                respuesta = "No pude generar una consulta para tu pregunta. ¿Podrías ser más específico?"
                sql_generado = None
        
        # 3. Guardar en historial
        guardar_conversacion(
            usuario_id, 
            mensaje_usuario, 
            respuesta, 
            intencion, 
            confianza,
            sql_generado
        )
        
        print(f"[IA] {respuesta}\n")
        
        # 4. Devolver respuesta
        return jsonify({
            'respuesta': respuesta,
            'intencion': intencion,
            'confianza': confianza,
            'sql_generado': sql_generado if sql_generado else None
        })
        
    except Exception as e:
        print(f"[ERROR] En /chat: {e}")
        return jsonify({
            'error': 'Error interno del servidor',
            'detalle': str(e)
        }), 500

def procesar_intenciones_simples(intencion, mensaje):
    """Procesar intenciones que no requieren BD"""
    if intencion == 'saludo':
        return "¡Hola! Soy el asistente del ERP. Puedo ayudarte con consultas sobre stock, ventas, clientes, productos, generar informes y más. ¿En qué puedo ayudarte?"
    
    elif intencion == 'ayuda':
        return """Puedo ayudarte con:
- Consultas de stock e inventario ("¿qué productos tienen stock bajo?")
- Consultas de ventas ("¿cuánto vendimos esta semana?")
- Información de clientes ("¿quiénes son los mejores clientes?")
- Información de productos ("muéstrame los productos más vendidos")
- Generar informes ("dame un informe de ventas del mes")
- Alertas y problemas ("¿hay algún problema pendiente?")

¿Qué necesitas?"""
    
    return "¿En qué puedo ayudarte?"

@app.route('/test-ollama', methods=['GET'])
def test_ollama():
    """Endpoint para probar conexión con Ollama"""
    ollama = get_ollama_client()
    
    if not ollama.check_connection():
        return jsonify({
            'estado': 'error',
            'mensaje': 'Ollama no está disponible. ¿Está ejecutándose?'
        }), 503
    
    # Hacer una consulta de prueba
    respuesta = ollama.generate("Di solo 'OK' si me recibes", temperature=0.1)
    
    return jsonify({
        'estado': 'ok',
        'ollama_activo': True,
        'modelo': ollama.model,
        'prueba_respuesta': respuesta
    })

@app.route('/historial/<int:usuario_id>', methods=['GET'])
def obtener_historial(usuario_id):
    """Obtener historial de conversaciones de un usuario"""
    try:
        sql = """
            SELECT 
                mensaje_usuario,
                respuesta_ia,
                intencion,
                timestamp
            FROM conversaciones_ia
            WHERE usuario_id = %s
            ORDER BY timestamp DESC
            LIMIT 20
        """
        resultados = ejecutar_consulta(sql, (usuario_id,))
        
        if resultados:
            return jsonify({
                'historial': resultados
            })
        else:
            return jsonify({
                'historial': []
            })
            
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🤖 SERVICIO IA - ERP INTELIGENTE")
    print("=" * 60)
    print("Puerto: 5000")
    print("Endpoints:")
    print("  - GET  /              : Info del servicio")
    print("  - POST /chat          : Chat con IA")
    print("  - GET  /test-ollama   : Probar Ollama")
    print("  - GET  /historial/:id : Historial de usuario")
    print("=" * 60)
    
    # Verificar Ollama
    ollama = get_ollama_client()
    if ollama.check_connection():
        print("✅ Ollama conectado")
    else:
        print("⚠️  Ollama NO disponible - Iniciar con: ollama serve")
    
    print("=" * 60)
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
