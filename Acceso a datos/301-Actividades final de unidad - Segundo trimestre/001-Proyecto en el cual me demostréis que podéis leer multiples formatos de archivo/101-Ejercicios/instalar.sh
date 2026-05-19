#!/bin/bash
# Script de instalación rápida para Linux/Mac
# Biblioteca Digital - Sistema Integral de Gestión de Datos

echo "================================================"
echo "   BIBLIOTECA DIGITAL - Instalación Rápida"
echo "================================================"
echo ""

echo "Verificando Python..."
python3 --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python no está instalado"
    echo "Por favor, instala Python 3.7 o superior"
    exit 1
fi

echo ""
echo "Instalando dependencias..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Falló la instalación de dependencias"
    exit 1
fi

echo ""
echo "================================================"
echo "   Instalación completada exitosamente!"
echo "================================================"
echo ""
echo "Para ejecutar el programa:"
echo "  python3 006-programa_principal.py"
echo ""
