<?php

$conexion = new mysqli("localhost", "chatjocarsa", "chatjocarsa", "chatjocarsa");

$resultado = $conexion->query("SELECT * FROM mensajes_conversacion WHERE conversacion_id = ".$_GET['id']);
$json = [];
while ($fila = $resultado->fetch_assoc()) {
    $json[] = $fila;
}

echo json_encode($json);

$conexion->close();
