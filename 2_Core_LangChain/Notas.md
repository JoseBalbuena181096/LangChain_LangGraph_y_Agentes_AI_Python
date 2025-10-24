## Componentes clave

Los principales componentes clave de lanchaing, son 
- Chain: Secuencia de llamadas a componentes, como modelos de lenguaje, herramientas externas y otras cadenas.
- Runnable: Objeto que puede ser invocado para ejecutar una secuencia de llamadas a componentes. Recibe una serie de entradas y produce una serie de salidas.

Langchaing nos permite unir diferentes runnables en una secuencia, para formar una cadena de llamadas.


## Tarea: Mini-Proyecto: Análisis de sentimientos con LangChain
📋 Objetivo

En esta tarea construirás desde cero un sistema completo de análisis de sentimientos usando LangChain. Aprenderás a crear funciones personalizadas, convertirlas en objetos Runnable usando RunnableLambda, y combinarlas en cadenas de procesamiento complejas.

⚠️ Importante: Esta tarea introduce conceptos avanzados de LangChain y es completamente normal que encuentres dificultades. No te preocupes si no puedes completar todos los puntos, el objetivo principal es que practiques el uso de RunnableLambda y entiendas cómo encadenar operaciones. La solución completa estará disponible en la siguiente clase para consulta. ¡Experimenta, aprende del proceso y diviértete construyendo!



🎯 Lo que aprenderás

RunnableLambda: Convertir funciones Python en objetos Runnable

Cadenas complejas: Combinar múltiples operaciones de procesamiento

Manejo de JSON: Estructurar respuestas del modelo

Preprocesamiento: Limpiar y preparar texto para análisis

Arquitectura modular: Dividir problemas complejos en pasos simples



🏗️ Arquitectura del Sistema

Tu sistema final tendrá esta estructura:

Texto de entrada → Preprocesamiento → Análisis Completo → Resultado
                                           ↙        ↘
                                    Resumen    Sentimiento


🛠️ Implementación Paso a Paso

1. Configuración Inicial

Empezemos con las importaciones y configuración básica:

from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
import json
 
# Configuración del modelo
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


Pregunta reflexiva: ¿Por qué usamos temperature=0 para análisis de sentimientos?



2. Preprocesador de Texto

Objetivo: Crear una función que limpie y prepare el texto.

Tu turno: Implementa la función de preprocesamiento:

def preprocess_text(text):
    """Limpia el texto eliminando espacios extras y limitando longitud"""
    # Pista: usa .strip() para eliminar espacios
    # Pista: limita a 500 caracteres con slicing [:500]
    return # ¡Completa aquí!
 
# Convertir la función en un Runnable
preprocessor = RunnableLambda(preprocess_text)


3. Generador de Resúmenes

Objetivo: Crear una función que genere un resumen conciso del texto.

def generate_summary(text):
    """Genera un resumen conciso del texto"""
    prompt = f"Resume en una sola oración: {text}"
    response = llm.invoke(prompt)
    return response.content


Reto: ¿Podrías mejorar este prompt para obtener mejores resúmenes?



4. Analizador de Sentimientos

Objetivo: Crear una función que analice el sentimiento y devuelva JSON estructurado.

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


Pregunta: ¿Por qué es importante el manejo de errores con try/except aquí?



5. Función de Combinación

Objetivo: Unificar los resultados de resumen y análisis de sentimientos.

def merge_results(data):
    """Combina los resultados de ambas ramas en un formato unificado"""
    return {
        "resumen": data["resumen"],
        "sentimiento": data["sentimiento_data"]["sentimiento"],
        "razon": data["sentimiento_data"]["razon"]
    }


6. Función de Procesamiento Principal

Objetivo: Coodinar el análisis completo (resumen + sentimientos).

def process_one(t):
    resumen = generate_summary(t)              # Llamada 1 al LLM
    sentimiento_data = analyze_sentiment(t)    # Llamada 2 al LLM
    return merge_results({
        "resumen": resumen,
        "sentimiento_data": sentimiento_data
    })
 
# Convertir en Runnable
process = RunnableLambda(process_one)


7. Construcción de la Cadena Final

Objetivo: Conectar todos los componentes usando LCEL.

# La cadena completa
chain = preprocessor | process


¡Eso es todo! Tu sistema está listo para usar.



8. Probando tu Sistema

# Prueba con diferentes textos
textos_prueba = [
    "¡Me encanta este producto! Funciona perfectamente y llegó muy rápido.",
    "El servicio al cliente fue terrible, nadie me ayudó con mi problema.",
    "El clima está nublado hoy, probablemente llueva más tarde."
]
 
for texto in textos_prueba:
    resultado = chain.invoke(texto)
    print(f"Texto: {texto}")
    print(f"Resultado: {resultado}")
    print("-" * 50)


💭 Reflexiones Finales

¿Qué ventajas tiene dividir el procesamiento en funciones separadas?

¿Cómo mejorarías la precisión del análisis de sentimientos?

¿Qué otros de análisis podrías añadir a este sistema?

¿Cómo manejarías textos en diferentes idiomas?



¡Recuerda: el objetivo es aprender y experimentar. No te presiones para completar todo perfectamente! 🚀

