from langchain_openai import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.prompts import PromptTemplate

import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import os
import time

print(os.getenv("OPENAI_API_KEY"))

# configurar la pagina de la app
st.set_page_config(
    page_title="Chatbot Básico", 
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🤖 Chatbot Básico con Langchain")
st.markdown("""
    Este es un *chatbot de ejemplo* construido con langChain + Streamlit. 
    ¡Escribe tu mensaje abajo para comenzar!
""")

with st.sidebar:
    st.header("Configuración")
    temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)
    model_name = st.selectbox("Modelo", ["gpt-5-nano", "gpt-3.5-turbo", "gpt-4o-mini"])
    
    # ¿Cómo recrearías el modelo con los nuevos parámetros?
    chat_model = ChatOpenAI(model_name = model_name, temperature = temperature)

if st.button("🗑️ Nueva conversación"):
    # ¿Qué necesitas limpiar?
    # ¿Qué función de Streamlit refresca la página?
    st.session_state.mensajes = []
    st.rerun()

## Inicializar el historial de mensajes
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

## Monstrar mensajes previos en la interfaz de streamlit
for msg in st.session_state.mensajes:
    if isinstance(msg, SystemMessage): # Mensaje del sistema de comportamiento
        # No muestro nada por pantalla
        continue
    role = "assistant" if isinstance(msg, AIMessage) else "user" # Rol del mensaje si este es de la IA o del usuario
    
    with st.chat_message(role):
        st.markdown(msg.content)
    
## Cuadro de entrada de texto de usuario
pregunta = st.chat_input("Escribe tu mensaje: ")

if pregunta:
    ## Mostrar el mensaje del usuario en la interfaz
    with st.chat_message("user"):
        st.markdown(pregunta)
    
    try:
        ## Crear la cadena con el prompt template y el modelo
        prompt_template = PromptTemplate(
            input_variables=["mensaje", "historial"],
            template="""Eres un asistente útil y amigable llamado ChatBot Pro. 
            Historial de conversación:
            {historial}
            Responde de manera clara y concisa a la siguiente pregunta: {mensaje}"""
        )
        
        # Crear la cadena combinando el prompt con el modelo
        cadena = prompt_template | chat_model
        
        ## Mostrar la respuesta del modelo con streaming
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            # Preparar el historial como string
            historial_str = ""
            for msg in st.session_state.mensajes:
                if isinstance(msg, HumanMessage):
                    historial_str += f"Usuario: {msg.content}\n"
                elif isinstance(msg, AIMessage):
                    historial_str += f"Asistente: {msg.content}\n"
            
            # ¡Aquí está la magia del streaming!
            for chunk in cadena.stream({"mensaje": pregunta, "historial": historial_str}):
                full_response += chunk.content
                response_placeholder.markdown(full_response + "▌")  # El cursor parpadeante
                time.sleep(0.025)  # Pequeña pausa para simular "tiempo de escritura"
            
            response_placeholder.markdown(full_response)
        
        # No olvides almacenar los mensajes
        st.session_state.mensajes.append(HumanMessage(content=pregunta))
        st.session_state.mensajes.append(AIMessage(content=full_response))
        
    except Exception as e:
        # ¿Qué tipo de errores podrían ocurrir aquí?
        st.error(f"Error al generar respuesta: {str(e)}")
        st.info("Verifica que tu API Key de OpenAI esté configurada correctamente.")
