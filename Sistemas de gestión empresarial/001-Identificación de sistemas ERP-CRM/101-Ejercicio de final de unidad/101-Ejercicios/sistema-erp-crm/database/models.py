"""
Sistema de Gestión de Gimnasio - Modelos de Datos
Módulo de Acceso a Datos

Clases para gestionar operaciones CRUD de cada entidad
"""

from database.database import DatabaseManager
from datetime import datetime, timedelta

class Socio:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def crear(self, numero_socio, nombre, apellidos, email=None, telefono=None, 
              fecha_nacimiento=None, direccion=None, ciudad=None):
        """Crea un nuevo socio"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO socios (numero_socio, nombre, apellidos, email, telefono, 
                               fecha_nacimiento, direccion, ciudad)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (numero_socio, nombre, apellidos, email, telefono, fecha_nacimiento, direccion, ciudad))
        
        socio_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return socio_id
    
    def obtener_todos(self):
        """Obtiene todos los socios"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT s.id, s.numero_socio, s.nombre, s.apellidos, s.email, s.telefono, 
                   s.ciudad, s.estado,
                   CASE 
                       WHEN m.fecha_fin >= date('now') THEN 'Con membresía'
                       ELSE 'Sin membresía'
                   END as estado_membresia
            FROM socios s
            LEFT JOIN membresias m ON s.id = m.socio_id AND m.estado = 'activa'
            ORDER BY s.fecha_registro DESC
        ''')
        
        socios = cursor.fetchall()
        conn.close()
        return socios
    
    def obtener_por_id(self, socio_id):
        """Obtiene un socio por ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM socios WHERE id = ?', (socio_id,))
        socio = cursor.fetchone()
        conn.close()
        return socio
    
    def actualizar(self, socio_id, **kwargs):
        """Actualiza datos de un socio"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        campos = []
        valores = []
        for campo, valor in kwargs.items():
            campos.append(f"{campo} = ?")
            valores.append(valor)
        
        valores.append(socio_id)
        query = f"UPDATE socios SET {', '.join(campos)} WHERE id = ?"
        
        cursor.execute(query, valores)
        conn.commit()
        conn.close()


class Entrenador:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def crear(self, codigo_empleado, nombre, apellidos, especialidad, email=None, 
              telefono=None, certificaciones=None, fecha_contratacion=None, horario=None):
        """Crea un nuevo entrenador"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO entrenadores (codigo_empleado, nombre, apellidos, email, telefono,
                                    especialidad, certificaciones, fecha_contratacion, horario)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (codigo_empleado, nombre, apellidos, email, telefono, especialidad, 
              certificaciones, fecha_contratacion, horario))
        
        entrenador_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return entrenador_id
    
    def obtener_todos(self):
        """Obtiene todos los entrenadores"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT e.id, e.codigo_empleado, e.nombre, e.apellidos, e.especialidad, 
                   e.telefono, e.email, e.estado,
                   COUNT(c.id) as total_clases
            FROM entrenadores e
            LEFT JOIN clases c ON e.id = c.entrenador_id AND c.activa = 1
            WHERE e.estado = 'activo'
            GROUP BY e.id
            ORDER BY e.nombre
        ''')
        
        entrenadores = cursor.fetchall()
        conn.close()
        return entrenadores
    
    def obtener_por_id(self, entrenador_id):
        """Obtiene un entrenador por ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM entrenadores WHERE id = ?', (entrenador_id,))
        entrenador = cursor.fetchone()
        conn.close()
        return entrenador


class Clase:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def crear(self, nombre, descripcion, entrenador_id, capacidad_maxima=20, 
              duracion_minutos=60, dia_semana=None, hora_inicio=None, sala=None, nivel='intermedio'):
        """Crea una nueva clase grupal"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO clases (nombre, descripcion, entrenador_id, capacidad_maxima,
                              duracion_minutos, dia_semana, hora_inicio, sala, nivel)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, descripcion, entrenador_id, capacidad_maxima, duracion_minutos,
              dia_semana, hora_inicio, sala, nivel))
        
        clase_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return clase_id
    
    def obtener_todas(self):
        """Obtiene todas las clases"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.id, c.nombre, c.dia_semana, c.hora_inicio, c.duracion_minutos,
                   e.nombre || ' ' || e.apellidos as entrenador,
                   c.capacidad_maxima, c.nivel, c.sala,
                   COUNT(r.id) as plazas_ocupadas
            FROM clases c
            LEFT JOIN entrenadores e ON c.entrenador_id = e.id
            LEFT JOIN reservas_clases r ON c.id = r.clase_id AND r.estado = 'confirmada'
            WHERE c.activa = 1
            GROUP BY c.id
            ORDER BY c.dia_semana, c.hora_inicio
        ''')
        
        clases = cursor.fetchall()
        conn.close()
        return clases
    
    def obtener_por_id(self, clase_id):
        """Obtiene una clase por ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM clases WHERE id = ?', (clase_id,))
        clase = cursor.fetchone()
        conn.close()
        return clase


class Membresia:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def crear(self, socio_id, tipo_membresia_id, fecha_inicio, duracion_meses, precio_pagado):
        """Crea una nueva membresía"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Calcular fecha de fin
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = fecha_inicio_dt + timedelta(days=duracion_meses * 30)
        fecha_fin = fecha_fin_dt.strftime('%Y-%m-%d')
        
        cursor.execute('''
            INSERT INTO membresias (socio_id, tipo_membresia_id, fecha_inicio, 
                                  fecha_fin, precio_pagado)
            VALUES (?, ?, ?, ?, ?)
        ''', (socio_id, tipo_membresia_id, fecha_inicio, fecha_fin, precio_pagado))
        
        membresia_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return membresia_id
    
    def obtener_todas(self):
        """Obtiene todas las membresías"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT m.id, s.numero_socio, s.nombre || ' ' || s.apellidos as socio,
                   tm.nombre as tipo_membresia, m.fecha_inicio, m.fecha_fin,
                   m.precio_pagado, m.estado,
                   CASE 
                       WHEN m.fecha_fin >= date('now') THEN 'Vigente'
                       ELSE 'Vencida'
                   END as estado_vigencia
            FROM membresias m
            JOIN socios s ON m.socio_id = s.id
            JOIN tipos_membresia tm ON m.tipo_membresia_id = tm.id
            ORDER BY m.fecha_pago DESC
        ''')
        
        membresias = cursor.fetchall()
        conn.close()
        return membresias
    
    def obtener_tipos_membresia(self):
        """Obtiene todos los tipos de membresía disponibles"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, nombre, descripcion, duracion_meses, precio,
                   acceso_clases, acceso_piscina, acceso_sauna
            FROM tipos_membresia
            WHERE activo = 1
            ORDER BY precio
        ''')
        
        tipos = cursor.fetchall()
        conn.close()
        return tipos


class Asistencia:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def registrar_entrada(self, socio_id):
        """Registra la entrada de un socio al gimnasio"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO asistencias (socio_id, fecha_hora_entrada)
            VALUES (?, ?)
        ''', (socio_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
        asistencia_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return asistencia_id
    
    def registrar_salida(self, asistencia_id):
        """Registra la salida de un socio del gimnasio"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE asistencias 
            SET fecha_hora_salida = ?
            WHERE id = ?
        ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), asistencia_id))
        
        conn.commit()
        conn.close()
    
    def obtener_asistencias_hoy(self):
        """Obtiene las asistencias del día actual"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.id, s.numero_socio, s.nombre || ' ' || s.apellidos as socio,
                   a.fecha_hora_entrada, a.fecha_hora_salida
            FROM asistencias a
            JOIN socios s ON a.socio_id = s.id
            WHERE date(a.fecha_hora_entrada) = date('now')
            ORDER BY a.fecha_hora_entrada DESC
        ''')
        
        asistencias = cursor.fetchall()
        conn.close()
        return asistencias


class Reporte:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def ingresos_por_mes(self):
        """Reporte de ingresos por membresías por mes"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                strftime('%Y-%m', fecha_pago) as mes,
                COUNT(*) as total_membresias,
                SUM(precio_pagado) as total_ingresos
            FROM membresias
            GROUP BY strftime('%Y-%m', fecha_pago)
            ORDER BY mes DESC
            LIMIT 12
        ''')
        
        datos = cursor.fetchall()
        conn.close()
        return datos
    
    def membresias_por_vencer(self):
        """Membresías que vencen en los próximos 7 días"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT s.numero_socio, s.nombre || ' ' || s.apellidos as socio,
                   s.telefono, s.email, m.fecha_fin,
                   tm.nombre as tipo_membresia
            FROM membresias m
            JOIN socios s ON m.socio_id = s.id
            JOIN tipos_membresia tm ON m.tipo_membresia_id = tm.id
            WHERE m.estado = 'activa' 
            AND m.fecha_fin BETWEEN date('now') AND date('now', '+7 days')
            ORDER BY m.fecha_fin ASC
        ''')
        
        membresias = cursor.fetchall()
        conn.close()
        return membresias
    
    def clases_mas_populares(self):
        """Top clases más reservadas"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                c.nombre as clase,
                e.nombre || ' ' || e.apellidos as entrenador,
                c.dia_semana, c.hora_inicio,
                COUNT(r.id) as total_reservas,
                c.capacidad_maxima,
                ROUND(COUNT(r.id) * 100.0 / c.capacidad_maxima, 1) as porcentaje_ocupacion
            FROM clases c
            LEFT JOIN entrenadores e ON c.entrenador_id = e.id
            LEFT JOIN reservas_clases r ON c.id = r.clase_id AND r.estado = 'confirmada'
            WHERE c.activa = 1
            GROUP BY c.id
            ORDER BY total_reservas DESC
            LIMIT 10
        ''')
        
        clases = cursor.fetchall()
        conn.close()
        return clases
    
    def asistencias_mensuales(self):
        """Estadísticas de asistencias mensuales"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                strftime('%Y-%m', fecha_hora_entrada) as mes,
                COUNT(DISTINCT socio_id) as socios_unicos,
                COUNT(*) as total_visitas,
                ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT socio_id), 1) as promedio_visitas
            FROM asistencias
            GROUP BY strftime('%Y-%m', fecha_hora_entrada)
            ORDER BY mes DESC
            LIMIT 6
        ''')
        
        datos = cursor.fetchall()
        conn.close()
        return datos