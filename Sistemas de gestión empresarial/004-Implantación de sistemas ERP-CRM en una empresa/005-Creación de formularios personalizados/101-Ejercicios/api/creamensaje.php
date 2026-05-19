<?php

$conexion = new mysqli("localhost", "chatjocarsa", "chatjocarsa", "chatjocarsa");

$resultado = $conexion->query("
  INSERT INTO mensajes_conversacion VALUES(
    NULL,
    ".$_GET['id'].",
    NOW(),
    1,
    '".$_GET['titulo']."'
  );
");


$conexion->close();
