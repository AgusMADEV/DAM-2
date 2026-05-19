<?php
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit(0);
}

$db = new SQLite3('moba.db');
$db->busyTimeout(2000);

// Players
$db->exec('CREATE TABLE IF NOT EXISTS players (
    id TEXT PRIMARY KEY,
    x REAL,
    y REAL,
    z REAL,
    last_update INTEGER
)');

// Bullets
$db->exec('CREATE TABLE IF NOT EXISTS bullets (
    id TEXT PRIMARY KEY,
    owner_id TEXT,
    x REAL,
    y REAL,
    z REAL,
    vx REAL,
    vy REAL,
    vz REAL,
    created INTEGER,
    last_update INTEGER
)');

$playerId = $_SERVER['REMOTE_ADDR'];
$now = time();

// ----------------------------
// Helper: update bullet physics
// ----------------------------
function step_bullets(SQLite3 $db, int $now) {
    // Move bullets based on elapsed seconds since last_update
    $res = $db->query("SELECT id, x, y, z, vx, vy, vz, last_update, created FROM bullets");
    $update = $db->prepare("UPDATE bullets SET x = ?, y = ?, z = ?, last_update = ? WHERE id = ?");

    while ($row = $res->fetchArray(SQLITE3_ASSOC)) {
        $dt = max(0, $now - (int)$row['last_update']); // seconds, integer resolution is fine here
        if ($dt > 0) {
            $x = (float)$row['x'] + (float)$row['vx'] * $dt;
            $y = (float)$row['y'] + (float)$row['vy'] * $dt;
            $z = (float)$row['z'] + (float)$row['vz'] * $dt;

            $update->bindValue(1, $x, SQLITE3_FLOAT);
            $update->bindValue(2, $y, SQLITE3_FLOAT);
            $update->bindValue(3, $z, SQLITE3_FLOAT);
            $update->bindValue(4, $now, SQLITE3_INTEGER);
            $update->bindValue(5, $row['id'], SQLITE3_TEXT);
            $update->execute();
        }
    }

    // Cleanup bullets:
    // - older than 3 seconds
    // - or out of bounds
    $db->exec("DELETE FROM bullets WHERE created < " . ($now - 3));
    $db->exec("DELETE FROM bullets WHERE ABS(x) > 20 OR ABS(z) > 20");
}

// ----------------------------
// Handle POST: update player, optionally insert bullet
// ----------------------------
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);
    if (!is_array($input)) $input = [];

    $x = isset($input['x']) ? (float)$input['x'] : 0.0;
    $y = isset($input['y']) ? (float)$input['y'] : 0.0;
    $z = isset($input['z']) ? (float)$input['z'] : 0.0;

    // Update/insert player
    $stmt = $db->prepare('INSERT OR REPLACE INTO players (id, x, y, z, last_update) VALUES (?, ?, ?, ?, ?)');
    $stmt->bindValue(1, $playerId, SQLITE3_TEXT);
    $stmt->bindValue(2, $x, SQLITE3_FLOAT);
    $stmt->bindValue(3, $y, SQLITE3_FLOAT);
    $stmt->bindValue(4, $z, SQLITE3_FLOAT);
    $stmt->bindValue(5, $now, SQLITE3_INTEGER);
    $stmt->execute();

    // Optional shot
    if (isset($input['shot']) && is_array($input['shot'])) {
        $shot = $input['shot'];

        // Minimal validation
        $bid = isset($shot['id']) ? (string)$shot['id'] : '';
        if ($bid !== '') {
            $bx = isset($shot['x']) ? (float)$shot['x'] : $x;
            $by = isset($shot['y']) ? (float)$shot['y'] : 0.35;
            $bz = isset($shot['z']) ? (float)$shot['z'] : $z;
            $vx = isset($shot['vx']) ? (float)$shot['vx'] : 0.0;
            $vy = isset($shot['vy']) ? (float)$shot['vy'] : 0.0;
            $vz = isset($shot['vz']) ? (float)$shot['vz'] : 0.0;
            $created = isset($shot['created']) ? (int)$shot['created'] : $now;

            // Insert bullet (ignore duplicates (same id) by replacing)
            $bst = $db->prepare('INSERT OR REPLACE INTO bullets (id, owner_id, x, y, z, vx, vy, vz, created, last_update)
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)');
            $bst->bindValue(1, $bid, SQLITE3_TEXT);
            $bst->bindValue(2, $playerId, SQLITE3_TEXT);
            $bst->bindValue(3, $bx, SQLITE3_FLOAT);
            $bst->bindValue(4, $by, SQLITE3_FLOAT);
            $bst->bindValue(5, $bz, SQLITE3_FLOAT);
            $bst->bindValue(6, $vx, SQLITE3_FLOAT);
            $bst->bindValue(7, $vy, SQLITE3_FLOAT);
            $bst->bindValue(8, $vz, SQLITE3_FLOAT);
            $bst->bindValue(9, $created, SQLITE3_INTEGER);
            $bst->bindValue(10, $now, SQLITE3_INTEGER);
            $bst->execute();
        }
    }
}

// Remove inactive players (> 5s)
$db->exec("DELETE FROM players WHERE last_update < " . ($now - 5));

// Step bullets on every request (simple authoritative sim)
step_bullets($db, $now);

// Get other players
$players = [];
$pstmt = $db->prepare("SELECT id, x, y, z FROM players WHERE id != ?");
$pstmt->bindValue(1, $playerId, SQLITE3_TEXT);
$pres = $pstmt->execute();
while ($row = $pres->fetchArray(SQLITE3_ASSOC)) {
    $players[] = $row;
}

// Get all bullets EXCEPT your own (so you see yours locally; avoids double bullets)
$bullets = [];
$bstmt = $db->prepare("SELECT id, owner_id, x, y, z FROM bullets WHERE owner_id != ?");
$bstmt->bindValue(1, $playerId, SQLITE3_TEXT);
$bres = $bstmt->execute();
while ($row = $bres->fetchArray(SQLITE3_ASSOC)) {
    $bullets[] = [
        "id" => $row["id"],
        "x"  => (float)$row["x"],
        "y"  => (float)$row["y"],
        "z"  => (float)$row["z"],
        "owner_id" => $row["owner_id"]
    ];
}

echo json_encode([
    "players" => $players,
    "bullets" => $bullets
]);

