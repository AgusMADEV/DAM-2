# 🚀 Guía de Instalación - TotalKit ERP

## 📋 Requisitos del Sistema

- **PHP**: Versión 7.4 o superior
- **MySQL**: Versión 5.7 o superior
- **Servidor Web**: Apache (XAMPP recomendado)
- **Navegador**: Chrome, Firefox, Edge o Safari (versiones recientes)

## 🔧 Instalación Paso a Paso

### Paso 1: Preparar el Servidor

#### Si usas XAMPP:
1. Descargar e instalar [XAMPP](https://www.apachefriends.org/)
2. Iniciar **Apache** y **MySQL** desde el panel de control de XAMPP
3. Verificar que funcionan abriendo: `http://localhost/`

### Paso 2: Crear la Base de Datos

1. Abrir **phpMyAdmin**: `http://localhost/phpmyadmin/`
2. Hacer clic en "Nueva" en el panel izquierdo
3. Nombre de la base de datos: `tienda_camisetas`
4. Cotejamiento: `utf8mb4_unicode_ci`
5. Hacer clic en "Crear"

### Paso 3: Importar la Estructura

1. Seleccionar la base de datos `tienda_camisetas` recién creada
2. Ir a la pestaña "Importar"
3. Hacer clic en "Seleccionar archivo"
4. Buscar y seleccionar el archivo `base_datos.sql`
5. Hacer clic en "Continuar" al final de la página
6. Esperar a que termine la importación

✅ **Verificación**: Deberías ver 17 tablas creadas y 3 vistas

### Paso 4: Configurar el Proyecto

1. Copiar todos los archivos del proyecto a la carpeta de XAMPP:
   - **Windows**: `C:\xampp\htdocs\totalkit\`
   - **Mac**: `/Applications/XAMPP/htdocs/totalkit/`
   - **Linux**: `/opt/lampp/htdocs/totalkit/`

2. Abrir el archivo `index.php` con un editor de texto

3. Verificar/modificar las credenciales de base de datos (líneas 7-10):
   ```php
   $db_host = "localhost";        // Normalmente no cambia
   $db_name = "tienda_camisetas"; // Nombre que pusiste en Paso 2
   $db_user = "root";             // Usuario MySQL (normalmente "root")
   $db_pass = "";                 // Contraseña MySQL (vacía por defecto)
   ```

4. Guardar el archivo

### Paso 5: Acceder al Sistema

1. Abrir el navegador web
2. Ir a: `http://localhost/totalkit/`
3. Deberías ver la pantalla de login con tema verde (fútbol)

### Paso 6: Iniciar Sesión

Usar las credenciales por defecto:
- **Usuario**: `admin`
- **Contraseña**: `admin123`

¡Listo! Ya estás dentro del sistema TotalKit ERP ⚽🎉

## 🎨 Estructura de Archivos

```
totalkit/
│
├── index.php           ← Archivo principal del sistema
├── estilos.css        ← Hoja de estilos (tema verde césped)
├── base_datos.sql     ← Script de base de datos
├── README.md          ← Documentación completa
├── ejercicio.md       ← Resumen del ejercicio
└── INSTALACION.md     ← Este archivo
```

## 🔍 Solución de Problemas

### Error: "No se puede conectar a la base de datos"

**Posibles causas y soluciones:**

1. **MySQL no está iniciado**
   - Abrir panel de control XAMPP
   - Hacer clic en "Start" junto a MySQL
   - Esperar a que el botón se ponga verde

2. **Credenciales incorrectas**
   - Verificar usuario y contraseña en `index.php`
   - Por defecto en XAMPP: usuario `root`, contraseña vacía

3. **Base de datos no existe**
   - Ir a phpMyAdmin
   - Verificar que existe `tienda_camisetas`
   - Si no existe, repetir Paso 2

### Error: "Página en blanco" o "Error 500"

**Posibles causas:**

1. **Error de sintaxis PHP**
   - Verificar que no se modificó accidentalmente el código
   - Ver errores en: `C:\xampp\apache\logs\error.log`

2. **PHP no está iniciado**
   - Verificar que Apache esté corriendo en XAMPP
   - Reiniciar Apache si es necesario

### Error: "No se encuentran las tablas"

**Solución:**
- La importación del SQL falló
- Repetir Paso 3 completo
- Verificar que el archivo `base_datos.sql` no está corrupto
- Asegurarse que seleccionaste la base de datos `tienda_camisetas` antes de importar

### Los estilos no se cargan (página sin colores verdes)

**Verificaciones:**
1. El archivo `estilos.css` está en la misma carpeta que `index.php`
2. El nombre del archivo es exactamente `estilos.css` (minúsculas)
3. Refrescar página con Ctrl+F5 (fuerza recarga de CSS)

### Error al insertar productos (foreign key)

**Solución:**
- Asegúrate de crear primero:
  1. Equipos
  2. Marcas
  3. Temporadas
  4. Tallas
  5. Tipos de camiseta
- Los productos dependen de estas tablas

## 📱 Acceso desde Otros Dispositivos

Para acceder desde un móvil o tablet en la misma red:

1. Averiguar la IP de tu computadora:
   - Windows: `ipconfig` en cmd
   - Mac/Linux: `ifconfig` en terminal

2. En el dispositivo móvil, abrir navegador y ir a:
   `http://[TU_IP]/totalkit/`
   
   Ejemplo: `http://192.168.1.100/totalkit/`

## 🔒 Cambiar Credenciales de Login

Para mayor seguridad, modifica el usuario y contraseña en `index.php` (líneas 13-14):

```php
$usuario_valido = "tunombredeusuario";
$contrasena_valida = "tucontraseñasegura";
```

## 💾 Backup de Datos

### Exportar base de datos:
1. Ir a phpMyAdmin
2. Seleccionar `tienda_camisetas`
3. Clic en "Exportar"
4. Clic en "Continuar"
5. Se descargará un archivo `.sql`

### Restaurar desde backup:
1. Seguir Paso 3 de instalación
2. Usar el archivo de backup en lugar de `base_datos.sql`

## 🎓 Datos de Prueba Incluidos

El sistema viene con datos reales de ejemplo:

**16 Equipos:**
- Real Madrid, FC Barcelona, Atlético Madrid (LaLiga)
- Manchester United, Liverpool, Manchester City (Premier League)
- AC Milan, Inter Milan, Juventus (Serie A)
- Bayern München, Borussia Dortmund (Bundesliga)
- Paris Saint-Germain (Ligue 1)
- España, Brasil, Argentina, Portugal (Selecciones)

**18 Camisetas:**
- Primera, segunda y tercera equipación
- Versiones con jugadores (Bellingham #5, Lewandowski #9, Messi #10)
- Múltiples tallas (S, M, L)
- Temporadas actuales (2024/25, 2025/26)

**Otros datos:**
- 4 clientes con equipo favorito
- 3 pedidos completados
- 5 reseñas de productos
- 8 marcas deportivas (Nike, Adidas, Puma, etc.)
- 5 temporadas
- 6 tallas (XS a XXL)
- 6 tipos de camiseta

Puedes modificar, eliminar o agregar más datos desde el panel del sistema.

## 🚀 Siguientes Pasos

Una vez instalado exitosamente:

1. **Explorar el Dashboard**: Ver estadísticas de camisetas
2. **Revisar Equipos**: Ver equipos de LaLiga, Premier League, etc.
3. **Probar CRUD**: Insertar nuevas camisetas, clientes, etc.
4. **Revisar Pedidos**: Ver flujo de pedidos de camisetas
5. **Analizar el Código**: Estudiar cómo funciona el sistema
6. **Personalizar**: Cambiar colores, añadir más equipos

## 💡 Consejos Útiles

### Para añadir nuevas camisetas:
1. Primero asegúrate de tener el equipo creado
2. Ten marca, temporada, talla y tipo de camiseta
3. Completa todos los campos requeridos
4. Usa códigos de producto únicos (ej: RM-2425-H-M)

### Para personalizar camisetas con jugador:
1. Marca el campo `version_jugador` como 1
2. Ingresa el nombre del jugador en MAYÚSCULAS
3. Ingresa el número de dorsal
4. Ajusta el precio (versión jugador es +30€ aprox)

### Para gestionar stock:
1. Crea el mismo producto en múltiples tallas
2. Usa códigos diferentes por talla (ej: RM-2425-H-S, RM-2425-H-M)
3. Controla el stock independientemente por talla

## 📞 Ayuda Adicional

Si encuentras problemas no listados aquí:

1. Revisar `README.md` para documentación completa
2. Verificar logs de error de Apache
3. Consultar documentación de XAMPP
4. Revisar permisos de carpetas (en Linux/Mac)
5. Verificar versiones de PHP y MySQL

## 🏆 Equipos Populares por Agregar

Si quieres añadir más equipos:

**LaLiga:**
- Sevilla FC, Valencia CF, Real Sociedad, Athletic Bilbao

**Premier League:**
- Arsenal, Chelsea, Tottenham, Newcastle United

**Serie A:**
- AS Roma, Napoli, Lazio, Atalanta

**Bundesliga:**
- RB Leipzig, Bayer Leverkusen, Eintracht Frankfurt

**Otras Ligas:**
- Ajax (Países Bajos)
- Benfica, Porto (Portugal)
- Celtic, Rangers (Escocia)

**Selecciones:**
- Francia, Alemania, Italia, Inglaterra, Países Bajos, Bélgica

---

**¡Disfruta gestionando tu tienda de camisetas de fútbol! ⚽👕🏆**

_Sistema desarrollado como ejercicio de SGE - DAM 2º_
_Febrero 2026_
