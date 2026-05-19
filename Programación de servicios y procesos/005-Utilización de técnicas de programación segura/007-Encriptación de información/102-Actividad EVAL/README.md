# 🔐 ACTIVIDAD EVALUABLE - Sistema de Encriptación de Datos de Clientes

## 📋 Descripción del Proyecto

Este proyecto implementa un sistema web seguro que muestra datos de clientes de una base de datos MySQL, utilizando **cifrado César** para proteger la información durante su transmisión. Los datos se encriptan en el servidor y pueden ser desencriptados en el cliente.

## 🎯 Objetivos Cumplidos

### 1. ✅ Clase Encriptador Definida
- **Ubicación**: `servidor.php` (líneas 18-43)
- **Método `encripta`**: Toma un string y lo cifra usando el algoritmo César con desplazamiento de 5 posiciones
- **Método `desencripta`**: Revierte el cifrado César para obtener el texto original

### 2. ✅ Conexión a Base de Datos
- **Credenciales**:
  - Host: `localhost`
  - Usuario: `tienda2526`
  - Contraseña: `tienda2526`
  - Base de datos: `tienda2526`
- **Ubicación**: `servidor.php` (líneas 49-59)

### 3. ✅ Consulta de Datos de Clientes
- **Consulta SQL**: `SELECT * FROM clientes`
- **Almacenamiento**: Array asociativo
- **Ubicación**: `servidor.php` (líneas 61-70)

### 4. ✅ Encriptación de Datos
Para cada campo de cada registro:
1. Se convierte a string
2. Se aplica el método `encripta()` de la clase `Encriptador`
3. Se codifica con `base64_encode()` para hacerlo seguro en JSON
- **Ubicación**: `servidor.php` (líneas 75-91)

### 5. ✅ Salida en Formato JSON
- Header: `Content-Type: application/json; charset=utf-8`
- Formato: JSON con UTF-8 y formato legible (JSON_PRETTY_PRINT)
- **Ubicación**: `servidor.php` (líneas 96-108)

## 📁 Estructura de Archivos

```
102-Actividad EVAL/
├── servidor.php    # Backend: Clase Encriptador + conexión DB + API JSON
├── cliente.html    # Frontend: Interfaz visual + desencriptación en cliente
└── README.md       # Esta documentación
```

## 🔧 Tecnologías Utilizadas

- **PHP 7.4+**: Servidor y lógica de encriptación
- **MySQL**: Base de datos de clientes
- **HTML5 + CSS3**: Interfaz de usuario moderna
- **JavaScript ES6**: Lógica del cliente y desencriptación
- **XAMPP**: Servidor local de desarrollo

## 🚀 Cómo Usar

### Requisitos Previos
1. XAMPP instalado y en ejecución
2. Base de datos `tienda2526` con tabla `clientes`
3. Credenciales de acceso configuradas

### Pasos de Ejecución
1. Asegúrate de que Apache y MySQL estén corriendo en XAMPP
2. Abre el archivo `cliente.html` en tu navegador:
   ```
   http://localhost/DAM-2/.../102-Actividad EVAL/cliente.html
   ```
3. Haz clic en el botón **"Cargar Datos"** para obtener los clientes encriptados
4. Usa el botón **"Desencriptar"** para alternar entre datos encriptados y desencriptados

## 🔐 Algoritmo de Cifrado César

### En el Servidor (PHP)
```php
function encripta($objeto) {
    $resultado = "";
    for($i = 0; $i < strlen($objeto); $i++) {
        $ascii = ord($objeto[$i]);
        $ascii += 5;  // Desplazamiento de 5
        $resultado .= chr($ascii);
    }
    return $resultado;
}
```

### En el Cliente (JavaScript)
```javascript
desencripta(objeto) {
    let desencriptado = "";
    for(let i = 0; i < objeto.length; i++) {
        let ascii = objeto.charCodeAt(i);
        ascii -= 5;  // Revertir desplazamiento
        desencriptado += String.fromCharCode(ascii);
    }
    return desencriptado;
}
```

## 🔄 Flujo de Datos

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   MySQL     │      │  servidor.php │      │ cliente.html│
│  (clientes) │─────▶│  Encriptador  │─────▶│ Desencripta │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ▼
                     1. Cifrado César (+5)
                     2. Base64 encode
                     3. JSON encode
```

## 📊 Ejemplo de Datos

### Dato Original
```
"Juan"
```

### Después de César (+5)
```
"Ozfs" (binario cifrado)
```

### Después de Base64
```
"T3pmcw==" (texto seguro para JSON)
```

### JSON Final
```json
{
    "nombre": "T3pmcw=="
}
```

## 🎨 Características de la Interfaz

- ✨ Diseño moderno con tema oscuro
- 📊 Panel de información con estadísticas
- 🔄 Alternancia entre modo encriptado/desencriptado
- 📱 Responsive design
- 🎯 Indicadores visuales de estado (encriptado en amarillo, desencriptado en verde)
- ⚡ Carga asíncrona de datos con fetch API

## 🔒 Restricciones Cumplidas

- ❌ **No se usan librerías externas** de encriptación
- ✅ **Solo cifrado César** como técnica de programación segura
- ✅ **Implementación manual** del algoritmo de encriptación
- ✅ **Código propio** sin dependencias externas

## 📝 Notas Técnicas

### Seguridad
El cifrado César es un método educativo y **NO debe usarse en producción**. Es vulnerable a:
- Análisis de frecuencia
- Fuerza bruta (solo 25 posibles claves)
- Ataques de texto plano conocido

Para aplicaciones reales, usar:
- AES-256
- RSA
- TLS/HTTPS
- Hashing con bcrypt o Argon2

### Base64 Encoding
Se usa `base64_encode()` para convertir los caracteres binarios cifrados en texto seguro para JSON, evitando problemas con caracteres especiales o no imprimibles.

## 👥 Equipo de Desarrollo

Actividad realizada como parte del módulo:
- **Asignatura**: Programación de Servicios y Procesos
- **Unidad**: 005 - Utilización de técnicas de programación segura
- **Tema**: 007 - Encriptación de información

## 📚 Referencias

- Apuntes de clase en carpeta `101-Ejercicios/`
- Ejercicio base: `005-metodos de una clase.php`
- Ejercicio avanzado: `008-ahora encripto.php`

---

**Fecha de creación**: 8 de febrero de 2026  
**Versión**: 1.0  
**Estado**: ✅ Completado
