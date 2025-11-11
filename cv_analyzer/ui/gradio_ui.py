import gradio as gr
from models.cv_model import AnalisisCV
from services.pdf_processor import extraer_texto_pdf
from services.cv_evaluator import evaluar_candidato
import time


def procesar_cv(archivo_pdf, descripcion_puesto, progress=gr.Progress()):
    """
    Procesa el CV y la descripción del puesto, retorna el análisis formateado.
    
    Args:
        archivo_pdf: Archivo PDF subido por el usuario
        descripcion_puesto: Texto con la descripción del puesto
        progress: Objeto Progress de Gradio para mostrar retroalimentación
        
    Returns:
        tuple: (html_resultado, visibilidad_resultados, estado_mensaje)
    """
    
    # Validaciones iniciales
    progress(0, desc="🔍 Validando datos de entrada...")
    time.sleep(0.3)
    
    if archivo_pdf is None:
        mensaje_error = "⚠️ **Por favor sube un archivo PDF** con el currículum del candidato"
        return mensaje_error, gr.update(visible=False), gr.update(value=mensaje_error, visible=True)
    
    if not descripcion_puesto or descripcion_puesto.strip() == "":
        mensaje_error = "⚠️ **Por favor proporciona una descripción detallada** del puesto de trabajo"
        return mensaje_error, gr.update(visible=False), gr.update(value=mensaje_error, visible=True)
    
    try:
        # Actualizar estado inicial visible
        mensaje_inicial = "🔄 **Procesando...** Extrayendo texto del PDF"
        
        # Actualizar estado
        progress(0.1, desc="📄 Iniciando procesamiento del PDF...")
        time.sleep(0.2)
        
        # Variable para capturar progreso del PDF
        progreso_actual = {"mensaje": "", "porcentaje": 0}
        
        def callback_progreso(mensaje, porcentaje):
            """Callback para actualizar progreso durante extracción de PDF"""
            progreso_actual["mensaje"] = mensaje
            progreso_actual["porcentaje"] = porcentaje
            # Normalizar porcentaje (0-100 -> 0.1-0.5 para la primera mitad del proceso)
            progress(0.1 + (porcentaje / 100) * 0.4, desc=mensaje)
        
        # Extraer texto del PDF con feedback
        texto_cv = extraer_texto_pdf(archivo_pdf, progress_callback=callback_progreso)
        
        # Verificar errores en la extracción
        if texto_cv.startswith("Error"):
            mensaje_error = f"❌ **Error al procesar el PDF:**\n\n{texto_cv}"
            progress(1.0, desc="❌ Error en el procesamiento")
            html_error = f"<div style='padding:20px; background-color:#FEE2E2; border-radius:10px; border-left:5px solid #DC2626;'><h3 style='color:#991B1B; margin-top:0;'>❌ Error</h3><p style='color:#991B1B;'>{texto_cv}</p></div>"
            return html_error, gr.update(visible=True), gr.update(value=mensaje_error, visible=True)
        
        # PDF procesado exitosamente
        progress(0.55, desc="✅ PDF procesado correctamente")
        time.sleep(0.2)
        
        # Preparar análisis con IA
        progress(0.6, desc="🤖 Conectando con el modelo de IA...")
        time.sleep(0.3)
        
        progress(0.7, desc="🧠 Analizando currículum con inteligencia artificial...")
        time.sleep(0.3)
        
        # Evaluar candidato
        resultado = evaluar_candidato(texto_cv, descripcion_puesto)
        
        progress(0.85, desc="📊 Generando reporte de análisis...")
        time.sleep(0.2)
        
        # Generar HTML con los resultados
        html_resultado = generar_html_resultados(resultado)
        
        progress(1.0, desc="✅ ¡Análisis completado exitosamente!")
        
        mensaje_exito = f"✅ **Análisis completado** - Porcentaje de ajuste: {resultado.porcentaje_ajuste}%"
        
        return html_resultado, gr.update(visible=True), gr.update(value=mensaje_exito, visible=True)
        
    except Exception as e:
        mensaje_error = f"❌ **Error inesperado:**\n\n{str(e)}\n\nPor favor, verifica el archivo PDF y la descripción del puesto e intenta nuevamente."
        progress(1.0, desc="❌ Error durante el procesamiento")
        html_error = f"<div style='padding:20px; background-color:#FEE2E2; border-radius:10px; border-left:5px solid #DC2626;'><h3 style='color:#991B1B; margin-top:0;'>❌ Error Inesperado</h3><p style='color:#991B1B;'>{str(e)}</p><p style='color:#991B1B; font-size:0.9em;'>Por favor, verifica el archivo PDF y la descripción del puesto e intenta nuevamente.</p></div>"
        return html_error, gr.update(visible=True), gr.update(value=mensaje_error, visible=True)


def generar_html_resultados(resultado: AnalisisCV):
    """
    Genera un HTML formateado con los resultados del análisis.
    
    Args:
        resultado: Objeto AnalisisCV con los datos del análisis
        
    Returns:
        str: HTML formateado con los resultados
    """
    
    # Determinar nivel y color según porcentaje
    if resultado.porcentaje_ajuste >= 80:
        color = "#10b981"  # Verde
        nivel = "EXCELENTE"
        icono = "🟢"
        mensaje = "Candidato altamente recomendado"
        recomendacion = """
        <div style="background-color: #d1fae5; padding: 20px; border-radius: 10px; border-left: 5px solid #10b981;">
            <h3 style="color: #065f46; margin-top: 0;">✅ CANDIDATO RECOMENDADO</h3>
            <p style="color: #065f46; margin-bottom: 0;">
                El perfil del candidato está bien alineado con los requisitos del puesto. 
                Se recomienda proceder con las siguientes etapas del proceso de selección.
            </p>
        </div>
        """
    elif resultado.porcentaje_ajuste >= 60:
        color = "#fbbf24"  # Amarillo
        nivel = "BUENO"
        icono = "🟡"
        mensaje = "Candidato recomendado con reservas"
        recomendacion = """
        <div style="background-color: #fef3c7; padding: 20px; border-radius: 10px; border-left: 5px solid #fbbf24;">
            <h3 style="color: #92400e; margin-top: 0;">⚠️ CANDIDATO CON POTENCIAL</h3>
            <p style="color: #92400e; margin-bottom: 0;">
                El candidato muestra potencial pero requiere evaluación adicional. 
                Se recomienda una entrevista técnica para validar competencias específicas.
            </p>
        </div>
        """
    elif resultado.porcentaje_ajuste >= 40:
        color = "#f97316"  # Naranja
        nivel = "REGULAR"
        icono = "🟠"
        mensaje = "Candidato requiere evaluación adicional"
        recomendacion = """
        <div style="background-color: #fed7aa; padding: 20px; border-radius: 10px; border-left: 5px solid #f97316;">
            <h3 style="color: #7c2d12; margin-top: 0;">⚠️ CANDIDATO CON POTENCIAL</h3>
            <p style="color: #7c2d12; margin-bottom: 0;">
                El candidato muestra potencial pero requiere evaluación adicional. 
                Se recomienda una entrevista técnica para validar competencias específicas.
            </p>
        </div>
        """
    else:
        color = "#ef4444"  # Rojo
        nivel = "BAJO"
        icono = "🔴"
        mensaje = "Candidato no recomendado"
        recomendacion = """
        <div style="background-color: #fee2e2; padding: 20px; border-radius: 10px; border-left: 5px solid #ef4444;">
            <h3 style="color: #991b1b; margin-top: 0;">❌ CANDIDATO NO RECOMENDADO</h3>
            <p style="color: #991b1b; margin-bottom: 0;">
                El perfil no se alinea suficientemente con los requisitos del puesto. 
                Se recomienda continuar la búsqueda de candidatos más adecuados.
            </p>
        </div>
        """
    
    # Generar HTML para habilidades
    habilidades_html = ""
    if resultado.habilidades_clave:
        for habilidad in resultado.habilidades_clave:
            habilidades_html += f'<span style="display: inline-block; background-color: #10b981; color: white; padding: 8px 16px; border-radius: 20px; margin: 5px; font-weight: bold;">✅ {habilidad}</span>'
    else:
        habilidades_html = "<p style='color: #666;'>No se identificaron habilidades técnicas específicas</p>"
    
    # Generar HTML para fortalezas
    fortalezas_html = ""
    if resultado.fortalezas:
        for i, fortaleza in enumerate(resultado.fortalezas, 1):
            fortalezas_html += f"<p style='margin: 10px 0;'><strong>{i}.</strong> {fortaleza}</p>"
    else:
        fortalezas_html = "<p style='color: #666;'>No se identificaron fortalezas específicas</p>"
    
    # Generar HTML para áreas de mejora
    areas_mejora_html = ""
    if resultado.areas_mejora:
        for i, area in enumerate(resultado.areas_mejora, 1):
            areas_mejora_html += f"<p style='margin: 10px 0;'><strong>{i}.</strong> {area}</p>"
    else:
        areas_mejora_html = "<p style='color: #666;'>No se identificaron áreas de mejora específicas</p>"
    
    # Construir el HTML completo
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto;">
        
        <!-- Evaluación Principal -->
        <div style="text-align: center; margin-bottom: 30px;">
            <h2 style="color: #1f2937; margin-bottom: 10px;">🎯 Evaluación Principal</h2>
            <div style="background-color: #f9fafb; padding: 30px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <div style="font-size: 48px; font-weight: bold; color: {color}; margin-bottom: 10px;">
                    {resultado.porcentaje_ajuste}%
                </div>
                <div style="font-size: 24px; color: {color}; font-weight: bold; margin-bottom: 5px;">
                    {icono} {nivel}
                </div>
                <div style="font-size: 18px; color: #4b5563;">
                    {mensaje}
                </div>
            </div>
        </div>
        
        <hr style="border: none; border-top: 2px solid #e5e7eb; margin: 30px 0;">
        
        <!-- Perfil del Candidato -->
        <h2 style="color: #1f2937;">👤 Perfil del Candidato</h2>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 30px;">
            <div style="background-color: #dbeafe; padding: 15px; border-radius: 10px;">
                <strong>👨‍💼 Nombre:</strong> {resultado.nombre_candidato}
            </div>
            <div style="background-color: #dbeafe; padding: 15px; border-radius: 10px;">
                <strong>⏱️ Experiencia:</strong> {resultado.experiencia_años} años
            </div>
        </div>
        <div style="background-color: #dbeafe; padding: 15px; border-radius: 10px; margin-bottom: 30px;">
            <strong>🎓 Educación:</strong> {resultado.education}
        </div>
        
        <!-- Experiencia Relevante -->
        <h2 style="color: #1f2937;">💼 Experiencia Relevante</h2>
        <div style="background-color: #dbeafe; padding: 20px; border-radius: 10px; margin-bottom: 30px;">
            <p style="margin: 0; line-height: 1.6;">{resultado.experiencia_relevante}</p>
        </div>
        
        <hr style="border: none; border-top: 2px solid #e5e7eb; margin: 30px 0;">
        
        <!-- Habilidades -->
        <h2 style="color: #1f2937;">🛠️ Habilidades Técnicas Clave</h2>
        <div style="margin-bottom: 30px;">
            {habilidades_html}
        </div>
        
        <hr style="border: none; border-top: 2px solid #e5e7eb; margin: 30px 0;">
        
        <!-- Fortalezas y Áreas de Mejora -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 30px;">
            <div>
                <h2 style="color: #1f2937;">💪 Fortalezas Principales</h2>
                <div style="background-color: #f9fafb; padding: 20px; border-radius: 10px; min-height: 200px;">
                    {fortalezas_html}
                </div>
            </div>
            <div>
                <h2 style="color: #1f2937;">📈 Áreas de Desarrollo</h2>
                <div style="background-color: #f9fafb; padding: 20px; border-radius: 10px; min-height: 200px;">
                    {areas_mejora_html}
                </div>
            </div>
        </div>
        
        <hr style="border: none; border-top: 2px solid #e5e7eb; margin: 30px 0;">
        
        <!-- Recomendación Final -->
        <h2 style="color: #1f2937;">📋 Recomendación Final</h2>
        {recomendacion}
        
    </div>
    """
    
    return html


def crear_interfaz():
    """
    Crea y configura la interfaz de Gradio.
    
    Returns:
        gr.Blocks: Interfaz de Gradio configurada
    """
    
    # Descripción de ejemplo para el placeholder
    descripcion_ejemplo = """Ejemplo detallado:

**Puesto:** Desarrollador Frontend Senior

**Requisitos obligatorios:**
- 3+ años de experiencia en desarrollo frontend
- Dominio de React.js y JavaScript/TypeScript
- Experiencia con HTML5, CSS3 y frameworks CSS (Bootstrap, Tailwind)
- Conocimiento de herramientas de build (Webpack, Vite)

**Requisitos deseables:**
- Experiencia con Next.js o similares
- Conocimientos de testing (Jest, Cypress)
- Familiaridad con metodologías ágiles
- Inglés intermedio-avanzado

**Responsabilidades:**
- Desarrollo de interfaces de usuario responsivas
- Colaboración con equipos de diseño y backend
- Optimización de rendimiento de aplicaciones web
- Mantenimiento de código legacy"""
    
    with gr.Blocks(
        title="Sistema de Evaluación de CVs",
        theme=gr.themes.Soft(),
        css="""
        .estado-mensaje {
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            font-weight: bold;
        }
        """
    ) as demo:
        
        gr.Markdown("""
        # 📄 Sistema de Evaluación de CVs con IA
        
        **Analiza currículums y evalúa candidatos de manera objetiva usando IA**
        
        Este sistema utiliza inteligencia artificial para:
        - Extraer información clave de currículums en PDF
        - Analizar la experiencia y habilidades del candidato
        - Evaluar el ajuste al puesto específico
        - Proporcionar recomendaciones objetivas de contratación
        """)
        
        # Estado del proceso
        estado_mensaje = gr.Markdown("", visible=False, elem_classes="estado-mensaje")
        
        with gr.Row():
            # Columna de entrada
            with gr.Column(scale=1):
                gr.Markdown("## 📋 Datos de Entrada")
                
                archivo_input = gr.File(
                    label="1. Sube el CV del candidato (PDF)",
                    file_types=[".pdf"],
                    type="filepath"
                )
                
                gr.Markdown("**2. Descripción del puesto de trabajo**")
                descripcion_input = gr.Textbox(
                    label="Detalla los requisitos, responsabilidades y habilidades necesarias:",
                    placeholder=descripcion_ejemplo,
                    lines=15,
                    max_lines=20
                )
                
                with gr.Row():
                    analizar_btn = gr.Button("🔍 Analizar Candidato", variant="primary", scale=2)
                    limpiar_btn = gr.Button("🗑️ Limpiar", scale=1)
            
            # Columna de resultados
            with gr.Column(scale=1):
                gr.Markdown("## 📊 Resultado del Análisis")
                
                instrucciones = gr.Markdown("""
                👆 **Instrucciones:**
                
                1. Sube un CV en formato PDF en la columna izquierda
                2. Describe detalladamente el puesto de trabajo
                3. Haz clic en "Analizar Candidato"
                4. Aquí aparecerá el análisis completo del candidato
                
                **Consejos para mejores resultados:**
                - Usa CVs con texto seleccionable (no imágenes escaneadas)
                - Sé específico en la descripción del puesto
                - Incluye tanto requisitos obligatorios como deseables
                
                **💡 Nota:** Durante el análisis verás mensajes de progreso en tiempo real
                """, visible=True)
                
                resultado_output = gr.HTML(visible=False)
        
        # Configurar eventos con progress tracking explícito
        analizar_btn.click(
            fn=lambda: (gr.update(value="<div style='text-align:center; padding:30px; background-color:#FEF3C7; border-radius:10px;'><h2>🔄 Analizando...</h2><p>Por favor espera, estamos procesando el CV</p></div>", visible=True), gr.update(visible=False)),
            inputs=None,
            outputs=[resultado_output, instrucciones]
        ).then(
            fn=procesar_cv,
            inputs=[archivo_input, descripcion_input],
            outputs=[resultado_output, resultado_output, estado_mensaje]
        )
        
        def limpiar():
            return (
                None,  # archivo_input
                "",  # descripcion_input
                gr.update(visible=False),  # resultado_output
                gr.update(visible=True),  # instrucciones
                gr.update(value="", visible=False)  # estado_mensaje
            )
        
        limpiar_btn.click(
            fn=limpiar,
            outputs=[archivo_input, descripcion_input, resultado_output, instrucciones, estado_mensaje]
        )
    
    return demo


def main(share=False):
    """
    Función principal para ejecutar la aplicación
    
    Args:
        share: Si True, crea una URL pública para compartir
    """
    import socket
    
    demo = crear_interfaz()
    
    # Obtener IP local
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except:
        local_ip = "tu_ip_local"
    
    print("\n" + "="*70)
    print("🚀 SISTEMA DE EVALUACIÓN DE CVs - GRADIO")
    print("="*70)
    print("\n📡 URLs de Acceso:\n")
    print(f"   🏠 Local:    http://localhost:7860")
    print(f"   🌐 Red:      http://{local_ip}:7860")
    
    if share:
        print("\n   ✨ COMPARTIR PÚBLICAMENTE HABILITADO")
        print("   ⏱️  Enlace público válido por 72 horas")
        print("   🔗 El enlace público aparecerá abajo después de iniciar...")
    else:
        print("\n   💡 Para compartir públicamente, usa: --share")
    
    print("\n" + "="*70)
    print("⚠️  Presiona Ctrl+C para detener el servidor")
    print("="*70 + "\n")
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=share,
        show_error=True,
        favicon_path=None,
        inbrowser=False  # No abrir automáticamente
    )


if __name__ == "__main__":
    # Por defecto siempre compartir públicamente
    SHARE_PUBLIC = True
    main(share=SHARE_PUBLIC)
