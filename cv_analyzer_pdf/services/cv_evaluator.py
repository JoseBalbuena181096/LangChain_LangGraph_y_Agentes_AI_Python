from langchain_openai import ChatOpenAI
from models.cv_model import AnalisisCV
from prompts.cv_prompts import crear_sistema_prompts
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def crear_evaluador_cv():
    # Verificar que la API key esté configurada
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY no está configurada. "
            "Por favor, crea un archivo .env basado en .env.example "
            "y configura tu clave de OpenAI."
        )
    
    # Usar el modelo configurado o el por defecto
    model_name = os.getenv("OPENAI_MODEL", "gpt-5-nano")
    
    modelo_base = ChatOpenAI(
        model=model_name,
        temperature=0.2,
        api_key=api_key
    )

    modelo_estructurado = modelo_base.with_structured_output(AnalisisCV)
    chat_prompt = crear_sistema_prompts()
    cadena_evaluacion = chat_prompt | modelo_estructurado

    return cadena_evaluacion

def evaluar_candidato(texto_cv: str, descripcion_puesto: str) -> AnalisisCV:
    try:
        cadena_evaluacion = crear_evaluador_cv()

        resultado = cadena_evaluacion.invoke({
            "texto_cv": texto_cv,
            "descripcion_puesto": descripcion_puesto
        })
        
        return resultado
    
    except ValueError as ve:
        # Error de configuración (API key faltante)
        return AnalisisCV(
            nombre_candidato="Error de configuración",
            experiencia_años=0,
            habilidades_clave=["Configuración requerida"],
            education="No disponible",
            experiencia_relevante=str(ve),
            fortalezas=["Revisar configuración de API"],
            areas_mejora=["Configurar OPENAI_API_KEY en archivo .env"],
            porcentaje_ajuste=0
        )
    
    except Exception as e:
        # Otros errores
        return AnalisisCV(
            nombre_candidato="Error en procesamiento",
            experiencia_años=0,
            habilidades_clave=["Error al procesar CV"],
            education="No se puede determinar",
            experiencia_relevante=f"Error durante el análisis: {str(e)}",
            fortalezas=["Requiere revisión manual del CV"],
            areas_mejora=["Verificar formato y legibilidad del PDF"],
            porcentaje_ajuste=0
        )
