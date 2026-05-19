<?php 
// Conexión a la base de datos
$conexion = mysqli_connect("localhost","usuarioempresarial","usuarioempresarial","empresarial"); 

// Procesar eliminación si se solicita
if(isset($_GET['operacion']) && $_GET['operacion'] == "eliminar" && isset($_GET['id'])){
  $id_eliminar = $_GET['id'];
  $tabla = $_GET['tabla'];
  mysqli_query($conexion, "DELETE FROM ".$tabla." WHERE Identificador = ".$id_eliminar.";");
  // Redirigir para evitar reenvío del formulario
  header("Location: mostrar_tabla.php?tabla=".$tabla);
  exit();
}
?>
<!doctype html>
<html lang="es">
  <head>
    <title>Sistema de Gestión - Ver Tabla</title>
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
        display:flex;
        justify-content:space-between;
        align-items:center;
      }
      .botones-header{
        display:flex;
        gap:10px;
      }
      .botones-header a{
        background:white;
        color:var(--color_primario);
        text-decoration:none;
        padding:10px 20px;
        border-radius:var(--radio);
        font-weight:bold;
      }
      .botones-header a:hover{
        background:aliceblue;
      }
      main{
        padding:var(--margen);
        flex:1;
      }
      table{
        width:100%;
        border:3px solid var(--color_primario);
        border-collapse:collapse;
        background:white;
      }
      table tr:nth-child(even){
        background:#f5f5f5;
      }
      table td{
        padding:calc(var(--margen)/2);
      }
      table th{
        background:var(--color_primario);
        padding:calc(var(--margen)/2);
        color:white;
      }
      .eliminar{
        width:25px;
        height:25px;
        background:red;
        color:white;
        border-radius:50px;
        line-height:25px;
        font-weight:bold;
        display:inline-block;
        text-decoration:none;
        text-align:center;
      }
      .eliminar:hover{
        background:darkred;
      }
    </style>
  </head>
  <body>
    <header>
      <div>
        <h1>Sistema de Gestión Empresarial</h1>
        <?php if(isset($_GET['tabla'])){ echo "<p>Tabla: ".$_GET['tabla']."</p>"; } ?>
      </div>
      <div class="botones-header">
        <a href="listar_tablas.php">← Volver al menú</a>
        <?php if(isset($_GET['tabla'])){ 
          echo "<a href='añadir_registro.php?tabla=".$_GET['tabla']."'>+ Añadir registro</a>"; 
        } ?>
      </div>
    </header>
    <main>
      <?php
        if(isset($_GET['tabla'])){
          $tabla = $_GET['tabla'];
          
          // Consulta para obtener los registros de la tabla
          $resultado = mysqli_query($conexion, "SELECT * FROM ".$tabla.";");
          
          if(mysqli_num_rows($resultado) > 0){
            echo "<table>";
            $contador = 0;
            
            // Mostrar registros
            while($fila = mysqli_fetch_assoc($resultado)){
              // Primera fila: encabezados
              if($contador == 0){
                echo "<tr>";
                foreach($fila as $clave=>$valor){
                  echo "<th>".$clave."</th>";
                }
                echo "<th>Acciones</th>";
                echo "</tr>";
              }
              
              // Filas de datos
              echo "<tr>";
              foreach($fila as $clave=>$valor){
                echo "<td>".$valor."</td>";
              }
              echo "<td><a href='?operacion=eliminar&tabla=".$tabla."&id=".$fila['Identificador']."' class='eliminar' onclick='return confirm(\"¿Estás seguro de eliminar este registro?\")'>x</a></td>";
              echo "</tr>";
              $contador++;
            }
            
            echo "</table>";
          }else{
            echo "<p>No hay registros en esta tabla.</p>";
          }
        }else{
          echo "<p>No se ha seleccionado ninguna tabla.</p>";
        }
      ?>
    </main>
  </body>
</html>
