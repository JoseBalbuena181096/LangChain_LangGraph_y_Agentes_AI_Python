from langchain_core.tools import tool
from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI
from typing import Tuple
import os
from dotenv import load_dotenv
from operator import attrgetter

load_dotenv()

llm = ChatOpenAI(model_name="gpt-5-nano", temperature=0)


@tool("user_db_tool", response_format="content_and_artifact")
def herramienta_perzonalizada(query: str) -> Tuple[str, int]:
    """ Consulta la base de usarios de la empresa. """
    # Código que accede a la base de datos 
    return f"Respuesta a la consulta: {query}", 10

# def herramienta_perzonalizada2(query: str) -> str:
#     """ Consulta la base de datos de usarios de la empresa. """
#     # Código que accede a la base de datos 
#     return f"Respuesta a la consulta: {query}"


llm_with_tools = llm.bind_tools([herramienta_perzonalizada])
response = llm_with_tools.invoke("Genera un resumen de la información que hay en la base de datos para el usario UX341234")
tool_response = herramienta_perzonalizada.invoke(
    response.tool_calls[0]["args"]
)

chain = llm_with_tools | attrgetter("tool_calls") | herramienta_perzonalizada.map()

response = chain.invoke("Genera un resumen de la información que hay en la base de datos para el usuario UX341234")
print(response[0].content)

# output = herramienta_perzonalizada.run("¿Cuántos usuarios hay en la base de datos?")
# print(output)  # Debería imprimir la respuesta a la consulta
# print(herramienta_perzonalizada.name)  # Imprime el nombre de la herramienta
# print(herramienta_perzonalizada.description)  # Imprime la descripción de la herramienta

# mi_tool = StructuredTool.from_function(herramienta_perzonalizada2)
# output = mi_tool.run("¿Cuántos usuarios hay en la base de datos?")
# print(output)  # Debería imprimir la respuesta a la consulta
# print(mi_tool.description)  # Imprime la descripción de la herramienta
# print(mi_tool.name)  # Imprime el nombre de la herramienta