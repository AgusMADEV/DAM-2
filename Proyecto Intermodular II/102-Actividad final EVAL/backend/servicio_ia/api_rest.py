"""
API REST para gestión de datos - ERP Inteligente
Endpoints CRUD para Productos, Ventas, Clientes, Inventario
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

# Configuración de BD
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'erp_inteligente',
    'charset': 'utf8mb4'
}

def get_db_connection():
    try:
        return pymysql.connect(**DB_CONFIG)
    except Exception as e:
        print(f"[ERROR] Conexión BD: {e}")
        return None

# ============================================
# PRODUCTOS
# ============================================

@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    try:
        conexion = get_db_connection()
        if not conexion:
            return jsonify({'success': False, 'error': 'Error de conexión a BD'}), 500
        
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute('''
            SELECT p.*, c.nombre as categoria_nombre
            FROM productos p
            LEFT JOIN categorias_productos c ON p.categoria_id = c.id
            WHERE p.activo = TRUE
            ORDER BY p.nombre
        ''')
        
        productos = cursor.fetchall()
        conexion.close()
        
        return jsonify({'success': True, 'data': productos})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    try:
        conexion = get_db_connection()
        if not conexion:
            return jsonify({'success': False, 'error': 'Error de conexión a BD'}), 500
        
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM productos WHERE id = %s', (id,))
        producto = cursor.fetchone()
        conexion.close()
        
        if producto:
            return jsonify({'success': True, 'data': producto})
        else:
            return jsonify({'success': False, 'error': 'Producto no encontrado'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================
# VENTAS
# ============================================

@app.route('/api/ventas', methods=['GET'])
def obtener_ventas():
    try:
        conexion = get_db_connection()
        if not conexion:
            return jsonify({'success': False, 'error': 'Error de conexión a BD'}), 500
        
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute('''
            SELECT 
                v.*,
                c.nombre as cliente_nombre,
                u.nombre as usuario_nombre
            FROM ventas v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            LEFT JOIN usuarios u ON v.usuario_id = u.id
            ORDER BY v.fecha DESC
            LIMIT 100
        ''')
        
        ventas = cursor.fetchall()
        conexion.close()
        
        return jsonify({'success': True, 'data': ventas})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/ventas/<int:id>/lineas', methods=['GET'])
def obtener_lineas_venta(id):
    try:
        conexion = get_db_connection()
        if not conexion:
            return jsonify({'success': False, 'error': 'Error de conexión a BD'}), 500
        
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute('''
            SELECT 
                lv.*,
                p.nombre as producto_nombre,
                p.codigo as producto_codigo
            FROM lineas_venta lv
            LEFT JOIN productos p ON lv.producto_id = p.id
            WHERE lv.venta_id = %s
        ''', (id,))
        
        lineas = cursor.fetchall()
        conexion.close()
        
        return jsonify({'success': True, 'data': lineas})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================
# CLIENTES
# ============================================

@app.route('/api/clientes', methods=['GET'])
def obtener_clientes():
    try:
        conexion = get_db_connection()
        if not conexion:
            return jsonify({'success': False, 'error': 'Error de conexión a BD'}), 500
        
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute('''
            SELECT 
                c.*,
                COUNT(DISTINCT v.id) as num_ventas,
                COALESCE(SUM(v.total), 0) as total_facturado
            FROM clientes c
            LEFT JOIN ventas v ON c.id = v.cliente_id
            WHERE c.activo = TRUE
            GROUP BY c.id
            ORDER BY total_facturado DESC
        ''')
        
        clientes = cursor.fetchall()
        conexion.close()
        
        return jsonify({'success': True, 'data': clientes})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/clientes/<int:id>', methods=['GET'])
def obtener_cliente(id):
    try:
        conexion = get_db_connection()
        if not conexion:
            return jsonify({'success': False, 'error': 'Error de conexión a BD'}), 500
        
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM clientes WHERE id = %s', (id,))
        cliente = cursor.fetchone()
        conexion.close()
        
        if cliente:
            return jsonify({'success': True, 'data': cliente})
        else:
            return jsonify({'success': False, 'error': 'Cliente no encontrado'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================
# INVENTARIO (ALERTAS DE STOCK)
# ============================================

@app.route('/api/inventario', methods=['GET'])
def obtener_inventario():
    try:
        conexion = get_db_connection()
        if not conexion:
            return jsonify({'success': False, 'error': 'Error de conexión a BD'}), 500
        
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute('''
            SELECT 
                p.*,
                c.nombre as categoria_nombre,
                CASE 
                    WHEN p.stock_actual < p.stock_minimo * 0.3 THEN 'critico'
                    WHEN p.stock_actual < p.stock_minimo THEN 'bajo'
                    WHEN p.stock_actual > p.stock_maximo THEN 'exceso'
                    ELSE 'normal'
                END as estado_stock
            FROM productos p
            LEFT JOIN categorias_productos c ON p.categoria_id = c.id
            WHERE p.activo = TRUE
            ORDER BY 
                CASE 
                    WHEN p.stock_actual < p.stock_minimo * 0.3 THEN 1
                    WHEN p.stock_actual < p.stock_minimo THEN 2
                    WHEN p.stock_actual > p.stock_maximo THEN 3
                    ELSE 4
                END,
                p.nombre
        ''')
        
        inventario = cursor.fetchall()
        conexion.close()
        
        return jsonify({'success': True, 'data': inventario})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/inventario/alertas', methods=['GET'])
def obtener_alertas_inventario():
    try:
        conexion = get_db_connection()
        if not conexion:
            return jsonify({'success': False, 'error': 'Error de conexión a BD'}), 500
        
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute('''
            SELECT * FROM alertas 
            WHERE tipo = 'stock_bajo' AND activa = TRUE
            ORDER BY 
                CASE severidad
                    WHEN 'critica' THEN 1
                    WHEN 'alta' THEN 2
                    WHEN 'media' THEN 3
                    ELSE 4
                END,
                fecha_creacion DESC
        ''')
        
        alertas = cursor.fetchall()
        conexion.close()
        
        return jsonify({'success': True, 'data': alertas})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================
# CATEGORÍAS
# ============================================

@app.route('/api/categorias', methods=['GET'])
def obtener_categorias():
    try:
        conexion = get_db_connection()
        if not conexion:
            return jsonify({'success': False, 'error': 'Error de conexión a BD'}), 500
        
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM categorias_productos WHERE activa = TRUE ORDER BY nombre')
        categorias = cursor.fetchall()
        conexion.close()
        
        return jsonify({'success': True, 'data': categorias})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================
# ESTADÍSTICAS
# ============================================

@app.route('/api/estadisticas/ventas-mes', methods=['GET'])
def obtener_ventas_por_mes():
    """Ventas totales por mes (últimos 12 meses)"""
    try:
        conexion = get_db_connection()
        if not conexion:
            return jsonify({'success': False, 'error': 'Error de conexión a BD'}), 500
        
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT 
                DATE_FORMAT(fecha, '%Y-%m') as mes,
                DATE_FORMAT(fecha, '%b %Y') as mes_nombre,
                COUNT(*) as total_ventas,
                SUM(total) as total_facturado
            FROM ventas
            WHERE fecha >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
            GROUP BY DATE_FORMAT(fecha, '%Y-%m'), DATE_FORMAT(fecha, '%b %Y')
            ORDER BY mes ASC
        """)
        
        datos = cursor.fetchall()
        conexion.close()
        
        return jsonify({'success': True, 'data': datos})
        
    except Exception as e:
        print(f"[ERROR] /api/estadisticas/ventas-mes: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/estadisticas/productos-top', methods=['GET'])
def obtener_productos_top():
    """Top 10 productos más vendidos"""
    try:
        conexion = get_db_connection()
        if not conexion:
            return jsonify({'success': False, 'error': 'Error de conexión a BD'}), 500
        
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute('''
            SELECT 
                p.nombre,
                p.codigo,
                SUM(lv.cantidad) as unidades_vendidas,
                SUM(lv.subtotal) as total_vendido,
                COUNT(DISTINCT lv.venta_id) as num_ventas
            FROM productos p
            INNER JOIN lineas_venta lv ON p.id = lv.producto_id
            INNER JOIN ventas v ON lv.venta_id = v.id
            WHERE v.fecha >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
            GROUP BY p.id, p.nombre, p.codigo
            ORDER BY unidades_vendidas DESC
            LIMIT 10
        ''')
        
        datos = cursor.fetchall()
        conexion.close()
        
        return jsonify({'success': True, 'data': datos})
        
    except Exception as e:
        print(f"[ERROR] /api/estadisticas/productos-top: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/estadisticas/categorias', methods=['GET'])
def obtener_ventas_por_categoria():
    """Ventas totales por categoría"""
    try:
        conexion = get_db_connection()
        if not conexion:
            return jsonify({'success': False, 'error': 'Error de conexión a BD'}), 500
        
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute('''
            SELECT 
                c.nombre as categoria,
                COUNT(DISTINCT p.id) as num_productos,
                SUM(lv.cantidad) as unidades_vendidas,
                SUM(lv.subtotal) as total_vendido
            FROM categorias_productos c
            LEFT JOIN productos p ON c.id = p.categoria_id
            LEFT JOIN lineas_venta lv ON p.id = lv.producto_id
            LEFT JOIN ventas v ON lv.venta_id = v.id
            WHERE v.fecha >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
            GROUP BY c.id, c.nombre
            ORDER BY total_vendido DESC
        ''')
        
        datos = cursor.fetchall()
        conexion.close()
        
        return jsonify({'success': True, 'data': datos})
        
    except Exception as e:
        print(f"[ERROR] /api/estadisticas/categorias: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/estadisticas/inventario', methods=['GET'])
def obtener_estado_inventario():
    """Estado general del inventario por categoría"""
    try:
        conexion = get_db_connection()
        if not conexion:
            return jsonify({'success': False, 'error': 'Error de conexión a BD'}), 500
        
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute('''
            SELECT 
                CASE 
                    WHEN stock_actual < (stock_minimo * 0.3) THEN 'Crítico'
                    WHEN stock_actual < stock_minimo THEN 'Bajo'
                    ELSE 'Normal'
                END as estado,
                COUNT(*) as cantidad_productos,
                SUM(stock_actual) as stock_total,
                SUM(stock_actual * precio_venta) as valor_inventario
            FROM productos
            WHERE activo = TRUE
            GROUP BY estado
            ORDER BY 
                CASE estado
                    WHEN 'Crítico' THEN 1
                    WHEN 'Bajo' THEN 2
                    ELSE 3
                END
        ''')
        
        datos = cursor.fetchall()
        conexion.close()
        
        return jsonify({'success': True, 'data': datos})
        
    except Exception as e:
        print(f"[ERROR] /api/estadisticas/inventario: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/estadisticas/resumen', methods=['GET'])
def obtener_resumen_estadisticas():
    """Resumen general de estadísticas"""
    try:
        conexion = get_db_connection()
        if not conexion:
            return jsonify({'success': False, 'error': 'Error de conexión a BD'}), 500
        
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        
        # Venta promedio
        cursor.execute('SELECT AVG(total) as venta_promedio FROM ventas WHERE fecha >= DATE_SUB(NOW(), INTERVAL 6 MONTH)')
        venta_promedio = cursor.fetchone()['venta_promedio']
        
        # Producto más vendido
        cursor.execute('''
            SELECT p.nombre 
            FROM productos p
            INNER JOIN lineas_venta lv ON p.id = lv.producto_id
            INNER JOIN ventas v ON lv.venta_id = v.id
            WHERE v.fecha >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
            GROUP BY p.id, p.nombre
            ORDER BY SUM(lv.cantidad) DESC
            LIMIT 1
        ''')
        producto_top_result = cursor.fetchone()
        producto_top = producto_top_result['nombre'] if producto_top_result else 'N/A'
        
        # Total facturado
        cursor.execute('SELECT SUM(total) as total_facturado FROM ventas WHERE fecha >= DATE_SUB(NOW(), INTERVAL 6 MONTH)')
        total_facturado = cursor.fetchone()['total_facturado']
        
        # Margen promedio (estimado)
        cursor.execute('''
            SELECT AVG((p.precio_venta - p.precio_compra) / p.precio_venta * 100) as margen_promedio
            FROM productos p
            WHERE p.precio_compra > 0 AND p.precio_venta > 0
        ''')
        margen_promedio = cursor.fetchone()['margen_promedio']
        
        conexion.close()
        
        return jsonify({
            'success': True,
            'data': {
                'venta_promedio': float(venta_promedio or 0),
                'producto_top': producto_top,
                'total_facturado': float(total_facturado or 0),
                'margen_promedio': float(margen_promedio or 0)
            }
        })
        
    except Exception as e:
        print(f"[ERROR] /api/estadisticas/resumen: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================
# SERVIDOR
# ============================================

if __name__ == '__main__':
    print("=" * 60)
    print("📊 API REST - ERP INTELIGENTE")
    print("=" * 60)
    print("Puerto: 5001")
    print("Endpoints disponibles:")
    print("  - GET  /api/productos          : Lista de productos")
    print("  - GET  /api/productos/:id      : Detalle de producto")
    print("  - GET  /api/ventas             : Lista de ventas")
    print("  - GET  /api/ventas/:id/lineas  : Líneas de una venta")
    print("  - GET  /api/clientes           : Lista de clientes")
    print("  - GET  /api/clientes/:id       : Detalle de cliente")
    print("  - GET  /api/inventario         : Estado del inventario")
    print("  - GET  /api/inventario/alertas : Alertas de stock")
    print("  - GET  /api/categorias         : Lista de categorías")
    print("  - GET  /api/estadisticas/ventas-mes    : Ventas por mes")
    print("  - GET  /api/estadisticas/productos-top : Top 10 productos")
    print("  - GET  /api/estadisticas/categorias    : Ventas por categoría")
    print("  - GET  /api/estadisticas/inventario    : Estado inventario")
    print("  - GET  /api/estadisticas/resumen       : Resumen general")
    print("=" * 60)
    
    # Verificar conexión a BD
    conn = get_db_connection()
    if conn:
        print("✅ Conexión a MySQL OK")
        conn.close()
    else:
        print("❌ Error de conexión a MySQL")
    
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5001)
