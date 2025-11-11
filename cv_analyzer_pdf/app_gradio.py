"""
Sistema de Evaluación de CVs con IA - Versión Gradio

Este script ejecuta la aplicación con interfaz Gradio.
Incluye opción para compartir públicamente la aplicación.
"""

import sys
from pathlib import Path
import argparse

# Agregar el directorio raíz al path para importaciones
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from ui.gradio_ui import main

if __name__ == "__main__":
    # Configurar argumentos de línea de comandos
    parser = argparse.ArgumentParser(description='Sistema de Evaluación de CVs con Gradio')
    parser.add_argument(
        '--share',
        action='store_true',
        help='Crear enlace público para compartir la aplicación (válido por 72 horas)'
    )
    parser.add_argument(
        '--no-share',
        action='store_true',
        help='No compartir públicamente (solo local)'
    )
    
    args = parser.parse_args()
    
    # Determinar si se debe compartir (por defecto TRUE)
    # Solo será False si se usa --no-share explícitamente
    share = not args.no_share
    
    print("=" * 60)
    print("🚀 Iniciando Sistema de Evaluación de CVs con Gradio")
    print("=" * 60)
    print("")
    
    if share:
        print("🌐 Modo: PÚBLICO - Generando enlace compartible")
        print("⏱️  El enlace será válido por 72 horas")
        print("⚠️  Cualquiera con el enlace podrá usar la aplicación")
    else:
        print("🏠 Modo: LOCAL - Solo accesible desde tu red")
        print("💡 Usa --share para generar un enlace público")
    
    print("")
    print("📊 La aplicación se abrirá automáticamente")
    print("🔗 URL Local: http://localhost:7860")
    print("")
    print("⚠️  Presiona Ctrl+C para detener el servidor")
    print("=" * 60)
    print("")
    
    main(share=share)
