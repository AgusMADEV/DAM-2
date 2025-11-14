"""
Sistema de Gestión de Gimnasio - Modelo de Base de Datos
Módulo de Acceso a Datos

Este archivo contiene la definición de la base de datos SQLite
con tablas para socios, entrenadores, clases, membresías y asistencias.
"""

import sqlite3
import hashlib
from datetime import datetime, timedelta
import os

class DatabaseManager:
    def __init__(self, db_path="gimnasio.db"):
        """Inicializa el gestor de base de datos"""
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Obtiene una conexión a la base de datos"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Crea las tablas si no existen"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla de usuarios del sistema (administradores, recepcionistas)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                rol TEXT DEFAULT 'recepcionista',
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de socios (miembros del gimnasio)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS socios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_socio TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                apellidos TEXT NOT NULL,
                email TEXT UNIQUE,
                telefono TEXT,
                fecha_nacimiento DATE,
                direccion TEXT,
                ciudad TEXT,
                fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
                estado TEXT DEFAULT 'activo',
                foto TEXT
            )
        ''')
        
        # Tabla de entrenadores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entrenadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo_empleado TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                apellidos TEXT NOT NULL,
                email TEXT UNIQUE,
                telefono TEXT,
                especialidad TEXT,
                certificaciones TEXT,
                fecha_contratacion DATE,
                horario TEXT,
                estado TEXT DEFAULT 'activo',
                foto TEXT
            )
        ''')
        
        # Tabla de tipos de membresía
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tipos_membresia (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                duracion_meses INTEGER NOT NULL,
                precio DECIMAL(10,2) NOT NULL,
                acceso_clases BOOLEAN DEFAULT 1,
                acceso_piscina BOOLEAN DEFAULT 0,
                acceso_sauna BOOLEAN DEFAULT 0,
                activo BOOLEAN DEFAULT 1
            )
        ''')
        
        # Tabla de membresías de socios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS membresias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                socio_id INTEGER,
                tipo_membresia_id INTEGER,
                fecha_inicio DATE NOT NULL,
                fecha_fin DATE NOT NULL,
                precio_pagado DECIMAL(10,2) NOT NULL,
                estado TEXT DEFAULT 'activa',
                fecha_pago DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (socio_id) REFERENCES socios(id),
                FOREIGN KEY (tipo_membresia_id) REFERENCES tipos_membresia(id)
            )
        ''')
        
        # Tabla de clases grupales
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                entrenador_id INTEGER,
                capacidad_maxima INTEGER DEFAULT 20,
                duracion_minutos INTEGER DEFAULT 60,
                dia_semana TEXT,
                hora_inicio TIME,
                sala TEXT,
                nivel TEXT DEFAULT 'intermedio',
                activa BOOLEAN DEFAULT 1,
                FOREIGN KEY (entrenador_id) REFERENCES entrenadores(id)
            )
        ''')
        
        # Tabla de reservas de clases
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservas_clases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                clase_id INTEGER,
                socio_id INTEGER,
                fecha_clase DATE NOT NULL,
                fecha_reserva DATETIME DEFAULT CURRENT_TIMESTAMP,
                estado TEXT DEFAULT 'confirmada',
                FOREIGN KEY (clase_id) REFERENCES clases(id),
                FOREIGN KEY (socio_id) REFERENCES socios(id)
            )
        ''')
        
        # Tabla de asistencias al gimnasio
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS asistencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                socio_id INTEGER,
                fecha_hora_entrada DATETIME DEFAULT CURRENT_TIMESTAMP,
                fecha_hora_salida DATETIME,
                FOREIGN KEY (socio_id) REFERENCES socios(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Insertar datos iniciales
        self.insert_initial_data()
    
    def insert_initial_data(self):
        """Inserta datos iniciales para testing"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Verificar si ya existen datos (para evitar duplicados)
        cursor.execute("SELECT COUNT(*) FROM socios")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return  # Ya hay datos, no insertar de nuevo
        
        # Usuario administrador por defecto
        admin_password = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute('''
            INSERT OR IGNORE INTO usuarios (nombre, email, password_hash, rol)
            VALUES (?, ?, ?, ?)
        ''', ("Administrador", "admin@gimnasio.com", admin_password, "administrador"))
        
        # Tipos de membresía de ejemplo
        tipos_membresia_ejemplo = [
            ("Básica Mensual", "Acceso básico al gimnasio", 1, 35.00, 0, 0, 0),
            ("Estándar Mensual", "Acceso al gimnasio y clases grupales", 1, 45.00, 1, 0, 0),
            ("Premium Mensual", "Acceso completo: gimnasio, clases, piscina y sauna", 1, 65.00, 1, 1, 1),
            ("Básica Trimestral", "Acceso básico al gimnasio por 3 meses", 3, 95.00, 0, 0, 0),
            ("Estándar Anual", "Acceso al gimnasio y clases por 12 meses", 12, 480.00, 1, 0, 0),
        ]
        
        for membresia in tipos_membresia_ejemplo:
            cursor.execute('''
                INSERT OR IGNORE INTO tipos_membresia 
                (nombre, descripcion, duracion_meses, precio, acceso_clases, acceso_piscina, acceso_sauna)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', membresia)
        
        # Entrenadores de ejemplo
        entrenadores_ejemplo = [
            ("ENT001", "Carlos", "Pérez Fitness", "carlos.perez@gimnasio.com", "666123456", 
             "Musculación y Fuerza", "Personal Trainer NSCA, Nutrición Deportiva", "2020-01-15", "L-V 9:00-17:00"),
            ("ENT002", "María", "González Active", "maria.gonzalez@gimnasio.com", "677234567", 
             "Yoga y Pilates", "Instructora de Yoga RYT-200, Pilates Mat", "2021-03-10", "L-S 10:00-14:00"),
            ("ENT003", "David", "Martínez Cardio", "david.martinez@gimnasio.com", "688345678", 
             "Spinning y Cardio", "Instructor de Spinning, HIIT Certified", "2019-06-20", "L-V 7:00-15:00"),
        ]
        
        for entrenador in entrenadores_ejemplo:
            cursor.execute('''
                INSERT OR IGNORE INTO entrenadores 
                (codigo_empleado, nombre, apellidos, email, telefono, especialidad, certificaciones, fecha_contratacion, horario)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', entrenador)
        
        # Socios de ejemplo
        socios_ejemplo = [
            ("SOC001", "Juan", "López García", "juan.lopez@email.com", "666987654", "1990-05-15", "Calle Mayor 123", "Madrid"),
            ("SOC002", "Ana", "Martínez Ruiz", "ana.martinez@email.com", "677876543", "1985-08-22", "Av. Libertad 45", "Madrid"),
            ("SOC003", "Pedro", "Sánchez Villa", "pedro.sanchez@email.com", "688765432", "1995-12-10", "Plaza España 7", "Madrid"),
            ("SOC004", "Laura", "Fernández Costa", "laura.fernandez@email.com", "699654321", "1992-03-18", "Calle Sol 56", "Madrid"),
        ]
        
        for socio in socios_ejemplo:
            cursor.execute('''
                INSERT OR IGNORE INTO socios 
                (numero_socio, nombre, apellidos, email, telefono, fecha_nacimiento, direccion, ciudad)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', socio)
        
        # Clases grupales de ejemplo
        clases_ejemplo = [
            ("Spinning Intenso", "Clase de ciclismo indoor de alta intensidad", 3, 25, 45, "Lunes", "09:00", "Sala 1", "avanzado"),
            ("Yoga Flow", "Clase de yoga dinámico para todos los niveles", 2, 20, 60, "Martes", "10:00", "Sala 2", "intermedio"),
            ("HIIT Training", "Entrenamiento interválico de alta intensidad", 1, 15, 45, "Miércoles", "19:00", "Sala 1", "intermedio"),
            ("Pilates Mat", "Pilates en colchoneta, fortalecimiento del core", 2, 18, 60, "Jueves", "11:00", "Sala 2", "principiante"),
            ("Zumba", "Fitness con ritmos latinos", 1, 30, 60, "Viernes", "20:00", "Sala 3", "principiante"),
        ]
        
        for clase in clases_ejemplo:
            cursor.execute('''
                INSERT OR IGNORE INTO clases 
                (nombre, descripcion, entrenador_id, capacidad_maxima, duracion_minutos, dia_semana, hora_inicio, sala, nivel)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', clase)
        
        # Membresías activas de ejemplo
        fecha_hoy = datetime.now()
        membresias_ejemplo = [
            (1, 2, fecha_hoy.strftime('%Y-%m-%d'), (fecha_hoy + timedelta(days=30)).strftime('%Y-%m-%d'), 45.00),
            (2, 3, fecha_hoy.strftime('%Y-%m-%d'), (fecha_hoy + timedelta(days=30)).strftime('%Y-%m-%d'), 65.00),
            (3, 1, fecha_hoy.strftime('%Y-%m-%d'), (fecha_hoy + timedelta(days=30)).strftime('%Y-%m-%d'), 35.00),
        ]
        
        for membresia in membresias_ejemplo:
            cursor.execute('''
                INSERT OR IGNORE INTO membresias 
                (socio_id, tipo_membresia_id, fecha_inicio, fecha_fin, precio_pagado)
                VALUES (?, ?, ?, ?, ?)
            ''', membresia)
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Genera hash SHA256 de la contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verificar_usuario(self, email, password):
        """Verifica las credenciales de un usuario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        cursor.execute('''
            SELECT id, nombre, rol FROM usuarios 
            WHERE email = ? AND password_hash = ?
        ''', (email, password_hash))
        
        usuario = cursor.fetchone()
        conn.close()
        return usuario

if __name__ == "__main__":
    # Inicializar base de datos
    db = DatabaseManager()
    print("✅ Base de datos del gimnasio inicializada correctamente")
    print("👤 Usuario admin creado: admin@gimnasio.com / admin123")
    print("💪 Datos de ejemplo cargados: socios, entrenadores, clases y membresías")