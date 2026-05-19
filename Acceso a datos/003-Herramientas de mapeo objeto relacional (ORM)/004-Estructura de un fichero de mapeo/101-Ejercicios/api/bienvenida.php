<?php

$conexion = new mysqli("localhost", "chatjocarsa", "chatjocarsa", "chatjocarsa");

$resultado = $conexion->query("
  SELECT frase
  FROM frases_bienvenida
  WHERE activa = 1
  ORDER BY RAND()
  LIMIT 1;
");
$json = [];
while ($fila = $resultado->fetch_assoc()) {
    $json[] = $fila;
}

echo json_encode($json);

$conexion->close();
