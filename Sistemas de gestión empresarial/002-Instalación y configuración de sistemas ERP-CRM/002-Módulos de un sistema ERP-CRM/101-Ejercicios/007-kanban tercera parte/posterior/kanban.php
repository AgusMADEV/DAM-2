<?php
/**
 * JsonSqliteBridge (PHP)
 * ----------------------
 * Convierte JSON <-> SQLite de forma recursiva.
 *
 * Reglas base:
 *  - Cada CLAVE del objeto raíz del JSON es una TABLA TOP-LEVEL.
 *  - Las subestructuras (dict/list) se materializan como tablas hijas con FK al padre.
 *  - Las listas de escalares se almacenan como (parent_id, idx, valor).
 *
 * Diferencias/ajustes para SQLite:
 *  - Tipos: bool -> INTEGER, int -> INTEGER, float -> REAL, resto -> TEXT.
 *  - 'Identificador' INTEGER PRIMARY KEY AUTOINCREMENT.
 *  - PRAGMA foreign_keys=ON.
 *  - 'loadFromArray' crea SIEMPRE una BD nueva (borra archivo si existe).
 */

// --- Clase auxiliar de definición de tabla (fuera de JsonSqliteBridge) ---
class TableDef {
    public string $name;
    public ?string $parent;   // nombre tabla padre o null
    public ?string $relname;  // campo en el padre que relaciona con esta tabla
    public string  $kind;     // 'dict' | 'list_scalar'
    public array   $columns = [];  // dict: col => tipo SQL
    public array   $children = []; // nombres de tablas hijas

    public function __construct(string $name, ?string $parent, ?string $relname, string $kind) {
        $this->name   = $name;
        $this->parent = $parent;
        $this->relname= $relname;
        $this->kind   = $kind;
    }
}

class JsonSqliteBridge
{
    // Estado de inferencia (para 'write')
    private array $tables = [];      // name -> TableDef
    private array $edges  = [];      // [ [parent, child], ... ]

    // ============ Helpers de nombre / tipos ============
    private static function ident(string $name): string {
        $name = trim(mb_strtolower($name));
        $name = preg_replace('/[^a-z0-9_]+/u', '_', $name);
        $name = preg_replace('/_+/', '_', $name);
        $name = trim($name, '_');
        if ($name === '') $name = 'col';
        if (preg_match('/^\d/', $name)) $name = 'n_' . $name;
        if (in_array($name, ['index','key','primary','value','table'])) $name = '_' . $name;
        return $name;
    }

    private static function joinPath(string ...$parts): string {
        $clean = array_filter(array_map([self::class, 'ident'], $parts), fn($p) => $p !== '');
        return self::ident(implode('_', $clean));
    }

    private static function sqlScalarType(mixed $v): string {
        if (is_bool($v))  return 'INTEGER';
        if (is_int($v))   return 'INTEGER';
        if (is_float($v)) return 'REAL';
        return 'TEXT';
    }

    private static function mergeType(string $a, string $b): string {
        if ($a === $b) return $a;
        $pair = [$a => true, $b => true];
        if (isset($pair['TEXT'])) return 'TEXT';
        if (isset($pair['INTEGER']) && isset($pair['REAL'])) return 'REAL';
        return 'TEXT';
    }

    // ============ Modelo de tabla ============
    private function ensureTable(string $name, ?string $parent = null, ?string $relname = null, string $kind='dict'): object {
        $tname = self::ident($name);
        if (!isset($this->tables[$tname])) {
            $this->tables[$tname] = new TableDef($tname, $parent, $relname, $kind);
        } else {
            if ($this->tables[$tname]->kind === 'list_scalar' && $kind === 'dict') {
                $this->tables[$tname]->kind = 'dict';
            }
        }
        if ($parent) {
            $p = self::ident($parent);
            $this->edges[] = [$p, $tname];
            if (!in_array($tname, $this->tables[$p]->children, true)) {
                $this->tables[$p]->children[] = $tname;
            }
        }
        return $this->tables[$tname];
    }

    // ============ Inferencia recursiva ============
    private function inferValue(string $pathTable, mixed $value, ?string $parentTable, ?string $relname): void {
        if (is_array($value) && self::isAssoc($value)) {
            // dict
            $t = $this->ensureTable($pathTable, $parentTable, $relname, 'dict');
            foreach ($value as $k => $v) {
                if (is_array($v) && (self::isAssoc($v) || count($v) > 0)) {
                    // dict o list
                    $this->inferValue(self::joinPath($pathTable, (string)$k), $v, $t->name, (string)$k);
                } else {
                    $col = self::ident((string)$k);
                    $tt = self::sqlScalarType($v);
                    $t->columns[$col] = isset($t->columns[$col]) ? self::mergeType($t->columns[$col], $tt) : $tt;
                }
            }
        } elseif (is_array($value)) {
            // list
            $elemKind = 'scalar';
            foreach ($value as $el) { $elemKind = (is_array($el) && self::isAssoc($el)) ? 'dict' : 'scalar'; break; }
            if ($elemKind === 'dict') {
                $t = $this->ensureTable($pathTable, $parentTable, $relname, 'dict');
                foreach ($value as $el) {
                    if (!is_array($el) || !self::isAssoc($el)) continue;
                    foreach ($el as $k => $v) {
                        if (is_array($v) && (self::isAssoc($v) || count($v) > 0)) {
                            $this->inferValue(self::joinPath($pathTable, (string)$k), $v, $t->name, (string)$k);
                        } else {
                            $col = self::ident((string)$k);
                            $tt = self::sqlScalarType($v);
                            $t->columns[$col] = isset($t->columns[$col]) ? self::mergeType($t->columns[$col], $tt) : $tt;
                        }
                    }
                }
            } else {
                $this->ensureTable($pathTable, $parentTable, $relname, 'list_scalar');
            }
        } else {
            // escalar en raíz => tabla con una columna 'valor'
            if ($parentTable === null) {
                $t = $this->ensureTable($pathTable, null, $relname, 'dict');
                $t->columns['valor'] = isset($t->columns['valor'])
                    ? self::mergeType($t->columns['valor'], self::sqlScalarType($value))
                    : self::sqlScalarType($value);
            }
        }
    }

    // ============ Topología ============
    private function topoTables(): array {
        $indeg = [];
        $graph = [];
        foreach ($this->edges as [$p, $c]) {
            $graph[$p] ??= [];
            $graph[$p][] = $c;
            $indeg[$c] = ($indeg[$c] ?? 0) + 1;
            $indeg[$p] = $indeg[$p] ?? 0;
        }
        foreach ($this->tables as $tname => $_) {
            $indeg[$tname] = $indeg[$tname] ?? 0;
        }
        $q = [];
        foreach ($indeg as $t => $d) if ($d === 0) $q[] = $t;
        $out = []; $seen = [];
        while ($q) {
            $u = array_shift($q);
            if (isset($seen[$u])) continue;
            $seen[$u] = true;
            $out[] = $u;
            foreach ($graph[$u] ?? [] as $v) {
                $indeg[$v]--;
                if ($indeg[$v] === 0) $q[] = $v;
            }
        }
        foreach ($this->tables as $t => $_) if (!isset($seen[$t])) $out[] = $t;
        return $out;
    }

    // ============ SQLite ============
    private static function newPdo(string $dbPath): PDO {
        $dsn = "sqlite:" . $dbPath;
        $pdo = new PDO($dsn);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $pdo->exec("PRAGMA foreign_keys = ON;");
        $pdo->exec("PRAGMA journal_mode = WAL;");
        $pdo->exec("PRAGMA synchronous = NORMAL;");
        return $pdo;
    }

    private static function resetDatabaseFile(string $dbPath): void {
        if (file_exists($dbPath)) {
            @unlink($dbPath);
        }
        // SQLite crea el archivo al abrir la conexión
    }

    // ============ DDL ============
    private function createAll(PDO $pdo): void {
        $order = $this->topoTables();

        // Eliminamos si existiera (por robustez en reintentos)
        foreach (array_reverse($order) as $t) {
            $pdo->exec("DROP TABLE IF EXISTS \"$t\";");
        }

        foreach ($order as $tname) {
            $t = $this->tables[$tname];

            $cols = ['"Identificador" INTEGER PRIMARY KEY AUTOINCREMENT'];
            if ($t->parent) {
                $cols[] = "\"{$t->parent}_id\" INTEGER NOT NULL";
            }
            if ($t->kind === 'dict') {
                foreach ($t->columns as $c => $typ) {
                    $cols[] = "\"".self::ident($c)."\" $typ";
                }
            } else {
                // list_scalar
                $cols[] = '"idx" INTEGER NOT NULL';
                $cols[] = '"valor" TEXT';
            }

            $fk = '';
            if ($t->parent) {
                $fk = " ,FOREIGN KEY (\"{$t->parent}_id\") REFERENCES \"{$t->parent}\"(\"Identificador\") ON DELETE CASCADE ON UPDATE CASCADE";
            }

            $ddl = "CREATE TABLE \"$tname\" ( ".implode(", ", $cols)." $fk );";
            $pdo->exec($ddl);

            // Índice para FK (recomendable)
            if ($t->parent) {
                $pdo->exec("CREATE INDEX IF NOT EXISTS \"idx_{$tname}_{$t->parent}_id\" ON \"$tname\" (\"{$t->parent}_id\");");
            }
        }
    }

    // ============ INSERT ============
    private function insertListScalar(PDO $pdo, TableDef $tdef, mixed $value, ?int $parentId): void {
        if (!is_array($value) || self::isAssoc($value)) $value = [$value];
        $sql = "INSERT INTO \"{$tdef->name}\" (\"{$tdef->parent}_id\",\"idx\",\"valor\") VALUES (?,?,?)";
        $stmt = $pdo->prepare($sql);
        $i = 0;
        foreach ($value as $el) {
            if (is_array($el)) {
                $val = json_encode($el, JSON_UNESCAPED_UNICODE);
            } else {
                $val = $el;
            }
            $stmt->execute([$parentId, $i, $val]);
            $i++;
        }
    }

    private function insertDictRow(PDO $pdo, TableDef $tdef, array $data, ?int $parentId): int {
        $cols = [];
        $vals = [];
        $place = [];

        foreach (array_keys($tdef->columns) as $c) {
            $cols[] = "\"".self::ident($c)."\"";
            $v = $data[$c] ?? null;
            if (is_array($v)) $v = null; // las estructuras anidadas van a tablas hijas
            $vals[] = $v;
            $place[] = '?';
        }
        if ($tdef->parent) {
            array_unshift($cols, "\"{$tdef->parent}_id\"");
            array_unshift($vals, $parentId);
            array_unshift($place, '?');
        }

        if (count($cols) > 0) {
            $sql = "INSERT INTO \"{$tdef->name}\" (".implode(",", $cols).") VALUES (".implode(",", $place).")";
            $stmt = $pdo->prepare($sql);
            $stmt->execute($vals);
        } else {
            // tabla sin columnas (salvo Identificador y posible FK)
            if ($tdef->parent) {
                $sql = "INSERT INTO \"{$tdef->name}\" (\"{$tdef->parent}_id\") VALUES (?)";
                $stmt = $pdo->prepare($sql);
                $stmt->execute([$parentId]);
            } else {
                $pdo->exec("INSERT INTO \"{$tdef->name}\" DEFAULT VALUES;");
            }
        }

        $newId = (int)$pdo->lastInsertId();

        // hijos
        foreach ($data as $k => $v) {
            if (!is_array($v) || (!self::isAssoc($v) && count($v) === 0)) {
                continue;
            }
            $childName = self::joinPath($tdef->name, (string)$k);
            $child = $this->tables[$childName] ?? null;
            if ($child === null) {
                if (self::isAssoc($v)) {
                    $child = $this->ensureTable($childName, $tdef->name, (string)$k, 'dict');
                    $this->insertDictRow($pdo, $child, [], $newId);
                }
                continue;
            }
            if ($child->kind === 'dict') {
                if (self::isAssoc($v)) {
                    $this->insertDictRow($pdo, $child, $v, $newId);
                } else {
                    foreach ($v as $el) {
                        if (is_array($el) && self::isAssoc($el)) {
                            $this->insertDictRow($pdo, $child, $el, $newId);
                        }
                    }
                }
            } else {
                $this->insertListScalar($pdo, $child, $v, $newId);
            }
        }
        return $newId;
    }

    // ============ API WRITE ============
    public function loadFromJsonFile(string $jsonPath, string $dbPath): bool {
        $root = json_decode(file_get_contents($jsonPath), true);
        if (!is_array($root) || !self::isAssoc($root)) {
            throw new InvalidArgumentException("El JSON raíz debe ser un objeto: cada clave es una tabla padre top-level.");
        }
        return $this->loadFromArray($root, $dbPath);
    }

    public function loadFromArray(array $root, string $dbPath): bool {
        if (!self::isAssoc($root)) {
            throw new InvalidArgumentException("El JSON raíz debe ser un objeto.");
        }

        // Inferencia
        $this->tables = [];
        $this->edges  = [];
        foreach ($root as $topKey => $topVal) {
            $topTable = self::ident((string)$topKey);
            if (is_array($topVal) && !self::isAssoc($topVal)) {
                foreach ($topVal as $el) {
                    $this->inferValue($topTable, $el, null, null);
                }
            } else {
                $this->inferValue($topTable, $topVal, null, null);
            }
        }

        // Nueva BD
        self::resetDatabaseFile($dbPath);
        $pdo = self::newPdo($dbPath);

        // Crear esquema
        $this->createAll($pdo);

        // Insertar datos
        $pdo->beginTransaction();
        try {
            foreach ($root as $topKey => $topVal) {
                /** @var TableDef $topTable */
                $topTable = $this->tables[self::ident((string)$topKey)];
                if (is_array($topVal) && !self::isAssoc($topVal)) {
                    foreach ($topVal as $el) {
                        $row = (is_array($el) && self::isAssoc($el)) ? $el : ['valor' => $el];
                        $this->insertDictRow($pdo, $topTable, $row, null);
                    }
                } elseif (is_array($topVal) && self::isAssoc($topVal)) {
                    $this->insertDictRow($pdo, $topTable, $topVal, null);
                } else {
                    $this->insertDictRow($pdo, $topTable, ['valor' => $topVal], null);
                }
            }
            $pdo->commit();
        } catch (Throwable $e) {
            $pdo->rollBack();
            throw $e;
        }

        return true;
    }

    // ============ API READ ============
    public function dumpToArray(string $dbPath): array {
        if (!file_exists($dbPath)) {
            throw new RuntimeException("No existe la base de datos: $dbPath");
        }
        $pdo = self::newPdo($dbPath);

        // Tablas
        $tables = [];
        $res = $pdo->query("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;");
        while ($row = $res->fetch(PDO::FETCH_ASSOC)) $tables[] = $row['name'];
        if (!$tables) throw new RuntimeException("No hay tablas en la base de datos.");

        // Columnas
        $tableColumns = [];
        foreach ($tables as $t) {
            $tableColumns[$t] = [];
            $stmt = $pdo->query("PRAGMA table_info(\"$t\");");
            while ($r = $stmt->fetch(PDO::FETCH_ASSOC)) {
                $tableColumns[$t][] = $r['name'];
            }
        }

        // FKs
        $parentOf = [];
        $fkColOfChild = [];
        $childrenOf = [];
        foreach ($tables as $t) {
            $childrenOf[$t] = $childrenOf[$t] ?? [];
        }
        foreach ($tables as $t) {
            $fk = $pdo->query("PRAGMA foreign_key_list(\"$t\");");
            while ($r = $fk->fetch(PDO::FETCH_ASSOC)) {
                $parent   = $r['table'];
                $childCol = $r['from'];   // p.ej. parent_id
                $parentOf[$t] = $parent;
                $fkColOfChild[$t] = $childCol;
                $childrenOf[$parent][] = $t;
            }
        }

        $rootTables = array_values(array_filter($tables, fn($t) => !isset($parentOf[$t])));

        // Todas las filas
        $allRows = [];
        foreach ($tables as $t) {
            $stmt = $pdo->query("SELECT * FROM \"$t\"");
            $allRows[$t] = $stmt->fetchAll(PDO::FETCH_ASSOC);
        }

        // Index por (child, parent_id)
        $childRowsByParent = [];
        foreach ($parentOf as $child => $parent) {
            $fk = $fkColOfChild[$child] ?? null;
            if (!$fk) continue;
            foreach ($allRows[$child] as $row) {
                $pid = $row[$fk] ?? null;
                if ($pid === null) continue;
                $key = $child."|".$pid;
                $childRowsByParent[$key] ??= [];
                $childRowsByParent[$key][] = $row;
            }
        }

        $buildNode = function(string $table, array $row) use (&$buildNode, $tableColumns, $fkColOfChild, $childrenOf, $childRowsByParent): array {
            $cols = $tableColumns[$table];
            $fkCol = $fkColOfChild[$table] ?? null;

            // columnas escalares (sin Identificador, idx, valor, ni FK)
            $scalarCols = [];
            foreach ($cols as $c) {
                if ($c === 'Identificador' || $c === 'idx' || $c === 'valor') continue;
                if ($fkCol !== null && $c === $fkCol) continue;
                $scalarCols[] = $c;
            }

            $node = [];
            foreach ($scalarCols as $c) {
                $node[$c] = $row[$c] ?? null;
            }

            foreach ($childrenOf[$table] ?? [] as $child) {
                $relField = self::childFieldName($table, $child);
                $childCols = array_flip($tableColumns[$child]);
                $key = $child."|".$row['Identificador'];
                $rowsChild = $childRowsByParent[$key] ?? [];
                if (!$rowsChild) continue;

                if (isset($childCols['idx']) && isset($childCols['valor'])) {
                    // list_scalar
                    usort($rowsChild, fn($a,$b) => ($a['idx'] ?? 0) <=> ($b['idx'] ?? 0));
                    $seq = [];
                    foreach ($rowsChild as $rc) $seq[] = $rc['valor'];
                    $node[$relField] = $seq;
                } else {
                    if (count($rowsChild) === 1) {
                        $node[$relField] = $buildNode($child, $rowsChild[0]);
                    } else {
                        $tmp = [];
                        foreach ($rowsChild as $rc) $tmp[] = $buildNode($child, $rc);
                        $node[$relField] = $tmp;
                    }
                }
            }
            return $node;
        };

        $result = [];
        foreach ($rootTables as $rt) {
            $rows = $allRows[$rt];
            usort($rows, fn($a,$b) => ((int)$a['Identificador']) <=> ((int)$b['Identificador']));
            $arr = [];
            foreach ($rows as $r) $arr[] = $buildNode($rt, $r);
            $result[$rt] = $arr;
        }

        return $result;
    }

    public function dumpToJsonFile(string $dbPath, string $outputPath): array {
        $arr = $this->dumpToArray($dbPath);
        file_put_contents($outputPath, json_encode($arr, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
        return $arr;
    }

    // ============ utils ============
    private static function isAssoc(array $a): bool {
        if ($a === []) return false; // tratamos [] como lista vacía
        return array_keys($a) !== range(0, count($a)-1);
    }

    private static function childFieldName(string $parent, string $child): string {
        $prefix = $parent . "_";
        if (function_exists('str_starts_with')) {
            if (str_starts_with($child, $prefix)) {
                return substr($child, strlen($prefix));
            }
        } else {
            if (substr($child, 0, strlen($prefix)) === $prefix) {
                return substr($child, strlen($prefix));
            }
        }
        return $child;
    }
}

