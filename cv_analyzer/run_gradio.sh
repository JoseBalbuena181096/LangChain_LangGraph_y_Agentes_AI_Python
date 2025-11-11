#!/bin/bash

# Script para ejecutar el analizador de CVs con Gradio

echo "🚀 Iniciando Sistema de Evaluación de CVs con Gradio..."
echo ""
echo "📋 Verificando dependencias..."

# Verificar si Gradio está instalado
if python -c "import gradio" &> /dev/null; then
    echo "✅ Gradio instalado"
else
    echo "❌ Gradio no encontrado"
    echo "📦 Instalando Gradio..."
    pip install gradio
fi

# Verificar otras dependencias
if python -c "import langchain" &> /dev/null; then
    echo "✅ LangChain instalado"
else
    echo "⚠️  LangChain no encontrado. Instalando todas las dependencias..."
    pip install -r requirements.txt
fi

echo ""
echo "🔧 Verificando configuración..."

# Verificar archivo .env
if [ -f ".env" ]; then
    echo "✅ Archivo .env encontrado"
else
    echo "⚠️  Archivo .env no encontrado"
    echo "📝 Por favor crea un archivo .env basado en .env.example"
    echo ""
    read -p "¿Deseas continuar de todos modos? (s/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "🌐 Iniciando servidor Gradio..."
echo "🔗 La aplicación estará disponible en: http://localhost:7860"
echo "⚠️  Presiona Ctrl+C para detener"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Ejecutar la aplicación
python app_gradio.py
