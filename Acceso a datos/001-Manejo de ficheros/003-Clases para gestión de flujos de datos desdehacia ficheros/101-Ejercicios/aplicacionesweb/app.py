#!/usr/bin/env python3
"""
app.py — Backend Flask para demo de codificación de texto en imagen.

- Sirve una UI (index) con formulario.
- Recibe datos JSON de cliente (name, surname, email, phone).
- Llama al codificador (coder.py) para generar el PNG.
- Devuelve el PNG directamente en la respuesta (Content-Type: image/png).
"""

import io
import json
from flask import Flask, render_template, request, Response
from coder import encode_to_image  # importamos tu función del script coder/decoder (mismo directorio)
from PIL import Image

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.post("/encode")
def encode():
    """
    Espera JSON como:
        {
          "name": "...",
          "surname": "...",
          "email": "...",
          "phone": "..."
        }
    Responde: image/png con el PNG generado.
    """
    try:
        data = request.get_json(silent=True) or {}
        required = ("name","surname","email","phone")
        if any(not data.get(k) for k in required):
            return Response("Faltan campos obligatorios.", status=400)

        # Serializamos a JSON con UTF-8 garantizado; esto es lo que iría dentro de la imagen
        text = json.dumps({
            "name": data["name"],
            "surname": data["surname"],
            "email": data["email"],
            "phone": data["phone"],
        }, ensure_ascii=False)

        # Usamos encode_to_image para obtener un archivo temporal en memoria.
        # La función original guarda a disco; aquí generamos en memoria con Pillow para evitar I/O.
        # Implementamos el mismo pipeline que encode_to_image: construimos header, payload y la imagen.
        # — Para mantener la “llamada al script”, podemos reutilizar las rutinas internas:
        #   import coder y reusar bytes_to_pixels + header composition, o
        #   crear un pequeño helper aquí. Para claridad, llamamos a encode_to_image a un buffer.
        #
        # Truco: llamamos a encode_to_image pero con un archivo-like BytesIO usando save() después.
        # Realmente encode_to_image espera una ruta; así que replicamos ruta-interna con PIL en memoria:

        # === Variante totalmente en memoria (idéntica a encode_to_image) ===
        from coder import MAGIC, bytes_to_pixels
        import zlib

        text_bytes = text.encode("utf-8")
        length = len(text_bytes)
        crc = zlib.crc32(text_bytes) & 0xFFFFFFFF
        header = MAGIC + length.to_bytes(4, "big") + crc.to_bytes(4, "big")
        payload = header + text_bytes

        payload_padded, side = bytes_to_pixels(payload)
        img = Image.new("RGB", size=(side, side), color=(0, 0, 0))
        pixels = img.load()

        idx = 0
        total = len(payload_padded)
        for y in range(side):
            for x in range(side):
                if idx + 3 <= total:
                    r = payload_padded[idx]
                    g = payload_padded[idx + 1]
                    b = payload_padded[idx + 2]
                    pixels[x, y] = (r, g, b)
                    idx += 3
                else:
                    break

        # Guardamos a un buffer en memoria
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        return Response(buf.read(), mimetype="image/png",
                        headers={"Content-Disposition": "inline; filename=cliente.png"})

    except Exception as e:
        return Response(f"Error al codificar: {e}", status=500)


if __name__ == "__main__":
    # pip install flask pillow
    # FLASK_APP=app.py flask run  (o)  python app.py
    app.run(host="0.0.0.0", port=5000, debug=True)

