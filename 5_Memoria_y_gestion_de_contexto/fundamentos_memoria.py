from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI 
import os
from dotenv import load_dotenv 

load_dotenv()
print(os.getenv("OPENAI_API_KEY"))

llm = ChatOpenAI(model="gpt-5-nano", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente útil."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | llm

history = []

print("Chat en terminal (escribe 'salir' para terminar)\n")

while True:
    try:
        user_input = input("Tú: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nHasta luego!")
        break

    if not user_input:
        continue
    if user_input.lower() in {"salir", "exit", "quit"}:
        print("Hasta luego!")
        break

    respuesta = chain.invoke({"history": history,"input": user_input})
    print("Asistente:", respuesta.content)

    # Actualizar el historial de la conversación
    history.extend([
        HumanMessage(content=user_input), 
        AIMessage(content=respuesta.content)])