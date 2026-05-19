<?php
  ob_start();                  // Start capturing output
  include "index.php";        // Execute the PHP file
  $html = ob_get_clean();      // Get the generated HTML
  file_put_contents("compilado.html", $html);
?>
