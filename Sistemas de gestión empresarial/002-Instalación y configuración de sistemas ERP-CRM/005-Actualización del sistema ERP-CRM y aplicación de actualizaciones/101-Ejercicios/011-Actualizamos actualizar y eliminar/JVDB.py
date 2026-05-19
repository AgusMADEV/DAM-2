import re
import mysql.connector
import json

class JVDB():
  _re_ident = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")  # para validar identificadores

  def __init__(self, host, usuario, contrasena, basedatos):
    self.host = host
    self.usuario = usuario
    self.contrasena = contrasena
    self.basedatos = basedatos

    self.conexion = mysql.connector.connect(
        host=self.host,
        user=self.usuario,
        password=self.contrasena,
        database=self.basedatos
    )
    self.cursor = self.conexion.cursor()

  def _validar_ident(self, nombre: str):
    if not isinstance(nombre, str) or not self._re_ident.match(nombre):
      raise ValueError(f"Identificador inválido: {nombre!r}")

  def _columnas_tabla(self, tabla: str):
    self._validar_ident(tabla)
    self.cursor.execute(f"DESCRIBE `{tabla}`")
    return {fila[0] for fila in self.cursor.fetchall()}

  def seleccionar(self, tabla):
    self._validar_ident(tabla)
    self.cursor.execute(f"SELECT * FROM `{tabla}`")
    columnas = self.cursor.column_names
    filas = self.cursor.fetchall()
    datos = [dict(zip(columnas, fila)) for fila in filas]
    return json.dumps(datos, ensure_ascii=False, indent=2)

  def tablas(self):
    self.cursor.execute("SHOW TABLES")
    filas = self.cursor.fetchall()
    datos = [{"tabla": fila[0]} for fila in filas]
    return json.dumps(datos, ensure_ascii=False, indent=2)

  def buscar(self, tabla, columna, valor):
    self._validar_ident(tabla)
    self._validar_ident(columna)
    sql = f"SELECT * FROM `{tabla}` WHERE `{columna}` LIKE %s"
    self.cursor.execute(sql, (f"%{valor}%",))
    columnas = self.cursor.column_names
    filas = self.cursor.fetchall()
    datos = [dict(zip(columnas, fila)) for fila in filas]
    return json.dumps(datos, ensure_ascii=False, indent=2)

  def insertar(self, tabla, datos):
    """
    Inserta una fila (dict) o varias filas (list[dict]) en `tabla`.
    - datos = {"col":"valor", ...}  o  [{"col":...}, {"col":...}, ...]
    Devuelve JSON con número de insertados e IDs si están disponibles.
    """
    # Normaliza entrada
    if isinstance(datos, dict):
      filas = [datos]
    elif isinstance(datos, list) and all(isinstance(d, dict) for d in datos):
      filas = datos
    else:
      raise TypeError("`datos` debe ser dict o list[dict].")

    if not filas:
      return json.dumps({"insertados": 0, "ids": []}, ensure_ascii=False, indent=2)

    # Valida tabla y columnas
    self._validar_ident(tabla)
    columnas_validas = self._columnas_tabla(tabla)

    # Unión de claves presentes; filtra solo columnas reales
    columnas = sorted({k for fila in filas for k in fila.keys() if k in columnas_validas})
    if not columnas:
      raise ValueError("Ninguna clave de `datos` coincide con columnas de la tabla.")

    # Construye SQL parametrizado
    col_list = ", ".join(f"`{c}`" for c in columnas)
    placeholders = ", ".join(["%s"] * len(columnas))
    sql = f"INSERT INTO `{tabla}` ({col_list}) VALUES ({placeholders})"

    # Mapea valores por fila, poniendo None en columnas ausentes
    values = [tuple(f.get(c, None) for c in columnas) for f in filas]

    try:
      self.cursor.executemany(sql, values)
      self.conexion.commit()
      insertados = self.cursor.rowcount

      # Estimación de IDs insertados (funciona bien con AUTO_INCREMENT y sin triggers múltiples)
      ids = []
      if self.cursor.lastrowid and insertados > 0:
        start = self.cursor.lastrowid - insertados + 1
        # evita IDs negativos si el conector no los calcula bien
        if start > 0:
          ids = list(range(start, start + insertados))

      return json.dumps({"insertados": insertados, "ids": ids}, ensure_ascii=False, indent=2)

    except mysql.connector.Error as e:
      self.conexion.rollback()
      # Devuelve error en JSON para manejo aguas arriba
      return json.dumps(
        {"error": True, "mensaje": str(e), "sqlstate": getattr(e, "sqlstate", None)},
        ensure_ascii=False, indent=2
      )

  def cerrar(self):
    try:
      if self.cursor: self.cursor.close()
      if self.conexion: self.conexion.close()
    except Exception:
      pass
  # --- add below existing imports / methods in JVDB.py ---

  def _pk_column(self, tabla: str):
    """Devuelve el nombre de la columna PK (single-column) o None si no hay."""
    self._validar_ident(tabla)
    self.cursor.execute(f"SHOW KEYS FROM `{tabla}` WHERE Key_name='PRIMARY'")
    rows = self.cursor.fetchall()
    # single-column PK expected
    if rows and len(rows) == 1:
      # Column_name is at index 4 usually for mysql-connector's SHOW KEYS
      col = rows[0][4]
      return col
    # fallback: try DESCRIBE and pick first with 'PRI'
    self.cursor.execute(f"DESCRIBE `{tabla}`")
    for desc in self.cursor.fetchall():
      if len(desc) >= 4 and desc[3] == 'PRI':
        return desc[0]
    return None

  def actualizar(self, tabla: str, pk_value, cambios: dict):
    """
    Actualiza una fila por PK en `tabla`.
    - pk_value: valor del PK (single-column).
    - cambios: dict {col: nuevo_valor, ...}
    Devuelve JSON con 'actualizados'.
    """
    self._validar_ident(tabla)
    if not isinstance(cambios, dict) or not cambios:
      return json.dumps({"error": True, "mensaje": "Cambios vacíos o inválidos"}, ensure_ascii=False, indent=2)

    pk = self._pk_column(tabla)
    if not pk:
      return json.dumps({"error": True, "mensaje": "Tabla sin PK simple, no se puede actualizar"}, ensure_ascii=False, indent=2)

    columnas_validas = self._columnas_tabla(tabla)
    sets = [c for c in cambios.keys() if c in columnas_validas and c != pk]
    if not sets:
      return json.dumps({"error": True, "mensaje": "Ninguna columna válida para actualizar"}, ensure_ascii=False, indent=2)

    set_clause = ", ".join(f"`{c}`=%s" for c in sets)
    sql = f"UPDATE `{tabla}` SET {set_clause} WHERE `{pk}`=%s"
    values = [cambios[c] for c in sets] + [pk_value]

    try:
      self.cursor.execute(sql, tuple(values))
      self.conexion.commit()
      return json.dumps({"actualizados": self.cursor.rowcount}, ensure_ascii=False, indent=2)
    except mysql.connector.Error as e:
      self.conexion.rollback()
      return json.dumps(
        {"error": True, "mensaje": str(e), "sqlstate": getattr(e, "sqlstate", None)},
        ensure_ascii=False, indent=2
      )

  def eliminar(self, tabla: str, pk_value):
    """
    Elimina una fila por PK en `tabla`.
    Devuelve JSON con 'eliminados'.
    """
    self._validar_ident(tabla)
    pk = self._pk_column(tabla)
    if not pk:
      return json.dumps({"error": True, "mensaje": "Tabla sin PK simple, no se puede eliminar"}, ensure_ascii=False, indent=2)

    sql = f"DELETE FROM `{tabla}` WHERE `{pk}`=%s"
    try:
      self.cursor.execute(sql, (pk_value,))
      self.conexion.commit()
      return json.dumps({"eliminados": self.cursor.rowcount}, ensure_ascii=False, indent=2)
    except mysql.connector.Error as e:
      self.conexion.rollback()
      return json.dumps(
        {"error": True, "mensaje": str(e), "sqlstate": getattr(e, "sqlstate", None)},
        ensure_ascii=False, indent=2
      )

