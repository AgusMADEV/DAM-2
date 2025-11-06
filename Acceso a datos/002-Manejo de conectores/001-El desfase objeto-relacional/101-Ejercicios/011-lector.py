#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import mysql.connector
from collections import defaultdict

# ================== CONFIG ==================
DB = {
    "host": "localhost",
    "user": "desfase",
    "password": "desfase",
    "database": "desfase",
}
OUTPUT_JSON = "./dump_recuperado.json"

# ================== UTILS ==================
def fetchall_dict(cur, sql, params=None):
    cur.execute(sql, params or ())
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]

def is_list_scalar_table(columns: set[str]) -> bool:
    # Heurística: tabla con columnas idx y valor (además de Identificador y FK)
    return "idx" in columns and "valor" in columns

def child_field_name(parent: str, child: str) -> str:
    # Ej: parent='clientes', child='clientes_informacion_contacto_telefonos'
    # -> field = 'informacion_contacto_telefonos'
    prefix = parent + "_"
    if child.startswith(prefix):
        return child[len(prefix):]
    # Si por alguna razón no cumple, devolvemos el nombre tal cual
    return child

# ================== CONEXIÓN ==================
conn = mysql.connector.connect(**DB)
cur = conn.cursor()

# ================== DESCUBRIR ESQUEMA ==================
db = DB["database"]

# 1) Tablas existentes
tables = [r["TABLE_NAME"] for r in fetchall_dict(
    cur,
    """
    SELECT TABLE_NAME
    FROM information_schema.tables
    WHERE table_schema=%s AND TABLE_TYPE='BASE TABLE'
    """,
    (db,)
)]

if not tables:
    raise RuntimeError("No hay tablas en la base de datos.")

# 2) Columnas de cada tabla
table_columns: dict[str, list[str]] = {}
for t in tables:
    rows = fetchall_dict(cur, """
        SELECT COLUMN_NAME
        FROM information_schema.columns
        WHERE table_schema=%s AND table_name=%s
        ORDER BY ORDINAL_POSITION
    """, (db, t))
    table_columns[t] = [r["COLUMN_NAME"] for r in rows]

# 3) Relaciones FK (child -> parent)
#    Asumimos la convención del generador: FK desde child(`{parent}_id`) → parent(`Identificador`)
rels = fetchall_dict(cur, """
    SELECT
      kcu.TABLE_NAME AS child_table,
      kcu.COLUMN_NAME AS child_column,
      kcu.REFERENCED_TABLE_NAME AS parent_table,
      kcu.REFERENCED_COLUMN_NAME AS parent_column
    FROM information_schema.KEY_COLUMN_USAGE kcu
    WHERE kcu.TABLE_SCHEMA=%s
      AND kcu.REFERENCED_TABLE_NAME IS NOT NULL
""", (db,))

parent_of: dict[str, str] = {}               # child_table -> parent_table
fk_col_of_child: dict[str, str] = {}         # child_table -> fk col (e.g., clientes_id)
children_of: dict[str, list[str]] = defaultdict(list)  # parent_table -> [child_table]

for r in rels:
    child = r["child_table"]
    parent = r["parent_table"]
    parent_of[child] = parent
    fk_col_of_child[child] = r["child_column"]
    children_of[parent].append(child)

# 4) Tablas raíz (sin padre)
root_tables = [t for t in tables if t not in parent_of]

# ================== CARGA DE DATOS (CACHE) ==================
# Para eficiencia, cacheamos todas las filas por tabla
all_rows: dict[str, list[dict]] = {}
for t in tables:
    all_rows[t] = fetchall_dict(cur, f"SELECT * FROM `{t}`")

# Índices por PK (Identificador) por tabla (útil para mirar rápido una fila concreta si se necesita)
by_id: dict[str, dict[int, dict]] = {}
for t in tables:
    pk_idx = {}
    for row in all_rows[t]:
        pk_idx[row["Identificador"]] = row
    by_id[t] = pk_idx

# Índices por FK: child_rows_by_parent[(child_table, parent_id)] -> [rows]
child_rows_by_parent: dict[tuple[str, int], list[dict]] = defaultdict(list)
for child in parent_of:
    fk = fk_col_of_child[child]
    for row in all_rows[child]:
        pid = row.get(fk)
        if pid is not None:
            child_rows_by_parent[(child, pid)].append(row)

# ================== RECONSTRUCCIÓN RECURSIVA ==================
def build_node(table: str, row: dict) -> dict:
    """
    Reconstruye un nodo (dict) para una fila de la tabla dada:
    - Incluye columnas escalares propias (excepto Identificador y FK).
    - Recorre hijos: decide si son objeto (1 fila) o lista (2+ filas).
      - Si el hijo es list-scalar (idx, valor) → lista de valores ordenada por idx.
      - Si es dict → objeto (1) o lista (n).
    """
    cols = table_columns[table]
    fk_col = fk_col_of_child.get(table)  # None para tablas raíz
    # columnas que queremos volcar como escalares (excluimos Identificador y FK)
    scalar_cols = [c for c in cols if c not in {"Identificador", "idx", "valor"} and c != fk_col]

    node = {}
    for c in scalar_cols:
        node[c] = row.get(c)

    # Procesar hijos
    for child in children_of.get(table, []):
        rel_field = child_field_name(table, child)
        child_cols = set(table_columns[child])

        # Filas del hijo para este padre
        rows_child = child_rows_by_parent.get((child, row["Identificador"]), [])

        if not rows_child:
            continue

        if is_list_scalar_table(child_cols):
            # Lista de escalares: ordenar por idx y devolver [valor,...]
            seq = sorted(
                [(rc.get("idx"), rc.get("valor")) for rc in rows_child],
                key=lambda x: (x[0] if x[0] is not None else 0)
            )
            node[rel_field] = [val for _, val in seq]
        else:
            # Hijo dict: decidir si objeto o lista
            if len(rows_child) == 1:
                # objeto único
                child_row = rows_child[0]
                node[rel_field] = build_node(child, child_row)
            else:
                # varias filas → lista de objetos
                node[rel_field] = [build_node(child, r) for r in rows_child]

    return node

# ================== RECONSTRUIR RAÍZ ==================
# Por diseño de tu generador, los root tables suelen corresponder a listas en JSON.
# Así que devolvemos SIEMPRE una lista por cada raíz (aunque tenga 1 fila).
result = {}
for rt in root_tables:
    # filas de la raíz ordenadas por Identificador
    rows = sorted(all_rows[rt], key=lambda r: r["Identificador"])
    result[rt] = [build_node(rt, r) for r in rows]

# ================== SALIDA ==================
# 1) Como diccionario de Python:
python_dict_result = result

# 2) Guardar a JSON:
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(python_dict_result, f, ensure_ascii=False, indent=2)

print("✅ Recuperación completada.")
print(f"Tablas raíz detectadas: {', '.join(root_tables)}")
print(f"JSON guardado en: {OUTPUT_JSON}")

# (Opcional) imprimir una vista muy resumida
for k, v in python_dict_result.items():
    print(f"- {k}: {len(v)} elemento(s)")

