# Script para ejecutar el monitor de servidor continuamente
# Ejecuta el monitor cada 60 segundos

$pythonPath = "D:/xampp/htdocs/DAM-2/Desarrollo de interfaces/005-Creación de informes/002-Herramientas gráficas integradas en el IDE y externas al mismo/.venv/Scripts/python.exe"
$scriptPath = "d:\xampp\htdocs\DAM-2\Desarrollo de interfaces\005-Creación de informes\002-Herramientas gráficas integradas en el IDE y externas al mismo\102-Actividad EVAL\server_monitor.py"

Write-Host "🚀 Iniciando el monitor de servidor..." -ForegroundColor Green
Write-Host "📊 Los datos se guardarán en la carpeta monitor_data/" -ForegroundColor Cyan
Write-Host "⏱️  Ejecutando cada 60 segundos. Presiona Ctrl+C para detener." -ForegroundColor Yellow
Write-Host ""

$counter = 1
while ($true) {
    Write-Host "[$counter] Recopilando datos del sistema... " -NoNewline -ForegroundColor White
    $startTime = Get-Date
    
    try {
        Set-Location "d:\xampp\htdocs\DAM-2\Desarrollo de interfaces\005-Creación de informes\002-Herramientas gráficas integradas en el IDE y externas al mismo\102-Actividad EVAL"
        & $pythonPath $scriptPath
        $endTime = Get-Date
        $duration = ($endTime - $startTime).TotalSeconds
        Write-Host "✓ Completado en $([math]::Round($duration, 2))s" -ForegroundColor Green
    }
    catch {
        Write-Host "✗ Error: $_" -ForegroundColor Red
    }
    
    $counter++
    Start-Sleep -Seconds 60
}
