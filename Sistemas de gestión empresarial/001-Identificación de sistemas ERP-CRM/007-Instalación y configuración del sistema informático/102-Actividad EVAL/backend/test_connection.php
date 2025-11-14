<?php
// Script de prueba de conexión a la base de datos
require_once 'config/database.php';

echo "🔍 Probando conexión a la base de datos...\n\n";

try {
    echo "✅ Conexión establecida exitosamente\n";
    echo "📊 Base de datos: " . $dbname . "\n";
    echo "🏠 Host: " . $host . "\n";
    echo "👤 Usuario: " . $username . "\n\n";
    
    // Verificar si la tabla usuarios existe
    $stmt = $pdo->query("SHOW TABLES LIKE 'usuarios'");
    if ($stmt->rowCount() > 0) {
        echo "✅ Tabla 'usuarios' encontrada\n";
        
        // Verificar si existe el usuario admin
        $stmt = $pdo->prepare("SELECT username, nombre, email FROM usuarios WHERE username = 'admin'");
        $stmt->execute();
        $user = $stmt->fetch();
        
        if ($user) {
            echo "✅ Usuario admin encontrado:\n";
            echo "   - Username: " . $user['username'] . "\n";
            echo "   - Nombre: " . $user['nombre'] . "\n";
            echo "   - Email: " . $user['email'] . "\n";
            
            // Verificar el hash de la contraseña
            $stmt = $pdo->prepare("SELECT password FROM usuarios WHERE username = 'admin'");
            $stmt->execute();
            $hash = $stmt->fetchColumn();
            
            if (password_verify('admin123', $hash)) {
                echo "✅ Contraseña 'admin123' verificada correctamente\n";
            } else {
                echo "❌ La contraseña 'admin123' NO coincide con el hash almacenado\n";
                echo "🔧 Necesitas ejecutar el script fix_password.sql\n";
            }
        } else {
            echo "❌ Usuario admin NO encontrado\n";
        }
    } else {
        echo "❌ Tabla 'usuarios' NO encontrada\n";
        echo "🔧 Necesitas ejecutar el script erp_sistema.sql\n";
    }
    
} catch (PDOException $e) {
    echo "❌ Error de conexión: " . $e->getMessage() . "\n";
    echo "\n🔧 Posibles soluciones:\n";
    echo "1. Verificar que MySQL esté ejecutándose\n";
    echo "2. Verificar credenciales en config/database.php\n";
    echo "3. Verificar que la base de datos 'erp_sistema' existe\n";
}
?>