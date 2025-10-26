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

## Promt Tamplate
Son plantillas que se utilizan para generar prompts personalizados. En langchain se utilizan para definir la estructura y contenido de los mensajes que se enviarán al modelo de lenguaje. Es muy importante el prompt engineering para obtener mejores resultados, por que en los template promts aplicar esto determina por completo el resultado del comportamineto del modelo.

En las plantillas podemos tener roles como system, user, assistant, etc.

### Root prompts 
Los root prompts son los prompts más básicos que se utilizan para iniciar la conversación con el modelo. Estos prompts se utilizan para definir la tarea que se va a realizar y los datos que se van a utilizar.

## Tarea: Mejora tu Chatbot con ChatPromptTemplate, GPT y OpenAI
📋 Objetivo

En esta tarea transformarás tu chatbot del tema anterior para usar ChatPromptTemplate en lugar de PromptTemplate. Descubrirás las ventajas de trabajar con templates diseñados específicamente para modelos de chat y cómo estructurar prompts de forma más clara y eficiente.

⚠️ Importante: Esta tarea se centra en conceptos fundamentales de LangChain para aplicaciones conversacionales. Si encuentras dificultades, no te preocupes, el objetivo es que comprendas las diferencias entre ambos enfoques y sus casos de uso. La solución completa estará disponible al final de este artículo. ¡Experimenta y aprende las mejores prácticas!



🎯 Lo que aprenderás

ChatPromptTemplate: Templates optimizados para modelos de chat

Estructura de mensajes: System, Human, AI messages en templates

Separación clara: Instrucciones del sistema vs conversación

Mejores prácticas: Cuándo usar cada tipo de template

Optimización: Aprovechamiento del formato nativo de chat de los LLMs



🏁 Punto de partida

Tu código actual usa PromptTemplate y debería verse así:

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate
 
# ... configuración de Streamlit ...
 
# Template actual con PromptTemplate
prompt_template = PromptTemplate(
    input_variables=["mensaje", "historial"],
    template="""Eres un asistente útil y amigable llamado ChatBot Pro. 
 
Historial de conversación:
{historial}
 
Responde de manera clara y concisa a la siguiente pregunta: {mensaje}"""
)
 
# Cadena actual
cadena = prompt_template | chat_model


🔄 ¿Por qué cambiar a ChatPromptTemplate?

Problemas con PromptTemplate:

❌ Todo mezclado: Instrucciones del sistema y conversación en un solo bloque de texto
❌ Menos claro: Difícil separar qué es configuración y qué es conversación
❌ Menos natural: No aprovecha la estructura nativa de chat de los modelos
❌ Mantenimiento difícil: Cambios en las instrucciones requieren editar todo el template

Ventajas de ChatPromptTemplate:

✅ Estructura clara: Separación entre system, human y assistant messages
✅ Mejor organización: Cada tipo de mensaje tiene su propósito específico
✅ Más natural: Aprovecha cómo están entrenados los modelos de chat
✅ Fácil mantenimiento: Cambios independientes en cada sección



🛠️ Implementación Paso a Paso

1. Actualizar Importaciones

Primer paso: Añadir las importaciones necesarias.

# Añade esta importación a las existentes
from langchain.prompts import ChatPromptTemplate


2. Crear el ChatPromptTemplate

Objetivo: Reemplazar el PromptTemplate actual con ChatPromptTemplate.

Tu turno: Reemplaza el template actual con este nuevo enfoque:

# Reemplaza el PromptTemplate existente con:
chat_prompt = ChatPromptTemplate.from_messages([
    # Mensaje del sistema - Define la personalidad una sola vez
    ("system", "Eres un asistente útil y amigable llamado ChatBot Pro. Responde de manera clara y concisa."),
    
    # El historial y mensaje actual - se manejan como texto formateado
    ("human", "Historial de conversación:\n{historial}\n\nPregunta actual: {mensaje}")
])


Diferencias clave:

("system", "..."): Define el comportamiento base del asistente (separado y claro)

("human", "..."): Contiene el historial y la pregunta actual

Estructura clara: Cada mensaje tiene un rol específico



3. Actualizar la Cadena

Objetivo: Usar el nuevo template en la cadena.

# Actualiza la cadena (¡sigue siendo simple!)
cadena = chat_prompt | chat_model


4. Personalización del Sistema (Desafío)

Objetivo: Hacer el mensaje del sistema configurable desde el sidebar.

with st.sidebar:
    st.header("Configuración")
    temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)
    model_name = st.selectbox("Modelo", ["gpt-3.5-turbo", "gpt-4", "gpt-4o-mini"])
    
    # ¡Nuevo! Personalidad configurable
    personalidad = st.selectbox(
        "Personalidad del Asistente",
        [
            "Útil y amigable",
            "Profesional y formal", 
            "Casual y relajado",
            "Experto técnico",
            "Creativo y divertido"
        ]
    )
    
    # Recrear modelo
    chat_model = ChatOpenAI(model=model_name, temperature=temperature)
    
    # Template dinámico basado en personalidad
    system_messages = {
        "Útil y amigable": "Eres un asistente útil y amigable llamado ChatBot Pro. Responde de manera clara y concisa.",
        "Profesional y formal": "Eres un asistente profesional y formal. Proporciona respuestas precisas y bien estructuradas.",
        "Casual y relajado": "Eres un asistente casual y relajado. Habla de forma natural y amigable, como un buen amigo.",
        "Experto técnico": "Eres un asistente experto técnico. Proporciona respuestas detalladas con precisión técnica.",
        "Creativo y divertido": "Eres un asistente creativo y divertido. Usa analogías, ejemplos creativos y mantén un tono alegre."
    }
    
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_messages[personalidad]),
        ("human", "Historial de conversación:\n{historial}\n\nPregunta actual: {mensaje}")
    ])
    
    cadena = chat_prompt | chat_model


💡 Conceptos Clave a Recordar

Estructura de ChatPromptTemplate

ChatPromptTemplate.from_messages([
    ("system", "Instrucciones base del asistente"),    # Configuración
    ("human", "Contenido del usuario + historial"),   # Datos de entrada
    ("assistant", "Respuesta anterior (opcional)")    # Para few-shot examples
])


Roles de mensajes:

system: Instrucciones y configuración del comportamiento

human: Mensajes del usuario (incluyendo contexto/historial)

assistant: Respuestas del modelo (para ejemplos o continuación)

Ventajas del nuevo enfoque:

Claridad: Separación visual entre configuración y datos

Mantenimiento: Cambios independientes en cada sección

Flexibilidad: Fácil intercambiar instrucciones del sistema

Mejores prácticas: Sigue las convenciones de modelos de chat



📝 Solución Completa

Aquí tienes el código completo con la transformación de PromptTemplate a ChatPromptTemplate, incluyendo el desafío del punto 4 (personalización del sistema):

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
 
# Configuración inicial
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")
st.title("🤖 Chatbot Básico con LangChain")
st.markdown("Este es un *chatbot de ejemplo* construido con LangChain + Streamlit. ¡Escribe tu mensaje abajo para comenzar!")
 
with st.sidebar:
    st.header("Configuración")
    temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)
    model_name = st.selectbox("Modelo", ["gpt-3.5-turbo", "gpt-4", "gpt-4o-mini"])
    
    # PUNTO 4: Personalidad configurable
    personalidad = st.selectbox(
        "Personalidad del Asistente",
        [
            "Útil y amigable",
            "Profesional y formal", 
            "Casual y relajado",
            "Experto técnico",
            "Creativo y divertido"
        ]
    )
    
    # Recrear el modelo con nuevos parámetros
    chat_model = ChatOpenAI(model=model_name, temperature=temperature)
    
    # Definir mensajes del sistema según personalidad
    system_messages = {
        "Útil y amigable": "Eres un asistente útil y amigable llamado ChatBot Pro. Responde de manera clara y concisa.",
        "Profesional y formal": "Eres un asistente profesional y formal. Proporciona respuestas precisas y bien estructuradas.",
        "Casual y relajado": "Eres un asistente casual y relajado. Habla de forma natural y amigable, como un buen amigo.",
        "Experto técnico": "Eres un asistente experto técnico. Proporciona respuestas detalladas con precisión técnica.",
        "Creativo y divertido": "Eres un asistente creativo y divertido. Usa analogías, ejemplos creativos y mantén un tono alegre."
    }
    
    # NUEVO: ChatPromptTemplate con personalidad dinámica
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_messages[personalidad]),
        ("human", "Historial de conversación:\n{historial}\n\nPregunta actual: {mensaje}")
    ])
    
    # Crear cadena usando LCEL
    cadena = chat_prompt | chat_model
 
# Inicializar el historial de mensajes en session_state
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
 
# Renderizar historial existente
for msg in st.session_state.mensajes:
    if isinstance(msg, SystemMessage):
        continue  # no mostrar mensajes del sistema al usuario
    
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)
 
if st.button("🗑️ Nueva conversación"):
    st.session_state.mensajes = []
    st.rerun()
 
# Input de usuario
pregunta = st.chat_input("Escribe tu mensaje:")
 
if pregunta:
    # Mostrar y almacenar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(pregunta)
    
    # Preparar historial como texto
    historial_texto = ""
    for msg in st.session_state.mensajes[-10:]:  # Últimos 10 mensajes
        if isinstance(msg, HumanMessage):
            historial_texto += f"Usuario: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            historial_texto += f"Asistente: {msg.content}\n"
    
    if not historial_texto:
        historial_texto = "(No hay historial previo)"
    
    # Generar y mostrar respuesta del asistente
    try:
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
 
            # Streaming de la respuesta con ChatPromptTemplate
            for chunk in cadena.stream({"mensaje": pregunta, "historial": historial_texto}):
                full_response += chunk.content
                response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
        
        # Almacenar mensajes en el historial
        st.session_state.mensajes.append(HumanMessage(content=pregunta))
        st.session_state.mensajes.append(AIMessage(content=full_response))
        
    except Exception as e:
        st.error(f"Error al generar respuesta: {str(e)}")
        st.info("Verifica que tu API Key de OpenAI esté configurada correctamente.")


🔑 Puntos Clave de la Solución

1. La diferencia principal - PromptTemplate vs ChatPromptTemplate:

# ❌ ANTES: PromptTemplate (todo mezclado)
prompt_template = PromptTemplate(
    input_variables=["mensaje", "historial"],
    template="""Eres un asistente útil y amigable llamado ChatBot Pro. 
 
Historial de conversación:
{historial}
 
Responde de manera clara y concisa a la siguiente pregunta: {mensaje}"""
)
 
# ✅ AHORA: ChatPromptTemplate (estructura clara)
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente útil y amigable llamado ChatBot Pro. Responde de manera clara y concisa."),
    ("human", "Historial de conversación:\n{historial}\n\nPregunta actual: {mensaje}")
])


2. Ventajas implementadas:

✅ Mejor estructura: System message separado del human message

✅ Más claro: Instrucciones del asistente vs datos del usuario bien diferenciados

✅ Mejor práctica: Sigue las convenciones de modelos de chat

✅ Fácil mantenimiento: Cambios independientes en system vs human messages



3. El uso sigue siendo idéntico:

# La cadena funciona exactamente igual
cadena = chat_prompt | chat_model
cadena.stream({"mensaje": pregunta, "historial": historial_texto})


4. Preparación del historial:

# El historial se sigue formateando como texto
historial_texto = ""
for msg in st.session_state.mensajes[-10:]:
    if isinstance(msg, HumanMessage):
        historial_texto += f"Usuario: {msg.content}\n"
    elif isinstance(msg, AIMessage):
        historial_texto += f"Asistente: {msg.content}\n"


¡La mejora es sutil pero importante: mejor organización y estructura más profesional! 🎉


### Lectura: MessagesPlaceholder y Few-Shot Examples
¿Qué es el In-Context Learning (ICL)?

El In-Context Learning o Aprendizaje en Contexto es la capacidad de los modelos de lenguaje de aprender nuevas tareas o patrones simplemente proporcionándoles ejemplos dentro del mismo prompt, sin necesidad de entrenar o ajustar el modelo.

Es como mostrarle a alguien cómo hacer algo dándole ejemplos directos:

"Mira, así se hace esto... y esto otro... ¿ahora puedes hacer tú algo similar?"



¿Qué son los Few-Shot Examples?

Los Few-Shot Examples (ejemplos de pocos intentos) son una técnica de ICL donde proporcionamos al modelo entre 2-10 ejemplos de la tarea que queremos que realice. Estos ejemplos sirven como "entrenamiento instantáneo".

Estructura típica:

Sistema: Instrucciones generales
Ejemplo 1: Input → Output esperado
Ejemplo 2: Input → Output esperado  
Ejemplo 3: Input → Output esperado
Pregunta real: Input actual → ?


MessagesPlaceholder: La Herramienta Perfecta

MessagesPlaceholder es ideal para few-shot examples porque:

✅ Mantiene la estructura de mensajes (Human/AI)

✅ Permite insertar múltiples ejemplos dinámicamente

✅ El modelo entiende mejor el formato de conversación

✅ Fácil de reutilizar para diferentes tareas



Evolución del Código: De Historial a Few-Shot

Código Base (Historial de Conversación)

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
 
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente útil que mantiene el contexto de la conversación."),
    MessagesPlaceholder(variable_name="historial"),
    ("human", "Usuario: {pregunta_actual}")
])
 
# Simulamos un historial de conversación
historial_conversacion = [
    HumanMessage(content="Usuario: ¿Cuál es la capital de Francia?"),
    AIMessage(content="IA: La capital de Francia es París."),
    HumanMessage(content="Usuario: ¿Y cuántos habitantes tiene?"),
    AIMessage(content="IA: París tiene aproximadamente 2.2 millones de habitantes en la ciudad propiamente dicha.")
]


Código Evolucionado (Few-Shot Examples)

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
 
# Template para clasificación de sentimientos con few-shot examples
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un experto en análisis de sentimientos. Clasifica cada texto como: POSITIVO, NEGATIVO o NEUTRO."),
    MessagesPlaceholder(variable_name="ejemplos"),
    ("human", "Texto a analizar: {texto_usuario}")
])
 
# Few-shot examples para análisis de sentimientos
ejemplos_sentimientos = [
    HumanMessage(content="Texto a analizar: Me encanta este producto, es increíble"),
    AIMessage(content="POSITIVO"),
    HumanMessage(content="Texto a analizar: El servicio fue terrible, muy decepcionante"),
    AIMessage(content="NEGATIVO"),
    HumanMessage(content="Texto a analizar: El clima está nublado hoy"),
    AIMessage(content="NEUTRO")
]
 
# Generar el prompt con los ejemplos
mensajes = chat_prompt.format_messages(
    ejemplos=ejemplos_sentimientos,
    texto_usuario="¡Qué día tan maravilloso!"
)
 
# Ver el resultado
for i, m in enumerate(mensajes):
    print(f"Mensaje {i+1} ({m.__class__.__name__}):")
    print(m.content)
    print("-" * 40)


Salida del Código:

Mensaje 1 (SystemMessage):
Eres un experto en análisis de sentimientos. Clasifica cada texto como: POSITIVO, NEGATIVO o NEUTRO.
----------------------------------------
Mensaje 2 (HumanMessage):
Texto a analizar: Me encanta este producto, es increíble
----------------------------------------
Mensaje 3 (AIMessage):
POSITIVO
----------------------------------------
Mensaje 4 (HumanMessage):
Texto a analizar: El servicio fue terrible, muy decepcionante
----------------------------------------
Mensaje 5 (AIMessage):
NEGATIVO
----------------------------------------
Mensaje 6 (HumanMessage):
Texto a analizar: El clima está nublado hoy
----------------------------------------
Mensaje 7 (AIMessage):
NEUTRO
----------------------------------------
Mensaje 8 (HumanMessage):
Texto a analizar: ¡Qué día tan maravilloso!
----------------------------------------


Ventajas de Este Enfoque

Con MessagesPlaceholder:

✅ Estructura clara: Cada ejemplo mantiene su rol (Human/AI)
✅ Escalable: Fácil añadir/quitar ejemplos
✅ Reutilizable: Cambiar ejemplos = Nueva tarea
✅ Natural: El modelo entiende el formato conversacional

Sin MessagesPlaceholder (texto plano):

❌ Menos claro: Todo mezclado en un string
❌ Más errores: El modelo puede confundirse
❌ Difícil mantenimiento: Cambios requieren reescribir todo
❌ Menos efectivo: Pierde la estructura conversacional



Otros Ejemplos de Uso

1. Extracción de Información

ejemplos_extraccion = [
    HumanMessage(content="Texto: Juan Pérez trabaja en Google como ingeniero desde 2020"),
    AIMessage(content="Nombre: Juan Pérez, Empresa: Google, Puesto: ingeniero, Año: 2020"),
    HumanMessage(content="Texto: María Silva es doctora en el Hospital Central"),
    AIMessage(content="Nombre: María Silva, Empresa: Hospital Central, Puesto: doctora, Año: N/A")
]


2. Traducción con Estilo

ejemplos_traduccion = [
    HumanMessage(content="Formal en inglés: Good morning, how are you today?"),
    AIMessage(content="Casual en español: ¡Hola! ¿Qué tal?"),
    HumanMessage(content="Formal en inglés: I would like to schedule a meeting"),
    AIMessage(content="Casual en español: ¿Podemos quedar?")
]


Mejores Prácticas

2-5 ejemplos: Suficiente para mostrar el patrón, no demasiados

Ejemplos diversos: Cubrir diferentes casos/variaciones

Formato consistente: Mismo patrón en todos los ejemplos

Ejemplos de calidad: Outputs perfectos como referencia



Conclusión

MessagesPlaceholder transforma los few-shot examples de una técnica básica a una herramienta poderosa y flexible. La estructura clara de mensajes Human/AI hace que el modelo comprenda mejor qué esperamos, resultando en respuestas más precisas y consistentes.

Recuerda: No es solo insertar ejemplos, es enseñarle al modelo a través de la conversación. ¡Esa es la magia del In-Context Learning!

## Pydantic
Es una biblioteca de Python para la validación de datos y la serialización de objetos. Permite definir esquemas de datos y validar los datos de entrada de manera sencilla.

