# 🚀 INICIO RÁPIDO - Agente IA Autónomo

## Pasos para Ejecutar (5 minutos)

### 1️⃣ Iniciar Servicios de XAMPP
```
- Abrir XAMPP Control Panel
- Iniciar Apache
- Iniciar MySQL
```

### 2️⃣ Crear Base de Datos
```
Opción A - Desde phpMyAdmin:
  1. Ir a http://localhost/phpmyadmin
  2. Crear nueva base de datos: "agente_ia_autonomo"
  3. Seleccionar la base de datos
  4. Ir a pestaña "Importar"
  5. Seleccionar archivo: database/schema.sql
  6. Hacer clic en "Continuar"

Opción B - Desde terminal:
  mysql -u root -p < database/schema.sql
```

### 3️⃣ Verificar Instalación
```
Abrir en navegador:
http://localhost/003-Agente%20IA/101-Ejercicios/setup.php

Debe mostrar todos los checks en verde ✓
```

### 4️⃣ Acceder a la Aplicación
```
Abrir en navegador:
http://localhost/003-Agente%20IA/101-Ejercicios/

¡Listo! Ya puedes crear y ejecutar misiones
```

## 📝 Crear Tu Primera Misión

1. Hacer clic en "Nueva Misión"
2. Rellenar formulario:
   - **Título**: "Sistema de Login"
   - **Descripción**: "Crear autenticación de usuarios"
   - **Objetivo**: "Implementar login con PHP, MySQL, validaciones y seguridad"
   - **Prioridad**: Alta
3. Hacer clic en "Crear Misión"
4. En la lista, hacer clic en "Ejecutar"
5. Ver el progreso en tiempo real

## ⚙️ Configuración Opcional

### Para usar IA Real (OpenAI):
Editar `config/config.php`:
```php
define('AI_API_KEY', 'tu-api-key-aqui');
```

### Sin API Key:
El sistema funciona en "modo simulación" - perfecto para desarrollo y testing.

## 🐛 Solución de Problemas

### Error "Base de datos no encontrada"
→ Ejecutar el paso 2 (crear base de datos)

### Los estilos no se cargan
→ Verificar que la ruta sea correcta en el navegador
→ Limpiar caché del navegador (Ctrl+F5)

### Error de conexión
→ Verificar que MySQL esté corriendo en XAMPP
→ Revisar usuario/contraseña en config/database.php

## 📚 Siguiente Paso

Lee el archivo `README.md` para documentación completa del proyecto.

---

**¿Todo funcionando?** ¡Perfecto! Ahora explora el dashboard, crea misiones y observa cómo el agente trabaja de forma autónoma. 🤖✨
