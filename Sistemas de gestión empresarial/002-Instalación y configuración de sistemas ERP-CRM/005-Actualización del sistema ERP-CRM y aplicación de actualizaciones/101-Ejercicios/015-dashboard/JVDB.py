import re
import mysql.connector
import datetime, decimal, base64, json

class JVDB:
  _re_ident = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")  # valida identificadores SQL simples

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
    # cursor por defecto (tupla). Usamos column_names para mapear a dict
    self.cursor = self.conexion.cursor()

  # ---------- Utilidades internas ----------

  def _validar_ident(self, nombre: str):
    if not isinstance(nombre, str) or not self._re_ident.match(nombre):
      raise ValueError(f"Identificador inválido: {nombre!r}")

  def _columnas_tabla(self, tabla: str):
    self._validar_ident(tabla)
    self.cursor.execute(f"DESCRIBE `{tabla}`")
    return {fila[0] for fila in self.cursor.fetchall()}

  def _pk_column(self, tabla: str):
    """Devuelve el nombre de la columna PK (si es de una sola columna)."""
    self._validar_ident(tabla)
    self.cursor.execute(f"SHOW KEYS FROM `{tabla}` WHERE Key_name='PRIMARY'")
    rows = self.cursor.fetchall()
    # SHOW KEYS devuelve 1 fila por columna PK. Aceptamos solo PK simple.
    if rows and len(rows) == 1:
      # Column_name suele ir en índice 4
      return rows[0][4]
    # Fallback: DESCRIBE y buscar 'PRI'
    self.cursor.execute(f"DESCRIBE `{tabla}`")
    for desc in self.cursor.fetchall():
      # desc = (Field, Type, Null, Key, Default, Extra)
      if len(desc) >= 4 and desc[3] == 'PRI':
        return desc[0]
    return None

  def _json_default(self, obj):
    if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
      return obj.isoformat()
    if isinstance(obj, decimal.Decimal):
      return float(obj)
    if isinstance(obj, (bytes, bytearray)):
      try:
        return obj.decode('utf-8')
      except Exception:
        return base64.b64encode(obj).decode('ascii')
    if isinstance(obj, memoryview):
      b = obj.tobytes()
      try:
        return b.decode('utf-8')
      except Exception:
        return base64.b64encode(b).decode('ascii')
    return str(obj)

  def _json(self, payload):
    return json.dumps(payload, ensure_ascii=False, indent=2, default=self._json_default)

  # ---------- Lectura ----------

  def seleccionar(self, tabla: str):
    self._validar_ident(tabla)
    self.cursor.execute(f"SELECT * FROM `{tabla}`")
    columnas = self.cursor.column_names
    filas = self.cursor.fetchall()
    datos = [dict(zip(columnas, fila)) for fila in filas]
    return self._json(datos)

  def tablas(self):
    self.cursor.execute("SHOW TABLES")
    filas = self.cursor.fetchall()
    datos = [{"tabla": fila[0]} for fila in filas]
    return self._json(datos)

  def buscar(self, tabla: str, columna: str, valor: str):
    self._validar_ident(tabla)
    self._validar_ident(columna)
    sql = f"SELECT * FROM `{tabla}` WHERE `{columna}` LIKE %s"
    self.cursor.execute(sql, (f"%{valor}%",))
    columnas = self.cursor.column_names
    filas = self.cursor.fetchall()
    datos = [dict(zip(columnas, fila)) for fila in filas]
    return self._json(datos)

  # ---------- Escritura ----------

  def insertar(self, tabla: str, datos):
    """
    Inserta una fila (dict) o varias filas (list[dict]) en `tabla`.
    Devuelve JSON: {"insertados": n, "ids": [..]} o {"error": True, "mensaje": "..."}
    """
    # Normaliza entrada
    if isinstance(datos, dict):
      filas = [datos]
    elif isinstance(datos, list) and all(isinstance(d, dict) for d in datos):
      filas = datos
    else:
      return self._json({"error": True, "mensaje": "`datos` debe ser dict o list[dict]."})

    if not filas:
      return self._json({"insertados": 0, "ids": []})

    # Valida tabla y columnas
    self._validar_ident(tabla)
    columnas_validas = self._columnas_tabla(tabla)

    # Unión de claves presentes; filtra solo columnas reales
    columnas = sorted({k for fila in filas for k in fila.keys() if k in columnas_validas})
    if not columnas:
      return self._json({"error": True, "mensaje": "Ninguna clave de `datos` coincide con columnas de la tabla."})

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

      # Estimación de IDs insertados (AUTO_INCREMENT)
      ids = []
      if getattr(self.cursor, "lastrowid", None) and insertados > 0:
        start = self.cursor.lastrowid - insertados + 1
        if start and start > 0:
          ids = list(range(start, start + insertados))

      return self._json({"insertados": insertados, "ids": ids})

    except mysql.connector.Error as e:
      self.conexion.rollback()
      return self._json({"error": True, "mensaje": str(e), "sqlstate": getattr(e, "sqlstate", None)})

  def actualizar(self, tabla: str, pk_value, cambios: dict):
    """
    Actualiza una fila por PK simple en `tabla`.
    cambios: dict {col: nuevo_valor, ...}  (puede ser de 1 única columna para inline-edit)
    """
    self._validar_ident(tabla)
    if not isinstance(cambios, dict) or not cambios:
      return self._json({"error": True, "mensaje": "Cambios vacíos o inválidos"})

    pk = self._pk_column(tabla)
    if not pk:
      return self._json({"error": True, "mensaje": "Tabla sin PK simple, no se puede actualizar"})

    columnas_validas = self._columnas_tabla(tabla)
    sets = [c for c in cambios.keys() if c in columnas_validas and c != pk]
    if not sets:
      return self._json({"error": True, "mensaje": "Ninguna columna válida para actualizar"})

    set_clause = ", ".join(f"`{c}`=%s" for c in sets)
    sql = f"UPDATE `{tabla}` SET {set_clause} WHERE `{pk}`=%s"
    values = [cambios[c] for c in sets] + [pk_value]

    try:
      self.cursor.execute(sql, tuple(values))
      self.conexion.commit()
      return self._json({"actualizados": self.cursor.rowcount})
    except mysql.connector.Error as e:
      self.conexion.rollback()
      return self._json({"error": True, "mensaje": str(e), "sqlstate": getattr(e, "sqlstate", None)})

  def eliminar(self, tabla: str, pk_value):
    """Elimina una fila por PK simple en `tabla`."""
    self._validar_ident(tabla)
    pk = self._pk_column(tabla)
    if not pk:
      return self._json({"error": True, "mensaje": "Tabla sin PK simple, no se puede eliminar"})

    sql = f"DELETE FROM `{tabla}` WHERE `{pk}`=%s"
    try:
      self.cursor.execute(sql, (pk_value,))
      self.conexion.commit()
      return self._json({"eliminados": self.cursor.rowcount})
    except mysql.connector.Error as e:
      self.conexion.rollback()
      return self._json({"error": True, "mensaje": str(e), "sqlstate": getattr(e, "sqlstate", None)})

  # ---------- Cierre ----------

  def cerrar(self):
    try:
      if self.cursor: self.cursor.close()
      if self.conexion: self.conexion.close()
    except Exception:
      pass
  # --- FK helpers ---

  def fk_info(self, tabla: str):
    """
    Devuelve lista de FKs de `tabla`:
    [{col, ref_table, ref_column, label_column}]
    """
    self._validar_ident(tabla)
    sql = """
      SELECT k.COLUMN_NAME, k.REFERENCED_TABLE_NAME, k.REFERENCED_COLUMN_NAME
      FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE k
      WHERE k.TABLE_SCHEMA=%s AND k.TABLE_NAME=%s AND k.REFERENCED_TABLE_NAME IS NOT NULL
    """
    self.cursor.execute(sql, (self.basedatos, tabla))
    rows = self.cursor.fetchall()
    out = []
    for col, rtab, rcol in rows:
      # escoger columna "humana" de la tabla referenciada
      lbl = self.guess_label_column(rtab)
      out.append({"col": col, "ref_table": rtab, "ref_column": rcol, "label_column": lbl})
    return out

  def guess_label_column(self, tabla: str):
    """
    Heurística para columna 'humana' en tabla referenciada.
    """
    self._validar_ident(tabla)
    self.cursor.execute(f"DESCRIBE `{tabla}`")
    cols = list(self.cursor.fetchall())  # (Field, Type, Null, Key, Default, Extra)
    names = [c[0] for c in cols]
    # candidatos comunes
    preferred = ['nombre','name','titulo','title','descripcion','email','etiqueta','label']
    for cand in preferred:
      if cand in names:
        return cand
    # PK para excluir
    pk = None
    for c in cols:
      if len(c) >= 4 and c[3] == 'PRI':
        pk = c[0]; break
    # primer VARCHAR/TEXT que no sea PK
    for c in cols:
      colname, coltype = c[0], c[1].lower()
      if colname != pk and ('char' in coltype or 'text' in coltype):
        return colname
    # fallback: primera no PK
    for c in cols:
      if c[0] != pk:
        return c[0]
    # ultimísimo recurso
    return names[0] if names else None

  def seleccionar_humano(self, tabla: str):
    """
    Hace SELECT * con LEFT JOINs a las tablas referenciadas para traer labels.
    Devuelve: [{... , fkcol: id, fkcol__label: label, ...}, ...]
    """
    self._validar_ident(tabla)
    fks = self.fk_info(tabla)
    # base select
    base_alias = "t0"
    joins = []
    select_cols = []

    # columnas base
    self.cursor.execute(f"DESCRIBE `{tabla}`")
    base_cols = [r[0] for r in self.cursor.fetchall()]
    select_cols += [f"`{base_alias}`.`{c}` AS `{c}`" for c in base_cols]

    # joins por cada FK
    for i, fk in enumerate(fks, start=1):
      alias = f"t{i}"
      rtab = fk['ref_table']; rcol = fk['ref_column']; lcol = fk['label_column']
      if not lcol:
        lcol = self._pk_column(rtab)  # fallback
      joins.append(
        f"LEFT JOIN `{rtab}` `{alias}` ON `{base_alias}`.`{fk['col']}` = `{alias}`.`{rcol}`"
      )
      select_cols.append(f"`{alias}`.`{lcol}` AS `{fk['col']}__label`")

    sql = f"SELECT {', '.join(select_cols)} FROM `{tabla}` `{base_alias}` {' '.join(joins)}"
    self.cursor.execute(sql)
    columnas = self.cursor.column_names
    filas = self.cursor.fetchall()
    datos = [dict(zip(columnas, fila)) for fila in filas]
    meta = {
      "pk": self._pk_column(tabla),
      "fks": fks  # para que el front sepa qué columnas son FK y su label_column
    }
    return self._json({"rows": datos, "meta": meta})

  def fk_options(self, tabla: str):
    """
    Devuelve opciones para cada FK de `tabla`:
    { fkcol: [ {value:<id>, label:<texto>}, ... ], ... }
    """
    self._validar_ident(tabla)
    fks = self.fk_info(tabla)
    out = {}
    for fk in fks:
      rtab = fk['ref_table']
      pk = self._pk_column(rtab)
      lbl = fk['label_column'] or pk
      self.cursor.execute(f"SELECT `{pk}`, `{lbl}` FROM `{rtab}` ORDER BY `{lbl}` ASC")
      opts = [{"value": row[0], "label": row[1]} for row in self.cursor.fetchall()]
      out[fk['col']] = opts
    return self._json(out)

