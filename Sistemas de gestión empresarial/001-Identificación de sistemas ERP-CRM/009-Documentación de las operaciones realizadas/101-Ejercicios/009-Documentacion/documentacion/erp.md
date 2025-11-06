📁..
   ├─ 📁anterior
   │  ├─ 📁cabecera
   │  │  ├─ 📄comportamiento.js
   │  │  ├─ 📄estilo.css
   │  │  └─ 📄index.php
   │  ├─ 📁comun
   │  │  ├─ 📄estilo.css
   │  │  ├─ 📄Ubuntu-B.ttf
   │  │  └─ 📄Ubuntu-R.ttf
   │  ├─ 📁crm
   │  │  ├─ 📄comportamiento.js
   │  │  ├─ 📄estilo.css
   │  │  └─ 📄index.php
   │  ├─ 📁escritorio
   │  │  ├─ 📄comportamiento.js
   │  │  ├─ 📄estilo.css
   │  │  └─ 📄index.html
   │  ├─ 📁iniciarsesion
   │  │  ├─ 📄comportamiento.js
   │  │  ├─ 📄estilo.css
   │  │  └─ 📄index.html
   │  ├─ 📁listadodemodulos
   │  │  ├─ 📄comportamiento.js
   │  │  ├─ 📄estilo.css
   │  │  └─ 📄index.php
   │  ├─ 📁plantillas
   │  │  ├─ 📁calendario
   │  │  ├─ 📁fichas
   │  │  ├─ 📁formulario
   │  │  ├─ 📁grafica
   │  │  ├─ 📁kanban
   │  │  │  ├─ 📄comportamiento.js
   │  │  │  ├─ 📄estilo.css
   │  │  │  ├─ 📄index.php
   │  │  │  └─ 📄kanban.json
   │  │  └─ 📁lista
   │  └─ 📄index.php
   ├─ 📁basededatos
   │  └─ 📄instalacion.sql
   ├─ 📁documentacion
   │  ├─ 📁__pycache__
   │  │  ├─ 📄arbol.cpython-312.pyc
   │  │  ├─ 📄cabeceras.cpython-312.pyc
   │  │  ├─ 📄cabeceras_stream.cpython-312.pyc
   │  │  └─ 📄docai.cpython-312.pyc
   │  ├─ 📄arbol.py
   │  ├─ 📄cabeceras.py
   │  ├─ 📄cabeceras_stream.py
   │  ├─ 📄docai.py
   │  ├─ 📄documentacion.py
   │  └─ 📄erp.md
   ├─ 📁instalador
   │  └─ 📄index.php
   └─ 📁posterior
      ├─ 📁data
      │  └─ 📄kanban.sqlite
      ├─ 📄config.php
      ├─ 📄data_1757686436.json
      ├─ 📄iniciarsesion.php
      ├─ 📄kanban.php
      ├─ 📄listadodemodulos.php
      └─ 📄savekanban.php
# ..
## anterior

- [index.php](anterior/index.php)

    ### Explicación del archivo `index.php`
    
    Este archivo es el punto de entrada principal para la aplicación ERP Jose Vicente. Su objetivo es verificar si el usuario ha iniciado sesión y, en caso afirmativo, mostrar la interfaz principal de la aplicación.
    
    #### Papel dentro del proyecto global
    
    - **Autenticación**: Verifica si el usuario ha iniciado sesión.
    - **Redirección**: Si no está autenticado, redirige al usuario a la página de inicio de sesión.
    - **Interfaz Principal**: Muestra la interfaz principal de la aplicación si el usuario está autenticado.
    
    #### Dependencias y relaciones con otros archivos
    
    1. **`session_start()`**:
       - Inicia una nueva sesión o reanuda una sesión existente.
    
    2. **Verificación de Sesión**:
       - Verifica si la variable `$_SESSION['usuario']` está definida.
       - Si no está definida, redirige al usuario a la página de inicio de sesión (`iniciarsesion/index.html`) y termina el script con `exit`.
    
    3. **Inclusión de Archivos**:
       - Incluye el archivo de cabecera (`cabecera/index.php`).
       - Comenta la inclusión del archivo de listado de módulos (`listadodemodulos/index.php`).
       - Incluye el archivo de plantilla Kanban (`plantillas/kanban/index.php`).
    
    #### Resumen
    
    - **Funcionalidad**: Verifica la autenticación del usuario y muestra la interfaz principal.
    - **Dependencias**:
      - `session_start()`
      - Archivos de cabecera, listado de módulos y plantilla Kanban.
    
    Este archivo es crucial para controlar el acceso a la aplicación y asegurar que solo los usuarios autenticados puedan ver su contenido.

    ```php
    <?php
  session_start();
  if(!isset($_SESSION['usuario'])){
    header("Location: iniciarsesion/index.html");
    exit;
  }
?>
<!doctype html>
<html lang="es">
  <head>
    <title>ERP Jose Vicente</title>
    <meta charset="utf-8">
    <link rel="stylesheet" href="comun/estilo.css">
  </head>
  <body>
    <?php include "cabecera/index.php" ?>
    <?php /*include "listadodemodulos/index.php"*/ ?>
    <?php include "plantillas/kanban/index.php" ?>
  </body>
</html>

    ```
### cabecera

- [comportamiento.js](anterior/cabecera/comportamiento.js)
- [estilo.css](anterior/cabecera/estilo.css)

    > ⚠️ Error llamando a Ollama: timed out

    ```css
    #superior{
  background:var(--solido-fondo);
  padding:20px;
  color:var(--solido-frente);
  font-weight:bold;
  display:flex;
  justify-content: space-between;
}
#inferior{
  background:white;
  padding:20px;
  color:black;
  font-weight:bold;
  display:flex;
  justify-content: space-between;
  border-bottom:1px solid var(--solido-fondo);
}
#inferior nav{
  display:flex;
}

    ```
- [index.php](anterior/cabecera/index.php)

    > ⚠️ Error llamando a Ollama: timed out

    ```php
    <!-- Módulo cabecera -->

<style>
  <?php include "estilo.css";?>
</style>

<div>
  <header id="superior">
    <nav>
       ☰ Aplicaciones Aplicaciones
    </nav>
    <nav>
      💬 ⏰ JOCARSA A
    </nav>
  </header>
  <header id="inferior">
    <nav>
      Aplicaciones
    </nav>
    <nav>
      <input type="search">
    </nav>
    <nav>
      <div>X de Y</div>
      <div id="paginacion">
      ⏪⏩
      </div>
      <div id="vista">
        🪟​🪟​
      </div>
    </nav>
   </div>
</div>

<script>
  <?php include "comportamiento.js";?>
</script>

<!-- Módulo cabecera -->

    ```
### comun

- [estilo.css](anterior/comun/estilo.css)
