<?php

$conexion = new mysqli("localhost", "chatjocarsa", "chatjocarsa", "chatjocarsa");

$resultado = $conexion->query("SELECT * FROM conversaciones ORDER BY fecha DESC");
$json = [];
while ($fila = $resultado->fetch_assoc()) {
    $json[] = $fila;
}

echo json_encode($json);

$conexion->close();
