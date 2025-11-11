import gradio as gr
from models.cv_model import AnalisisCV
from services.pdf_processor import extraer_texto_pdf
from services.cv_evaluator import evaluar_candidato
import time
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os
import tempfile


def procesar_cv(archivo_pdf, descripcion_puesto, progress=gr.Progress()):
    """
    Procesa el CV y la descripción del puesto, retorna el análisis formateado.
    
    Args:
        archivo_pdf: Archivo PDF subido por el usuario
        descripcion_puesto: Texto con la descripción del puesto
        progress: Objeto Progress de Gradio para mostrar retroalimentación
        
    Returns:
        tuple: (html_resultado, visibilidad_resultados, estado_mensaje, resultado_obj, descripcion_puesto_out, visibilidad_boton_exportar)
    """
    
    # Validaciones iniciales
    progress(0, desc="🔍 Validando datos de entrada...")
    time.sleep(0.3)
    
    if archivo_pdf is None:
        mensaje_error = "⚠️ **Por favor sube un archivo PDF** con el currículum del candidato"
        return mensaje_error, gr.update(visible=False), gr.update(value=mensaje_error, visible=True), None, "", gr.update(visible=False)
    
    if not descripcion_puesto or descripcion_puesto.strip() == "":
        mensaje_error = "⚠️ **Por favor proporciona una descripción detallada** del puesto de trabajo"
        return mensaje_error, gr.update(visible=False), gr.update(value=mensaje_error, visible=True), None, "", gr.update(visible=False)
    
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
            return html_error, gr.update(visible=True), gr.update(value=mensaje_error, visible=True), None, "", gr.update(visible=False)
        
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
        
        return html_resultado, gr.update(visible=True), gr.update(value=mensaje_exito, visible=True), resultado, descripcion_puesto, gr.update(visible=True)
        
    except Exception as e:
        mensaje_error = f"❌ **Error inesperado:**\n\n{str(e)}\n\nPor favor, verifica el archivo PDF y la descripción del puesto e intenta nuevamente."
        progress(1.0, desc="❌ Error durante el procesamiento")
        html_error = f"<div style='padding:20px; background-color:#FEE2E2; border-radius:10px; border-left:5px solid #DC2626;'><h3 style='color:#991B1B; margin-top:0;'>❌ Error Inesperado</h3><p style='color:#991B1B;'>{str(e)}</p><p style='color:#991B1B; font-size:0.9em;'>Por favor, verifica el archivo PDF y la descripción del puesto e intenta nuevamente.</p></div>"
        return html_error, gr.update(visible=True), gr.update(value=mensaje_error, visible=True), None, "", gr.update(visible=False)



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


def generar_pdf_analisis(resultado: AnalisisCV, descripcion_puesto: str = ""):
    """
    Genera un PDF profesional con el análisis completo del CV.
    
    Args:
        resultado: Objeto AnalisisCV con los datos del análisis
        descripcion_puesto: Descripción del puesto para incluir en el reporte
        
    Returns:
        str: Ruta al archivo PDF generado
    """
    
    # Crear archivo temporal para el PDF
    temp_dir = tempfile.gettempdir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"analisis_cv_{timestamp}.pdf"
    pdf_path = os.path.join(temp_dir, pdf_filename)
    
    # Crear documento PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, topMargin=0.75*inch, bottomMargin=0.75*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=colors.HexColor('#374151'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=6,
        alignment=TA_JUSTIFY,
        leading=14
    )
    
    # Título principal
    story.append(Paragraph("📄 REPORTE DE EVALUACIÓN DE CV", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Fecha y hora del análisis
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    story.append(Paragraph(f"<b>Fecha del análisis:</b> {fecha_actual}", normal_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Determinar nivel y color según porcentaje
    if resultado.porcentaje_ajuste >= 80:
        nivel = "EXCELENTE"
        nivel_color = colors.HexColor('#10b981')
        recomendacion_texto = "Candidato altamente recomendado. El perfil está bien alineado con los requisitos del puesto. Se recomienda proceder con las siguientes etapas del proceso de selección."
    elif resultado.porcentaje_ajuste >= 60:
        nivel = "BUENO"
        nivel_color = colors.HexColor('#fbbf24')
        recomendacion_texto = "Candidato con potencial. Muestra potencial pero requiere evaluación adicional. Se recomienda una entrevista técnica para validar competencias específicas."
    elif resultado.porcentaje_ajuste >= 40:
        nivel = "REGULAR"
        nivel_color = colors.HexColor('#f97316')
        recomendacion_texto = "Candidato requiere evaluación adicional. El perfil muestra algunas coincidencias pero necesita validación en áreas clave."
    else:
        nivel = "BAJO"
        nivel_color = colors.HexColor('#ef4444')
        recomendacion_texto = "Candidato no recomendado. El perfil no se alinea suficientemente con los requisitos del puesto. Se recomienda continuar la búsqueda de candidatos más adecuados."
    
    # Tabla de evaluación principal con ajuste de texto
    story.append(Paragraph("🎯 EVALUACIÓN PRINCIPAL", heading_style))
    
    # Estilo para celdas de tabla
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#1f2937'),
        alignment=TA_CENTER,
        leading=12
    )
    
    eval_data = [
        [
            Paragraph('<b>Porcentaje de Ajuste</b>', table_cell_style),
            Paragraph('<b>Nivel</b>', table_cell_style)
        ],
        [
            Paragraph(f'<b>{resultado.porcentaje_ajuste}%</b>', table_cell_style),
            Paragraph(f'<b>{nivel}</b>', table_cell_style)
        ]
    ]
    eval_table = Table(eval_data, colWidths=[3.4*inch, 3.4*inch])
    eval_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9fafb')),
        ('TEXTCOLOR', (0, 1), (0, 1), nivel_color),
        ('TEXTCOLOR', (0, 1), (1, 1), nivel_color),
        ('FONTSIZE', (0, 1), (-1, 1), 14),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, 1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, 1), 12),
    ]))
    story.append(eval_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Perfil del candidato con mejor formato
    story.append(Paragraph("👤 PERFIL DEL CANDIDATO", heading_style))
    
    # Estilo para contenido de tabla
    table_content_style = ParagraphStyle(
        'TableContent',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#1f2937'),
        alignment=TA_LEFT,
        leading=13
    )
    
    perfil_data = [
        [Paragraph('<b>Nombre:</b>', table_content_style), Paragraph(resultado.nombre_candidato, table_content_style)],
        [Paragraph('<b>Años de Experiencia:</b>', table_content_style), Paragraph(f'{resultado.experiencia_años} años', table_content_style)],
        [Paragraph('<b>Educación:</b>', table_content_style), Paragraph(resultado.education, table_content_style)]
    ]
    perfil_table = Table(perfil_data, colWidths=[2*inch, 4.8*inch])
    perfil_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#dbeafe')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#93c5fd')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(perfil_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Experiencia relevante
    story.append(Paragraph("💼 EXPERIENCIA RELEVANTE", heading_style))
    story.append(Paragraph(resultado.experiencia_relevante, normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Habilidades técnicas
    story.append(Paragraph("🛠️ HABILIDADES TÉCNICAS CLAVE", heading_style))
    if resultado.habilidades_clave:
        habilidades_texto = ", ".join([f"<b>{hab}</b>" for hab in resultado.habilidades_clave])
        story.append(Paragraph(habilidades_texto, normal_style))
    else:
        story.append(Paragraph("No se identificaron habilidades técnicas específicas", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Fortalezas
    story.append(Paragraph("💪 FORTALEZAS PRINCIPALES", heading_style))
    if resultado.fortalezas:
        for i, fortaleza in enumerate(resultado.fortalezas, 1):
            story.append(Paragraph(f"{i}. {fortaleza}", normal_style))
    else:
        story.append(Paragraph("No se identificaron fortalezas específicas", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Áreas de mejora
    story.append(Paragraph("📈 ÁREAS DE DESARROLLO", heading_style))
    if resultado.areas_mejora:
        for i, area in enumerate(resultado.areas_mejora, 1):
            story.append(Paragraph(f"{i}. {area}", normal_style))
    else:
        story.append(Paragraph("No se identificaron áreas de mejora específicas", normal_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Recomendación final con mejor formato
    story.append(Paragraph("📋 RECOMENDACIÓN FINAL", heading_style))
    
    # Estilo para recomendación
    recom_style = ParagraphStyle(
        'Recomendacion',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#1f2937'),
        alignment=TA_JUSTIFY,
        leading=15,
        spaceBefore=10,
        spaceAfter=10
    )
    
    recom_paragraph = Paragraph(recomendacion_texto, recom_style)
    recom_data = [[recom_paragraph]]
    recom_table = Table(recom_data, colWidths=[6.8*inch])
    
    if resultado.porcentaje_ajuste >= 80:
        bg_color = colors.HexColor('#d1fae5')
        border_color = colors.HexColor('#10b981')
    elif resultado.porcentaje_ajuste >= 60:
        bg_color = colors.HexColor('#fef3c7')
        border_color = colors.HexColor('#fbbf24')
    elif resultado.porcentaje_ajuste >= 40:
        bg_color = colors.HexColor('#fed7aa')
        border_color = colors.HexColor('#f97316')
    else:
        bg_color = colors.HexColor('#fee2e2')
        border_color = colors.HexColor('#ef4444')
    
    recom_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg_color),
        ('GRID', (0, 0), (-1, -1), 2, border_color),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
    ]))
    story.append(recom_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Descripción del puesto (si se proporcionó)
    if descripcion_puesto and descripcion_puesto.strip():
        story.append(PageBreak())
        story.append(Paragraph("📋 DESCRIPCIÓN DEL PUESTO", heading_style))
        
        # Estilo para descripción del puesto
        desc_style = ParagraphStyle(
            'DescripcionPuesto',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#1f2937'),
            alignment=TA_LEFT,
            leading=14,
            spaceBefore=6,
            spaceAfter=6
        )
        
        # Procesar cada línea de la descripción
        for linea in descripcion_puesto.split('\n'):
            if linea.strip():
                # Convertir ** a <b> para negritas
                linea_formateada = linea.replace('**', '<b>', 1).replace('**', '</b>', 1)
                story.append(Paragraph(linea_formateada, desc_style))
    
    # Footer
    story.append(Spacer(1, 0.5*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#6b7280'),
        alignment=TA_CENTER
    )
    story.append(Paragraph(f"Generado por Sistema de Evaluación de CVs con IA - {fecha_actual}", footer_style))
    
    # Construir PDF
    doc.build(story)
    
    return pdf_path


def exportar_pdf(resultado_obj, descripcion_puesto):
    """
    Exporta el análisis a PDF.
    
    Args:
        resultado_obj: Objeto AnalisisCV con los datos del análisis
        descripcion_puesto: Descripción del puesto
        
    Returns:
        str: Ruta al archivo PDF generado
    """
    if resultado_obj is None:
        return None
    
    try:
        pdf_path = generar_pdf_analisis(resultado_obj, descripcion_puesto)
        return pdf_path
    except Exception as e:
        print(f"Error al generar PDF: {str(e)}")
        return None


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
        
        # Variables de estado para almacenar el resultado y descripción (hidden)
        resultado_state = gr.State(value=None)
        descripcion_state = gr.State(value="")
        
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
                
                # Botón de exportar PDF (inicialmente oculto)
                with gr.Row():
                    exportar_btn = gr.Button("📥 Exportar Análisis a PDF", variant="secondary", visible=False, scale=1)
                
                # Archivo de descarga
                archivo_pdf_output = gr.File(label="📄 Descargar Reporte PDF", visible=False)
        
        # Configurar eventos con progress tracking explícito
        analizar_btn.click(
            fn=lambda: (gr.update(value="<div style='text-align:center; padding:30px; background-color:#FEF3C7; border-radius:10px;'><h2>🔄 Analizando...</h2><p>Por favor espera, estamos procesando el CV</p></div>", visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)),
            inputs=None,
            outputs=[resultado_output, instrucciones, exportar_btn, archivo_pdf_output]
        ).then(
            fn=procesar_cv,
            inputs=[archivo_input, descripcion_input],
            outputs=[resultado_output, resultado_output, estado_mensaje, resultado_state, descripcion_state, exportar_btn]
        )
        
        # Evento para exportar a PDF
        exportar_btn.click(
            fn=exportar_pdf,
            inputs=[resultado_state, descripcion_state],
            outputs=archivo_pdf_output
        ).then(
            fn=lambda: gr.update(visible=True),
            inputs=None,
            outputs=archivo_pdf_output
        )
        
        def limpiar():
            return (
                None,  # archivo_input
                "",  # descripcion_input
                gr.update(visible=False),  # resultado_output
                gr.update(visible=True),  # instrucciones
                gr.update(value="", visible=False),  # estado_mensaje
                None,  # resultado_state
                "",  # descripcion_state
                gr.update(visible=False),  # exportar_btn
                gr.update(visible=False)  # archivo_pdf_output
            )
        
        limpiar_btn.click(
            fn=limpiar,
            outputs=[archivo_input, descripcion_input, resultado_output, instrucciones, estado_mensaje, resultado_state, descripcion_state, exportar_btn, archivo_pdf_output]
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
    print(f"   🏠 Local:    http://localhost:7862")
    print(f"   🌐 Red:      http://{local_ip}:7862")
    
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
        server_port=7862,
        share=share,
        show_error=True,
        favicon_path=None,
        inbrowser=False  # No abrir automáticamente
    )


if __name__ == "__main__":
    # Por defecto siempre compartir públicamente
    SHARE_PUBLIC = True
    main(share=SHARE_PUBLIC)
