<?php
/*
   Enrutador de muestra - Actividad de Práctica
   Sistemas de gestión empresarial
   Alimenta a la interfaz, bebe de la base de datos
*/

$routes = [
    'GET' => [
        '/' => function() { echo "<h1>Página Principal</h1><p>Bienvenido al sistema de enrutamiento</p>"; },
        '/contacto' => function() { echo "<h1>Página de Contacto</h1><p>Contáctanos en: contacto@ejemplo.com</p>"; },
        '/acerca' => function() { echo "<h1>Acerca de Nosotros</h1><p>Sistema de enrutamiento desarrollado para SGE</p>"; },
        '/hola' => function() {
            echo "<h1>¡Bienvenido/a!</h1>";
            echo "<p>Esta es una ruta personalizada creada para la práctica de enrutamiento.</p>";
            echo "<p>Fecha y hora actual: " . date('d/m/Y H:i:s') . "</p>";
        },
        '/menu' => function() { 
            $elementos = ['Productos','Servicios','Empleados'];
            echo json_encode($elementos, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
        },
        '/tabla' => function() { 

            $alumnos = [
                [
                    "id" => 1,
                    "nombre" => "Ana",
                    "apellidos" => "García López",
                    "curso" => "DAM 1",
                    "nota" => 8.5,
                    "estado" => "Aprobado"
                ],
                [
                    "id" => 2,
                    "nombre" => "Luis",
                    "apellidos" => "Martínez Pérez",
                    "curso" => "DAW 2",
                    "nota" => 6.7,
                    "estado" => "Aprobado"
                ],
                [
                    "id" => 3,
                    "nombre" => "María",
                    "apellidos" => "Sánchez Ruiz",
                    "curso" => "ASIR 1",
                    "nota" => 4.9,
                    "estado" => "Suspenso"
                ],
                [
                    "id" => 4,
                    "nombre" => "Carlos",
                    "apellidos" => "Fernández Gil",
                    "curso" => "DAM 2",
                    "nota" => 9.1,
                    "estado" => "Aprobado"
                ],
                [
                    "id" => 5,
                    "nombre" => "Elena",
                    "apellidos" => "Hernández Soto",
                    "curso" => "DAW 1",
                    "nota" => 7.3,
                    "estado" => "Aprobado"
                ]
            ];

            echo json_encode($alumnos, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
        },
    ]
];

$method = $_SERVER['REQUEST_METHOD'];
$path = $_SERVER['REQUEST_URI'];

$parsed = parse_url($path);
$cleanPath = $parsed['path'];

// Remove your project base path
$base = '/dam-2/Sistemas%20de%20gesti%C3%B3n%20empresarial/003-Organizaci%C3%B3n%20y%20consulta%20de%20la%20informaci%C3%B3n/001-Definici%C3%B3n%20de%20campos/102-Actividad%20EVAL';
$finalPath = str_replace($base, '', $cleanPath);

if (empty($finalPath)) {
    $finalPath = '/';
}

if (isset($routes[$method][$finalPath])) {
    $routes[$method][$finalPath]();
} else {
    echo "<h2>404 - Ruta no encontrada</h2>";
    echo "<p>Lo siento, la página que estás buscando no existe.</p>";
    echo "<p>Rutas disponibles:</p>";
    echo "<ul>";
    foreach (array_keys($routes['GET']) as $route) {
        echo "<li><a href='$route'>$route</a></li>";
    }
    echo "</ul>";
}
