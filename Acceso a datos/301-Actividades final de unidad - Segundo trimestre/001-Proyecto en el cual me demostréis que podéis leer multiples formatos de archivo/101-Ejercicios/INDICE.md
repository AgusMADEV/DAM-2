# 📑 ÍNDICE COMPLETO DEL PROYECTO

## 🏛️ BIBLIOTECA DIGITAL - Índice de Archivos

Este documento proporciona una guía completa de todos los archivos del proyecto y su propósito.

---

## 📂 ESTRUCTURA DEL PROYECTO

```
101-Ejercicios/
│
├── 🐍 CÓDIGO FUENTE (6 archivos)
│   ├── 001-gestion_biblioteca.py          [150 líneas]
│   ├── 002-sistema_hash.py                [250 líneas]
│   ├── 003-serializacion_pickle.py        [350 líneas]
│   ├── 004-esteganografia.py              [400 líneas]
│   ├── 005-explorador_directorios.py      [350 líneas]
│   └── 006-programa_principal.py          [400 líneas]
│
├── 📚 DOCUMENTACIÓN (6 archivos)
│   ├── README.md                          [Principal]
│   ├── MEMORIA.md                         [Técnica completa]
│   ├── GUIA_RAPIDA.md                     [Uso rápido]
│   ├── PRIMEROS_PASOS.md                  [Tutorial inicial]
│   ├── HISTORIAL_VERSIONES.md             [Evolución]
│   ├── RESUMEN_EJECUTIVO.md               [Para evaluación]
│   └── INDICE.md                          [Este archivo]
│
├── ⚙️ CONFIGURACIÓN (3 archivos)
│   ├── requirements.txt                   [Dependencias]
│   ├── instalar.bat                       [Windows]
│   └── instalar.sh                        [Linux/Mac]
│
└── 💾 DATOS GENERADOS (directorio)
    └── biblioteca_datos/
        ├── texto/       [CSV y TXT]
        ├── hash/        [JSON con hashes]
        ├── binario/     [Archivos pickle]
        ├── imagenes/    [Imágenes con datos]
        └── logs/        [Informes del sistema]
```

---

## 🐍 CÓDIGO FUENTE - Descripción Detallada

### 001-gestion_biblioteca.py
**Propósito**: Gestión de archivos de texto (CSV/TXT)  
**Líneas**: ~150  
**Complejidad**: ⭐ Básica

**Contenido:**
- Clase `BibliotecaDigital`
- Escritura CSV con DictWriter
- Lectura CSV con DictReader
- Registro en TXT con timestamp
- Demo integrada

**Cuándo usarlo:**
- Para entender manejo básico de archivos
- Como punto de inicio del proyecto
- Para ver operaciones de texto plano

**Ejecutar:**
```bash
python 001-gestion_biblioteca.py
```

---

### 002-sistema_hash.py
**Propósito**: Sistema de hashes MD5 para indexación  
**Líneas**: ~250  
**Complejidad**: ⭐⭐ Media

**Contenido:**
- Clase `BibliotecaHash`
- Generación de hashes MD5
- CRUD completo (Create, Read, Update, Delete)
- Búsqueda O(1) directa
- Estadísticas del sistema
- Demo con comparación de rendimiento

**Cuándo usarlo:**
- Para entender algoritmos de hash
- Para ver optimización de búsqueda
- Para comparar O(1) vs O(n)

**Ejecutar:**
```bash
python 002-sistema_hash.py
```

**Archivos generados:**
- `biblioteca_datos/hash/*.json` (5 archivos con hash como nombre)

---

### 003-serializacion_pickle.py
**Propósito**: Serialización binaria de objetos Python  
**Líneas**: ~350  
**Complejidad**: ⭐⭐⭐ Media-Alta

**Contenido:**
- Clase `Libro` (objetos con lógica de negocio)
- Clase `BibliotecaBinaria`
- Métodos: `agregar_reseña()`, `agregar_prestamo()`, `esta_disponible()`
- Serialización con pickle
- Comparación Pickle vs JSON
- Demo con objetos complejos

**Cuándo usarlo:**
- Para entender serialización binaria
- Para ver preservación de objetos completos
- Para comparar con JSON

**Ejecutar:**
```bash
python 003-serializacion_pickle.py
```

**Archivos generados:**
- `biblioteca_datos/binario/*.pkl` (objetos serializados)

---

### 004-esteganografia.py
**Propósito**: Codificación/decodificación en imágenes (LSB)  
**Líneas**: ~400  
**Complejidad**: ⭐⭐⭐⭐ Alta

**Contenido:**
- Clase `Esteganografia`
- Algoritmo LSB (Least Significant Bit)
- Conversión texto ↔ binario
- Codificación en píxeles RGB
- Decodificación desde imágenes
- Comparación visual
- Cálculo de capacidad
- Demo completa con imagen

**Cuándo usarlo:**
- Para entender esteganografía
- Para ver manipulación de bits
- Para operaciones con imágenes

**Ejecutar:**
```bash
python 004-esteganografia.py
```

**Archivos generados:**
- `biblioteca_datos/imagenes/portada_biblioteca.png` (base)
- `biblioteca_datos/imagenes/portada_con_datos.png` (con datos ocultos)

**Requiere**: Pillow (PIL)

---

### 005-explorador_directorios.py
**Propósito**: Navegación y análisis del sistema de archivos  
**Líneas**: ~350  
**Complejidad**: ⭐⭐⭐ Media-Alta

**Contenido:**
- Clase `ExploradorBiblioteca`
- Navegación recursiva
- Visualización en árbol ASCII
- Estadísticas completas
- Búsqueda por extensión
- Búsqueda por patrón
- Generación de informes JSON
- Demo con análisis completo

**Cuándo usarlo:**
- Para ver estructura del proyecto
- Para obtener estadísticas
- Para entender recursividad

**Ejecutar:**
```bash
python 005-explorador_directorios.py
```

**Archivos generados:**
- `biblioteca_datos/logs/informe_biblioteca.json` (informe completo)

---

### 006-programa_principal.py
**Propósito**: Menú integrado que unifica todos los módulos  
**Líneas**: ~400  
**Complejidad**: ⭐⭐ Media

**Contenido:**
- Menú interactivo
- Importación dinámica de módulos
- Demostración completa automatizada
- Manejo de excepciones global
- Información del proyecto
- Sistema de navegación

**Cuándo usarlo:**
- **Siempre** - Es el punto de entrada recomendado
- Para ejecutar demos individuales
- Para demostración completa

**Ejecutar:**
```bash
python 006-programa_principal.py
```

**Opciones del menú:**
1. Archivos de texto
2. Sistema de hashes
3. Serialización pickle
4. Esteganografía
5. Explorador
6. **Demo completa** ← Recomendado primero
7. Información
0. Salir

---

## 📚 DOCUMENTACIÓN - Guía de Lectura

### README.md
**Propósito**: Documentación principal del proyecto  
**Longitud**: ~500 líneas  
**Tiempo de lectura**: 15 minutos

**Contenido:**
- Descripción del proyecto
- Requisitos cumplidos
- Estructura de archivos
- Instalación y ejecución
- Casos de uso
- Comparación de formatos
- Conceptos técnicos
- Evolución del proyecto

**Cuándo leerlo:**
- **Primero** después de ejecutar el proyecto
- Para entender el panorama general
- Antes de revisar el código

---

### MEMORIA.md
**Propósito**: Memoria técnica completa  
**Longitud**: ~800 líneas  
**Tiempo de lectura**: 30 minutos

**Contenido:**
- Introducción y contexto
- Objetivos del proyecto
- Análisis de requisitos
- Diseño del sistema
- Implementación detallada
- Pruebas y validación
- Resultados y métricas
- Conclusiones
- Bibliografía

**Cuándo leerlo:**
- Para evaluación técnica
- Para entender decisiones de diseño
- Para ver metodología completa

---

### GUIA_RAPIDA.md
**Propósito**: Referencia rápida de uso  
**Longitud**: ~200 líneas  
**Tiempo de lectura**: 5 minutos

**Contenido:**
- Instalación rápida (3 pasos)
- Ejecución básica
- Descripción de módulos
- Casos de uso breves
- Solución de problemas
- Ejemplos de código

**Cuándo leerlo:**
- Para empezar rápido
- Como referencia durante uso
- Para recordar comandos

---

### PRIMEROS_PASOS.md
**Propósito**: Tutorial paso a paso para principiantes  
**Longitud**: ~300 líneas  
**Tiempo de lectura**: 10 minutos

**Contenido:**
- Verificación de requisitos
- Navegación al proyecto
- Instalación de dependencias
- Primera ejecución
- Verificación de resultados
- Exploración de módulos
- Problemas comunes
- Checklist de verificación

**Cuándo leerlo:**
- **Primera vez** que usas el proyecto
- Si tienes problemas de instalación
- Para guía detallada paso a paso

---

### HISTORIAL_VERSIONES.md
**Propósito**: Evolución del desarrollo incremental  
**Longitud**: ~400 líneas  
**Tiempo de lectura**: 15 minutos

**Contenido:**
- Filosofía de desarrollo
- Evolución versión por versión
- Métricas de cada versión
- Análisis de complejidad
- Conceptos técnicos aplicados
- Metodología de desarrollo
- Estadísticas finales

**Cuándo leerlo:**
- Para entender el proceso de desarrollo
- Para ver cómo creció el proyecto
- Para aprender metodología

---

### RESUMEN_EJECUTIVO.md
**Propósito**: Resumen para evaluación rápida  
**Longitud**: ~300 líneas  
**Tiempo de lectura**: 5 minutos

**Contenido:**
- Cumplimiento de requisitos
- Entregables del proyecto
- Ejecución rápida
- Resultados demostrados
- Innovaciones destacadas
- Métricas del proyecto
- Criterios de evaluación

**Cuándo leerlo:**
- Para evaluación rápida
- Para resumen completo
- Para presentación del proyecto

---

### INDICE.md (este archivo)
**Propósito**: Guía de navegación del proyecto  
**Longitud**: ~250 líneas  
**Tiempo de lectura**: 8 minutos

**Contenido:**
- Estructura completa
- Descripción de cada archivo
- Guías de lectura
- Orden recomendado
- Referencias cruzadas

**Cuándo leerlo:**
- Para orientarse en el proyecto
- Para encontrar información específica
- Como mapa de navegación

---

## ⚙️ ARCHIVOS DE CONFIGURACIÓN

### requirements.txt
**Propósito**: Lista de dependencias Python  
**Contenido:**
```
Pillow>=10.0.0
```

**Uso:**
```bash
pip install -r requirements.txt
```

---

### instalar.bat
**Propósito**: Script de instalación para Windows  
**Uso:**
```cmd
instalar.bat
```

---

### instalar.sh
**Propósito**: Script de instalación para Linux/Mac  
**Uso:**
```bash
chmod +x instalar.sh
./instalar.sh
```

---

## 💾 DATOS GENERADOS

### biblioteca_datos/texto/
**Contenido:**
- `libros.csv` - Catálogo de libros en CSV
- `registro.txt` - Log de actividades con timestamp

**Generado por**: 001-gestion_biblioteca.py

---

### biblioteca_datos/hash/
**Contenido:**
- `5016c5d6...json` - El Quijote
- `382c8905...json` - Cien años de soledad
- `42afa766...json` - 1984
- `55c24df0...json` - Rayuela
- `ca558f3a...json` - La sombra del viento

**Generado por**: 002-sistema_hash.py

---

### biblioteca_datos/binario/
**Contenido:**
- `libro_*.pkl` - Objetos Libro individuales
- `coleccion.pkl` - Colección completa de libros
- `estado.pkl` - Estado completo del sistema

**Generado por**: 003-serializacion_pickle.py

---

### biblioteca_datos/imagenes/
**Contenido:**
- `portada_biblioteca.png` - Imagen base (800x600)
- `portada_con_datos.png` - Imagen con datos ocultos

**Generado por**: 004-esteganografia.py

---

### biblioteca_datos/logs/
**Contenido:**
- `informe_biblioteca.json` - Informe completo del sistema

**Generado por**: 005-explorador_directorios.py

---

## 🎯 ORDEN RECOMENDADO DE LECTURA

### Para Uso Rápido (15 minutos)
1. `PRIMEROS_PASOS.md` (10 min)
2. Ejecutar: `python 006-programa_principal.py` → Opción 6
3. `GUIA_RAPIDA.md` (5 min)

### Para Comprensión Completa (1 hora)
1. `PRIMEROS_PASOS.md` (10 min)
2. Ejecutar: `python 006-programa_principal.py` → Opción 6 (3 min)
3. `README.md` (15 min)
4. Ejecutar módulos individuales (20 min)
5. `HISTORIAL_VERSIONES.md` (15 min)

### Para Evaluación Técnica (30 minutos)
1. `RESUMEN_EJECUTIVO.md` (5 min)
2. Ejecutar demo completa (3 min)
3. `MEMORIA.md` - secciones clave (15 min)
4. Revisar código fuente de 2-3 módulos (7 min)

### Para Aprender Desarrollo (2 horas)
1. `README.md` (15 min)
2. `HISTORIAL_VERSIONES.md` (15 min)
3. Leer código en orden: 001 → 002 → 003 → 004 → 005 (1 hora)
4. `MEMORIA.md` - implementación (20 min)
5. Experimentar modificando código (10 min)

---

## 🔍 BÚSQUEDA RÁPIDA

### ¿Cómo instalar?
→ `PRIMEROS_PASOS.md` - Paso 3

### ¿Cómo ejecutar?
→ `GUIA_RAPIDA.md` - Ejecución

### ¿Qué hace cada módulo?
→ Este archivo - Sección "Código Fuente"

### ¿Cómo funciona el hash?
→ `MEMORIA.md` - Sección 5.2.2
→ `002-sistema_hash.py` (código fuente)

### ¿Cómo funciona la esteganografía?
→ `MEMORIA.md` - Sección 5.2.4
→ `004-esteganografia.py` (código fuente)

### ¿Qué archivos se generan?
→ Este archivo - Sección "Datos Generados"
→ Ejecutar: `python 005-explorador_directorios.py`

### ¿Cuánto código hay?
→ `HISTORIAL_VERSIONES.md` - Estadísticas finales
→ `RESUMEN_EJECUTIVO.md` - Métricas

### ¿Cómo se desarrolló?
→ `HISTORIAL_VERSIONES.md` - Evolución completa

### ¿Cumple los requisitos?
→ `RESUMEN_EJECUTIVO.md` - Cumplimiento de requisitos

### ¿Tiene problemas?
→ `PRIMEROS_PASOS.md` - Problemas comunes
→ `GUIA_RAPIDA.md` - Troubleshooting

---

## 📊 ESTADÍSTICAS DEL PROYECTO

### Código
- **Archivos Python**: 6
- **Líneas totales**: ~1,900
- **Clases**: 6
- **Métodos**: 45+

### Documentación
- **Archivos Markdown**: 7
- **Líneas totales**: ~2,500
- **Páginas impresas**: ~50

### Formatos Implementados
1. CSV (texto tabular)
2. TXT (texto plano)
3. JSON (datos estructurados)
4. PKL (objetos Python)
5. PNG (imágenes)

---

## ✅ VALIDACIÓN

### Todo está correcto si:
- [ ] Hay 6 archivos `.py`
- [ ] Hay 7 archivos `.md`
- [ ] Hay 3 archivos de configuración
- [ ] Se ejecuta sin errores
- [ ] Se generan 5 carpetas en `biblioteca_datos/`
- [ ] Hay archivos en cada carpeta de datos

---

**Proyecto completo y documentado al 100%** ✅

*Última actualización: 5 de marzo de 2026*
