<?php
/**
 * ACTIVIDAD EVALUABLE - Sistema de Encriptación de Datos de Clientes
 * 
 * Este archivo implementa un servidor PHP que:
 * 1. Define una clase Encriptador con cifrado César
 * 2. Se conecta a la base de datos MySQL
 * 3. Consulta los datos de clientes
 * 4. Encripta cada campo usando el método César
 * 5. Devuelve los datos en formato JSON
 */

// MODO DEBUG (activar durante desarrollo)
error_reporting(E_ALL);
ini_set('display_errors', 1);

/**
 * Clase Encriptador
 * Implementa el método de cifrado César con desplazamiento de 5 posiciones
 */
class Encriptador {
    /**
     * Encripta un string usando cifrado César
     * @param string $objeto - El texto a encriptar
     * @return string - El texto encriptado
     */
    function encripta($objeto) {
        $resultado = "";
        for($i = 0; $i < strlen($objeto); $i++) {
            $ascii = ord($objeto[$i]);
            $ascii += 5;  // Desplazamiento de 5 posiciones (cifrado César)
            $resultado .= chr($ascii);
        }
        return $resultado;
    }
    
    /**
     * Desencripta un string cifrado con César
     * @param string $objeto - El texto encriptado
     * @return string - El texto original
     */
    function desencripta($objeto) {
        $desencriptado = "";
        for($i = 0; $i < strlen($objeto); $i++) {
            $ascii = ord($objeto[$i]);
            $ascii -= 5;  // Revertir el desplazamiento
            $desencriptado .= chr($ascii);
        }
        return $desencriptado;
    }
}

// Crear instancia del encriptador
$encriptador = new Encriptador();

// PASO 2: Conectar a la base de datos MySQL
$mysqli = new mysqli("localhost", "tienda2526", "tienda2526", "tienda2526");

// Comprobar la conexión
if ($mysqli->connect_errno) {
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode([
        "error" => true,
        "mensaje" => "Error de conexión a la base de datos: " . $mysqli->connect_error
    ]);
    exit;
}

// PASO 3: Consultar los datos de clientes
$sql = "SELECT * FROM customers";
$result = $mysqli->query($sql);

// Comprobar si la consulta fue exitosa
if (!$result) {
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode([
        "error" => true,
        "mensaje" => "Error en la consulta SQL: " . $mysqli->error
    ]);
    exit;
}

// Array para almacenar los datos encriptados
$datosEncriptados = [];

// PASO 4: Encriptar los datos de cada cliente
while ($fila = $result->fetch_assoc()) {
    $filaEncriptada = [];
    
    // Procesar cada campo del registro
    foreach ($fila as $campo => $valor) {
        // Convertir el valor a string para asegurar compatibilidad
        $valor = (string)$valor;
        
        // Aplicar el método encripta de la clase Encriptador
        $cifrado = $encriptador->encripta($valor);
        
        // Convertir a texto seguro para JSON usando base64_encode
        $filaEncriptada[$campo] = base64_encode($cifrado);
    }
    
    // Agregar la fila encriptada al array de resultados
    $datosEncriptados[] = $filaEncriptada;
}

// Cerrar la conexión a la base de datos
$mysqli->close();

// PASO 5: Imprimir los datos en formato JSON
header('Content-Type: application/json; charset=utf-8');

// Codificar a JSON con formato legible
$json = json_encode($datosEncriptados, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);

// Verificar si hubo errores en la codificación
if ($json === false) {
    echo json_encode([
        "error" => true,
        "mensaje" => "Error al codificar JSON: " . json_last_error_msg()
    ]);
    exit;
}

// Enviar el JSON al cliente
echo $json;
?>
