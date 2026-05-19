# ⚡ Inicio Rápido - InmoWeb AI

Guía ultra-rápida para poner en marcha el proyecto en menos de 5 minutos.

---

## 🚀 3 Pasos para Empezar

### 1️⃣ Verificar Ollama

```bash
# Verificar que Ollama está instalado
ollama --version

# Listar modelos instalados
ollama list

# Si no está Qwen 2.5, instalarlo (esto tarda ~5 minutos)
ollama pull qwen2.5:7b-instruct-q4_0

# Verificar que funciona
ollama run qwen2.5:7b-instruct-q4_0 "Hola mundo"
```

### 2️⃣ Crear Entorno Virtual e Instalar Dependencias

```bash
# Navegar al directorio del proyecto
cd "d:\xampp\htdocs\DAM-2\Proyecto Intermodular II\301-Actividades final de unidad - Segundo trimestre\002-IA generativa\101-Ejercicios"

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# En Windows PowerShell:
.venv\Scripts\Activate.ps1
# En Windows CMD:
.venv\Scripts\activate.bat
# En Linux/Mac:
source .venv/bin/activate

# Instalar dependencias en el entorno virtual
pip install -r requirements.txt
```

### 3️⃣ Ejecutar

```bash
# Asegúrate de que el entorno virtual está activado (deberías ver (.venv) en el prompt)

# Iniciar el servidor
python app.py

# Abrir en el navegador
# http://localhost:5000
```

> 💡 **Nota:** Cada vez que abras una nueva terminal, deberás activar el entorno virtual con `.venv\Scripts\Activate.ps1` antes de ejecutar el proyecto.

---

## ✅ Verificación Rápida

Si todo funciona correctamente, deberías ver:

1. **En la terminal:**
   ```
   * Running on http://127.0.0.1:5000
   * Running on http://192.168.x.x:5000
   ```

2. **En el navegador:**
   - Sidebar azul con logo "InmoWebAI"
   - Formulario de generación
   - Panel de vista previa a la derecha

---

## 🎯 Primera Prueba

1. Haz clic en la plantilla **"👑 Inmobiliaria de Lujo"**
2. Haz clic en **"Generar Sitio Web"**
3. Espera 10-30 segundos
4. ¡Deberías ver un sitio web inmobiliario en el preview!

---

## ❌ Problemas Comunes

### "ModuleNotFoundError: No module named 'flask'"
```bash
pip install Flask requests
```

### "Connection refused" o "Error al generar"
- Ollama no está corriendo
- Solución: Abre Ollama o ejecuta `ollama serve` en otra terminal

### "Model not found"
```bash
ollama pull qwen2.5:7b-instruct-q4_0
```

### Puerto 5000 ocupado
En `app.py` línea final, cambia:
```python
app.run(host="0.0.0.0", port=5001, debug=True)
```

---

## 📚 Siguiente Paso

Lee el [README.md](README.md) completo para conocer todas las funcionalidades.

---

**¡Listo! Ya puedes empezar a generar sitios web inmobiliarios con IA 🏠✨**
