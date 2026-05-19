# Ejercicio Personal - Librería de Componentes UI
## Versión 2

**Autor:** Agust�n Mateo  
**Curso:** DAM 2 - Desarrollo de Interfaces  
**Fecha:** 17 de febrero de 2026

## 📝 Descripción

Esta versión de la librería incluye funcionalidades interactivas y un componente de gráficos.

## 🎯 Características de la Versión 2

### ✨ Componentes Existentes

1. **SimpleTable → DataTable**
   - ✅ Búsqueda en tiempo real
   - ✅ Ordenamiento por columnas (asc/desc)
   - ✅ Paginación básica
   - ✅ Contador de registros

2. **StatsCard**
   - ✅ Animaciones al actualizar valores
   - ✅ Indicador de cambio (positivo/negativo)
   - ✅ Métodos públicos para actualización

### 📦 Componentes Adicionales

3. **BarChart**
   - Gráfico de barras con Canvas
   - Colores personalizables
   - Etiquetas y valores
   - Responsive

4. **SearchBox**
   - Campo de búsqueda reutilizable
   - Debounce para optimizar
   - Eventos personalizados

## 📦 Componentes Disponibles

### StatsCard
```javascript
const card = new AgusmaLab.StatsCard('#tarjeta', {
  titulo: 'Ventas',
  valor: '€1,234',
  icono: '💰',
  colorIcono: 'success',
  cambio: '+12%',
  tipoCambio: 'positivo'
});

// Métodos
card.actualizarValor('€2,500');
card.mostrarCambio('+25%', 'positivo');
```

### DataTable
```javascript
const tabla = new AgusmaLab.DataTable('#tabla', {
  titulo: 'Usuarios',
  columnas: [
    { campo: 'nombre', etiqueta: 'Nombre', ordenable: true },
    { campo: 'email', etiqueta: 'Email' }
  ],
  datos: [...],
  busqueda: true,
  ordenamiento: true,
  paginacion: true,
  filasPorPagina: 10
});
```

### BarChart
```javascript
new AgusmaLab.BarChart('#grafico', {
  titulo: 'Ventas Mensuales',
  etiquetas: ['Ene', 'Feb', 'Mar', 'Abr', 'May'],
  datos: [120, 150, 180, 140, 200],
  color: '#3b82f6',
  ancho: 600,
  alto: 300
});
```

## 🔄 Próximas Mejoras (v3)

- Más tipos de gráficos (líneas, pastel)
- Formularios personalizados
- Modales y notificaciones
- Modo oscuro completo
- Temas personalizables
- Exportación de datos (CSV, JSON)


