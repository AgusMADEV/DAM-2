<?php
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit(0);
}

// Create/connect to SQLite database
$db = new SQLite3('moba.db');

// Create table if not exists
$db->exec('CREATE TABLE IF NOT EXISTS players (
    id TEXT PRIMARY KEY,
    x REAL,
    y REAL,
    z REAL,
    last_update INTEGER
)');

// Get client IP as player ID
$playerId = $_SERVER['REMOTE_ADDR'];
$now = time();

// Handle POST requests (update position)
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);
    $x = $input['x'] ?? 0;
    $y = $input['y'] ?? 0;
    $z = $input['z'] ?? 0;

    // Update or insert player position
    $stmt = $db->prepare('INSERT OR REPLACE INTO players (id, x, y, z, last_update) VALUES (?, ?, ?, ?, ?)');
    $stmt->bindValue(1, $playerId, SQLITE3_TEXT);
    $stmt->bindValue(2, $x, SQLITE3_FLOAT);
    $stmt->bindValue(3, $y, SQLITE3_FLOAT);
    $stmt->bindValue(4, $z, SQLITE3_FLOAT);
    $stmt->bindValue(5, $now, SQLITE3_INTEGER);
    $stmt->execute();
}

// Remove players inactive for more than 5 seconds
$db->exec("DELETE FROM players WHERE last_update < " . ($now - 5));

// Get all other players
$result = $db->query("SELECT id, x, y, z FROM players WHERE id != '$playerId'");
$players = [];
while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
    $players[] = $row;
}

echo json_encode($players);
?>
