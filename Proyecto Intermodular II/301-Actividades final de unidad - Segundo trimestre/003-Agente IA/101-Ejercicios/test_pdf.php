<?php
/**
 * Archivo de prueba para generar un PDF profesional con tablas, estilos y datos de ejemplo.
 */

require_once 'ReportGenerator.php';

// Crear instancia del generador
$report = new ReportGenerator();

// Configurar colores personalizados (azul corporativo)
$report->setColors(
    [41, 128, 185],   // Cabecera: azul
    [236, 240, 241],  // Fila 1: gris claro
    [255, 255, 255],  // Fila 2: blanco
    [52, 73, 94]      // Texto: gris oscuro
);

// Configurar cabecera y pie de página
$report->setHeaderFooter(
    'INFORME DE VENTAS - EMPRESA XYZ',
    'Documento generado el ' . date('d/m/Y H:i') . ' - Página {nb}'
);

// Título del reporte
$report->setReportTitle('Reporte Mensual de Ventas');

// Agregar fecha y descripción
$report->addText('Fecha de generación: ' . date('d/m/Y'), 11, 'B');
$report->addText('Este reporte muestra las estadísticas de ventas del mes actual, incluyendo productos más vendidos y rendimiento por vendedor.', 10);

// Sección 1: Productos más vendidos
$report->addSection('Top 10 Productos Más Vendidos');

$headersProductos = ['#', 'Producto', 'Categoría', 'Unidades', 'Precio Unit.', 'Total'];
$datosProductos = [
    ['1', 'Laptop Dell XPS 15', 'Electrónica', '45', '€1,299.99', '€58,499.55'],
    ['2', 'iPhone 15 Pro Max', 'Móviles', '78', '€1,199.00', '€93,522.00'],
    ['3', 'Samsung Galaxy S24', 'Móviles', '62', '€999.00', '€61,938.00'],
    ['4', 'MacBook Pro M3', 'Electrónica', '34', '€2,499.00', '€84,966.00'],
    ['5', 'AirPods Pro 2', 'Accesorios', '156', '€279.00', '€43,524.00'],
    ['6', 'iPad Air 11"', 'Tablets', '89', '€649.00', '€57,761.00'],
    ['7', 'Sony WH-1000XM5', 'Audio', '123', '€399.00', '€49,077.00'],
    ['8', 'Monitor LG UltraWide', 'Periféricos', '45', '€549.00', '€24,705.00'],
    ['9', 'Teclado Mecánico Logitech', 'Periféricos', '234', '€129.00', '€30,186.00'],
    ['10', 'Mouse Logitech MX Master 3', 'Periféricos', '178', '€99.00', '€17,622.00']
];

$report->addTable($headersProductos, $datosProductos, [10, 50, 35, 25, 30, 30]);

// Sección 2: Rendimiento por vendedor
$report->addSection('Rendimiento por Vendedor');

$report->addText('A continuación se muestra el desempeño individual de cada vendedor durante el mes:', 10);

$headersVendedores = ['Vendedor', 'Ventas', 'Clientes', 'Comisión'];
$datosVendedores = [
    ['Ana García Martínez', '€125,340.00', '342', '€3,760.20'],
    ['Carlos López Ruiz', '€98,765.00', '287', '€2,962.95'],
    ['María Rodríguez Sánchez', '€156,890.00', '421', '€4,706.70'],
    ['Juan Fernández Torres', '€87,234.00', '245', '€2,617.02'],
    ['Laura Jiménez Morales', '€134,567.00', '389', '€4,037.01'],
    ['Pedro González Díaz', '€109,876.00', '312', '€3,296.28']
];

$report->addTable($headersVendedores, $datosVendedores, [60, 40, 35, 35]);

// Sección 3: Resumen ejecutivo
$report->addSection('Resumen Ejecutivo');

$report->addText('Ventas Totales del Mes: €712,672.00', 12, 'B');
$report->addText('Total de Transacciones: 1,996', 11);
$report->addText('Ticket Medio: €356.94', 11);
$report->addText('Incremento respecto al mes anterior: +12.5%', 11, 'B');

$report->addText('', 10);
$report->addText('Observaciones:', 11, 'B');
$report->addText('• Los productos de gama alta (Laptop, MacBook, iPhone) representan el 65% de los ingresos totales.', 10);
$report->addText('• María Rodríguez lidera en ventas con €156,890 y 421 clientes atendidos.', 10);
$report->addText('• Los accesorios (AirPods, teclados, ratones) muestran un alto volumen de unidades vendidas.', 10);
$report->addText('• Se recomienda aumentar el stock de productos más vendidos para el próximo mes.', 10);

// Generar y descargar el PDF
$report->generatePDF('reporte_ventas_' . date('Y-m-d') . '.pdf', 'I');
$report->close();

echo "PDF generado correctamente. Si no se descarga automáticamente, verifica la configuración de tu navegador.";
?>
