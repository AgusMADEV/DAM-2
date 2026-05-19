# 📚 Actividad Final: Procesamiento Multinúcleo

## 🎯 Objetivo de la Actividad

Demostrar el dominio de los conceptos de **programación multinúcleo** mediante la creación de una aplicación que:

1. ✅ Distribuya el trabajo entre múltiples núcleos del procesador
2. ✅ Demuestre mejora de rendimiento medible
3. ✅ Aplique los conceptos vistos en clase sobre procesos paralelos
4. ✅ Muestre sincronización y gestión de resultados

## 📖 Conceptos Aplicados

### Del Módulo de Programación Multiproceso

#### ✅ 1. Procesos Paralelos
- División de tareas en subtareas independientes
- Ejecución simultánea en diferentes núcleos
- Aprovechamiento de hardware multinúcleo

#### ✅ 2. Módulo `multiprocessing`
- `multiprocessing.Pool()` - Pool de procesos workers
- `pool.map()` - Distribución automática de trabajo
- `multiprocessing.cpu_count()` - Detección de núcleos disponibles
- `multiprocessing.current_process()` - Identificación de procesos

#### ✅ 3. Sincronización de Resultados
- Recolección de resultados de múltiples procesos
- Orden de procesamiento vs orden de finalización
- Gestión de excepciones en procesos paralelos

#### ✅ 4. Medición de Rendimiento
- Comparación secuencial vs paralelo
- Cálculo de speedup (aceleración)
- Análisis de eficiencia del paralelismo

## 📂 Estructura del Proyecto

```
101-Ejercicios/
│
├── README.md                 # Documentación general
├── ejercicio.md             # Este archivo (instrucciones)
│
├── version1_secuencial.py   # Versión sin paralelismo
├── version1_paralelo.py     # Versión con multiprocessing
├── comparador.py            # Script de benchmarking
│
└── ... (versiones futuras)
```

## 🚀 Guía de Uso

### Paso 1: Ejecutar Versión Secuencial

```powershell
cd "d:\xampp\htdocs\DAM-2\Programación de servicios y procesos\301-Actividades final de unidad - Segundo trimestre\001-Multinucleo\101-Ejercicios"
python version1_secuencial.py
```

**Qué observar:**
- ⏱️ Tiempo total de ejecución
- 🐌 Procesamiento uno por uno
- 📊 Uso de un solo núcleo de CPU

### Paso 2: Ejecutar Versión Paralela

```powershell
python version1_paralelo.py
```

**Qué observar:**
- ⚡ Múltiples números procesándose simultáneamente
- 🚀 Tiempo total reducido
- 🖥️ Uso de todos los núcleos disponibles

### Paso 3: Comparar Rendimiento

```powershell
python comparador.py
```

**Qué observar:**
- 📈 Mejora de rendimiento (%)
- 🔢 Speedup (cuántas veces más rápido)
- 💯 Eficiencia del paralelismo
- 💡 Análisis comparativo detallado

## 🔍 Análisis del Código

### Funciones Clave

#### `procesar_numero(n)` 
```python
def procesar_numero(n):
    """
    Función que será ejecutada por cada proceso worker.
    Realiza trabajo intensivo en CPU.
    """
    primo = es_primo(n)
    divisores = encontrar_divisores(n)
    return {'numero': n, 'es_primo': primo, ...}
```

**Características:**
- ✅ Función pura (sin efectos secundarios)
- ✅ Independiente (no depende de otras tareas)
- ✅ CPU-intensive (ideal para paralelismo)

#### `procesar_lista_paralelo(numeros)`
```python
def procesar_lista_paralelo(numeros):
    num_nucleos = multiprocessing.cpu_count()
    with multiprocessing.Pool(processes=num_nucleos) as pool:
        resultados = pool.map(procesar_numero, numeros)
    return resultados
```

**Cómo funciona:**
1. 🔍 Detecta número de núcleos disponibles
2. 🏊 Crea un Pool con N procesos (N = núcleos)
3. 📤 Distribuye los números entre los procesos
4. ⚙️ Cada proceso ejecuta `procesar_numero()` en paralelo
5. 📥 pool.map() recolecta y ordena los resultados

## 📊 Resultados Esperados

### En un procesador de 8 núcleos:

| Método      | Tiempo | Speedup | Eficiencia |
|-------------|--------|---------|------------|
| Secuencial  | 24s    | 1.00x   | 100%       |
| Paralelo    | 4s     | 6.00x   | 75%        |

**Mejora:** ~83% de reducción de tiempo

### Factores que Afectan el Rendimiento

✅ **Favorables:**
- Más números a procesar
- Números más grandes (más trabajo por tarea)
- Más núcleos disponibles
- Tareas independientes

❌ **Desfavorables:**
- Overhead de crear procesos
- Sincronización y comunicación
- Pocas tareas (< número de núcleos)
- Tareas muy pequeñas

## 🎓 Conceptos Teóricos Aplicados

### Ley de Amdahl
```
Speedup máximo = 1 / (S + P/N)
S = parte secuencial
P = parte paralelizable
N = número de procesadores
```

En nuestro caso:
- S ≈ 0.05 (5% secuencial: inicialización, I/O)
- P ≈ 0.95 (95% paralelizable: cálculos)
- N = núcleos disponibles

### Granularidad de Tareas

**Grano grueso (coarse-grained):** ✅ Usado en este proyecto
- Pocas tareas grandes
- Menor overhead
- Mejor para CPU-bound

**Grano fino (fine-grained):**
- Muchas tareas pequeñas
- Mayor overhead
- Mejor para I/O-bound

## 🔄 Evolución del Proyecto

### ✅ Versión 1 (Actual): Básica
- Procesamiento de números
- Cálculo de primos y divisores
- Comparación de rendimiento

### 🔜 Versión 2 (Próxima): Procesamiento de Archivos
- Leer múltiples archivos de texto
- Contar palabras, líneas
- Análisis de contenido en paralelo

### 🔜 Versión 3: Procesamiento de Imágenes
- Aplicar filtros a imágenes
- Redimensionamiento en batch
- Similar al proyecto de clase

### 🔜 Versión 4: Interfaz Gráfica
- Dashboard con métricas en tiempo real
- Visualización de uso de CPU
- Progress bars por proceso

## 🐛 Troubleshooting

### Problema: "freeze_support" error en Windows
**Solución:**
```python
if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
```

### Problema: No se ve mejora de rendimiento
**Causas posibles:**
1. Muy pocos números (< núcleos)
2. Números muy pequeños (poco trabajo)
3. Overhead del paralelismo > beneficio

**Solución:** Aumenta la cantidad y tamaño de números

### Problema: Prints desordenados
**Causa:** Múltiples procesos escribiendo simultáneamente

**Solución:** Usar Queue o procesar prints después de recolectar resultados

## 💡 Ejercicios Adicionales

### Nivel 1: Modificaciones Básicas
1. Cambia la lista de números por otros más grandes
2. Añade más números a la lista
3. Prueba con diferentes cantidades de workers

### Nivel 2: Nuevas Funcionalidades
1. Calcula factorial de números grandes
2. Implementa búsqueda de números perfectos
3. Añade estadísticas de uso de memoria

### Nivel 3: Optimizaciones
1. Implementa un sistema de caché de resultados
2. Añade Queue para comunicación entre procesos
3. Implementa manejo de errores robusto

## 📚 Referencias

### Documentación Oficial
- [multiprocessing — Python Docs](https://docs.python.org/3/library/multiprocessing.html)
- [concurrent.futures — Python Docs](https://docs.python.org/3/library/concurrent.futures.html)

### Apuntes del Curso
- `001-Programación multiproceso/005-Programación paralela y distribuida/`
- `001-Programación multiproceso/009-Programación de aplicaciones multiproceso/`
- `002-Programación multihilo/007-Programación de aplicaciones multihilo/`

### Ejemplos de Clase
- `006-comprimir multiproceso.py` - Compresión paralela de archivos
- `003-quiero usar multihilo.py` - Ejemplo de Pool
- Proyecto Final EVAL - Sistema de procesamiento de imágenes

## ✅ Criterios de Evaluación

- ✅ Uso correcto de `multiprocessing.Pool`
- ✅ Distribución efectiva del trabajo
- ✅ Mejora medible de rendimiento
- ✅ Código bien documentado
- ✅ Manejo adecuado de resultados
- ✅ Comparación y análisis de resultados
- ✅ Aplicación de conceptos teóricos

---

**¡Éxito en tu proyecto!** 🚀

Si tienes dudas, revisa los ejemplos de clase o consulta la documentación oficial de Python.
