<?php
/**
 * Single-file Kahoot-like live quiz (PHP + JSON + 1s polling)
 *
 * Usage:
 *  Presenter: index.php?role=presenter&key=changeme
 *  Student:   index.php?role=student
 *
 * Files created:
 *  ./quiz_data/quiz.json      -> questions + current question state
 *  ./quiz_data/results.json   -> student answers + timestamps
 */

declare(strict_types=1);
ini_set('display_errors', '1');
error_reporting(E_ALL);

session_start();

/* =========================
   CONFIG
   ========================= */
$PRESENTER_KEY = 'changeme'; // <-- set your presenter key here

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
    "version" => 1,
    "createdAt" => time(),
    "updatedAt" => time(),
    "status" => "idle", // idle | open | closed
    "currentQuestionId" => null,
    "questions" => [
      // each:
      // [
      //   "id" => "q_...",
      //   "text" => "...",
      //   "options" => ["A","B","C","D"],
      //   "correctIndex" => 0,
      //   "createdAt" => time()
      // ]
    ],
  ];
}

function default_results(): array {
  return [
    "version" => 1,
    "createdAt" => time(),
    "updatedAt" => time(),
    "answers" => [
      // questionId => [
      //   studentId => [
      //     "studentName" => "...",
      //     "optionIndex" => 2,
      //     "ts" => time()
      //   ]
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

if ($role === 'student') {
  // student identity (persist in session)
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

  if ($api === 'state') {
    // Students + presenter poll this every 1s
    $quiz = get_quiz($QUIZ_FILE);
    $results = get_results($RESULTS_FILE);

    $current = null;
    if (!empty($quiz["currentQuestionId"])) {
      foreach ($quiz["questions"] as $q) {
        if (($q["id"] ?? null) === $quiz["currentQuestionId"]) {
          $current = $q;
          break;
        }
      }
    }

    // build counts for current question
    $counts = [];
    if ($current) {
      $qid = $current["id"];
      $opts = $current["options"] ?? [];
      $counts = array_fill(0, count($opts), 0);

      $answers = $results["answers"][$qid] ?? [];
      if (is_array($answers)) {
        foreach ($answers as $ans) {
          $oi = (int)($ans["optionIndex"] ?? -1);
          if ($oi >= 0 && $oi < count($counts)) $counts[$oi]++;
        }
      }
    }

    // hide correct answer from students while open
    $safeCurrent = $current;
    if ($role === 'student' && $quiz["status"] === 'open' && $safeCurrent) {
      unset($safeCurrent["correctIndex"]);
    }

    $respond([
      "ok" => true,
      "serverTime" => time(),
      "quiz" => [
        "status" => $quiz["status"],
        "currentQuestionId" => $quiz["currentQuestionId"],
        "updatedAt" => $quiz["updatedAt"],
        "questionsCount" => count($quiz["questions"]),
      ],
      "currentQuestion" => $safeCurrent,
      "counts" => $counts,
      "me" => ($role === 'student') ? [
        "studentId" => $studentId,
        "studentName" => $studentName
      ] : ["role" => "presenter"]
    ]);
  }

  if ($role !== 'presenter' && in_array($api, ['create_question','set_current','open','close','reset'], true)) {
    $respond(["ok" => false, "error" => "Presenter only"], 403);
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
      // if no current question yet, set it
      if (empty($quiz["currentQuestionId"])) {
        $quiz["currentQuestionId"] = $q["id"];
        $quiz["status"] = "closed";
      }
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
      save_quiz($QUIZ_FILE, $quiz);

      // optionally ensure results structure exists (no-op if not)
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

    // validate option index against question
    $current = null;
    foreach ($quiz["questions"] as $q) {
      if (($q["id"] ?? null) === $qid) { $current = $q; break; }
    }
    if (!$current) $respond(["ok" => false, "error" => "Question not found"], 404);
    $optsCount = count($current["options"] ?? []);
    if ($optionIndex < 0 || $optionIndex >= $optsCount) $respond(["ok" => false, "error" => "Option out of range"], 400);

    with_lock('kahoot_clone_results', function() use ($RESULTS_FILE, $qid, $studentId, $studentName, $optionIndex) {
      $results = get_results($RESULTS_FILE);
      if (!isset($results["answers"][$qid]) || !is_array($results["answers"][$qid])) {
        $results["answers"][$qid] = [];
      }

      // single vote per student per question (overwrite disabled)
      if (isset($results["answers"][$qid][$studentId])) {
        return;
      }

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
  <title>Live Quiz (Single PHP)</title>
  <style>
    :root { --bg:#0b1220; --card:#121b2f; --muted:#93a4c7; --text:#e9efff; --accent:#6ea8fe; --danger:#ff6b6b; --ok:#51cf66; }
    *{ box-sizing:border-box; }
    body{ margin:0; font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; background: radial-gradient(1200px 600px at 20% 0%, #162143 0%, var(--bg) 55%); color:var(--text); }
    .wrap{ max-width:1100px; margin:0 auto; padding:20px; }
    .topbar{ display:flex; align-items:center; justify-content:space-between; gap:12px; flex-wrap:wrap; }
    .pill{ padding:6px 10px; border-radius:999px; background: rgba(255,255,255,0.08); color:var(--muted); font-size:12px; }
    .grid{ display:grid; grid-template-columns: 1fr; gap:16px; margin-top:16px; }
    @media(min-width: 900px){ .grid.presenter{ grid-template-columns: 1.1fr 0.9fr; } }
    .card{ background: rgba(18,27,47,0.92); border:1px solid rgba(255,255,255,0.08); border-radius:16px; padding:16px; box-shadow: 0 10px 30px rgba(0,0,0,0.35); }
    h1{ margin:0; font-size:18px; letter-spacing:0.2px; }
    h2{ margin:0 0 10px 0; font-size:14px; color:var(--muted); font-weight:600; }
    label{ display:block; font-size:12px; color:var(--muted); margin:10px 0 6px; }
    input[type="text"], textarea, select{
      width:100%; padding:10px 12px; border-radius:12px; border:1px solid rgba(255,255,255,0.10);
      background: rgba(0,0,0,0.22); color: var(--text); outline:none;
    }
    textarea{ min-height:70px; resize:vertical; }
    .row{ display:flex; gap:10px; flex-wrap:wrap; }
    .row > *{ flex:1; min-width: 180px; }
    button{
      border:0; border-radius:12px; padding:10px 12px; cursor:pointer; color:#081023;
      background: var(--accent); font-weight:700;
    }
    button.secondary{ background: rgba(255,255,255,0.10); color: var(--text); border:1px solid rgba(255,255,255,0.12); }
    button.danger{ background: var(--danger); color:#240b0b; }
    button.ok{ background: var(--ok); color:#081a0b; }
    button:disabled{ opacity:0.55; cursor:not-allowed; }
    .muted{ color: var(--muted); font-size:12px; line-height:1.4; }
    .questionText{ font-size:18px; font-weight:800; margin:0 0 12px 0; }
    .options{ display:grid; grid-template-columns: 1fr; gap:10px; }
    @media(min-width: 700px){ .options{ grid-template-columns: 1fr 1fr; } }
    .optBtn{ text-align:left; padding:14px; border-radius:14px; background: rgba(255,255,255,0.08); color: var(--text); border:1px solid rgba(255,255,255,0.10); font-weight:700; }
    .optBtn:hover{ border-color: rgba(110,168,254,0.55); }
    .bar{ height:10px; border-radius:999px; background: rgba(255,255,255,0.08); overflow:hidden; }
    .bar > div{ height:100%; background: var(--accent); width:0%; transition: width 160ms linear; }
    .kpi{ display:flex; gap:10px; flex-wrap:wrap; }
    .kpi .pill{ background: rgba(110,168,254,0.12); color: #cfe1ff; border:1px solid rgba(110,168,254,0.20); }
    .small{ font-size:11px; }
    .hr{ height:1px; background: rgba(255,255,255,0.10); margin:14px 0; }
  </style>
</head>
<body>
<div class="wrap">
  <div class="topbar">
    <h1>Live Quiz (Single PHP + JSON)</h1>
    <div class="kpi">
      <span class="pill" id="statusPill">status: …</span>
      <span class="pill" id="qidPill">question: …</span>
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
        <h2>Create question (on the fly)</h2>

        <label>Question</label>
        <textarea id="qText" placeholder="Type the question…"></textarea>

        <div class="row">
          <div>
            <label>Option A</label>
            <input id="opt0" type="text" placeholder="Answer option A" />
          </div>
          <div>
            <label>Option B</label>
            <input id="opt1" type="text" placeholder="Answer option B" />
          </div>
        </div>

        <div class="row">
          <div>
            <label>Option C</label>
            <input id="opt2" type="text" placeholder="Answer option C (optional)" />
          </div>
          <div>
            <label>Option D</label>
            <input id="opt3" type="text" placeholder="Answer option D (optional)" />
          </div>
        </div>

        <label>Correct answer</label>
        <select id="correctIndex">
          <option value="0">A</option>
          <option value="1">B</option>
          <option value="2">C</option>
          <option value="3">D</option>
        </select>

        <div class="row" style="margin-top:12px;">
          <button id="createBtn">Create question</button>
          <button class="secondary" id="refreshBtn">Refresh now</button>
        </div>

        <div class="hr"></div>

        <h2>Live control</h2>
        <div class="row">
          <button class="ok" id="openBtn">Open answering</button>
          <button class="secondary" id="closeBtn">Close answering</button>
          <button class="danger" id="resetBtn">Reset quiz + results</button>
        </div>

        <label style="margin-top:12px;">Jump to an existing question</label>
        <select id="questionPicker"></select>
        <div class="row" style="margin-top:10px;">
          <button class="secondary" id="setCurrentBtn">Set current</button>
        </div>

        <p class="muted" id="presenterMsg" style="margin-top:10px;"></p>
      </div>

      <div class="card">
        <h2>Live view</h2>
        <p class="questionText" id="liveQuestion">Waiting…</p>
        <div id="liveOptions"></div>

        <div class="hr"></div>

        <h2>Counts (current question)</h2>
        <div id="countsBox" class="muted">No data.</div>
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

        <p class="questionText" id="studentQuestion">Waiting for presenter…</p>
        <div class="options" id="studentOptions"></div>
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

  function setTopPills(state) {
    $("statusPill").textContent = `status: ${state.quiz?.status ?? "?"}`;
    $("qidPill").textContent = `question: ${state.quiz?.currentQuestionId ?? "none"}`;
    $("updatedPill").textContent = `updated: ${state.quiz?.updatedAt ? new Date(state.quiz.updatedAt*1000).toLocaleTimeString() : "?"}`;
  }

  // ===== Presenter UI =====
  function presenterRender(state) {
    const q = state.currentQuestion;

    $("liveQuestion").textContent = q ? q.text : "No current question.";
    const optsWrap = $("liveOptions");
    optsWrap.innerHTML = "";

    if (q && q.options && q.options.length) {
      const ul = document.createElement("div");
      ul.className = "muted";
      ul.innerHTML = q.options.map((t, i) => {
        const isCorrect = (typeof q.correctIndex === "number" && i === q.correctIndex);
        return `<div style="margin:8px 0;">
          <div><strong>${String.fromCharCode(65+i)}.</strong> ${escapeHtml(t)} ${isCorrect ? '<span class="pill small" style="margin-left:8px;">correct</span>' : ''}</div>
        </div>`;
      }).join("");
      optsWrap.appendChild(ul);
    } else {
      optsWrap.textContent = "Create a question to start.";
    }

    // counts
    const countsBox = $("countsBox");
    const counts = state.counts || [];
    if (q && q.options && q.options.length) {
      const total = counts.reduce((a,b)=>a+b,0) || 0;
      countsBox.innerHTML = q.options.map((t, i) => {
        const c = counts[i] ?? 0;
        const pct = total ? Math.round((c/total)*100) : 0;
        return `
          <div style="margin:10px 0;">
            <div style="display:flex;justify-content:space-between;gap:12px;">
              <div><strong>${String.fromCharCode(65+i)}.</strong> ${escapeHtml(t)}</div>
              <div><strong>${c}</strong> (${pct}%)</div>
            </div>
            <div class="bar"><div style="width:${pct}%;"></div></div>
          </div>
        `;
      }).join("") + `<div class="muted">Total answers: <strong>${total}</strong></div>`;
    } else {
      countsBox.textContent = "No data.";
    }

    // question picker
    const picker = $("questionPicker");
    if (picker && state.quiz?.questionsCount !== undefined) {
      // Fetch quiz list indirectly: simplest is to keep a local cache by calling state + reading from server is not included.
      // To keep it single endpoint, we rebuild picker by asking server for full list is not currently returned.
      // Instead: we approximate by letting presenter paste ID via "Set current" only.
      // BUT: we can include full list by asking server to return it for presenter in state.
      // For simplicity, we will re-request state with a query parameter in a future improvement.
    }
  }

  // ===== Student UI =====
  let lastRenderedQid = null;
  let answeredForQid = {}; // local UI lock

  function studentRender(state) {
    const q = state.currentQuestion;
    const status = state.quiz?.status;

    const qEl = $("studentQuestion");
    const optsEl = $("studentOptions");
    const msgEl = $("studentMsg");

    optsEl.innerHTML = "";

    if (!q) {
      qEl.textContent = "Waiting for presenter…";
      msgEl.textContent = "";
      return;
    }

    qEl.textContent = q.text;

    // if question changed, reset local UI lock
    if (q.id !== lastRenderedQid) {
      lastRenderedQid = q.id;
      msgEl.textContent = "";
    }

    if (status !== "open") {
      msgEl.textContent = "Not open yet (or already closed).";
    }

    const already = !!answeredForQid[q.id];

    (q.options || []).forEach((t, i) => {
      const b = document.createElement("button");
      b.className = "optBtn";
      b.textContent = `${String.fromCharCode(65+i)}. ${t}`;
      b.disabled = (status !== "open") || already;

      b.addEventListener("click", async () => {
        b.disabled = true;
        const res = await apiPost("answer", { questionId: q.id, optionIndex: i });
        if (res.ok) {
          answeredForQid[q.id] = true;
          msgEl.textContent = "Answer recorded.";
        } else {
          msgEl.textContent = "Could not submit: " + (res.error || "error");
          // allow retry if not recorded
          b.disabled = false;
        }
      });

      optsEl.appendChild(b);
    });

    if (already) {
      msgEl.textContent = "Answer already recorded for this question.";
    }
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({
      "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"
    }[c]));
  }

  // ===== Heartbeat (1 second) =====
  async function tick() {
    try {
      const state = await apiGetState();
      if (!state || !state.ok) return;
      setTopPills(state);

      if (ROLE === "presenter") presenterRender(state);
      else studentRender(state);

    } catch (e) {
      // ignore transient errors
    }
  }

  // Presenter actions
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

    $("resetBtn").addEventListener("click", async () => {
      if (!confirm("Reset quiz and ALL results?")) return;
      await apiPost("reset", {});
      await tick();
    });

    $("refreshBtn").addEventListener("click", tick);

    // Minimal "set current": prompt for ID (keeps file single + simple)
    const setBtn = document.createElement("button");
    setBtn.className = "secondary";
    setBtn.textContent = "Set current by ID…";
    setBtn.addEventListener("click", async () => {
      const qid = prompt("Enter questionId (e.g., q_ab12cd…):");
      if (!qid) return;
      await apiPost("set_current", { questionId: qid.trim() });
      await tick();
    });
    $("setCurrentBtn").replaceWith(setBtn);
  }

  tick();
  setInterval(tick, 1000);
</script>
</body>
</html>

