@echo off
REM Script de instalación rápida para Windows
REM Biblioteca Digital - Sistema Integral de Gestión de Datos

echo ================================================
echo    BIBLIOTECA DIGITAL - Instalacion Rapida
echo ================================================
echo.

echo Verificando Python...
python --version
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en PATH
    echo Por favor, instala Python 3.7 o superior
    pause
    exit /b 1
)

echo.
echo Instalando dependencias...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Fallo la instalacion de dependencias
    pause
    exit /b 1
)

echo.
echo ================================================
echo    Instalacion completada exitosamente!
echo ================================================
echo.
echo Para ejecutar el programa:
echo   python 006-programa_principal.py
echo.
pause
