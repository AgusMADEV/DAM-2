"""
Sistema ERP-CRM - Modelo de Base de Datos
Módulo de Acceso a Datos

Este archivo contiene la definición de la base de datos SQLite
con tablas para clientes, productos, ventas y usuarios.
"""

import sqlite3
import hashlib
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self, db_path="empresa.db"):
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
        
        # Tabla de usuarios del sistema
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                rol TEXT DEFAULT 'empleado',
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de clientes (CRM)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellidos TEXT NOT NULL,
                email TEXT UNIQUE,
                telefono TEXT,
                direccion TEXT,
                ciudad TEXT,
                codigo_postal TEXT,
                fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
                estado TEXT DEFAULT 'activo'
            )
        ''')
        
        # Tabla de productos (ERP)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                categoria TEXT,
                precio DECIMAL(10,2) NOT NULL,
                stock INTEGER DEFAULT 0,
                stock_minimo INTEGER DEFAULT 5,
                activo BOOLEAN DEFAULT 1,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de ventas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER,
                usuario_id INTEGER,
                fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
                total DECIMAL(10,2) NOT NULL,
                estado TEXT DEFAULT 'pendiente',
                FOREIGN KEY (cliente_id) REFERENCES clientes(id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')
        
        # Tabla de detalle de ventas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detalle_ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venta_id INTEGER,
                producto_id INTEGER,
                cantidad INTEGER NOT NULL,
                precio_unitario DECIMAL(10,2) NOT NULL,
                subtotal DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (venta_id) REFERENCES ventas(id),
                FOREIGN KEY (producto_id) REFERENCES productos(id)
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
        
        # Usuario administrador por defecto
        admin_password = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute('''
            INSERT OR IGNORE INTO usuarios (nombre, email, password_hash, rol)
            VALUES (?, ?, ?, ?)
        ''', ("Administrador", "admin@empresa.com", admin_password, "administrador"))
        
        # Productos de ejemplo
        productos_ejemplo = [
            ("PROD001", "Ordenador Portátil", "Laptop Dell Inspiron 15", "Tecnología", 699.99, 10, 2),
            ("PROD002", "Mouse Inalámbrico", "Mouse óptico Logitech", "Periféricos", 29.99, 50, 5),
            ("PROD003", "Teclado Mecánico", "Teclado gaming RGB", "Periféricos", 89.99, 25, 3),
            ("PROD004", "Monitor 24''", "Monitor Full HD Samsung", "Tecnología", 179.99, 15, 2),
        ]
        
        for producto in productos_ejemplo:
            cursor.execute('''
                INSERT OR IGNORE INTO productos 
                (codigo, nombre, descripcion, categoria, precio, stock, stock_minimo)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', producto)
        
        # Clientes de ejemplo
        clientes_ejemplo = [
            ("Juan", "Pérez García", "juan.perez@email.com", "666123456", "Calle Mayor 123", "Madrid", "28001"),
            ("María", "González López", "maria.gonzalez@email.com", "677234567", "Av. Libertad 45", "Barcelona", "08001"),
            ("Carlos", "Ruiz Martín", "carlos.ruiz@email.com", "688345678", "Plaza España 7", "Sevilla", "41001"),
        ]
        
        for cliente in clientes_ejemplo:
            cursor.execute('''
                INSERT OR IGNORE INTO clientes 
                (nombre, apellidos, email, telefono, direccion, ciudad, codigo_postal)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', cliente)
        
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
    print("✅ Base de datos inicializada correctamente")
    print("👤 Usuario admin creado: admin@empresa.com / admin123")