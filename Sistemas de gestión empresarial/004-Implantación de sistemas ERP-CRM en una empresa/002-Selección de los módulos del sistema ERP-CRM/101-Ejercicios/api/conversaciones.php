<?php

$conexion = new mysqli("localhost", "chatjocarsa", "chatjocarsa", "chatjocarsa");


$resultado = $conexion->query("SELECT * FROM conversaciones");

while ($fila = $resultado->fetch_assoc()) {
    var_dump($fila);
}

$conexion->close();
