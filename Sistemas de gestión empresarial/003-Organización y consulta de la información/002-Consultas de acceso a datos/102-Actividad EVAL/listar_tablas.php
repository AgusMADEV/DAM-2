<?php 
// Conexión a la base de datos
$conexion = mysqli_connect("localhost","usuarioempresarial","usuarioempresarial","empresarial"); 
?>
<!doctype html>
<html lang="es">
  <head>
    <title>Sistema de Gestión - Listar Tablas</title>
    <meta charset="utf-8">
    <style>
      :root{
        --margen: 20px;
        --color_primario: indigo;
        --radio: 5px;
      }
      html,body{
        width:100%;
        height:100%;
        padding:0px;
        margin:0px;
        font-family:sans-serif;
      }
      body{
        display:flex;
        flex-direction: column;
        background:aliceblue;
      }
      header{
        background:var(--color_primario);
        color:white;
        padding:var(--margen);
        text-align:center;
      }
      main{
        padding:var(--margen);
        flex:1;
      }
      .menu-tablas{
        display:flex;
        flex-direction:column;
        gap:var(--margen);
        max-width:400px;
        margin:20px auto;
      }
      .menu-tablas a{
        background:white;
        color:var(--color_primario);
        text-decoration:none;
        padding:var(--margen);
        border-radius:var(--radio);
        border:2px solid var(--color_primario);
        text-align:center;
        font-weight:bold;
        transition: all 0.3s;
      }
      .menu-tablas a:hover{
        background:var(--color_primario);
        color:white;
      }
    </style>
  </head>
  <body>
    <header>
      <h1>Sistema de Gestión Empresarial</h1>
      <p>Seleccione una tabla para gestionar</p>
    </header>
    <main>
      <div class="menu-tablas">
        <?php
          // Consulta para obtener todas las tablas de la base de datos
          $resultado = mysqli_query($conexion, "SHOW TABLES;");
          
          // Generar enlace para cada tabla
          while($fila = mysqli_fetch_assoc($resultado)){
            $nombre_tabla = $fila['Tables_in_empresarial'];
            echo "<a href='mostrar_tabla.php?tabla=".$nombre_tabla."'>".$nombre_tabla."</a>";
          }
        ?>
      </div>
    </main>
  </body>
</html>
