from langchain_openai import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import os

print(os.getenv("OPENAI_API_KEY"))

# configurar la pagina de la app
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")

st.title("🤖 Chatbot Básico con Langchain")
st.markdown("""
    Este es un *chatbot de ejemplo* construido con langChain + Streamlit. 
    ¡Escribe tu mensaje abajo para comenzar!
""")

## configurar langchain
chat_model = ChatOpenAI(model = "gpt-5-nano", temperature = 0.7)

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
    
    ## Almacenamos el mensaje del usuario en la memoria de streamlit
    st.session_state.mensajes.append(HumanMessage(content=pregunta))
    
    ## Generar respuesta usando el modelo de lenguaje
    respuesta = chat_model.invoke(st.session_state.mensajes)

    ## Mostrar la respuesta del modelo en la interfaz
    with st.chat_message("assistant"):
        st.markdown(respuesta.content)
        
    ## Almacenamos la respuesta del modelo en la memoria de streamlit
    st.session_state.mensajes.append(respuesta)
