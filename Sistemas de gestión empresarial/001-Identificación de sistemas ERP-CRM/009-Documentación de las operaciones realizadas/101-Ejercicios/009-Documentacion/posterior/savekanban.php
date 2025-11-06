<?php
// save_kanban.php
header('Content-Type: application/json; charset=utf-8');

try {
  // 1) Leer body
  $raw = file_get_contents('php://input');
  if ($raw === false) throw new RuntimeException("No se pudo leer el body.");
  $payload = json_decode($raw, true, 512, JSON_THROW_ON_ERROR);

  if (!isset($payload['data']) || !is_array($payload['data'])) {
    throw new InvalidArgumentException("Falta 'data' o no es un objeto/array JSON.");
  }

  // 2) Cargar la clase (ajusta la ruta si procede)
  require_once __DIR__ . '/kanban.php';

  // 3) Instanciar bridge y guardar a SQLite
  $bridge = new JsonSqliteBridge();

  // Ruta de la BD. Si quieres “histórico por fecha”, cámbialo por un nombre con timestamp.
  $dbDir = __DIR__ . '/data';
  if (!is_dir($dbDir)) { mkdir($dbDir, 0775, true); }

  // Opción A: sobreescribir siempre el mismo archivo
  $dbPath = $dbDir . '/kanban.sqlite';

  // Opción B (histórico): descomenta
  // $dbPath = $dbDir . '/kanban_' . date('Ymd_His') . '.sqlite';

  // El método crea SIEMPRE una BD nueva (borra si existe)
  $bridge->loadFromArray($payload['data'], $dbPath);

  // 4) (Opcional) Devolver el JSON reconstruido para verificar round-trip
  $roundtrip = $bridge->dumpToArray($dbPath);

  echo json_encode([
    'ok' => true,
    'message' => 'Kanban guardado en SQLite correctamente.',
    'db' => basename($dbPath),
    'tables' => array_keys($roundtrip),
  ], JSON_UNESCAPED_UNICODE);

} catch (Throwable $e) {
  http_response_code(400);
  echo json_encode([
    'ok' => false,
    'error' => $e->getMessage(),
    'trace' => (ini_get('display_errors') ? $e->getTraceAsString() : null)
  ], JSON_UNESCAPED_UNICODE);
}

