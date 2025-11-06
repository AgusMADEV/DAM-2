import re
import mysql.connector

# ===================== DATOS (ejemplo) =====================
clientes = [{
  "nombre": "Elena",
  "apellidos": "Botezatu",
  "dni": "48925673M",
  "edad": 31,
  "emails": [
    { "tipo": "personal", "direccion": "elena.botezatu@gmail.com" },
    { "tipo": "profesional", "direcciones": ["contacto@psicoelena.com"] }
  ]
}, {
  "nombre": "Elena",
  "apellidos": "Botezatu",
  "dni": "48925673M",
  "edad": 32,
  "emails": [
    { "tipo": "personal", "direccion": "elena.botezatu@gmail.com" },
    { "tipo": "profesional", "direcciones": ["contacto@psicoelena.com"] }
  ]
}]

# ===================== HELPERS =====================
def ident(name: str) -> str:
    """Sanitiza identificadores SQL."""
    name = (name or "").strip().lower()
    name = re.sub(r'[^a-z0-9_]+', '_', name)
    name = re.sub(r'_+', '_', name).strip('_')
    if not name:
        name = 'col'
    if name[0].isdigit():
        name = 'n_' + name
    return name

def sql_scalar_type(value):
    if isinstance(value, bool):
        return "TINYINT(1)"
    if isinstance(value, int):
        return "INT"
    if isinstance(value, float):
        return "DOUBLE"
    return "VARCHAR(255)"  # por defecto texto

def merge_type(a, b):
    if a == b:
        return a
    pair = {a, b}
    if pair == {"INT", "DOUBLE"}:
        return "DOUBLE"
    if pair == {"TINYINT(1)", "INT"}:
        return "INT"
    return "TEXT"

# ===================== INFERENCIA DE ESQUEMA =====================
root_table = "clientes"
root_table_i = ident(root_table)

root_scalar_cols = {}  # nombre_col -> tipo_sql
child_defs = {}        # campo -> {"kind": "scalar_list"/"object_list", "cols":{}, "sub_scalar_lists": set()}

for row in clientes:
    for k, v in row.items():
        if isinstance(v, list):
            if len(v) == 0:
                child_defs.setdefault(k, {"kind":"scalar_list"})
            else:
                first = v[0]
                if isinstance(first, dict):
                    child = child_defs.setdefault(k, {"kind":"object_list","cols":{}, "sub_scalar_lists": set()})
                    for item in v:
                        if not isinstance(item, dict):
                            continue
                        for k2, v2 in item.items():
                            if isinstance(v2, list):
                                # sublista escalar
                                if len(v2) == 0 or not isinstance(v2[0], dict):
                                    child["sub_scalar_lists"].add(k2)
                                # si fuese lista de dicts, se podría extender a bisnieta aquí
                            elif isinstance(v2, dict):
                                # nieto objeto (no implementado en este ejemplo)
                                pass
                            else:
                                t = sql_scalar_type(v2)
                                if k2 in child["cols"]:
                                    child["cols"][k2] = merge_type(child["cols"][k2], t)
                                else:
                                    child["cols"][k2] = t
                else:
                    child_defs.setdefault(k, {"kind":"scalar_list"})
        elif isinstance(v, dict):
            # dict a nivel raíz (1:1) — no implementado en este ejemplo
            pass
        else:
            t = sql_scalar_type(v)
            if k in root_scalar_cols:
                root_scalar_cols[k] = merge_type(root_scalar_cols[k], t)
            else:
                root_scalar_cols[k] = t

# ===================== CONEXIÓN & CREACIÓN DE TABLAS =====================
conn = mysql.connector.connect(
    host="localhost",
    user="desfase",
    password="desfase",
    database="desfase"
)
cursor = conn.cursor()

def exec_safe(sql):
    cursor.execute(sql)

child_table_names = {}
grandchild_table_names = []  # solo nombres para dropear/crear

for field, info in child_defs.items():
    child_name = f"{root_table_i}_{ident(field)}"
    child_table_names[field] = child_name
    if info.get("kind") == "object_list":
        for sub in info.get("sub_scalar_lists", []):
            grandchild_table_names.append(f"{child_name}_{ident(sub)}")

# Dropear en orden: nietas -> hijas -> raíz
for t in grandchild_table_names:
    exec_safe(f"DROP TABLE IF EXISTS `{t}`;")
for t in child_table_names.values():
    exec_safe(f"DROP TABLE IF EXISTS `{t}`;")
exec_safe(f"DROP TABLE IF EXISTS `{root_table_i}`;")

# Crear raíz
cols_sql = ["`Identificador` INT NOT NULL AUTO_INCREMENT"]
for col, t in root_scalar_cols.items():
    cols_sql.append(f"`{ident(col)}` {t} DEFAULT NULL")
cols_sql.append("PRIMARY KEY (`Identificador`)")
create_root = f"""
CREATE TABLE `{root_table_i}` (
  {", ".join(cols_sql)}
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
exec_safe(create_root)

# Crear hijas
for field, info in child_defs.items():
    child_name = child_table_names[field]
    lines = [
        "`Identificador` INT NOT NULL AUTO_INCREMENT",
        f"`{root_table_i}_id` INT NOT NULL"
    ]
    if info["kind"] == "scalar_list":
        lines.append("`valor` VARCHAR(255) DEFAULT NULL")
    else:  # object_list
        for k2, t2 in info.get("cols", {}).items():
            lines.append(f"`{ident(k2)}` {t2} DEFAULT NULL")
    lines.append("PRIMARY KEY (`Identificador`)")
    lines.append(f"KEY `fk_{child_name}_{root_table_i}` (`{root_table_i}_id`)")
    create_child = f"""
    CREATE TABLE `{child_name}` (
      {", ".join(lines)},
      CONSTRAINT `fk_{child_name}_{root_table_i}`
        FOREIGN KEY (`{root_table_i}_id`)
        REFERENCES `{root_table_i}` (`Identificador`)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    exec_safe(create_child)

# Crear nietas (sublistas escalares)
for field, info in child_defs.items():
    if info.get("kind") != "object_list":
        continue
    child_name = child_table_names[field]
    for sub in info.get("sub_scalar_lists", []):
        grand = f"{child_name}_{ident(sub)}"
        create_grand = f"""
        CREATE TABLE `{grand}` (
          `Identificador` INT NOT NULL AUTO_INCREMENT,
          `{child_name}_id` INT NOT NULL,
          `valor` VARCHAR(255) DEFAULT NULL,
          PRIMARY KEY (`Identificador`),
          KEY `fk_{grand}_{child_name}` (`{child_name}_id`),
          CONSTRAINT `fk_{grand}_{child_name}`
            FOREIGN KEY (`{child_name}_id`)
            REFERENCES `{child_name}` (`Identificador`)
            ON DELETE CASCADE
            ON UPDATE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        exec_safe(create_grand)

conn.commit()

# ===================== INSERCIÓN DE DATOS =====================
def insert_root_row(row: dict) -> int:
    """Inserta un registro en la tabla raíz y devuelve su ID."""
    cols = []
    vals = []
    ph = []
    for col in root_scalar_cols.keys():
        cols.append(f"`{ident(col)}`")
        vals.append(row.get(col, None))
        ph.append("%s")
    sql = f"INSERT INTO `{root_table_i}` ({', '.join(cols)}) VALUES ({', '.join(ph)})"
    cursor.execute(sql, vals)
    return cursor.lastrowid

def insert_child_scalar_list(child_table: str, parent_id: int, values):
    """Inserta lista de escalares como filas hija."""
    if not isinstance(values, list):
        return
    sql = f"INSERT INTO `{child_table}` (`{root_table_i}_id`, `valor`) VALUES (%s, %s)"
    for v in values:
        cursor.execute(sql, (parent_id, None if isinstance(v, (dict,list)) else v))

def insert_child_object_list(field: str, child_table: str, parent_id: int, items, info):
    """Inserta lista de objetos + sus sublistas escalares (nietas)."""
    if not isinstance(items, list):
        return
    # Preparar columnas del hijo
    child_cols = list(info.get("cols", {}).keys())
    col_id = f"`{root_table_i}_id`"
    cols_sql = [col_id] + [f"`{ident(c)}`" for c in child_cols]
    ph = ["%s"] * (1 + len(child_cols))
    sql = f"INSERT INTO `{child_table}` ({', '.join(cols_sql)}) VALUES ({', '.join(ph)})"

    # Para sublistas (nietas)
    sublists = list(info.get("sub_scalar_lists", []))
    grand_tables = { sub: f"{child_table}_{ident(sub)}" for sub in sublists }
    grand_sql = { sub: f"INSERT INTO `{grand_tables[sub]}` (`{child_table}_id`, `valor`) VALUES (%s, %s)" for sub in sublists }

    for obj in items:
        if not isinstance(obj, dict):
            continue
        row_vals = [parent_id]
        for c in child_cols:
            v = obj.get(c, None)
            if isinstance(v, (list, dict)):
                # columnas del hijo solo guardan escalares
                row_vals.append(None)
            else:
                row_vals.append(v)
        cursor.execute(sql, row_vals)
        child_id = cursor.lastrowid

        # Sublistas escalares → nietas
        for sub in sublists:
            arr = obj.get(sub, None)
            if isinstance(arr, list):
                for el in arr:
                    cursor.execute(grand_sql[sub], (child_id, el if not isinstance(el, (dict,list)) else None))

def insert_data(data_rows):
    for row in data_rows:
        rid = insert_root_row(row)
        # recorrer campos para hijas
        for field, info in child_defs.items():
            values = row.get(field, None)
            if values is None:
                continue
            child_table = child_table_names[field]
            if info["kind"] == "scalar_list":
                insert_child_scalar_list(child_table, rid, values)
            else:
                insert_child_object_list(field, child_table, rid, values, info)

insert_data(clientes)
conn.commit()

print("Inserción completada.")
print(f"Registros insertados en `{root_table_i}`: {cursor.rowcount} (último batch puede no reflejar total)")

