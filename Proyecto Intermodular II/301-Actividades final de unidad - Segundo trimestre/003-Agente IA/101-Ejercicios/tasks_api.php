<?php
/**
 * Sistema de Gestión de Tareas - API REST CRUD
 * Generado por Agente IA Autónomo usando Ollama (qwen2.5-coder:7b)
 * Iteración 3 - Progreso: 70%
 */

header('Content-Type: application/json');

// Conexión a la base de datos
$host = 'localhost';
$dbname = 'tasks_db';
$user = 'root';
$password = '';
try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $user, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die(json_encode(['error' => 'Error de conexión a la base de datos: ' . $e->getMessage()]));
}

// Función para ejecutar consultas
function executeQuery($query, $params = []) {
    global $pdo;
    try {
        $stmt = $pdo->prepare($query);
        $stmt->execute($params);
        return $stmt;
    } catch (PDOException $e) {
        die(json_encode(['error' => 'Error en la consulta: ' . $e->getMessage()]));
    }
}

// Endpoints

// Crear tarea
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $title = $_POST['title'];
    $description = $_POST['description'];
    $status = $_POST['status'];

    if (empty($title) || empty($description) || empty($status)) {
        die(json_encode(['error' => 'Todos los campos son requeridos']));
    }

    $query = "INSERT INTO tasks (title, description, status) VALUES (:title, :description, :status)";
    executeQuery($query, ['title' => $title, 'description' => $description, 'status' => $status]);
    echo json_encode(['message' => 'Tarea creada con éxito']);
}

// Listar tareas
if ($_SERVER['REQUEST_METHOD'] == 'GET') {
    $status = $_GET['status'] ?? null;
    $search = $_GET['search'] ?? null;

    $query = "SELECT * FROM tasks";
    if ($status) {
        $query .= " WHERE status = :status";
    }
    if ($search) {
        $query .= " WHERE title LIKE CONCAT('%', :search, '%')";
    }

    $params = [];
    if ($status) {
        $params['status'] = $status;
    }
    if ($search) {
        $params['search'] = $search;
    }

    $stmt = executeQuery($query, $params);
    echo json_encode(['tasks' => $stmt->fetchAll(PDO::FETCH_ASSOC)]);
}

// Actualizar tarea
if ($_SERVER['REQUEST_METHOD'] == 'PUT') {
    parse_str(file_get_contents('php://input'), $_PUT);
    $id = $_PUT['id'];
    $title = $_PUT['title'];
    $description = $_PUT['description'];
    $status = $_PUT['status'];

    if (empty($title) || empty($description) || empty($status)) {
        die(json_encode(['error' => 'Todos los campos son requeridos']));
    }

    $query = "UPDATE tasks SET title = :title, description = :description, status = :status WHERE id = :id";
    executeQuery($query, ['id' => $id, 'title' => $title, 'description' => $description, 'status' => $status]);
    echo json_encode(['message' => 'Tarea actualizada con éxito']);
}

// Eliminar tarea
if ($_SERVER['REQUEST_METHOD'] == 'DELETE') {
    parse_str(file_get_contents('php://input'), $_DELETE);
    $id = $_DELETE['id'];

    if (empty($id)) {
        die(json_encode(['error' => 'ID de tarea requerido']));
    }

    $query = "DELETE FROM tasks WHERE id = :id";
    executeQuery($query, ['id' => $id]);
    echo json_encode(['message' => 'Tarea eliminada con éxito']);
}
?>
