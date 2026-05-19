# 🎬 PRIMEROS PASOS - Ejecución del Proyecto

## 🚀 Tutorial Paso a Paso para Principiantes

Este documento te guiará en la primera ejecución del proyecto. **Tiempo estimado: 5-10 minutos**

---

## ✅ PASO 1: Verificar Requisitos

### Windows

Abre **PowerShell** o **CMD** y ejecuta:

```cmd
python --version
```

**Resultado esperado**: `Python 3.7.0` o superior

Si no funciona:
- Descarga Python desde: https://www.python.org/downloads/
- Durante la instalación, marca "Add Python to PATH"

### Linux/Mac

Abre **Terminal** y ejecuta:

```bash
python3 --version
```

**Resultado esperado**: `Python 3.7.0` o superior

---

## ✅ PASO 2: Navegar al Proyecto

### Windows (PowerShell/CMD)

```cmd
cd "d:\xampp\htdocs\DAM-2\Acceso a datos\301-Actividades final de unidad - Segundo trimestre\001-Proyecto en el cual me demostréis que podéis leer multiples formatos de archivo\101-Ejercicios"
```

### Linux/Mac (Terminal)

```bash
cd "/ruta/completa/al/proyecto/101-Ejercicios"
```

**Verificar que estás en el lugar correcto:**

```bash
# Listar archivos
dir      # Windows
ls       # Linux/Mac
```

**Deberías ver:**
- 001-gestion_biblioteca.py
- 002-sistema_hash.py
- 003-serializacion_pickle.py
- 004-esteganografia.py
- 005-explorador_directorios.py
- 006-programa_principal.py
- README.md
- requirements.txt

---

## ✅ PASO 3: Instalar Dependencias

### Opción A: Script Automático (Recomendado)

**Windows:**
```cmd
instalar.bat
```

**Linux/Mac:**
```bash
chmod +x instalar.sh
./instalar.sh
```

### Opción B: Manual

```bash
pip install -r requirements.txt
```

**Resultado esperado:**
```
Collecting Pillow>=10.0.0
  Installing collected packages: Pillow
Successfully installed Pillow-10.0.0
```

Si ya está instalado:
```
Requirement already satisfied: Pillow
```

---

## ✅ PASO 4: Primera Ejecución

### Ejecutar el Programa Principal

```bash
python 006-programa_principal.py
```

**Verás el menú principal:**

```
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║         🏛️  BIBLIOTECA DIGITAL 📚                        ║
║                                                          ║
║      Sistema Integral de Gestión de Datos                ║
║           Versión 1.0 - 2026                            ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

============================================================
MENÚ PRINCIPAL
============================================================

1. 📝 Gestión de Archivos de Texto (CSV/TXT)
2. 🔍 Sistema de Búsqueda con Hashes
3. 🔒 Serialización Binaria (Pickle)
4. 🖼️  Esteganografía en Imágenes
5. 📂 Explorador de Directorios
6. 🎯 Demostración Completa
7. ℹ️  Información del Proyecto
0. ❌ Salir

Selecciona una opción:
```

---

## ✅ PASO 5: Ejecutar Demostración Completa

1. **Escribe**: `6`
2. **Presiona**: `Enter`
3. **Confirma**: `s` (cuando te pregunte si deseas continuar)

**¿Qué hará?**

Ejecutará automáticamente todos los módulos en secuencia:

1. ✅ **Archivos de Texto** (~30 segundos)
   - Crea estructura de directorios
   - Guarda 4 libros en CSV
   - Crea logs en TXT

2. ✅ **Sistema de Hashes** (~30 segundos)
   - Guarda 5 libros con índice MD5
   - Demuestra búsqueda O(1)
   - Genera estadísticas

3. ✅ **Serialización Pickle** (~30 segundos)
   - Crea objetos Libro completos
   - Serializa con métodos y atributos
   - Compara con JSON

4. ✅ **Esteganografía** (~45 segundos)
   - Crea imagen base
   - Oculta datos en imagen
   - Decodifica y verifica

5. ✅ **Explorador de Directorios** (~30 segundos)
   - Muestra árbol de archivos
   - Genera estadísticas
   - Busca por extensión

**Tiempo total**: ~2-3 minutos

---

## ✅ PASO 6: Verificar Resultados

Después de la ejecución, verás archivos generados en:

```
biblioteca_datos/
├── texto/           → CSV y TXT
├── hash/            → JSON con hashes
├── binario/         → Archivos pickle
├── imagenes/        → Imágenes con datos ocultos
└── logs/            → Informes del sistema
```

**Comprobar archivos creados:**

```bash
# Windows
tree /F biblioteca_datos

# Linux/Mac
ls -R biblioteca_datos
```

---

## ✅ PASO 7: Explorar Módulos Individuales

Después de la demo completa, prueba los módulos individuales:

### Opción 1: Archivos de Texto

```bash
python 001-gestion_biblioteca.py
```

**Verás:**
- Creación de directorios
- Guardado de libros en CSV
- Logs con timestamp

### Opción 2: Sistema de Hashes

```bash
python 002-sistema_hash.py
```

**Verás:**
- Generación de hashes MD5
- Búsqueda instantánea
- Comparación O(1) vs O(n)

### Opción 3: Serialización Pickle

```bash
python 003-serializacion_pickle.py
```

**Verás:**
- Objetos completos guardados
- Preservación de métodos
- Comparación Pickle vs JSON

### Opción 4: Esteganografía

```bash
python 004-esteganografia.py
```

**Verás:**
- Creación de imagen base
- Codificación de datos invisibles
- Decodificación exitosa

### Opción 5: Explorador

```bash
python 005-explorador_directorios.py
```

**Verás:**
- Árbol visual de directorios
- Estadísticas de archivos
- Búsquedas por tipo

---

## 🎯 FLUJO RECOMENDADO PARA EVALUACIÓN

### Para Profesor/Evaluador (10 minutos)

1. **Leer**: `RESUMEN_EJECUTIVO.md` (3 minutos)

2. **Ejecutar**:
   ```bash
   python 006-programa_principal.py
   ```
   Opción 6 → Demo completa (3 minutos)

3. **Verificar** archivos generados (2 minutos):
   ```bash
   tree /F biblioteca_datos
   ```

4. **Revisar** código fuente de 1-2 módulos (2 minutos)

### Para Estudiante (30 minutos)

1. **Leer**: `GUIA_RAPIDA.md` (5 minutos)

2. **Ejecutar** módulos individuales (15 minutos):
   - Cada módulo uno por uno
   - Observar resultados
   - Entender flujo

3. **Leer**: `README.md` completo (10 minutos)

4. **Experimentar**: Modificar datos y volver a ejecutar

---

## ❓ PROBLEMAS COMUNES Y SOLUCIONES

### Error: "python no se reconoce"

**Problema**: Python no está en PATH

**Solución**:
```bash
# Windows - usar py en lugar de python
py 006-programa_principal.py

# O reinstalar Python marcando "Add to PATH"
```

### Error: "No module named 'PIL'"

**Problema**: Pillow no instalado

**Solución**:
```bash
pip install Pillow
```

### Error: "biblioteca_datos no existe"

**Problema**: Todavía no se han ejecutado los módulos

**Solución**: Esto es normal la primera vez. Los directorios se crean automáticamente al ejecutar.

### Error: "Permission denied"

**Problema**: No tienes permisos en el directorio

**Solución**:
```bash
# Linux/Mac - dar permisos
chmod +x instalar.sh
```

### Los archivos no se generan

**Problema**: Estás en el directorio incorrecto

**Solución**: Verifica con `pwd` (Linux) o `cd` (Windows) que estás en `101-Ejercicios/`

---

## 📱 EJECUCIÓN EN DIFERENTES ENTORNOS

### Visual Studio Code

1. Abre la carpeta del proyecto en VSCode
2. Abrir terminal integrada: `Ctrl + ñ` o `Ctrl + ``
3. Ejecutar:
   ```bash
   python 006-programa_principal.py
   ```

### PyCharm

1. Abre el proyecto
2. Click derecho en `006-programa_principal.py`
3. "Run '006-programa_principal'"

### Jupyter Notebook

```python
# Ejecutar en una celda
!python 006-programa_principal.py
```

---

## 🎓 DESPUÉS DE LA PRIMERA EJECUCIÓN

### Qué revisar:

1. **Archivos CSV** en `biblioteca_datos/texto/`
   - Abre `libros.csv` con Excel o Bloc de notas
   - Verifica formato estructurado

2. **Archivos Hash** en `biblioteca_datos/hash/`
   - Abre cualquier `.json`
   - Observa que el nombre es un hash MD5

3. **Archivos Pickle** en `biblioteca_datos/binario/`
   - Son binarios, no legibles
   - Representan objetos Python completos

4. **Imágenes** en `biblioteca_datos/imagenes/`
   - Abre `portada_biblioteca.png`
   - Abre `portada_con_datos.png`
   - Son visualmente idénticas (datos ocultos)

5. **Logs** en `biblioteca_datos/logs/`
   - Abre `informe_biblioteca.json`
   - Verifica estructura JSON con estadísticas

### Qué aprender:

- **CSV**: Datos tabulares legibles
- **Hash**: Indexación rápida O(1)
- **Pickle**: Objetos completos con métodos
- **Esteganografía**: Datos ocultos invisibles
- **Explorador**: Análisis del sistema

---

## 📚 SIGUIENTES PASOS

### Explorar la Documentación

1. **README.md** - Visión general
2. **MEMORIA.md** - Detalles técnicos
3. **HISTORIAL_VERSIONES.md** - Evolución del desarrollo

### Modificar y Experimentar

1. Cambia los datos de los libros en cada módulo
2. Añade más libros al sistema
3. Prueba con tus propias imágenes para esteganografía
4. Modifica el menú del programa principal

### Leer el Código

1. Empieza por `001-gestion_biblioteca.py` (más simple)
2. Continúa con `002-sistema_hash.py`
3. Avanza progresivamente en complejidad

---

## ✅ CHECKLIST DE VERIFICACIÓN

Usa este checklist para asegurar que todo funciona:

- [ ] Python instalado correctamente
- [ ] Navegas al directorio `101-Ejercicios`
- [ ] Instalaste Pillow con pip
- [ ] Ejecutaste `006-programa_principal.py`
- [ ] Seleccionaste opción 6 (Demo completa)
- [ ] Viste todos los módulos ejecutarse
- [ ] Se creó el directorio `biblioteca_datos`
- [ ] Hay archivos en `texto/`, `hash/`, `binario/`, `imagenes/`, `logs/`
- [ ] Puedes ejecutar módulos individuales
- [ ] Entiendes qué hace cada módulo

**Si marcaste todas las opciones**: ¡Felicitaciones! El proyecto funciona correctamente. 🎉

**Si alguna falla**: Revisa la sección de problemas comunes arriba.

---

## 🎯 OBJETIVO FINAL

Al terminar esta guía deberías:

✅ Tener el proyecto ejecutándose correctamente  
✅ Comprender qué hace cada módulo  
✅ Ver los archivos generados en cada formato  
✅ Estar listo para explorar el código  

---

## 📞 ¿NECESITAS MÁS AYUDA?

1. **Para uso básico**: Lee `GUIA_RAPIDA.md`
2. **Para entender el código**: Lee `README.md`
3. **Para detalles técnicos**: Lee `MEMORIA.md`
4. **Para ver la evolución**: Lee `HISTORIAL_VERSIONES.md`

---

**¡Disfruta explorando el proyecto!** 🚀

*Recuerda: Este proyecto demuestra 5 formatos diferentes de persistencia de datos. Cada uno tiene sus ventajas y casos de uso específicos.*
