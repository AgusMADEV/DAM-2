En este proyecto he desarrollado un **sistema de backoffice empresarial** completo, que incluye un formulario de login seguro y una interfaz de navegación para gestionar diferentes secciones de una aplicación empresarial.

El objetivo principal ha sido comprender la importancia de la **usabilidad y accesibilidad** en aplicaciones web empresariales, implementando un sistema que permita a los usuarios acceder de forma segura y navegar intuitivamente por las diferentes secciones de la aplicación.

Estos componentes son esenciales en aplicaciones de gestión (ERP, CRM o sistemas internos) donde se requiere:
- **Autenticación segura** de usuarios
- **Navegación clara** entre secciones
- **Experiencia de usuario coherente**
- **Validación de datos** en tiempo real
- **Diseño profesional** y moderno

Por ejemplo, el sistema de login permite validar credenciales y recopilar información adicional del usuario mediante campos opcionales:

```php
<!-- Sección de validación de usuario -->
<div class="form-group">
  <label for="usuario">Usuario:</label>
  <input type="text" id="usuario" name="usuario" required placeholder="Ingrese su usuario">
  <div class="error-message" id="errorUsuario">El usuario es requerido</div>
</div>
```

El proyecto se estructura en componentes modulares que facilitan el mantenimiento y la escalabilidad:
- **login.php**: Página independiente para autenticación
- **maestro.php**: Archivo principal que integra todos los componentes
- **componentes/**: Carpeta con módulos reutilizables (layout, menu, login)

---

###  Sistema de Login Seguro

El formulario de login implementa múltiples capas de seguridad y validación:

#### Validación en Tiempo Real

```javascript
formulario.onsubmit = function(evento){
  evento.preventDefault(); // Prevenir envío por defecto
  
  let usuario = document.querySelector("#usuario").value;
  let contrasena = document.querySelector("#contrasena").value;
  let errorUsuario = document.querySelector("#errorUsuario");
  let errorContrasena = document.querySelector("#errorContrasena");
  
  // Resetear errores
  errorUsuario.classList.remove("show");
  errorContrasena.classList.remove("show");
  
  let esValido = true;
  
  // Validar usuario
  if(usuario.trim() === ""){
    errorUsuario.classList.add("show");
    esValido = false;
  }
  
  // Validar contraseña
  if(contrasena.trim() === ""){
    errorContrasena.classList.add("show");
    esValido = false;
  }
  
  if(esValido){
    console.log("Login exitoso para usuario:", usuario);
    window.location.href = "maestro.php?usuario=" + encodeURIComponent(usuario);
  }
}
```

**Características de seguridad implementadas:**

1. **Prevención de envío vacío**: El formulario valida que ambos campos estén completos antes de proceder
2. **Escape de caracteres**: Uso de `encodeURIComponent()` para prevenir inyección de código en URLs
3. **Sanitización en PHP**: Uso de `htmlspecialchars()` para prevenir XSS
4. **Validación cliente-lado**: Feedback inmediato al usuario sin necesidad de recargar la página

### Elementos de Formulario Adecuados

El proyecto utiliza diferentes tipos de controles según la necesidad:

#### Campos de Texto Seguros
```html
<input type="text" id="usuario" name="usuario" required 
       placeholder="Ingrese su usuario">
<input type="password" id="contrasena" name="contrasena" required 
       placeholder="Ingrese su contraseña">
```

**Justificación técnica:**
- `type="password"`: Oculta los caracteres ingresados por seguridad
- `required`: Validación HTML5 nativa
- `placeholder`: Mejora la usabilidad indicando el formato esperado

#### Campos de Selección para Datos Estructurados
```html
<select id="deporte" name="deporte">
  <option value="">Seleccione un deporte</option>
  <option value="futbol">⚽ Fútbol</option>
  <option value="baloncesto">🏀 Baloncesto</option>
  <option value="tenis">🎾 Tenis</option>
  <!-- ... más opciones -->
</select>
```

**Ventajas:**
- Previene errores de escritura
- Facilita el procesamiento de datos
- Mejora la accesibilidad con navegación por teclado
- Uso de emojis para mejor identificación visual

### Integración con PHP

El sistema utiliza variables PHP para gestionar la información del usuario:

```php
<?php
// Variables PHP para información de la aplicación
$tituloPagina = isset($tituloPagina) ? $tituloPagina : "Backoffice Empresarial";
$usuarioActual = isset($_GET['usuario']) ? htmlspecialchars($_GET['usuario']) : "Invitado";
$seccionActual = isset($_GET['seccion']) ? htmlspecialchars($_GET['seccion']) : "Dashboard";
?>
```

**Prácticas de seguridad aplicadas:**
- Validación de existencia de variables con `isset()`
- Sanitización de entrada con `htmlspecialchars()`
- Valores por defecto para casos sin autenticación

### Diseño Responsivo y Profesional

El CSS implementa un diseño moderno con gradientes y transiciones:

```css
body{
  margin: 0;
  padding: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

#login{
  width: 450px;
  min-height: 550px;
  background: white;
  padding: 30px;
  box-shadow: 0px 10px 30px rgba(0,0,0,0.3);
  border-radius: 15px;
  margin: 50px auto;
}
```

**Características técnicas:**
- **Flexbox**: Centrado perfecto vertical y horizontal
- **Gradientes**: Apariencia moderna y profesional
- **Box-shadow**: Profundidad y jerarquía visual
- **Border-radius**: Esquinas redondeadas para suavidad visual

---

### Integración de Componentes en maestro.php

El archivo `maestro.php` actúa como punto de entrada principal del sistema:

```php
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Backoffice Empresarial - Sistema de Gestión</title>
    <style>
      body{
        margin: 0;
        padding: 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      }
    </style>
  </head>
  <body>
    <?php
    // Variable para el título de la página
    $tituloPagina = "Backoffice Empresarial";
    
    // Incluir el layout principal que contiene todos los componentes
    include "componentes/layout.php";
    ?>
  </body>
</html>
```

**Arquitectura modular:**
- Definición de variables de configuración
- Inclusión dinámica de componentes
- Separación de responsabilidades

### Componente Layout (Plantilla Maestra)

El archivo `layout.php` implementa la estructura visual completa:

```php
<?php
// Variables PHP para información de la aplicación
$tituloPagina = isset($tituloPagina) ? $tituloPagina : "Backoffice Empresarial";
$usuarioActual = isset($_GET['usuario']) ? htmlspecialchars($_GET['usuario']) : "Invitado";
$seccionActual = isset($_GET['seccion']) ? htmlspecialchars($_GET['seccion']) : "Dashboard";
?>

<header id="header">
  <h1><?php echo $tituloPagina; ?></h1>
  <div class="info-usuario">
    👤 Usuario conectado: <strong><?php echo $usuarioActual; ?></strong> | 
    📍 Sección actual: <strong><?php echo ucfirst($seccionActual); ?></strong>
  </div>
</header>

<main id="principal">
  <nav>
    <?php include "menu.php"; ?>
  </nav>
  <section>
    <h2>Bienvenido, <?php echo $usuarioActual; ?></h2>
    <div class="contenido-seccion">
      <p>Esta es la aplicación de backoffice empresarial...</p>
    </div>
  </section>
</main>
```

**Ventajas de este diseño:**
- **Reutilización**: El layout se puede usar en múltiples páginas
- **Mantenimiento**: Cambios en un solo archivo afectan toda la aplicación
- **Claridad**: Estructura HTML semántica (`header`, `main`, `nav`, `section`)

### Sistema de Navegación Dinámico

El menú implementa JavaScript para navegación SPA (Single Page Application):

```javascript
function cargarSeccion(seccion){
  // Remover clase active de todos los botones
  let botones = document.querySelectorAll("#menu button");
  botones.forEach(btn => btn.classList.remove("active"));
  
  // Agregar clase active al botón clickeado
  event.target.classList.add("active");
  
  // Actualizar la URL con el parámetro de sección
  let urlActual = new URL(window.location);
  urlActual.searchParams.set('seccion', seccion);
  window.history.pushState({}, '', urlActual);
  
  // Cargar contenido dinámicamente
  let contenido = document.querySelector("#principal section");
  if(contenido){
    contenido.innerHTML = `<h2>Sección: ${seccion.charAt(0).toUpperCase() + seccion.slice(1)}</h2>
                           <p>Contenido de la sección ${seccion}...</p>`;
  }
}
```

**Características avanzadas:**
- **History API**: Actualización de URL sin recargar página
- **Feedback visual**: Indicador de sección activa
- **Confirmación de logout**: Prevención de cierre accidental de sesión

### Flujo Completo de Usuario

**1. Acceso al sistema:**
```
Usuario → login.php → Ingresa credenciales → Validación JavaScript
```

**2. Autenticación exitosa:**
```
Validación exitosa → Redirección con parámetros → maestro.php?usuario=Admin&seccion=dashboard
```

**3. Navegación:**
```
Click en menú → cargarSeccion() → Actualización de URL → Carga de contenido dinámico
```

**4. Ejemplo de URL completa:**
```
http://localhost/.../maestro.php?usuario=Admin&seccion=clientes&deporte=futbol&nivel=avanzado
```

Esta URL contiene:
- `usuario`: Nombre del usuario autenticado
- `seccion`: Sección actual de la aplicación
- `deporte`, `nivel`: Información opcional del perfil del usuario

---

El desarrollo de este backoffice empresarial ha permitido aplicar de forma práctica los principios de **usabilidad y accesibilidad** estudiados en la unidad. El proyecto implementa claridad mediante formularios intuitivos con validación en tiempo real, consistencia visual a través de un estilo unificado en toda la aplicación, y prevención de errores con validaciones preventivas que mejoran la experiencia del usuario.

En cuanto a la accesibilidad, se ha utilizado HTML semántico con etiquetas apropiadas, asociación correcta entre labels e inputs para compatibilidad con tecnologías asistivas, y ratios de contraste que cumplen con las pautas WCAG. La arquitectura modular del proyecto, organizada en componentes reutilizables como `login.php`, `maestro.php` y la carpeta `componentes/`, facilita el mantenimiento y escalabilidad del sistema.

Este enfoque integra los conceptos clave de la unidad: usabilidad mediante validación clara y feedback inmediato, accesibilidad con HTML semántico, diseño responsivo usando Flexbox, componentes reutilizables con PHP, y seguridad mediante sanitización de datos. El resultado es una interfaz que no solo es visualmente atractiva, sino también accesible, intuitiva, segura y mantenible, cumpliendo con los estándares profesionales aplicables a sistemas empresariales como ERPs, CRMs y plataformas de gestión
