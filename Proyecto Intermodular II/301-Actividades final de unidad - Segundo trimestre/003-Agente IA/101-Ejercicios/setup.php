<?php
/**
 * Script de instalación/setup del Agente IA Autónomo
 * Ejecutar una sola vez después de la instalación inicial
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);

?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instalación - Agente IA Autónomo</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 800px;
            width: 100%;
            padding: 40px;
        }
        h1 {
            color: #6366f1;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #64748b;
            margin-bottom: 30px;
        }
        .section {
            margin-bottom: 30px;
            padding: 20px;
            background: #f8fafc;
            border-radius: 8px;
            border-left: 4px solid #6366f1;
        }
        .section h2 {
            font-size: 18px;
            margin-bottom: 15px;
            color: #0f172a;
        }
        .check-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px;
            margin-bottom: 8px;
            background: white;
            border-radius: 6px;
        }
        .check-icon {
            font-size: 20px;
        }
        .success { color: #10b981; }
        .error { color: #ef4444; }
        .warning { color: #f59e0b; }
        .btn {
            display: inline-block;
            padding: 12px 24px;
            background: #6366f1;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
            font-size: 16px;
        }
        .btn:hover {
            background: #4f46e5;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
        }
        .btn-secondary {
            background: #64748b;
        }
        .btn-secondary:hover {
            background: #475569;
        }
        code {
            background: #1e293b;
            color: #10b981;
            padding: 2px 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }
        .alert {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .alert-success {
            background: #d1fae5;
            color: #065f46;
            border-left: 4px solid #10b981;
        }
        .alert-error {
            background: #fee2e2;
            color: #991b1b;
            border-left: 4px solid #ef4444;
        }
        .alert-warning {
            background: #fef3c7;
            color: #92400e;
            border-left: 4px solid #f59e0b;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Instalación del Agente IA Autónomo</h1>
        <p class="subtitle">Verificación del sistema y configuración inicial</p>

        <?php
        $errors = [];
        $warnings = [];
        $success = [];

        // 1. Verificar versión de PHP
        echo '<div class="section">';
        echo '<h2>1. Requisitos del Sistema</h2>';
        
        $phpVersion = phpversion();
        if (version_compare($phpVersion, '8.0.0', '>=')) {
            echo '<div class="check-item"><span class="check-icon success">✓</span> PHP ' . $phpVersion . ' (OK)</div>';
            $success[] = 'PHP version correcta';
        } else {
            echo '<div class="check-item"><span class="check-icon error">✗</span> PHP ' . $phpVersion . ' (Se requiere 8.0+)</div>';
            $errors[] = 'Versión de PHP insuficiente';
        }

        // 2. Verificar extensiones necesarias
        $extensiones = ['pdo', 'pdo_mysql', 'json', 'curl', 'mbstring'];
        foreach ($extensiones as $ext) {
            if (extension_loaded($ext)) {
                echo '<div class="check-item"><span class="check-icon success">✓</span> Extensión ' . $ext . ' (OK)</div>';
            } else {
                echo '<div class="check-item"><span class="check-icon error">✗</span> Extensión ' . $ext . ' (No disponible)</div>';
                $errors[] = 'Falta la extensión ' . $ext;
            }
        }

        echo '</div>';

        // 3. Verificar conexión a base de datos
        echo '<div class="section">';
        echo '<h2>2. Conexión a Base de Datos</h2>';
        
        try {
            require_once __DIR__ . '/config/database.php';
            $db = Database::getInstance()->getConnection();
            echo '<div class="check-item"><span class="check-icon success">✓</span> Conexión a MySQL establecida</div>';
            
            // Verificar tablas
            $tables = ['misiones', 'iteraciones', 'decisiones', 'artefactos', 'logs_agente', 'conocimiento', 'configuracion'];
            $stmt = $db->query("SHOW TABLES");
            $existingTables = $stmt->fetchAll(PDO::FETCH_COLUMN);
            
            $allTablesExist = true;
            foreach ($tables as $table) {
                if (in_array($table, $existingTables)) {
                    echo '<div class="check-item"><span class="check-icon success">✓</span> Tabla ' . $table . ' existe</div>';
                } else {
                    echo '<div class="check-item"><span class="check-icon error">✗</span> Tabla ' . $table . ' no existe</div>';
                    $allTablesExist = false;
                }
            }
            
            if (!$allTablesExist) {
                echo '<div class="alert alert-warning" style="margin-top: 15px;">';
                echo '<strong>⚠️ Acción Requerida:</strong> Ejecuta el script SQL:<br>';
                echo '<code>mysql -u root -p < database/schema.sql</code>';
                echo '</div>';
                $warnings[] = 'Faltan tablas en la base de datos';
            }
            
        } catch (Exception $e) {
            echo '<div class="check-item"><span class="check-icon error">✗</span> Error: ' . $e->getMessage() . '</div>';
            echo '<div class="alert alert-error" style="margin-top: 15px;">';
            echo '<strong>Error de conexión:</strong> Verifica la configuración en <code>config/database.php</code>';
            echo '</div>';
            $errors[] = 'No se puede conectar a la base de datos';
        }
        
        echo '</div>';

        // 4. Verificar permisos de escritura
        echo '<div class="section">';
        echo '<h2>3. Permisos de Archivos</h2>';
        
        $dirs = [
            __DIR__ . '/logs',
            __DIR__ . '/output',
            __DIR__ . '/temp'
        ];
        
        foreach ($dirs as $dir) {
            if (is_dir($dir) && is_writable($dir)) {
                echo '<div class="check-item"><span class="check-icon success">✓</span> ' . basename($dir) . '/ tiene permisos de escritura</div>';
            } else {
                if (!is_dir($dir)) {
                    mkdir($dir, 0755, true);
                    echo '<div class="check-item"><span class="check-icon success">✓</span> Directorio ' . basename($dir) . '/ creado</div>';
                } else {
                    echo '<div class="check-item"><span class="check-icon warning">⚠</span> ' . basename($dir) . '/ sin permisos de escritura</div>';
                    $warnings[] = 'Permisos insuficientes en ' . basename($dir);
                }
            }
        }
        
        echo '</div>';

        // 5. Verificar configuración de IA
        echo '<div class="section">';
        echo '<h2>4. Configuración de IA</h2>';
        
        require_once __DIR__ . '/config/config.php';
        
        if (!empty(AI_API_KEY)) {
            echo '<div class="check-item"><span class="check-icon success">✓</span> API Key configurada</div>';
            echo '<div class="check-item"><span class="check-icon success">✓</span> Modelo: ' . AI_MODEL . '</div>';
        } else {
            echo '<div class="check-item"><span class="check-icon warning">⚠</span> API Key no configurada</div>';
            echo '<div class="alert alert-warning" style="margin-top: 15px;">';
            echo '<strong>Modo Simulación:</strong> El agente funcionará en modo simulación sin IA real.<br>';
            echo 'Para usar una IA real, configura <code>AI_API_KEY</code> en <code>config/config.php</code>';
            echo '</div>';
            $warnings[] = 'API Key no configurada (modo simulación)';
        }
        
        echo '</div>';

        // Resumen final
        echo '<div class="section">';
        echo '<h2>📊 Resumen de la Instalación</h2>';
        
        if (empty($errors) && empty($warnings)) {
            echo '<div class="alert alert-success">';
            echo '<strong>✅ ¡Todo listo!</strong> El sistema está correctamente configurado y listo para usarse.';
            echo '</div>';
            echo '<a href="index.html" class="btn">Ir al Panel de Control</a>';
        } elseif (!empty($errors)) {
            echo '<div class="alert alert-error">';
            echo '<strong>❌ Errores encontrados:</strong><ul style="margin: 10px 0 0 20px;">';
            foreach ($errors as $error) {
                echo '<li>' . $error . '</li>';
            }
            echo '</ul></div>';
            echo '<button class="btn btn-secondary" onclick="location.reload()">Recargar y Verificar</button>';
        } else {
            echo '<div class="alert alert-warning">';
            echo '<strong>⚠️ Advertencias:</strong><ul style="margin: 10px 0 0 20px;">';
            foreach ($warnings as $warning) {
                echo '<li>' . $warning . '</li>';
            }
            echo '</ul></div>';
            echo '<a href="index.html" class="btn">Continuar de Todas Formas</a> ';
            echo '<button class="btn btn-secondary" onclick="location.reload()">Recargar y Verificar</button>';
        }
        
        echo '</div>';
        ?>

        <div style="margin-top: 30px; padding-top: 30px; border-top: 2px solid #e2e8f0; color: #64748b; font-size: 14px;">
            <strong>💡 Ayuda:</strong> Si encuentras problemas, consulta el archivo <code>README.md</code> o revisa los logs en <code>logs/</code>
        </div>
    </div>
</body>
</html>
