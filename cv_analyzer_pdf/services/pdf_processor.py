import PyPDF2
from io import BytesIO
from langchain_community.document_loaders import PyPDFLoader
from typing import Callable, Optional
import tempfile
import os

def extraer_texto_pdf(archivo_pdf, progress_callback: Optional[Callable[[str, int], None]] = None):
    """
    Extrae texto de un archivo PDF usando LangChain PyPDFLoader.
    
    Args:
        archivo_pdf: Archivo PDF (puede ser un objeto file o una ruta)
        progress_callback: Función opcional para reportar progreso (mensaje, porcentaje)
    
    Returns:
        str: Texto extraído del PDF o mensaje de error
    """
    try:
        # Validar que el archivo no sea None
        if archivo_pdf is None:
            return "Error: No se proporcionó ningún archivo PDF."
        
        if progress_callback:
            progress_callback("📄 Validando archivo PDF...", 10)
        
        # Si es una ruta de archivo (string), usarla directamente
        if isinstance(archivo_pdf, str):
            pdf_path = archivo_pdf
            temp_file = None
        else:
            # Si es un objeto file, crear archivo temporal
            # Validar el tamaño del archivo
            if hasattr(archivo_pdf, 'size') and archivo_pdf.size == 0:
                return "Error: El archivo PDF está vacío."
            
            if hasattr(archivo_pdf, 'size') and archivo_pdf.size > 200 * 1024 * 1024:
                return "Error: El archivo es demasiado grande (máximo 200 MB)."
            
            # Crear archivo temporal
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            
            if progress_callback:
                progress_callback("💾 Guardando archivo temporal...", 20)
            
            # Resetear y leer contenido
            if hasattr(archivo_pdf, 'seek'):
                archivo_pdf.seek(0)
            
            contenido_pdf = archivo_pdf.read()
            
            if not contenido_pdf:
                if temp_file:
                    os.unlink(temp_file.name)
                return "Error: No se pudo leer el contenido del archivo PDF."
            
            temp_file.write(contenido_pdf)
            temp_file.close()
            pdf_path = temp_file.name
        
        if progress_callback:
            progress_callback("🔍 Analizando estructura del PDF...", 40)
        
        # Usar LangChain PyPDFLoader
        loader = PyPDFLoader(pdf_path)
        
        if progress_callback:
            progress_callback("📖 Extrayendo texto del PDF...", 60)
        
        # Cargar documentos
        documentos = loader.load()
        
        # Limpiar archivo temporal si existe
        if temp_file and os.path.exists(pdf_path):
            try:
                os.unlink(pdf_path)
            except:
                pass
        
        # Validar que se hayan extraído documentos
        if not documentos:
            return "Error: No se pudo extraer contenido del PDF. El archivo podría estar corrupto."
        
        if progress_callback:
            progress_callback(f"✅ Procesando {len(documentos)} página(s)...", 80)
        
        # Construir texto completo con información de páginas
        texto_completo = ""
        paginas_con_contenido = 0
        
        for i, doc in enumerate(documentos, 1):
            texto_pagina = doc.page_content.strip()
            if texto_pagina:
                paginas_con_contenido += 1
                texto_completo += f"\n--- PÁGINA {i} ---\n"
                texto_completo += texto_pagina + "\n"
        
        if progress_callback:
            progress_callback(f"✅ Extracción completada: {paginas_con_contenido} página(s) con contenido", 100)
        
        texto_completo = texto_completo.strip()
        
        if not texto_completo:
            return "Error: El PDF parece estar vacío o contener solo imágenes. Por favor, usa un PDF con texto seleccionable."
        
        # Validar que tenga contenido mínimo
        if len(texto_completo) < 50:
            return "Error: El PDF contiene muy poco texto. Verifica que sea un currículum válido."
        
        return texto_completo
    
    except Exception as e:
        # Limpiar archivo temporal en caso de error
        if 'temp_file' in locals() and temp_file and os.path.exists(pdf_path):
            try:
                os.unlink(pdf_path)
            except:
                pass
        
        error_msg = str(e)
        
        # Mensajes de error más descriptivos
        if "PdfReadError" in error_msg or "PDF" in error_msg:
            return "Error: El archivo PDF está corrupto o no es válido. Por favor, intenta con otro archivo."
        elif "permission" in error_msg.lower():
            return "Error: No se tienen permisos para leer el archivo."
        elif "memory" in error_msg.lower():
            return "Error: El archivo es demasiado grande para procesar."
        else:
            return f"Error inesperado al procesar el PDF: {error_msg}"
    
    except PyPDF2.errors.PdfReadError as e:
        return f"Error: El archivo no es un PDF válido o está corrupto. {str(e)}"
    except Exception as e:
        return f"Error al procesar el archivo PDF: {str(e)}"