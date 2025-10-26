from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
import os


print(os.getenv("OPENAI_API_KEY"))


class AnalisisTexto(BaseModel):
    resumen: str = Field(description="Resumen breve del texto")
    sentimiento: str = Field(description="Sentimiento del texto (POSITIVO, NEGATIVO, NEUTRO)")


llm =  ChatOpenAI(model = "gpt-5-nano", temperature = 0.7)

structured_llm = llm.with_structured_output(AnalisisTexto)

texto_prueba = "Me encató la nueva película de acción, tiene muchos giros y una trama emocionante."

resultado = structured_llm.invoke(f'Analiza el siguiente texto: {texto_prueba}')
print(resultado)
print(resultado.model_dump_json())
