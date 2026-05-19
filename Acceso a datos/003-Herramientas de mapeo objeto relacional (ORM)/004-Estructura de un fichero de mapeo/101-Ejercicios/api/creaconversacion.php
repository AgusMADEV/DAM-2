<?php

header('Content-Type: application/json');

$conexion = new mysqli("localhost", "chatjocarsa", "chatjocarsa", "chatjocarsa");

$conexion->query("
  INSERT INTO conversaciones VALUES(
    NULL,
    1,
    1,
    NOW(),
    '".$conexion->real_escape_string($_GET['titulo'])."'
  )
");

echo json_encode([
  "ok" => true,
  "id" => $conexion->insert_id
]);

$conexion->close();

