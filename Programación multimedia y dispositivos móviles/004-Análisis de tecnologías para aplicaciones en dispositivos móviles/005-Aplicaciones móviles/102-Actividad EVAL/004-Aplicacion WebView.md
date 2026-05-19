# Aplicación WebView en Android Studio

## Objetivo
Crear una aplicación Android que cargue y muestre páginas web utilizando el componente WebView.

## Enunciado paso a paso

### 1. Descarga e instala Android Studio

- Visita https://developer.android.com/studio?hl=es-419
- Sigue los pasos para descargar e instalar Android Studio en tu computadora

### 2. Crea un nuevo proyecto de aplicación web

- Abre Android Studio
- Crea un nuevo proyecto "Empty Activity"
- **Nombre del proyecto**: AplicacionWeb
- **Nombre del paquete**: com.jocarsa.aplicacionweb

### 3. Desarrolla la interfaz gráfica de usuario

Abre el archivo `activity_main.xml` ubicado en `app/src/main/res/layout/`

Añade un componente WebView con el siguiente código XML:

```xml
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:id="@+id/main"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <WebView
        android:id="@+id/mivistaweb"
        android:layout_width="0dp"
        android:layout_height="0dp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
```

**Explicación del layout:**
- Se utiliza `ConstraintLayout` como contenedor principal
- El `WebView` ocupa todo el espacio disponible (0dp en ancho y alto con constraints a todos los lados)
- Se le asigna el ID `mivistaweb` para poder referenciarlo desde el código Kotlin

### 4. Implementa el controlador de la aplicación

Abre el archivo `MainActivity.kt` ubicado en `app/src/main/java/com/jocarsa/aplicacionweb/`

Añade el siguiente código para configurar y cargar una página web en el WebView:

```kotlin
package com.jocarsa.aplicacionweb

import android.os.Bundle
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val webView = findViewById<WebView>(R.id.mivistaweb)
        webView.webViewClient = WebViewClient()
        webView.settings.javaScriptEnabled = true
        webView.loadUrl("https://jocarsa.com")
    }
}
```

**Explicación del código:**
- `findViewById<WebView>(R.id.mivistaweb)`: Obtiene la referencia al WebView del layout
- `webViewClient = WebViewClient()`: Hace que los enlaces se abran dentro del WebView en lugar del navegador externo
- `settings.javaScriptEnabled = true`: Habilita la ejecución de JavaScript en las páginas web
- `loadUrl("https://jocarsa.com")`: Carga la URL especificada

### 5. Configura los permisos necesarios

Abre el archivo `AndroidManifest.xml` ubicado en `app/src/main/`

Añade el permiso de Internet antes de la etiqueta `<application>`:

```xml
<uses-permission android:name="android.permission.INTERNET" />
```

### 6. Prueba la aplicación

- Conecta un dispositivo Android o abre el emulador de Android Studio
- Ejecuta la aplicación (botón Run o Shift+F10)
- Verifica que se cargue correctamente la página web https://jocarsa.com en el WebView

## Conceptos clave

### WebView
Componente que permite mostrar contenido web dentro de una aplicación Android.

### WebViewClient
Clase que gestiona eventos del WebView, como la navegación entre páginas.

### JavaScript Enabled
Permite que el WebView ejecute código JavaScript de las páginas web cargadas.

## Restricciones

- No utilices librerías externas ni estructuras no vistas en esta actividad
- Mantén el código dentro de los límites del contenido impartido

## Posibles extensiones

- Añadir una barra de progreso mientras carga la página
- Implementar botones de navegación (atrás, adelante, recargar)
- Gestionar el botón de retroceso del dispositivo
- Añadir control de errores de conexión
