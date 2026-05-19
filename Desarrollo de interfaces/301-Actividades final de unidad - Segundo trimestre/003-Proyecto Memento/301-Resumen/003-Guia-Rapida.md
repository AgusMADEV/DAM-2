# 🧠 Memento 3D - Guía Rápida de Uso

## 🚀 Inicio Rápido

### 1. Abrir la Aplicación
Con XAMPP corriendo, abre en tu navegador:
```
http://localhost/DAM-2/Desarrollo%20de%20interfaces/301-Actividades%20final%20de%20unidad%20-%20Segundo%20trimestre/003-Proyecto%20Memento/101-Ejercicios/memento-mejorado.html
```

O simplemente abre el archivo `memento-mejorado.html` directamente.

---

## 🎮 Controles Básicos

### Navegación en el Espacio 3D
```
W - Avanzar hacia adelante
S - Retroceder
A - Moverse a la izquierda
D - Moverse a la derecha
Q - Subir
E - Bajar

Ratón: Arrastrar para mirar alrededor
```

### Interacciones
- **Click en un nodo**: Ver detalles y hacer zoom automático
- **Click fuera del modal**: Cerrar el modal de detalles

---

## ✨ Funcionalidades Principales

### 📝 Crear un Nuevo Recuerdo
1. Click en el botón **"➕ Nuevo Recuerdo"**
2. Rellena el formulario:
   - **Nombre** (obligatorio)
   - **Hobbie** (obligatorio)
   - **Edad** (obligatorio)
   - **Ciudad** (obligatorio)
   - **Profesión** (obligatorio)
   - **Fecha** (opcional)
   - **Descripción** (opcional)
3. Click en **"💾 Guardar Recuerdo"**
4. El nuevo recuerdo aparece en el espacio 3D

### 🔍 Buscar Recuerdos
1. Escribe en el campo de búsqueda en el panel izquierdo
2. Los nodos se filtran automáticamente en tiempo real
3. El contador **"Visibles"** muestra cuántos coinciden

### 🏷️ Filtrar por Propiedades
En la sección **"Filtros por Propiedad"**:
- **"Usar en relación"**: Incluye esta propiedad para calcular similitudes
- **"Mostrar en etiqueta"**: Muestra esta propiedad en el texto del nodo

Desactiva checkboxes para reducir el peso de ciertas propiedades en la agrupación.

### 📤 Exportar Datos
1. Click en **"📤 Exportar JSON"**
2. Se descarga un archivo `memento-backup-[fecha].json`
3. Guárdalo como backup de tus recuerdos

### 📥 Importar Datos
1. Click en **"📥 Importar JSON"**
2. Selecciona un archivo JSON válido
3. Los datos actuales se reemplazan por los importados
4. La escena se regenera automáticamente

---

## 🎨 Personalizar la Visualización

### Conexiones entre Nodos
- **Max conexiones por nodo**: Controla cuántas líneas se dibujan desde cada nodo (1-8)
- **Mostrar conexiones**: Activa/desactiva las líneas de conexión
- Las líneas de colores representan propiedades compartidas

### Apariencia de las Cápsulas
- **Mostrar cápsulas**: Activa/desactiva los modelos 3D
- **Transparencia cápsulas**: Ajusta la opacidad de las cápsulas (5-100%)

### Reactivar Física
Si los nodos se quedan estáticos, click en **"🔄 Reactivar Física"** para que vuelvan a moverse.

---

## 📊 Panel de Estadísticas

El panel superior muestra en tiempo real:
- **Recuerdos**: Total de recuerdos en la base de datos
- **Conexiones**: Número de líneas visibles en la escena
- **Personas**: Cantidad de personas únicas
- **Visibles**: Recuerdos que pasan el filtro de búsqueda

---

## 🎯 Entendiendo las Agrupaciones

Los nodos se agrupan automáticamente según similitudes:

### Colores de las Conexiones
Cada color representa una propiedad compartida:
- Nodos con la **misma profesión** → línea de un color
- Nodos con la **misma ciudad** → línea de otro color
- Múltiples propiedades compartidas → colores mezclados

### Comportamiento de la Física
- **Nodos similares** → se atraen y forman clusters
- **Nodos diferentes** → se repelen y se alejan
- Cuando los nodos se estabilizan, dejan de moverse (optimización)

---

## 💡 Consejos de Uso

### Para Mejor Exploración
1. Navega lentamente con W/A/S/D para apreciar las agrupaciones
2. Usa Q/E para ver la escena desde arriba o abajo
3. Click en varios nodos para comparar sus propiedades
4. Observa los colores de las líneas para identificar conexiones

### Para Crear Datos de Calidad
1. Usa nombres reales o ficticios coherentes
2. Varía las edades, ciudades y profesiones para ver mejores agrupaciones
3. Añade descripciones detalladas para recordar el contexto
4. Usa fechas para tener una línea temporal

### Para Gestión de Datos
1. Exporta regularmente como backup
2. Usa archivos JSON descriptivos
3. Puedes editar el JSON manualmente y reimportarlo
4. Los datos persisten automáticamente en el navegador

---

## ❓ Solución de Problemas

### Los nodos no se mueven
✅ Click en **"🔄 Reactivar Física"**

### No veo conexiones
✅ Activa el checkbox **"Mostrar conexiones"**  
✅ Aumenta **"Max conexiones por nodo"**

### No encuentro un recuerdo
✅ Usa la **búsqueda** escribiendo cualquier palabra relacionada  
✅ Limpia el campo de búsqueda para ver todos

### Las cápsulas no se ven
✅ Activa **"Mostrar cápsulas"**  
✅ Aumenta la **transparencia**

### Perdí mis datos
✅ Los datos están en **IndexedDB** del navegador  
✅ No se pierden al cerrar la pestaña  
✅ Se pierden si limpias datos del navegador  
✅ **Exporta regularmente como precaución**

---

## 🎓 Casos de Uso Educativos

### Diario Personal
- Guarda momentos importantes de tu vida
- Agrupa por períodos (usando fechas)
- Visualiza conexiones entre eventos

### Gestión de Contactos
- Almacena información de conocidos
- Agrupa por ciudad o profesión
- Encuentra personas con hobbies similares

### Investigación de Datos
- Importa datasets de personas
- Visualiza patrones y clustering
- Analiza relaciones semánticas

### Proyecto de Clase
- Cada estudiante añade sus datos
- Exporta e importa entre compañeros
- Combina múltiples JSON en uno solo

---

## 🔗 Archivos del Proyecto

```
📁 101-Ejercicios/
  ├── memento-mejorado.html         ← Abrir este archivo
  ├── datos-ampliados.json          ← Datos de ejemplo mejorados
  ├── personas2.json                ← Datos originales
  └── 013-click en pastillas.html   ← Versión original
```

---

## 📱 Compatibilidad

### Navegadores Soportados
- ✅ Chrome/Edge (Recomendado)
- ✅ Firefox
- ⚠️ Safari (puede tener problemas con WebGL)
- ❌ Internet Explorer (no soportado)

### Requisitos
- WebGL habilitado
- JavaScript habilitado
- IndexedDB soportado (todos los navegadores modernos)

---

## 🎉 ¡Disfruta de Memento 3D!

Explora tus recuerdos en un espacio tridimensional interactivo y descubre conexiones que no sabías que existían.

**¿Dudas o problemas?** Revisa la documentación completa en `002-Documentacion-Mejoras.md`