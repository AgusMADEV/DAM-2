<?php
/**
 * Clase que permite generar PDFs profesionales usando la biblioteca FPDF.
 * Incluye soporte para tablas, logos, cabeceras, pies de página y estilos personalizados.
 */
class ReportGenerator {
    private $pdf;
    private $headerColor = [41, 128, 185]; // Azul profesional
    private $rowColor1 = [236, 240, 241]; // Gris claro
    private $rowColor2 = [255, 255, 255]; // Blanco
    private $textColor = [52, 73, 94]; // Gris oscuro
    private $logoPath = null;
    private $headerText = '';
    private $footerText = '';

    /**
     * Constructor de la clase. Inicializa una instancia de FPDF.
     */
    public function __construct() {
        require_once 'fpdf.php';
        $this->pdf = new FPDF();
        $this->pdf->SetAutoPageBreak(true, 20);
    }

    /**
     * Configura los colores del reporte.
     * 
     * @param array $headerColor RGB para cabecera [R, G, B]
     * @param array $rowColor1 RGB para filas alternas 1
     * @param array $rowColor2 RGB para filas alternas 2
     * @param array $textColor RGB para texto
     */
    public function setColors($headerColor, $rowColor1 = null, $rowColor2 = null, $textColor = null) {
        $this->headerColor = $headerColor;
        if ($rowColor1) $this->rowColor1 = $rowColor1;
        if ($rowColor2) $this->rowColor2 = $rowColor2;
        if ($textColor) $this->textColor = $textColor;
    }

    /**
     * Configura el logo del reporte.
     * 
     * @param string $logoPath Ruta al archivo de imagen del logo
     */
    public function setLogo($logoPath) {
        if (file_exists($logoPath)) {
            $this->logoPath = $logoPath;
        }
    }

    /**
     * Configura el texto de cabecera y pie de página.
     * 
     * @param string $header Texto para la cabecera
     * @param string $footer Texto para el pie de página
     */
    public function setHeaderFooter($header, $footer = '') {
        $this->headerText = $header;
        $this->footerText = $footer;
    }

    /**
     * Agrega una página con cabecera personalizada.
     */
    private function addPageWithHeader() {
        $this->pdf->AddPage();
        
        // Cabecera
        if ($this->logoPath) {
            $this->pdf->Image($this->logoPath, 10, 6, 30);
        }
        
        list($r, $g, $b) = $this->headerColor;
        $this->pdf->SetFillColor($r, $g, $b);
        $this->pdf->SetTextColor(255, 255, 255);
        $this->pdf->SetFont('Arial', 'B', 16);
        
        $startX = $this->logoPath ? 45 : 10;
        $this->pdf->SetXY($startX, 10);
        $this->pdf->Cell(0, 10, utf8_decode($this->headerText), 0, 1, 'L', true);
        
        // Restaurar color de texto
        list($r, $g, $b) = $this->textColor;
        $this->pdf->SetTextColor($r, $g, $b);
        $this->pdf->Ln(5);
    }

    /**
     * Establece el título del reporte.
     * 
     * @param string $title Título del reporte
     */
    public function setReportTitle($title) {
        $this->addPageWithHeader();
        $this->pdf->SetFont('Arial', 'B', 20);
        list($r, $g, $b) = $this->headerColor;
        $this->pdf->SetTextColor($r, $g, $b);
        $this->pdf->Cell(0, 15, utf8_decode($title), 0, 1, 'C');
        $this->pdf->Ln(5);
        
        // Restaurar color
        list($r, $g, $b) = $this->textColor;
        $this->pdf->SetTextColor($r, $g, $b);
    }

    /**
     * Agrega texto al PDF.
     * 
     * @param string $text Texto a agregar
     * @param int $size Tamaño de fuente (default: 12)
     * @param string $style Estilo de fuente: '', 'B', 'I', 'U' (default: '')
     */
    public function addText($text, $size = 12, $style = '') {
        $this->pdf->SetFont('Arial', $style, $size);
        $this->pdf->MultiCell(0, 6, utf8_decode($text));
        $this->pdf->Ln(3);
    }

    /**
     * Agrega una tabla con datos dinámicos.
     * 
     * @param array $headers Array con los nombres de las columnas
     * @param array $data Array de arrays con los datos de cada fila
     * @param array $widths Array con los anchos de cada columna (opcional)
     */
    public function addTable($headers, $data, $widths = null) {
        // Calcular anchos automáticamente si no se proporcionan
        if (!$widths) {
            $columnCount = count($headers);
            $pageWidth = 190; // Ancho útil de la página (210 - 20 márgenes)
            $widths = array_fill(0, $columnCount, $pageWidth / $columnCount);
        }

        // Cabecera de la tabla
        list($r, $g, $b) = $this->headerColor;
        $this->pdf->SetFillColor($r, $g, $b);
        $this->pdf->SetTextColor(255, 255, 255);
        $this->pdf->SetDrawColor(200, 200, 200);
        $this->pdf->SetLineWidth(0.3);
        $this->pdf->SetFont('Arial', 'B', 11);

        foreach ($headers as $i => $header) {
            $this->pdf->Cell($widths[$i], 8, utf8_decode($header), 1, 0, 'C', true);
        }
        $this->pdf->Ln();

        // Restaurar colores para datos
        list($r, $g, $b) = $this->textColor;
        $this->pdf->SetTextColor($r, $g, $b);
        $this->pdf->SetFont('Arial', '', 10);

        // Datos de la tabla con colores alternados
        $fill = false;
        foreach ($data as $row) {
            $color = $fill ? $this->rowColor1 : $this->rowColor2;
            list($r, $g, $b) = $color;
            $this->pdf->SetFillColor($r, $g, $b);

            foreach ($row as $i => $cell) {
                $this->pdf->Cell($widths[$i], 7, utf8_decode($cell), 1, 0, 'L', true);
            }
            $this->pdf->Ln();
            $fill = !$fill;
        }
        $this->pdf->Ln(5);
    }

    /**
     * Agrega una sección con título.
     * 
     * @param string $title Título de la sección
     */
    public function addSection($title) {
        $this->pdf->SetFont('Arial', 'B', 14);
        list($r, $g, $b) = $this->headerColor;
        $this->pdf->SetTextColor($r, $g, $b);
        $this->pdf->Cell(0, 10, utf8_decode($title), 0, 1, 'L');
        
        // Línea decorativa
        $this->pdf->SetDrawColor($r, $g, $b);
        $this->pdf->SetLineWidth(0.5);
        $this->pdf->Line(10, $this->pdf->GetY(), 200, $this->pdf->GetY());
        $this->pdf->Ln(5);
        
        // Restaurar color de texto
        list($r, $g, $b) = $this->textColor;
        $this->pdf->SetTextColor($r, $g, $b);
    }

    /**
     * Genera y descarga el PDF.
     * 
     * @param string $filename Nombre del archivo PDF
     * @param string $destination 'I' (inline), 'D' (download), 'F' (file), 'S' (string)
     */
    public function generatePDF($filename, $destination = 'I') {
        // Agregar pie de página si está configurado
        if ($this->footerText) {
            $this->pdf->SetY(-15);
            $this->pdf->SetFont('Arial', 'I', 8);
            $this->pdf->SetTextColor(128, 128, 128);
            $this->pdf->Cell(0, 10, utf8_decode($this->footerText), 0, 0, 'C');
        }

        try {
            $this->pdf->Output($destination, $filename);
        } catch (Exception $e) {
            die('Error al generar el PDF: ' . $e->getMessage());
        }
    }

    /**
     * Cierra y limpia la instancia de FPDF.
     */
    public function close() {
        $this->pdf->Close();
    }
}
?>
