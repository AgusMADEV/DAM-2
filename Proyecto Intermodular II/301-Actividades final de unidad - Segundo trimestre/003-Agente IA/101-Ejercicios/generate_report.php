<?php
/**
 * Generador simple de reportes PDF - Prueba básica
 */

require_once 'ReportGenerator.php';

// Crear reporte
$report = new ReportGenerator();

// Configuración
$report->setHeaderFooter('MI EMPRESA - REPORTE BÁSICO', 'Generado con ReportGenerator');

// Título
$report->setReportTitle('Lista de Usuarios Registrados');

// Descripción
$report->addText('Este es un ejemplo básico de reporte PDF generado con PHP y FPDF.', 10);
$report->addText('Fecha: ' . date('d/m/Y H:i:s'), 10, 'I');

// Sección
$report->addSection('Usuarios Activos');

// Tabla de usuarios
$headers = ['ID', 'Nombre', 'Email', 'Registro', 'Estado'];
$data = [
    ['001', 'Juan Pérez', 'juan@example.com', '15/01/2024', 'Activo'],
    ['002', 'María López', 'maria@example.com', '18/01/2024', 'Activo'],
    ['003', 'Carlos García', 'carlos@example.com', '20/01/2024', 'Activo'],
    ['004', 'Ana Martínez', 'ana@example.com', '22/01/2024', 'Inactivo'],
    ['005', 'Luis Rodríguez', 'luis@example.com', '25/01/2024', 'Activo']
];

$report->addTable($headers, $data);

// Estadísticas
$report->addSection('Estadísticas');
$report->addText('Total de usuarios: 5', 11, 'B');
$report->addText('Usuarios activos: 4 (80%)', 11);
$report->addText('Usuarios inactivos: 1 (20%)', 11);

// Generar PDF (inline en navegador)
$report->generatePDF('usuarios_' . date('Ymd') . '.pdf', 'I');
?>
