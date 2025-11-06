# Gestor Personal de Actividades

Pequeña aplicación en Python (Tkinter) para gestionar actividades personales (CRUD) y persistencia en JSON.

Características principales
- Añadir, editar y eliminar actividades.
- Guardado automático en `data/store.json` (JSON).
- Importar y exportar CSV (herramienta CLI y posibilidad de integrar en UI).
- Búsqueda y filtrado básicos.
- Estadísticas simples (conteo por categoría / mes).
- Tests básicos con `unittest`.

Requisitos
- Python 3.8+ (sólo librerías estándar utilizadas).

Estructura del proyecto

GestorActividades/
- app.py                      # punto de entrada
- domain/                     # modelos y validadores
  - models.py
  - validators.py
  - mappers.py
- services/                   # lógica de negocio, import/export, reporting
  - activity_service.py
  - import_export.py
  - reporting.py
- storage/                    # repositorio JSON y utilidades de filesystem
  - repo_json.py
  - filesystem.py
- ui/                         # estilos, vistas y controlador
  - styles.py
  - views.py
  - controllers.py
- data/
  - store.json                # fichero de datos (iniciado vacío)
  - export/                   # export CSV por defecto
- logs/
  - app.log
- tests/
  - test_models.py
  - test_services.py
- tools/
  - cli.py                    # utilidades CLI para export/import

Cómo ejecutar la aplicación (GUI)

1. Abrir PowerShell en la carpeta del proyecto:

```powershell
cd "d:\xampp\htdocs\DAM-2\Acceso a datos\001-Manejo de ficheros\102-Actividad Final EVAL\GestorActividades"
```

2. Ejecutar la app:

```powershell
python .\app.py
```

La ventana muestra tres pestañas: Lista, Formulario y Estadísticas.

Operaciones básicas (GUI)
- Añadir: pestaña Formulario -> rellenar campos -> botón "Añadir".
- Editar: seleccionar una fila en Lista, cargar valores en formulario (manual en este esqueleto), modificar y pulsar "Actualizar".
- Eliminar: seleccionar una fila en Lista y pulsar "Eliminar" en Formulario.
- Exportar CSV: disponible desde la CLI (ver más abajo). Podemos añadir un botón de exportación en la UI si lo deseas.

Dónde se guardan los datos
- Archivo principal: `data/store.json` (lista JSON de actividades).
- Logs: `logs/app.log` (registro de operaciones).

CLI: exportar / importar CSV

Exportar todas las actividades a CSV:

```powershell
python .\tools\cli.py --export data\export\activities.csv
```

Importar desde CSV (las actividades se intentan crear en el repo):

```powershell
python .\tools\cli.py --import path\to\file.csv
```

Tests

Ejecutar todos los tests con unittest:

```powershell
python -m unittest discover -v -s "d:\xampp\htdocs\DAM-2\Acceso a datos\001-Manejo de ficheros\102-Actividad Final EVAL\GestorActividades\tests" -p "test_*.py"
```

O, desde la raíz del proyecto:

```powershell
python -m unittest discover -v
```

Notas y siguientes mejoras sugeridas
- Aislar ruta de datos en tests (usar tempdir) para evitar modificar `data/store.json` durante pruebas.
- Añadir atajos de teclado (Ctrl+N para nueva, Supr para eliminar, Enter para enviar formulario).
- Integrar export/import dentro de la UI y añadir confirmaciones y progreso.
- Mejorar la validación y el manejo de errores (mensajes más detallados, logging extendido).
- Implementar particionado por mes (guardar copia/backup en `data/YYYY/MM/`). Existe soporte inicial en `storage/filesystem.py`.

Si quieres, implemento ahora cualquiera de las mejoras anteriores (README creado). Indica cuál prefieres y la añado.
