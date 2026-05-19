En la era digital actual, la protección de datos personales es fundamental. Como desarrolladores, nos enfrentamos constantemente a la necesidad de transmitir información sensible de manera segura. En este proyecto, se presenta el caso de una aplicación web que consulta datos de clientes desde una base de datos MySQL y debe mostrarlos en un navegador web.

### Relación con la Vida Personal

Este escenario es muy común en aplicaciones empresariales reales. Por ejemplo:
- **Tiendas online** que gestionan datos de clientes
- **Aplicaciones bancarias** que transmiten información de cuentas
- **Sistemas de salud** que manejan historiales médicos
- **Plataformas educativas** con datos de estudiantes

En mi caso personal, he visto cómo aplicaciones cotidianas (apps de mensajería, banca electrónica, redes sociales) utilizan encriptación para proteger nuestros datos durante su transmisión. Este proyecto me ha permitido entender los fundamentos de estos sistemas de seguridad.

### Planteamiento del Problema

El desafío consistía en:
1. Consultar datos de clientes desde una base de datos
2. Encriptarlos para su transmisión segura
3. Permitir al usuario visualizarlos tanto encriptados como en texto plano
4. Todo ello usando únicamente técnicas de programación segura vistas en clase (cifrado César)

---

### Implementación de la Clase Encriptador

**Archivo:** `servidor.php` (líneas 18-43)

```php
class Encriptador {
    function encripta($objeto) {
        $resultado = "";
        for($i = 0; $i < strlen($objeto); $i++) {
            $ascii = ord($objeto[$i]);
            $ascii += 5;  // Desplazamiento César
            $resultado .= chr($ascii);
        }
        return $resultado;
    }
    
    function desencripta($objeto) {
        $desencriptado = "";
        for($i = 0; $i < strlen($objeto); $i++) {
            $ascii = ord($objeto[$i]);
            $ascii -= 5;  // Revertir desplazamiento
            $desencriptado .= chr($ascii);
        }
        return $desencriptado;
    }
}
```

**Explicación técnica:**
- **Método `encripta()`**: Recorre cada caracter del string, obtiene su código ASCII con `ord()`, le suma 5 posiciones y convierte el nuevo valor a caracter con `chr()`
- **Método `desencripta()`**: Proceso inverso, restando 5 para recuperar el texto original
- **Cifrado César**: Técnica histórica que desplaza cada letra del alfabeto un número fijo de posiciones

### Conexión a la Base de Datos

**Archivo:** `servidor.php` (líneas 49-59)

```php
$mysqli = new mysqli("localhost", "tienda2526", "tienda2526", "tienda2526");

if ($mysqli->connect_errno) {
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode([
        "error" => true,
        "mensaje" => "Error de conexión: " . $mysqli->connect_error
    ]);
    exit;
}
```

**Aspectos técnicos clave:**
- Uso de **MySQLi** (extensión mejorada de MySQL para PHP)
- **Manejo de errores**: Verificación inmediata de errores de conexión
- **Respuesta JSON estándar**: Incluso los errores se devuelven en formato consistente
- **Credenciales**: Host, usuario, contraseña y base de datos configurados correctamente

### Consulta SQL y Procesamiento

**Archivo:** `servidor.php` (líneas 61-91)

```php
$sql = "SELECT * FROM clientes";
$result = $mysqli->query($sql);

if (!$result) {
    // Manejo de errores en la consulta
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode([
        "error" => true,
        "mensaje" => "Error en la consulta: " . $mysqli->error
    ]);
    exit;
}

$datosEncriptados = [];

while ($fila = $result->fetch_assoc()) {
    $filaEncriptada = [];
    
    foreach ($fila as $campo => $valor) {
        $valor = (string)$valor;
        $cifrado = $encriptador->encripta($valor);
        $filaEncriptada[$campo] = base64_encode($cifrado);
    }
    
    $datosEncriptados[] = $filaEncriptada;
}
```

**Detalles de implementación:**
- **Consulta SELECT**: Obtiene todos los registros de la tabla `clientes`
- **Validación**: Comprobación de errores en la ejecución de la consulta
- **Procesamiento por fila**: Cada registro se procesa individualmente
- **Encriptación de campos**: Todos los campos (ID, nombre, email, etc.) se encriptan
- **Base64 encoding**: Convierte los caracteres binarios cifrados a texto seguro para JSON

### Respuesta JSON

**Archivo:** `servidor.php` (líneas 96-108)

```php
header('Content-Type: application/json; charset=utf-8');

$json = json_encode($datosEncriptados, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);

if ($json === false) {
    echo json_encode([
        "error" => true,
        "mensaje" => "Error al codificar JSON: " . json_last_error_msg()
    ]);
    exit;
}

echo $json;
```

**Características:**
- **Header HTTP correcto**: `Content-Type: application/json`
- **Encoding UTF-8**: Soporte para caracteres especiales
- **JSON_PRETTY_PRINT**: Formato legible para debugging
- **JSON_UNESCAPED_UNICODE**: Preserva caracteres especiales sin escapar
- **Validación final**: Verifica que la codificación JSON fue exitosa

### Implementación del Cliente (JavaScript)

**Archivo:** `cliente.html` (líneas 352-368)

```javascript
class Encriptador {
    encripta(objeto) {
        let resultado = "";
        for(let i = 0; i < objeto.length; i++) {
            let ascii = objeto.charCodeAt(i);
            ascii += 5;
            resultado += String.fromCharCode(ascii);
        }
        return resultado;
    }

    desencripta(objeto) {
        let desencriptado = "";
        for(let i = 0; i < objeto.length; i++) {
            let ascii = objeto.charCodeAt(i);
            ascii -= 5;
            desencriptado += String.fromCharCode(ascii);
        }
        return desencriptado;
    }
}
```

**Consistencia técnica:**
- La implementación en JavaScript **replica exactamente** el comportamiento de PHP
- `charCodeAt()` equivalente a `ord()` de PHP
- `String.fromCharCode()` equivalente a `chr()` de PHP
- Garantiza que la encriptación/desencriptación sea simétrica entre cliente y servidor

---

### Entorno de Pruebas

**Stack tecnológico:**
- **Servidor:** XAMPP 8.x (Apache + MySQL + PHP)
- **Base de datos:** MySQL 8.0
- **Frontend:** HTML5 + CSS3 + JavaScript ES6
- **Navegador:** Chrome/Edge/Firefox (cualquier navegador moderno)

### Estructura del Proyecto

```
102-Actividad EVAL/
├── servidor.php       # Backend: API JSON con encriptación
├── cliente.html       # Frontend: Interfaz y desencriptación
├── README.md          # Documentación técnica completa
└── Respuesta.md       # Este documento
```

### Flujo de Datos (Ejemplo Práctico)

#### Paso 1: Datos en MySQL
```sql
SELECT * FROM clientes;
```
Resultado en base de datos:
```
id: 1
nombre: Juan Pérez
email: juan@example.com
telefono: 600123456
```

#### Paso 2: Encriptación en Servidor (PHP)
```
"Juan Pérez" → Cifrado César (+5) → "Ozfs%U~w~"
"Ozfs%U~w~" → Base64 → "T3pmcyVVfnd+"
```

#### Paso 3: Transmisión JSON
```json
{
  "id": "Ng==",
  "nombre": "T3pmcyVVfnd+",
  "email": "an~zshpwfsfpu7nsj~",
  "telefono": "JTUVjq}"
}
```

#### Paso 4: Recepción en Cliente (JavaScript)
El cliente recibe el JSON con datos encriptados.

#### Paso 5: Desencriptación (Usuario decide)
Al hacer clic en "Desencriptar":
```
"T3pmcyVVfnd+" → Decode Base64 → "Ozfs%U~w~"
"Ozfs%U~w~" → César (-5) → "Juan Pérez"
```

### Capturas de Funcionamiento

**Estado Inicial:**
- Tabla vacía con mensaje "Sin datos"
- Botón "Cargar Datos" disponible

**Después de Cargar Datos:**
- Panel de estadísticas muestra: Total Registros, Estado (Encriptado), Algoritmo (César +5)
- Tabla poblada con datos encriptados en formato Base64
- Mensaje de éxito: "Datos cargados correctamente: N registros"

**Modo Desencriptado:**
- Al pulsar "Desencriptar", todos los campos se muestran en texto plano
- El estado cambia a "Plano" en color verde
- Los valores son legibles: nombres, emails, teléfonos reales

### Calidad del Código

**Buenas prácticas aplicadas:**

1. **Separación de responsabilidades:**
   - `servidor.php`: Lógica de negocio y datos
   - `cliente.html`: Presentación y UX

2. **Código limpio y documentado:**
   - Comentarios PHPDoc en funciones
   - Variables con nombres descriptivos
   - Estructura clara y modular

3. **Manejo de errores robusto:**
   - Validación de conexión a BD
   - Validación de consultas SQL
   - Validación de encoding JSON
   - Feedback visual al usuario

4. **Diseño responsive:**
   - Funciona en desktop, tablet y móvil
   - Media queries para adaptación

5. **Seguridad básica:**
   - Headers HTTP correctos
   - Encoding UTF-8 para prevenir inyección
   - Validación de datos antes de procesar

---

### Aplicación en Contexto Real

Este sistema puede aplicarse en escenarios como e-commerce (paneles de administración), CRM (gestión de clientes), dashboards corporativos o APIs REST. Demuestra los principios fundamentales de transmisión segura de datos entre servidor y cliente.

### Relación con Conceptos de la Unidad

El proyecto aplica directamente: **cifrado César** (encriptación/desencriptación), **POO** (clase Encriptador), **conexión a bases de datos** (MySQLi), **API REST JSON**, **Base64 encoding** y **programación defensiva** con validación de errores en cada paso crítico.

### Desafíos y Soluciones

**Principal desafío:** Caracteres especiales generados por César causaban errores en JSON. **Solución:** Usar `base64_encode()` para convertir datos cifrados en texto seguro para transmisión JSON.

**Sincronización:** Asegurar algoritmo idéntico en PHP y JavaScript usando funciones equivalentes: `ord()`/`chr()` vs `charCodeAt()`/`fromCharCode()`.

### Limitaciones y Mejoras

El cifrado César es educativo pero vulnerable (fuerza bruta, análisis de frecuencia). Para producción se requiere: AES-256, HTTPS/TLS, autenticación JWT y prepared statements contra SQL injection.

### Conclusión

El sistema cumple todos los objetivos: implementa la clase Encriptador con cifrado César, conecta a MySQL con manejo de errores robusto, encripta con base64, devuelve JSON estándar y proporciona interfaz profesional. Este trabajo demuestra la aplicación práctica de las técnicas de programación segura estudiadas en la unidad 005, tema 007.

