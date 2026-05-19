# 🏠 InmoWeb AI - Generador de Sitios Web Inmobiliarios

**Proyecto de IA Generativa - Actividad 301-002**  
**Asignatura:** Proyecto Intermodular II  
**Curso:** 2º DAM

---

## 📖 Descripción del Proyecto

**InmoWeb AI** es un generador de sitios web especializado en el sector inmobiliario que utiliza Inteligencia Artificial para crear páginas HTML+CSS profesionales a partir de descripciones en lenguaje natural.

El proyecto está basado en el ejercicio de clase sobre generadores web con IA, pero ha sido completamente personalizado y ampliado con funcionalidades avanzadas específicas para el sector inmobiliario.

---

## ✨ Características Principales

### 🎨 Modificaciones Estéticas

- **Paleta de colores corporativa:** Azul (#003d82) y dorado (#d4af37) inspirados en el sector inmobiliario
- **Tipografía dual:** Playfair Display para títulos elegantes + Inter para legibilidad
- **Layout con sidebar:** Navegación lateral fija con estadísticas en tiempo real
- **Diseño responsive:** Preview multi-dispositivo (escritorio, tablet, móvil)
- **Animaciones suaves:** Transiciones fluidas en hover y cambios de estado
- **Iconografía temática:** Emojis y símbolos relacionados con bienes raíces

### ⚙️ Modificaciones Funcionales (2º Curso)

1. **Base de Datos SQLite**
   - Persistencia de proyectos generados
   - Almacenamiento de metadatos (tipo, precio, ubicación, características)
   - Sistema CRUD completo (Create, Read, Update, Delete)

2. **Sistema de Plantillas Especializadas**
   - 4 plantillas predefinidas: Lujo, Moderna, Vacacional, Comercial
   - Carga rápida con parámetros preconfigurados
   - Personalización antes de generar

3. **Gestión de Proyectos**
   - Galería de proyectos guardados
   - Vista previa de cada proyecto
   - Exportación a archivos HTML independientes
   - Eliminación de proyectos

4. **Parámetros Enriquecidos**
   - Tipo de propiedad (apartamentos, casas, villas, etc.)
   - Rango de precios
   - Ubicación geográfica
   - Características destacadas

5. **Preview Responsive**
   - Vista previa en tiempo real
   - Simulación de diferentes dispositivos
   - Iframe aislado para seguridad

6. **Estadísticas de Uso**
   - Contador de generaciones totales
   - Contador de proyectos guardados
   - Badge con número de proyectos en navegación

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **Flask 3.0.0:** Framework web Python
- **SQLite3:** Base de datos embebida
- **Requests:** Cliente HTTP para Ollama
- **Python 3.10+**

### Frontend
- **HTML5 + CSS3:** Estructura y estilos
- **JavaScript (ES6+):** Lógica del cliente
- **Google Fonts:** Playfair Display + Inter

### IA Generativa
- **Ollama:** Servidor local de modelos LLM
- **Qwen 2.5 (7B Instruct):** Modelo de lenguaje optimizado

---

## 📁 Estructura del Proyecto

```
101-Ejercicios/
├── app.py                  # Backend Flask con API REST
├── requirements.txt        # Dependencias Python
├── inmoweb.db             # Base de datos SQLite (generada automáticamente)
├── templates/
│   └── index.html         # Interfaz principal (SPA)
└── static/
    ├── css/
    │   └── style.css      # Estilos personalizados
    └── js/
        └── main.js        # Lógica del frontend
```

---

## 🚀 Instalación y Ejecución

### Prerequisitos

1. **Python 3.10 o superior**
   ```bash
   python --version
   ```

2. **Ollama instalado y ejecutándose**
   - Descargar desde: https://ollama.ai/
   - Instalar el modelo:
     ```bash
     ollama pull qwen2.5:7b-instruct-q4_0
     ```
   - Verificar que está corriendo:
     ```bash
     ollama list
     ```

### Instalación

1. **Navegar al directorio del proyecto**
   ```bash
   cd "d:\xampp\htdocs\DAM-2\Proyecto Intermodular II\301-Actividades final de unidad - Segundo trimestre\002-IA generativa\101-Ejercicios"
   ```

2. **Crear y activar entorno virtual (RECOMENDADO)**
   ```bash
   # Crear entorno virtual
   python -m venv .venv
   
   # Activar entorno virtual
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   
   # Windows CMD:
   .venv\Scripts\activate.bat
   
   # Linux/Mac:
   source .venv/bin/activate
   ```
   
   > 💡 Verás `(.venv)` al inicio de tu prompt cuando esté activo.

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

### Ejecución

1. **Asegurarse de que el entorno virtual está activo**
   ```bash
   # Si no ves (.venv) en el prompt, actívalo:
   .venv\Scripts\Activate.ps1
   ```

2. **Iniciar el servidor Flask**
   ```bash
   python app.py
   ```

3. **Abrir en el navegador**
   ```
   http://localhost:5000
   ```

---

## 📝 Uso de la Aplicación

### 1. Generar un Sitio Web

1. Describe el sitio web en el área de texto principal
2. (Opcional) Selecciona tipo de propiedad, precio, ubicación y características
3. Haz clic en **"Generar Sitio Web"**
4. Espera unos segundos mientras la IA crea tu página
5. Visualiza el resultado en el panel de la derecha

### 2. Usar Plantillas Rápidas

- Haz clic en cualquiera de las 4 plantillas predefinidas
- Los campos se rellenarán automáticamente
- Personaliza si lo deseas
- Genera el sitio web

### 3. Guardar un Proyecto

1. Después de generar una página, haz clic en **"💾 Guardar Proyecto"**
2. Ingresa un nombre para el proyecto
3. (Opcional) Añade una descripción
4. Haz clic en **"Guardar"**

### 4. Gestionar Proyectos

- Ve a la sección **"📁 Mis Proyectos"** en el sidebar
- **Ver:** Carga el proyecto en el generador para editarlo
- **⬇️:** Descarga el HTML como archivo independiente
- **🗑️:** Elimina el proyecto de la base de datos

### 5. Probar en Diferentes Dispositivos

- Usa los botones 🖥️ 📱 en la vista previa
- Cambia entre escritorio, tablet y móvil
- Verifica que el diseño es responsive

---

## 🎯 Criterios de Evaluación Cumplidos

### 1. Modificaciones Estéticas ✅

- [x] Paleta de colores personalizada (azul corporativo + dorado)
- [x] Tipografías profesionales (Playfair Display + Inter)
- [x] Layout diferente al original (sidebar + grid)
- [x] Animaciones y transiciones suaves
- [x] Iconografía temática inmobiliaria
- [x] Diseño responsive mejorado

### 2. Modificaciones Funcionales (Esenciales para 2º Curso) ✅

- [x] **Base de datos SQLite:** Persistencia completa con tablas relacionales
- [x] **CRUD completo:** Create (guardar), Read (listar/ver), Delete (eliminar)
- [x] **API REST:** Endpoints `/generate`, `/save`, `/proyectos`, `/proyecto/<id>`, `/exportar/<id>`
- [x] **Sistema de plantillas:** 4 plantillas especializadas precargables
- [x] **Parámetros enriquecidos:** Campos adicionales específicos del dominio
- [x] **Exportación de archivos:** Descarga de HTML como archivos independientes
- [x] **Estadísticas en tiempo real:** Contadores de generaciones y proyectos
- [x] **Preview multi-dispositivo:** Simulación de responsive design

### 3. Respeto a la Temática Base ✅

- [x] Mantiene el concepto: Generador web con IA
- [x] Usa Ollama como motor de IA generativa
- [x] Genera HTML+CSS sin JavaScript
- [x] Interfaz similar pero personalizada

### 4. Código Profesional ✅

- [x] Código comentado y bien estructurado
- [x] Separación de responsabilidades (MVC implícito)
- [x] Manejo de errores robusto
- [x] Variables CSS organizadas
- [x] Funciones reutilizables en JavaScript

---

## 🔧 Endpoints de la API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Página principal |
| POST | `/generate` | Genera HTML con IA |
| POST | `/save` | Guarda un proyecto |
| GET | `/proyectos` | Lista todos los proyectos |
| GET | `/proyecto/<id>` | Obtiene un proyecto específico |
| DELETE | `/proyecto/<id>` | Elimina un proyecto |
| GET | `/exportar/<id>` | Descarga proyecto como HTML |

---

## 🗄️ Esquema de Base de Datos

### Tabla: `proyectos`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER PRIMARY KEY | Identificador único |
| nombre | TEXT NOT NULL | Nombre del proyecto |
| tipo_propiedad | TEXT | Tipo de inmueble |
| descripcion | TEXT | Descripción breve |
| precio | TEXT | Rango de precios |
| ubicacion | TEXT | Ubicación geográfica |
| caracteristicas | TEXT | Características destacadas |
| html_generado | TEXT NOT NULL | Código HTML completo |
| fecha_creacion | TIMESTAMP | Fecha de creación |

---

## 🎨 Paleta de Colores

| Color | Hex | Uso |
|-------|-----|-----|
| Azul Primario | `#003d82` | Sidebar, botones, títulos |
| Azul Claro | `#005bb5` | Hover states |
| Azul Oscuro | `#002554` | Degradados |
| Dorado | `#d4af37` | Acentos, badges, highlights |
| Dorado Claro | `#f5d76e` | Hover dorado |
| Blanco | `#ffffff` | Fondos, texto sobre oscuro |
| Grises | `#f9fafb` - `#111827` | Escala completa |

---

## 🚧 Mejoras Futuras

- [ ] Sistema de usuarios con autenticación
- [ ] Compartir proyectos vía URL
- [ ] Editor WYSIWYG inline
- [ ] Más modelos de IA (GPT-4, Claude, etc.)
- [ ] Integración con servicios de hosting
- [ ] Galería pública de proyectos destacados
- [ ] Versionado de proyectos
- [ ] Colaboración en tiempo real

---

## 🐛 Solución de Problemas

### Error: "No se pudo conectar con la IA"

**Causa:** Ollama no está ejecutándose o el modelo no está instalado.

**Solución:**
1. Verificar que Ollama está corriendo:
   ```bash
   ollama list
   ```
2. Si no está el modelo, instalarlo:
   ```bash
   ollama pull qwen2.5:7b-instruct-q4_0
   ```

### Error: "Module 'flask' not found"

**Causa:** Dependencias no instaladas.

**Solución:**
```bash
pip install -r requirements.txt
```

### Error: "Address already in use"

**Causa:** El puerto 5000 está ocupado.

**Solución:**
1. Cambiar el puerto en `app.py`:
   ```python
   app.run(host="0.0.0.0", port=5001, debug=True)
   ```
2. O matar el proceso en el puerto:
   ```bash
   # Windows
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   ```

---

## 📚 Diferencias con el Proyecto de Clase

| Aspecto | Proyecto de Clase | InmoWeb AI |
|---------|-------------------|------------|
| **Temática** | Genérico (cualquier web) | Especializado (inmobiliaria) |
| **Base de Datos** | ❌ No tiene | ✅ SQLite completa |
| **Persistencia** | ❌ Solo sesión | ✅ Guardado permanente |
| **Layout** | Dos columnas simple | Sidebar + navegación |
| **Plantillas** | Sugerencias básicas | 4 plantillas completas |
| **Parámetros** | Solo prompt | Prompt + 4 campos adicionales |
| **Gestión** | ❌ No existe | ✅ CRUD completo |
| **Exportación** | ❌ Solo copiar | ✅ Descarga + exportación |
| **Estadísticas** | ❌ No tiene | ✅ Contadores en vivo |
| **Preview** | Básico | Multi-dispositivo |
| **Colores** | Genéricos | Corporativos inmobiliarios |
| **Tipografía** | Poppins | Playfair + Inter |

---

## 👨‍💻 Autor

**Proyecto desarrollado como parte de la asignatura Proyecto Intermodular II**  
**2º Desarrollo de Aplicaciones Multiplataforma (DAM)**  
**Actividad:** 301-002 - IA Generativa

---

## 📄 Licencia

Este proyecto es parte de un trabajo académico y está disponible para fines educativos.

---

## 🙏 Agradecimientos

- **Profesor:** Jose Vicente Carratala Sanchis
- **Ollama:** Por proporcionar modelos LLM locales
- **Qwen Team:** Por el modelo Qwen 2.5
- **Google Fonts:** Por las tipografías Playfair Display e Inter

---

## 📞 Soporte

Para cualquier duda o problema con el proyecto:

1. Revisar la sección **Solución de Problemas**
2. Verificar que Ollama está corriendo correctamente
3. Comprobar que las dependencias están instaladas
4. Consultar los logs en la consola de Flask

---

**¡Gracias por usar InmoWeb AI! 🏠✨**
