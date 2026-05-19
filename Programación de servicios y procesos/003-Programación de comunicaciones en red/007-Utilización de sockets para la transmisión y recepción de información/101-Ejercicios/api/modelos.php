<?php

include "inc/config.php";

$resultado = $conexion->query("
  SELECT * FROM modelos;
");
$json = [];
while ($fila = $resultado->fetch_assoc()) {
    $json[] = $fila;
}

echo json_encode($json);

$conexion->close();
