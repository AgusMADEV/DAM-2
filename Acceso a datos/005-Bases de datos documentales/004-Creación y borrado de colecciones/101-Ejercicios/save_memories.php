<?php
header('Content-Type: application/json; charset=utf-8');

$file = __DIR__ . '/memories.json';

function read_json_file($path) {
  if (!file_exists($path)) return [];
  $raw = file_get_contents($path);
  if ($raw === false || trim($raw) === '') return [];
  $data = json_decode($raw, true);
  return is_array($data) ? $data : [];
}

function write_json_file($path, $data) {
  $json = json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
  // LOCK_EX to avoid concurrent write corruption
  return file_put_contents($path, $json, LOCK_EX) !== false;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  $data = json_decode(file_get_contents('php://input'), true);
  if (!is_array($data)) {
    echo json_encode(['success' => false, 'error' => 'JSON inválido']);
    exit;
  }

  $memories = read_json_file($file);
  $memories[] = $data;

  if (!write_json_file($file, $memories)) {
    echo json_encode(['success' => false, 'error' => 'No se pudo escribir el archivo']);
    exit;
  }

  echo json_encode(['success' => true]);
  exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
  echo json_encode(read_json_file($file), JSON_UNESCAPED_UNICODE);
  exit;
}

echo json_encode(['success' => false, 'error' => 'Método no soportado']);

