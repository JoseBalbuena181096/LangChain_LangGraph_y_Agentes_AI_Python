from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_openai import ChatOpenAI
import json
from dotenv import load_dotenv
load_dotenv()
import os

print(os.getenv("OPENAI_API_KEY"))
# Configuración del modelo
llm = ChatOpenAI(model="gpt-5-nano", temperature=0)

# Preprocesador: limpia espacios y limita a 500 caracteres
def preprocess_text(text):
    """Limpia el texto eliminando espacios extras y limitando longitud"""
    return text.strip()[:500]

preprocessor = RunnableLambda(preprocess_text)

# Generación de resumen
def generate_summary(text):
    """Genera un resumen conciso del texto"""
    prompt = f"Resume en una sola oración: {text}"
    response = llm.invoke(prompt)
    return response.content

summary_brach = RunnableLambda(generate_summary)

# Análisis de sentimiento con formato JSON
def analyze_sentiment(text):
    """Analiza el sentimiento y devuelve resultado estructurado"""
    prompt = f"""Analiza el sentimiento del siguiente texto.
    Responde ÚNICAMENTE en formato JSON válido:
    {{"sentimiento": "positivo|negativo|neutro", "razon": "justificación breve"}}
    
    Texto: {text}"""
    
    response = llm.invoke(prompt)
    try:
        return json.loads(response.content)
    except json.JSONDecodeError:
        return {"sentimiento": "neutro", "razon": "Error en análisis"}
    
sentiment_branch = RunnableLambda(analyze_sentiment)

# Combinación de resultados
def merge_results(data):
    """Combina los resultados de ambas ramas en un formato unificado"""
    return {
        "resumen": data["resumen"],
        "sentimiento": data["sentimiento_data"]["sentimiento"],
        "razon": data["sentimiento_data"]["razon"]
    }

merger = RunnableLambda(merge_results)

parallel_analysis = RunnableParallel({
    "resumen": summary_brach,
    "sentimiento_data": sentiment_branch
})

# Cadena completa
chain = preprocessor | parallel_analysis | merger

review_batch = [
    "Este producto es muy malo. No me ha gustado nada en el absoluto.",
    "El servicio al cliente fue terrible, nadie me ayudó con mi problema.",
    "El clima está nublado hoy, probablemente llueva más tarde.",
    "Esta bien, cumple su funcion pero no es lo mejor que hay."

]

## Procesar todos los elementos de forma paralela
resultado_batch = chain.batch(review_batch)
print(resultado_batch)
