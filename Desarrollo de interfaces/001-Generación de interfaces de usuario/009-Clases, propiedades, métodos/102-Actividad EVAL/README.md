# Actividad Práctica JocarsaUX
## Sistema de Gestión Deportiva, Gaming y Turismo

### 📋 Descripción General

Esta actividad práctica demuestra el uso completo de los diferentes renderizadores disponibles en el framework **JocarsaUX** aplicados a tres áreas de interés personal: deportes, videojuegos y turismo. El sistema implementa todas las funcionalidades principales del framework con datos realistas y casos de uso prácticos.

### 🎯 Objetivos de la Actividad

1. **Experimentar con diferentes renderizadores**: Utilizar `tableRenderer`, `formRenderer`, `chartRenderer`, `gridRenderer` y `menuRenderer`
2. **Integrar datos de hobbies personales**: Aplicar el framework a datos reales de deportes, gaming y turismo
3. **Practicar filtros y ordenamiento**: Implementar búsquedas y ordenación en tiempo real
4. **Demostrar integración completa**: Crear un sistema cohesivo que use todos los componentes

### 🏗️ Estructura del Proyecto

```
102-Actividad EVAL/
├── index.html              # Archivo principal de la aplicación
├── datos-deportivos.js      # Dataset con estadísticas de equipos de fútbol
├── datos-gaming.js          # Dataset con puntuaciones de videojuegos
├── datos-turismo.js         # Dataset con estadísticas turísticas globales
└── README.md               # Esta documentación
```

### 🔧 Componentes Implementados

#### 1. 🏆 **TableRenderer - Gestión Deportiva**
- **Dataset**: Estadísticas completas de equipos de fútbol de La Liga
- **Características**:
  - 12 equipos con 21 campos por equipo
  - Filtrado en tiempo real por cualquier campo
  - Ordenamiento clickeable en todas las columnas
  - Paginación con 8 equipos por página
  - Datos incluyen: puntos, goles, diferencia de goles, entrenador, estadio, etc.

```javascript
uxTabla.tableRenderer({
    target: mainContainer,
    data: datosDeportivos,
    title: '🏆 Estadísticas del Torneo de Fútbol',
    subtitle: 'Tabla interactiva con filtros y ordenamiento - Temporada 2024',
    rowsPerPage: 8
});
```

#### 2. ⚽ **GridRenderer - Vista Cards Equipos**
- **Funcionalidad**: Presentación alternativa de datos deportivos en formato tarjetas
- **Características**:
  - Vista responsiva en cards con hover effects
  - 6 tarjetas por página
  - Click en tarjetas muestra información detallada
  - Mismo dataset que la tabla pero con presentación visual mejorada

```javascript
uxCards.gridRenderer({
    target: mainContainer,
    data: datosDeportivos,
    title: '⚽ Equipos del Torneo',
    cardsPerPage: 6,
    titleField: 'equipo',
    onCardClick: (equipo, index) => {
        // Mostrar información detallada del equipo
    }
});
```

#### 3. 🎮 **FormRenderer - Registro Gaming**
- **Dataset**: Modelo basado en puntuaciones de videojuegos
- **Características**:
  - Detección automática de tipos de campo
  - Campos numéricos para puntuaciones y estadísticas
  - Campos select para plataformas, rangos y modos de juego
  - Campos de texto para nombres y descripciones
  - Validación automática según el tipo detectado

```javascript
uxForm.formRenderer({
    target: mainContainer,
    data: [datosGaming[0]], // Usar primer registro como modelo
    title: '🎮 Registro de Puntuaciones Gaming',
    columns: 2,
    onSubmit: (datos) => {
        // Procesar datos del formulario
    }
});
```

#### 4. 🏮 **TableRenderer - Ranking Gaming**
- **Dataset**: 12 jugadores con estadísticas completas de diferentes videojuegos
- **Características**:
  - Datos de diferentes plataformas (PC, Xbox, PlayStation)
  - Estadísticas detalladas: K/D ratio, partidas ganadas, experiencia total
  - Información de clanes, armas favoritas y regiones
  - Filtrado por jugador, juego, plataforma, etc.

#### 5. ✈️ **ChartRenderer - Estadísticas Turísticas**
- **Dataset**: 15 países con datos turísticos completos
- **Características**:
  - Generación automática de gráficos circulares
  - Datos categóricos: regiones, temporadas altas, tipos de turismo
  - Visualización automática de patrones en los datos
  - Leyendas interactivas con porcentajes y valores absolutos

```javascript
uxCharts.chartRenderer({
    target: mainContainer,
    data: datosTurismo,
    title: '✈️ Estadísticas Turísticas Globales',
    subtitle: 'Gráficos automáticos basados en datos de visitantes por regiones'
});
```

#### 6. 🗺️ **FormRenderer - Nuevo Destino Turístico**
- **Funcionalidad**: Formulario para agregar nuevos destinos turísticos
- **Características**:
  - Formulario de 2 columnas para mejor aprovechamiento del espacio
  - Campos especializados según el tipo de dato detectado
  - Integración con el dataset existente como modelo

#### 7. 🎛️ **MenuRenderer - Navegación Principal**
- **Características**:
  - Menú lateral organizado en secciones temáticas
  - 4 secciones principales: Deportes, Gaming, Turismo, Ejemplos Avanzados
  - Navegación fluida entre diferentes vistas
  - Indicador visual del elemento activo

#### 8. 📊 **Dashboard Integral**
- **Funcionalidad**: Vista combinada que demuestra múltiples renderizadores simultáneamente
- **Características**:
  - Mini-tabla deportiva con top 5 equipos
  - Mini-grid gaming con mejores puntuaciones
  - Mini-gráfico turístico con resumen de datos
  - Resumen de funcionalidades implementadas

### 📋 Datos Implementados

#### 🏆 Datos Deportivos
- **Equipos**: 12 equipos de fútbol de La Liga
- **Campos por equipo**: 21 campos incluyendo estadísticas, información del club y métricas financieras
- **Ejemplos de campos**: puntos, goles a favor/contra, entrenador, estadio, capacidad, presupuesto, valor de mercado

#### 🎮 Datos Gaming
- **Jugadores**: 12 perfiles de gaming con estadísticas completas
- **Juegos representados**: Call of Duty, Halo, Valorant, Rocket League, Fortnite, Apex Legends, Overwatch 2, League of Legends, Counter-Strike 2, Minecraft, FIFA 24, World of Warcraft
- **Campos por jugador**: 20 campos incluyendo métricas de rendimiento, información de clan y preferencias

#### ✈️ Datos Turísticos
- **Países**: 15 destinos turísticos principales a nivel mundial
- **Campos por país**: 20 campos incluyendo estadísticas de visitantes, información económica, cultural y logística
- **Regiones representadas**: Europa, Asia, América del Norte, América del Sur, Oceanía

### 🔍 Funcionalidades Demostradas

#### **Filtros Dinámicos**
- Búsqueda en tiempo real en todas las tablas
- Filtrado por cualquier campo visible
- Actualización inmediata de resultados
- Contador dinámico de elementos filtrados

#### **Ordenamiento Inteligente**
- Detección automática de tipos de datos (numérico vs. texto)
- Ordenamiento numérico para campos cuantitativos
- Ordenamiento alfanumérico para campos de texto
- Indicadores visuales de dirección de ordenamiento

#### **Paginación Eficiente**
- Navegación por páginas en datasets grandes
- Controles de página anterior/siguiente
- Salto directo a páginas específicas
- Información contextual de página actual

#### **Detección Automática de Tipos**
- **Campos numéricos**: Detección automática para estadísticas y métricas
- **Campos select**: Generación automática cuando hay opciones limitadas repetitivas
- **Campos textarea**: Para textos largos (promedio > 80 caracteres)
- **Campos texto**: Por defecto para el resto de datos

#### **Gráficos Automáticos**
- Detección automática de datos graficables
- Generación de gráficos circulares para datos categóricos
- Cálculo automático de porcentajes y totales
- Paleta de colores predefinida y consistente

#### **Interfaz Responsiva**
- Adaptación automática a diferentes tamaños de pantalla
- Grid responsivo para tarjetas y gráficos
- Menú lateral colapsable en dispositivos móviles
- Optimización para touch en dispositivos táctiles

### 🚀 Instrucciones de Uso

1. **Abrir la aplicación**: Navegar a `index.html` en un navegador web
2. **Explorar el menú**: Utilizar el menú lateral para navegar entre secciones
3. **Probar filtros**: Usar los campos de búsqueda para filtrar datos en tiempo real
4. **Experimentar con ordenamiento**: Hacer click en las cabeceras de las tablas
5. **Interactuar con formularios**: Rellenar y enviar los formularios de registro
6. **Visualizar gráficos**: Explorar los gráficos automáticos generados
7. **Dashboard integral**: Acceder a la vista combinada para ver múltiples componentes

### 🎓 Valor Educativo

Esta actividad demuestra:
- **Programación orientada a objetos**: Uso de clases y métodos de JocarsaUX
- **Manipulación del DOM**: Generación dinámica de elementos HTML
- **Gestión de eventos**: Interactividad con clicks, búsquedas y navegación
- **Diseño responsivo**: Adaptación a diferentes dispositivos y pantallas
- **Arquitectura modular**: Separación clara entre datos, lógica y presentación
- **Experiencia de usuario**: Interfaces intuitivas y feedback visual inmediato

### 💡 Extensiones Posibles

- **Persistencia de datos**: Integración con localStorage o base de datos
- **Exportación de datos**: Funcionalidad para descargar tablas en CSV/Excel
- **Más tipos de gráficos**: Barras, líneas, histogramas
- **Filtros avanzados**: Rangos numéricos, fechas, múltiples criterios
- **Temas personalizables**: Diferentes esquemas de colores
- **Internacionalización**: Soporte para múltiples idiomas

---

**Desarrollado como actividad práctica para el curso de Desarrollo de Interfaces de Usuario**  
*Módulo: Clases, propiedades y métodos*