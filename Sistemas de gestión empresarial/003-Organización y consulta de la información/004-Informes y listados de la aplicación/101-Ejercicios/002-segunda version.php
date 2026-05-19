<?php
/**
 * Single-file Kahoot-like live quiz (PHP + JSON + 1s polling)
 *
 * NEW in this version:
 * 1) Presenter button: "Publish results" (reveals correct + feedback to students)
 * 2) Student gets green/red feedback after publish (correct/incorrect)
 * 3) Clear, consistent theme (clean dark)
 * 4) Student sees live percentages per option (based on total answers so far)
 * 5) Student sees score so far (avg = points/answered; each question = 1 point)
 * 6) Presenter sees a grid/table of students and evaluations
 *
 * Usage:
 *  Presenter: index.php?role=presenter&key=changeme
 *  Student:   index.php?role=student
 *
 * Data:
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
$PRESENTER_KEY = 'changeme'; // <-- change this

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
   DEFAULT DATA STRUCTURES
   ========================= */
function default_quiz(): array {
  return [
    "version" => 2,
    "createdAt" => time(),
    "updatedAt" => time(),
    "status" => "idle",            // idle | open | closed
    "currentQuestionId" => null,
    "resultsPublished" => false,   // NEW: whether current question results are published
    "questions" => []
  ];
}

function default_results(): array {
  return [
    "version" => 2,
    "createdAt" => time(),
    "updatedAt" => time(),
    "answers" => [
      // questionId => [
      //   studentId => ["studentName"=>..., "optionIndex"=>..., "ts"=>...]
      // ]
    ]
  ];
}

function get_quiz(string $QUIZ_FILE): array {
  return read_json_file($QUIZ_FILE, default_quiz());
}
function get_results(string $RESULTS_FILE): array {
  return read_json_file($RESULTS_FILE, default_results());
}
function save_quiz(string $QUIZ_FILE, array $quiz): void {
  $quiz["updatedAt"] = time();
  write_json_file_atomic($QUIZ_FILE, $quiz);
}
function save_results(string $RESULTS_FILE, array $results): void {
  $results["updatedAt"] = time();
  write_json_file_atomic($RESULTS_FILE, $results);
}

/* =========================
   HELPERS
   ========================= */
function find_question(array $quiz, ?string $qid): ?array {
  if (!$qid) return null;
  foreach ($quiz["questions"] as $q) {
    if (($q["id"] ?? null) === $qid) return $q;
  }
  return null;
}

function compute_students_table(array $quiz, array $results): array {
  // Build: studentId => ["name"=>..., "points"=>int, "answered"=>int, "avg"=>float]
  $students = [];

  // map qid -> correctIndex
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
        // keep latest name seen
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

  // sort by points desc, then name asc
  usort($students, function($a, $b){
    if ($a["points"] !== $b["points"]) return $b["points"] <=> $a["points"];
    return strcmp((string)$a["studentName"], (string)$b["studentName"]);
  });

  return $students;
}

/* =========================
   AUTH / IDENTITIES
   ========================= */
$role = $_GET['role'] ?? ($_SESSION['role'] ?? 'student');
$role = ($role === 'presenter') ? 'presenter' : 'student';
$_SESSION['role'] = $role;

if ($role === 'presenter') {
  $key = (string)($_GET['key'] ?? '');
  if (!hash_equals($PRESENTER_KEY, $key)) {
    http_response_code(403);
    header('Content-Type: text/plain; charset=utf-8');
    echo "Forbidden (bad presenter key). Use: ?role=presenter&key=YOURKEY\n";
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
    $_SESSION['studentName'] = 'Student-' . substr($studentId, -4);
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

  // Presenter-only endpoints guard
  if ($role !== 'presenter' && in_array($api, ['create_question','set_current','open','close','reset','publish'], true)) {
    $respond(["ok" => false, "error" => "Presenter only"], 403);
  }

  if ($api === 'state') {
    $quiz = get_quiz($QUIZ_FILE);
    $results = get_results($RESULTS_FILE);

    $current = find_question($quiz, $quiz["currentQuestionId"] ?? null);

    // counts + percentages
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

    // Student feedback + score so far
    $student = null;
    if ($role === 'student') {
      // compute score from all answered questions so far
      $points = 0;
      $answered = 0;

      // map correct answers
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

      // current question: has student answered?
      $hasAnswered = false;
      $myOptionIndex = null;
      $isCorrect = null;

      if ($current) {
        $qid = (string)$current["id"];
        if (isset($results["answers"][$qid][$studentId])) {
          $hasAnswered = true;
          $myOptionIndex = (int)($results["answers"][$qid][$studentId]["optionIndex"] ?? -1);
        }

        // Only reveal correctness when presenter published results
        if ($hasAnswered && ($quiz["resultsPublished"] ?? false) === true) {
          $ci = (int)($current["correctIndex"] ?? -1);
          $isCorrect = ($myOptionIndex === $ci);
        }
      }

      $student = [
        "studentId" => $studentId,
        "studentName" => $studentName,
        "score" => [
          "points" => $points,
          "answered" => $answered,
          "avg" => $avg
        ],
        "current" => [
          "hasAnswered" => $hasAnswered,
          "myOptionIndex" => $myOptionIndex,
          "isCorrect" => $isCorrect
        ]
      ];
    }

    // hide correctIndex from students until published
    $safeCurrent = $current;
    if ($role === 'student' && $safeCurrent) {
      if (($quiz["resultsPublished"] ?? false) !== true) {
        unset($safeCurrent["correctIndex"]);
      }
    }

    // Presenter gets full question list + student grid
    $presenter = null;
    if ($role === 'presenter') {
      $studentsTable = compute_students_table($quiz, $results);
      $presenter = [
        "questions" => $quiz["questions"],
        "students" => $studentsTable
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

    if ($text === '') $respond(["ok" => false, "error" => "Question text is required"], 400);
    if (!is_array($optionsRaw)) $respond(["ok" => false, "error" => "Options must be array"], 400);

    $options = [];
    foreach ($optionsRaw as $o) {
      $o = trim((string)$o);
      if ($o !== '') $options[] = $o;
    }
    if (count($options) < 2) $respond(["ok" => false, "error" => "At least 2 non-empty options required"], 400);
    if ($correctIndex < 0 || $correctIndex >= count($options)) $correctIndex = 0;

    $qid = 'q_' . bin2hex(random_bytes(6));
    $q = [
      "id" => $qid,
      "text" => $text,
      "options" => $options,
      "correctIndex" => $correctIndex,
      "createdAt" => time(),
    ];

    with_lock('kahoot_clone_quiz', function() use ($QUIZ_FILE, $q) {
      $quiz = get_quiz($QUIZ_FILE);
      $quiz["questions"][] = $q;

      if (empty($quiz["currentQuestionId"])) {
        $quiz["currentQuestionId"] = $q["id"];
        $quiz["status"] = "closed";
      }
      // new question -> not published
      $quiz["resultsPublished"] = false;

      save_quiz($QUIZ_FILE, $quiz);
    });

    $respond(["ok" => true, "questionId" => $qid]);
  }

  if ($api === 'set_current') {
    $qid = (string)($_POST['questionId'] ?? '');
    if ($qid === '') $respond(["ok" => false, "error" => "questionId required"], 400);

    with_lock('kahoot_clone_quiz', function() use ($QUIZ_FILE, $RESULTS_FILE, $qid) {
      $quiz = get_quiz($QUIZ_FILE);

      $exists = false;
      foreach ($quiz["questions"] as $q) {
        if (($q["id"] ?? '') === $qid) { $exists = true; break; }
      }
      if (!$exists) return;

      $quiz["currentQuestionId"] = $qid;
      $quiz["status"] = "closed";
      $quiz["resultsPublished"] = false; // NEW: reset publish on change
      save_quiz($QUIZ_FILE, $quiz);

      $results = get_results($RESULTS_FILE);
      if (!isset($results["answers"][$qid])) $results["answers"][$qid] = [];
      save_results($RESULTS_FILE, $results);
    });

    $respond(["ok" => true]);
  }

  if ($api === 'open') {
    with_lock('kahoot_clone_quiz', function() use ($QUIZ_FILE) {
      $quiz = get_quiz($QUIZ_FILE);
      if (!empty($quiz["currentQuestionId"])) {
        $quiz["status"] = "open";
        $quiz["resultsPublished"] = false; // opening resets publish
        save_quiz($QUIZ_FILE, $quiz);
      }
    });
    $respond(["ok" => true]);
  }

  if ($api === 'close') {
    with_lock('kahoot_clone_quiz', function() use ($QUIZ_FILE) {
      $quiz = get_quiz($QUIZ_FILE);
      if (!empty($quiz["currentQuestionId"])) {
        $quiz["status"] = "closed";
        save_quiz($QUIZ_FILE, $quiz);
      }
    });
    $respond(["ok" => true]);
  }

  if ($api === 'publish') {
    // publish results for current question
    with_lock('kahoot_clone_quiz', function() use ($QUIZ_FILE) {
      $quiz = get_quiz($QUIZ_FILE);
      if (!empty($quiz["currentQuestionId"])) {
        $quiz["resultsPublished"] = true;
        // usually you'd close on publish
        if (($quiz["status"] ?? '') === 'open') $quiz["status"] = 'closed';
        save_quiz($QUIZ_FILE, $quiz);
      }
    });
    $respond(["ok" => true]);
  }

  if ($api === 'reset') {
    with_lock('kahoot_clone_quiz', function() use ($QUIZ_FILE, $RESULTS_FILE) {
      save_quiz($QUIZ_FILE, default_quiz());
      save_results($RESULTS_FILE, default_results());
    });
    $respond(["ok" => true]);
  }

  if ($api === 'answer') {
    if ($role !== 'student') $respond(["ok" => false, "error" => "Student only"], 403);

    $qid = (string)($_POST['questionId'] ?? '');
    $optionIndex = (int)($_POST['optionIndex'] ?? -1);
    if ($qid === '' || $optionIndex < 0) $respond(["ok" => false, "error" => "Invalid payload"], 400);

    $quiz = get_quiz($QUIZ_FILE);
    if (($quiz["status"] ?? 'idle') !== 'open') $respond(["ok" => false, "error" => "Question is not open"], 409);
    if (($quiz["currentQuestionId"] ?? null) !== $qid) $respond(["ok" => false, "error" => "Not the current question"], 409);

    $current = find_question($quiz, $qid);
    if (!$current) $respond(["ok" => false, "error" => "Question not found"], 404);

    $optsCount = count($current["options"] ?? []);
    if ($optionIndex < 0 || $optionIndex >= $optsCount) $respond(["ok" => false, "error" => "Option out of range"], 400);

    with_lock('kahoot_clone_results', function() use ($RESULTS_FILE, $qid, $studentId, $studentName, $optionIndex) {
      $results = get_results($RESULTS_FILE);
      if (!isset($results["answers"][$qid]) || !is_array($results["answers"][$qid])) {
        $results["answers"][$qid] = [];
      }

      // single vote per student per question
      if (isset($results["answers"][$qid][$studentId])) return;

      $results["answers"][$qid][$studentId] = [
        "studentName" => $studentName,
        "optionIndex" => $optionIndex,
        "ts" => time()
      ];
      save_results($RESULTS_FILE, $results);
    });

    $respond(["ok" => true]);
  }

  $respond(["ok" => false, "error" => "Unknown api"], 404);
}

/* =========================
   HTML UI
   ========================= */
?>
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Live Quiz</title>
  <style>
    :root{
      --bg:#0b1020;
      --card:#101a33;
      --card2:#0e1730;
      --stroke:rgba(255,255,255,.10);
      --muted:#9db0d8;
      --text:#eef3ff;
      --accent:#6ea8fe;
      --accent2:#8bd3ff;
      --good:#51cf66;
      --bad:#ff6b6b;
      --warn:#ffd43b;
      --shadow:rgba(0,0,0,.38);
    }
    *{box-sizing:border-box}
    html,body{height:100%}
    body{
      margin:0;
      font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
      color:var(--text);
      background:
        radial-gradient(1200px 700px at 15% 0%, #18295a 0%, transparent 55%),
        radial-gradient(900px 600px at 90% 10%, #0f3b4a 0%, transparent 55%),
        linear-gradient(180deg, var(--bg), #070a14 75%);
    }
    .wrap{max-width:1200px;margin:0 auto;padding:18px}
    .topbar{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
    h1{margin:0;font-size:16px;letter-spacing:.2px}
    .kpis{display:flex;gap:10px;flex-wrap:wrap}
    .pill{
      padding:7px 10px;border-radius:999px;
      background:rgba(255,255,255,.06);
      border:1px solid var(--stroke);
      color:var(--muted);
      font-size:12px;
      backdrop-filter: blur(6px);
    }
    .pill.good{border-color:rgba(81,207,102,.35);color:#c8f7d2;background:rgba(81,207,102,.10)}
    .pill.bad{border-color:rgba(255,107,107,.35);color:#ffe2e2;background:rgba(255,107,107,.10)}
    .pill.warn{border-color:rgba(255,212,59,.35);color:#fff3c7;background:rgba(255,212,59,.10)}
    .grid{display:grid;grid-template-columns:1fr;gap:14px;margin-top:14px}
    @media(min-width:980px){.grid.presenter{grid-template-columns:1.05fr .95fr}}
    .card{
      background:rgba(16,26,51,.92);
      border:1px solid var(--stroke);
      border-radius:18px;
      padding:16px;
      box-shadow:0 14px 36px var(--shadow);
    }
    .subgrid{display:grid;grid-template-columns:1fr;gap:14px}
    @media(min-width:980px){.subgrid{grid-template-columns:1fr}}
    h2{margin:0 0 10px 0;font-size:13px;color:var(--muted);font-weight:700;text-transform:uppercase;letter-spacing:.08em}
    label{display:block;font-size:12px;color:var(--muted);margin:10px 0 6px}
    input[type="text"], textarea, select{
      width:100%;padding:10px 12px;border-radius:12px;
      border:1px solid var(--stroke);
      background:rgba(0,0,0,.22);
      color:var(--text);
      outline:none;
    }
    textarea{min-height:72px;resize:vertical}
    .row{display:flex;gap:10px;flex-wrap:wrap}
    .row>*{flex:1;min-width:200px}
    button{
      border:0;border-radius:12px;padding:10px 12px;
      cursor:pointer;font-weight:800;color:#071024;
      background:linear-gradient(135deg,var(--accent),var(--accent2));
    }
    button.secondary{
      background:rgba(255,255,255,.08);
      color:var(--text);
      border:1px solid var(--stroke);
      font-weight:700;
    }
    button.ok{background:linear-gradient(135deg,var(--good),#a9f3b7);color:#06210b}
    button.danger{background:linear-gradient(135deg,var(--bad),#ffb0b0);color:#2a0a0a}
    button.warn{background:linear-gradient(135deg,var(--warn),#ffeaa0);color:#241b02}
    button:disabled{opacity:.55;cursor:not-allowed}
    .muted{color:var(--muted);font-size:12px;line-height:1.45}
    .qtext{font-size:18px;font-weight:900;margin:0 0 12px 0}
    .hr{height:1px;background:rgba(255,255,255,.10);margin:14px 0}
    .options{display:grid;grid-template-columns:1fr;gap:10px}
    @media(min-width:720px){.options{grid-template-columns:1fr 1fr}}
    .optBtn{
      text-align:left;padding:14px;border-radius:14px;
      background:rgba(255,255,255,.06);color:var(--text);
      border:1px solid var(--stroke);font-weight:800;
      transition:transform .06s ease, border-color .12s ease, background .12s ease;
    }
    .optBtn:hover{transform:translateY(-1px);border-color:rgba(110,168,254,.55);background:rgba(110,168,254,.10)}
    .optMeta{display:flex;justify-content:space-between;gap:12px;font-size:12px;color:var(--muted);margin-top:6px}
    .bar{height:10px;border-radius:999px;background:rgba(255,255,255,.08);overflow:hidden;border:1px solid rgba(255,255,255,.08)}
    .bar > div{height:100%;background:linear-gradient(135deg,var(--accent),var(--accent2));width:0%;transition:width 160ms linear}
    .feedback{
      padding:10px 12px;border-radius:14px;
      border:1px solid var(--stroke);
      background:rgba(255,255,255,.05);
      margin-top:12px;
    }
    .feedback.good{border-color:rgba(81,207,102,.35);background:rgba(81,207,102,.10)}
    .feedback.bad{border-color:rgba(255,107,107,.35);background:rgba(255,107,107,.10)}
    table{width:100%;border-collapse:collapse;font-size:12px}
    th,td{padding:10px 8px;border-bottom:1px solid rgba(255,255,255,.08);text-align:left}
    th{color:#cfe1ff;font-size:11px;text-transform:uppercase;letter-spacing:.07em}
    .right{text-align:right}
    .mono{font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace}
  </style>
</head>
<body>
<div class="wrap">
  <div class="topbar">
    <h1>Live Quiz</h1>
    <div class="kpis">
      <span class="pill" id="statusPill">status: …</span>
      <span class="pill" id="qidPill">question: …</span>
      <span class="pill" id="pubPill">published: …</span>
      <span class="pill" id="updatedPill">updated: …</span>
      <?php if ($role === 'student'): ?>
        <span class="pill">you: <?= htmlspecialchars($_SESSION['studentName'] ?? 'student', ENT_QUOTES, 'UTF-8') ?></span>
      <?php else: ?>
        <span class="pill">role: presenter</span>
      <?php endif; ?>
    </div>
  </div>

<?php if ($role === 'presenter'): ?>
  <div class="grid presenter">
    <div class="card">
      <h2>Create question</h2>

      <label>Question</label>
      <textarea id="qText" placeholder="Type the question…"></textarea>

      <div class="row">
        <div><label>Option A</label><input id="opt0" type="text" placeholder="Option A" /></div>
        <div><label>Option B</label><input id="opt1" type="text" placeholder="Option B" /></div>
      </div>

      <div class="row">
        <div><label>Option C</label><input id="opt2" type="text" placeholder="Option C (optional)" /></div>
        <div><label>Option D</label><input id="opt3" type="text" placeholder="Option D (optional)" /></div>
      </div>

      <label>Correct answer</label>
      <select id="correctIndex">
        <option value="0">A</option>
        <option value="1">B</option>
        <option value="2">C</option>
        <option value="3">D</option>
      </select>

      <div class="row" style="margin-top:12px;">
        <button id="createBtn">Create</button>
        <button class="secondary" id="refreshBtn">Refresh</button>
      </div>

      <div class="hr"></div>

      <h2>Live control</h2>
      <div class="row">
        <button class="ok" id="openBtn">Open</button>
        <button class="secondary" id="closeBtn">Close</button>
        <button class="warn" id="publishBtn">Publish results</button>
        <button class="danger" id="resetBtn">Reset</button>
      </div>

      <label style="margin-top:12px;">Select current question</label>
      <select id="questionPicker"></select>
      <div class="row" style="margin-top:10px;">
        <button class="secondary" id="setCurrentBtn">Set current</button>
      </div>

      <p class="muted" id="presenterMsg" style="margin-top:10px;"></p>
    </div>

    <div class="card">
      <h2>Live view</h2>
      <p class="qtext" id="liveQuestion">Waiting…</p>
      <div id="liveOptions" class="muted"></div>

      <div class="hr"></div>

      <h2>Current counts</h2>
      <div id="countsBox" class="muted">No data.</div>

      <div class="hr"></div>

      <h2>Students & evaluation</h2>
      <div class="muted" id="studentsBox">No students yet.</div>
    </div>
  </div>

<?php else: ?>
  <div class="grid">
    <div class="card">
      <h2>Student</h2>

      <form method="post" style="margin-bottom:12px;">
        <label>Your name (stored in session)</label>
        <div class="row">
          <input type="text" name="studentName" value="<?= htmlspecialchars($_SESSION['studentName'] ?? '', ENT_QUOTES, 'UTF-8') ?>" />
          <button class="secondary" type="submit">Save</button>
        </div>
      </form>

      <div class="row">
        <div class="pill" id="scorePill">score: …</div>
        <div class="pill" id="avgPill">avg: …</div>
      </div>

      <div class="hr"></div>

      <p class="qtext" id="studentQuestion">Waiting for presenter…</p>
      <div class="options" id="studentOptions"></div>

      <div id="studentFeedback" class="feedback" style="display:none;"></div>

      <div class="hr"></div>

      <h2>Live percentages</h2>
      <div id="studentPercents" class="muted">No data.</div>

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
    $("statusPill").textContent = `status: ${state.quiz?.status ?? "?"}`;
    $("qidPill").textContent = `question: ${state.quiz?.currentQuestionId ?? "none"}`;
    $("pubPill").textContent = `published: ${state.quiz?.resultsPublished ? "yes" : "no"}`;
    $("updatedPill").textContent = `updated: ${state.quiz?.updatedAt ? new Date(state.quiz.updatedAt*1000).toLocaleTimeString() : "?"}`;
  }

  // ===== Presenter render =====
  function presenterRender(state) {
    const q = state.currentQuestion;
    const counts = state.counts || [];
    const perc = state.percentages || [];
    const total = state.totalAnswers || 0;

    $("liveQuestion").textContent = q ? q.text : "No current question.";

    const optsWrap = $("liveOptions");
    optsWrap.innerHTML = "";

    if (q && q.options && q.options.length) {
      optsWrap.innerHTML = q.options.map((t, i) => {
        const isCorrect = (typeof q.correctIndex === "number" && i === q.correctIndex);
        return `<div style="margin:10px 0;">
          <div><strong>${String.fromCharCode(65+i)}.</strong> ${escapeHtml(t)} ${isCorrect ? '<span class="pill good" style="margin-left:8px;">correct</span>' : ''}</div>
        </div>`;
      }).join("");
    } else {
      optsWrap.textContent = "Create a question to start.";
    }

    // counts box with percentages
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
      }).join("") + `<div class="muted">Total answers: <strong>${total}</strong></div>`;
    } else {
      countsBox.textContent = "No data.";
    }

    // question picker
    const picker = $("questionPicker");
    if (picker && state.presenter?.questions) {
      const qs = state.presenter.questions;
      picker.innerHTML = qs.map(qx => {
        const sel = (qx.id === state.quiz.currentQuestionId) ? "selected" : "";
        const label = (qx.text || "").slice(0, 60);
        return `<option value="${escapeHtml(qx.id)}" ${sel}>${escapeHtml(qx.id)} — ${escapeHtml(label)}</option>`;
      }).join("");
      if (qs.length === 0) picker.innerHTML = `<option value="">(no questions yet)</option>`;
    }

    // students table
    const studentsBox = $("studentsBox");
    const students = state.presenter?.students || [];
    if (!students.length) {
      studentsBox.textContent = "No students yet.";
    } else {
      studentsBox.innerHTML = `
        <table>
          <thead>
            <tr>
              <th>Student</th>
              <th class="right">Points</th>
              <th class="right">Answered</th>
              <th class="right">Avg</th>
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
        <div class="muted" style="margin-top:8px;">Avg is points/answered (each question = 1 point).</div>
      `;
    }
  }

  // ===== Student render =====
  let answeredLocal = {}; // qid => true

  function studentRender(state) {
    const q = state.currentQuestion;
    const status = state.quiz?.status;
    const published = !!state.quiz?.resultsPublished;

    const qEl = $("studentQuestion");
    const optsEl = $("studentOptions");
    const msgEl = $("studentMsg");

    const score = state.student?.score;
    if (score) {
      $("scorePill").textContent = `score: ${score.points}/${score.answered}`;
      $("avgPill").textContent = `avg: ${score.avg}`;
    }

    optsEl.innerHTML = "";
    msgEl.textContent = "";

    if (!q) {
      qEl.textContent = "Waiting for presenter…";
      $("studentPercents").textContent = "No data.";
      hideFeedback();
      return;
    }

    qEl.textContent = q.text;

    // show percentages live
    renderStudentPercents(state);

    const already = answeredLocal[q.id] || state.student?.current?.hasAnswered;
    const canAnswer = (status === "open") && !already;

    (q.options || []).forEach((t, i) => {
      const b = document.createElement("button");
      b.className = "optBtn";
      b.innerHTML = `<div><strong>${String.fromCharCode(65+i)}.</strong> ${escapeHtml(t)}</div>
                     <div class="optMeta"><span>Live</span><span class="mono">${(state.percentages?.[i] ?? 0)}%</span></div>
                     <div class="bar"><div style="width:${(state.percentages?.[i] ?? 0)}%;"></div></div>`;
      b.disabled = !canAnswer;

      b.addEventListener("click", async () => {
        b.disabled = true;
        const res = await apiPost("answer", { questionId: q.id, optionIndex: i });
        if (res.ok) {
          answeredLocal[q.id] = true;
          msgEl.textContent = "Answer recorded.";
        } else {
          msgEl.textContent = "Could not submit: " + (res.error || "error");
          b.disabled = false;
        }
      });

      optsEl.appendChild(b);
    });

    if (already) {
      msgEl.textContent = "Answer already recorded for this question.";
    } else if (status !== "open") {
      msgEl.textContent = "Not open yet (or already closed).";
    }

    // feedback when published
    if (published && state.student?.current?.hasAnswered && typeof state.student.current.isCorrect === "boolean") {
      if (state.student.current.isCorrect) {
        showFeedback(true, "Correct ✅ (+1 point)");
      } else {
        showFeedback(false, "Incorrect ❌ (0 points)");
      }
    } else {
      // keep feedback hidden until published
      hideFeedback();
    }
  }

  function renderStudentPercents(state) {
    const q = state.currentQuestion;
    const percBox = $("studentPercents");
    if (!q || !q.options || !q.options.length) {
      percBox.textContent = "No data.";
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
    }).join("") + `<div class="muted">Total answers so far: <strong>${total}</strong></div>`;
  }

  function showFeedback(ok, text) {
    const box = $("studentFeedback");
    box.style.display = "block";
    box.className = "feedback " + (ok ? "good" : "bad");
    box.innerHTML = `<strong>${ok ? "SUCCESS" : "FAILED"}</strong> — ${escapeHtml(text)}`;
  }
  function hideFeedback() {
    const box = $("studentFeedback");
    box.style.display = "none";
    box.className = "feedback";
    box.textContent = "";
  }

  // ===== Heartbeat (1 second) =====
  async function tick() {
    try {
      const state = await apiGetState();
      if (!state || !state.ok) return;
      setTopPills(state);

      if (ROLE === "presenter") presenterRender(state);
      else studentRender(state);
    } catch (e) {}
  }

  // ===== Presenter actions =====
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
        ? `Created question: ${res.questionId}`
        : `Error: ${res.error || "unknown"}`;

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
      $("presenterMsg").textContent = "Results published for current question.";
      await tick();
    });

    $("resetBtn").addEventListener("click", async () => {
      if (!confirm("Reset quiz and ALL results?")) return;
      await apiPost("reset", {});
      $("presenterMsg").textContent = "Reset done.";
      await tick();
    });

    $("refreshBtn").addEventListener("click", tick);

    $("setCurrentBtn").addEventListener("click", async () => {
      const picker = $("questionPicker");
      const qid = picker?.value || "";
      if (!qid) return;
      await apiPost("set_current", { questionId: qid });
      $("presenterMsg").textContent = `Current question set: ${qid}`;
      await tick();
    });
  }

  tick();
  setInterval(tick, 1000);
</script>
</body>
</html>

