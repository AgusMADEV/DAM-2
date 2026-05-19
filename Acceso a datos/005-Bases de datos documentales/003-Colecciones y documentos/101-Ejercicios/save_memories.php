<?php
header('Content-Type: application/json');

// Ruta al archivo JSON donde se guardarán los recuerdos
$file = 'memories.json';

// Obtener los datos enviados
$data = json_decode(file_get_contents('php://input'), true);

// Si es una solicitud POST, guardar los datos
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $memories = [];
    if (file_exists($file)) {
        $memories = json_decode(file_get_contents($file), true);
    }
    $memories[] = $data;
    file_put_contents($file, json_encode($memories, JSON_PRETTY_PRINT));
    echo json_encode(['success' => true]);
    exit;
}

// Si es una solicitud GET, devolver los recuerdos guardados
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    if (file_exists($file)) {
        echo file_get_contents($file);
    } else {
        echo json_encode([]);
    }
    exit;
}
?>

