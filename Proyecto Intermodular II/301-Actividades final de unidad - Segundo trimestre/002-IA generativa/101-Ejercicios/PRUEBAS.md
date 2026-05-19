# 🧪 Guía de Pruebas - InmoWeb AI

Esta guía te ayudará a probar todas las funcionalidades del proyecto antes de la entrega.

---

## ✅ Checklist de Pruebas

### 1. Configuración Inicial

- [ ] Python instalado (versión 3.10+)
- [ ] Ollama instalado y ejecutándose
- [ ] Modelo Qwen 2.5 descargado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Servidor Flask corriendo (`python app.py`)
- [ ] Navegador abierto en `http://localhost:5000`

### 2. Interfaz y Navegación

- [ ] El sidebar se muestra correctamente
- [ ] El logo y título "InmoWebAI" son visibles
- [ ] Los 3 botones de navegación funcionan (Generador, Mis Proyectos, Plantillas)
- [ ] Las estadísticas (Generaciones, Guardados) se muestran en el footer del sidebar
- [ ] El diseño es responsive (prueba redimensionando la ventana)

### 3. Generador - Funcionalidad Básica

- [ ] El formulario tiene todos los campos visibles
- [ ] Puedes escribir en el textarea de descripción
- [ ] Los selectores (tipo, precio) tienen opciones
- [ ] Los inputs (ubicación, características) funcionan
- [ ] El botón "Generar Sitio Web" está visible

### 4. Generar una Página Web

**Test 1: Generación simple**
- [ ] Escribe: "Landing page moderna para inmobiliaria"
- [ ] Haz clic en "Generar Sitio Web"
- [ ] El botón cambia a "Generando..."
- [ ] Aparece mensaje de carga
- [ ] El preview muestra el HTML generado (espera 10-30 segundos)
- [ ] Aparece mensaje de éxito
- [ ] Los botones de acción (Guardar, Copiar, Descargar) se hacen visibles

**Test 2: Generación con parámetros**
- [ ] Rellena todos los campos:
  - Descripción: "Web elegante para villas de lujo"
  - Tipo: Villas de lujo
  - Precio: Más de 1M €
  - Ubicación: Costa mediterránea
  - Características: piscina, vistas al mar
- [ ] Genera y verifica que el HTML refleja estos parámetros

### 5. Plantillas Rápidas

- [ ] Haz clic en la plantilla "👑 Inmobiliaria de Lujo"
- [ ] Los campos se rellenan automáticamente
- [ ] Aparece mensaje "Plantilla cargada"
- [ ] Puedes modificar los campos
- [ ] Genera y verifica el resultado

**Prueba las 4 plantillas:**
- [ ] 👑 Inmobiliaria de Lujo
- [ ] 🏢 Moderna y Minimalista
- [ ] 🏖️ Alquiler Vacacional
- [ ] 🏪 Comercial

### 6. Preview Multi-dispositivo

- [ ] Por defecto muestra vista "Escritorio" (🖥️ activo)
- [ ] Haz clic en tablet 📱
- [ ] El iframe cambia de tamaño
- [ ] Haz clic en móvil 📱
- [ ] El iframe se hace más estrecho
- [ ] Vuelve a escritorio
- [ ] Funciona correctamente

### 7. Acciones sobre el HTML Generado

**Copiar al portapapeles:**
- [ ] Genera una página
- [ ] Haz clic en "📋 Copiar HTML"
- [ ] Aparece mensaje "HTML copiado al portapapeles"
- [ ] Pega (Ctrl+V) en un editor de texto
- [ ] Verifica que es código HTML válido

**Descargar archivo:**
- [ ] Haz clic en "⬇️ Descargar"
- [ ] Se descarga un archivo `.html`
- [ ] Ábrelo en el navegador
- [ ] Se visualiza correctamente

### 8. Guardar Proyectos

- [ ] Genera una página web
- [ ] Haz clic en "💾 Guardar Proyecto"
- [ ] Se abre un modal
- [ ] El modal tiene:
  - Campo "Nombre del proyecto"
  - Campo "Descripción breve" (pre-rellenado)
  - Botones "Cancelar" y "Guardar"
- [ ] Escribe un nombre: "Prueba Villa Mediterránea"
- [ ] Haz clic en "Guardar"
- [ ] El modal se cierra
- [ ] Aparece mensaje de éxito
- [ ] El contador "Guardados" incrementa en 1
- [ ] El badge en "Mis Proyectos" incrementa en 1

**Test de validación:**
- [ ] Intenta guardar sin nombre
- [ ] Aparece alerta "Por favor, ingresa un nombre"

### 9. Gestionar Proyectos

**Ver lista de proyectos:**
- [ ] Haz clic en "📁 Mis Proyectos" en el sidebar
- [ ] Se muestra la lista de proyectos guardados
- [ ] Cada proyecto muestra:
  - Nombre
  - Fecha
  - Tipo de propiedad (si existe)
  - Descripción (si existe)
  - 3 botones: Ver, ⬇️, 🗑️

**Cargar un proyecto:**
- [ ] Haz clic en "👁️ Ver" en un proyecto
- [ ] Cambia a la vista "Generador"
- [ ] Los campos se rellenan con los datos del proyecto
- [ ] El preview muestra el HTML
- [ ] Aparece mensaje de éxito

**Exportar un proyecto:**
- [ ] Haz clic en "⬇️" en un proyecto
- [ ] Se descarga un archivo HTML con el nombre del proyecto
- [ ] Ábrelo en el navegador
- [ ] Funciona correctamente

**Eliminar un proyecto:**
- [ ] Haz clic en "🗑️" en un proyecto
- [ ] Aparece confirmación "¿Estás seguro?"
- [ ] Confirma
- [ ] El proyecto desaparece de la lista
- [ ] El contador se actualiza

### 10. Vista de Plantillas

- [ ] Haz clic en "📋 Plantillas" en el sidebar
- [ ] Se muestran 4 tarjetas de plantillas
- [ ] Cada tarjeta tiene:
  - Icono grande
  - Título
  - Descripción
  - Botón "Usar Plantilla"
- [ ] Haz clic en "Usar Plantilla" en cualquiera
- [ ] Cambia a la vista "Generador"
- [ ] Los campos se rellenan

### 11. Base de Datos

**Verificar que se crea la base de datos:**
- [ ] Después de guardar un proyecto, verifica que existe el archivo `inmoweb.db`
- [ ] Puedes abrirlo con un visor SQLite (DB Browser for SQLite)
- [ ] Existe la tabla `proyectos`
- [ ] Los datos guardados están en la tabla

### 12. API Endpoints

**Test manual con curl o Postman:**

```bash
# Listar proyectos
curl http://localhost:5000/proyectos

# Generar página
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Landing moderna para inmobiliaria"}'

# Guardar proyecto
curl -X POST http://localhost:5000/save \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Test", "html": "<html></html>"}'
```

- [ ] GET `/proyectos` devuelve JSON con lista
- [ ] POST `/generate` devuelve JSON con `html`
- [ ] POST `/save` devuelve JSON con `success: true`

### 13. Manejo de Errores

**Prompt vacío:**
- [ ] Deja el textarea vacío
- [ ] Haz clic en "Generar"
- [ ] Aparece mensaje de error
- [ ] No hace la petición a la API

**Ollama no disponible:**
- [ ] Detén Ollama
- [ ] Intenta generar una página
- [ ] Aparece mensaje de error (HTML de error estilizado)
- [ ] Se muestra el error técnico

**Guardar sin nombre:**
- [ ] Genera una página
- [ ] Abre el modal de guardar
- [ ] Deja el nombre vacío
- [ ] Haz clic en "Guardar"
- [ ] Aparece alerta

### 14. Estadísticas

- [ ] El contador "Generaciones" incrementa cada vez que generas
- [ ] El contador "Guardados" incrementa cada vez que guardas
- [ ] El contador "Guardados" decrementa cuando eliminas
- [ ] El badge en "Mis Proyectos" coincide con el total guardado

### 15. Rendimiento

- [ ] La generación tarda entre 5-30 segundos (depende del hardware)
- [ ] El preview se actualiza inmediatamente después de generarse
- [ ] No hay lag al cambiar de vista
- [ ] No hay lag al cambiar el dispositivo del preview

---

## 🎯 Escenarios de Uso Completos

### Escenario 1: Usuario Nuevo

1. Abre la aplicación
2. Lee las instrucciones
3. Prueba la plantilla "Inmobiliaria de Lujo"
4. Genera el sitio
5. Ve el preview
6. Prueba en móvil
7. Guarda el proyecto como "Mi Primera Villa"
8. Va a "Mis Proyectos"
9. Ve su proyecto guardado

### Escenario 2: Usuario Avanzado

1. Escribe un prompt personalizado largo
2. Rellena todos los parámetros
3. Genera
4. Revisa en diferentes dispositivos
5. Copia el HTML
6. Lo pega en un editor y lo revisa
7. Descarga el archivo
8. Guarda el proyecto con nombre descriptivo
9. Genera otra versión con diferentes parámetros
10. Compara ambas versiones cargándolas desde "Mis Proyectos"

### Escenario 3: Gestión de Proyectos

1. Genera y guarda 5 proyectos diferentes
2. Va a "Mis Proyectos"
3. Ve la lista completa
4. Carga el proyecto #2
5. Modifica el prompt
6. Regenera
7. Guarda como nuevo proyecto
8. Exporta el proyecto #3
9. Elimina el proyecto #1
10. Verifica que el contador se actualizó

---

## 🐛 Errores Comunes y Soluciones

### Error: "No se ha podido generar la página con la IA"

**Causa:** Ollama no está corriendo o no responde.

**Verificación:**
```bash
# Verificar que Ollama está corriendo
ollama list

# Probar el modelo manualmente
ollama run qwen2.5:7b-instruct-q4_0 "Hola"
```

### Error: "Address already in use: 5000"

**Causa:** Otro proceso está usando el puerto 5000.

**Solución:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Luego reinicia Flask
python app.py
```

### Error: "ModuleNotFoundError: No module named 'flask'"

**Causa:** Dependencias no instaladas.

**Solución:**
```bash
pip install -r requirements.txt
```

### La generación es muy lenta (>60 segundos)

**Causa:** Hardware limitado o modelo muy grande.

**Solución:**
1. Usar un modelo más pequeño:
   ```bash
   ollama pull qwen2.5:3b-instruct-q4_0
   ```
2. Cambiar en `app.py`:
   ```python
   MODEL_NAME = "qwen2.5:3b-instruct-q4_0"
   ```

---

## 📊 Tabla de Resultados de Pruebas

Marca ✅ cuando completes cada sección:

| Sección | Estado | Notas |
|---------|--------|-------|
| 1. Configuración | ⬜ | |
| 2. Interfaz | ⬜ | |
| 3. Formulario | ⬜ | |
| 4. Generación | ⬜ | |
| 5. Plantillas | ⬜ | |
| 6. Preview | ⬜ | |
| 7. Acciones | ⬜ | |
| 8. Guardar | ⬜ | |
| 9. Gestión | ⬜ | |
| 10. Vista Plantillas | ⬜ | |
| 11. Base de Datos | ⬜ | |
| 12. API | ⬜ | |
| 13. Errores | ⬜ | |
| 14. Estadísticas | ⬜ | |
| 15. Rendimiento | ⬜ | |

---

## 🎓 Presentación del Proyecto

Cuando presentes el proyecto al profesor, demuestra:

1. **Navegación completa:** Muestra las 3 vistas
2. **Generación con plantilla:** Usa una plantilla predefinida
3. **Generación personalizada:** Crea una desde cero con todos los parámetros
4. **Preview responsive:** Cambia entre dispositivos
5. **Guardar y recuperar:** Guarda un proyecto y luego cárgalo
6. **Exportación:** Descarga un proyecto y ábrelo externamente
7. **Base de datos:** Muestra el archivo `inmoweb.db` y su contenido
8. **Código:** Explica las partes más importantes:
   - Backend: Función `call_ollama()`, endpoints REST
   - Frontend: Sistema de vistas, fetch API
   - Base de datos: Esquema de la tabla `proyectos`
   - CSS: Variables personalizadas, layout grid

---

**¡Buena suerte con tu proyecto! 🚀**
