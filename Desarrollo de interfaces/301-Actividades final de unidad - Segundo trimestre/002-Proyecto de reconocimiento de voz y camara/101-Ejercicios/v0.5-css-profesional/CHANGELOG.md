# v0.5 - CSS profesional con variables + glassmorphism

## Nuevas características visuales

✅ **Sistema de CSS Variables**
- Variables CSS en `:root` para todos los colores y medidas
- Colores: primary, secondary, accent, success, warning, danger
- Sombras: sm, md, lg
- Fácil personalización y mantenimiento

✅ **Glassmorphism**
- `backdrop-filter: blur(20px)` en paneles
- Fondos translúcidos con `rgba(255, 255, 255, 0.7)`
- Soporte webkit para Safari
- Efecto cristal moderno y elegante

✅ **Tipografía profesional**
- Google Fonts: Inter (300, 400, 500, 600)
- Letter spacing optimizado (-0.025em en h1)
- Jerarquía visual mejorada
- Tamaños relativos (em/rem)

✅ **Layout Grid mejorado**
- CSS Grid con 2 columnas (main: 1fr, sidebar: 420px)
- Gap de 24px entre paneles
- Responsive: 1 columna en móviles

✅ **Componentes mejorados**
- Botones con estados hover, active y transiciones
- Transform translateY en hover (-1px)
- Tabla con border-radius y overflow hidden
- Status boxes con altura mínima
- Empty state centrado con iconos grandes

✅ **Sombras y profundidad**
- Box-shadow en 3 niveles (sm, md, lg)
- Hover state con elevación mejorada
- Sombras sutiles en bordes

✅ **Animaciones y transiciones**
- Transiciones suaves (0.2s ease, 0.15s ease)
- Hover effects en tr, buttons, panels
- Active state en botones

✅ **Responsive Design**
- Media query 1200px: 1 columna
- Media query 768px: padding reducido, fuentes ajustadas
- Grid gap adaptativo

## Cambios técnicos CSS

- Import de Google Fonts Inter
- 13 variables CSS en :root
- backdrop-filter + -webkit-backdrop-filter
- border-collapse: separate para border-radius en tabla
- text-transform: uppercase en th
- Grid layout con minmax
- Empty state con iconos grandes (3em)

## Paleta de colores

- Background: #f8f9fa (gris muy claro)
- Surface: #ffffff (blanco)
- Glass: rgba(255, 255, 255, 0.7)
- Text primary: #1a1a1a (casi negro)
- Text secondary: #6b7280 (gris medio)
- Accent: #2563eb (azul)
- Success: #10b981 (verde)
- Warning: #f59e0b (naranja)
