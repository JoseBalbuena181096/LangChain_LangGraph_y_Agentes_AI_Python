Para ejecutarlo debemos

Activar el ambiente adecuado:
```bash
conda activate llms
```

Ingresar a la ruta adecuada

```bash
cd '/home/jose/Ingenieria_de_LLM/LangChain_LangGraph_y_Agentes_AI_Python' 
```
Exportar las variables de ambiente:

```bash
export $(cat .env | xargs)
```

Ejecutar el script:
```bash
python 1_Intro_LangChain/hello_word.py
``` 

Podemos tambien usar python-dotenv (más profesional):
```bash
pip install python-dotenv
```

Y luego modificar el script:
```python
from dotenv import load_dotenv

load_dotenv()

import os

print(os.getenv("OPENAI_API_KEY"))
```

Como el de google ya lo hemos configurado para que carge las variables de ambiente, no es necesario exportarlas manualmente. Se ejecuta asi de rapido:
```bash
python /home/jose/Ingenieria_de_LLM/LangChain_LangGraph_y_Agentes_AI_Python/1_Intro_LangChain/hello_word_Gemini.py

```

Las plantillas en langchain son una forma de crear prompts personalizados.
- Posemos usar variables en las plantillas para personalizar el prompt.
- Posemos usar condicionales en las plantillas para controlar el flujo del prompt.
- Posemos usar bucles en las plantillas para repetir partes del prompt.
- Las variables en las plantillas pueden ser usadas para pasar información dinámica al prompt.


Las cadenas son una secuencia de pasos que nos permiten crear prompts personalizados, por medio de cadenas secuenciales.

LCE: LangChain Expression Language
Son una forma de definir cadenas secuenciales de manera más concisa y legible.


## Lectura: Arquitectura de Paquetes en LangChain
En esta lección nos detendremos a comprender la arquitectura general de LangChain y su ecosistema al día de hoy.

Esto nos dará un mapa mental de cómo encajan las piezas: modelos, cadenas, agentes, memoria, herramientas, y también cómo LangGraph expande las capacidades de LangChain. Aunque no escribamos mucho código nuevo aquí, este conocimiento conceptual será muy útil cuando abordemos proyectos más complejos en secciones posteriores.

Arquitectura de Paquetes LangChain

Antes de entrar en los componentes específicos, es importante entender cómo se organiza LangChain. El ecosistema se ha modularizado significativamente para mejorar la mantenibilidad, reducir dependencias y permitir instalaciones más ligeras:

Estructura modular:

┌─────────────────────────────────────────────────────────┐
│                    Aplicación de Usuario                │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────┴───────────────────────────────┐
│                      langchain                          │
│  (Chains, Agents, Memory, Callbacks de alto nivel)      │
└─────────────────────────┬───────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
┌───────┴──────┐ ┌────────┴──────┐ ┌───────┴────────┐
│              │ │               │ │                │
│langchain-core│ │  langchain-   │ │Partner Packages│
│              │ │  community    │ │                │
│ Abstracciones│ │ Integraciones │ │ - openai       │
│ Interfaces   │ │ de terceros   │ │ - anthropic    │
│ LCEL         │ │               │ │ - ollama       │
│              │ │               │ │ - groq         │
└──────────────┘ └───────────────┘ └────────────────┘


Los cuatro niveles principales:

• langchain-core: Contiene las abstracciones fundamentales e interfaces base. Aquí están las clases abstractas como BaseLanguageModel, BasePromptTemplate, Runnable, y el corazón del LCEL (LangChain Expression Language). Es la base sobre la que se construye todo lo demás.

• langchain-community: Integraciones con servicios y herramientas de terceros que no tienen soporte oficial optimizado. Incluye conectores para bases de datos vectoriales de código abierto, loaders de documentos, herramientas diversas, etc.

• Partner Packages: Paquetes separados mantenidos oficialmente para integraciones específicas con proveedores principales (langchain-openai, langchain-anthropic, langchain-ollama, etc.). Estos están optimizados y tienen mejor soporte que las integraciones genéricas.

Ventajas de esta arquitectura:

Instalaciones ligeras: Solo instalas lo que necesitas. Si solo usas OpenAI, instalas langchain-core y langchain-openai.

Mejor mantenimiento: Cada integración puede evolucionar independientemente.

Menos conflictos de dependencias: Las integraciones específicas no afectan al core.

Actualizaciones más rápidas: Los partner packages se pueden actualizar sin esperar releases del paquete principal.

Implicaciones prácticas:

En la actualidad, cuando veas ejemplos de código, notarás imports como:
```python

from langchain_core.prompts import ChatPromptTemplate  # Abstracciones base
from langchain.chains import ConversationChain         # Funcionalidad de alto nivel
from langchain_openai import ChatOpenAI                # Integración específica
from langchain_community.vectorstores import FAISS    # Herramienta de terceros
```


Esta estructura te ayuda a entender qué está pasando bajo el capó y te permite hacer instalaciones más selectivas según tus necesidades.


##  Lectura: ¿Qué es Streamlit?
Antes de sumergirnos en la construcción del chatbot, necesitamos entender qué hace especial a Streamlit y por qué es la herramienta perfecta para nuestro proyecto. Streamlit es, en esencia, la respuesta a una pregunta que todo científico de datos o desarrollador de IA se ha hecho alguna vez: "¿Por qué necesito aprender JavaScript, HTML y CSS solo para mostrar mi modelo en funcionamiento?"

La filosofía del "script que se convierte en app"
Streamlit opera bajo una premisa revolucionaria: tu script de Python es tu aplicación web. No hay separación entre lógica de backend y frontend, no hay archivos de configuración complejos ni servidores que montar. Escribes código Python normal y corriente, añades unas pocas funciones que empiezan con st., y mágicamente tienes una aplicación web interactiva.

Esta simplicidad no es casualidad. Los creadores de Streamlit observaron que la mayoría de aplicaciones de datos siguen un patrón similar: muestran información, permiten al usuario interactuar con controles, y actualizan la vista. En lugar de obligarte a manejar estados complejos y ciclos de vida de componentes, Streamlit dice: "Dime qué quieres mostrar, yo me encargo del resto."

El ciclo reactivo: la magia detrás del telón
El corazón de Streamlit es su modelo de ejecución reactiva. Cada vez que el usuario interactúa con tu aplicación (presiona un botón, escribe en un campo, mueve un slider) Streamlit vuelve a ejecutar tu script completo de arriba a abajo. Este "rerun" recalcula toda la interfaz basándose en el nuevo estado.

Para quienes vienen del desarrollo web tradicional, esto puede sonar ineficiente. ¿Reejecutar todo el código en cada interacción? Pero Streamlit ha optimizado este proceso de tal manera que se siente instantáneo, y la simplicidad conceptual que aporta es inmensa: no tienes que pensar en qué partes de tu interfaz necesitan actualizarse; Streamlit se encarga de todo.

Estado persistente: la memoria de tu aplicación
Aquí surge una pregunta natural: si el script se ejecuta desde cero en cada interacción, ¿cómo mantenemos información entre clicks? La respuesta es st.session_state, un diccionario especial que Streamlit mantiene en memoria para cada sesión de usuario.

Piensa en st.session_state como la memoria a corto plazo de tu aplicación. Ahí puedes guardar el historial de mensajes de tu chatbot, contadores, configuraciones del usuario, o cualquier dato que necesite sobrevivir al siguiente rerun. Es tu espacio personal de almacenamiento por sesión de navegador.

Componentes listos para usar: enfócate en lo importante
Una de las grandes fortalezas de Streamlit es su biblioteca de componentes pre-construidos. Para nuestro chatbot, esto significa que no necesitaremos diseñar burbujas de chat, manejar layouts complejos, o crear campos de entrada personalizados. Streamlit incluye st.chat_message() para mostrar mensajes con el formato visual correcto, y st.chat_input() para capturar la entrada del usuario con el estilo de un chat moderno.

Esta filosofía de "componentes inteligentes" se extiende por toda la librería: gráficos con st.plotly_chart(), tablas con st.dataframe(), controles de archivo con st.file_uploader(). Cada función encapsula no solo la funcionalidad, sino también las mejores prácticas de diseño UX.

Declarativo y progresivo: código que se lee como se ve
El diseño en Streamlit es declarativo: el orden en que escribes las funciones st.* es exactamente el orden en que aparecen en la pantalla. ¿Quieres un título, después una descripción, luego el chat, y finalmente el input del usuario? Simplemente escríbelos en ese orden. No hay divs, no hay CSS, no hay posicionamiento absoluto. Tu código se lee como un mapa visual de tu aplicación.

Además, Streamlit es progresivo. Puedes empezar con la estructura más simple (una columna de elementos apilados) y después añadir complejidad: columnas lado a lado con st.columns(), pestañas con st.tabs(), o barras laterales con st.sidebar. Pero para nuestro chatbot, la simplicidad lineal será perfecta.

El ciclo de vida de una conversación
En una aplicación de chat con Streamlit, el flujo mental es siempre predecible:

Inicialización: Verificas si st.session_state tiene el historial de mensajes; si no, lo creas vacío.

Renderizado del historial: Recorres los mensajes guardados y los muestras con st.chat_message().

Captura de entrada: Usas st.chat_input() para obtener el nuevo mensaje del usuario.

Procesamiento: Si hay un mensaje nuevo, lo añades al historial, consultas tu modelo de IA, y añades también la respuesta.

Actualización automática: Streamlit detecta los cambios en session_state y vuelve a ejecutar el script, mostrando la conversación actualizada.

Este ciclo, repetido en cada turno, crea la ilusión de una conversación fluida, cuando en realidad son múltiples ejecuciones independientes del mismo script.

Secretos y configuración: seguridad sin complejidad
Las aplicaciones reales necesitan manejar credenciales: API keys, tokens de acceso, configuraciones sensibles. Streamlit resuelve esto con su sistema de "secretos", que puede leer tanto de variables de entorno del sistema como de archivos de configuración especiales cuando despliegas en Streamlit Cloud.

La regla de oro es simple: las claves nunca van en el código. Streamlit facilita este principio con st.secrets, que actúa como un diccionario donde puedes acceder a tus credenciales de forma segura, sin exponerlas en tu repositorio.

Cachés inteligentes: optimización cuando la necesites
Aunque nuestro proyecto inicial no lo requerirá, Streamlit incluye decoradores de caché sofisticados: @st.cache_data para datos y @st.cache_resource para objetos complejos como modelos de ML. Estos mecanismos evitan recálculos costosos en cada rerun, manteniendo la responsividad de tu aplicación incluso cuando grows.

El caché de Streamlit es inteligente: detecta automáticamente cuando los parámetros de entrada cambian y solo entonces vuelve a ejecutar la función. Para cargar un modelo pesado o procesar un dataset grande, estos decoradores son invaluables.

Streamlit vs. el mundo web tradicional
Streamlit no pretende competir con React + Flask para aplicaciones web de producción a gran escala. Su propuesta de valor es diferente: ser el puente más rápido entre una idea y una demostración interactiva. Es el equivalente web de un Jupyter notebook: perfecto para explorar, prototipar y compartir, con la ventaja adicional de una interfaz amigable para usuarios no técnicos.

Para nuestro chatbot, esta filosofía es perfecta. No necesitamos escalabilidad extrema ni arquitecturas complejas; necesitamos iterar rápido y mantener el foco en la lógica de conversación, no en los detalles de presentación.

Lo que Streamlit nos regala en este proyecto
Resumiendo, Streamlit nos aporta exactamente lo que necesitamos:

Una interfaz de chat lista para usar, sin maquetación manual ni CSS.

Estado persistente por sesión que mantiene viva la conversación entre interacciones.

Un modelo mental simple: cada rerun es una nueva oportunidad de mostrar el estado actual.

Extensibilidad natural: podemos empezar simple y añadir complejidad gradualmente.

Un camino claro hacia el despliegue: de prototipo local a aplicación compartible en la nube.

Con este entendimiento, en la siguiente sección podremos concentrarnos completamente en la lógica del chatbot y su integración con LangChain, confiando en que Streamlit traducirá nuestras intenciones en una interfaz clara y funcional para nuestros usuarios.

## Para ejecutar un streamlit app
Para ejecutar la app, abre una terminal y navega hasta el directorio donde se encuentra el archivo `streamlit_chatbot.py`. Luego, ejecuta el siguiente comando:

```bash
streamlit run streamlit_chatbot.py
```

Esto iniciará la app en tu navegador predeterminado. Puedes interactuar con el chatbot escribiendo mensajes en la caja de texto y presionando Enter. La conversación se mostrará en la interfaz, y el historial se guardará en `st.session_state`.

## Langchain tipos de mensaje
AI: Mensaje generado por el modelo de IA.
Human: Mensaje enviado por el usuario.
System: Mensaje que define el comportamiento del modelo.

Tarea: Mejoras adicionales: LCEL, Prompt Templates, Streaming...
📋 Objetivo

En esta tarea transformarás tu chatbot básico en una aplicación más robusta y profesional. Aprenderás a implementar funcionalidades como configuración dinámica, templates de prompts, streaming de respuestas y mejor manejo de errores.

⚠️ Importante: Esta tarea contiene conceptos avanzados y es completamente normal que no puedas completar todos los puntos en tu primer intento. No te preocupes si encuentras dificultades, el objetivo es que explores, experimentes y aprendas el proceso. La solución completa está disponible en la siguiente clase del curso para que puedas consultar y comparar tu progreso. ¡Haz lo que puedas y disfruta el proceso de aprendizaje!



🎯 Lo que aprenderás

PromptTemplate: Cómo crear prompts estructurados y reutilizables

LCEL (LangChain Expression Language): El nuevo paradigma de cadenas en LangChain

Streaming: Respuestas en tiempo real para mejor experiencia de usuario

Configuración dinámica: Permitir al usuario ajustar parámetros del modelo

Manejo de errores: Hacer tu aplicación más robusta



🏁 Punto de partida

Tu código actual debería verse similar al siguiente:

from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import streamlit as st
 
# Configurar la página de la app
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")
st.title("🤖 Chatbot Básico con LangChain")
st.markdown("Este es un *chatbot de ejemplo* construido con LangChain + Streamlit. ¡Escribe tu mensaje abajo para comenzar!")
 
chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
 
# Inicializar el historial de mensajes
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
 
# Mostrar mensajes previos en la interfaz
for msg in st.session_state.mensajes:
    if isinstance(msg, SystemMessage):
        # No muestro el mensaje por pantalla
        continue
    
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)
 
# Cuadro de entrada de texto de usuario
pregunta = st.chat_input("Escribe tu mensaje: ")
 
if pregunta:
    # Mostrar inmediatamente el mensaje del usuario en la interfaz
    with st.chat_message("user"):
        st.markdown(pregunta)
    
    # Almacenamos el mensaje en la memoria de streamlit
    st.session_state.mensajes.append(HumanMessage(content=pregunta))
    
    # Generar respuesta usando el modelo de lenguaje
    respuesta = chat_model.invoke(st.session_state.mensajes)
    
    # Mostrar la respuesta en la interfaz
    with st.chat_message("assistant"):
        st.markdown(respuesta.content)
    
    st.session_state.mensajes.append(respuesta)


🛠️ Mejoras a implementar

1. Sidebar de Configuración

Objetivo: Permitir al usuario ajustar la temperatura y seleccionar el modelo.

Pista: Usa st.sidebar para crear una barra lateral. Dentro de ella:

with st.sidebar:
    st.header("Configuración")
    temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)
    model_name = st.selectbox("Modelo", ["gpt-3.5-turbo", "gpt-4", "gpt-4o-mini"])
    
    # ¿Cómo recrearías el modelo con los nuevos parámetros?
    chat_model = # ¡Completa aquí!


Pregunta reflexiva: ¿Por qué es útil recrear el modelo cada vez que cambian los parámetros?



2. Implementando PromptTemplate

Objetivo: Crear un template estructurado que incluya el historial de conversación.

Importación necesaria:

from langchain.prompts import PromptTemplate

Tu turno: Crea un PromptTemplate que:

Tenga variables mensaje e historial

Defina la personalidad del chatbot

Use el historial para mantener contexto

prompt_template = PromptTemplate(
    input_variables=["mensaje", "historial"],
    template="""Eres un asistente útil y amigable llamado ChatBot Pro. 
 
Historial de conversación:
{historial}
 
Responde de manera clara y concisa a la siguiente pregunta: {mensaje}"""
)


3. LCEL - LangChain Expression Language

Objetivo: Usar el nuevo paradigma de cadenas con el operador |.

Concepto clave: LCEL permite encadenar componentes de forma intuitiva:

# En lugar de usar cadenas tradicionales, ahora puedes hacer:
cadena = prompt_template | chat_model


¿Qué hace esto?: El operador | conecta el output del PromptTemplate directamente al input del ChatModel.



4. Streaming de Respuestas

Objetivo: Mostrar la respuesta del modelo palabra por palabra, como ChatGPT.

Implementación sugerida:

if pregunta:
    with st.chat_message("user"):
        st.markdown(pregunta)
    
    try:
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
 
            # ¡Aquí está la magia del streaming!
            for chunk in cadena.stream({"mensaje": pregunta, "historial": st.session_state.mensajes}):
                full_response += chunk.content
                response_placeholder.markdown(full_response + "▌")  # El cursor parpadeante
            
            response_placeholder.markdown(full_response)
        
        # No olvides almacenar los mensajes
        st.session_state.mensajes.append(HumanMessage(content=pregunta))
        st.session_state.mensajes.append(AIMessage(content=full_response))
        
    except Exception as e:
        # ¿Qué tipo de errores podrían ocurrir aquí?
        st.error(f"Error al generar respuesta: {str(e)}")
        st.info("Verifica que tu API Key de OpenAI esté configurada correctamente.")


Pregunta: ¿Qué representa el símbolo "▌" en el código anterior?



5. Botón de Nueva Conversación

Objetivo: Permitir al usuario limpiar el historial fácilmente.

Pista simple:

if st.button("🗑️ Nueva conversación"):
    # ¿Qué necesitas limpiar?
    # ¿Qué función de Streamlit refresca la página?


💡 Reflexiones Finales

¿Qué ventajas tiene usar PromptTemplate vs. strings simples?

¿Cómo mejora LCEL la legibilidad del código?

¿Por qué el streaming mejora la experiencia de usuario?

¿Qué otros errores podrías manejar en una aplicación real?



¡Diviértete construyendo y no dudes en experimentar con las funcionalidades! 🚀