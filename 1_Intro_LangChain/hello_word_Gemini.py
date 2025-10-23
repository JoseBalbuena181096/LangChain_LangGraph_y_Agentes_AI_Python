from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
import os

print(os.getenv("GOOGLE_API_KEY"))

## temperatura controla la aleatoriedad, mientras mas baja mas determinista o esperada, y mas alta mas aleatoria
llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash", temperature = 0.7) 

pregunta = "En que year llego el ser un humano a la luna?"

## Invocar el modelo
response = llm.invoke(pregunta)
print("Respuesta del modelo: ", response.content)
