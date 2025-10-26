import PyPDF2
from io import BytesIO

def extraer_texto_pdf(archivo_pdf):
    try:
        # Validar que el archivo no sea None
        if archivo_pdf is None:
            return "Error: No se proporcionó ningún archivo PDF."
        
        # Validar el tamaño del archivo
        if hasattr(archivo_pdf, 'size') and archivo_pdf.size == 0:
            return "Error: El archivo PDF está vacío."
        
        # Resetear el puntero del archivo al inicio
        archivo_pdf.seek(0)
        
        # Leer el contenido del archivo
        contenido_pdf = archivo_pdf.read()
        
        # Validar que el contenido no esté vacío
        if not contenido_pdf:
            return "Error: No se pudo leer el contenido del archivo PDF."
        
        # Resetear nuevamente para futuras operaciones
        archivo_pdf.seek(0)
        
        pdf_reader = PyPDF2.PdfReader(BytesIO(contenido_pdf))
        
        # Validar que el PDF tenga páginas
        if len(pdf_reader.pages) == 0:
            return "Error: El PDF no contiene páginas."
        
        texto_completo = ""

        for numero_pagina, pagina in enumerate(pdf_reader.pages, 1):
            try:
                texto_pagina = pagina.extract_text()
                if texto_pagina.strip():
                    texto_completo += f"\n--- PÁGINA {numero_pagina} ---\n"
                    texto_completo += texto_pagina + "\n"
            except Exception as e_pagina:
                # Continuar con la siguiente página si hay error en una página específica
                continue
        
        texto_completo = texto_completo.strip()

        if not texto_completo:
            return "Error: El PDF parece estar vacío o contener solo imágenes."
        
        return texto_completo
    
    except PyPDF2.errors.PdfReadError as e:
        return f"Error: El archivo no es un PDF válido o está corrupto. {str(e)}"
    except Exception as e:
        return f"Error al procesar el archivo PDF: {str(e)}"