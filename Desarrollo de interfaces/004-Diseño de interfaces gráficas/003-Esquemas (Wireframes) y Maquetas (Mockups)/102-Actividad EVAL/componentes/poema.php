<style>
  .poema-container h1{
    color:#2c3e50;
    text-align:center;
    margin-top:20px;
  }
  .poema-container h2{
    color:#7f8c8d;
    text-align:center;
    font-style:italic;
    font-weight:normal;
  }
  .poema-container .info-poema{
    text-align:center;
    color:#666;
    margin-bottom:30px;
  }
  .estrofa{
    margin:20px 0;
    padding:15px;
    background:#f8f9fa;
    border-left:4px solid #3498db;
  }
  .estrofa p{
    margin:5px 0;
    line-height:1.6;
    color:#2c3e50;
  }
  .metadatos{
    margin-top:40px;
    padding:20px;
    background:#ecf0f1;
    border-radius:5px;
  }
  .metadatos h3{
    color:#2c3e50;
    margin-top:10px;
  }
  .metadatos p{
    color:#555;
  }
  .volver{
    display:inline-block;
    margin-top:20px;
    padding:10px 20px;
    background:#3498db;
    color:white;
    text-decoration:none;
    border-radius:5px;
  }
  .volver:hover{
    background:#2980b9;
  }
</style>

<main>
  <div class="poema-container">
    <?php
    // 3. VISUALIZACIÓN INDIVIDUAL DEL POEMA
    if(isset($_GET['poema'])){
      $nombrePoema = $_GET['poema'];
      $jsonFile = 'api/poemas/' . $nombrePoema . '.json';
      
      // Verificar que el archivo existe
      if(file_exists($jsonFile)){
        $jsonData = file_get_contents($jsonFile);
        $poema = json_decode($jsonData, true);
        $poemaData = $poema['poema'];

        // Mostrar título y autor
        echo "<h1>" . htmlspecialchars($poemaData['titulo']) . "</h1>";
        echo "<h2>de " . htmlspecialchars($poemaData['autor']) . "</h2>";
        echo "<p class='info-poema'><strong>Libro:</strong> " . htmlspecialchars($poemaData['libro']) . " (" . htmlspecialchars($poemaData['año']) . ")</p>";

        // Mostrar estrofas y versos
        foreach ($poemaData['estrofas'] as $estrofa) {
            echo "<div class='estrofa'>";
            foreach ($estrofa['versos'] as $verso) {
                echo "<p>" . htmlspecialchars($verso) . "</p>";
            }
            echo "</div>";
        }

        // Mostrar metadatos
        echo "<div class='metadatos'>";
        echo "<h3>Temas:</h3><p>" . implode(", ", $poemaData['temas']) . "</p>";
        echo "<h3>Símbolos:</h3><p>" . implode(", ", $poemaData['simbolos']) . "</p>";
        echo "</div>";
        
        echo "<a href='?p=poemas' class='volver'>← Volver a la lista de poemas</a>";
      } else {
        echo "<h2>Error: Poema no encontrado</h2>";
        echo "<p>El archivo del poema solicitado no existe.</p>";
        echo "<a href='?p=poemas' class='volver'>← Volver a la lista de poemas</a>";
      }
    } else {
      echo "<h2>Error: No se ha especificado ningún poema</h2>";
      echo "<a href='?p=poemas' class='volver'>← Volver a la lista de poemas</a>";
    }
    ?>
  </div>
</main>
