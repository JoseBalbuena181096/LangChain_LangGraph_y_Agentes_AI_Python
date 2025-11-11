"""
Script de prueba para verificar la funcionalidad de exportación a PDF
"""
from models.cv_model import AnalisisCV
from ui.gradio_ui import generar_pdf_analisis

# Crear un análisis de prueba
resultado_prueba = AnalisisCV(
    nombre_candidato="Juan Pérez García",
    experiencia_años=5,
    habilidades_clave=["Python", "Machine Learning", "TensorFlow", "PyTorch", "SQL"],
    education="Ingeniería en Sistemas Computacionales - Universidad Nacional",
    experiencia_relevante="Desarrollador senior con 5 años de experiencia en proyectos de machine learning y análisis de datos. Ha trabajado en implementación de modelos predictivos y sistemas de recomendación.",
    fortalezas=[
        "Amplia experiencia en frameworks de ML modernos",
        "Sólidos conocimientos en Python y sus bibliotecas científicas",
        "Historial comprobado en proyectos de gran escala",
        "Excelentes habilidades de trabajo en equipo"
    ],
    areas_mejora=[
        "Experiencia limitada con cloud computing (AWS/Azure)",
        "Podría fortalecer conocimientos en MLOps",
        "Certificaciones profesionales por obtener"
    ],
    porcentaje_ajuste=85
)

descripcion_prueba = """
**Puesto:** Machine Learning Engineer Senior

**Requisitos obligatorios:**
- 3+ años de experiencia en ML/AI
- Dominio de Python y frameworks de ML
- Experiencia con TensorFlow o PyTorch
- Conocimientos de SQL y bases de datos

**Requisitos deseables:**
- Experiencia con servicios cloud
- Conocimientos de MLOps
- Inglés avanzado
"""

try:
    print("🔄 Generando PDF de prueba...")
    pdf_path = generar_pdf_analisis(resultado_prueba, descripcion_prueba)
    print(f"✅ PDF generado exitosamente en: {pdf_path}")
    print(f"\n📄 Puedes abrir el archivo con: xdg-open {pdf_path}")
except Exception as e:
    print(f"❌ Error al generar PDF: {str(e)}")
    import traceback
    traceback.print_exc()
