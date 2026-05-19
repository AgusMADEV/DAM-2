# Ejercicio Personal - Librería de Componentes UI
## Versión 1 - Básica

**Autor:** Agust�n Mateo  
**Curso:** DAM 2 - Desarrollo de Interfaces  
**Fecha:** 17 de febrero de 2026

## 📝 Descripción

Esta es mi versión personal del ejercicio de clase sobre creación de una librería de interfaces gráficas personalizada. El objetivo es demostrar control sobre los elementos de interfaz de usuario existentes y crear componentes personalizados tanto visual como funcionalmente.

## 🎯 Objetivo de la Versión 1

En esta primera versión básica implemento:

1. **Tarjetas de Estadísticas (StatsCard)** - Componente simple para mostrar datos clave
2. **Tabla Básica (SimpleTable)** - Tabla con datos estáticos
3. **Estilos básicos** - CSS con variables para personalización

## 📦 Componentes Incluidos

### 1. StatsCard
Tarjetas visuales para mostrar estadísticas o métricas importantes.

**Características:**
- Título y valor
- Icono opcional
- Colores personalizables
- Diseño responsive

### 2. SimpleTable
Tabla HTML mejorada con estilos personalizados.

**Características:**
- Cabeceras definibles
- Datos tabulares
- Estilos zebra para filas
- Responsive básico

## 🚀 Uso

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <link rel="stylesheet" href="agusmalab.css">
</head>
<body>
  <div id="tarjeta1"></div>
  <div id="tabla1"></div>
  
  <script src="agusmalab.js"></script>
  <script>
    new AgusmaLab.StatsCard('#tarjeta1', {
      titulo: 'Usuarios',
      valor: '1,234'
    });
    
    new AgusmaLab.SimpleTable('#tabla1', {
      columnas: ['Nombre', 'Email', 'Ciudad'],
      datos: [
        ['Ana García', 'ana@example.com', 'Madrid'],
        ['Carlos López', 'carlos@example.com', 'Barcelona']
      ]
    });
  </script>
</body>
</html>
```

## 🔄 Próximas Mejoras (v2)

- Agregar búsqueda a la tabla
- Implementar ordenamiento de columnas
- Añadir paginación
- Más tipos de gráficos
- Modo oscuro


