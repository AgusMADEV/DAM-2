# �️ GESTIÓN DE RESTAURANTES - Sistema Integral de Gestión de Datos

## 📋 Descripción del Proyecto

Este proyecto es un **sistema completo de gestión de restaurantes** que demuestra el dominio de múltiples formatos de persistencia de datos en Python. Ha sido desarrollado como proyecto final para la asignatura de **Acceso a Datos** de DAM (Desarrollo de Aplicaciones Multiplataforma).

El proyecto integra 5 métodos diferentes de almacenamiento y recuperación de información, mostrando las ventajas y casos de uso de cada uno.

## 🎯 Requisitos Cumplidos

### ✅ 1. Escritura y Lectura de Archivos en Modo Texto
- **Archivo CSV**: Almacenamiento estructurado de datos de platos y menús
- **Archivo TXT**: Registro de pedidos y logs del sistema
- **Codificación UTF-8**: Soporte completo para caracteres especiales
- **Manejo de excepciones**: Gestión robusta de errores

### ✅ 2. Codificación y Descodificación de Información en Imágenes (Esteganografía)
- **Técnica LSB** (Least Significant Bit): Modificación imperceptible de píxeles
- **Ocultación de datos**: Información invisible a simple vista
- **Capacidad**: Hasta ~180 KB de texto en imagen de 800x600
- **Aplicaciones**: Seguridad, marcas de agua, protección de datos

### ✅ 3. Utilización de Hashes para Codificar Archivos
- **Algoritmo MD5**: Generación de identificadores únicos
- **Acceso directo O(1)**: Búsqueda instantánea vs secuencial O(n)
- **Índice eficiente**: Ideal para grandes volúmenes de datos
- **Comparación demostrada**: 1000x más rápido con 1000 elementos

### ✅ 4. Proyecto de Revisión y Árbol de Sistema de Archivos
- **Navegación recursiva**: Exploración completa del directorio
- **Estadísticas**: Análisis de archivos por tipo, tamaño y fecha
- **Búsqueda avanzada**: Por extensión, nombre y patrón
- **Informes JSON**: Documentación automática del sistema

### ✅ 5. Librería Pickle para Binario
- **Serialización completa**: Objetos Python con métodos y atributos
- **Preservación de tipos**: datetime, listas, diccionarios anidados
- **Colecciones**: Guardado de múltiples objetos relacionados
- **Ventajas sobre JSON**: Mantiene la estructura completa del objeto

## 📁 Estructura del Proyecto

```
101-Ejercicios/
│
├── 001-gestion_restaurante.py     # Archivos de texto (CSV/TXT)
├── 002-sistema_hash.py            # Sistema de hashes MD5
├── 003-serializacion_pickle.py    # Serialización binaria
├── 004-esteganografia.py          # Codificación en imágenes
├── 005-explorador_directorios.py  # Árbol de archivos
├── 006-programa_principal.py      # Menú integrado
├── README.md                      # Este archivo
│
└── restaurante_datos/             # Datos generados (se crea automáticamente)
    ├── texto/                     # CSV y TXT
    ├── hash/                      # Archivos JSON indexados
    ├── binario/                   # Archivos pickle
    ├── imagenes/                  # Imágenes con datos ocultos
    └── logs/                      # Informes del sistema
```

## 🚀 Instalación y Ejecución

### Requisitos Previos

- **Python 3.7+**
- **Pillow** (para procesamiento de imágenes)

### Instalación de Dependencias

```bash
pip install Pillow
```

### Ejecución del Proyecto

#### Opción 1: Programa Principal con Menú (Recomendado)

```bash
python 006-programa_principal.py
```

Este programa ofrece un menú interactivo para ejecutar cada módulo por separado o una demostración completa.

#### Opción 2: Ejecutar Módulos Individuales

```bash
# Archivos de texto
python 001-gestion_restaurante.py

# Sistema de hashes
python 002-sistema_hash.py

# Serialización con pickle
python 003-serializacion_pickle.py

# Esteganografía
python 004-esteganografia.py

# Explorador de directorios
python 005-explorador_directorios.py
```

## 💡 Casos de Uso Demostrados

### 1. Gestión de Archivos de Texto
```python
from restaurante import GestionRestaurante

restaurante = GestionRestaurante()
platos = [{"id": "...", "nombre": "...", "precio": "...", "categoria": "..."}]
restaurante.guardar_en_csv(platos, "menu.csv")
```

**Ventajas:**
- ✅ Formato universal y legible
- ✅ Compatible con Excel y otras herramientas
- ✅ Fácil de editar manualmente

### 2. Sistema de Hashes
```python
from sistema_hash import RestauranteHash

restaurante = RestauranteHash()
restaurante.guardar_plato_hash(plato)
plato = restaurante.buscar_plato_por_id("PLT-001")
```

**Ventajas:**
- ✅ Búsqueda instantánea O(1)
- ✅ Ideal para grandes volúmenes
- ✅ No requiere índices adicionales

### 3. Serialización Pickle
```python
from serializacion_pickle import RestauranteBinario, Plato

plato = Plato(id="...", nombre="...", precio=..., ingredientes=[...])
plato.agregar_valoracion("Cliente", 5, "Delicioso")

restaurante = RestauranteBinario()
restaurante.guardar_plato_binario(plato)
```

**Ventajas:**
- ✅ Guarda objetos completos con métodos
- ✅ Preserva tipos de datos complejos
- ✅ Más eficiente que JSON

### 4. Esteganografía
```python
from esteganografia import Esteganografia

esteg = Esteganografia()
receta_secreta = {"ingrediente_especial": "Trufa negra", "tecnica": "Sous-vide 62°C"}
esteg.codificar_imagen("plato.png", receta_secreta, "plato_con_receta.png")

# La imagen es idéntica visualmente pero contiene la receta oculta
receta = esteg.decodificar_imagen("plato_con_receta.png")
```

**Ventajas:**
- ✅ Seguridad: datos invisibles
- ✅ No afecta la imagen visualmente
- ✅ Difícil de detectar sin herramientas especiales

### 5. Explorador de Directorios
```python
from explorador_directorios import ExploradorRestaurante

explorador = ExploradorRestaurante()
explorador.generar_informe_completo()
archivos_json = explorador.buscar_archivos_por_extension('.json')
```

**Ventajas:**
- ✅ Auditoría completa del sistema
- ✅ Búsqueda rápida de archivos
- ✅ Análisis de uso de espacio

## 📊 Comparación de Formatos

| Formato | Velocidad | Tamaño | Legibilidad | Complejidad | Seguridad |
|---------|-----------|---------|-------------|-------------|-----------|
| **CSV/TXT** | ⭐⭐⭐ | Grande | Alta | Baja | Baja |
| **Hash+JSON** | ⭐⭐⭐⭐⭐ | Media | Alta | Media | Media |
| **Pickle** | ⭐⭐⭐⭐ | Pequeño | Nula | Alta | Media |
| **Esteganografía** | ⭐⭐ | Grande | Invisible | Alta | Alta |

## 🎓 Conceptos Técnicos Demostrados

### Programación Orientada a Objetos
- Clases y métodos
- Encapsulación
- Herencia y composición

### Manejo de Archivos
- Modos de apertura (r, w, a, rb, wb)
- Context managers (with)
- Codificación de caracteres

### Algoritmos
- Hash MD5
- Recursividad
- Búsqueda y ordenamiento

### Estructuras de Datos
- Listas y diccionarios
- Objetos complejos
- Serialización

### Manipulación de Bits
- Operadores bitwise (&, |)
- Representación binaria
- LSB (Least Significant Bit)

## 🔧 Detalles Técnicos

### Sistema de Hashes

El sistema utiliza MD5 para convertir IDs de platos en identificadores únicos:

```
ID Plato: "PLT-001-PAELLA"
  ↓ MD5
Hash: "a5f2b8c9d1e3f4a5b6c7d8e9f0a1b2c3"
  ↓
Archivo: hash/a5f2b8c9d1e3f4a5b6c7d8e9f0a1b2c3.json
```

**Complejidad:**
- Búsqueda secuencial: O(n) - revisa todos los archivos
- Búsqueda con hash: O(1) - acceso directo

### Esteganografía LSB

Cada píxel RGB tiene 3 valores (0-255). Se modifica el bit menos significativo:

```
Píxel original: RGB(135, 206, 235)
Binario rojo:   10000111
Bit a ocultar:  1
Binario nuevo:  10000111 (sin cambio)
```

**Capacidad de una imagen 800x600:**
- Píxeles: 480,000
- Bits disponibles: 1,440,000 (3 por píxel)
- Caracteres: 180,000 (8 bits cada uno)

## 📈 Evolución del Proyecto

### Versión 1.0 - Base
- Estructura de directorios
- Archivos CSV y TXT
- Operaciones básicas

### Versión 2.0 - Optimización
- Sistema de hashes MD5
- Búsqueda O(1)
- Estadísticas

### Versión 3.0 - Objetos Complejos
- Clase Libro personalizada
- Serialización con pickle
- Relaciones entre objetos

### Versión 4.0 - Seguridad
- Esteganografía LSB
- Ocultación de datos
- Comparación visual

### Versión 5.0 - Análisis
- Explorador recursivo
- Informes automáticos
- Búsqueda avanzada

### Versión Final - Integración
- Menú unificado
- Demostración completa
- Documentación exhaustiva

## 🎯 Casos de Uso Reales

1. **Restaurantes**: Gestión de menús, pedidos y recetas con diferentes formatos
2. **Recetas secretas**: Preservación de recetas con información oculta en imágenes
3. **Sistemas de backup**: Serialización eficiente de estados del inventario
4. **Seguridad**: Protección de recetas patentadas e información sensible
5. **Auditoría**: Análisis de ventas y exploración de estructuras de archivos

## ⚠️ Consideraciones de Seguridad

### Pickle
- ⚠️ Solo cargar archivos de fuentes confiables
- ⚠️ Puede ejecutar código arbitrario al deserializar
- ✅ Ideal para entornos controlados

### Esteganografía
- ✅ Datos ocultos imperceptibles
- ⚠️ Puede detectarse con análisis forense
- ✅ Añadir encriptación para mayor seguridad

## 📝 Notas de Desarrollo

### Buenas Prácticas Aplicadas
- ✅ Documentación clara con docstrings
- ✅ Manejo exhaustivo de excepciones
- ✅ Nombres descriptivos de variables
- ✅ Código modular y reutilizable
- ✅ Principio DRY (Don't Repeat Yourself)

### Posibles Mejoras Futuras
- [ ] Añadir encriptación AES para pickle
- [ ] Implementar base de datos SQLite
- [ ] GUI con tkinter o PyQt
- [ ] API REST con Flask
- [ ] Tests unitarios con pytest
- [ ] Logging avanzado
- [ ] Compresión de archivos

## 👨‍💻 Autor

Proyecto desarrollado para la asignatura de **Acceso a Datos**  
**DAM (Desarrollo de Aplicaciones Multiplataforma)** - 2º Curso  
Año: 2026

## 📄 Licencia

Este proyecto es de uso educativo y está desarrollado como parte del currículo académico.

## 🙏 Agradecimientos

- Agradecimientos al profesor por los ejercicios de referencia
- Documentación oficial de Python
- Comunidad de Stack Overflow
- Biblioteca Pillow (PIL)

---

## 🚀 ¡Empieza Ahora!

```bash
python 006-programa_principal.py
```

**Selecciona la opción 6** para ver la demostración completa de todos los módulos.

---

*Proyecto desarrollado con ❤️ para demostrar el dominio de múltiples formatos de persistencia de datos en Python.*
