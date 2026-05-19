# 🚀 GUÍA RÁPIDA DE USO

## Instalación en 3 Pasos

### Windows
```cmd
cd "ruta\del\proyecto\101-Ejercicios"
instalar.bat
```

### Linux/Mac
```bash
cd "ruta/del/proyecto/101-Ejercicios"
chmod +x instalar.sh
./instalar.sh
```

### Manual
```bash
pip install -r requirements.txt
```

## Ejecución

### Programa Principal (Recomendado)
```bash
python 006-programa_principal.py
```

**Menú disponible:**
1. 📝 Archivos de Texto
2. 🔍 Sistema de Hashes
3. 🔒 Serialización Pickle
4. 🖼️ Esteganografía
5. 📂 Explorador de Directorios
6. 🎯 **Demostración Completa** ⭐ (ejecuta todo)
7. ℹ️ Información

### Módulos Individuales
```bash
python 001-gestion_biblioteca.py      # Archivos CSV/TXT
python 002-sistema_hash.py             # Hashes MD5
python 003-serializacion_pickle.py     # Pickle binario
python 004-esteganografia.py           # Esteganografía
python 005-explorador_directorios.py   # Explorador
```

## ¿Qué hace cada módulo?

### 1️⃣ Gestión de Biblioteca (Texto)
- ✅ Guarda libros en CSV
- ✅ Lee libros desde CSV  
- ✅ Registra actividad en TXT
- 📊 **Resultado**: `biblioteca_datos/texto/`

### 2️⃣ Sistema de Hashes
- ✅ Genera hash MD5 del ISBN
- ✅ Búsqueda instantánea O(1)
- ✅ 1000x más rápido que búsqueda secuencial
- 📊 **Resultado**: `biblioteca_datos/hash/`

### 3️⃣ Serialización Pickle
- ✅ Guarda objetos Python completos
- ✅ Preserva métodos y atributos
- ✅ Más eficiente que JSON para objetos
- 📊 **Resultado**: `biblioteca_datos/binario/`

### 4️⃣ Esteganografía
- ✅ Oculta datos en imágenes
- ✅ Modificación imperceptible
- ✅ Capacidad: 180 KB en 800x600 px
- 📊 **Resultado**: `biblioteca_datos/imagenes/`

### 5️⃣ Explorador de Directorios
- ✅ Muestra árbol completo
- ✅ Genera estadísticas
- ✅ Busca por extensión/nombre
- 📊 **Resultado**: `biblioteca_datos/logs/`

## Datos Generados

Después de ejecutar, encontrarás:

```
biblioteca_datos/
├── texto/
│   ├── libros.csv          # Catálogo en CSV
│   └── registro.txt        # Log de actividades
│
├── hash/
│   ├── 5016c5d6...json     # Libro 1
│   ├── 382c8905...json     # Libro 2
│   └── ...                 # Más libros
│
├── binario/
│   ├── libro_001.pkl       # Objeto serializado
│   ├── coleccion.pkl       # Colección completa
│   └── estado.pkl          # Estado del sistema
│
├── imagenes/
│   ├── portada_biblioteca.png       # Imagen base
│   └── portada_con_datos.png        # Con datos ocultos
│
└── logs/
    └── informe_biblioteca.json      # Informe del sistema
```

## Casos de Uso

### Buscar un libro por ISBN (Hash)
```python
from importlib import import_module
modulo = import_module('002-sistema_hash')
biblioteca = modulo.BibliotecaHash()
libro = biblioteca.buscar_libro_por_isbn("978-0-7432-7356-5")
print(libro['titulo'])  # "Cien años de soledad"
```

### Ocultar datos secretos en imagen
```python
from importlib import import_module
modulo = import_module('004-esteganografia')
esteg = modulo.Esteganografia()

datos = {"ubicacion": "Estante secreto", "valor": "15000 EUR"}
esteg.codificar_imagen("imagen.png", datos, "imagen_segura.png")

# Recuperar datos
recuperados = esteg.decodificar_imagen("imagen_segura.png")
```

### Ver estructura de archivos
```python
from importlib import import_module
modulo = import_module('005-explorador_directorios')
explorador = modulo.ExploradorBiblioteca()
explorador.generar_informe_completo()
```

## Troubleshooting

### Error: "No module named 'PIL'"
```bash
pip install Pillow
```

### Error: "biblioteca_datos no existe"
Ejecuta primero los módulos 1 o 2 para crear la estructura.

### Error: ImportError al ejecutar módulos
Asegúrate de estar en el directorio `101-Ejercicios/`:
```bash
cd "ruta/101-Ejercicios"
python 006-programa_principal.py
```

### Los módulos no se importan correctamente
En el programa principal, los módulos se importan dinámicamente.
Si hay problemas, ejecuta cada módulo individualmente.

## Características Destacadas

### 🔥 Sistema de Hashes
- **Problema**: Buscar 1 libro entre 1000 tarda 100ms
- **Solución**: Con hash tarda 0.1ms (1000x más rápido)

### 🔥 Esteganografía
- **Problema**: ¿Cómo enviar datos secretos sin que se note?
- **Solución**: Ocultos en imagen (cambio < 0.4%)

### 🔥 Pickle vs JSON
- **JSON**: Solo datos básicos (dict, list, str, int)
- **Pickle**: Objetos completos con métodos y datetime

## Demostración Completa

Para ver TODO en acción:

```bash
python 006-programa_principal.py
```

Selecciona opción **6** → Demostración Completa

Esto ejecutará automáticamente:
1. ✅ Archivos de texto (4 libros)
2. ✅ Sistema de hashes (5 libros indexados)
3. ✅ Serialización (objetos completos)
4. ✅ Esteganografía (datos ocultos)
5. ✅ Explorador (análisis completo)

**Tiempo estimado**: 2-3 minutos

## Documentación Completa

- `README.md` - Documentación general
- `MEMORIA.md` - Memoria técnica completa
- Este archivo - Guía rápida

## Soporte

Si encuentras algún problema:
1. Verifica que Python 3.7+ esté instalado
2. Asegúrate de que Pillow está instalado
3. Revisa que estés en el directorio correcto
4. Consulta la documentación completa en README.md

## Ejemplo Completo

```bash
# 1. Instalar
pip install -r requirements.txt

# 2. Ejecutar programa principal
python 006-programa_principal.py

# 3. Seleccionar opción 6 (Demostración Completa)

# 4. Explorar resultados
cd biblioteca_datos
dir /s     # Windows
ls -R      # Linux/Mac
```

---

**¡Listo para usar!** 🎉

El proyecto demuestra dominio completo de:
✅ Archivos de texto
✅ Hashes para búsqueda
✅ Serialización binaria
✅ Esteganografía
✅ Exploración de archivos

Para más información: `README.md` o `MEMORIA.md`
