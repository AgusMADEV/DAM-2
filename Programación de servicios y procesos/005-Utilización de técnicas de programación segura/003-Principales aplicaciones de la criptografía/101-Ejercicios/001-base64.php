<?php
  $cadena = "Jose Vicente";
  echo $cadena;
  echo "<br>";
  
  $codificado = base64_encode($cadena);
  echo $codificado;
  echo "<br>";
  
  $descodificado = base64_decode($codificado);
  echo $descodificado;
  echo "<br>";
?>
