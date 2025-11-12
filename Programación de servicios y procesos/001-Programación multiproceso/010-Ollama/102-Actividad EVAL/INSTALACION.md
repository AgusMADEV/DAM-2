# 🚀 Guía de Instalación y Verificación

## ✅ Lista de Verificación Pre-Ejecución

Antes de ejecutar el programa, asegúrate de cumplir estos requisitos:

### 1. Python Instalado
```powershell
python --version
```
Debe mostrar Python 3.x o superior

### 2. Ollama Instalado y Ejecutándose
```powershell
# Verificar que Ollama está ejecutándose
curl http://localhost:11434/api/tags
```
Debe devolver una respuesta JSON con los modelos instalados

### 3. Modelo Descargado
```powershell
# Listar modelos disponibles
ollama list
```
Debe aparecer `qwen2.5:7b-instruct-q4_0` en la lista

Si no está instalado:
```powershell
ollama pull qwen2.5:7b-instruct-q4_0
```

### 4. Archivos del Proyecto
Verifica que tienes todos estos archivos en la carpeta `102-Actividad EVAL`:

- ✅ `consulta_blog.py` - Programa principal
- ✅ `blog.sql` - Esquema de la base de datos
- ✅ `README.md` - Documentación principal
- ✅ `Respuesta.md` - Documento de respuesta detallado
- ✅ `EJEMPLOS_PREGUNTAS.md` - Ejemplos de preguntas
- ✅ `INSTALACION.md` - Este archivo

---

## 🔧 Instalación de Ollama (si no lo tienes)

### Windows

1. Descarga Ollama desde: https://ollama.ai/download
2. Ejecuta el instalador
3. Abre PowerShell y verifica:
```powershell
ollama --version
```

4. Descarga el modelo:
```powershell
ollama pull qwen2.5:7b-instruct-q4_0
```

### Linux/Mac

```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull qwen2.5:7b-instruct-q4_0
```

---

## ▶️ Ejecución del Programa

### Método 1: Línea de Comandos

1. Abre PowerShell
2. Navega a la carpeta:
```powershell
cd "d:\xampp\htdocs\DAM-2\Programación de servicios y procesos\001-Programación multiproceso\010-Ollama\102-Actividad EVAL"
```

3. Ejecuta el programa:
```powershell
python consulta_blog.py
```

### Método 2: Desde VS Code

1. Abre la carpeta en VS Code
2. Abre el archivo `consulta_blog.py`
3. Presiona `F5` o haz clic en "Run Python File"
4. El programa se ejecutará en el terminal integrado

---

## 🧪 Prueba Rápida

Después de ejecutar el programa, prueba con esta pregunta simple:

```
¿Qué tablas tiene la base de datos?
```

**Respuesta esperada:**
- El programa debe cargar el esquema correctamente
- Debe mostrar los 5 pasos de ejecución
- Debe devolver información sobre las tablas `entradas` y `usuarios`

---

## ❗ Solución de Problemas

### Error: "No module named 'subprocess'"
**Causa**: Instalación de Python incorrecta  
**Solución**: Reinstala Python desde python.org

### Error: "curl no se reconoce como comando"
**Causa**: curl no está en el PATH (raro en Windows 10+)  
**Solución**: 
```powershell
# Verifica que curl existe
where.exe curl
```
Si no existe, actualiza Windows o instala curl manualmente

### Error: "Connection refused" o "Failed to connect to localhost"
**Causa**: Ollama no está ejecutándose  
**Solución**:
```powershell
# Windows: Reinicia el servicio de Ollama desde la bandeja del sistema
# O ejecuta:
ollama serve
```

### Error: "model not found"
**Causa**: El modelo no está descargado  
**Solución**:
```powershell
ollama pull qwen2.5:7b-instruct-q4_0
```

### Error: "No se encontró el archivo: blog.sql"
**Causa**: El archivo blog.sql no está en la misma carpeta  
**Solución**: Verifica que `blog.sql` está en la misma carpeta que `consulta_blog.py`

### El programa se queda esperando mucho tiempo
**Causa**: El modelo está procesando (puede tardar en primera ejecución)  
**Solución**: Espera hasta 2 minutos. Si tarda más, presiona Ctrl+C y reintenta

### Respuesta vacía o errores de parsing
**Causa**: Problema con el formato de respuesta de Ollama  
**Solución**: Verifica que Ollama está actualizado:
```powershell
ollama version
```

---

## 🔍 Verificación de Funcionamiento Correcto

Un programa que funciona correctamente mostrará:

```
======================================================================
               SISTEMA DE CONSULTAS SQL PARA BLOG
                    Powered by Ollama + Python
======================================================================

[1/5] Cargando esquema de la base de datos...
      ✓ Esquema cargado correctamente (XXXX caracteres)

[2/5] Esperando pregunta del usuario...
      Introduce tu pregunta sobre el blog: [TU PREGUNTA AQUÍ]
      ✓ Pregunta recibida: "[TU PREGUNTA]"

[3/5] Construyendo el prompt para el modelo de lenguaje...
      ✓ Prompt construido (XXXX caracteres)

[4/5] Enviando consulta al modelo Ollama...
      Modelo: qwen2.5:7b-instruct-q4_0
      URL: http://localhost:11434/api/generate
      Esperando respuesta... (esto puede tardar unos segundos)

      ✓ Respuesta recibida del modelo

[5/5] Procesando y presentando la respuesta...

======================================================================
RESPUESTA DEL SISTEMA:
======================================================================

[RESPUESTA DEL MODELO AQUÍ]

======================================================================

[✓] Proceso completado exitosamente.
```

---

## 📊 Requisitos del Sistema

### Mínimos
- **CPU**: 2 núcleos
- **RAM**: 4 GB
- **Disco**: 5 GB libres (para el modelo)
- **SO**: Windows 10/11, Linux, macOS

### Recomendados
- **CPU**: 4+ núcleos
- **RAM**: 8 GB o más
- **Disco**: SSD
- **SO**: Windows 11, Ubuntu 22.04+, macOS 13+

---

## 🎯 Verificación de Archivos

Verifica el contenido de cada archivo:

### `consulta_blog.py`
```powershell
python -m py_compile consulta_blog.py
```
No debe mostrar errores

### `blog.sql`
```powershell
Get-Content blog.sql | Select-Object -First 10
```
Debe mostrar comentarios SQL y CREATE TABLE

---

## 📝 Comandos Útiles

### Ver logs de Ollama (Linux/Mac)
```bash
journalctl -u ollama -f
```

### Reiniciar Ollama (Windows)
1. Click derecho en el icono de Ollama en la bandeja
2. Selecciona "Quit Ollama"
3. Vuelve a abrir Ollama desde el menú inicio

### Listar modelos instalados
```powershell
ollama list
```

### Eliminar un modelo (para reinstalar)
```powershell
ollama rm qwen2.5:7b-instruct-q4_0
ollama pull qwen2.5:7b-instruct-q4_0
```

---

## 🆘 Soporte

Si encuentras problemas:

1. Verifica todos los elementos de la lista de verificación
2. Revisa la sección de solución de problemas
3. Consulta los logs de Ollama
4. Verifica que todos los archivos están presentes
5. Asegúrate de tener conexión a localhost

---

## ✅ Checklist Final

Antes de considerar la instalación completa, verifica:

- [ ] Python instalado y funcionando
- [ ] Ollama instalado y ejecutándose
- [ ] Modelo `qwen2.5:7b-instruct-q4_0` descargado
- [ ] Todos los archivos del proyecto presentes
- [ ] Archivo `blog.sql` en la carpeta correcta
- [ ] `curl` disponible en PowerShell
- [ ] Conexión a `localhost:11434` funcionando
- [ ] Prueba rápida exitosa

---

## 🎓 Siguientes Pasos

Una vez verificada la instalación:

1. ✅ Lee `README.md` para entender el programa
2. ✅ Revisa `Respuesta.md` para detalles técnicos
3. ✅ Consulta `EJEMPLOS_PREGUNTAS.md` para ideas de pruebas
4. ✅ Ejecuta el programa con diferentes preguntas
5. ✅ Experimenta y aprende

---

**¡Todo listo para usar el Sistema de Consultas SQL! 🚀**
