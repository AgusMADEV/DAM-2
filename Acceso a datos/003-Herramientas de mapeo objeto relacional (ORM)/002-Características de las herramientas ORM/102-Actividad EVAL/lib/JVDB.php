<?php

/**
 * Clase JVDB - Gestor de Base de Datos MySQL
 * 
 * Esta clase implementa una interfaz simplificada para interactuar con
 * bases de datos MySQL, proporcionando métodos para operaciones CRUD básicas.
 * 
 * Métodos disponibles:
 * - seleccionar($tabla): Devuelve todos los registros de una tabla en JSON
 * - buscar($tabla, $columna, $valor): Busca registros por criterio
 * - tablas(): Lista todas las tablas de la base de datos
 */
class JVDB {
    private $host;
    private $usuario;
    private $contrasena;
    private $basedatos;
    private $conexion;

    /**
     * Constructor - Establece la conexión con la base de datos
     * 
     * @param string $host Servidor de la base de datos
     * @param string $usuario Usuario de MySQL
     * @param string $contrasena Contraseña de MySQL
     * @param string $basedatos Nombre de la base de datos
     */
    public function __construct($host, $usuario, $contrasena, $basedatos) {
        $this->host = $host;
        $this->usuario = $usuario;
        $this->contrasena = $contrasena;
        $this->basedatos = $basedatos;

        // Crear conexión con mysqli
        $this->conexion = new mysqli($this->host, $this->usuario, $this->contrasena, $this->basedatos);
        
        // Verificar si la conexión fue exitosa
        if ($this->conexion->connect_error) {
            die("Error de conexión: " . $this->conexion->connect_error);
        }
    }

    /**
     * Método seleccionar - Obtiene todos los registros de una tabla
     * 
     * @param string $tabla Nombre de la tabla a consultar
     * @return string JSON con los datos obtenidos
     */
    public function seleccionar($tabla) {
        $sql = "SELECT * FROM $tabla";
        $resultado = $this->conexion->query($sql);

        // Verificar si la consulta fue exitosa
        if (!$resultado) {
            return json_encode(["error" => "Error en la consulta: " . $this->conexion->error], JSON_UNESCAPED_UNICODE);
        }

        $datos = [];
        // Usar fetch_assoc para obtener datos en formato asociativo
        while ($fila = $resultado->fetch_assoc()) {
            $datos[] = $fila;
        }

        // Devolver datos en formato JSON
        return json_encode($datos, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    }

    /**
     * Método buscar - Busca registros por un criterio específico
     * 
     * @param string $tabla Nombre de la tabla
     * @param string $columna Nombre de la columna a buscar
     * @param string $valor Valor a buscar (búsqueda parcial con LIKE)
     * @return string JSON con los resultados
     */
    public function buscar($tabla, $columna, $valor) {
        $sql = "SELECT * FROM $tabla WHERE $columna LIKE ?";
        $stmt = $this->conexion->prepare($sql);
        $like = "%" . $valor . "%";
        $stmt->bind_param("s", $like);
        $stmt->execute();

        $resultado = $stmt->get_result();
        $datos = [];
        while ($fila = $resultado->fetch_assoc()) {
            $datos[] = $fila;
        }

        return json_encode($datos, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    }

    /**
     * Método tablas - Lista todas las tablas de la base de datos
     * 
     * @return string JSON con los nombres de las tablas
     */
    public function tablas() {
        $sql = "SHOW TABLES";
        $resultado = $this->conexion->query($sql);

        $datos = [];
        while ($fila = $resultado->fetch_array()) {
            $datos[] = $fila[0];
        }

        return json_encode($datos, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    }

    /**
     * Destructor - Cierra la conexión al finalizar
     */
    public function __destruct() {
        if ($this->conexion) {
            $this->conexion->close();
        }
    }
}
?>
