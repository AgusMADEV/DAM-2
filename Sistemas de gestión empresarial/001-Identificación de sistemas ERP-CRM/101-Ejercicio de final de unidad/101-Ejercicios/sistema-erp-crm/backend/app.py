"""
Sistema de Gestión de Gimnasio - Servidor Backend
Programación de Servicios y Procesos - API REST con Flask

Este módulo implementa la API REST para conectar el frontend
con la base de datos del sistema de gestión de gimnasio.
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import sys

# Agregar el directorio de la base de datos al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from database.database import DatabaseManager
from database.models import Socio, Entrenador, Clase, Membresia, Asistencia, Reporte

# Crear aplicación Flask
app = Flask(__name__)
CORS(app)  # Permitir CORS para el frontend

# Inicializar base de datos
db_manager = DatabaseManager()

# Inicializar modelos
socio_model = Socio(db_manager)
entrenador_model = Entrenador(db_manager)
clase_model = Clase(db_manager)
membresia_model = Membresia(db_manager)
asistencia_model = Asistencia(db_manager)
reporte_model = Reporte(db_manager)

# Rutas para servir archivos estáticos del frontend
@app.route('/')
def index():
    """Servir la página principal"""
    frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend_path, 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    """Servir archivos estáticos del frontend (CSS, JS, imágenes)"""
    frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend_path, filename)

# ==================== API ROUTES ====================

# Rutas para Socios
@app.route('/api/socios', methods=['GET'])
def obtener_socios():
    """Obtener todos los socios"""
    try:
        socios = socio_model.obtener_todos()
        socios_dict = []
        for socio in socios:
            socios_dict.append({
                'id': socio[0],
                'numero_socio': socio[1],
                'nombre': socio[2],
                'apellidos': socio[3],
                'email': socio[4],
                'telefono': socio[5],
                'ciudad': socio[6],
                'estado': socio[7],
                'estado_membresia': socio[8]
            })
        return jsonify({
            'success': True,
            'data': socios_dict
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/socios/<int:socio_id>', methods=['GET'])
def obtener_socio(socio_id):
    """Obtener un socio específico"""
    try:
        socio = socio_model.obtener_por_id(socio_id)
        if socio:
            socio_dict = {
                'id': socio[0],
                'numero_socio': socio[1],
                'nombre': socio[2],
                'apellidos': socio[3],
                'email': socio[4],
                'telefono': socio[5],
                'fecha_nacimiento': socio[6],
                'direccion': socio[7],
                'ciudad': socio[8],
                'fecha_registro': socio[9],
                'estado': socio[10]
            }
            return jsonify({
                'success': True,
                'data': socio_dict
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Socio no encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/socios', methods=['POST'])
def crear_socio():
    """Crear un nuevo socio"""
    try:
        data = request.get_json()
        socio_id = socio_model.crear(
            numero_socio=data['numero_socio'],
            nombre=data['nombre'],
            apellidos=data['apellidos'],
            email=data.get('email'),
            telefono=data.get('telefono'),
            fecha_nacimiento=data.get('fecha_nacimiento'),
            direccion=data.get('direccion'),
            ciudad=data.get('ciudad')
        )
        return jsonify({
            'success': True,
            'data': {'id': socio_id},
            'message': 'Socio creado correctamente'
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/socios/<int:socio_id>', methods=['PUT'])
def actualizar_socio(socio_id):
    """Actualizar un socio existente"""
    try:
        data = request.get_json()
        socio_model.actualizar(socio_id, **data)
        return jsonify({
            'success': True,
            'message': 'Socio actualizado correctamente'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Rutas para Entrenadores
@app.route('/api/entrenadores', methods=['GET'])
def obtener_entrenadores():
    """Obtener todos los entrenadores"""
    try:
        entrenadores = entrenador_model.obtener_todos()
        entrenadores_dict = []
        for entrenador in entrenadores:
            entrenadores_dict.append({
                'id': entrenador[0],
                'codigo_empleado': entrenador[1],
                'nombre': entrenador[2],
                'apellidos': entrenador[3],
                'especialidad': entrenador[4],
                'telefono': entrenador[5],
                'email': entrenador[6],
                'estado': entrenador[7],
                'total_clases': entrenador[8]
            })
        return jsonify({
            'success': True,
            'data': entrenadores_dict
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/entrenadores', methods=['POST'])
def crear_entrenador():
    """Crear un nuevo entrenador"""
    try:
        data = request.get_json()
        entrenador_id = entrenador_model.crear(
            codigo_empleado=data['codigo_empleado'],
            nombre=data['nombre'],
            apellidos=data['apellidos'],
            especialidad=data['especialidad'],
            email=data.get('email'),
            telefono=data.get('telefono'),
            certificaciones=data.get('certificaciones'),
            fecha_contratacion=data.get('fecha_contratacion'),
            horario=data.get('horario')
        )
        return jsonify({
            'success': True,
            'data': {'id': entrenador_id},
            'message': 'Entrenador creado correctamente'
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Rutas para Clases
@app.route('/api/clases', methods=['GET'])
def obtener_clases():
    """Obtener todas las clases"""
    try:
        clases = clase_model.obtener_todas()
        clases_dict = []
        for clase in clases:
            plazas_disponibles = clase[6] - clase[9]
            clases_dict.append({
                'id': clase[0],
                'nombre': clase[1],
                'dia_semana': clase[2],
                'hora_inicio': clase[3],
                'duracion_minutos': clase[4],
                'entrenador': clase[5],
                'capacidad_maxima': clase[6],
                'nivel': clase[7],
                'sala': clase[8],
                'plazas_ocupadas': clase[9],
                'plazas_disponibles': plazas_disponibles
            })
        return jsonify({
            'success': True,
            'data': clases_dict
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/clases', methods=['POST'])
def crear_clase():
    """Crear una nueva clase"""
    try:
        data = request.get_json()
        clase_id = clase_model.crear(
            nombre=data['nombre'],
            descripcion=data.get('descripcion', ''),
            entrenador_id=int(data['entrenador_id']),
            capacidad_maxima=int(data.get('capacidad_maxima', 20)),
            duracion_minutos=int(data.get('duracion_minutos', 60)),
            dia_semana=data['dia_semana'],
            hora_inicio=data['hora_inicio'],
            sala=data.get('sala'),
            nivel=data.get('nivel', 'intermedio')
        )
        return jsonify({
            'success': True,
            'data': {'id': clase_id},
            'message': 'Clase creada correctamente'
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Rutas para Membresías
@app.route('/api/membresias', methods=['GET'])
def obtener_membresias():
    """Obtener todas las membresías"""
    try:
        membresias = membresia_model.obtener_todas()
        membresias_dict = []
        for membresia in membresias:
            membresias_dict.append({
                'id': membresia[0],
                'numero_socio': membresia[1],
                'socio': membresia[2],
                'tipo_membresia': membresia[3],
                'fecha_inicio': membresia[4],
                'fecha_fin': membresia[5],
                'precio_pagado': float(membresia[6]),
                'estado': membresia[7],
                'estado_vigencia': membresia[8]
            })
        return jsonify({
            'success': True,
            'data': membresias_dict
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/membresias/tipos', methods=['GET'])
def obtener_tipos_membresia():
    """Obtener tipos de membresía disponibles"""
    try:
        tipos = membresia_model.obtener_tipos_membresia()
        tipos_dict = []
        for tipo in tipos:
            tipos_dict.append({
                'id': tipo[0],
                'nombre': tipo[1],
                'descripcion': tipo[2],
                'duracion_meses': tipo[3],
                'precio': float(tipo[4]),
                'acceso_clases': bool(tipo[5]),
                'acceso_piscina': bool(tipo[6]),
                'acceso_sauna': bool(tipo[7])
            })
        return jsonify({
            'success': True,
            'data': tipos_dict
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/membresias', methods=['POST'])
def crear_membresia():
    """Crear una nueva membresía"""
    try:
        data = request.get_json()
        membresia_id = membresia_model.crear(
            socio_id=int(data['socio_id']),
            tipo_membresia_id=int(data['tipo_membresia_id']),
            fecha_inicio=data['fecha_inicio'],
            duracion_meses=int(data['duracion_meses']),
            precio_pagado=float(data['precio_pagado'])
        )
        return jsonify({
            'success': True,
            'data': {'id': membresia_id},
            'message': 'Membresía creada correctamente'
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Rutas para Asistencias
@app.route('/api/asistencias/hoy', methods=['GET'])
def obtener_asistencias_hoy():
    """Obtener asistencias del día actual"""
    try:
        asistencias = asistencia_model.obtener_asistencias_hoy()
        asistencias_dict = []
        for asistencia in asistencias:
            asistencias_dict.append({
                'id': asistencia[0],
                'numero_socio': asistencia[1],
                'socio': asistencia[2],
                'entrada': asistencia[3],
                'salida': asistencia[4]
            })
        return jsonify({
            'success': True,
            'data': asistencias_dict
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/asistencias/entrada', methods=['POST'])
def registrar_entrada():
    """Registrar entrada de un socio"""
    try:
        data = request.get_json()
        asistencia_id = asistencia_model.registrar_entrada(int(data['socio_id']))
        return jsonify({
            'success': True,
            'data': {'id': asistencia_id},
            'message': 'Entrada registrada correctamente'
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Rutas para Informes y Reportes
@app.route('/api/informes/dashboard', methods=['GET'])
def obtener_estadisticas_dashboard():
    """Obtener estadísticas para el dashboard"""
    try:
        socios = socio_model.obtener_todos()
        entrenadores = entrenador_model.obtener_todos()
        clases = clase_model.obtener_todas()
        membresias = membresia_model.obtener_todas()
        
        total_socios = len(socios)
        total_entrenadores = len(entrenadores)
        total_clases = len(clases)
        
        # Calcular ingresos del mes actual
        ingresos_mes = sum(float(m[6]) for m in membresias if m[7] == 'activa')
        
        # Contar socios con membresía activa
        socios_activos = sum(1 for s in socios if s[8] == 'Con membresía')
        
        return jsonify({
            'success': True,
            'data': {
                'total_socios': total_socios,
                'socios_activos': socios_activos,
                'total_entrenadores': total_entrenadores,
                'total_clases': total_clases,
                'ingresos_mes': ingresos_mes
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/informes/ingresos-mes', methods=['GET'])
def obtener_ingresos_por_mes():
    """Obtener reporte de ingresos por mes"""
    try:
        datos = reporte_model.ingresos_por_mes()
        reporte = []
        for item in datos:
            reporte.append({
                'mes': item[0],
                'total_membresias': item[1],
                'total_ingresos': float(item[2])
            })
        return jsonify({
            'success': True,
            'data': reporte
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/informes/membresias-vencer', methods=['GET'])
def obtener_membresias_por_vencer():
    """Obtener membresías que están por vencer"""
    try:
        membresias = reporte_model.membresias_por_vencer()
        membresias_dict = []
        for membresia in membresias:
            membresias_dict.append({
                'numero_socio': membresia[0],
                'socio': membresia[1],
                'telefono': membresia[2],
                'email': membresia[3],
                'fecha_fin': membresia[4],
                'tipo_membresia': membresia[5]
            })
        return jsonify({
            'success': True,
            'data': membresias_dict
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/informes/clases-populares', methods=['GET'])
def obtener_clases_populares():
    """Obtener clases más populares"""
    try:
        clases = reporte_model.clases_mas_populares()
        clases_dict = []
        for clase in clases:
            clases_dict.append({
                'clase': clase[0],
                'entrenador': clase[1],
                'dia_semana': clase[2],
                'hora_inicio': clase[3],
                'total_reservas': clase[4],
                'capacidad_maxima': clase[5],
                'porcentaje_ocupacion': float(clase[6])
            })
        return jsonify({
            'success': True,
            'data': clases_dict
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/informes/asistencias-mensuales', methods=['GET'])
def obtener_asistencias_mensuales():
    """Obtener estadísticas de asistencias mensuales"""
    try:
        datos = reporte_model.asistencias_mensuales()
        reporte = []
        for item in datos:
            reporte.append({
                'mes': item[0],
                'socios_unicos': item[1],
                'total_visitas': item[2],
                'promedio_visitas': float(item[3])
            })
        return jsonify({
            'success': True,
            'data': reporte
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Ruta de estado del sistema
@app.route('/api/status', methods=['GET'])
def estado_sistema():
    """Verificar el estado del sistema"""
    try:
        # Verificar conexión a la base de datos
        conn = db_manager.get_connection()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Sistema de Gestión de Gimnasio funcionando correctamente',
            'version': '1.0.0'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Manejo de errores
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Recurso no encontrado'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Error interno del servidor'
    }), 500

if __name__ == '__main__':
    print("🏋️ Iniciando Sistema de Gestión de Gimnasio...")
    print("📊 Base de datos SQLite inicializada")
    print("🌐 Servidor disponible en: http://localhost:5000")
    print("📱 API REST disponible en: http://localhost:5000/api/")
    print("\n📋 Endpoints disponibles:")
    print("  👥 Socios:")
    print("     - GET  /api/socios")
    print("     - POST /api/socios")
    print("  💪 Entrenadores:")
    print("     - GET  /api/entrenadores")
    print("     - POST /api/entrenadores")
    print("  📅 Clases:")
    print("     - GET  /api/clases")
    print("     - POST /api/clases")
    print("  💳 Membresías:")
    print("     - GET  /api/membresias")
    print("     - GET  /api/membresias/tipos")
    print("     - POST /api/membresias")
    print("  📊 Informes:")
    print("     - GET  /api/informes/dashboard")
    print("     - GET  /api/informes/ingresos-mes")
    print("     - GET  /api/informes/membresias-vencer")
    print("     - GET  /api/status")
    
    app.run(debug=True, host='0.0.0.0', port=5000)