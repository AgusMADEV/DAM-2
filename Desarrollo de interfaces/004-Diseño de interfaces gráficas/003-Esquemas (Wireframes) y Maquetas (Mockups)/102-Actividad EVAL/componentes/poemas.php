<style>
  main h3{
    color:#333;
    border-bottom:2px solid #ddd;
    padding-bottom:10px;
  }
  .libro-info{
    color:#666;
    font-size:0.9em;
    margin-bottom:10px;
  }
  main ul{
    list-style-type:none;
    padding-left:0;
  }
  main ul li{
    padding:8px 0;
    border-bottom:1px solid #eee;
  }
  main ul li a{
    color:#0066cc;
    text-decoration:none;
    transition:all 0.3s;
  }
  main ul li a:hover{
    color:#004499;
    text-decoration:underline;
  }
</style>

<main>
  <h2>Poemas de Federico García Lorca</h2>
  <?php
  // 1. CARGA DE DATOS desde el archivo JSON
  $jsonFile = 'api/poemas.json';
  $jsonData = file_get_contents($jsonFile);
  $data = json_decode($jsonData, true);

  // 2. MOSTRAR LISTA DE POEMAS por cada libro
  foreach ($data['obras_poeticas'] as $libro) {
      echo "<h3>" . htmlspecialchars($libro['libro']) . "</h3>\n";
      
      if (isset($libro['año']) || isset($libro['estilo'])) {
          echo "<div class='libro-info'>";
          if (isset($libro['año'])) {
              echo "Año: " . htmlspecialchars($libro['año']) . " | ";
          }
          if (isset($libro['estilo'])) {
              echo "Estilo: " . htmlspecialchars($libro['estilo']);
          }
          echo "</div>\n";
      }
      
      if (isset($libro['poemas']) && is_array($libro['poemas'])) {
          echo "<ul>\n";
          foreach ($libro['poemas'] as $poema) {
              echo "  <li><a href='?p=poema&poema=" . urlencode($poema['titulo']) . "'>" . htmlspecialchars($poema['titulo']) . "</a></li>\n";
          }
          echo "</ul>\n";
      }
      echo "<br>\n";
  }
  ?>
</main>
