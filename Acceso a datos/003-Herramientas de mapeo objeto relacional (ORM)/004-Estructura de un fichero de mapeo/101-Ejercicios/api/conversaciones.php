<?php

$conexion = new mysqli("localhost", "chatjocarsa", "chatjocarsa", "chatjocarsa");

$resultado = $conexion->query("
  SELECT * FROM conversaciones 
  WHERE usuario_nombre = ".$_GET['idusuario']."
  ORDER BY fecha DESC
  ");
$json = [];
while ($fila = $resultado->fetch_assoc()) {
    $json[] = $fila;
}

echo json_encode($json);

$conexion->close();
