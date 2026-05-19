<?php
session_start();
error_reporting(E_ALL);
ini_set('display_errors', 1);

//
// CONFIG
//
const DB_HOST = 'localhost';
const DB_NAME = 'ollama_api';
const DB_USER = 'apiinteligenciaartificial';
const DB_PASS = 'TAME123$';

//
// DB CONNECTION
//
function get_pdo(): PDO {
    static $pdo = null;
    if ($pdo === null) {
        $dsn = 'mysql:host=' . DB_HOST . ';dbname=' . DB_NAME . ';charset=utf8mb4';
        $pdo = new PDO($dsn, DB_USER, DB_PASS, [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]);
    }
    return $pdo;
}

//
// AUTH
//
function is_logged_in(): bool {
    return isset($_SESSION['admin_user_id']);
}

function require_login() {
    if (!is_logged_in()) {
        header("Location: ?login=1");
        exit;
    }
}

function html_escape($s) {
    return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8');
}

//
// HANDLE LOGIN / LOGOUT
//
if (isset($_GET['logout'])) {
    session_destroy();
    header("Location: ?login=1");
    exit;
}

$login_error = null;

if (isset($_POST['action']) && $_POST['action'] === 'do_login') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';

    try {
        $pdo = get_pdo();
        $stmt = $pdo->prepare("SELECT * FROM users WHERE username = :u AND password = :p AND is_active = 1 LIMIT 1");
        $stmt->execute([
            ':u' => $username,
            ':p' => $password
        ]);
        $user = $stmt->fetch();
        if ($user && $username === 'jocarsa' && $password === 'jocarsa') {
            $_SESSION['admin_user_id'] = $user['id'];
            $_SESSION['admin_username'] = $user['username'];
            header("Location: admin.php");
            exit;
        } else {
            $login_error = "Invalid credentials.";
        }
    } catch (Throwable $e) {
        $login_error = "Error: " . $e->getMessage();
    }
}

//
// LOGIN SCREEN
//
if (!is_logged_in() && isset($_GET['login'])) {
    ?>
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Admin Login</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                background: #f0f2f5;
                margin: 0;
            }
            .login-wrapper {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .login-box {
                background: #fff;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                width: 320px;
            }
            .login-box h1 {
                font-size: 20px;
                margin-bottom: 20px;
                text-align: center;
            }
            .login-box label {
                display: block;
                margin-bottom: 5px;
                font-weight: 600;
            }
            .login-box input[type="text"],
            .login-box input[type="password"] {
                width: 100%;
                padding: 8px;
                margin-bottom: 15px;
                border-radius: 4px;
                border: 1px solid #ccd0d4;
                box-sizing: border-box;
            }
            .login-box button {
                width: 100%;
                padding: 10px;
                background: #2271b1;
                color: #fff;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-weight: 600;
            }
            .login-box button:hover {
                background: #135e96;
            }
            .login-error {
                color: #b32d2e;
                margin-bottom: 10px;
                font-size: 14px;
            }
            .hint {
                margin-top: 10px;
                font-size: 12px;
                color: #555;
            }
        </style>
    </head>
    <body>
    <div class="login-wrapper">
        <div class="login-box">
            <h1>Admin Login</h1>
            <?php if ($login_error): ?>
                <div class="login-error"><?php echo html_escape($login_error); ?></div>
            <?php endif; ?>
            <form method="post">
                <input type="hidden" name="action" value="do_login">
                <label for="username">Username</label>
                <input type="text" name="username" id="username" value="jocarsa">
                <label for="password">Password</label>
                <input type="password" name="password" id="password" value="jocarsa">
                <button type="submit">Login</button>
            </form>
            <div class="hint">
                User: <code>jocarsa</code> / Pass: <code>jocarsa</code>
            </div>
        </div>
    </div>
    </body>
    </html>
    <?php
    exit;
}

//
// MAIN ADMIN
//
require_login();

$section = $_GET['section'] ?? 'dashboard';

try {
    $pdo = get_pdo();
} catch (Throwable $e) {
    die("DB connection error: " . html_escape($e->getMessage()));
}

//
// HANDLE ACTIONS (CRUD)
//
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = $_POST['action'] ?? '';

    try {
        switch ($action) {
            // USERS
            case 'add_user':
                $username = $_POST['username'] ?? '';
                $password = $_POST['password'] ?? '';
                $email    = $_POST['email'] ?? null;
                $is_active = isset($_POST['is_active']) ? 1 : 0;
                $stmt = $pdo->prepare("INSERT INTO users (username, password, email, is_active) VALUES (:u, :p, :e, :a)");
                $stmt->execute([
                    ':u' => $username,
                    ':p' => $password,
                    ':e' => $email,
                    ':a' => $is_active
                ]);
                break;
            case 'update_user':
                $id       = (int)($_POST['id'] ?? 0);
                $username = $_POST['username'] ?? '';
                $password = $_POST['password'] ?? '';
                $email    = $_POST['email'] ?? null;
                $is_active = isset($_POST['is_active']) ? 1 : 0;
                $stmt = $pdo->prepare("UPDATE users SET username=:u, password=:p, email=:e, is_active=:a WHERE id=:id");
                $stmt->execute([
                    ':u' => $username,
                    ':p' => $password,
                    ':e' => $email,
                    ':a' => $is_active,
                    ':id'=> $id
                ]);
                break;
            case 'delete_user':
                $id = (int)($_POST['id'] ?? 0);
                $stmt = $pdo->prepare("DELETE FROM users WHERE id=:id");
                $stmt->execute([':id' => $id]);
                break;

            // PLANS
            case 'add_plan':
                $name = $_POST['name'] ?? '';
                $description = $_POST['description'] ?? null;
                $qph = (int)($_POST['queries_per_hour'] ?? 60);
                $is_active = isset($_POST['is_active']) ? 1 : 0;
                $stmt = $pdo->prepare("INSERT INTO plans (name, description, queries_per_hour, is_active) VALUES (:n, :d, :q, :a)");
                $stmt->execute([
                    ':n' => $name,
                    ':d' => $description,
                    ':q' => $qph,
                    ':a' => $is_active
                ]);
                break;
            case 'update_plan':
                $id = (int)($_POST['id'] ?? 0);
                $name = $_POST['name'] ?? '';
                $description = $_POST['description'] ?? null;
                $qph = (int)($_POST['queries_per_hour'] ?? 60);
                $is_active = isset($_POST['is_active']) ? 1 : 0;
                $stmt = $pdo->prepare("UPDATE plans SET name=:n, description=:d, queries_per_hour=:q, is_active=:a WHERE id=:id");
                $stmt->execute([
                    ':n' => $name,
                    ':d' => $description,
                    ':q' => $qph,
                    ':a' => $is_active,
                    ':id'=> $id
                ]);
                break;
            case 'delete_plan':
                $id = (int)($_POST['id'] ?? 0);
                $stmt = $pdo->prepare("DELETE FROM plans WHERE id=:id");
                $stmt->execute([':id' => $id]);
                break;

            // USER PLANS
            case 'add_user_plan':
                $user_id = (int)($_POST['user_id'] ?? 0);
                $plan_id = (int)($_POST['plan_id'] ?? 0);
                $is_active = isset($_POST['is_active']) ? 1 : 0;
                $stmt = $pdo->prepare("INSERT INTO user_plans (user_id, plan_id, is_active) VALUES (:u, :p, :a)");
                $stmt->execute([
                    ':u' => $user_id,
                    ':p' => $plan_id,
                    ':a' => $is_active
                ]);
                break;
            case 'update_user_plan':
                $id = (int)($_POST['id'] ?? 0);
                $user_id = (int)($_POST['user_id'] ?? 0);
                $plan_id = (int)($_POST['plan_id'] ?? 0);
                $is_active = isset($_POST['is_active']) ? 1 : 0;
                $stmt = $pdo->prepare("UPDATE user_plans SET user_id=:u, plan_id=:p, is_active=:a WHERE id=:id");
                $stmt->execute([
                    ':u' => $user_id,
                    ':p' => $plan_id,
                    ':a' => $is_active,
                    ':id'=> $id
                ]);
                break;
            case 'delete_user_plan':
                $id = (int)($_POST['id'] ?? 0);
                $stmt = $pdo->prepare("DELETE FROM user_plans WHERE id=:id");
                $stmt->execute([':id' => $id]);
                break;

            // API KEYS
            case 'add_api_key':
                $user_id = (int)($_POST['user_id'] ?? 0);
                $description = $_POST['description'] ?? null;
                $api_key = bin2hex(random_bytes(16));
                $stmt = $pdo->prepare("INSERT INTO api_keys (user_id, api_key, description) VALUES (:u, :k, :d)");
                $stmt->execute([
                    ':u' => $user_id,
                    ':k' => $api_key,
                    ':d' => $description
                ]);
                break;
            case 'update_api_key':
                $id = (int)($_POST['id'] ?? 0);
                $description = $_POST['description'] ?? null;
                $is_active = isset($_POST['is_active']) ? 1 : 0;
                $stmt = $pdo->prepare("UPDATE api_keys SET description=:d, is_active=:a WHERE id=:id");
                $stmt->execute([
                    ':d' => $description,
                    ':a' => $is_active,
                    ':id'=> $id
                ]);
                break;
            case 'delete_api_key':
                $id = (int)($_POST['id'] ?? 0);
                $stmt = $pdo->prepare("DELETE FROM api_keys WHERE id=:id");
                $stmt->execute([':id' => $id]);
                break;

        }
    } catch (Throwable $e) {
        echo "<pre>Action error: " . html_escape($e->getMessage()) . "</pre>";
    }

    $redirectSection = $_POST['section'] ?? 'dashboard';
    header("Location: admin.php?section=" . urlencode($redirectSection));
    exit;
}

//
// FETCH DATA FOR VIEWS
//
$users = $plans = $user_plans = $api_keys = [];
if (in_array($section, ['users','user_plans','api_keys','reports'], true)) {
    $stmt = $pdo->query("SELECT * FROM users ORDER BY id ASC");
    $users = $stmt->fetchAll();
}
if (in_array($section, ['plans','user_plans','reports'], true)) {
    $stmt = $pdo->query("SELECT * FROM plans ORDER BY id ASC");
    $plans = $stmt->fetchAll();
}
if ($section === 'user_plans') {
    $sql = "SELECT up.*, u.username, p.name AS plan_name
            FROM user_plans up
            JOIN users u ON up.user_id = u.id
            JOIN plans p ON up.plan_id = p.id
            ORDER BY up.id ASC";
    $stmt = $pdo->query($sql);
    $user_plans = $stmt->fetchAll();
}
if ($section === 'api_keys') {
    $sql = "SELECT ak.*, u.username
            FROM api_keys ak
            JOIN users u ON ak.user_id = u.id
            ORDER BY ak.id ASC";
    $stmt = $pdo->query($sql);
    $api_keys = $stmt->fetchAll();
}

//
// REPORTING (existing)
//
$usage_by_user = [];
$usage_last = [];
if ($section === 'reports') {
    $sql = "SELECT u.username, SUM(au.request_count) AS total_requests
            FROM api_usage au
            JOIN api_keys ak ON au.api_key_id = ak.id
            JOIN users u ON ak.user_id = u.id
            GROUP BY u.id
            ORDER BY total_requests DESC";
    $stmt = $pdo->query($sql);
    $usage_by_user = $stmt->fetchAll();

    $sql = "SELECT au.*, ak.api_key, u.username
            FROM api_usage au
            JOIN api_keys ak ON au.api_key_id = ak.id
            JOIN users u ON ak.user_id = u.id
            ORDER BY au.hour_start DESC
            LIMIT 100";
    $stmt = $pdo->query($sql);
    $usage_last = $stmt->fetchAll();
}

//
// MONITORING: load JSONL logs (minutes, hours, weeks, months)
//
$monitor_data = [
    'minutes' => [
        'labels'    => [],
        'cpu'       => [],
        'ram'       => [],
        'gpu'       => [],
        'gpu_mem'   => [],
        'disk'      => [],
        'gpu_temp'  => [],
        'disk_temp' => [],
    ],
    'hours' => [
        'labels'    => [],
        'cpu'       => [],
        'ram'       => [],
        'gpu'       => [],
        'gpu_mem'   => [],
        'disk'      => [],
        'gpu_temp'  => [],
        'disk_temp' => [],
    ],
    'weeks' => [
        'labels'    => [],
        'cpu'       => [],
        'ram'       => [],
        'gpu'       => [],
        'gpu_mem'   => [],
        'disk'      => [],
        'gpu_temp'  => [],
        'disk_temp' => [],
    ],
    'months' => [
        'labels'    => [],
        'cpu'       => [],
        'ram'       => [],
        'gpu'       => [],
        'gpu_mem'   => [],
        'disk'      => [],
        'gpu_temp'  => [],
        'disk_temp' => [],
    ],
];

$current_cpu = $current_ram = $current_gpu = $current_gpu_mem = $current_disk = null;
$current_gpu_temp = $current_disk_temp = null;

if ($section === 'monitor') {
    $baseDir = __DIR__;

    $logFiles = [
        'minutes' => $baseDir . '/log_minutes.jsonl',
        'hours'   => $baseDir . '/log_hours.jsonl',
        'weeks'   => $baseDir . '/log_weeks.jsonl',
        'months'  => $baseDir . '/log_months.jsonl',
    ];

    // Max points per scale for charts
    $maxPoints = [
        'minutes' => 120, // last 120 minutes
        'hours'   => 72,  // last 72 hours
        'weeks'   => 52,  // last 52 weeks
        'months'  => 24,  // last 24 months
    ];

    // Helper: format labels based on timestamp + scale
    $makeLabel = function (?string $ts, string $scale): ?string {
        if (!$ts) {
            return null;
        }
        try {
            $dt = new DateTime($ts);
        } catch (Throwable $e) {
            return $ts;
        }

        switch ($scale) {
            case 'minutes':
                return $dt->format('H:i:s');
            case 'hours':
                return $dt->format('d-m H:i');
            case 'weeks':
                return 'W' . $dt->format('o-W'); // ISO week label
            case 'months':
                return $dt->format('Y-m');
            default:
                return $ts;
        }
    };

    foreach ($logFiles as $scale => $path) {
        if (!is_readable($path)) {
            continue;
        }

        $lines = file($path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
        if ($lines === false || empty($lines)) {
            continue;
        }

        $limit = $maxPoints[$scale] ?? 200;
        $lines = array_slice($lines, -$limit);

        foreach ($lines as $line) {
            $entry = json_decode($line, true);
            if (!is_array($entry)) {
                continue;
            }

            $ts = $entry['timestamp'] ?? null;
            $label = $makeLabel($ts, $scale);
            if ($label === null) {
                continue;
            }

            $monitor_data[$scale]['labels'][] = $label;

            // CPU
            $monitor_data[$scale]['cpu'][] = isset($entry['cpu_load_percent'])
                ? (float)$entry['cpu_load_percent']
                : null;

            // RAM %
            $ramPercent = $entry['ram']['percent'] ?? null;
            $monitor_data[$scale]['ram'][] = $ramPercent !== null
                ? (float)$ramPercent
                : null;

            // GPU (first GPU)
            $gpuUtil = null;
            $gpuMemPercent = null;
            $gpuTemp = null;
            if (!empty($entry['gpus']) && is_array($entry['gpus'])) {
                $firstGpu = $entry['gpus'][0];
                if (isset($firstGpu['util_gpu_percent'])) {
                    $gpuUtil = (float)$firstGpu['util_gpu_percent'];
                }
                if (isset($firstGpu['mem_percent'])) {
                    $gpuMemPercent = (float)$firstGpu['mem_percent'];
                }
                if (isset($firstGpu['temp_gpu_c'])) {
                    $gpuTemp = (float)$firstGpu['temp_gpu_c'];
                }
            }
            $monitor_data[$scale]['gpu'][]      = $gpuUtil;
            $monitor_data[$scale]['gpu_mem'][]  = $gpuMemPercent;
            $monitor_data[$scale]['gpu_temp'][] = $gpuTemp;

            // Disk
            $diskPercent = $entry['disk_nvme0n1p2']['percent'] ?? null;
            $diskTemp    = $entry['disk_nvme0n1p2']['temp_c'] ?? null;
            $monitor_data[$scale]['disk'][]      = $diskPercent !== null ? (float)$diskPercent : null;
            $monitor_data[$scale]['disk_temp'][] = $diskTemp !== null ? (float)$diskTemp : null;
        }
    }

    // Current state = last point from minutes scale (raw per-minute data)
    if (!empty($monitor_data['minutes']['labels'])) {
        $idx = count($monitor_data['minutes']['labels']) - 1;
        $current_cpu       = $monitor_data['minutes']['cpu'][$idx] ?? null;
        $current_ram       = $monitor_data['minutes']['ram'][$idx] ?? null;
        $current_gpu       = $monitor_data['minutes']['gpu'][$idx] ?? null;
        $current_gpu_mem   = $monitor_data['minutes']['gpu_mem'][$idx] ?? null;
        $current_disk      = $monitor_data['minutes']['disk'][$idx] ?? null;
        $current_gpu_temp  = $monitor_data['minutes']['gpu_temp'][$idx] ?? null;
        $current_disk_temp = $monitor_data['minutes']['disk_temp'][$idx] ?? null;
    }
}

//
// HTML LAYOUT
//
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ollama API Admin</title>
    <link rel="stylesheet" href="admin.css">
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
<div class="admin-header">
    <div class="title">Ollama API Admin</div>
    <div class="user-info">
        Logged in as <?php echo html_escape($_SESSION['admin_username'] ?? ''); ?> |
        <a href="?logout=1">Log out</a>
    </div>
</div>
<div class="admin-container">
    <div class="admin-sidebar">
        <a href="admin.php" class="<?php echo $section === 'dashboard' ? 'active' : ''; ?>">Dashboard</a>
        <a href="admin.php?section=users" class="<?php echo $section === 'users' ? 'active' : ''; ?>">Users</a>
        <a href="admin.php?section=plans" class="<?php echo $section === 'plans' ? 'active' : ''; ?>">Plans</a>
        <a href="admin.php?section=user_plans" class="<?php echo $section === 'user_plans' ? 'active' : ''; ?>">User Plans</a>
        <a href="admin.php?section=api_keys" class="<?php echo $section === 'api_keys' ? 'active' : ''; ?>">API Keys</a>
        <a href="admin.php?section=reports" class="<?php echo $section === 'reports' ? 'active' : ''; ?>">Reports</a>
        <a href="admin.php?section=monitor" class="<?php echo $section === 'monitor' ? 'active' : ''; ?>">Monitoring</a>
    </div>
    <div class="admin-content">
        <?php if ($section === 'dashboard'): ?>
            <h1>Dashboard</h1>
            <p>Welcome, <?php echo html_escape($_SESSION['admin_username'] ?? ''); ?>.</p>
            <p>Use the menu on the left to manage users, plans, API keys and view usage reports and system monitoring.</p>

        <?php elseif ($section === 'users'): ?>
            <h1>Users</h1>

            <form method="post" class="form-inline">
                <input type="hidden" name="action" value="add_user">
                <input type="hidden" name="section" value="users">
                <strong>Add User:</strong>
                <label>Username <input type="text" name="username" required></label>
                <label>Password <input type="text" name="password" required></label>
                <label>Email <input type="text" name="email"></label>
                <label><input type="checkbox" name="is_active" checked> Active</label>
                <button type="submit" class="button">Add</button>
            </form>

            <table>
                <tr>
                    <th>ID</th><th>Username</th><th>Password</th><th>Email</th><th>Active</th><th>Created</th><th>Actions</th>
                </tr>
                <?php foreach ($users as $u): ?>
                    <tr>
                        <form method="post">
                            <td><?php echo (int)$u['id']; ?>
                                <input type="hidden" name="id" value="<?php echo (int)$u['id']; ?>">
                                <input type="hidden" name="section" value="users">
                            </td>
                            <td><input type="text" name="username" value="<?php echo html_escape($u['username']); ?>"></td>
                            <td><input type="text" name="password" value="<?php echo html_escape($u['password']); ?>"></td>
                            <td><input type="text" name="email" value="<?php echo html_escape($u['email']); ?>"></td>
                            <td><input type="checkbox" name="is_active" <?php echo $u['is_active'] ? 'checked' : ''; ?>></td>
                            <td class="small"><?php echo html_escape($u['created_at']); ?></td>
                            <td>
                                <button type="submit" name="action" value="update_user" class="button secondary">Save</button>
                                <button type="submit" name="action" value="delete_user" class="button danger"
                                        onclick="return confirm('Delete this user?');">Delete</button>
                            </td>
                        </form>
                    </tr>
                <?php endforeach; ?>
            </table>

        <?php elseif ($section === 'plans'): ?>
            <h1>Plans</h1>

            <form method="post" class="form-inline">
                <input type="hidden" name="action" value="add_plan">
                <input type="hidden" name="section" value="plans">
                <strong>Add Plan:</strong>
                <label>Name <input type="text" name="name" required></label>
                <label>Description <input type="text" name="description"></label>
                <label>Queries/hour <input type="number" name="queries_per_hour" value="100"></label>
                <label><input type="checkbox" name="is_active" checked> Active</label>
                <button type="submit" class="button">Add</button>
            </form>

            <table>
                <tr>
                    <th>ID</th><th>Name</th><th>Description</th><th>Queries/hour</th><th>Active</th><th>Created</th><th>Actions</th>
                </tr>
                <?php foreach ($plans as $p): ?>
                    <tr>
                        <form method="post">
                            <td><?php echo (int)$p['id']; ?>
                                <input type="hidden" name="id" value="<?php echo (int)$p['id']; ?>">
                                <input type="hidden" name="section" value="plans">
                            </td>
                            <td><input type="text" name="name" value="<?php echo html_escape($p['name']); ?>"></td>
                            <td><input type="text" name="description" value="<?php echo html_escape($p['description']); ?>"></td>
                            <td><input type="number" name="queries_per_hour" value="<?php echo (int)$p['queries_per_hour']; ?>"></td>
                            <td><input type="checkbox" name="is_active" <?php echo $p['is_active'] ? 'checked' : ''; ?>></td>
                            <td class="small"><?php echo html_escape($p['created_at']); ?></td>
                            <td>
                                <button type="submit" name="action" value="update_plan" class="button secondary">Save</button>
                                <button type="submit" name="action" value="delete_plan" class="button danger"
                                        onclick="return confirm('Delete this plan?');">Delete</button>
                            </td>
                        </form>
                    </tr>
                <?php endforeach; ?>
            </table>

        <?php elseif ($section === 'user_plans'): ?>
            <h1>User Plans</h1>

            <form method="post" class="form-inline">
                <input type="hidden" name="action" value="add_user_plan">
                <input type="hidden" name="section" value="user_plans">
                <strong>Add User Plan:</strong>
                <label>User
                    <select name="user_id">
                        <?php foreach ($users as $u): ?>
                            <option value="<?php echo (int)$u['id']; ?>"><?php echo html_escape($u['username']); ?></option>
                        <?php endforeach; ?>
                    </select>
                </label>
                <label>Plan
                    <select name="plan_id">
                        <?php foreach ($plans as $p): ?>
                            <option value="<?php echo (int)$p['id']; ?>"><?php echo html_escape($p['name']); ?></option>
                        <?php endforeach; ?>
                    </select>
                </label>
                <label><input type="checkbox" name="is_active" checked> Active</label>
                <button type="submit" class="button">Add</button>
            </form>

            <table>
                <tr>
                    <th>ID</th><th>User</th><th>Plan</th><th>Started</th><th>Expires</th><th>Active</th><th>Actions</th>
                </tr>
                <?php
                $sql = "SELECT up.*, u.username, p.name AS plan_name
                        FROM user_plans up
                        JOIN users u ON up.user_id = u.id
                        JOIN plans p ON up.plan_id = p.id
                        ORDER BY up.id ASC";
                $stmt = $pdo->query($sql);
                $user_plans = $stmt->fetchAll();
                ?>
                <?php foreach ($user_plans as $up): ?>
                    <tr>
                        <form method="post">
                            <td><?php echo (int)$up['id']; ?>
                                <input type="hidden" name="id" value="<?php echo (int)$up['id']; ?>">
                                <input type="hidden" name="section" value="user_plans">
                            </td>
                            <td>
                                <select name="user_id">
                                    <?php foreach ($users as $u): ?>
                                        <option value="<?php echo (int)$u['id']; ?>"
                                            <?php echo ((int)$u['id'] === (int)$up['user_id']) ? 'selected' : ''; ?>>
                                            <?php echo html_escape($u['username']); ?>
                                        </option>
                                    <?php endforeach; ?>
                                </select>
                            </td>
                            <td>
                                <select name="plan_id">
                                    <?php foreach ($plans as $p): ?>
                                        <option value="<?php echo (int)$p['id']; ?>"
                                            <?php echo ((int)$p['id'] === (int)$up['plan_id']) ? 'selected' : ''; ?>>
                                            <?php echo html_escape($p['name']); ?>
                                        </option>
                                    <?php endforeach; ?>
                                </select>
                            </td>
                            <td class="small"><?php echo html_escape($up['started_at']); ?></td>
                            <td class="small"><?php echo html_escape($up['expires_at']); ?></td>
                            <td><input type="checkbox" name="is_active" <?php echo $up['is_active'] ? 'checked' : ''; ?>></td>
                            <td>
                                <button type="submit" name="action" value="update_user_plan" class="button secondary">Save</button>
                                <button type="submit" name="action" value="delete_user_plan" class="button danger"
                                        onclick="return confirm('Delete this user plan?');">Delete</button>
                            </td>
                        </form>
                    </tr>
                <?php endforeach; ?>
            </table>

        <?php elseif ($section === 'api_keys'): ?>
            <h1>API Keys</h1>

            <form method="post" class="form-inline">
                <input type="hidden" name="action" value="add_api_key">
                <input type="hidden" name="section" value="api_keys">
                <strong>Add API Key:</strong>
                <label>User
                    <select name="user_id">
                        <?php foreach ($users as $u): ?>
                            <option value="<?php echo (int)$u['id']; ?>"><?php echo html_escape($u['username']); ?></option>
                        <?php endforeach; ?>
                    </select>
                </label>
                <label>Description <input type="text" name="description"></label>
                <button type="submit" class="button">Generate</button>
            </form>

            <table>
                <tr>
                    <th>ID</th><th>User</th><th>API Key</th><th>Description</th><th>Active</th>
                    <th>Created</th><th>Last Used</th><th>Actions</th>
                </tr>
                <?php
                $sql = "SELECT ak.*, u.username
                        FROM api_keys ak
                        JOIN users u ON ak.user_id = u.id
                        ORDER BY ak.id ASC";
                $stmt = $pdo->query($sql);
                $api_keys = $stmt->fetchAll();
                ?>
                <?php foreach ($api_keys as $ak): ?>
                    <tr>
                        <form method="post">
                            <td><?php echo (int)$ak['id']; ?>
                                <input type="hidden" name="id" value="<?php echo (int)$ak['id']; ?>">
                                <input type="hidden" name="section" value="api_keys">
                            </td>
                            <td><?php echo html_escape($ak['username']); ?></td>
                            <td class="small">
                                <span class="tag"><?php echo html_escape($ak['api_key']); ?></span>
                            </td>
                            <td><input type="text" name="description" value="<?php echo html_escape($ak['description']); ?>"></td>
                            <td><input type="checkbox" name="is_active" <?php echo $ak['is_active'] ? 'checked' : ''; ?>></td>
                            <td class="small"><?php echo html_escape($ak['created_at']); ?></td>
                            <td class="small"><?php echo html_escape($ak['last_used_at']); ?></td>
                            <td>
                                <button type="submit" name="action" value="update_api_key" class="button secondary">Save</button>
                                <button type="submit" name="action" value="delete_api_key" class="button danger"
                                        onclick="return confirm('Delete this API key?');">Delete</button>
                            </td>
                        </form>
                    </tr>
                <?php endforeach; ?>
            </table>

        <?php elseif ($section === 'reports'): ?>
            <h1>Reports</h1>

            <h2>Usage by User</h2>
            <table>
                <tr>
                    <th>User</th><th>Total Requests</th>
                </tr>
                <?php foreach ($usage_by_user as $row): ?>
                    <tr>
                        <td><?php echo html_escape($row['username']); ?></td>
                        <td><?php echo (int)$row['total_requests']; ?></td>
                    </tr>
                <?php endforeach; ?>
            </table>

            <h2>Last 100 Usage Records</h2>
            <table>
                <tr>
                    <th>User</th><th>API Key</th><th>Hour Start</th><th>Requests</th>
                </tr>
                <?php foreach ($usage_last as $row): ?>
                    <tr>
                        <td><?php echo html_escape($row['username']); ?></td>
                        <td class="small"><span class="tag"><?php echo html_escape($row['api_key']); ?></span></td>
                        <td class="small"><?php echo html_escape($row['hour_start']); ?></td>
                        <td><?php echo (int)$row['request_count']; ?></td>
                    </tr>
                <?php endforeach; ?>
            </table>

        <?php elseif ($section === 'monitor'): ?>
            <h1>Monitoring</h1>

            <?php
            $hasAnyData =
                !empty($monitor_data['minutes']['labels']) ||
                !empty($monitor_data['hours']['labels'])   ||
                !empty($monitor_data['weeks']['labels'])   ||
                !empty($monitor_data['months']['labels']);
            ?>

            <?php if (!$hasAnyData): ?>
                <p>No monitoring data found yet. Make sure the Python script is running and writing
                    <code>log_minutes.jsonl</code>, <code>log_hours.jsonl</code>,
                    <code>log_weeks.jsonl</code> and <code>log_months.jsonl</code> in this folder.</p>
            <?php else: ?>

                <!-- CURRENT STATUS (GAUGES) -->
                <h2>Current server status (last minute)</h2>
                <div class="charts-grid">
                    <div class="chart-card">
                        <h3>CPU Load (%)</h3>
                        <canvas id="gaugeCpu"></canvas>
                    </div>
                    <div class="chart-card">
                        <h3>RAM Usage (%)</h3>
                        <canvas id="gaugeRam"></canvas>
                    </div>
                    <div class="chart-card">
                        <h3>GPU Load (%)</h3>
                        <canvas id="gaugeGpu"></canvas>
                    </div>
                    <div class="chart-card">
                        <h3>GPU VRAM Usage (%)</h3>
                        <canvas id="gaugeGpuMem"></canvas>
                    </div>
                    <div class="chart-card">
                        <h3>Disk Usage (%)</h3>
                        <canvas id="gaugeDisk"></canvas>
                    </div>
                </div>

                <div class="charts-grid">
                    <div class="chart-card">
                        <h3>Temperatures (current)</h3>
                        <p class="small">
                            GPU temperature:
                            <strong>
                                <?php
                                echo ($current_gpu_temp !== null)
                                    ? html_escape(number_format((float)$current_gpu_temp, 1)) . " °C"
                                    : "N/A";
                                ?>
                            </strong><br>
                            NVMe disk temperature:
                            <strong>
                                <?php
                                echo ($current_disk_temp !== null)
                                    ? html_escape(number_format((float)$current_disk_temp, 1)) . " °C"
                                    : "N/A";
                                ?>
                            </strong>
                        </p>
                    </div>
                </div>

                <!-- HISTORICAL CHARTS -->
                <h2>Historical metrics</h2>

                <h3>Last 60 minutes (per minute)</h3>
                <?php if (empty($monitor_data['minutes']['labels'])): ?>
                    <p class="small">No per-minute data yet.</p>
                <?php else: ?>
                    <div class="charts-grid">
                        <div class="chart-card">
                            <h4>CPU (%)</h4>
                            <canvas id="chartMinutesCpu"></canvas>
                        </div>
                        <div class="chart-card">
                            <h4>RAM (%)</h4>
                            <canvas id="chartMinutesRam"></canvas>
                        </div>
                        <div class="chart-card">
                            <h4>GPU (%)</h4>
                            <canvas id="chartMinutesGpu"></canvas>
                        </div>
                        <div class="chart-card">
                            <h4>GPU VRAM (%)</h4>
                            <canvas id="chartMinutesGpuMem"></canvas>
                        </div>
                        <div class="chart-card">
                            <h4>Disk (%)</h4>
                            <canvas id="chartMinutesDisk"></canvas>
                        </div>
                        <div class="chart-card">
                            <h4>GPU Temp (°C)</h4>
                            <canvas id="chartMinutesGpuTemp"></canvas>
                        </div>
                        <div class="chart-card">
                            <h4>Disk Temp (°C)</h4>
                            <canvas id="chartMinutesDiskTemp"></canvas>
                        </div>
                    </div>
                <?php endif; ?>

                <h3>Last 24 hours (per hour)</h3>
                <?php if (empty($monitor_data['hours']['labels'])): ?>
                    <p class="small">No hourly data yet.</p>
                <?php else: ?>
                    <div class="charts-grid">
                        <div class="chart-card">
                            <h4>CPU (%)</h4>
                            <canvas id="chartHoursCpu"></canvas>
                        </div>
                        <div class="chart-card">
                            <h4>RAM (%)</h4>
                            <canvas id="chartHoursRam"></canvas>
                        </div>
                        <div class="chart-card">
                            <h4>GPU (%)</h4>
                            <canvas id="chartHoursGpu"></canvas>
                        </div>
                        <div class="chart-card">
                            <h4>GPU VRAM (%)</h4>
                            <canvas id="chartHoursGpuMem"></canvas>
                        </div>
                        <div class="chart-card">
                            <h4>Disk (%)</h4>
                            <canvas id="chartHoursDisk"></canvas>
                        </div>
                        <div class="chart-card">
                            <h4>GPU Temp (°C)</h4>
                            <canvas id="chartHoursGpuTemp"></canvas>
                        </div>
                        <div class="chart-card">
                            <h4>Disk Temp (°C)</h4>
                            <canvas id="chartHoursDiskTemp"></canvas>
                        </div>
                    </div>
                <?php endif; ?>

                <h3>Last weeks (weekly averages)</h3>
                <?php if (empty($monitor_data['weeks']['labels'])): ?>
                    <p class="small">No weekly data yet.</p>
                <?php else: ?>
                    <div class="charts-grid">
                        <div class="chart-card">
                            <h4>CPU (%)</h4>
                            <canvas id="chartWeeksCpu"></canvas>
                        </div>
                        <div class="chart-card">
                            <h4>RAM (%)</h4>
                            <canvas id="chartWeeksRam"></canvas>
                        </div>
                        <div class="chart-card">
                            <h4>GPU (%)</h4>
                            <canvas id="chartWeeksGpu"></canvas>
                        </div>
                        <div class="chart-card">
                            <h4>GPU VRAM (%)</h4>
                            <canvas id="chartWeeksGpuMem"></canvas>
                        </div>
                        <div class="chart-card">
                            <h4>Disk (%)</h4>
                            <canvas id="chartWeeksDisk"></canvas>
                        </div>
                        <div class="chart-card">
                            <h4>GPU Temp (°C)</h4>
                            <canvas id="chartWeeksGpuTemp"></canvas>
                        </div>
                        <div class="chart-card">
                            <h4>Disk Temp (°C)</h4>
                            <canvas id="chartWeeksDiskTemp"></canvas>
                        </div>
                    </div>
                <?php endif; ?>

                <h3>Last months (monthly averages)</h3>
                <?php if (empty($monitor_data['months']['labels'])): ?>
                    <p class="small">No monthly data yet.</p>
                <?php else: ?>
                    <div class="charts-grid">
                        <div class="chart-card">
                            <h4>CPU (%)</h4>
                            <canvas id="chartMonthsCpu"></canvas>
                        </div>
                        <div class="chart-card">
                            <h4>RAM (%)</h4>
                            <canvas id="chartMonthsRam"></canvas>
                        </div>
                        <div class="chart-card">
                            <h4>GPU (%)</h4>
                            <canvas id="chartMonthsGpu"></canvas>
                        </div>
                        <div class="chart-card">
                            <h4>GPU VRAM (%)</h4>
                            <canvas id="chartMonthsGpuMem"></canvas>
                        </div>
                        <div class="chart-card">
                            <h4>Disk (%)</h4>
                            <canvas id="chartMonthsDisk"></canvas>
                        </div>
                        <div class="chart-card">
                            <h4>GPU Temp (°C)</h4>
                            <canvas id="chartMonthsGpuTemp"></canvas>
                        </div>
                        <div class="chart-card">
                            <h4>Disk Temp (°C)</h4>
                            <canvas id="chartMonthsDiskTemp"></canvas>
                        </div>
                    </div>
                <?php endif; ?>

                <script>
                    const monitor = <?php echo json_encode($monitor_data); ?>;
                    const currentState = {
                        cpu:     <?php echo json_encode($current_cpu); ?>,
                        ram:     <?php echo json_encode($current_ram); ?>,
                        gpu:     <?php echo json_encode($current_gpu); ?>,
                        gpu_mem: <?php echo json_encode($current_gpu_mem); ?>,
                        disk:    <?php echo json_encode($current_disk); ?>
                    };

                    function makeLineChart(canvasId, seriesLabel, labels, data, color, yLabel, suggestedMax) {
                        const element = document.getElementById(canvasId);
                        if (!element) return;
                        const ctx = element.getContext('2d');

                        new Chart(ctx, {
                            type: 'line',
                            data: {
                                labels: labels,
                                datasets: [{
                                    label: seriesLabel,
                                    data: data,
                                    fill: false,
                                    tension: 0.2,
                                    borderColor: color,
                                    pointRadius: 0
                                }]
                            },
                            options: {
                                responsive: true,
                                plugins: {
                                    legend: {
                                        display: true
                                    }
                                },
                                scales: {
                                    x: {
                                        display: true
                                    },
                                    y: {
                                        display: true,
                                        title: {
                                            display: true,
                                            text: yLabel
                                        },
                                        suggestedMin: 0,
                                        suggestedMax: suggestedMax
                                    }
                                }
                            }
                        });
                    }

                    // Simple semicircle gauge using a doughnut chart
                    function makeGaugeChart(canvasId, value, label, color) {
                        const element = document.getElementById(canvasId);
                        if (!element) return;
                        const ctx = element.getContext('2d');

                        const v = (typeof value === 'number') ? Math.max(0, Math.min(100, value)) : 0;

                        new Chart(ctx, {
                            type: 'doughnut',
                            data: {
                                labels: [label, ''],
                                datasets: [{
                                    data: [v, 100 - v],
                                    backgroundColor: [color, 'rgba(220,220,220,0.4)'],
                                    borderWidth: 0
                                }]
                            },
                            options: {
                                circumference: 180,
                                rotation: -90,
                                cutout: '70%',
                                plugins: {
                                    legend: { display: false },
                                    tooltip: {
                                        callbacks: {
                                            label: function () {
                                                return label + ': ' + v.toFixed(1) + '%';
                                            }
                                        }
                                    }
                                },
                                responsive: true
                            }
                        });
                    }

                    // Gauges (current state)
                    makeGaugeChart('gaugeCpu',     currentState.cpu,     'CPU',      'rgba(54, 162, 235, 1)');
                    makeGaugeChart('gaugeRam',     currentState.ram,     'RAM',      'rgba(75, 192, 192, 1)');
                    makeGaugeChart('gaugeGpu',     currentState.gpu,     'GPU',      'rgba(255, 99, 132, 1)');
                    makeGaugeChart('gaugeGpuMem',  currentState.gpu_mem, 'GPU VRAM', 'rgba(255, 159, 64, 1)');
                    makeGaugeChart('gaugeDisk',    currentState.disk,    'Disk',     'rgba(153, 102, 255, 1)');

                    // Helper to draw all charts for a given scale
                    function drawScaleCharts(scale, prefix, colorSet) {
                        const d = monitor[scale];
                        if (!d || !d.labels || d.labels.length === 0) return;

                        makeLineChart(prefix + 'Cpu',     'CPU %',      d.labels, d.cpu,      colorSet.cpu,     '%', 100);
                        makeLineChart(prefix + 'Ram',     'RAM %',      d.labels, d.ram,      colorSet.ram,     '%', 100);
                        makeLineChart(prefix + 'Gpu',     'GPU %',      d.labels, d.gpu,      colorSet.gpu,     '%', 100);
                        makeLineChart(prefix + 'GpuMem',  'GPU VRAM %', d.labels, d.gpu_mem,  colorSet.gpuMem,  '%', 100);
                        makeLineChart(prefix + 'Disk',    'Disk %',     d.labels, d.disk,     colorSet.disk,    '%', 100);
                        makeLineChart(prefix + 'GpuTemp', 'GPU °C',     d.labels, d.gpu_temp, colorSet.gpuTemp, '°C', 100);
                        makeLineChart(prefix + 'DiskTemp','Disk °C',    d.labels, d.disk_temp,colorSet.diskTemp,'°C', 100);
                    }

                    const colors = {
                        minutes: {
                            cpu:     'rgba(54, 162, 235, 1)',
                            ram:     'rgba(75, 192, 192, 1)',
                            gpu:     'rgba(255, 99, 132, 1)',
                            gpuMem:  'rgba(255, 159, 64, 1)',
                            disk:    'rgba(153, 102, 255, 1)',
                            gpuTemp: 'rgba(201, 203, 207, 1)',
                            diskTemp:'rgba(140, 86, 75, 1)'
                        },
                        hours: {
                            cpu:     'rgba(54, 162, 235, 1)',
                            ram:     'rgba(75, 192, 192, 1)',
                            gpu:     'rgba(255, 99, 132, 1)',
                            gpuMem:  'rgba(255, 159, 64, 1)',
                            disk:    'rgba(153, 102, 255, 1)',
                            gpuTemp: 'rgba(201, 203, 207, 1)',
                            diskTemp:'rgba(140, 86, 75, 1)'
                        },
                        weeks: {
                            cpu:     'rgba(54, 162, 235, 1)',
                            ram:     'rgba(75, 192, 192, 1)',
                            gpu:     'rgba(255, 99, 132, 1)',
                            gpuMem:  'rgba(255, 159, 64, 1)',
                            disk:    'rgba(153, 102, 255, 1)',
                            gpuTemp: 'rgba(201, 203, 207, 1)',
                            diskTemp:'rgba(140, 86, 75, 1)'
                        },
                        months: {
                            cpu:     'rgba(54, 162, 235, 1)',
                            ram:     'rgba(75, 192, 192, 1)',
                            gpu:     'rgba(255, 99, 132, 1)',
                            gpuMem:  'rgba(255, 159, 64, 1)',
                            disk:    'rgba(153, 102, 255, 1)',
                            gpuTemp: 'rgba(201, 203, 207, 1)',
                            diskTemp:'rgba(140, 86, 75, 1)'
                        }
                    };

                    // Draw all scales
                    drawScaleCharts('minutes', 'chartMinutes', colors.minutes);
                    drawScaleCharts('hours',   'chartHours',   colors.hours);
                    drawScaleCharts('weeks',   'chartWeeks',   colors.weeks);
                    drawScaleCharts('months',  'chartMonths',  colors.months);
                </script>
            <?php endif; ?>

        <?php else: ?>
            <h1>Unknown section</h1>
        <?php endif; ?>
    </div>
</div>
</body>
</html>

