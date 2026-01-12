<?php
// Variables PHP para información de la aplicación
$tituloPagina = isset($tituloPagina) ? $tituloPagina : "Backoffice Empresarial";
$usuarioActual = isset($_GET['usuario']) ? htmlspecialchars($_GET['usuario']) : "Invitado";
$seccionActual = isset($_GET['seccion']) ? htmlspecialchars($_GET['seccion']) : "Dashboard";
?>

<style>
  *{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  
  body{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
  
  #header{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px 30px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  }
  
  #header h1{
    font-size: 28px;
    margin-bottom: 5px;
  }
  
  #header .info-usuario{
    font-size: 14px;
    opacity: 0.9;
  }
  
  #principal{
    display: flex;
    width: 100%;
    min-height: calc(100vh - 80px);
  }
  
  #principal nav{
    flex: 0 0 280px;
    background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    padding: 25px;
    box-shadow: 2px 0 10px rgba(0,0,0,0.1);
  }
  
  #principal section{
    flex: 1;
    background: #f5f7fa;
    padding: 30px;
    overflow-y: auto;
  }
  
  #principal section h2{
    color: #2c3e50;
    margin-bottom: 20px;
    font-size: 26px;
  }
  
  #principal section .contenido-seccion{
    background: white;
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    min-height: 400px;
  }
  
  #footer{
    background: #2c3e50;
    color: white;
    padding: 15px 30px;
    text-align: center;
    font-size: 14px;
  }
</style>

<header id="header">
  <h1><?php echo $tituloPagina; ?></h1>
  <div class="info-usuario">
    👤 Usuario conectado: <strong><?php echo $usuarioActual; ?></strong> | 
    📍 Sección actual: <strong><?php echo ucfirst($seccionActual); ?></strong>
  </div>
</header>

<main id="principal">
  <nav>
    <?php include "menu.php"; ?>
  </nav>
  <section>
    <h2>Bienvenido, <?php echo $usuarioActual; ?></h2>
    <div class="contenido-seccion">
      <p>Esta es la aplicación de backoffice empresarial. Utilice el menú lateral para navegar entre las diferentes secciones.</p>
      <br>
      <h3>Información del Sistema:</h3>
      <ul>
        <li><strong>Título:</strong> <?php echo $tituloPagina; ?></li>
        <li><strong>Usuario:</strong> <?php echo $usuarioActual; ?></li>
        <li><strong>Sección:</strong> <?php echo $seccionActual; ?></li>
        <li><strong>Fecha:</strong> <?php echo date('d/m/Y H:i:s'); ?></li>
      </ul>
    </div>
  </section>
</main>

<footer id="footer">
  © <?php echo date('Y'); ?> - <?php echo $tituloPagina; ?> - Todos los derechos reservados
</footer>

<script>
  // Script para mantener información del usuario
  console.log("Usuario actual:", "<?php echo $usuarioActual; ?>");
  console.log("Sección actual:", "<?php echo $seccionActual; ?>");
</script>
