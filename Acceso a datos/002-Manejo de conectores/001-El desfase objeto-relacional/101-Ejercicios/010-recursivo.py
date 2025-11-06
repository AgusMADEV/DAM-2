#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import hashlib
import mysql.connector
from collections import defaultdict, deque

# =============== CONFIG ===============
JSON_PATH = "./datos.json"   # <-- ruta del JSON externo
DB = {
    "host": "localhost",
    "user": "desfase",
    "password": "desfase",
    "database": "desfase",
}

# =============== IDENT & TYPES ===============
def ident(name: str) -> str:
    """Sanitiza identificadores MySQL (tabla/col)."""
    name = (name or "").strip().lower()
    name = re.sub(r'[^a-z0-9_]+', '_', name)
    name = re.sub(r'_+', '_', name).strip('_')
    if not name:
        name = "col"
    if name[0].isdigit():
        name = "n_" + name
    if name in {"index", "key", "primary", "value"}:
        name = "_" + name
    return name

def cap_name(name: str, maxlen: int = 64) -> str:
    """
    Corta y añade hash si excede maxlen. Úsalo para nombres de constraints/índices.
    """
    if len(name) <= maxlen:
        return name
    h = hashlib.sha1(name.encode("utf-8")).hexdigest()[:8]
    keep = maxlen - 1 - len(h)  # espacio para '_' + hash
    if keep < 1:
        keep = maxlen - len(h)   # por si acaso
    return f"{name[:keep]}_{h}"

def fk_name(child: str, parent: str) -> str:
    return cap_name(f"fk_{child}_{parent}", 64)

def idx_name(child: str, parent: str) -> str:
    # podemos usar el mismo patrón
    return cap_name(f"fk_{child}_{parent}", 64)

def sql_scalar_type(v):
    """Mapeo conservador a tipos MySQL."""
    if isinstance(v, bool):  return "TINYINT(1)"
    if isinstance(v, int):   return "INT"
    if isinstance(v, float): return "DOUBLE"
    return "TEXT"  # robusto para cadenas largas

def merge_type(a, b):
    if a == b: return a
    pair = {a, b}
    if "TEXT" in pair: return "TEXT"
    if pair == {"INT", "DOUBLE"}: return "DOUBLE"
    if pair == {"TINYINT(1)", "INT"}: return "INT"
    return "TEXT"

def join_path(*parts) -> str:
    return ident("_".join([ident(p) for p in parts if p]))

# =============== TABLE DEF ===============
class TableDef:
    """kind: 'dict' | 'list_scalar'"""
    def __init__(self, name, parent=None, relname=None, kind='dict'):
        self.name = ident(name)
        self.parent = parent       # nombre tabla padre o None
        self.relname = relname     # nombre del campo en el padre
        self.kind = kind
        self.columns = {}          # solo para dict: col -> tipo SQL
        self.children = set()      # nombres de tablas hijas

tables: dict[str, TableDef] = {}
edges = set()  # (parent, child)

def ensure_table(name, parent=None, relname=None, kind='dict') -> TableDef:
    tname = ident(name)
    if tname not in tables:
        tables[tname] = TableDef(tname, parent, relname, kind)
    else:
        # subir de list_scalar a dict si hace falta
        if tables[tname].kind == 'list_scalar' and kind == 'dict':
            tables[tname].kind = 'dict'
    if parent:
        p = ident(parent)
        edges.add((p, tname))
        tables[p].children.add(tname)
    return tables[tname]

# =============== SCHEMA INFERENCE (RECURSIVE) ===============
def infer_value(path_table: str, value, parent_table: str | None, relname: str | None):
    if isinstance(value, dict):
        t = ensure_table(path_table, parent_table, relname, kind='dict')
        for k, v in value.items():
            if isinstance(v, (dict, list)):
                infer_value(join_path(path_table, k), v, t.name, k)
            else:
                col = ident(k)
                ttype = sql_scalar_type(v)
                t.columns[col] = merge_type(t.columns.get(col, ttype), ttype)

    elif isinstance(value, list):
        # decide por primer elemento; lista vacía => escalar
        elem_kind = "scalar"
        for el in value:
            elem_kind = "dict" if isinstance(el, dict) else "scalar"
            break
        if elem_kind == "dict":
            t = ensure_table(path_table, parent_table, relname, kind='dict')
            for el in value:
                if not isinstance(el, dict):
                    continue
                for k, v in el.items():
                    if isinstance(v, (dict, list)):
                        infer_value(join_path(path_table, k), v, t.name, k)
                    else:
                        col = ident(k)
                        ttype = sql_scalar_type(v)
                        t.columns[col] = merge_type(t.columns.get(col, ttype), ttype)
        else:
            ensure_table(path_table, parent_table, relname, kind='list_scalar')

    else:
        # escalar en raíz (poco frecuente), lo modelamos como dict con 'valor'
        if parent_table is None:
            t = ensure_table(path_table, None, relname, kind='dict')
            t.columns['valor'] = merge_type(t.columns.get('valor', sql_scalar_type(value)),
                                            sql_scalar_type(value))

# =============== TOPO SORT & DDL ===============
def topo_tables():
    indeg = defaultdict(int)
    graph = defaultdict(list)
    for p, c in edges:
        graph[p].append(c)
        indeg[c] += 1
        if p not in indeg:
            indeg[p] = indeg[p]
    roots = [t for t in tables if indeg[t] == 0]
    q = deque(roots); out = []; seen = set()
    while q:
        u = q.popleft()
        if u in seen: continue
        seen.add(u); out.append(u)
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    for t in tables:
        if t not in seen: out.append(t)
    return out

def drop_entire_schema(cursor, dbname: str):
    """Elimina TODAS las tablas de la BD ignorando FKs."""
    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
    try:
        cursor.execute("""
            SELECT TABLE_NAME FROM information_schema.tables
            WHERE table_schema = %s
        """, (dbname,))
        for (tname,) in cursor.fetchall():
            cursor.execute(f"DROP TABLE IF EXISTS `{tname}`;")
    finally:
        cursor.execute("SET FOREIGN_KEY_CHECKS=1;")

def create_all(cursor):
    order = topo_tables()
    # Desactivar FKs para DROP/CREATE
    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
    try:
        # DROP hijos→padres (por si hubiera residuos)
        for t in reversed(order):
            cursor.execute(f"DROP TABLE IF EXISTS `{t}`;")
        # CREATE padres→hijos
        for tname in order:
            t = tables[tname]
            cols = ["`Identificador` INT NOT NULL AUTO_INCREMENT"]
            if t.parent:
                cols.append(f"`{t.parent}_id` INT NOT NULL")
            if t.kind == 'dict':
                for c, typ in t.columns.items():
                    cols.append(f"`{ident(c)}` {typ} DEFAULT NULL")
            else:
                cols += ["`idx` INT NOT NULL", "`valor` TEXT DEFAULT NULL"]
            cols.append("PRIMARY KEY (`Identificador`)")

            # nombres de índice y constraint acotados a 64 chars
            fk_idx_sql = ""
            fk_sql = ""
            if t.parent:
                keyn = idx_name(t.name, t.parent)
                fkn = fk_name(t.name, t.parent)
                fk_idx_sql = f", KEY `{keyn}` (`{t.parent}_id`)"
                fk_sql = (f", CONSTRAINT `{fkn}` FOREIGN KEY (`{t.parent}_id`)"
                          f" REFERENCES `{t.parent}` (`Identificador`)"
                          f" ON DELETE CASCADE ON UPDATE CASCADE")

            ddl = f"""CREATE TABLE `{t.name}` (
              {", ".join(cols)}
              {fk_idx_sql}
              {fk_sql}
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"""
            cursor.execute(ddl)
    finally:
        cursor.execute("SET FOREIGN_KEY_CHECKS=1;")

# =============== INSERT (RECURSIVE) ===============
def insert_dict_row(cursor, tdef: TableDef, data: dict, parent_id: int | None):
    # columnas escalares
    cols = []
    vals = []
    for c in tdef.columns:
        cols.append(f"`{ident(c)}`")
        v = data.get(c, None)
        if isinstance(v, (dict, list)): v = None
        vals.append(v)
    # FK
    if tdef.parent:
        cols.insert(0, f"`{tdef.parent}_id`")
        vals.insert(0, parent_id)
    # INSERT
    if cols:
        sql = f"INSERT INTO `{tdef.name}` ({', '.join(cols)}) VALUES ({', '.join(['%s']*len(cols))})"
        cursor.execute(sql, vals)
    else:
        if tdef.parent:
            cursor.execute(f"INSERT INTO `{tdef.name}` (`{tdef.parent}_id`) VALUES (%s)", (parent_id,))
        else:
            cursor.execute(f"INSERT INTO `{tdef.name}` () VALUES ()")
    new_id = cursor.lastrowid

    # hijos
    for k, v in data.items():
        if not isinstance(v, (dict, list)): 
            continue
        child_name = join_path(tdef.name, k)
        child = tables.get(child_name)
        if child is None:
            if isinstance(v, dict):
                child = ensure_table(child_name, tdef.name, k, kind='dict')
                insert_dict_row(cursor, child, {}, new_id)
            continue
        if child.kind == 'dict':
            if isinstance(v, dict):
                insert_dict_row(cursor, child, v, new_id)
            else:
                for el in v:
                    if isinstance(el, dict):
                        insert_dict_row(cursor, child, el, new_id)
        else:
            insert_list_scalar(cursor, child, v, new_id)
    return new_id

def insert_list_scalar(cursor, tdef: TableDef, value, parent_id: int | None):
    if not isinstance(value, list): value = [value]
    sql = f"INSERT INTO `{tdef.name}` (`{tdef.parent}_id`, `idx`, `valor`) VALUES (%s, %s, %s)"
    for i, el in enumerate(value):
        if isinstance(el, (dict, list)):
            try:
                val = json.dumps(el, ensure_ascii=False)
            except Exception:
                val = None
        else:
            val = el
        cursor.execute(sql, (parent_id, i, val))

# =============== RUN (NO CLI) ===============
def run():
    # 1) Cargar JSON
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        root = json.load(f)
    if not isinstance(root, dict):
        raise ValueError("El JSON raíz debe ser un objeto: cada clave es una tabla padre top-level.")

    # 2) Inferencia de esquema
    tables.clear(); edges.clear()
    for top_key, top_val in root.items():
        top_table = ident(top_key)  # p.ej., 'clientes'
        if isinstance(top_val, list):
            for el in top_val:
                infer_value(top_table, el, parent_table=None, relname=None)
        else:
            infer_value(top_table, top_val, parent_table=None, relname=None)

    # 3) Conectar y reset total de BD
    conn = mysql.connector.connect(**DB)
    cur = conn.cursor()
    drop_entire_schema(cur, DB["database"])
    conn.commit()

    # 4) Crear esquema nuevo
    create_all(cur)
    conn.commit()

    # 5) Insertar datos
    for top_key, top_val in root.items():
        top_table = tables[ident(top_key)]
        if isinstance(top_val, list):
            for el in top_val:
                row = el if isinstance(el, dict) else {"valor": el}
                insert_dict_row(cur, top_table, row, parent_id=None)
        elif isinstance(top_val, dict):
            insert_dict_row(cur, top_table, top_val, parent_id=None)
        else:
            insert_dict_row(cur, top_table, {"valor": top_val}, parent_id=None)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Reset completado, esquema creado e inserción realizada con éxito.")

if __name__ == "__main__":
    run()

