from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
import os

print(os.getenv("OPENAI_API_KEY"))

## temperatura controla la aleatoriedad, mientras mas baja mas determinista o esperada, y mas alta mas aleatoria
llm = ChatOpenAI(model = "gpt-5-nano", temperature = 0.7)

pregunta = "En que year llego el ser un humano a la luna?"

## Invocar el modelo
response = llm.invoke(pregunta)
print("Respuesta del modelo: ", response.content)
