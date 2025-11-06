<?php
header('Content-Type: application/json');

if (isset($_GET['ruta']) && $_GET['ruta'] == "categorias") {
    require "config.php";

    // Prepare and execute query
    $stmt = $pdo->prepare("SELECT * FROM categorias_aplicaciones");
    $stmt->execute();

    // Fetch all results as associative array
    $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Return as JSON
    echo json_encode($result, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
}

if (isset($_GET['ruta']) && $_GET['ruta'] == "aplicaciones") {
    require "config.php";

    // Prepare and execute query
    $stmt = $pdo->prepare("SELECT * FROM aplicaciones");
    $stmt->execute();

    // Fetch all results as associative array
    $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Return as JSON
    echo json_encode($result, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
}
?>

