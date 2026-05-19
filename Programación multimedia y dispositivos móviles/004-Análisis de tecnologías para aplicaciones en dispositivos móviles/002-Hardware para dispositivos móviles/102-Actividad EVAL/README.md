# 🎵 TAMEify - Plataforma de Música para Móviles

## 📋 Descripción del Proyecto

TAMEify es una aplicación web para dispositivos móviles que simula una plataforma de streaming de música. Permite a los usuarios visualizar sus artistas favoritos, navegar entre diferentes pantallas y gestionar su biblioteca musical.

## ✨ Características Implementadas

### 1. 📡 Carga de Datos desde API
- **Función fetch**: Se utiliza para cargar los datos de artistas favoritos desde `api/favoritos.json`
- **Variable global**: Los datos se almacenan en `datosFavoritos` para su uso posterior
- **Manejo de errores**: Incluye gestión de errores con `catch()` y mensajes informativos

### 2. 🎨 Despliegue Dinámico de Lista
- **Sistema de plantillas**: Usa `<template>` para crear elementos reutilizables
- **Clonación de nodos**: Cada artista se genera clonando la plantilla con `cloneNode(true)`
- **Personalización**: Los datos (imagen y nombre) se reemplazan dinámicamente
- **Grid responsivo**: Layout adaptativo con CSS Grid

### 3. 🖱️ Manejo de Eventos
- **Click en artistas**: Cada elemento tiene un evento onclick asignado
- **Navegación entre pantallas**: Alterna entre pantalla inicial y pantalla de lista
- **Interactividad**: Efectos hover y transiciones suaves

### 4. 📱 Diseño Mobile-First
- **Viewport optimizado**: Meta tag configurado para dispositivos móviles
- **Interfaz táctil**: Botones grandes y áreas clicables amplias
- **Footer fijo**: Navegación inferior siempre accesible

## 🗂️ Estructura del Proyecto

```
102-Actividad EVAL/
├── index.html          # Archivo principal de la aplicación
└── README.md          # Documentación del proyecto
```

## 🚀 Cómo Ejecutar

1. Abre el archivo `index.html` en un navegador web
2. Para mejor experiencia móvil, abre las DevTools (F12) y activa el modo dispositivo móvil
3. La aplicación cargará automáticamente los datos de favoritos

## 💻 Tecnologías Utilizadas

- **HTML5**: Estructura semántica y templates
- **CSS3**: Estilos modernos, Grid Layout, Flexbox, transiciones
- **JavaScript (ES6)**: Fetch API, manipulación del DOM, eventos

## 📖 Conceptos Aplicados

### Fetch API
```javascript
fetch("../101-Ejercicios/api/favoritos.json")
  .then(respuesta => respuesta.json())
  .then(datos => {
    // Procesar datos
  })
  .catch(error => {
    // Manejar errores
  });
```

### Clonación de Plantillas
```javascript
let plantilla = document.querySelector("#elemento_lista");
let instancia = plantilla.content.cloneNode(true);
```

### Event Handlers
```javascript
articulo.onclick = function() {
  mostrarPantallaLista(dato);
};
```

## 🎯 Objetivos Cumplidos

- ✅ **Carga de datos**: Fetch implementado correctamente con manejo de promesas
- ✅ **Despliegue dinámico**: Bucle forEach que recorre y renderiza cada artista
- ✅ **Eventos click**: Navegación funcional entre pantallas
- ✅ **Plantillas HTML**: Sistema de templates para elementos reutilizables
- ✅ **Diseño responsive**: Adaptado para dispositivos móviles

## 🔄 Flujo de la Aplicación

1. **Carga inicial**: La página carga y muestra un mensaje "Cargando..."
2. **Fetch de datos**: Se obtienen los artistas desde la API
3. **Renderizado**: Cada artista se muestra en una tarjeta con imagen y nombre
4. **Interacción**: Al hacer click en un artista, se muestra su pantalla de detalle
5. **Navegación**: El usuario puede volver al inicio con el botón "Volver"

## 🎨 Diseño Visual

- **Tema oscuro**: Fondo negro (#121212) para mejor visualización
- **Colores de acento**: Magenta para botones principales
- **Efectos hover**: Transformaciones y sombras en elementos interactivos
- **Gradientes**: Reproductor con gradiente rojo oscuro

## 🔮 Mejoras Futuras

- 🎵 Integración con API real de música (Spotify, Deezer)
- ▶️ Reproductor de audio funcional
- 💾 Almacenamiento local de favoritos
- 🔍 Funcionalidad de búsqueda
- 📱 Progressive Web App (PWA)
- 🎨 Temas personalizables (claro/oscuro)

## 📚 Referencias

- Basado en los ejercicios de la carpeta `101-Ejercicios`
- Documentación MDN Web Docs: Fetch API, Templates, DOM Manipulation

## 👨‍💻 Autor

Proyecto desarrollado como actividad evaluable para el módulo de **Programación Multimedia y Dispositivos Móviles** - DAM-2

---

**Fecha**: Febrero 2026  
**Versión**: 1.0.0
