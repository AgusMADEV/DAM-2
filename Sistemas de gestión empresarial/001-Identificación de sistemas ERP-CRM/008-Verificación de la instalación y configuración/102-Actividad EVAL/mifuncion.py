import xml.etree.ElementTree as ET
import sqlite3

def miInterfaz(destino):
    cadena = "<form method='POST'>"
    # Parse the XML file
    tree = ET.parse(destino)
    root = tree.getroot()

    for campo in root:
        if campo.tag == "campotexto":
            cadena += f"<label for='{campo.get('nombre')}'>{campo.get('nombre').title()}:</label>"
            cadena += f"<input type='text' name='{campo.get('nombre')}' placeholder='{campo.get('nombre')}'><br>"
        elif campo.tag == "areadetexto":
            cadena += f"<label for='{campo.get('nombre')}'>{campo.get('nombre').title()}:</label>"
            cadena += f"<textarea name='{campo.get('nombre')}'></textarea><br>"
    
    cadena += "<input type='submit' value='Guardar'></form>"

    # Crear la tabla en la base de datos
    conexion = sqlite3.connect("odoo.db")
    cursor = conexion.cursor()
    
    # Recopilar los campos primero
    campos_sql = []
    for campo in root:
        if campo.tag == "campotexto":
            campos_sql.append(f'"{campo.get("nombre")}" TEXT')
        elif campo.tag == "areadetexto":
            campos_sql.append(f'"{campo.get("nombre")}" TEXT')
    
    # Construir la query SQL correctamente
    if campos_sql:
        peticion = f'''
        CREATE TABLE IF NOT EXISTS "interfaz" (
              "Identificador" INTEGER,
              {', '.join(campos_sql)},
              PRIMARY KEY("Identificador" AUTOINCREMENT)
        );
        '''
    else:
        peticion = '''
        CREATE TABLE IF NOT EXISTS "interfaz" (
              "Identificador" INTEGER,
              PRIMARY KEY("Identificador" AUTOINCREMENT)
        );
        '''

    cursor.execute(peticion)
    conexion.commit()
    conexion.close()

    return cadena

def guardarDatos(datos):
    """Función para guardar los datos del formulario en la base de datos"""
    conexion = sqlite3.connect("odoo.db")
    cursor = conexion.cursor()
    
    # Filtrar datos vacíos y construir la query de inserción dinámicamente
    datos_filtrados = {k: v for k, v in datos.items() if v.strip()}
    
    if datos_filtrados:
        campos = list(datos_filtrados.keys())
        valores = list(datos_filtrados.values())
        
        # Escapar nombres de campos con comillas dobles
        campos_escapados = [f'"{campo}"' for campo in campos]
        
        query = f"INSERT INTO interfaz ({', '.join(campos_escapados)}) VALUES ({', '.join(['?' for _ in valores])})"
        cursor.execute(query, valores)
        
        conexion.commit()
    
    conexion.close()