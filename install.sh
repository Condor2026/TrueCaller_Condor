#!/bin/bash
# install.sh - Instalación automática de TrueCall_Condor

echo "🦅 TrueCall_Condor - Instalación"
echo "================================"

# Detectar sistema
if [ -f /data/data/com.termux/files/usr/bin/termux-info ]; then
    echo "📱 Termux detectado"
    pkg update -y
    pkg install python -y
elif [ -f /etc/debian_version ]; then
    echo "🐧 Debian/Ubuntu detectado"
    sudo apt update
    sudo apt install python3 python3-pip -y
else
    echo "⚠️  Sistema no soportado. Instala Python 3 y pip manualmente."
fi

echo "📦 Instalando dependencias Python..."
pip install -r requirements.txt

echo "📁 Creando carpetas..."
mkdir -p reports assets

echo "✅ Instalación completada. Ejecuta: python3 truecall_condor.py"
