from langchain_core.prompts import ChatPromptTemplate

# Construir el prompt a base de mensajes
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un traductor del español al inglés muy preciso"),
    ("human", "{texto}"),
])

# Probar la plantilla y como se compone
mensajes = chat_prompt.format_messages(texto="Hola mundo, ¿cómo estás?")
print(mensajes)

for mensaje in mensajes:
    print(f"{type(mensaje)}: {mensaje.content}")