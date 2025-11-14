from flask import Flask, request
from mifuncion import miInterfaz, guardarDatos
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    # GET -> muestra formulario, POST -> inserta datos
    if request.method == 'POST':
        # Obtener campos dinámicamente del XML
        tree = ET.parse("interfaz.xml")
        root = tree.getroot()
        
        datos = {}
        for campo in root:
            nombre_campo = campo.get('nombre')
            if nombre_campo:
                datos[nombre_campo] = request.form.get(nombre_campo, '')
        
        # Guardar en la base de datos
        guardarDatos(datos)
        
        return f"<h2>Datos guardados correctamente!</h2><p>Se han guardado los siguientes datos:</p><ul>{''.join([f'<li><strong>{k}:</strong> {v}</li>' for k, v in datos.items() if v.strip()])}</ul><br><a href='/'>Volver al formulario</a>"
    else:
        return miInterfaz("interfaz.xml")

if __name__ == '__main__':
    app.run(debug=True)