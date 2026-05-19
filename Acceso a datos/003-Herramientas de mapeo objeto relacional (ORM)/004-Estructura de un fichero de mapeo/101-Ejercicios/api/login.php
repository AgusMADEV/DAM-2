<?php

$conexion = new mysqli("localhost", "chatjocarsa", "chatjocarsa", "chatjocarsa");
$peticion = "
  SELECT * FROM usuarios
  WHERE usuario = '".$_GET['usuario']."'
  AND 
  contrasena = '".$_GET['contrasena']."'
";
$resultado = $conexion->query($peticion);
//echo $peticion;
$json = [];
while ($fila = $resultado->fetch_assoc()) {
    $json[] = $fila;
}

echo json_encode($json);

$conexion->close();
