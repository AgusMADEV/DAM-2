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

// SQL query
$sql = "SELECT * FROM clientes";
$result = $conn->query($sql);

$data = array();

if ($result->num_rows > 0) {
    // Fetch all rows as an associative array
    while($row = $result->fetch_assoc()) {
        $data[] = $row;
    }
} else {
    $data = ["message" => "No records found"];
}

// Close connection
$conn->close();

// Return JSON response
echo json_encode($data);
?>

