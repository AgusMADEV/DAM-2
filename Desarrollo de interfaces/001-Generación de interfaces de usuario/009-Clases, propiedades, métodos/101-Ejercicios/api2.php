<?php
header('Content-Type: application/json');

// Database configuration
$servername = "localhost";
$username = "crimson";
$password = "crimson";
$dbname = "crimson";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die(json_encode(["error" => "Connection failed: " . $conn->connect_error]));
}

// Get the action from the query string
$action = isset($_GET['action']) ? $_GET['action'] : null;

// Route logic
if ($action === 'tablas') {
    // Get list of tables
    $tables = array();
    $result = $conn->query("SHOW TABLES");
    while ($row = $result->fetch_array()) {
        $tables[] = $row[0];
    }
    echo json_encode($tables);
}
elseif ($action === 'tabla' && isset($_GET['name'])) {
    $table = $_GET['name'];
    // Sanitize table name to prevent SQL injection
    if (!preg_match('/^[a-zA-Z0-9_]+$/', $table)) {
        echo json_encode(["error" => "Invalid table name"]);
        exit;
    }
    // Select all from the specified table
    $sql = "SELECT * FROM `$table`";
    $result = $conn->query($sql);
    $data = array();
    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $data[] = $row;
        }
    } else {
        $data = ["message" => "No records found"];
    }
    echo json_encode($data);
}
else {
    echo json_encode(["error" => "Invalid or missing parameters"]);
}

// Close connection
$conn->close();
?>

