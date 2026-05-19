# Actividad de Evaluación: Aplicación WebView

## Descripción

Desarrollar una aplicación Android que utilice el componente WebView para cargar y mostrar contenido web dentro de la aplicación.

## Objetivos de aprendizaje

1. Crear un proyecto Android desde cero
2. Diseñar interfaces de usuario con XML
3. Implementar controladores en Kotlin
4. Configurar permisos en el AndroidManifest
5. Trabajar con el componente WebView

## Requisitos del proyecto

### Requisitos funcionales

1. La aplicación debe cargar una página web específica al iniciar
2. El contenido web debe mostrarse a pantalla completa
3. La navegación debe ocurrir dentro de la aplicación (no abrir navegador externo)
4. Debe soportar JavaScript

### Especificaciones técnicas

- **Nombre del proyecto**: AplicacionWeb
- **Nombre del paquete**: com.jocarsa.aplicacionweb
- **URL a cargar**: https://jocarsa.com
- **Tipo de Activity**: Empty Activity
- **Componente principal**: WebView

## Estructura del proyecto

```
AplicacionWeb/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/jocarsa/aplicacionweb/
│   │   │   │   └── MainActivity.kt
│   │   │   ├── res/
│   │   │   │   └── layout/
│   │   │   │       └── activity_main.xml
│   │   │   └── AndroidManifest.xml
```

## Tareas a realizar

### Tarea 1: Configuración inicial (10 puntos)
- Descargar e instalar Android Studio
- Crear el proyecto con las especificaciones indicadas
- Configurar el entorno de desarrollo

### Tarea 2: Diseño de la interfaz (30 puntos)
- Modificar `activity_main.xml`
- Añadir el componente WebView con ID `mivistaweb`
- Configurar el layout para que ocupe toda la pantalla

### Tarea 3: Implementación del controlador (40 puntos)
- Modificar `MainActivity.kt`
- Obtener la referencia al WebView
- Configurar WebViewClient
- Habilitar JavaScript
- Cargar la URL especificada

### Tarea 4: Configuración de permisos (10 puntos)
- Añadir el permiso de Internet en el AndroidManifest

### Tarea 5: Pruebas y verificación (10 puntos)
- Ejecutar la aplicación en emulador o dispositivo físico
- Verificar que la página se carga correctamente
- Comprobar que la navegación funciona dentro de la app

## Criterios de evaluación

| Criterio | Puntos | Descripción |
|----------|--------|-------------|
| Configuración del proyecto | 10 | Proyecto creado con nombre y paquete correctos |
| Layout XML | 30 | WebView correctamente configurado en el layout |
| Código Kotlin | 40 | MainActivity implementada correctamente |
| Permisos | 10 | AndroidManifest con permisos necesarios |
| Funcionalidad | 10 | La aplicación funciona correctamente |
| **TOTAL** | **100** | |

## Entregables

1. Código fuente completo del proyecto
2. Captura de pantalla de la aplicación en funcionamiento
3. Archivo APK compilado (opcional)

## Restricciones

- **NO** utilices librerías externas
- **NO** implementes funcionalidades no especificadas en este documento
- Mantén el código simple y legible
- Usa únicamente los conceptos vistos en clase

## Plazo de entrega

Consultar con el profesor.

## Recursos adicionales

- Documentación oficial de Android: https://developer.android.com/
- Guía de WebView: https://developer.android.com/guide/webapps/webview

## Notas importantes

- Asegúrate de probar la aplicación antes de entregarla
- El código debe estar correctamente indentado
- Incluye comentarios explicativos en las partes clave del código
- Verifica que tienes conexión a Internet al probar la aplicación

## Criterios de calidad del código

- **Legibilidad**: El código debe ser fácil de leer y entender
- **Organización**: Estructura clara y ordenada
- **Nomenclatura**: Nombres de variables y funciones descriptivos
- **Funcionamiento**: La aplicación debe ejecutarse sin errores

## Solución de problemas comunes

### La aplicación se cierra al iniciar
- Verifica que has añadido el permiso de Internet en el AndroidManifest

### No se carga la página web
- Comprueba tu conexión a Internet
- Verifica que la URL es correcta

### Los enlaces abren el navegador externo
- Asegúrate de configurar el WebViewClient

### La página no se ve bien
- Verifica que JavaScript está habilitado
- Comprueba que el WebView ocupa toda la pantalla
