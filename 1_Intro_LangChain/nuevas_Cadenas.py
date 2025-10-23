from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

from dotenv import load_dotenv
load_dotenv()
import os

print(os.getenv("OPENAI_API_KEY"))

chat = ChatOpenAI(model = "gpt-5-nano", temperature = 0.7)

plantilla = PromptTemplate(
    # son las variables dinamicas que cambian  en el prompt
    input_variables=["nombre"],
    template="Saluda al usuario con su nombre. \nEl nombre es {nombre}\nAsistente:"
)

## la cadena se forma, de manera que la plantilla se le pasa como entrada al chat
chain = plantilla | chat

## Invocar la cadena
response = chain.invoke({"nombre": "Jose"})
print("Respuesta del modelo: ", response.content)
