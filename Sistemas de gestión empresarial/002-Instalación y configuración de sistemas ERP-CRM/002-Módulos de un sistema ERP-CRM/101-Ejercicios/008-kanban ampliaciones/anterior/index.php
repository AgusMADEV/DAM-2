<?php
  session_start();
  if(!isset($_SESSION['usuario'])){
    header("Location: iniciarsesion/index.html");
    exit;
  }
?>
<!doctype html>
<html lang="es">
  <head>
    <title>ERP Jose Vicente</title>
    <meta charset="utf-8">
    <link rel="stylesheet" href="comun/estilo.css">
  </head>
  <body>
    <?php include "cabecera/index.php" ?>
    <?php /*include "listadodemodulos/index.php"*/ ?>
    <?php include "plantillas/kanban/index.php" ?>
  </body>
</html>
