"""
Sistema ERP-CRM - Modelos de Datos
Módulo de Acceso a Datos

Clases para gestionar operaciones CRUD de cada entidad
"""

from database.database import DatabaseManager
from datetime import datetime

class Cliente:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def crear(self, nombre, apellidos, email=None, telefono=None, direccion=None, ciudad=None, codigo_postal=None):
        """Crea un nuevo cliente"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO clientes (nombre, apellidos, email, telefono, direccion, ciudad, codigo_postal)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, apellidos, email, telefono, direccion, ciudad, codigo_postal))
        
        cliente_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return cliente_id
    
    def obtener_todos(self):
        """Obtiene todos los clientes"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, nombre, apellidos, email, telefono, ciudad, estado
            FROM clientes
            ORDER BY fecha_registro DESC
        ''')
        
        clientes = cursor.fetchall()
        conn.close()
        return clientes
    
    def obtener_por_id(self, cliente_id):
        """Obtiene un cliente por ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM clientes WHERE id = ?', (cliente_id,))
        cliente = cursor.fetchone()
        conn.close()
        return cliente
    
    def actualizar(self, cliente_id, **kwargs):
        """Actualiza datos de un cliente"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        campos = []
        valores = []
        for campo, valor in kwargs.items():
            campos.append(f"{campo} = ?")
            valores.append(valor)
        
        valores.append(cliente_id)
        query = f"UPDATE clientes SET {', '.join(campos)} WHERE id = ?"
        
        cursor.execute(query, valores)
        conn.commit()
        conn.close()


class Producto:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def crear(self, codigo, nombre, descripcion, categoria, precio, stock=0, stock_minimo=5):
        """Crea un nuevo producto"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO productos (codigo, nombre, descripcion, categoria, precio, stock, stock_minimo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (codigo, nombre, descripcion, categoria, precio, stock, stock_minimo))
        
        producto_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return producto_id
    
    def obtener_todos(self):
        """Obtiene todos los productos"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, codigo, nombre, categoria, precio, stock, stock_minimo,
                   CASE WHEN stock <= stock_minimo THEN 'Bajo' ELSE 'OK' END as estado_stock
            FROM productos
            WHERE activo = 1
            ORDER BY nombre
        ''')
        
        productos = cursor.fetchall()
        conn.close()
        return productos
    
    def obtener_por_id(self, producto_id):
        """Obtiene un producto por ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM productos WHERE id = ?', (producto_id,))
        producto = cursor.fetchone()
        conn.close()
        return producto
    
    def actualizar_stock(self, producto_id, cantidad):
        """Actualiza el stock de un producto"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE productos SET stock = stock + ? WHERE id = ?', (cantidad, producto_id))
        conn.commit()
        conn.close()


class Venta:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def crear(self, cliente_id, usuario_id, items):
        """
        Crea una nueva venta
        items: lista de diccionarios con producto_id, cantidad, precio_unitario
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Calcular total
        total = sum(item['cantidad'] * item['precio_unitario'] for item in items)
        
        # Crear la venta
        cursor.execute('''
            INSERT INTO ventas (cliente_id, usuario_id, total)
            VALUES (?, ?, ?)
        ''', (cliente_id, usuario_id, total))
        
        venta_id = cursor.lastrowid
        
        # Agregar detalles de la venta
        for item in items:
            subtotal = item['cantidad'] * item['precio_unitario']
            cursor.execute('''
                INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario, subtotal)
                VALUES (?, ?, ?, ?, ?)
            ''', (venta_id, item['producto_id'], item['cantidad'], item['precio_unitario'], subtotal))
            
            # Actualizar stock del producto
            cursor.execute('UPDATE productos SET stock = stock - ? WHERE id = ?', 
                         (item['cantidad'], item['producto_id']))
        
        conn.commit()
        conn.close()
        return venta_id
    
    def obtener_todas(self):
        """Obtiene todas las ventas con información del cliente"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT v.id, c.nombre, c.apellidos, v.fecha, v.total, v.estado
            FROM ventas v
            JOIN clientes c ON v.cliente_id = c.id
            ORDER BY v.fecha DESC
        ''')
        
        ventas = cursor.fetchall()
        conn.close()
        return ventas
    
    def obtener_detalle(self, venta_id):
        """Obtiene el detalle de una venta específica"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.nombre, dv.cantidad, dv.precio_unitario, dv.subtotal
            FROM detalle_ventas dv
            JOIN productos p ON dv.producto_id = p.id
            WHERE dv.venta_id = ?
        ''', (venta_id,))
        
        detalle = cursor.fetchall()
        conn.close()
        return detalle


class Reporte:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def ventas_por_mes(self):
        """Reporte de ventas por mes"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                strftime('%Y-%m', fecha) as mes,
                COUNT(*) as total_ventas,
                SUM(total) as total_ingresos
            FROM ventas
            GROUP BY strftime('%Y-%m', fecha)
            ORDER BY mes DESC
            LIMIT 12
        ''')
        
        datos = cursor.fetchall()
        conn.close()
        return datos
    
    def productos_bajo_stock(self):
        """Productos con stock bajo"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT codigo, nombre, stock, stock_minimo
            FROM productos
            WHERE stock <= stock_minimo AND activo = 1
            ORDER BY stock ASC
        ''')
        
        productos = cursor.fetchall()
        conn.close()
        return productos
    
    def top_clientes(self):
        """Top 10 clientes por volumen de compras"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                c.nombre, c.apellidos,
                COUNT(v.id) as total_compras,
                SUM(v.total) as total_gastado
            FROM clientes c
            JOIN ventas v ON c.id = v.cliente_id
            GROUP BY c.id
            ORDER BY total_gastado DESC
            LIMIT 10
        ''')
        
        clientes = cursor.fetchall()
        conn.close()
        return clientes