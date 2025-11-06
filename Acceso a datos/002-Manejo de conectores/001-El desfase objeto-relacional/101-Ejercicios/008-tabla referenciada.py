import re
import mysql.connector

# ===================== DATOS (ejemplo corregido) =====================
clientes = [{
  "nombre":"Jose Vicente",
  "apellidos":"Carratala Sanchis",
  "dni":"45325345G",
  "edad":47,
  "emails":[
    {"tipo":"personal","direccion":"info@josevicentecarratala.com"},
    {"tipo":"empresa","direcciones":["info@jocarsa.com"]}
  ]
},{
  "nombre":"Jose Vicente",
  "apellidos":"Carratala Sanchis",
  "dni":"45325345G",
  "edad":45,
  "emails":[
    {"tipo":"personal","direccion":"info@josevicentecarratala.com"},
    {"tipo":"empresa","direcciones":["info@jocarsa.com"]}
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
    # Promociones simples
    pair = {a, b}
    if pair == {"INT", "DOUBLE"}:
        return "DOUBLE"
    if pair == {"TINYINT(1)", "INT"}:
        return "INT"
    # fallback
    return "TEXT"

# ===================== INFERENCIA DE ESQUEMA =====================
root_table = "clientes"

# Columnas escalares de la tabla principal
root_scalar_cols = {}  # nombre_col -> tipo_sql

# Para campos lista a nivel raíz: definiciones hijas
# child_defs[campo] = {"kind": "scalar_list"|"object_list",
#                      "cols": {k: tipo},   # solo si object_list
#                      "sub_scalar_lists": set(subcampos)}
child_defs = {}

for row in clientes:
    for k, v in row.items():
        if isinstance(v, list):
            # Analizar lista
            if len(v) == 0:
                # Lista vacía → asumimos lista de escalares (valor VARCHAR)
                child = child_defs.setdefault(k, {"kind":"scalar_list"})
            else:
                first = v[0]
                if isinstance(first, dict):
                    child = child_defs.setdefault(k, {"kind":"object_list","cols":{}, "sub_scalar_lists": set()})
                    # Unimos todas las claves posibles y tipos
                    for item in v:
                        if not isinstance(item, dict):
                            continue
                        for k2, v2 in item.items():
                            if isinstance(v2, list):
                                # Sublista (si es de escalares)
                                if len(v2) == 0 or not isinstance(v2[0], dict):
                                    child["sub_scalar_lists"].add(k2)
                                # (si fuese lista de dicts, aquí podrías añadir otra rama nieta de objetos)
                            elif isinstance(v2, dict):
                                # Nieto objeto: podrías extender aquí si lo necesitas
                                pass
                            else:
                                # Escalar en hijo
                                t = sql_scalar_type(v2)
                                if k2 in child["cols"]:
                                    child["cols"][k2] = merge_type(child["cols"][k2], t)
                                else:
                                    child["cols"][k2] = t
                else:
                    # Lista de escalares
                    child = child_defs.setdefault(k, {"kind":"scalar_list"})
        elif isinstance(v, dict):
            # Si quieres soportar dicts a nivel raíz como tabla hija 1-1, amplía aquí
            pass
        else:
            # Escalar en raíz
            t = sql_scalar_type(v)
            if k in root_scalar_cols:
                root_scalar_cols[k] = merge_type(root_scalar_cols[k], t)
            else:
                root_scalar_cols[k] = t

# ===================== SQL: CREACIÓN DE TABLAS =====================
conn = mysql.connector.connect(
    host="localhost",
    user="desfase",
    password="desfase",
    database="desfase"
)
cursor = conn.cursor()

def exec_safe(sql):
    # print(sql)  # descomenta para depurar
    cursor.execute(sql)

root_table_i = ident(root_table)
# Drop en orden seguro: nietas → hijas → raíz
# (Primero recopilamos nombres)
drop_order = []

child_table_names = {}
grandchild_table_names = []  # lista de (tabla_nieta)

for field, info in child_defs.items():
    child_name = f"{root_table_i}_{ident(field)}"
    child_table_names[field] = child_name
    if info.get("kind") == "object_list":
        for sub in info.get("sub_scalar_lists", []):
            grandchild_table_names.append(f"{child_name}_{ident(sub)}")

# 1) DROP nietas
for t in grandchild_table_names:
    exec_safe(f"DROP TABLE IF EXISTS `{t}`;")
# 2) DROP hijas
for t in child_table_names.values():
    exec_safe(f"DROP TABLE IF EXISTS `{t}`;")
# 3) DROP raíz
exec_safe(f"DROP TABLE IF EXISTS `{root_table_i}`;")

# === Crear raíz
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

# === Crear hijas
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

# === Crear nietas (sublistas escalares dentro de objetos)
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

print("Esquema generado:")
print(f"- Tabla raíz: {root_table_i} columnas escalares: {list(root_scalar_cols.keys())}")
for field, info in child_defs.items():
    print(f"- Hija: {child_table_names[field]} ({info['kind']})")
    if info["kind"] == "object_list":
        print(f"    columnas: {list(info.get('cols', {}).keys())}")
        if info.get("sub_scalar_lists"):
            for sub in info["sub_scalar_lists"]:
                print(f"    Nieta: {child_table_names[field]}_{ident(sub)} (valor)")

