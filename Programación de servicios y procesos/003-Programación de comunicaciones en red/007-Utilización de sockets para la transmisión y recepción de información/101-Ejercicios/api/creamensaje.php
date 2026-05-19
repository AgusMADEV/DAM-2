<?php

include "inc/config.php";

$resultado = $conexion->query("
  INSERT INTO mensajes_conversacion VALUES(
    NULL,
    ".$_GET['id'].",
    NOW(),
    ".$_GET['usuario'].",
    '".$_GET['titulo']."'
  );
");


$conexion->close();
