# 002 - Animaciones CSS y Glassmorphism

## 🎨 Mejoras Implementadas

### Animaciones CSS

Se han implementado las siguientes animaciones mediante @keyframes:

1. **fadeIn** - Aparición suave con transición de opacidad
2. **scaleIn** - Aparición con escalado desde pequeño a tamaño normal
3. **slideIn** - Entrada deslizante desde la izquierda
4. **slideInDown** - Entrada deslizante desde arriba
5. **spin** - Rotación continua (usado en loader)
6. **pulse** - Pulsación suave (escalado rítmico)

### Efecto Glassmorphism

Se ha aplicado el efecto de cristal moderno (glassmorphism) a:

#### Panel de Controles (#controles)
- `backdrop-filter: blur(12px)` - Desenfoque del fondo
- `background: rgba(15, 23, 42, 0.75)` - Fondo semi-transparente
- Bordes con transparencia
- Sombras suaves

#### Modal (#modalCaja)
- `backdrop-filter: blur(16px)` - Desenfoque más intenso
- `background: rgba(30, 41, 59, 0.85)` - Fondo oscuro semi-transparente
- Bordes iluminados
- Animación de entrada con `scaleIn`

### Elementos Animados

1. **Panel de Control**: Animación `slideIn` al cargar
2. **Propiedades**: Cada bloque tiene `slideInDown` con delay escalonado
3. **Modal**: Animación `scaleIn` con efecto elástico
4. **Nodos 3D**: Componente personalizado `nodo-animado` que hace aparecer cada nodo con delay progresivo
5. **Loader**: Spinner animado con rotación continua

### Mejoras Visuales Adicionales

- **Scrollbars personalizados** con glassmorphism
- **Hover effects** en controles (scale, glow)
- **Sliders personalizados** con efectos luminosos
- **Botones con transiciones** suaves
- **Colores y sombras** mejorados con gradientes y glows
- **Tipografía mejorada** con sombras de texto

### Componente A-Frame Nuevo

**nodo-animado**: Componente que anima la aparición de nodos en la escena 3D
- Entrada escalonada basada en el índice del nodo
- Animación de escala con easing cúbico
- Transición suave de invisible a visible

## 🚀 Uso

Simplemente abre `index.html` en un navegador moderno y disfruta de:
- Animaciones suaves al cargar la interfaz
- Efecto cristal en paneles y modal
- Transiciones fluidas en todos los controles
- Aparición progresiva de los nodos 3D

## 🎯 Conceptos del Curso Aplicados

- **007 - Asociación de acciones a eventos**: Animaciones vinculadas a eventos de carga y interacción
- **004 - Diseño de interfaces**: Mejoras visuales modernas y atractivas
- **003 - Creación de componentes**: Componente A-Frame `nodo-animado` personalizado
- **CSS moderno**: Uso de backdrop-filter, custom properties, y animaciones avanzadas

## ⚡ Características Técnicas

- Compatible con navegadores modernos (Chrome, Firefox, Edge, Safari)
- Animaciones CSS nativas (mejor rendimiento)
- backdrop-filter para efectos de desenfoque reales
- Animaciones progresivas sin bloquear el thread principal
- Transiciones con easing personalizados

## 📝 Notas

El efecto glassmorphism requiere soporte de `backdrop-filter`. Navegadores compatibles:
- Chrome 76+
- Firefox 103+
- Safari 9+
- Edge 79+
