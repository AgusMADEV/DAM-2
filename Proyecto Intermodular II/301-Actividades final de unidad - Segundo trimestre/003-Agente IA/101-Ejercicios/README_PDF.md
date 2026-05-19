# 📄 Sistema Generador de Reportes PDF con PHP

## ✅ Archivos incluidos

1. **ReportGenerator.php** - Clase principal para generar PDFs profesionales
2. **fpdf.php** - Librería FPDF (ya descargada e instalada)
3. **test_pdf.php** - Ejemplo completo con reporte de ventas
4. **generate_report.php** - Ejemplo simple con lista de usuarios

## 🚀 Cómo usar

### Opción 1: Probar el ejemplo completo

Abre en tu navegador:
```
http://localhost/dam-2/Proyecto%20Intermodular%20II/301-Actividades%20final%20de%20unidad%20-%20Segundo%20trimestre/003-Agente%20IA/101-Ejercicios/test_pdf.php
```

Esto generará un PDF profesional con:
- ✅ Tablas con datos de ventas
- ✅ Colores y estilos personalizados
- ✅ Múltiples secciones
- ✅ Cabecera y pie de página
- ✅ Filas alternadas en colores

### Opción 2: Probar el ejemplo simple

```
http://localhost/dam-2/Proyecto%20Intermodular%20II/301-Actividades%20final%20de%20unidad%20-%20Segundo%20trimestre/003-Agente%20IA/101-Ejercicios/generate_report.php
```

Genera un PDF básico con lista de usuarios.

## 📖 Ejemplo de código

```php
<?php
require_once 'ReportGenerator.php';

// Crear instancia
$report = new ReportGenerator();

// Configurar colores (opcional)
$report->setColors(
    [41, 128, 185],   // Cabecera azul
    [236, 240, 241],  // Fila gris claro
    [255, 255, 255],  // Fila blanca
    [52, 73, 94]      // Texto gris oscuro
);

// Título
$report->setReportTitle('Mi Reporte');

// Agregar texto
$report->addText('Este es un párrafo de texto.', 12);

// Agregar tabla
$headers = ['Nombre', 'Email', 'Edad'];
$data = [
    ['Juan', 'juan@example.com', '25'],
    ['Ana', 'ana@example.com', '30']
];
$report->addTable($headers, $data);

// Generar PDF
$report->generatePDF('mi_reporte.pdf', 'I'); // 'I' = mostrar en navegador
?>
```

## 🎨 Características principales

### Métodos disponibles

| Método | Descripción |
|--------|-------------|
| `setColors($header, $row1, $row2, $text)` | Personaliza colores RGB |
| `setLogo($path)` | Agrega logo en cabecera |
| `setHeaderFooter($header, $footer)` | Configura encabezado y pie |
| `setReportTitle($title)` | Establece título principal |
| `addText($text, $size, $style)` | Agrega párrafos de texto |
| `addTable($headers, $data, $widths)` | Crea tablas con datos |
| `addSection($title)` | Agrega sección con línea decorativa |
| `generatePDF($filename, $destination)` | Genera el PDF |

### Opciones de salida

- **'I'** - Inline: Muestra en navegador
- **'D'** - Download: Descarga directa
- **'F'** - File: Guarda en servidor
- **'S'** - String: Retorna como string

## 📦 Sobre FPDF

**FPDF** es una librería PHP que permite generar archivos PDF:

- ✅ No requiere instalación de extensiones PHP
- ✅ Ligera y rápida
- ✅ Compatible con PHP 5+
- ✅ Soporta UTF-8 (con `utf8_decode()`)
- ✅ Permite tablas, imágenes, colores y estilos

**Sitio oficial:** http://www.fpdf.org

## 🔧 Solución de problemas

### Error: "Class 'FPDF' not found"
- Verifica que `fpdf.php` esté en el mismo directorio
- O ajusta la ruta en `require_once 'fpdf.php'`

### PDF se descarga en blanco
- Verifica que no haya salida HTML antes de generar el PDF
- Usa `ob_clean()` antes de `$report->generatePDF()` si es necesario

### Caracteres con tildes se ven mal
- Usa `utf8_decode()` en tus textos (ya incluido en la clase)
- O configura FPDF para UTF-8 completo

## ✨ Ejemplos de uso avanzado

### Cambiar colores corporativos

```php
// Verde corporativo
$report->setColors([39, 174, 96], [236, 240, 241], [255, 255, 255], [44, 62, 80]);

// Rojo corporativo
$report->setColors([231, 76, 60], [242, 242, 242], [255, 255, 255], [52, 52, 52]);
```

### Guardar en archivo en lugar de mostrar

```php
$report->generatePDF('reporte.pdf', 'F'); // Guarda en servidor
echo "PDF guardado correctamente en reporte.pdf";
```

### Forzar descarga

```php
$report->generatePDF('reporte.pdf', 'D'); // Descarga inmediata
```

## 📊 Resultado esperado

Al ejecutar `test_pdf.php` o `generate_report.php`, deberías ver:

1. **Cabecera** con título y colores personalizados
2. **Secciones** con líneas decorativas
3. **Tablas** con filas alternadas en colores
4. **Texto** con diferentes tamaños y estilos
5. **Pie de página** con información adicional

---

**✅ Sistema completado exitosamente**

Todos los archivos necesarios están listos y funcionales. Solo abre los archivos PHP en tu navegador para ver los PDFs generados.
