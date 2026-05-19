<?php
include "../lib/JVDB.php";

$conexion = new JVDB("localhost", "blog2526", "blog2526", "blog2526");

$routes = [
    'GET' => [
        '/' => function() {
            echo "Home Page";
        },
        '/contact' => function() {
            echo "Contact Page";
        },
        '/menu' => function() use ($conexion) {
            header('Content-Type: application/json; charset=utf-8');
            echo $conexion->tablas();
        },
        '/tabla' => function() use ($conexion) {
            header('Content-Type: application/json; charset=utf-8');

            $tabla = $_GET['tabla'] ?? null;
            if (!$tabla) {
                http_response_code(400);
                echo json_encode(['error' => 'Falta parámetro tabla']);
                return;
            }

            // (Opcional pero recomendado) validar que la tabla existe:
            $todas = json_decode($conexion->tablas(), true);
            if (!in_array($tabla, $todas)) {
                http_response_code(400);
                echo json_encode(['error' => 'Tabla no permitida']);
                return;
            }

            echo $conexion->seleccionar($tabla);
        },
    ]
];


$method = $_SERVER['REQUEST_METHOD'];

// Obtengo solo la ruta, sin query string
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

// Normalizo codificación (espacios, acentos, etc.)
$path = urldecode($path);

// Directorio base donde está este script (api)
$base = rtrim(dirname($_SERVER['SCRIPT_NAME']), '/');

// Quito el base de delante
$finalPath = substr($path, strlen($base));

if ($finalPath === '' || $finalPath === false) {
    $finalPath = '/';
}

// DEBUG opcional:
// var_dump($path, $base, $finalPath);

if (isset($routes[$method][$finalPath])) {
    $routes[$method][$finalPath]();
} else {
    print_r(array_keys($routes['GET']));
    echo "<h2>404 - Route not found</h2>";
}

