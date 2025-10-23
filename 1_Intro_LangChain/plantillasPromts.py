from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from dotenv import load_dotenv
load_dotenv()
import os

print(os.getenv("OPENAI_API_KEY"))

## temperatura controla la aleatoriedad, mientras mas baja mas determinista o esperada, y mas alta mas aleatoria
chat = ChatOpenAI(model = "gpt-5-nano", temperature = 0.7)

plantilla = PromptTemplate(
    # son las variables dinamicas que cambian  en el prompt
    input_variables=["nombre"],
    template="Saluda al usuario con su nombre. \nEl nombre es {nombre}\nAsistente:"
)

## primer cadena, invocamos el llm con la plantilla definida
chain = LLMChain(llm=chat, prompt=plantilla)

## Invocar la cadena
response = chain.run(nombre="Jose")
print("Respuesta del modelo: ", response)
