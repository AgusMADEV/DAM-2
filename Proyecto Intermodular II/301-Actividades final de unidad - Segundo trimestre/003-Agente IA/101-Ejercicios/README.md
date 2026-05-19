# 🤖 Agente IA Autónomo

Sistema de agente de inteligencia artificial que recibe misiones y persevera de forma autónoma, iterando hasta conseguir sus objetivos.

## 📋 Descripción

Este proyecto implementa un agente de IA autónomo capaz de:
- ✅ Recibir misiones/objetivos complejos
- ✅ Planificar y ejecutar acciones de forma iterativa
- ✅ Aprender de errores y ajustar su estrategia
- ✅ Generar código y soluciones técnicas
- ✅ Persistir hasta completar el objetivo
- ✅ Registrar todo el proceso en una base de datos

## 🎯 Características Principales

### Backend (PHP)
- **Sistema de iteración autónoma**: El agente ejecuta ciclos de análisis → planificación → ejecución → validación
- **Integración con IA**: Conexión con APIs de IA (OpenAI, u otras)
- **Persistencia completa**: Base de datos MySQL con historial de todas las iteraciones
- **Logging avanzado**: Registro detallado de decisiones y acciones
- **API REST**: Endpoints para gestionar misiones y monitorear el agente

### Frontend (HTML/CSS/JavaScript)
- **Panel de control moderno**: Interface visual atractiva con diseño responsive
- **Dashboard en tiempo real**: Estadísticas y métricas del agente
- **Gestión de misiones**: Crear, ejecutar y monitorear misiones
- **Visualización de iteraciones**: Ver el proceso paso a paso
- **Sistema de logs**: Consultar logs del sistema en tiempo real

### Base de Datos
- **Misiones**: Objetivos y estados
- **Iteraciones**: Cada ciclo del agente con entrada/salida
- **Decisiones**: Razonamiento del agente
- **Artefactos**: Código y archivos generados
- **Conocimiento**: Memoria persistente del agente
- **Logs**: Trazabilidad completa

## 🚀 Instalación

### Requisitos Previos
- XAMPP (o LAMP/WAMP/MAMP)
- PHP 8.0 o superior
- MySQL 5.7 o superior
- Navegador web moderno

### Pasos de Instalación

#### 1. Copiar Archivos
```bash
# Copiar el proyecto a la carpeta htdocs de XAMPP
cp -r 003-Agente\ IA d:/xampp/htdocs/
```

#### 2. Configurar Base de Datos
```bash
# Iniciar XAMPP y activar Apache + MySQL
# Abrir phpMyAdmin: http://localhost/phpmyadmin

# Importar el esquema de la base de datos
# Ejecutar el archivo: database/schema.sql
```

O manualmente desde línea de comandos:
```bash
mysql -u root -p < database/schema.sql
```

#### 3. Configurar Conexión

Editar `config/database.php` si es necesario:
```php
define('DB_HOST', 'localhost');
define('DB_NAME', 'agente_ia_autonomo');
define('DB_USER', 'root');
define('DB_PASS', ''); // Cambiar si tienes contraseña
```

#### 4. Configurar API de IA (Opcional)

Para usar una IA real, configurar en `config/config.php`:
```php
define('AI_API_KEY', 'tu_api_key_aqui');
```

O configurar variable de entorno:
```bash
# Windows
setx OPENAI_API_KEY "tu_api_key_aqui"

# Linux/Mac
export OPENAI_API_KEY="tu_api_key_aqui"
```

**Nota**: El sistema funciona sin API key en "modo simulación" para desarrollo y testing.

#### 5. Acceder a la Aplicación

Abrir en el navegador:
```
http://localhost/003-Agente%20IA/101-Ejercicios/
```

## 📖 Uso

### Crear una Misión

1. En el dashboard, hacer clic en "Nueva Misión"
2. Rellenar:
   - **Título**: Nombre descriptivo
   - **Descripción**: Breve explicación
   - **Objetivo Final**: Lo que el agente debe lograr
   - **Prioridad**: Baja/Media/Alta/Crítica
3. Hacer clic en "Crear Misión"

### Ejecutar el Agente

1. En la lista de misiones, buscar la misión deseada
2. Hacer clic en el botón "Ejecutar"
3. El agente comenzará a iterar automáticamente
4. Ver el progreso en tiempo real

### Monitorear el Proceso

- **Dashboard**: Ver estadísticas generales
- **Misiones**: Lista completa con estado y progreso
- **Detalle**: Hacer clic en una misión para ver iteraciones
- **Logs**: Consultar logs del sistema

## 🏗️ Arquitectura

### Flujo del Agente

```
1. ANÁLISIS
   ↓ Evaluar estado actual y contexto
2. PLANIFICACIÓN
   ↓ Decidir qué acción tomar
3. EJECUCIÓN
   ↓ Generar código/solución
4. VALIDACIÓN
   ↓ Verificar si se cumplió el objetivo
5. ¿Completado? → SÍ: FIN | NO: Volver a 1
```

### Estructura de Archivos

```
101-Ejercicios/
├── index.html              # Página principal
├── api/
│   └── api.php            # API REST
├── assets/
│   ├── css/
│   │   └── styles.css     # Estilos
│   └── js/
│       └── app.js         # Lógica frontend
├── classes/
│   ├── AgenteIA.php       # Clase principal del agente
│   ├── IAService.php      # Servicio de IA
│   └── Logger.php         # Sistema de logs
├── config/
│   ├── config.php         # Configuración general
│   └── database.php       # Conexión DB
├── database/
│   └── schema.sql         # Esquema de base de datos
├── logs/                  # Logs del sistema
├── output/                # Código generado
└── temp/                  # Archivos temporales
```

## 🎨 Modificaciones Realizadas

### Estéticas y Visuales
- ✅ Diseño moderno con gradientes y sombras
- ✅ Interface responsive (móvil, tablet, desktop)
- ✅ Animaciones suaves y transiciones
- ✅ Sistema de notificaciones toast
- ✅ Modales elegantes
- ✅ Paleta de colores profesional
- ✅ Iconos Font Awesome
- ✅ Tarjetas de estadísticas visuales

### Funcionales (Código y Base de Datos)
- ✅ **Sistema de iteración autónoma** completo
- ✅ **Base de datos robusta** con 7 tablas relacionales
- ✅ **API REST completa** con múltiples endpoints
- ✅ **Integración con IA** externa (OpenAI compatible)
- ✅ **Sistema de logging** multicapa (consola, archivo, BD)
- ✅ **Persistencia de conocimiento** del agente
- ✅ **Gestión de artefactos** generados
- ✅ **Sistema de decisiones** con razonamiento
- ✅ **Validación automática** de resultados
- ✅ **Manejo de errores** robusto

## 🔧 Configuración Avanzada

### Ajustar Parámetros del Agente

En `config/config.php`:

```php
define('MAX_ITERACIONES', 50);        // Máximo de iteraciones
define('TIMEOUT_ITERACION', 120);     // Timeout por iteración (seg)
define('AI_TEMPERATURE', 0.7);        // Creatividad de la IA (0-1)
define('AI_MAX_TOKENS', 4000);        // Tokens máximos por respuesta
```

### Cambiar Modelo de IA

```php
define('AI_MODEL', 'gpt-4');  // o 'gpt-3.5-turbo', 'claude-3', etc
```

## 📊 Base de Datos

### Tablas Principales

1. **misiones**: Objetivos del agente
2. **iteraciones**: Cada ciclo de ejecución
3. **decisiones**: Razonamiento del agente
4. **artefactos**: Código generado
5. **logs_agente**: Registro de eventos
6. **conocimiento**: Memoria del agente
7. **configuracion**: Parámetros del sistema

## 🐛 Troubleshooting

### El agente no se ejecuta

- Verificar que Apache y MySQL estén corriendo
- Revisar la configuración de la base de datos
- Consultar los logs en `logs/`

### Error de conexión a la API

- Verificar que AI_API_KEY esté configurada
- O usar el modo simulación (sin API key)

### Los estilos no se cargan

- Verificar la ruta en el navegador
- Limpiar caché del navegador
- Revisar permisos de archivos

## 📝 Próximas Mejoras

- [ ] Worker asíncrono para ejecuciones largas
- [ ] Websockets para actualizaciones en tiempo real
- [ ] Sistema de plugins para extender funcionalidad
- [ ] Integración con más APIs de IA
- [ ] Exportación de reportes
- [ ] Modo debug avanzado

## 👨‍💻 Desarrollo

### Tecnologías Utilizadas

- **Backend**: PHP 8.0+, PDO, cURL
- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Base de Datos**: MySQL 5.7+
- **Diseño**: CSS Grid, Flexbox, Animaciones CSS
- **Iconos**: Font Awesome 6
- **API Externa**: OpenAI (o compatible)

## 📄 Licencia

Este proyecto es parte de una actividad educativa del módulo de Proyecto Intermodular II.

## ✍️ Autor

Desarrollado como proyecto final del segundo trimestre.

---

**Nota**: Este agente es un sistema educativo y experimental. Para uso en producción, se recomienda implementar medidas de seguridad adicionales, optimización de rendimiento y gestión de errores más robusta.
