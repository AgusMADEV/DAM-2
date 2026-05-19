<div align="center">

# 🍳 FoodieHub Mobile

**Aplicación móvil de recetas • Mobile-first SPA**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-000?logo=flask)](https://flask.palletsprojects.com)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)](https://sqlite.org)
[![JavaScript](https://img.shields.io/badge/JavaScript-Vanilla-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

_Plataforma de gestión de recetas optimizada para dispositivos móviles con navegación animada_

</div>

---

## 📋 Índice

- [Descripción](#-descripción)
- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Arquitectura](#-arquitectura)
- [API REST](#-api-rest)
- [Mejoras Implementadas](#-mejoras-implementadas)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Autor](#-autor)

---

## 🎯 Descripción

**FoodieHub Mobile** es una aplicación web móvil desarrollada como proyecto de la asignatura **Programación Multimedia y Dispositivos Móviles (PMDM)**. La aplicación permite explorar, buscar y guardar recetas de cocina favoritas, implementando un diseño mobile-first con navegación fluida y animada.

El proyecto demuestra competencias en:
- ✅ Desarrollo de aplicaciones web móviles con tecnologías web
- ✅ Diseño responsive y mobile-first
- ✅ Framework de navegación personalizado con transiciones animadas
- ✅ Gestión de estado y persistencia de datos
- ✅ Integración frontend-backend con API REST
- ✅ Experiencia de usuario optimizada para dispositivos táctiles

---

## ✨ Características

### Funcionalidades Core

| Módulo | Descripción |
|--------|-------------|
| 🏠 **Inicio** | Pantalla de bienvenida con autenticación, categorías y recetas destacadas |
| 🔍 **Explorar** | Catálogo completo de recetas con búsqueda y filtros por dificultad |
| 📚 **Biblioteca** | Gestión de favoritos, estadísticas y ranking de usuarios |
| 👤 **Autenticación** | Registro e inicio de sesión con nombre y DNI |
| ❤️ **Favoritos** | Sistema de favoritos persistente en base de datos |
| 📱 **Mobile-First** | Diseño optimizado para pantallas ≤430px |
| 🎨 **Temas** | Modo claro y oscuro con persistencia en localStorage |
| 🔔 **Notificaciones** | Sistema de toast notifications con 4 variantes |

### Base de Datos

- **5 categorías**: Desayunos, Comidas, Postres, Ensaladas, Bebidas
- **13 recetas** pre-cargadas con ingredientes detallados
- **3 niveles de dificultad**: Fácil, Media, Difícil
- **Información completa**: Tiempo de preparación, ingredientes, categoría

---

## 🛠 Tecnologías

### Backend
- **Python 3.10+**
- **Flask 3.x** - Framework web
- **SQLite3** - Base de datos embebida

### Frontend
- **HTML5** - Estructura semántica
- **CSS3** - Design System con variables CSS
- **Vanilla JavaScript** - Sin frameworks, código puro

### Características Técnicas
- **SPA (Single Page Application)** - Navegación sin recargas
- **REST API** - Comunicación cliente-servidor
- **Mobile-First Design** - Prioridad en dispositivos móviles
- **Responsive** - Adaptable a diferentes tamaños de pantalla

---

## 📦 Instalación

### Requisitos
- Python 3.10 o superior
- pip (gestor de paquetes de Python)

### Pasos

1. **Clonar o descargar el proyecto**
   ```bash
   cd FoodieHub-Mobile
   ```

2. **Crear entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install flask
   ```

4. **Iniciar la aplicación**
   ```bash
   python app.py
   ```

5. **Abrir en el navegador**
   ```
   http://localhost:5091
   ```

---

## 🚀 Uso

### Primera Ejecución

1. La aplicación creará automáticamente la base de datos SQLite
2. Se cargarán 13 recetas de ejemplo en 5 categorías
3. Accede desde tu navegador (mejor en modo móvil)

### Navegación

#### Pantalla de Inicio
- **Registrarse**: Introduce tu nombre y DNI para iniciar sesión
- **Explorar categorías**: Visualiza las 5 categorías disponibles
- **Recetas destacadas**: Ver las 3 primeras recetas

#### Pantalla de Explorar
- **Buscar**: Filtra recetas por nombre, descripción o categoría
- **Filtrar por dificultad**: Fácil, Media, Difícil
- **Ver receta**: Abre el modal con detalles completos
- **Añadir a favoritos**: Marca tus recetas preferidas

#### Pantalla de Biblioteca
- **Favoritos**: Visualiza tus recetas guardadas
- **Estadísticas**: Métricas de la aplicación en tiempo real
- **Ranking**: Top 10 usuarios por favoritos y sesiones
- **Gestión de datos**: Seed, Export, Import

### Atajos de Teclado

| Tecla | Acción |
|-------|--------|
| `1` | Ir a Inicio |
| `2` | Ir a Explorar |
| `3` | Ir a Biblioteca |
| `Esc` | Cerrar modal |

### Gestos Táctiles

- **Swipe horizontal**: Desliza entre pantallas
  - ← Swipe izquierda: Siguiente pantalla
  - → Swipe derecha: Pantalla anterior

---

## 🏗 Arquitectura

```
┌──────────────────────────────────────────────┐
│           FRONTEND (SPA)                     │
│   index.html + app.js + styles.css           │
│                                              │
│   ┌────────┐  ┌─────────┐  ┌──────────┐    │
│   │ Inicio │  │ Explorar│  │ Biblioteca│    │
│   └────┬───┘  └────┬────┘  └─────┬────┘    │
│        └───────────┼──────────────┘          │
│              fetch() / JSON                  │
├────────────────────┼──────────────────────────┤
│           BACKEND (Flask)                    │
│          app.py · Port 5091                  │
│                                              │
│   ┌────────────────┼──────────────────┐     │
│   │  /api/users    │  /api/recipes    │     │
│   │  /api/sessions │  /api/favorites  │     │
│   │  /api/events   │  /api/stats      │     │
│   │  /api/categories /api/leaderboard │     │
│   └────────────────┼──────────────────┘     │
│                                              │
│         SQLite (file-based)                  │
│      foodiehub_mobile.sqlite3                │
└──────────────────────────────────────────────┘
```

---

## 📡 API REST

### Usuarios
- `POST /api/users/register` - Registrar/login usuario
- `POST /api/sessions/start` - Iniciar sesión de usuario
- `POST /api/sessions/<id>/end` - Finalizar sesión

### Recetas y Categorías
- `GET /api/categories` - Listar todas las categorías
- `GET /api/recipes` - Listar todas las recetas

### Favoritos
- `GET /api/favorites?userId=<id>` - Obtener favoritos de un usuario
- `POST /api/favorites/toggle` - Añadir/quitar favorito

### Estadísticas
- `GET /api/stats` - Métricas generales
- `GET /api/leaderboard` - Top 10 usuarios

### Eventos
- `POST /api/events` - Registrar evento de telemetría

### Gestión de Datos
- `POST /api/seed` - Cargar datos de prueba
- `GET /api/export` - Exportar base de datos a JSON
- `POST /api/import` - Importar datos desde JSON

---

## 🎨 Mejoras Implementadas

### ✅ 12 Mejoras Avanzadas

| # | Mejora | Descripción |
|---|--------|-------------|
| 1 | 🎨 **Design System v2** | Variables CSS completas (colores, radios, sombras, transiciones) |
| 2 | 🔔 **Toast Notifications** | 4 variantes (ok/info/warning/danger), auto-dismiss 3s |
| 3 | 🌓 **Toggle Dark/Light** | Temas persistentes con localStorage |
| 4 | 🟢 **Status LED** | Indicador animado de sesión activa con pulse |
| 5 | 🎭 **Recipe Modal** | Modal deslizante con detalles completos e ingredientes |
| 6 | 👆 **Swipe Navigation** | Gestos táctiles horizontales entre pantallas |
| 7 | 🔍 **Búsqueda Avanzada** | Filtrado en tiempo real por título, descripción y categoría |
| 8 | 🥇 **Rank Badges** | Medallas oro/plata/bronce para top 3 del ranking |
| 9 | 💊 **Active Chips** | Filtros de dificultad con estado activo visual |
| 10 | 🔴 **Badge Counts** | Contadores en tabs (recetas en Explorar, favoritos en Biblioteca) |
| 11 | ⌨️ **Keyboard Shortcuts** | Navegación rápida con teclas 1/2/3, Esc |
| 12 | 🌱 **Data Management** | Seed, Export/Import JSON para gestión completa de datos |

### Características Adicionales

- ✅ **Empty States** - Mensajes cuando no hay contenido
- ✅ **Responsive 480px+** - Adaptación a tablets
- ✅ **Smooth Animations** - Transiciones fluidas con cubic-bezier
- ✅ **Color-coded Difficulty** - Verde (Fácil), Amarillo (Media), Rojo (Difícil)
- ✅ **Session Tracking** - Telemetría de eventos y uso
- ✅ **Persistent Favorites** - Guardado en base de datos

---

## 📂 Estructura del Proyecto

```
FoodieHub-Mobile/
│
├── app.py                          # Backend Flask + API REST
├── requirements.txt                # Dependencias Python
├── .gitignore                      # Archivos ignorados por Git
├── README.md                       # Documentación del proyecto
│
├── templates/
│   └── index.html                  # HTML principal de la SPA
│
├── static/
│   ├── styles.css                  # Design System CSS
│   └── app.js                      # JavaScript del frontend
│
└── foodiehub_mobile.sqlite3        # Base de datos (auto-generada)
```

---

## 🎓 Contexto Académico

### Asignatura
**Programación Multimedia y Dispositivos Móviles (PMDM)**  
Ciclo Formativo de Grado Superior - Desarrollo de Aplicaciones Multiplataforma (DAM)

### Objetivos Cumplidos

✅ **Desarrollo móvil con tecnologías web**  
✅ **Framework de navegación personalizado**  
✅ **Diseño mobile-first responsive**  
✅ **Integración frontend-backend**  
✅ **Persistencia de datos**  
✅ **Gestión de estado compleja**  
✅ **Optimización para dispositivos táctiles**  
✅ **Animaciones y transiciones fluidas**

### Competencias Desarrolladas

1. **Técnicas**: HTML5, CSS3, JavaScript ES6+, Python, Flask, SQLite
2. **Diseño**: Mobile-first, Design Systems, UX/UI
3. **Arquitectura**: REST API, SPA, MVC
4. **Buenas prácticas**: Código limpio, comentarios, organización

---

## 🌟 Diferencias con el Proyecto de Clase

### Proyecto de Clase (PodWave)
- 🎧 Aplicación de podcasts estilo Spotify
- Reproductores de audio
- Canales y episodios
- Moods (Focus/Build/Calm)

### Este Proyecto (FoodieHub)
- 🍳 **Aplicación de recetas de cocina**
- 🗂️ **Categorías de comida** (Desayunos, Comidas, Postres, etc.)
- 📝 **Ingredientes y preparación**
- ⏱️ **Niveles de dificultad** (Fácil, Media, Difícil)
- 🎭 **Modal de detalles** completo con ingredientes
- 🍽️ **Temática gastronómica** completamente diferente

Aunque ambos proyectos comparten conceptos técnicos (navegación, favoritos, búsqueda), **FoodieHub es una aplicación completamente original** con temática, datos y funcionalidades propias.

---

## 👨‍💻 Autor

**Proyecto desarrollado para PMDM**  
2º DAM - Desarrollo de Aplicaciones Multiplataforma

---

## 📄 Licencia

Este proyecto es de uso educativo para la asignatura PMDM.

---

## 🚀 Próximas Mejoras (Opcional)

- [ ] Añadir categoría de ingredientes
- [ ] Sistema de valoraciones por estrellas
- [ ] Comentarios en recetas
- [ ] Subir fotos de platos
- [ ] Modo de cocina (pantalla siempre encendida)
- [ ] Timer integrado
- [ ] Lista de la compra
- [ ] Conversión de unidades

---

<div align="center">

**¡Disfruta cocinando con FoodieHub! 🍳👨‍🍳**

</div>
