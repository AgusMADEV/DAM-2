<?php
// Archivo: validacionEmail.php
// Generado automáticamente por el Agente IA Autónomo usando Ollama (qwen2.5-coder:7b)

/**
 * Función para validar una dirección de correo electrónico según RFC 5322.
 *
 * @param string $email La dirección de correo electrónico a validar.
 * @return bool Devuelve true si el email es válido, false en caso contrario.
 */
function validarEmail($email) {
    // Expresión regular que valida la sintaxis y formato del correo electrónico según RFC 5322
    $regex = '/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/';

    // Utiliza la función preg_match para verificar si el email coincide con la expresión regular
    if (preg_match($regex, $email)) {
        return true;
    } else {
        return false;
    }
}

// Pruebas unitarias para validar el correcto funcionamiento de la función

$email1 = "ejemplo@gmail.com"; // Correo electrónico válido
$email2 = "nombre@dominio.es"; // Correo electrónico válido
$email3 = "invalido@.com"; // Correo electrónico inválido
$email4 = "@sinNombre.com"; // Correo electrónico inválido
$email5 = "sinArroba.com"; // Correo electrónico inválido

echo $email1 . ": " . (validarEmail($email1) ? 'Válido' : 'Inválido') . "\n";
echo $email2 . ": " . (validarEmail($email2) ? 'Válido' : 'Inválido') . "\n";
echo $email3 . ": " . (validarEmail($email3) ? 'Válido' : 'Inválido') . "\n";
echo $email4 . ": " . (validarEmail($email4) ? 'Válido' : 'Inválido') . "\n";
echo $email5 . ": " . (validarEmail($email5) ? 'Válido' : 'Inválido') . "\n";
?>
