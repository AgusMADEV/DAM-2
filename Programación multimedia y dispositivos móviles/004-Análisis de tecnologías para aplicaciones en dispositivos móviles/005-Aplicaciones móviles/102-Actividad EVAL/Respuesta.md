Android Studio es el entorno de desarrollo integrado (IDE) oficial para el desarrollo de aplicaciones Android, proporcionado por Google. Su importancia radica en que ofrece todas las herramientas necesarias para crear, depurar y compilar aplicaciones móviles de manera eficiente.

En el contexto de aplicaciones web, Android Studio permite crear proyectos que integran contenido web dentro de aplicaciones nativas mediante el componente **WebView**. Este componente es fundamental porque:

- Permite mostrar contenido web sin necesidad de abrir un navegador externo
- Facilita la integración de tecnologías web (HTML, CSS, JavaScript) en aplicaciones Android
- Proporciona control sobre la experiencia de usuario al mantener al usuario dentro de la aplicación
- Es ideal para aplicaciones híbridas que combinan componentes nativos con contenido web

La creación de un proyecto de aplicación web en Android Studio sigue un flujo estructurado que incluye la configuración inicial del proyecto, el diseño de la interfaz mediante XML, la implementación de la lógica en Kotlin, y la configuración de permisos necesarios como el acceso a Internet.

---

### Configuración del WebView en XML

El componente WebView se configura en el archivo `activity_main.xml` utilizando **ConstraintLayout** como contenedor principal:

```xml
<WebView
    android:id="@+id/mivistaweb"
    android:layout_width="0dp"
    android:layout_height="0dp"
    app:layout_constraintBottom_toBottomOf="parent"
    app:layout_constraintEnd_toEndOf="parent"
    app:layout_constraintStart_toStartOf="parent"
    app:layout_constraintTop_toTopOf="parent" />
```

**Aspectos técnicos clave:**
- **ID único** (`android:id="@+id/mivistaweb"`): Permite referenciar el componente desde Kotlin
- **Dimensiones con constraints** (`0dp`): El WebView se adapta al espacio disponible según las restricciones definidas
- **Constraints a los cuatro lados**: Garantiza que el WebView ocupe toda la pantalla

### Configuración del comportamiento en Kotlin

En `MainActivity.kt`, se implementa la lógica para controlar el WebView:

```kotlin
val webView = findViewById<WebView>(R.id.mivistaweb)
webView.webViewClient = WebViewClient()
webView.settings.javaScriptEnabled = true
webView.loadUrl("https://jocarsa.com")
```

**Explicación técnica:**

1. **`findViewById<WebView>(R.id.mivistaweb)`**: Obtiene la referencia al componente del layout mediante su ID
2. **`webViewClient = WebViewClient()`**: Asigna un cliente que intercepta eventos de navegación, haciendo que los enlaces se abran dentro del WebView en lugar del navegador del sistema
3. **`settings.javaScriptEnabled = true`**: Habilita la ejecución de JavaScript, necesario para la mayoría de sitios web modernos
4. **`loadUrl("https://jocarsa.com")`**: Carga la URL especificada en el WebView

### Configuración de permisos

Es imprescindible añadir el permiso de Internet en `AndroidManifest.xml`:

```xml
<uses-permission android:name="android.permission.INTERNET" />
```

Sin este permiso, la aplicación no podrá realizar conexiones de red y fallará al intentar cargar contenido web.

---

### Implementación realizada

He desarrollado la aplicación **AplicacionWeb** siguiendo los pasos indicados:

**Paso 1: Creación del proyecto**
- Proyecto creado con nombre: `AplicacionWeb`
- Paquete: `com.jocarsa.aplicacionweb`
- Tipo: Empty Activity

**Paso 2: Diseño de la interfaz**
- Modificado `activity_main.xml` para incluir el WebView
- El componente ocupa toda la pantalla disponible
- Se ha asignado el ID `mivistaweb` para su posterior referencia

**Paso 3: Implementación del controlador**
- Configurado el WebViewClient para mantener la navegación dentro de la app
- Habilitado JavaScript para compatibilidad con sitios web modernos
- Cargada la URL https://jocarsa.com

**Paso 4: Configuración de permisos**
- Añadido el permiso INTERNET en el AndroidManifest

### Verificación del funcionamiento

**Pruebas realizadas:**

1. **Carga inicial**: La aplicación inicia correctamente y carga la página web especificada
2. **Visualización**: El contenido web se muestra correctamente a pantalla completa
3. **JavaScript**: Las funcionalidades interactivas del sitio web funcionan correctamente
4. **Navegación interna**: Al hacer clic en enlaces, la navegación se mantiene dentro de la aplicación

**Resultado:** La aplicación funciona correctamente, mostrando el contenido web de forma fluida y sin necesidad de abrir navegadores externos.

### Capturas de evidencia

- ✓ Aplicación compilada sin errores
- ✓ WebView carga correctamente la URL
- ✓ JavaScript funciona adecuadamente
- ✓ Navegación contenida dentro de la aplicación

## 4. Cierre/Conclusión enlazando con la unidad

Esta actividad ha permitido consolidar conocimientos fundamentales sobre el desarrollo de aplicaciones móviles en Android:

### Conocimientos reforzados

1. **Integración de contenido web en aplicaciones nativas**: El WebView es un componente esencial para crear aplicaciones híbridas que combinan la potencia de las tecnologías web con las capacidades nativas de Android.

2. **Arquitectura de aplicaciones Android**: Se ha practicado la separación entre la vista (XML) y el controlador (Kotlin), siguiendo el patrón arquitectónico fundamental de Android.

3. **Gestión de permisos**: Se ha comprendido la importancia de declarar permisos en el AndroidManifest para acceder a funcionalidades del sistema como Internet.

4. **Configuración de componentes**: Se ha aprendido a configurar tanto aspectos visuales (layout XML) como comportamentales (Kotlin) de los componentes Android.

### Aplicación en proyectos prácticos

Los conocimientos adquiridos son aplicables en múltiples escenarios reales:

- **Aplicaciones de noticias**: Mostrar contenido web de portales informativos
- **Sistemas de documentación**: Integrar manuales o ayudas en formato web
- **Aplicaciones empresariales**: Mostrar paneles de control web dentro de apps corporativas
- **Contenido dinámico**: Cargar contenido que se actualiza frecuentemente sin necesidad de actualizar la app

### Conexión con la unidad didáctica

Esta práctica se enmarca dentro del análisis de tecnologías para aplicaciones en dispositivos móviles, específicamente en el estudio de **aplicaciones híbridas** que combinan:

- Tecnologías nativas (Android SDK, Kotlin)
- Tecnologías web (HTML, CSS, JavaScript)
- Componentes de integración (WebView)

El WebView representa un puente fundamental entre el desarrollo web y el desarrollo móvil nativo, permitiendo aprovechar contenido web existente dentro de aplicaciones Android, optimizando así el desarrollo y mantenimiento de aplicaciones multiplataforma.

### Próximos pasos

Los conocimientos adquiridos sientan las bases para:
- Implementar comunicación bidireccional entre JavaScript y Kotlin
- Crear aplicaciones híbridas más complejas
- Optimizar el rendimiento de WebViews
- Implementar cacheo de contenido web
- Gestionar estados de carga y errores de red

---

**Conclusión final**: Esta actividad ha demostrado cómo Android Studio facilita la creación de aplicaciones que integran contenido web, proporcionando las herramientas necesarias para desarrollar soluciones híbridas eficientes y funcionales que responden a necesidades reales del mercado de aplicaciones móviles.
