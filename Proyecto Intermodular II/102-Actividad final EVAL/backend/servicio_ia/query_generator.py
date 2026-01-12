"""
Generador de Consultas SQL
Convierte intenciones del usuario en consultas SQL seguras
"""

import re
from typing import Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class QueryGenerator:
    """Generador de consultas SQL basado en intenciones"""
    
    def __init__(self):
        pass
    
    def generate(self, intent: str, texto_usuario: str) -> Tuple[Optional[str], Dict[str, Any]]:
        """
        Generar consulta SQL según la intención
        
        Args:
            intent: Intención clasificada
            texto_usuario: Texto original del usuario
            
        Returns:
            (consulta_sql, parametros)
        """
        # Mapeo de intenciones a métodos generadores
        generators = {
            'consulta_stock': self._query_stock,
            'consulta_ventas': self._query_ventas,
            'consulta_clientes': self._query_clientes,
            'consulta_productos': self._query_productos,
            'alerta': self._query_alertas
        }
        
        generator = generators.get(intent)
        if generator:
            return generator(texto_usuario)
        
        return (None, {})
    
    def _query_stock(self, texto: str) -> Tuple[str, Dict]:
        """Generar consulta para inventario/stock"""
        texto_lower = texto.lower()
        
        # Detectar si pregunta por stock bajo
        if any(word in texto_lower for word in ['bajo', 'poco', 'mínimo', 'crítico', 'escaso']):
            query = """
                SELECT 
                    p.codigo,
                    p.nombre,
                    c.nombre AS categoria,
                    p.stock_actual,
                    p.stock_minimo,
                    (p.stock_minimo - p.stock_actual) AS faltante
                FROM productos p
                LEFT JOIN categorias_productos c ON p.categoria_id = c.id
                WHERE p.stock_actual < p.stock_minimo 
                    AND p.activo = TRUE
                ORDER BY (p.stock_minimo - p.stock_actual) DESC
                LIMIT 20
            """
            return (query, {})
        
        # Detectar si pregunta por un producto específico
        # Buscar palabras que puedan ser nombres de productos
        palabras = re.findall(r'\b[A-ZÁÉÍÓÚ][a-záéíóúñ]+\b', texto)
        if palabras and len(palabras) > 0:
            # Asumir que la primera palabra capitalizada puede ser el producto
            producto_busqueda = palabras[0]
            query = """
                SELECT 
                    codigo,
                    nombre,
                    stock_actual,
                    stock_minimo,
                    stock_maximo
                FROM productos
                WHERE nombre LIKE %s AND activo = TRUE
                LIMIT 10
            """
            return (query, {'nombre': f'%{producto_busqueda}%'})
        
        # Consulta general de stock
        query = """
            SELECT 
                p.codigo,
                p.nombre,
                c.nombre AS categoria,
                p.stock_actual,
                p.stock_minimo
            FROM productos p
            LEFT JOIN categorias_productos c ON p.categoria_id = c.id
            WHERE p.activo = TRUE
            ORDER BY p.stock_actual ASC
            LIMIT 20
        """
        return (query, {})
    
    def _query_ventas(self, texto: str) -> Tuple[str, Dict]:
        """Generar consulta para ventas"""
        texto_lower = texto.lower()
        params = {}
        
        # Detectar rango temporal
        fecha_inicio, fecha_fin = self._extract_date_range(texto_lower)
        
        if 'hoy' in texto_lower:
            query = """
                SELECT 
                    v.numero_factura,
                    c.nombre AS cliente,
                    v.total,
                    v.estado,
                    v.metodo_pago,
                    v.fecha
                FROM ventas v
                LEFT JOIN clientes c ON v.cliente_id = c.id
                WHERE v.fecha = CURDATE()
                ORDER BY v.id DESC
            """
            return (query, {})
        
        elif any(word in texto_lower for word in ['semana', 'semanal']):
            query = """
                SELECT 
                    DATE(v.fecha) AS fecha,
                    COUNT(*) AS num_ventas,
                    SUM(v.total) AS total_ingresos,
                    AVG(v.total) AS ticket_promedio
                FROM ventas v
                WHERE v.fecha >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
                    AND v.estado = 'pagada'
                GROUP BY DATE(v.fecha)
                ORDER BY fecha DESC
            """
            return (query, {})
        
        elif any(word in texto_lower for word in ['mes', 'mensual']):
            query = """
                SELECT 
                    COUNT(*) AS num_ventas,
                    SUM(v.total) AS total_ingresos,
                    AVG(v.total) AS ticket_promedio,
                    MIN(v.total) AS venta_minima,
                    MAX(v.total) AS venta_maxima
                FROM ventas v
                WHERE YEAR(v.fecha) = YEAR(CURDATE())
                    AND MONTH(v.fecha) = MONTH(CURDATE())
                    AND v.estado = 'pagada'
            """
            return (query, {})
        
        # Top productos vendidos
        elif any(word in texto_lower for word in ['top', 'más vendidos', 'mejor']):
            query = """
                SELECT 
                    p.nombre,
                    SUM(lv.cantidad) AS unidades_vendidas,
                    SUM(lv.subtotal) AS ingresos_totales
                FROM lineas_venta lv
                JOIN productos p ON lv.producto_id = p.id
                JOIN ventas v ON lv.venta_id = v.id
                WHERE v.estado = 'pagada'
                    AND v.fecha >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                GROUP BY p.id
                ORDER BY unidades_vendidas DESC
                LIMIT 10
            """
            return (query, {})
        
        # Facturas pendientes
        elif any(word in texto_lower for word in ['pendiente', 'vencida', 'cobrar']):
            query = """
                SELECT 
                    v.numero_factura,
                    c.nombre AS cliente,
                    v.total,
                    v.fecha,
                    v.fecha_vencimiento,
                    DATEDIFF(CURDATE(), v.fecha_vencimiento) AS dias_vencido
                FROM ventas v
                JOIN clientes c ON v.cliente_id = c.id
                WHERE v.estado = 'pendiente'
                    AND v.fecha_vencimiento < CURDATE()
                ORDER BY dias_vencido DESC
                LIMIT 20
            """
            return (query, {})
        
        # Ventas generales
        query = """
            SELECT 
                v.numero_factura,
                c.nombre AS cliente,
                v.total,
                v.estado,
                v.fecha
            FROM ventas v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            ORDER BY v.fecha DESC
            LIMIT 20
        """
        return (query, {})
    
    def _query_clientes(self, texto: str) -> Tuple[str, Dict]:
        """Generar consulta para clientes"""
        texto_lower = texto.lower()
        
        # Top clientes
        if any(word in texto_lower for word in ['mejor', 'top', 'más', 'mayor']):
            query = """
                SELECT 
                    c.nombre,
                    c.email,
                    c.ciudad,
                    c.total_compras,
                    c.ultima_compra,
                    COUNT(v.id) AS num_compras
                FROM clientes c
                LEFT JOIN ventas v ON c.id = v.cliente_id AND v.estado = 'pagada'
                WHERE c.activo = TRUE
                GROUP BY c.id
                ORDER BY c.total_compras DESC
                LIMIT 10
            """
            return (query, {})
        
        # Clientes inactivos
        elif any(word in texto_lower for word in ['inactivo', 'sin comprar', 'no han comprado']):
            # Extraer días (por defecto 60)
            dias = 60
            match = re.search(r'(\d+)\s*día', texto_lower)
            if match:
                dias = int(match.group(1))
            
            query = """
                SELECT 
                    c.nombre,
                    c.email,
                    c.telefono,
                    c.ultima_compra,
                    DATEDIFF(CURDATE(), c.ultima_compra) AS dias_inactivo,
                    c.total_compras
                FROM clientes c
                WHERE c.ultima_compra < DATE_SUB(CURDATE(), INTERVAL %s DAY)
                    AND c.activo = TRUE
                ORDER BY dias_inactivo DESC
                LIMIT 20
            """
            return (query, {'dias': dias})
        
        # Clientes generales
        query = """
            SELECT 
                c.nombre,
                c.email,
                c.ciudad,
                c.total_compras,
                c.ultima_compra
            FROM clientes c
            WHERE c.activo = TRUE
            ORDER BY c.created_at DESC
            LIMIT 20
        """
        return (query, {})
    
    def _query_productos(self, texto: str) -> Tuple[str, Dict]:
        """Generar consulta para productos"""
        texto_lower = texto.lower()
        
        # Top productos por ventas
        if any(word in texto_lower for word in ['más vendidos', 'top', 'mejor']):
            query = """
                SELECT 
                    p.nombre,
                    p.precio_venta,
                    p.stock_actual,
                    SUM(lv.cantidad) AS unidades_vendidas,
                    SUM(lv.subtotal) AS ingresos_totales
                FROM productos p
                JOIN lineas_venta lv ON p.id = lv.producto_id
                JOIN ventas v ON lv.venta_id = v.id
                WHERE v.estado = 'pagada'
                    AND v.fecha >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                GROUP BY p.id
                ORDER BY unidades_vendidas DESC
                LIMIT 10
            """
            return (query, {})
        
        # Productos por categoría
        match = re.search(r'categoría\s+([a-záéíóúñ]+)', texto_lower)
        if match:
            categoria = match.group(1)
            query = """
                SELECT 
                    p.codigo,
                    p.nombre,
                    p.precio_venta,
                    p.stock_actual,
                    c.nombre AS categoria
                FROM productos p
                JOIN categorias_productos c ON p.categoria_id = c.id
                WHERE c.nombre LIKE %s
                    AND p.activo = TRUE
                ORDER BY p.nombre
                LIMIT 20
            """
            return (query, {'categoria': f'%{categoria}%'})
        
        # Listado general de productos
        query = """
            SELECT 
                p.codigo,
                p.nombre,
                c.nombre AS categoria,
                p.precio_venta,
                p.stock_actual
            FROM productos p
            LEFT JOIN categorias_productos c ON p.categoria_id = c.id
            WHERE p.activo = TRUE
            ORDER BY p.nombre
            LIMIT 20
        """
        return (query, {})
    
    def _query_alertas(self, texto: str) -> Tuple[str, Dict]:
        """Generar consulta para alertas"""
        texto_lower = texto.lower()
        
        # Alertas críticas
        if any(word in texto_lower for word in ['crítica', 'urgente', 'importante']):
            query = """
                SELECT 
                    tipo,
                    titulo,
                    descripcion,
                    severidad,
                    fecha_creacion
                FROM alertas
                WHERE leida = FALSE
                    AND severidad = 'critical'
                ORDER BY fecha_creacion DESC
                LIMIT 10
            """
            return (query, {})
        
        # Todas las alertas pendientes
        query = """
            SELECT 
                tipo,
                titulo,
                descripcion,
                severidad,
                fecha_creacion
            FROM alertas
            WHERE leida = FALSE
            ORDER BY 
                CASE severidad
                    WHEN 'critical' THEN 1
                    WHEN 'warning' THEN 2
                    ELSE 3
                END,
                fecha_creacion DESC
            LIMIT 20
        """
        return (query, {})
    
    def _extract_date_range(self, texto: str) -> Tuple[Optional[str], Optional[str]]:
        """Extraer rango de fechas del texto"""
        hoy = datetime.now().date()
        
        if 'hoy' in texto:
            return (str(hoy), str(hoy))
        elif 'ayer' in texto:
            ayer = hoy - timedelta(days=1)
            return (str(ayer), str(ayer))
        elif 'semana' in texto:
            inicio = hoy - timedelta(days=7)
            return (str(inicio), str(hoy))
        elif 'mes' in texto:
            inicio = hoy - timedelta(days=30)
            return (str(inicio), str(hoy))
        
        return (None, None)


# Singleton global
_query_generator = None

def get_query_generator() -> QueryGenerator:
    """Obtener instancia global del generador"""
    global _query_generator
    if _query_generator is None:
        _query_generator = QueryGenerator()
    return _query_generator
