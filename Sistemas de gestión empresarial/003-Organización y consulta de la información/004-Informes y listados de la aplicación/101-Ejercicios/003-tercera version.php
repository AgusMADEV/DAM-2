<?php
/**
 * Quiz en vivo tipo Kahoot (1 solo archivo PHP + JSON + polling 1s)
 *
 * Cambios pedidos:
 * 1) Si se accede a la URL “a pelo” (sin parámetros), asumimos ALUMNO.
 * 2) En presentador, el desplegable NO debe saltar a la primera pregunta al refrescar.
 *    - Se conserva la selección actual del desplegable.
 *    - Solo cambia la pregunta actual al pulsar “Establecer como actual”.
 * 3) Tema CSS CLARO.
 * 4) Toda la app en ESPAÑOL.
 *
 * Uso:
 *  Presentador: index.php?role=presenter&key=changeme
 *  Alumno:      index.php   (o index.php?role=student)
 *
 * Archivos:
 *  ./quiz_data/quiz.json
 *  ./quiz_data/results.json
 */

declare(strict_types=1);
ini_set('display_errors', '1');
error_reporting(E_ALL);

session_start();

/* =========================
   CONFIG
   ========================= */
$PRESENTER_KEY = 'changeme'; // <-- cambia esto

$DATA_DIR = __DIR__ . DIRECTORY_SEPARATOR . 'quiz_data';
$QUIZ_FILE = $DATA_DIR . DIRECTORY_SEPARATOR . 'quiz.json';
$RESULTS_FILE = $DATA_DIR . DIRECTORY_SEPARATOR . 'results.json';

if (!is_dir($DATA_DIR)) {
  @mkdir($DATA_DIR, 0775, true);
}

/* =========================
   FILE UTILS (atomic + flock)
   ========================= */
function read_json_file(string $path, array $default): array {
  if (!file_exists($path)) return $default;
  $raw = @file_get_contents($path);
  if ($raw === false || trim($raw) === '') return $default;
  $data = json_decode($raw, true);
  return is_array($data) ? $data : $default;
}

function write_json_file_atomic(string $path, array $data): void {
  $tmp = $path . '.tmp';
  $json = json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
  if ($json === false) $json = "{}";

  $fp = fopen($tmp, 'wb');
  if ($fp === false) return;
  fwrite($fp, $json);
  fflush($fp);
  fclose($fp);

  @rename($tmp, $path);
}

function with_lock(string $lockName, callable $fn) {
  $lockPath = sys_get_temp_dir() . DIRECTORY_SEPARATOR . $lockName . '.lock';
  $fp = fopen($lockPath, 'c+');
  if ($fp === false) return $fn();

  flock($fp, LOCK_EX);
  try {
    return $fn();
  } finally {
    flock($fp, LOCK_UN);
    fclose($fp);
  }
}

/* =========================
   DEFAULT DATA
   ========================= */
function default_quiz(): array {
  return [
    "version" => 2,
    "createdAt" => time(),
    "updatedAt" => time(),
    "status" => "idle",            // idle | open | closed
    "currentQuestionId" => null,
    "resultsPublished" => false,
    "questions" => []
  ];
}

function default_results(): array {
  return [
    "version" => 2,
    "createdAt" => time(),
    "updatedAt" => time(),
    "answers" => []
  ];
}

function get_quiz(string $path): array { return read_json_file($path, default_quiz()); }
function get_results(string $path): array { return read_json_file($path, default_results()); }
function save_quiz(string $path, array $quiz): void { $quiz["updatedAt"] = time(); write_json_file_atomic($path, $quiz); }
function save_results(string $path, array $results): void { $results["updatedAt"] = time(); write_json_file_atomic($path, $results); }

function find_question(array $quiz, ?string $qid): ?array {
  if (!$qid) return null;
  foreach ($quiz["questions"] as $q) {
    if (($q["id"] ?? null) === $qid) return $q;
  }
  return null;
}

function compute_students_table(array $quiz, array $results): array {
  $students = [];

  $correctMap = [];
  foreach (($quiz["questions"] ?? []) as $q) {
    if (isset($q["id"]) && array_key_exists("correctIndex", $q)) {
      $correctMap[$q["id"]] = (int)$q["correctIndex"];
    }
  }

  foreach (($results["answers"] ?? []) as $qid => $byStudent) {
    if (!is_array($byStudent)) continue;
    foreach ($byStudent as $sid => $ans) {
      if (!is_array($ans)) continue;
      $name = (string)($ans["studentName"] ?? $sid);

      if (!isset($students[$sid])) {
        $students[$sid] = ["studentId"=>$sid, "studentName"=>$name, "points"=>0, "answered"=>0, "avg"=>0.0];
      } else {
        if ($name !== '') $students[$sid]["studentName"] = $name;
      }

      $students[$sid]["answered"]++;

      $oi = (int)($ans["optionIndex"] ?? -1);
      if (isset($correctMap[$qid]) && $oi === (int)$correctMap[$qid]) {
        $students[$sid]["points"]++;
      }
    }
  }

  foreach ($students as &$s) {
    $s["avg"] = ($s["answered"] > 0) ? ($s["points"] / $s["answered"]) : 0.0;
  }
  unset($s);

  usort($students, function($a, $b){
    if ($a["points"] !== $b["points"]) return $b["points"] <=> $a["points"];
    return strcmp((string)$a["studentName"], (string)$b["studentName"]);
  });

  return $students;
}

/* =========================
   ROLE RESOLUTION
   ========================= */
/**
 * Requisito (1): Si se accede a la URL sin parámetros, asumimos alumno.
 * Esto evita quedarse “pegado” como presentador por sesión.
 */
if (empty($_GET)) {
  $_SESSION['role'] = 'student';
}

$role = $_GET['role'] ?? ($_SESSION['role'] ?? 'student');
$role = ($role === 'presenter') ? 'presenter' : 'student';
$_SESSION['role'] = $role;

/* =========================
   AUTH / IDENTITIES
   ========================= */
if ($role === 'presenter') {
  $key = (string)($_GET['key'] ?? '');
  if (!hash_equals($PRESENTER_KEY, $key)) {
    http_response_code(403);
    header('Content-Type: text/plain; charset=utf-8');
    echo "Acceso denegado (clave de presentador incorrecta).\n";
    echo "Usa: ?role=presenter&key=TUCLAVE\n";
    exit;
  }
}

$studentId = null;
$studentName = null;

if ($role === 'student') {
  if (empty($_SESSION['studentId'])) {
    $_SESSION['studentId'] = 's_' . bin2hex(random_bytes(6));
  }
  $studentId = (string)$_SESSION['studentId'];

  if (isset($_POST['studentName']) && is_string($_POST['studentName'])) {
    $_SESSION['studentName'] = trim($_POST['studentName']);
  }
  if (empty($_SESSION['studentName'])) {
    $_SESSION['studentName'] = 'Alumno-' . substr($studentId, -4);
  }
  $studentName = (string)$_SESSION['studentName'];
}

/* =========================
   API ROUTER
   ========================= */
$api = $_GET['api'] ?? null;
if ($api !== null) {
  header('Content-Type: application/json; charset=utf-8');

  $respond = function(array $payload, int $code = 200) {
    http_response_code($code);
    echo json_encode($payload, JSON_UNESCAPED_UNICODE);
    exit;
  };

  if ($role !== 'presenter' && in_array($api, ['create_question','set_current','open','close','reset','publish'], true)) {
    $respond(["ok" => false, "error" => "Solo presentador"], 403);
  }

  if ($api === 'state') {
    $quiz = get_quiz($QUIZ_FILE);
    $results = get_results($RESULTS_FILE);

    $current = find_question($quiz, $quiz["currentQuestionId"] ?? null);

    $counts = [];
    $percentages = [];
    $totalAnswers = 0;

    if ($current) {
      $qid = (string)$current["id"];
      $opts = $current["options"] ?? [];
      $counts = array_fill(0, count($opts), 0);

      $answers = $results["answers"][$qid] ?? [];
      if (is_array($answers)) {
        foreach ($answers as $ans) {
          $oi = (int)($ans["optionIndex"] ?? -1);
          if ($oi >= 0 && $oi < count($counts)) $counts[$oi]++;
        }
      }

      $totalAnswers = array_sum($counts);
      $percentages = array_map(function($c) use ($totalAnswers){
        return $totalAnswers > 0 ? round(($c / $totalAnswers) * 100, 1) : 0.0;
      }, $counts);
    }

    $student = null;
    if ($role === 'student') {
      $points = 0;
      $answered = 0;

      $correctMap = [];
      foreach (($quiz["questions"] ?? []) as $q) {
        if (isset($q["id"]) && array_key_exists("correctIndex", $q)) {
          $correctMap[$q["id"]] = (int)$q["correctIndex"];
        }
      }

      foreach (($results["answers"] ?? []) as $qid => $byStudent) {
        if (!is_array($byStudent)) continue;
        if (!isset($byStudent[$studentId])) continue;
        $answered++;
        $oi = (int)($byStudent[$studentId]["optionIndex"] ?? -1);
        if (isset($correctMap[$qid]) && $oi === (int)$correctMap[$qid]) $points++;
      }

      $avg = ($answered > 0) ? round($points / $answered, 3) : 0.0;

      $hasAnswered = false;
      $myOptionIndex = null;
      $isCorrect = null;

      if ($current) {
        $qid = (string)$current["id"];
        if (isset($results["answers"][$qid][$studentId])) {
          $hasAnswered = true;
          $myOptionIndex = (int)($results["answers"][$qid][$studentId]["optionIndex"] ?? -1);
        }

        if ($hasAnswered && ($quiz["resultsPublished"] ?? false) === true) {
          $ci = (int)($current["correctIndex"] ?? -1);
          $isCorrect = ($myOptionIndex === $ci);
        }
      }

      $student = [
        "studentId" => $studentId,
        "studentName" => $studentName,
        "score" => ["points"=>$points, "answered"=>$answered, "avg"=>$avg],
        "current" => ["hasAnswered"=>$hasAnswered, "myOptionIndex"=>$myOptionIndex, "isCorrect"=>$isCorrect]
      ];
    }

    $safeCurrent = $current;
    if ($role === 'student' && $safeCurrent) {
      if (($quiz["resultsPublished"] ?? false) !== true) {
        unset($safeCurrent["correctIndex"]);
      }
    }

    $presenter = null;
    if ($role === 'presenter') {
      $presenter = [
        "questions" => $quiz["questions"],
        "students" => compute_students_table($quiz, $results)
      ];
    }

    $respond([
      "ok" => true,
      "serverTime" => time(),
      "quiz" => [
        "status" => $quiz["status"],
        "currentQuestionId" => $quiz["currentQuestionId"],
        "resultsPublished" => (bool)($quiz["resultsPublished"] ?? false),
        "updatedAt" => $quiz["updatedAt"],
        "questionsCount" => count($quiz["questions"]),
      ],
      "currentQuestion" => $safeCurrent,
      "counts" => $counts,
      "percentages" => $percentages,
      "totalAnswers" => $totalAnswers,
      "student" => $student,
      "presenter" => $presenter
    ]);
  }

  if ($api === 'create_question') {
    $text = trim((string)($_POST['text'] ?? ''));
    $optionsRaw = $_POST['options'] ?? [];
    $correctIndex = (int)($_POST['correctIndex'] ?? 0);

    if ($text === '') $respond(["ok" => false, "error" => "La pregunta es obligatoria"], 400);
    if (!is_array($optionsRaw)) $respond(["ok" => false, "error" => "Opciones inválidas"], 400);

    $options = [];
    foreach ($optionsRaw as $o) {
      $o = trim((string)$o);
      if ($o !== '') $options[] = $o;
    }
    if (count($options) < 2) $respond(["ok" => false, "error" => "Mínimo 2 opciones no vacías"], 400);
    if ($correctIndex < 0 || $correctIndex >= count($options)) $correctIndex = 0;

    $qid = 'q_' . bin2hex(random_bytes(6));
    $q = [
      "id" => $qid,
      "text" => $text,
      "options" => $options,
      "correctIndex" => $correctIndex,
      "createdAt" => time(),
    ];

    with_lock('quiz_es_quiz', function() use ($QUIZ_FILE, $q) {
      $quiz = get_quiz($QUIZ_FILE);
      $quiz["questions"][] = $q;

      if (empty($quiz["currentQuestionId"])) {
        $quiz["currentQuestionId"] = $q["id"];
        $quiz["status"] = "closed";
      }
      $quiz["resultsPublished"] = false;
      save_quiz($QUIZ_FILE, $quiz);
    });

    $respond(["ok" => true, "questionId" => $qid]);
  }

  if ($api === 'set_current') {
    $qid = (string)($_POST['questionId'] ?? '');
    if ($qid === '') $respond(["ok" => false, "error" => "Falta questionId"], 400);

    with_lock('quiz_es_quiz', function() use ($QUIZ_FILE, $RESULTS_FILE, $qid) {
      $quiz = get_quiz($QUIZ_FILE);

      $exists = false;
      foreach ($quiz["questions"] as $q) {
        if (($q["id"] ?? '') === $qid) { $exists = true; break; }
      }
      if (!$exists) return;

      $quiz["currentQuestionId"] = $qid;
      $quiz["status"] = "closed";
      $quiz["resultsPublished"] = false;
      save_quiz($QUIZ_FILE, $quiz);

      $results = get_results($RESULTS_FILE);
      if (!isset($results["answers"][$qid])) $results["answers"][$qid] = [];
      save_results($RESULTS_FILE, $results);
    });

    $respond(["ok" => true]);
  }

  if ($api === 'open') {
    with_lock('quiz_es_quiz', function() use ($QUIZ_FILE) {
      $quiz = get_quiz($QUIZ_FILE);
      if (!empty($quiz["currentQuestionId"])) {
        $quiz["status"] = "open";
        $quiz["resultsPublished"] = false;
        save_quiz($QUIZ_FILE, $quiz);
      }
    });
    $respond(["ok" => true]);
  }

  if ($api === 'close') {
    with_lock('quiz_es_quiz', function() use ($QUIZ_FILE) {
      $quiz = get_quiz($QUIZ_FILE);
      if (!empty($quiz["currentQuestionId"])) {
        $quiz["status"] = "closed";
        save_quiz($QUIZ_FILE, $quiz);
      }
    });
    $respond(["ok" => true]);
  }

  if ($api === 'publish') {
    with_lock('quiz_es_quiz', function() use ($QUIZ_FILE) {
      $quiz = get_quiz($QUIZ_FILE);
      if (!empty($quiz["currentQuestionId"])) {
        $quiz["resultsPublished"] = true;
        if (($quiz["status"] ?? '') === 'open') $quiz["status"] = 'closed';
        save_quiz($QUIZ_FILE, $quiz);
      }
    });
    $respond(["ok" => true]);
  }

  if ($api === 'reset') {
    with_lock('quiz_es_quiz', function() use ($QUIZ_FILE, $RESULTS_FILE) {
      save_quiz($QUIZ_FILE, default_quiz());
      save_results($RESULTS_FILE, default_results());
    });
    $respond(["ok" => true]);
  }

  if ($api === 'answer') {
    if ($role !== 'student') $respond(["ok" => false, "error" => "Solo alumno"], 403);

    $qid = (string)($_POST['questionId'] ?? '');
    $optionIndex = (int)($_POST['optionIndex'] ?? -1);
    if ($qid === '' || $optionIndex < 0) $respond(["ok" => false, "error" => "Datos inválidos"], 400);

    $quiz = get_quiz($QUIZ_FILE);
    if (($quiz["status"] ?? 'idle') !== 'open') $respond(["ok" => false, "error" => "La pregunta no está abierta"], 409);
    if (($quiz["currentQuestionId"] ?? null) !== $qid) $respond(["ok" => false, "error" => "No es la pregunta actual"], 409);

    $current = find_question($quiz, $qid);
    if (!$current) $respond(["ok" => false, "error" => "Pregunta no encontrada"], 404);

    $optsCount = count($current["options"] ?? []);
    if ($optionIndex < 0 || $optionIndex >= $optsCount) $respond(["ok" => false, "error" => "Opción fuera de rango"], 400);

    with_lock('quiz_es_results', function() use ($RESULTS_FILE, $qid, $studentId, $studentName, $optionIndex) {
      $results = get_results($RESULTS_FILE);
      if (!isset($results["answers"][$qid]) || !is_array($results["answers"][$qid])) {
        $results["answers"][$qid] = [];
      }
      if (isset($results["answers"][$qid][$studentId])) return; // 1 voto por pregunta

      $results["answers"][$qid][$studentId] = [
        "studentName" => $studentName,
        "optionIndex" => $optionIndex,
        "ts" => time()
      ];
      save_results($RESULTS_FILE, $results);
    });

    $respond(["ok" => true]);
  }

  $respond(["ok" => false, "error" => "API desconocida"], 404);
}

/* =========================
   HTML
   ========================= */
?>
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Quiz en vivo</title>
  <style>
    :root{
      --bg:#f6f7fb;
      --card:#ffffff;
      --muted:#5b6477;
      --text:#141824;
      --stroke:rgba(20,24,36,.10);
      --shadow:0 14px 38px rgba(20,24,36,.10);
      --accent:#2563eb;
      --accent2:#06b6d4;
      --good:#16a34a;
      --bad:#dc2626;
      --warn:#d97706;
    }
    *{box-sizing:border-box}
    html,body{height:100%}
    body{
      margin:0;
      font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
      color:var(--text);
      background:
        radial-gradient(900px 500px at 10% 0%, rgba(37,99,235,.10), transparent 55%),
        radial-gradient(900px 500px at 90% 10%, rgba(6,182,212,.10), transparent 55%),
        var(--bg);
    }
    .wrap{max-width:1200px;margin:0 auto;padding:18px}
    .topbar{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
    h1{margin:0;font-size:16px;letter-spacing:.2px}
    .kpis{display:flex;gap:10px;flex-wrap:wrap}
    .pill{
      padding:7px 10px;border-radius:999px;
      background:rgba(255,255,255,.80);
      border:1px solid var(--stroke);
      color:var(--muted);
      font-size:12px;
      box-shadow:0 6px 14px rgba(20,24,36,.06);
    }
    .pill.good{border-color:rgba(22,163,74,.25);color:var(--good);background:rgba(22,163,74,.06)}
    .pill.bad{border-color:rgba(220,38,38,.25);color:var(--bad);background:rgba(220,38,38,.06)}
    .pill.warn{border-color:rgba(217,119,6,.25);color:var(--warn);background:rgba(217,119,6,.06)}
    .grid{display:grid;grid-template-columns:1fr;gap:14px;margin-top:14px}
    @media(min-width:980px){.grid.presentador{grid-template-columns:1.05fr .95fr}}
    .card{
      background:var(--card);
      border:1px solid var(--stroke);
      border-radius:18px;
      padding:16px;
      box-shadow:var(--shadow);
    }
    h2{margin:0 0 10px 0;font-size:13px;color:var(--muted);font-weight:800;text-transform:uppercase;letter-spacing:.08em}
    label{display:block;font-size:12px;color:var(--muted);margin:10px 0 6px}
    input[type="text"], textarea, select{
      width:100%;padding:10px 12px;border-radius:12px;
      border:1px solid var(--stroke);
      background:#fbfcff;
      color:var(--text);
      outline:none;
    }
    textarea{min-height:72px;resize:vertical}
    .row{display:flex;gap:10px;flex-wrap:wrap}
    .row>*{flex:1;min-width:200px}
    button{
      border:0;border-radius:12px;padding:10px 12px;
      cursor:pointer;font-weight:900;color:#ffffff;
      background:linear-gradient(135deg,var(--accent),var(--accent2));
    }
    button.secondary{
      background:#eef2ff;
      color:#1f2937;
      border:1px solid var(--stroke);
      font-weight:800;
    }
    button.ok{background:linear-gradient(135deg,#16a34a,#22c55e)}
    button.danger{background:linear-gradient(135deg,#dc2626,#f87171)}
    button.warn{background:linear-gradient(135deg,#d97706,#f59e0b)}
    button:disabled{opacity:.55;cursor:not-allowed}
    .muted{color:var(--muted);font-size:12px;line-height:1.45}
    .qtext{font-size:18px;font-weight:950;margin:0 0 12px 0}
    .hr{height:1px;background:rgba(20,24,36,.08);margin:14px 0}
    .options{display:grid;grid-template-columns:1fr;gap:10px}
    @media(min-width:720px){.options{grid-template-columns:1fr 1fr}}
    .optBtn{
      text-align:left;padding:14px;border-radius:14px;
      background:#ffffff;color:var(--text);
      border:1px solid rgba(20,24,36,.10);
      font-weight:900;
      transition:transform .06s ease, border-color .12s ease, background .12s ease;
    }
    .optBtn:hover{transform:translateY(-1px);border-color:rgba(37,99,235,.30);background:rgba(37,99,235,.04)}
    .optMeta{display:flex;justify-content:space-between;gap:12px;font-size:12px;color:var(--muted);margin-top:6px}
    .bar{height:10px;border-radius:999px;background:rgba(20,24,36,.08);overflow:hidden;border:1px solid rgba(20,24,36,.08)}
    .bar > div{height:100%;background:linear-gradient(135deg,var(--accent),var(--accent2));width:0%;transition:width 160ms linear}
    .feedback{
      padding:10px 12px;border-radius:14px;
      border:1px solid var(--stroke);
      background:#fbfcff;
      margin-top:12px;
    }
    .feedback.good{border-color:rgba(22,163,74,.25);background:rgba(22,163,74,.06)}
    .feedback.bad{border-color:rgba(220,38,38,.25);background:rgba(220,38,38,.06)}
    table{width:100%;border-collapse:collapse;font-size:12px}
    th,td{padding:10px 8px;border-bottom:1px solid rgba(20,24,36,.08);text-align:left}
    th{color:#334155;font-size:11px;text-transform:uppercase;letter-spacing:.07em}
    .right{text-align:right}
    .mono{font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace}
  </style>
</head>
<body>
<div class="wrap">
  <div class="topbar">
    <h1>Quiz en vivo</h1>
    <div class="kpis">
      <span class="pill" id="statusPill">estado: …</span>
      <span class="pill" id="qidPill">pregunta: …</span>
      <span class="pill" id="pubPill">publicado: …</span>
      <span class="pill" id="updatedPill">actualizado: …</span>
      <?php if ($role === 'student'): ?>
        <span class="pill">tú: <?= htmlspecialchars($_SESSION['studentName'] ?? 'alumno', ENT_QUOTES, 'UTF-8') ?></span>
      <?php else: ?>
        <span class="pill">rol: presentador</span>
      <?php endif; ?>
    </div>
  </div>

<?php if ($role === 'presenter'): ?>
  <div class="grid presentador">
    <div class="card">
      <h2>Crear pregunta</h2>

      <label>Pregunta</label>
      <textarea id="qText" placeholder="Escribe la pregunta…"></textarea>

      <div class="row">
        <div><label>Opción A</label><input id="opt0" type="text" placeholder="Opción A" /></div>
        <div><label>Opción B</label><input id="opt1" type="text" placeholder="Opción B" /></div>
      </div>

      <div class="row">
        <div><label>Opción C</label><input id="opt2" type="text" placeholder="Opción C (opcional)" /></div>
        <div><label>Opción D</label><input id="opt3" type="text" placeholder="Opción D (opcional)" /></div>
      </div>

      <label>Respuesta correcta</label>
      <select id="correctIndex">
        <option value="0">A</option>
        <option value="1">B</option>
        <option value="2">C</option>
        <option value="3">D</option>
      </select>

      <div class="row" style="margin-top:12px;">
        <button id="createBtn">Crear</button>
        <button class="secondary" id="refreshBtn">Refrescar</button>
      </div>

      <div class="hr"></div>

      <h2>Control</h2>
      <div class="row">
        <button class="ok" id="openBtn">Abrir respuestas</button>
        <button class="secondary" id="closeBtn">Cerrar</button>
        <button class="warn" id="publishBtn">Publicar resultados</button>
        <button class="danger" id="resetBtn">Reiniciar</button>
      </div>

      <label style="margin-top:12px;">Seleccionar pregunta (solo cambia al pulsar “Establecer”)</label>
      <select id="questionPicker"></select>
      <div class="row" style="margin-top:10px;">
        <button class="secondary" id="setCurrentBtn">Establecer como actual</button>
      </div>

      <p class="muted" id="presenterMsg" style="margin-top:10px;"></p>
    </div>

    <div class="card">
      <h2>Vista en vivo</h2>
      <p class="qtext" id="liveQuestion">Esperando…</p>
      <div id="liveOptions" class="muted"></div>

      <div class="hr"></div>

      <h2>Recuentos actuales</h2>
      <div id="countsBox" class="muted">Sin datos.</div>

      <div class="hr"></div>

      <h2>Alumnos y evaluación</h2>
      <div class="muted" id="studentsBox">Aún no hay alumnos.</div>
    </div>
  </div>

<?php else: ?>
  <div class="grid">
    <div class="card">
      <h2>Alumno</h2>

      <form method="post" style="margin-bottom:12px;">
        <label>Tu nombre (se guarda en la sesión)</label>
        <div class="row">
          <input type="text" name="studentName" value="<?= htmlspecialchars($_SESSION['studentName'] ?? '', ENT_QUOTES, 'UTF-8') ?>" />
          <button class="secondary" type="submit">Guardar</button>
        </div>
      </form>

      <div class="row">
        <div class="pill" id="scorePill">puntuación: …</div>
        <div class="pill" id="avgPill">media: …</div>
      </div>

      <div class="hr"></div>

      <p class="qtext" id="studentQuestion">Esperando al presentador…</p>
      <div class="options" id="studentOptions"></div>

      <div id="studentFeedback" class="feedback" style="display:none;"></div>

      <div class="hr"></div>

      <h2>Porcentajes en vivo</h2>
      <div id="studentPercents" class="muted">Sin datos.</div>

      <p class="muted" id="studentMsg" style="margin-top:10px;"></p>
    </div>
  </div>
<?php endif; ?>
</div>

<script>
  const ROLE = <?= json_encode($role) ?>;

  function $(id){ return document.getElementById(id); }

  async function apiPost(api, bodyObj) {
    const form = new FormData();
    for (const k of Object.keys(bodyObj || {})) {
      const v = bodyObj[k];
      if (Array.isArray(v)) {
        for (const item of v) form.append(k + "[]", item);
      } else {
        form.append(k, v);
      }
    }
    const res = await fetch(`?api=${encodeURIComponent(api)}&role=${encodeURIComponent(ROLE)}<?= ($role === 'presenter') ? '&key=' . urlencode($_GET['key'] ?? '') : '' ?>`, {
      method: 'POST',
      body: form
    });
    return await res.json();
  }

  async function apiGetState() {
    const res = await fetch(`?api=state&role=${encodeURIComponent(ROLE)}<?= ($role === 'presenter') ? '&key=' . urlencode($_GET['key'] ?? '') : '' ?>`);
    return await res.json();
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({
      "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"
    }[c]));
  }

  function setTopPills(state) {
    $("statusPill").textContent = `estado: ${state.quiz?.status ?? "?"}`;
    $("qidPill").textContent = `pregunta: ${state.quiz?.currentQuestionId ?? "ninguna"}`;
    $("pubPill").textContent = `publicado: ${state.quiz?.resultsPublished ? "sí" : "no"}`;
    $("updatedPill").textContent = `actualizado: ${state.quiz?.updatedAt ? new Date(state.quiz.updatedAt*1000).toLocaleTimeString() : "?"}`;
  }

  // ===== Presentador =====
  let pickerInitialized = false;

  function presenterRender(state) {
    const q = state.currentQuestion;
    const counts = state.counts || [];
    const perc = state.percentages || [];
    const total = state.totalAnswers || 0;

    $("liveQuestion").textContent = q ? q.text : "No hay pregunta actual.";

    const optsWrap = $("liveOptions");
    optsWrap.innerHTML = "";

    if (q && q.options && q.options.length) {
      optsWrap.innerHTML = q.options.map((t, i) => {
        const isCorrect = (typeof q.correctIndex === "number" && i === q.correctIndex);
        return `<div style="margin:10px 0;">
          <div><strong>${String.fromCharCode(65+i)}.</strong> ${escapeHtml(t)} ${isCorrect ? '<span class="pill good" style="margin-left:8px;">correcta</span>' : ''}</div>
        </div>`;
      }).join("");
    } else {
      optsWrap.textContent = "Crea una pregunta para empezar.";
    }

    const countsBox = $("countsBox");
    if (q && q.options && q.options.length) {
      countsBox.innerHTML = q.options.map((t, i) => {
        const c = counts[i] ?? 0;
        const p = perc[i] ?? 0;
        return `
          <div style="margin:12px 0;">
            <div style="display:flex;justify-content:space-between;gap:12px;">
              <div><strong>${String.fromCharCode(65+i)}.</strong> ${escapeHtml(t)}</div>
              <div class="mono"><strong>${c}</strong> (${p}%)</div>
            </div>
            <div class="bar"><div style="width:${p}%;"></div></div>
          </div>
        `;
      }).join("") + `<div class="muted">Total respuestas: <strong>${total}</strong></div>`;
    } else {
      countsBox.textContent = "Sin datos.";
    }

    // (2) Desplegable: NO saltar a la primera opción
    const picker = $("questionPicker");
    const qs = state.presenter?.questions || [];
    if (picker) {
      const prevValue = picker.value || ""; // conservar selección actual del usuario

      const optionsHtml = qs.map(qx => {
        const label = (qx.text || "").slice(0, 60);
        return `<option value="${escapeHtml(qx.id)}">${escapeHtml(qx.id)} — ${escapeHtml(label)}</option>`;
      }).join("");

      picker.innerHTML = optionsHtml || `<option value="">(aún no hay preguntas)</option>`;

      // Al primer render, si no hay selección previa, selecciona la pregunta actual
      if (!pickerInitialized) {
        if (state.quiz?.currentQuestionId) picker.value = state.quiz.currentQuestionId;
        pickerInitialized = true;
      } else {
        // En renders sucesivos: intenta restaurar la selección previa; si ya no existe, usa la actual del quiz
        if (prevValue && [...picker.options].some(o => o.value === prevValue)) {
          picker.value = prevValue;
        } else if (state.quiz?.currentQuestionId) {
          picker.value = state.quiz.currentQuestionId;
        }
      }
    }

    const studentsBox = $("studentsBox");
    const students = state.presenter?.students || [];
    if (!students.length) {
      studentsBox.textContent = "Aún no hay alumnos.";
    } else {
      studentsBox.innerHTML = `
        <table>
          <thead>
            <tr>
              <th>Alumno</th>
              <th class="right">Puntos</th>
              <th class="right">Respondidas</th>
              <th class="right">Media</th>
            </tr>
          </thead>
          <tbody>
            ${students.map(s => `
              <tr>
                <td>${escapeHtml(s.studentName)} <span class="muted mono">(${escapeHtml(s.studentId)})</span></td>
                <td class="right mono"><strong>${s.points}</strong></td>
                <td class="right mono">${s.answered}</td>
                <td class="right mono">${(Math.round(s.avg*1000)/1000).toFixed(3)}</td>
              </tr>
            `).join("")}
          </tbody>
        </table>
        <div class="muted" style="margin-top:8px;">Media = puntos / respondidas (cada pregunta vale 1 punto).</div>
      `;
    }
  }

  // ===== Alumno =====
  let answeredLocal = {};

  function studentRender(state) {
    const q = state.currentQuestion;
    const status = state.quiz?.status;
    const published = !!state.quiz?.resultsPublished;

    const qEl = $("studentQuestion");
    const optsEl = $("studentOptions");
    const msgEl = $("studentMsg");

    const score = state.student?.score;
    if (score) {
      $("scorePill").textContent = `puntuación: ${score.points}/${score.answered}`;
      $("avgPill").textContent = `media: ${score.avg}`;
    }

    optsEl.innerHTML = "";
    msgEl.textContent = "";

    if (!q) {
      qEl.textContent = "Esperando al presentador…";
      $("studentPercents").textContent = "Sin datos.";
      hideFeedback();
      return;
    }

    qEl.textContent = q.text;

    renderStudentPercents(state);

    const already = answeredLocal[q.id] || state.student?.current?.hasAnswered;
    const canAnswer = (status === "open") && !already;

    (q.options || []).forEach((t, i) => {
      const b = document.createElement("button");
      b.className = "optBtn";
      b.innerHTML = `<div><strong>${String.fromCharCode(65+i)}.</strong> ${escapeHtml(t)}</div>
                     <div class="optMeta"><span>En vivo</span><span class="mono">${(state.percentages?.[i] ?? 0)}%</span></div>
                     <div class="bar"><div style="width:${(state.percentages?.[i] ?? 0)}%;"></div></div>`;
      b.disabled = !canAnswer;

      b.addEventListener("click", async () => {
        b.disabled = true;
        const res = await apiPost("answer", { questionId: q.id, optionIndex: i });
        if (res.ok) {
          answeredLocal[q.id] = true;
          msgEl.textContent = "Respuesta registrada.";
        } else {
          msgEl.textContent = "No se pudo enviar: " + (res.error || "error");
          b.disabled = false;
        }
      });

      optsEl.appendChild(b);
    });

    if (already) {
      msgEl.textContent = "Ya has respondido esta pregunta.";
    } else if (status !== "open") {
      msgEl.textContent = "La pregunta no está abierta (o ya está cerrada).";
    }

    if (published && state.student?.current?.hasAnswered && typeof state.student.current.isCorrect === "boolean") {
      if (state.student.current.isCorrect) showFeedback(true, "Correcto ✅ (+1 punto)");
      else showFeedback(false, "Incorrecto ❌ (0 puntos)");
    } else {
      hideFeedback();
    }
  }

  function renderStudentPercents(state) {
    const q = state.currentQuestion;
    const percBox = $("studentPercents");
    if (!q || !q.options || !q.options.length) {
      percBox.textContent = "Sin datos.";
      return;
    }
    const perc = state.percentages || [];
    const counts = state.counts || [];
    const total = state.totalAnswers || 0;

    percBox.innerHTML = q.options.map((t, i) => {
      const p = perc[i] ?? 0;
      const c = counts[i] ?? 0;
      return `
        <div style="margin:12px 0;">
          <div style="display:flex;justify-content:space-between;gap:12px;">
            <div><strong>${String.fromCharCode(65+i)}.</strong> ${escapeHtml(t)}</div>
            <div class="mono"><strong>${p}%</strong> (${c})</div>
          </div>
          <div class="bar"><div style="width:${p}%;"></div></div>
        </div>
      `;
    }).join("") + `<div class="muted">Total de respuestas hasta ahora: <strong>${total}</strong></div>`;
  }

  function showFeedback(ok, text) {
    const box = $("studentFeedback");
    box.style.display = "block";
    box.className = "feedback " + (ok ? "good" : "bad");
    box.innerHTML = `<strong>${ok ? "ACIERTO" : "FALLO"}</strong> — ${escapeHtml(text)}`;
  }
  function hideFeedback() {
    const box = $("studentFeedback");
    box.style.display = "none";
    box.className = "feedback";
    box.textContent = "";
  }

  // ===== Heartbeat =====
  async function tick() {
    try {
      const state = await apiGetState();
      if (!state || !state.ok) return;
      setTopPills(state);

      if (ROLE === "presenter") presenterRender(state);
      else studentRender(state);
    } catch (e) {}
  }

  // ===== Acciones presentador =====
  if (ROLE === "presenter") {
    $("createBtn").addEventListener("click", async () => {
      const text = $("qText").value.trim();
      const options = [
        $("opt0").value.trim(),
        $("opt1").value.trim(),
        $("opt2").value.trim(),
        $("opt3").value.trim(),
      ];
      const correctIndex = parseInt($("correctIndex").value, 10) || 0;

      const res = await apiPost("create_question", { text, options, correctIndex });
      $("presenterMsg").textContent = res.ok
        ? `Pregunta creada: ${res.questionId}`
        : `Error: ${res.error || "desconocido"}`;

      if (res.ok) {
        $("qText").value = "";
        $("opt0").value = "";
        $("opt1").value = "";
        $("opt2").value = "";
        $("opt3").value = "";
      }
      await tick();
    });

    $("openBtn").addEventListener("click", async () => { await apiPost("open", {}); await tick(); });
    $("closeBtn").addEventListener("click", async () => { await apiPost("close", {}); await tick(); });

    $("publishBtn").addEventListener("click", async () => {
      await apiPost("publish", {});
      $("presenterMsg").textContent = "Resultados publicados para la pregunta actual.";
      await tick();
    });

    $("resetBtn").addEventListener("click", async () => {
      if (!confirm("¿Reiniciar el quiz y TODAS las respuestas?")) return;
      await apiPost("reset", {});
      $("presenterMsg").textContent = "Reinicio realizado.";
      pickerInitialized = false;
      await tick();
    });

    $("refreshBtn").addEventListener("click", tick);

    // (2) Solo cambia la pregunta al pulsar “Establecer como actual”
    $("setCurrentBtn").addEventListener("click", async () => {
      const picker = $("questionPicker");
      const qid = picker?.value || "";
      if (!qid) return;
      await apiPost("set_current", { questionId: qid });
      $("presenterMsg").textContent = `Pregunta actual establecida: ${qid}`;
      await tick();
    });
  }

  tick();
  setInterval(tick, 1000);
</script>
</body>
</html>

