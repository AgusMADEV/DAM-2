<?php
// save_polygons.php
// Receives: { area: "name", geojson: FeatureCollection }
// Saves: exports/name_YYYYmmdd_HHMMSS.svg

header('Content-Type: application/json; charset=utf-8');

function fail($msg, $code = 400) {
  http_response_code($code);
  echo json_encode(["ok" => false, "error" => $msg], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
  exit;
}

$raw = file_get_contents("php://input");
if ($raw === false || trim($raw) === "") fail("Empty body");

$data = json_decode($raw, true);
if (!is_array($data)) fail("Invalid JSON");

$area = $data["area"] ?? "area";
$geo  = $data["geojson"] ?? null;

if (!is_string($area)) $area = "area";
$area = preg_replace('/[^a-zA-Z0-9_\-]+/', '_', $area);

if (!is_array($geo) || ($geo["type"] ?? "") !== "FeatureCollection") {
  fail("geojson must be a FeatureCollection");
}

$features = $geo["features"] ?? [];
if (!is_array($features) || count($features) === 0) fail("No features");

// Collect all lon/lat points to compute bounds
$all = [];

function push_coords(&$all, $coords) {
  // coords could be:
  // Polygon: [ [ [lon,lat], ... ] , [hole...], ...]
  // MultiPolygon: [ [ [ [lon,lat], ... ] ], ... ]
  if (!is_array($coords)) return;

  // Detect depth by checking first items
  // We will recursively walk arrays until we find [lon,lat]
  $stack = [$coords];
  while ($stack) {
    $x = array_pop($stack);
    if (!is_array($x)) continue;

    // Candidate point: [lon, lat]
    if (count($x) === 2 && is_numeric($x[0]) && is_numeric($x[1])) {
      $all[] = [(float)$x[0], (float)$x[1]];
      continue;
    }
    // Otherwise expand
    foreach ($x as $y) $stack[] = $y;
  }
}

foreach ($features as $f) {
  $g = $f["geometry"] ?? null;
  if (!is_array($g)) continue;
  $type = $g["type"] ?? "";
  $coords = $g["coordinates"] ?? null;
  if ($type === "Polygon" || $type === "MultiPolygon") {
    push_coords($all, $coords);
  }
}

if (count($all) < 3) fail("Not enough coordinates to build SVG");

$minLon = $maxLon = $all[0][0];
$minLat = $maxLat = $all[0][1];

foreach ($all as $p) {
  $lon = $p[0]; $lat = $p[1];
  if ($lon < $minLon) $minLon = $lon;
  if ($lon > $maxLon) $maxLon = $lon;
  if ($lat < $minLat) $minLat = $lat;
  if ($lat > $maxLat) $maxLat = $lat;
}

// SVG canvas size
$W = 1400;
$H = 1000;
$pad = 20;

// Map lon/lat to x/y (simple equirectangular projection)
$lonSpan = max(1e-12, $maxLon - $minLon);
$latSpan = max(1e-12, $maxLat - $minLat);

function proj($lon, $lat, $minLon, $minLat, $lonSpan, $latSpan, $W, $H, $pad) {
  // x: left->right is lon increasing
  // y: top->bottom is lat decreasing (invert)
  $x = $pad + (($lon - $minLon) / $lonSpan) * ($W - 2*$pad);
  $y = $pad + (1.0 - (($lat - $minLat) / $latSpan)) * ($H - 2*$pad);
  return [$x, $y];
}

// Build SVG paths from GeoJSON Polygon/MultiPolygon (outer rings only)
function ring_to_path($ring, $minLon, $minLat, $lonSpan, $latSpan, $W, $H, $pad) {
  if (!is_array($ring) || count($ring) < 4) return "";
  $d = "";
  $first = true;
  foreach ($ring as $pt) {
    if (!is_array($pt) || count($pt) < 2) continue;
    $lon = (float)$pt[0];
    $lat = (float)$pt[1];
    [$x, $y] = proj($lon, $lat, $minLon, $minLat, $lonSpan, $latSpan, $W, $H, $pad);
    $cmd = $first ? "M" : "L";
    $d .= $cmd . " " . round($x, 2) . " " . round($y, 2) . " ";
    $first = false;
  }
  $d .= "Z";
  return trim($d);
}

$paths = [];
foreach ($features as $f) {
  $g = $f["geometry"] ?? null;
  if (!is_array($g)) continue;
  $type = $g["type"] ?? "";
  $coords = $g["coordinates"] ?? null;

  if ($type === "Polygon" && is_array($coords) && isset($coords[0])) {
    // coords[0] is outer ring
    $d = ring_to_path($coords[0], $minLon, $minLat, $lonSpan, $latSpan, $W, $H, $pad);
    if ($d !== "") $paths[] = $d;

  } elseif ($type === "MultiPolygon" && is_array($coords)) {
    foreach ($coords as $poly) {
      if (is_array($poly) && isset($poly[0])) {
        $d = ring_to_path($poly[0], $minLon, $minLat, $lonSpan, $latSpan, $W, $H, $pad);
        if ($d !== "") $paths[] = $d;
      }
    }
  }
}

if (count($paths) === 0) fail("No valid polygon paths to write");

// Prepare folder
$dir = __DIR__ . "/exports";
if (!is_dir($dir)) {
  if (!mkdir($dir, 0775, true)) fail("Cannot create exports directory", 500);
}

// Filename
$ts = date("Ymd_His");
$file = "{$area}_{$ts}.svg";
$full = $dir . "/" . $file;

// SVG content
$svg  = '';
$svg .= '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
$svg .= '<svg xmlns="http://www.w3.org/2000/svg" width="'.$W.'" height="'.$H.'" viewBox="0 0 '.$W.' '.$H.'">' . "\n";
$svg .= '  <rect x="0" y="0" width="'.$W.'" height="'.$H.'" fill="#0b1220"/>' . "\n";
$svg .= '  <g fill="#e7eefc" fill-opacity="0.18" stroke="#e7eefc" stroke-opacity="0.7" stroke-width="1">' . "\n";

foreach ($paths as $d) {
  $svg .= '    <path d="'.htmlspecialchars($d, ENT_QUOTES, 'UTF-8').'"/>' . "\n";
}

$svg .= "  </g>\n";
$svg .= "</svg>\n";

if (file_put_contents($full, $svg) === false) {
  fail("Cannot write SVG file", 500);
}

echo json_encode([
  "ok" => true,
  "file" => "exports/" . $file,
  "count" => count($paths),
  "bounds" => [
    "minLon" => $minLon, "minLat" => $minLat,
    "maxLon" => $maxLon, "maxLat" => $maxLat
  ]
], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);

