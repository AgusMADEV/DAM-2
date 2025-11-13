import mysql.connector
import json
import re


class AMA():
    """
    Clase principal de acceso a datos basada en el patrón visto en clase.
    Proporciona métodos simples para operaciones con MySQL.
    """
    
    # Expresión regular para validar identificadores SQL
    _re_ident = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
    
    def __init__(self, host, usuario, contrasena, basedatos):
        """
        Constructor que establece la conexión a MySQL
        
        Args:
            host: Servidor de la base de datos
            usuario: Usuario de MySQL
            contrasena: Contraseña del usuario
            basedatos: Nombre de la base de datos
        """
        self.host = host
        self.usuario = usuario
        self.contrasena = contrasena
        self.basedatos = basedatos
        
        # Establecer conexión
        self.conexion = mysql.connector.connect(
            host=self.host,
            user=self.usuario,
            password=self.contrasena,
            database=self.basedatos
        )
        
        self.cursor = self.conexion.cursor()
    
    def _validar_ident(self, nombre):
        """
        Valida que el identificador sea seguro para usar en SQL
        
        Args:
            nombre: Identificador a validar (tabla, columna, etc.)
        """
        if not isinstance(nombre, str) or not self._re_ident.match(nombre):
            raise ValueError(f"Identificador inválido: {nombre!r}")
    
    def seleccionar(self, tabla):
        """
        Selecciona todos los registros de una tabla
        
        Args:
            tabla: Nombre de la tabla
            
        Returns:
            JSON con los registros de la tabla
        """
        self._validar_ident(tabla)
        self.cursor.execute(f"SELECT * FROM `{tabla}`")
        columnas = self.cursor.column_names
        filas = self.cursor.fetchall()
        
        # Convertir a lista de diccionarios
        datos = [dict(zip(columnas, fila)) for fila in filas]
        
        return json.dumps(datos, ensure_ascii=False, indent=2, default=str)
    
    def buscar(self, tabla, columna, valor):
        """
        Busca registros en una tabla por un criterio
        
        Args:
            tabla: Nombre de la tabla
            columna: Columna donde buscar
            valor: Valor a buscar (con LIKE)
            
        Returns:
            JSON con los registros encontrados
        """
        self._validar_ident(tabla)
        self._validar_ident(columna)
        
        sql = f"SELECT * FROM `{tabla}` WHERE `{columna}` LIKE %s"
        self.cursor.execute(sql, (f"%{valor}%",))
        columnas = self.cursor.column_names
        filas = self.cursor.fetchall()
        
        # Convertir a lista de diccionarios
        datos = [dict(zip(columnas, fila)) for fila in filas]
        
        return json.dumps(datos, ensure_ascii=False, indent=2, default=str)
    
    def insertar(self, tabla, datos):
        """
        Inserta un nuevo registro en la tabla
        
        Args:
            tabla: Nombre de la tabla
            datos: Diccionario con los datos a insertar
            
        Returns:
            ID del registro insertado
        """
        self._validar_ident(tabla)
        
        if not datos:
            raise ValueError("Los datos no pueden estar vacíos")
        
        # Validar nombres de columnas
        for columna in datos.keys():
            self._validar_ident(columna)
        
        columnas = list(datos.keys())
        valores = list(datos.values())
        placeholders = ', '.join(['%s'] * len(valores))
        
        sql = f"INSERT INTO `{tabla}` ({', '.join([f'`{c}`' for c in columnas])}) VALUES ({placeholders})"
        self.cursor.execute(sql, valores)
        self.conexion.commit()
        
        return self.cursor.lastrowid
    
    def actualizar(self, tabla, datos, condiciones):
        """
        Actualiza registros en la tabla
        
        Args:
            tabla: Nombre de la tabla
            datos: Diccionario con los datos a actualizar
            condiciones: Diccionario con las condiciones WHERE
            
        Returns:
            Número de filas afectadas
        """
        self._validar_ident(tabla)
        
        if not datos:
            raise ValueError("Los datos a actualizar no pueden estar vacíos")
        if not condiciones:
            raise ValueError("Las condiciones no pueden estar vacías")
        
        # Validar identificadores
        for columna in list(datos.keys()) + list(condiciones.keys()):
            self._validar_ident(columna)
        
        # Construir SET
        set_clauses = [f"`{key}` = %s" for key in datos.keys()]
        where_clauses = [f"`{key}` = %s" for key in condiciones.keys()]
        
        sql = f"UPDATE `{tabla}` SET {', '.join(set_clauses)} WHERE {' AND '.join(where_clauses)}"
        valores = list(datos.values()) + list(condiciones.values())
        
        self.cursor.execute(sql, valores)
        self.conexion.commit()
        
        return self.cursor.rowcount
    
    def eliminar(self, tabla, condiciones):
        """
        Elimina registros de la tabla
        
        Args:
            tabla: Nombre de la tabla
            condiciones: Diccionario con las condiciones WHERE
            
        Returns:
            Número de filas eliminadas
        """
        self._validar_ident(tabla)
        
        if not condiciones:
            raise ValueError("Las condiciones no pueden estar vacías")
        
        # Validar identificadores
        for columna in condiciones.keys():
            self._validar_ident(columna)
        
        where_clauses = [f"`{key}` = %s" for key in condiciones.keys()]
        sql = f"DELETE FROM `{tabla}` WHERE {' AND '.join(where_clauses)}"
        valores = list(condiciones.values())
        
        self.cursor.execute(sql, valores)
        self.conexion.commit()
        
        return self.cursor.rowcount
    
    def tablas(self):
        """
        Obtiene la lista de tablas de la base de datos
        
        Returns:
            JSON con los nombres de las tablas
        """
        self.cursor.execute("SHOW TABLES")
        filas = self.cursor.fetchall()
        
        # Convertir a lista de diccionarios
        datos = [{"tabla": fila[0]} for fila in filas]
        
        return json.dumps(datos, ensure_ascii=False, indent=2)
    
    def describir(self, tabla):
        """
        Describe la estructura de una tabla
        
        Args:
            tabla: Nombre de la tabla
            
        Returns:
            JSON con la estructura de la tabla
        """
        self._validar_ident(tabla)
        
        self.cursor.execute(f"DESCRIBE `{tabla}`")
        columnas = self.cursor.column_names
        filas = self.cursor.fetchall()
        
        # Convertir a lista de diccionarios
        datos = [dict(zip(columnas, fila)) for fila in filas]
        
        return json.dumps(datos, ensure_ascii=False, indent=2, default=str)
    
    def ejecutar_sql(self, sql, parametros=None):
        """
        Ejecuta una consulta SQL personalizada
        
        Args:
            sql: Consulta SQL a ejecutar
            parametros: Parámetros para la consulta (opcional)
            
        Returns:
            JSON con los resultados (si es SELECT) o número de filas afectadas
        """
        self.cursor.execute(sql, parametros or ())
        
        # Si es una consulta SELECT, devolver resultados
        if sql.strip().upper().startswith('SELECT'):
            columnas = self.cursor.column_names
            filas = self.cursor.fetchall()
            datos = [dict(zip(columnas, fila)) for fila in filas]
            return json.dumps(datos, ensure_ascii=False, indent=2, default=str)
        else:
            # Si es INSERT, UPDATE, DELETE, hacer commit y devolver filas afectadas
            self.conexion.commit()
            return self.cursor.rowcount
    
    def cerrar(self):
        """
        Cierra la conexión a la base de datos
        """
        try:
            if self.cursor:
                self.cursor.close()
            if self.conexion:
                self.conexion.close()
        except Exception:
            pass


# Función de conveniencia para crear una instancia
def crear_conexion(host="localhost", usuario="", contrasena="", basedatos=""):
    """
    Función de conveniencia para crear una conexión AMA
    
    Args:
        host: Servidor de la base de datos
        usuario: Usuario de MySQL
        contrasena: Contraseña del usuario
        basedatos: Nombre de la base de datos
        
    Returns:
        Instancia de AMA configurada
    """
    return AMA(host, usuario, contrasena, basedatos)


if __name__ == "__main__":
    # Ejemplo de uso básico
    print("Componente de Acceso a Datos AMA - Final de Unidad 2")
    print("=" * 50)
    print("Basado en el patrón visto en clase")
    print()
    print("Ejemplo de uso:")
    print("conexion = AMA('localhost', 'usuario', 'password', 'database')")
    print("print(conexion.tablas())")
    print("print(conexion.seleccionar('mi_tabla'))")
    print("conexion.cerrar()")