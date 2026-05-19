En este proyecto he desarrollado un **sistema integral de gestión de restaurantes** que demuestra mi dominio sobre múltiples formatos de persistencia de datos en Python. El concepto fundamental que trabajo aquí es la **persistencia de datos heterogénea**, es decir, la capacidad de almacenar y recuperar información utilizando diferentes técnicas según las necesidades específicas de cada operación.

Este sistema sirve para gestionar información completa de restaurantes españoles (datos generales, reservas, reseñas) y se utiliza en contextos donde necesitamos:

- **Almacenamiento estructurado** (archivos de texto)
- **Búsqueda ultrarrápida** (sistema de hashes)
- **Preservación de objetos complejos** (serialización binaria)
- **Ocultación segura de información** (esteganografía)
- **Análisis del sistema de archivos** (exploración recursiva)

El proyecto integra 5 técnicas diferentes de acceso a datos, demostrando que comprendo cuándo y cómo usar cada una apropiadamente.

---

### Archivos de Texto (CSV y TXT)

**Definición**: Los archivos de texto son ficheros que almacenan información en formato legible por humanos, usando codificación UTF-8. CSV (Comma-Separated Values) es un formato estructurado donde cada línea representa un registro y los campos se separan por comas.

**Terminología técnica**:
- **Encoding UTF-8**: Codificación que permite caracteres especiales (tildes, ñ)
- **DictWriter/DictReader**: Clases de Python para trabajar con CSV usando diccionarios
- **Append mode ('a')**: Modo de escritura que añade contenido sin sobrescribir

**Funcionamiento paso a paso**:

En mi implementación, el proceso de guardar restaurantes en CSV sigue estos pasos:

```python
def guardar_en_csv(self, datos, nombre_archivo="restaurantes.csv"):
    """
    Guarda datos de restaurantes en formato CSV
    
    Args:
        datos: Lista de diccionarios con información de restaurantes
        nombre_archivo: Nombre del archivo CSV
    """
    ruta_completa = f"{self.ruta_base}/texto/{nombre_archivo}"
    
    try:
        with open(ruta_completa, 'w', newline='', encoding='utf-8') as archivo:
            if datos:
                campos = datos[0].keys()
                escritor = csv.DictWriter(archivo, fieldnames=campos)
                escritor.writeheader()
                escritor.writerows(datos)
                print(f"✓ Datos guardados en CSV: {ruta_completa}")
                return True
    except Exception as e:
        print(f"✗ Error al guardar CSV: {e}")
        return False
```

**Paso 1**: Construyo la ruta completa del archivo  
**Paso 2**: Abro el archivo en modo escritura ('w') con encoding UTF-8  
**Paso 3**: Extraigo los nombres de las columnas desde las claves del primer diccionario  
**Paso 4**: Creo un DictWriter con esos campos  
**Paso 5**: Escribo la cabecera con `writeheader()`  
**Paso 6**: Escribo todas las filas con `writerows()`

Para la lectura, el proceso es el inverso:

```python
def leer_desde_csv(self, nombre_archivo="restaurantes.csv"):
    """
    Lee datos desde un archivo CSV
    
    Args:
        nombre_archivo: Nombre del archivo CSV
        
    Returns:
        Lista de diccionarios con los datos leídos
    """
    ruta_completa = f"{self.ruta_base}/texto/{nombre_archivo}"
    
    try:
        with open(ruta_completa, 'r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            datos = list(lector)
            print(f"✓ Leídos {len(datos)} registros desde CSV")
            return datos
    except FileNotFoundError:
        print(f"✗ Archivo no encontrado: {ruta_completa}")
        return []
    except Exception as e:
        print(f"✗ Error al leer CSV: {e}")
        return []
```

### Sistema de Hashes (MD5)

**Definición**: Un hash es una función criptográfica que convierte cualquier entrada en una cadena de longitud fija (en MD5: 32 caracteres hexadecimales). Es determinista (misma entrada = mismo hash) y unidireccional (imposible revertir).

**Terminología técnica**:
- **MD5 (Message-Digest Algorithm 5)**: Algoritmo de hash de 128 bits
- **Complejidad O(1)**: Acceso en tiempo constante, independiente del tamaño de datos
- **Indexación por hash**: Usar el hash como nombre de archivo para acceso directo

**Funcionamiento paso a paso**:

El sistema de hashes que he implementado transforma el CIF del restaurante en un identificador único:

```python
def generar_hash(self, clave):
    """
    Genera un hash MD5 a partir de una clave
    
    Args:
        clave: String que se usará para generar el hash
        
    Returns:
        String con el hash MD5 en hexadecimal
    """
    return hashlib.md5(clave.encode()).hexdigest()
```

**Ejemplo real**: Si tengo un restaurante con CIF "A28010000", genero su hash:
- **Entrada**: "A28010000"
- **Hash MD5**: "27d125e8ce2adc341c37078042e995bf"
- **Archivo**: `27d125e8ce2adc341c37078042e995bf.json`

La ventaja crítica es la búsqueda O(1):

```python
def buscar_restaurante_por_cif(self, cif):
    """
    Busca un restaurante por su CIF de forma directa usando hash
    
    Args:
        cif: CIF del restaurante a buscar
        
    Returns:
        Diccionario con los datos del restaurante o None si no se encuentra
    """
    try:
        # Generar hash del CIF
        hash_cif = self.generar_hash(cif)
        ruta_archivo = f"{self.ruta_hash}/{hash_cif}.json"
        
        # Acceso directo al archivo (O(1) - constante)
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            restaurante = json.load(archivo)
            print(f"✓ Restaurante encontrado usando hash: {hash_cif}")
            return restaurante
            
    except FileNotFoundError:
        print(f"✗ Restaurante no encontrado con CIF: {cif}")
        return None
    except Exception as e:
        print(f"✗ Error al buscar restaurante: {e}")
        return None
```

**Comparación de rendimiento**:
- **Búsqueda secuencial** (sin hash): Si tengo 1000 restaurantes, debo abrir hasta 1000 archivos → O(n)
- **Búsqueda con hash**: Genero el hash y abro 1 solo archivo → O(1)
- **Mejora**: 1000x más rápido en el peor caso

### Serialización Binaria (Pickle)

**Definición**: Pickle es el módulo de Python para **serialización** (convertir objetos Python a bytes) y **deserialización** (bytes → objetos). Preserva completamente la estructura, métodos y tipo de los objetos.

**Terminología técnica**:
- **Serialización**: Proceso de convertir objetos en flujo de bytes
- **Deserialización**: Proceso inverso, reconstruir objetos desde bytes
- **Formato binario**: No legible por humanos, pero más eficiente que JSON
- **Persistencia de objetos**: Guardar instancias completas de clases

**Funcionamiento paso a paso**:

Primero defino una clase `Restaurante` con atributos y métodos:

```python
class Restaurante:
    """Clase que representa un restaurante con todas sus propiedades"""
    
    def __init__(self, cif, nombre, chef, ciudad, tipo_cocina, estrellas_michelin, precio_medio):
        self.cif = cif
        self.nombre = nombre
        self.chef = chef
        self.ciudad = ciudad
        self.tipo_cocina = tipo_cocina
        self.estrellas_michelin = estrellas_michelin
        self.precio_medio = precio_medio
        self.fecha_registro = datetime.now()
        self.reservas = []
        self.reseñas = []
    
    def agregar_reserva(self, cliente, fecha_reserva, num_comensales=2):
        """Registra una reserva en el restaurante"""
        reserva = {
            "cliente": cliente,
            "fecha_reserva": fecha_reserva,
            "num_comensales": num_comensales,
            "fecha_registro": datetime.now()
        }
        self.reservas.append(reserva)
    
    def agregar_reseña(self, usuario, calificacion, comentario):
        """Agrega una reseña al restaurante"""
        reseña = {
            "usuario": usuario,
            "calificacion": calificacion,
            "comentario": comentario,
            "fecha": datetime.now()
        }
        self.reseñas.append(reseña)
```

Luego serializo el objeto completo:

```python
def guardar_restaurante_binario(self, restaurante, nombre_archivo=None):
    """
    Serializa y guarda un objeto Restaurante en formato binario
    
    Args:
        restaurante: Objeto de la clase Restaurante
        nombre_archivo: Nombre del archivo (opcional, usa CIF si no se especifica)
        
    Returns:
        Boolean indicando éxito
    """
    if not nombre_archivo:
        # Usar CIF como nombre de archivo, reemplazando caracteres no válidos
        nombre_archivo = restaurante.cif.replace("-", "_") + ".pkl"
    
    ruta_completa = f"{self.ruta_binario}/{nombre_archivo}"
    
    try:
        with open(ruta_completa, 'wb') as archivo:
            pickle.dump(restaurante, archivo)
        print(f"✓ Restaurante serializado y guardado: {nombre_archivo}")
        return True
    except Exception as e:
        print(f"✗ Error al guardar restaurante: {e}")
        return False
```

**Paso 1**: Abro archivo en modo binario de escritura ('wb')  
**Paso 2**: Uso `pickle.dump()` para serializar el objeto completo  
**Paso 3**: El archivo .pkl contiene TODA la información del objeto, incluyendo datetime, listas, métodos

Para recuperarlo:

```python
def cargar_restaurante_binario(self, nombre_archivo):
    """
    Deserializa y carga un objeto Restaurante desde archivo binario
    
    Args:
        nombre_archivo: Nombre del archivo .pkl
        
    Returns:
        Objeto Restaurante deserializado o None si hay error
    """
    ruta_completa = f"{self.ruta_binario}/{nombre_archivo}"
    
    try:
        with open(ruta_completa, 'rb') as archivo:
            restaurante = pickle.load(archivo)
        print(f"✓ Restaurante deserializado: {restaurante.nombre}")
        return restaurante
    except FileNotFoundError:
        print(f"✗ Archivo no encontrado: {nombre_archivo}")
        return None
    except Exception as e:
        print(f"✗ Error al cargar restaurante: {e}")
        return None
```

**Ventaja sobre JSON**: Con JSON perdería los objetos `datetime`, los métodos de la clase y la estructura exacta. Con pickle recupero el objeto IDÉNTICO.

### Esteganografía (LSB en Imágenes)

**Definición**: La esteganografía es la técnica de ocultar información dentro de otro medio (en este caso, imágenes) de forma imperceptible. Uso el método **LSB (Least Significant Bit)** que modifica el bit menos significativo de cada componente RGB de los píxeles.

**Terminología técnica**:
- **LSB**: Bit menos significativo, el que menos afecta al valor final
- **RGB**: Red-Green-Blue, tres componentes de 8 bits cada uno (0-255)
- **Bit masking**: Operación `& 0xFE` que pone el LSB en 0, luego `| bit` lo establece
- **Delimitador**: Marca especial ("<<<FIN>>>") para identificar el final del mensaje

**Funcionamiento paso a paso**:

```python
def codificar_imagen(self, ruta_imagen_original, datos, ruta_imagen_salida=None):
    """
    Codifica información en una imagen usando LSB (Least Significant Bit)
    
    Args:
        ruta_imagen_original: Ruta de la imagen base
        datos: Datos a ocultar (puede ser dict, str, etc.)
        ruta_imagen_salida: Ruta donde guardar la imagen codificada
        
    Returns:
        Boolean indicando éxito
    """
    try:
        # Convertir datos a JSON si es un diccionario
        if isinstance(datos, dict):
            mensaje = json.dumps(datos, ensure_ascii=False)
        else:
            mensaje = str(datos)
        
        # Agregar delimitador para saber dónde termina el mensaje
        mensaje += "<<<FIN>>>"
        
        # Convertir mensaje a binario
        mensaje_binario = self.texto_a_binario(mensaje)
        
        # Cargar imagen
        imagen = Image.open(ruta_imagen_original)
        
        # Verificar si la imagen puede almacenar el mensaje
        pixeles_necesarios = len(mensaje_binario)
        pixeles_disponibles = imagen.size[0] * imagen.size[1] * 3  # RGB
        
        if pixeles_necesarios > pixeles_disponibles:
            print(f"✗ Error: La imagen es muy pequeña para el mensaje")
            print(f"  Necesarios: {pixeles_necesarios} bits")
            print(f"  Disponibles: {pixeles_disponibles} bits")
            return False
        
        # Convertir imagen a RGB si no lo es
        if imagen.mode != 'RGB':
            imagen = imagen.convert('RGB')
        
        # Obtener píxeles
        pixeles = list(imagen.getdata())
        
        # Codificar mensaje en los píxeles
        indice_mensaje = 0
        pixeles_modificados = []
        
        for pixel in pixeles:
            if indice_mensaje < len(mensaje_binario):
                # Modificar cada componente RGB
                r, g, b = pixel
                
                # Modificar bit menos significativo del rojo
                if indice_mensaje < len(mensaje_binario):
                    r = (r & 0xFE) | int(mensaje_binario[indice_mensaje])
                    indice_mensaje += 1
                
                # Modificar bit menos significativo del verde
                if indice_mensaje < len(mensaje_binario):
                    g = (g & 0xFE) | int(mensaje_binario[indice_mensaje])
                    indice_mensaje += 1
                
                # Modificar bit menos significativo del azul
                if indice_mensaje < len(mensaje_binario):
                    b = (b & 0xFE) | int(mensaje_binario[indice_mensaje])
                    indice_mensaje += 1
                
                pixeles_modificados.append((r, g, b))
            else:
                pixeles_modificados.append(pixel)
        
        # Crear nueva imagen con píxeles modificados
        imagen_codificada = Image.new(imagen.mode, imagen.size)
        imagen_codificada.putdata(pixeles_modificados)
        
        # Guardar imagen
        if not ruta_imagen_salida:
            nombre_base = os.path.basename(ruta_imagen_original)
            nombre_sin_ext = os.path.splitext(nombre_base)[0]
            ruta_imagen_salida = f"{self.ruta_imagenes}/{nombre_sin_ext}_codificada.png"
        
        imagen_codificada.save(ruta_imagen_salida, 'PNG')
        
        print(f"✓ Datos codificados exitosamente en la imagen")
        print(f"  Mensaje: {len(mensaje)} caracteres")
        print(f"  Imagen guardada en: {ruta_imagen_salida}")
        
        return True
```

**Ejemplo detallado**:

Supongamos que tengo un píxel con color RGB(200, 150, 100) y quiero codificar los bits "101":

1. **R = 200** → binario: 11001000
   - Bit del mensaje: 1
   - `(200 & 0xFE)` = 11001000 (el LSB ya es 0)
   - `| 1` = 11001001 = 201
   - **Nuevo R = 201** (cambió +1, imperceptible)

2. **G = 150** → binario: 10010110
   - Bit del mensaje: 0
   - `(150 & 0xFE)` = 10010110
   - `| 0` = 10010110 = 150
   - **Nuevo G = 150** (sin cambio)

3. **B = 100** → binario: 01100100
   - Bit del mensaje: 1
   - `(100 & 0xFE)` = 01100100
   - `| 1` = 01100101 = 101
   - **Nuevo B = 101** (cambió +1)

**Resultado**: RGB(200, 150, 100) → RGB(201, 150, 101)  
**Diferencia visual**: IMPERCEPTIBLE al ojo humano (±1 en escala de 255)

### Explorador de Directorios (Navegación Recursiva)

**Definición**: Un explorador de directorios recorre recursivamente la estructura de carpetas y archivos, generando un árbol completo del sistema de archivos. La recursión permite procesar subcarpetas de forma elegante.

**Terminología técnica**:
- **Recursión**: Función que se llama a sí misma para procesar subestructuras
- **os.walk/os.listdir**: Funciones para navegar directorios
- **os.path.getsize**: Obtener tamaño de archivo en bytes
- **Árbol de directorios**: Estructura jerárquica que representa carpetas y archivos

**Funcionamiento paso a paso**:

```python
def recorrer_directorio_recursivo(self, ruta=None, nivel=0, mostrar=True):
    """
    Recorre recursivamente un directorio y muestra su estructura
    
    Args:
        ruta: Ruta del directorio a recorrer
        nivel: Nivel de profundidad (para indentación)
        mostrar: Si se debe imprimir la estructura
        
    Returns:
        Diccionario con la estructura del directorio
    """
    if ruta is None:
        ruta = self.ruta_base
    
    estructura = {
        "nombre": os.path.basename(ruta) or ruta,
        "tipo": "directorio",
        "ruta": ruta,
        "hijos": []
    }
    
    try:
        elementos = sorted(os.listdir(ruta))
        
        # Separar directorios y archivos
        directorios = []
        archivos = []
        
        for elemento in elementos:
            ruta_completa = os.path.join(ruta, elemento)
            if os.path.isdir(ruta_completa):
                directorios.append(elemento)
            else:
                archivos.append(elemento)
        
        # Procesar directorios primero
        for i, directorio in enumerate(directorios):
            ruta_completa = os.path.join(ruta, directorio)
            es_ultimo_dir = (i == len(directorios) - 1) and len(archivos) == 0
            prefijo = "└── " if es_ultimo_dir else "├── "
            
            if mostrar:
                print("│   " * nivel + prefijo + f"📁 {directorio}/")
            
            self.estadisticas["total_directorios"] += 1
            
            # Recursión
            sub_estructura = self.recorrer_directorio_recursivo(
                ruta_completa, 
                nivel + 1, 
                mostrar
            )
            estructura["hijos"].append(sub_estructura)
        
        # Procesar archivos
        for i, archivo in enumerate(archivos):
            ruta_completa = os.path.join(ruta, archivo)
            es_ultimo = i == len(archivos) - 1
            prefijo = "└── " if es_ultimo else "├── "
            
            tamaño = self.obtener_tamaño_archivo(ruta_completa)
            extension = os.path.splitext(archivo)[1].lower()
            
            # Actualizar estadísticas
            self.estadisticas["total_archivos"] += 1
            self.estadisticas["tamaño_total"] += tamaño
            self.estadisticas["tipos_archivo"][extension] = \
                self.estadisticas["tipos_archivo"].get(extension, 0) + 1
            
            # Icono según extensión
            iconos = {
                '.csv': '📊',
                '.txt': '📝',
                '.json': '📋',
                '.pkl': '🔒',
                '.png': '🖼️',
                '.jpg': '🖼️',
                '.jpeg': '🖼️',
                '.md': '📄',
                '.py': '🐍'
            }
            icono = iconos.get(extension, '📄')
            
            if mostrar:
                tamaño_str = self.formatear_tamaño(tamaño)
                print("│   " * nivel + prefijo + f"{icono} {archivo} ({tamaño_str})")
```

**Paso 1**: Recibo la ruta y nivel de profundidad  
**Paso 2**: Listo todos los elementos con `os.listdir()`  
**Paso 3**: Separo directorios de archivos para ordenar la visualización  
**Paso 4**: Proceso directorios primero, llamando recursivamente a la función  
**Paso 5**: Proceso archivos, recopilando estadísticas (tamaño, extensión)  
**Paso 6**: Imprimo con indentación según el nivel (│, ├──, └──)

**Resultado visual**:
```
restaurantes_datos/
├── 📁 binario/
│   ├── 🔒 A28010000.pkl (2.45 KB)
│   └── 🔒 restaurantes_completos.pkl (8.12 KB)
├── 📁 hash/
│   ├── 📋 27d125e8ce2adc341c37078042e995bf.json (512 B)
│   └── 📋 78076ab321ea5edd6e0384e4c1e0d2d2.json (489 B)
└── 📁 texto/
    ├── 📊 restaurantes.csv (1.23 KB)
    └── 📝 registro.txt (456 B)
```

---

### Caso de Uso Real: Sistema de Gestión de Restaurante DiverXO

Voy a mostrar cómo aplico TODAS las técnicas en un flujo completo de trabajo:

```python
# ===== PASO 1: Crear datos iniciales en CSV (rápido de crear/leer para humanos) =====
from 001-gestion_biblioteca import SistemaRestaurantes

sistema_texto = SistemaRestaurantes()

restaurantes_iniciales = [
    {
        "cif": "A28010000",
        "nombre": "DiverXO",
        "chef": "Dabiz Muñoz",
        "ciudad": "Madrid",
        "tipo_cocina": "Fusión vanguardista",
        "estrellas_michelin": "3",
        "precio_medio": "250€"
    }
]

# Guardar en CSV para tener registro legible
sistema_texto.guardar_en_csv(restaurantes_iniciales)

# Log de operación en TXT
sistema_texto.guardar_en_texto("✓ Restaurante DiverXO registrado en el sistema")

# ===== PASO 2: Indexar en sistema hash para búsqueda rápida =====
from 002-sistema_hash import SistemaRestaurantesHash

sistema_hash = SistemaRestaurantesHash()

# Indexar cada restaurante
for rest in restaurantes_iniciales:
    exito, hash_id = sistema_hash.guardar_restaurante_hash(rest)
    print(f"Indexado: {rest['nombre']} → Hash: {hash_id}")

# Ahora puedo buscar en O(1)
diverxo = sistema_hash.buscar_restaurante_por_cif("A28010000")
print(f"Encontrado en tiempo constante: {diverxo['nombre']}")

# ===== PASO 3: Crear objeto completo con métodos y serializarlo =====
from 003-serializacion_pickle import Restaurante, SistemaRestaurantesBinario

# Crear objeto Restaurante con toda su funcionalidad
diverxo_obj = Restaurante(
    cif="A28010000",
    nombre="DiverXO",
    chef="Dabiz Muñoz",
    ciudad="Madrid",
    tipo_cocina="Fusión vanguardista",
    estrellas_michelin="3",
    precio_medio="250€"
)

# Agregar reservas
diverxo_obj.agregar_reserva("Juan Pérez", datetime(2026, 3, 15, 21, 0), 2)
diverxo_obj.agregar_reserva("María García", datetime(2026, 3, 20, 20, 30), 4)

# Agregar reseñas
diverxo_obj.agregar_reseña("foodlover123", 5, "Experiencia increíble, cada plato es arte puro")
diverxo_obj.agregar_reseña("gourmet_madrid", 5, "Dabiz Muñoz es un genio, 3 estrellas bien merecidas")

# Serializar con pickle
sistema_binario = SistemaRestaurantesBinario()
sistema_binario.guardar_restaurante_binario(diverxo_obj)

# ===== PASO 4: Ocultar información sensible en imagen =====
from 004-esteganografia import Esteganografia

estegano = Esteganografia()

# Información confidencial que quiero ocultar
datos_secretos = {
    "restaurante": "DiverXO",
    "receta_secreta": "Combinación de técnicas asiáticas con producto español",
    "proveedores": ["Mercado de San Miguel", "Lonja de Getaria"],
    "margen_beneficio": "45%"
}

# Ocultar en imagen
estegano.codificar_imagen(
    ruta_imagen_original="logo_diverxo.png",
    datos=datos_secretos,
    ruta_imagen_salida="restaurantes_datos/imagenes/logo_con_datos_ocultos.png"
)

print("✓ Datos confidenciales ocultos en la imagen")
print("  A simple vista: imagen normal")
print("  Con decodificador: información completa recuperable")

# ===== PASO 5: Analizar toda la estructura creada =====
from 005-explorador_directorios import ExploradorRestaurantes

explorador = ExploradorRestaurantes()

print("\n" + "="*60)
print("ESTRUCTURA COMPLETA DEL SISTEMA DE DATOS")
print("="*60)

# Generar árbol visual
explorador.recorrer_directorio_recursivo()

# Generar informe completo
informe = explorador.generar_informe_completo()
print(f"\nTotal archivos: {informe['estadisticas']['total_archivos']}")
print(f"Tamaño total: {explorador.formatear_tamaño(informe['estadisticas']['tamaño_total'])}")
```

**Salida del programa**:
```
✓ Datos guardados en CSV: restaurantes_datos/texto/restaurantes.csv
✓ Registro guardado en: restaurantes_datos/texto/registro.txt
✓ Restaurante guardado con hash: 27d125e8ce2adc341c37078042e995bf
  CIF: A28010000 → Hash: 27d125e8ce2adc341c37078042e995bf
Indexado: DiverXO → Hash: 27d125e8ce2adc341c37078042e995bf
✓ Restaurante encontrado usando hash: 27d125e8ce2adc341c37078042e995bf
Encontrado en tiempo constante: DiverXO
✓ Restaurante serializado y guardado: A28010000.pkl
✓ Datos codificados exitosamente en la imagen
  Mensaje: 127 caracteres
  Imagen guardada en: restaurantes_datos/imagenes/logo_con_datos_ocultos.png

============================================================
ESTRUCTURA COMPLETA DEL SISTEMA DE DATOS
============================================================
restaurantes_datos/
├── 📁 binario/
│   └── 🔒 A28010000.pkl (2.45 KB)
├── 📁 hash/
│   └── 📋 27d125e8ce2adc341c37078042e995bf.json (512 B)
├── 📁 imagenes/
│   └── 🖼️ logo_con_datos_ocultos.png (156.34 KB)
└── 📁 texto/
    ├── 📊 restaurantes.csv (1.23 KB)
    └── 📝 registro.txt (456 B)

Total archivos: 5
Tamaño total: 160.45 KB
```

### Errores Comunes y Cómo Evitarlos

#### Error 1: No especificar encoding UTF-8
```python
# ✗ INCORRECTO
with open("restaurantes.csv", 'w') as archivo:  # encoding por defecto
    # Falla con caracteres españoles (ñ, á, é, í, ó, ú)

# ✓ CORRECTO
with open("restaurantes.csv", 'w', encoding='utf-8') as archivo:
    # Funciona perfectamente con todos los caracteres
```

#### Error 2: No cerrar archivos (fugas de recursos)
```python
# ✗ INCORRECTO
archivo = open("datos.txt", 'r')
contenido = archivo.read()
# ¡Nunca se cierra! Fuga de memoria

# ✓ CORRECTO (usa context manager)
with open("datos.txt", 'r', encoding='utf-8') as archivo:
    contenido = archivo.read()
    # Se cierra automáticamente al salir del bloque
```

#### Error 3: Confundir 'w' con 'a' en escritura
```python
# ✗ INCORRECTO - Borra todo el contenido previo
with open("registro.txt", 'w', encoding='utf-8') as archivo:
    archivo.write("Nueva entrada")  # ¡Perdí todos mis logs anteriores!

# ✓ CORRECTO - Añade al final
with open("registro.txt", 'a', encoding='utf-8') as archivo:
    archivo.write("Nueva entrada\n")  # Preserva logs anteriores
```

#### Error 4: No validar capacidad en esteganografía
```python
# ✗ INCORRECTO
def codificar_sin_validar(imagen, mensaje):
    # Intenta codificar sin verificar espacio
    # CRASH si mensaje > capacidad de la imagen

# ✓ CORRECTO
pixeles_necesarios = len(mensaje_binario)
pixeles_disponibles = imagen.size[0] * imagen.size[1] * 3

if pixeles_necesarios > pixeles_disponibles:
    print(f"✗ Error: La imagen es muy pequeña")
    return False
```

#### Error 5: Usar pickle con datos no confiables
```python
# ✗ PELIGROSO - pickle puede ejecutar código arbitrario
with open("datos_internet.pkl", 'rb') as f:
    datos = pickle.load(f)  # ¡NUNCA con archivos externos no fiables!

# ✓ SEGURO - Solo usa pickle con tus propios archivos
# Para datos externos, usa JSON
with open("datos_internet.json", 'r') as f:
    datos = json.load(f)  # Seguro, solo carga datos estructurados
```

#### Error 6: Olvidar el modo binario ('b') con pickle
```python
# ✗ INCORRECTO
with open("restaurante.pkl", 'w') as f:  # Falta la 'b'
    pickle.dump(obj, f)  # ERROR: pickle requiere modo binario

# ✓ CORRECTO
with open("restaurante.pkl", 'wb') as f:
    pickle.dump(obj, f)  # Correcto: 'wb' = write binary
```

#### Error 7: No manejar FileNotFoundError
```python
# ✗ INCORRECTO - Crash del programa
def leer_archivo(nombre):
    with open(nombre, 'r') as f:
        return f.read()
    # Si el archivo no existe, el programa explota

# ✓ CORRECTO - Manejo elegante del error
def leer_archivo(nombre):
    try:
        with open(nombre, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"✗ Archivo no encontrado: {nombre}")
        return ""
    except Exception as e:
        print(f"✗ Error al leer: {e}")
        return ""
```

---

En este proyecto he demostrado mi dominio sobre **5 técnicas fundamentales de persistencia de datos**:

**Puntos clave**:

1. **Archivos de texto (CSV/TXT)**: Ideales para datos estructurados legibles por humanos y logs
2. **Sistema de hashes (MD5)**: Búsqueda ultrarrápida O(1) vs O(n) secuencial, 1000x más eficiente
3. **Serialización pickle**: Almacena objetos Python completos con métodos y tipos complejos
4. **Esteganografía LSB**: Oculta información de forma imperceptible modificando bits menos significativos
5. **Explorador recursivo**: Navega y analiza estructuras de directorios completas

**Integración con contenidos de la unidad**:

- Este proyecto se conecta directamente con **"Manejo de ficheros"** (Unidad 001), donde aprendí las clases `open()`, `csv.DictWriter/Reader`, y modos de apertura ('r', 'w', 'a', 'b')

- Se relaciona con **"Serialización/deserialización de objetos"** (001-005), implementando pickle para persistencia completa

- Complementa **"Bases de datos documentales"** (Unidad 005), ya que JSON es un formato documental y mi sistema de hashes simula una base de datos NoSQL clave-valor

- Prepara el camino para **"Manejo de conectores"** (Unidad 002), porque entiendo perfectamente cómo persistir datos antes de trabajar con SQL

**Aplicabilidad profesional**:

He creado un sistema real que podría usarse en producción incorporando:
- Logs de auditoría (TXT)
- Exportaciones de datos (CSV)
- Caché de objetos complejos (pickle)
- Marcas de agua digitales (esteganografía)
- Monitoreo de sistema de archivos (explorador)

La clave que he aprendido es: **no existe una única solución óptima**. Cada técnica tiene su caso de uso ideal, y un desarrollador profesional debe dominarlas todas para elegir la herramienta correcta según el contexto.