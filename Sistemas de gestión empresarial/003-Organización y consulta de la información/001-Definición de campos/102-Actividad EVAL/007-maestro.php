<!doctype html>
<html lang="es">
  <head>
    <title>Sistema de Enrutamiento - SGE</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
      body {
        font-family: Arial, sans-serif;
        max-width: 800px;
        margin: 50px auto;
        padding: 20px;
        background-color: #f4f4f4;
      }
      h1 {
        color: #333;
        border-bottom: 3px solid #4CAF50;
        padding-bottom: 10px;
      }
      h2 {
        color: #555;
      }
      p {
        line-height: 1.6;
        color: #666;
      }
      ul {
        list-style-type: none;
        padding: 0;
      }
      li {
        margin: 10px 0;
      }
      a {
        color: #4CAF50;
        text-decoration: none;
        font-weight: bold;
      }
      a:hover {
        text-decoration: underline;
      }
      .welcome-box {
        background-color: white;
        padding: 30px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
      }
    </style>
  </head>
  <body>
    <div class="welcome-box">
      <?php
        // Incluir el enrutador
        include 'index.php';
      ?>
    </div>
  </body>
</html>
