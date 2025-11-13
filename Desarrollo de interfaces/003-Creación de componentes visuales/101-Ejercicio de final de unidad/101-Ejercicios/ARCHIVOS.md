# 📦 Estructura del Proyecto UILib v1.0

## Archivos de la Librería

### Archivos Principales (Obligatorios)
```
uilib.css           → Estilos de todos los componentes (CSS puro)
uilib.js            → Lógica de todos los componentes (JavaScript vanilla)
```

## Documentación

```
README.md           → Documentación completa de la librería
GUIA-RAPIDA.md      → Tutorial rápido de integración (5 minutos)
ARCHIVOS.md         → Este archivo (índice del proyecto)
```

## Ejemplos de Uso

### 1. Demo Básica
```
index.html          → Demostración de todos los componentes
                      - Uso educativo
                      - Ejemplos de código
                      - Referencia visual
```

### 2. Sistema de Gestión Empresarial
```
ejemplo-proyecto-real.html
                    → Aplicación empresarial completa
                      - Dashboard con KPIs
                      - CRUD de empleados
                      - Gestión de productos
                      - Gestión de ventas
                      - Informes corporativos
                      - Navegación multi-tab
                      - Formularios complejos
```

### 3. E-Commerce Dashboard
```
ejemplo-ecommerce.html
                    → Panel analítico para tienda online
                      - KPIs de negocio
                      - Análisis de ventas
                      - Gestión de pedidos
                      - Filtros dinámicos
                      - Ranking de productos
                      - Informes automáticos
```

## Cómo Usar Este Proyecto

### Para Aprender
1. Abre `index.html` → Ver todos los componentes
2. Lee `README.md` → Documentación completa
3. Consulta `GUIA-RAPIDA.md` → Tutorial paso a paso

### Para Integrar en Tu Proyecto
1. Copia `uilib.css` y `uilib.js` a tu proyecto
2. Sigue la guía en `GUIA-RAPIDA.md`
3. Consulta los ejemplos según tu caso de uso:
   - Sistema administrativo → `ejemplo-proyecto-real.html`
   - E-commerce → `ejemplo-ecommerce.html`
   - Referencia API → `README.md`

### Para Desarrolladores

#### Modificar la Librería
```
uilib.css           → Editar estilos base
uilib.js            → Editar componentes o añadir nuevos
```

#### Probar Cambios
```bash
# Abre cualquier ejemplo en el navegador
index.html
ejemplo-proyecto-real.html
ejemplo-ecommerce.html
```

## Componentes Incluidos

### 1. DataTable
- **Archivo**: `uilib.js` (líneas ~35-270)
- **Estilos**: `uilib.css` (líneas ~75-190)
- **Características**:
  - Búsqueda en tiempo real
  - Ordenamiento por columnas
  - Paginación configurable
  - Columnas personalizables con render
  - Responsive

### 2. SearchableSelect
- **Archivo**: `uilib.js` (líneas ~275-430)
- **Estilos**: `uilib.css` (líneas ~195-265)
- **Características**:
  - Búsqueda con teclado
  - Insensible a diacríticos
  - Navegación con flechas
  - Basado en `<select>` nativo

### 3. BarChart
- **Archivo**: `uilib.js` (líneas ~435-545)
- **Estilos**: `uilib.css` (líneas ~310-330)
- **Características**:
  - Renderizado con Canvas
  - Valores sobre barras
  - Ejes y escalas automáticas
  - Responsive

### 4. StatsCard
- **Archivo**: `uilib.js` (líneas ~550-610)
- **Estilos**: `uilib.css` (líneas ~335-400)
- **Características**:
  - Icono personalizable
  - Cambio porcentual (positivo/negativo)
  - 5 variantes de color
  - Hover effect

### 5. ReportPanel
- **Archivo**: `uilib.js` (líneas ~615-670)
- **Estilos**: `uilib.css` (líneas ~405-445)
- **Características**:
  - Header, body, footer
  - Contenido HTML o DOM
  - Estructura semántica

## Tamaño de los Archivos

```
uilib.css           → ~13 KB (CSS sin comprimir)
uilib.js            → ~21 KB (JavaScript sin comprimir)
Total               → ~34 KB
```

**Comprimido (minificado):**
```
uilib.min.css       → ~8 KB estimado
uilib.min.js        → ~10 KB estimado
Total minificado    → ~18 KB
```

## Dependencias

**Cero dependencias externas**
- ✅ No requiere jQuery
- ✅ No requiere Bootstrap
- ✅ No requiere React/Vue/Angular
- ✅ JavaScript vanilla puro
- ✅ CSS moderno nativo

## Compatibilidad

### Navegadores Soportados
- ✅ Chrome/Edge (últimas 2 versiones)
- ✅ Firefox (últimas 2 versiones)
- ✅ Safari (últimas 2 versiones)
- ✅ Opera (últimas 2 versiones)

### Características Usadas
- CSS Grid
- CSS Custom Properties (variables)
- ES6 Classes
- Arrow Functions
- Template Literals
- Array Methods (map, filter, reduce)
- Canvas API
- DOM Manipulation

## Checklist de Integración

Cuando integres UILib en tu proyecto, verifica:

- [ ] Copiaste `uilib.css` y `uilib.js`
- [ ] Enlazaste CSS en el `<head>`
- [ ] Enlazaste JS antes de `</body>`
- [ ] Los IDs de tus contenedores son únicos
- [ ] Inicializas componentes después de que el DOM esté listo
- [ ] Probaste en diferentes navegadores
- [ ] El responsive funciona correctamente

## Próximos Pasos

### Extensiones Futuras
- [ ] LineChart (gráfico de líneas)
- [ ] PieChart (gráfico circular)
- [ ] Modal/Dialog
- [ ] Tabs component
- [ ] Notification/Toast
- [ ] DatePicker
- [ ] Versión minificada

### Mejoras Posibles
- [ ] TypeScript definitions
- [ ] NPM package
- [ ] CDN hosting
- [ ] Temas predefinidos
- [ ] Accesibilidad ARIA mejorada

## Contacto y Soporte

Este es un proyecto educativo para DAM-2.

- **Asignatura**: Desarrollo de Interfaces
- **Unidad**: 003 - Creación de Componentes Visuales
- **Criterios cumplidos**:
  - ✅ Componentes de tabla
  - ✅ Componentes de formularios
  - ✅ Componentes de gráficas
  - ✅ Componentes de informes
  - ✅ Integrables y reutilizables
  - ✅ Librería HTML-CSS-JS

---

**Última actualización**: 12 de noviembre de 2025  
**Versión**: 1.0.0
