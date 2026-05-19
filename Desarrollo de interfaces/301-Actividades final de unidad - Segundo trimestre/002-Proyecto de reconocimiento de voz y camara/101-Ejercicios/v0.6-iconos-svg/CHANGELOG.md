# v0.6 - Reemplazar emojis por iconos SVG minimalistas

## Nuevas características visuales

✅ **Iconos SVG en títulos**
- H2 "Gestión de Tareas" con icono clipboard SVG
- H2 "Control por Gestos" con icono corazón/heart SVG
- Clase `.icon` con estilos consistentes (20x20px, stroke-width: 2)

✅ **Iconos SVG en botones**
- Botón "Escuchar" con icono de micrófono SVG
- Botón "Limpiar" con icono de papelera SVG
- Iconos inline dentro de los botones (16x16px)

✅ **Empty state con SVG**
- Reemplazado emoji 📋 por SVG clipboard
- Icono grande (48x48px) con stroke currentColor
- Opacity 0.3 para efecto sutil

✅ **Estados de tareas con SVG**
- Tarea completada: SVG checkmark verde (#10b981)
- Tarea pendiente: SVG reloj gris (#94a3b8)
- Renderizado inline en tabla con estilos específicos

✅ **Gestos con caracteres minimalistas**
- II → Dos dedos
- ↑ → Pulgar arriba
- ● → Puño cerrado
- ▢ → Mano abierta
- Contenedores `.gesture-icon` con borde y background

✅ **CSS para iconos**
- Clase `.icon` global para SVG en headers y botones
- `stroke-linecap: round` y `stroke-linejoin: round`
- Fill: none, Stroke: currentColor (hereda color del padre)
- Responsive y escalable

✅ **Gesture info mejorado**
- Estructura de lista con iconos en cajas
- `.gesture-icon`: 32x32px con border y background
- Hover effect en li items
- Border-bottom entre items

## Cambios técnicos

- Eliminados todos los emojis de HTML (📋 📝 🎤 🗑️ ✌️ 👍 ✊ 🖐️ ✅ ⏳)
- SVG inline en títulos h2 con clase `.icon`
- SVG inline en botones (micrófono, papelera)
- SVG generado dinámicamente en `mostrarTabla()` para estados
- SVG en empty state con viewBox y path
- Caracteres Unicode simples para gestos (II, ↑, ●, ▢)
- CSS mejorado para `.gesture-icon` con border y padding

## Paleta SVG

- Stroke width: 2px (consistente)
- Checkmark verde: #10b981
- Reloj gris: #94a3b8
- Iconos heredan color con `currentColor`
- Opacity reducida en empty state (0.3)

## HTML limpio

Sin emojis, solo:
- SVG paths para iconos de interfaz
- Caracteres Unicode minimalistas para gestos
- Estructura semántica mejorada
- Meta description añadida
