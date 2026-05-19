<?php 
// Conexión a la base de datos
$conexion = mysqli_connect("localhost","usuarioempresarial","usuarioempresarial","empresarial"); 

// Procesar el formulario cuando se envía
if($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['tabla'])){
  $tabla = $_POST['tabla'];
  
  // Construir la consulta INSERT
  $campos = array();
  $valores = array();
  
  foreach($_POST as $clave=>$valor){
    if($clave != 'tabla' && $valor != ''){
      $campos[] = $clave;
      $valores[] = "'".$valor."'";
    }
  }
  
  if(count($campos) > 0){
    $sql = "INSERT INTO ".$tabla." (".implode(", ", $campos).") VALUES (".implode(", ", $valores).");";
    mysqli_query($conexion, $sql);
    
    // Redirigir a la tabla después de insertar
    header("Location: mostrar_tabla.php?tabla=".$tabla);
    exit();
  }
}
?>
<!doctype html>
<html lang="es">
  <head>
    <title>Sistema de Gestión - Añadir Registro</title>
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
      form{
        max-width:800px;
        margin:20px auto;
        background:white;
        padding:var(--margen);
        border-radius:var(--radio);
        border:2px solid var(--color_primario);
        display:grid;
        grid-template-columns: 1fr 1fr;
        gap:var(--margen);
      }
      form input{
        width:100%;
        padding:var(--margen);
        box-sizing:border-box;
        border:1px solid var(--color_primario);
        border-radius:var(--radio);
      }
      form input[type=submit]{
        background:var(--color_primario);
        color:white;
        font-weight:bold;
        cursor:pointer;
        grid-column: 1 / -1;
      }
      form input[type=submit]:hover{
        background:darkblue;
      }
      .info{
        background:#fff3cd;
        padding:var(--margen);
        border-radius:var(--radio);
        border:1px solid #ffc107;
        margin-bottom:var(--margen);
        max-width:800px;
        margin:20px auto;
      }
    </style>
  </head>
  <body>
    <header>
      <div>
        <h1>Sistema de Gestión Empresarial</h1>
        <?php if(isset($_GET['tabla'])){ echo "<p>Añadir registro a: ".$_GET['tabla']."</p>"; } ?>
      </div>
      <div class="botones-header">
        <?php if(isset($_GET['tabla'])){ 
          echo "<a href='mostrar_tabla.php?tabla=".$_GET['tabla']."'>← Volver a la tabla</a>"; 
        } ?>
      </div>
    </header>
    <main>
      <?php
        if(isset($_GET['tabla'])){
          $tabla = $_GET['tabla'];
          
          echo "<div class='info'>Rellena los campos que desees. Los campos vacíos no se incluirán en el registro.</div>";
          
          echo "<form method='POST' action='añadir_registro.php'>";
          echo "<input type='hidden' name='tabla' value='".$tabla."'>";
          
          // Obtener la estructura de la tabla
          $resultado = mysqli_query($conexion, "SELECT * FROM ".$tabla." LIMIT 1;");
          
          if($fila = mysqli_fetch_assoc($resultado)){
            foreach($fila as $clave=>$valor){
              // No mostrar campo para el identificador (auto-increment)
              if($clave != 'Identificador'){
                echo "<input type='text' name='".$clave."' placeholder='".$clave."'>";
              }
            }
          }
          
          echo "<input type='submit' value='Añadir registro'>";
          echo "</form>";
        }else{
          echo "<p>No se ha seleccionado ninguna tabla.</p>";
        }
      ?>
    </main>
  </body>
</html>
