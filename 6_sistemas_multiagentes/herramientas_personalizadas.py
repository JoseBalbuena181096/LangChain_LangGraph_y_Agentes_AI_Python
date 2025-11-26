from langchain_core.tools import tool
from langchain_core.tools import StructuredTool

@tool
def herramienta_perzonalizada(query: str, return_direct: bool = True) -> str:
    """ Consulta la base de usarios de la empresa. """
    # Código que accede a la base de datos 
    return f"Respuesta a la consulta: {query}"

def herramienta_perzonalizada2(query: str) -> str:
    """ Consulta la base de datos de usarios de la empresa. """
    # Código que accede a la base de datos 
    return f"Respuesta a la consulta: {query}"


# output = herramienta_perzonalizada.run("¿Cuántos usuarios hay en la base de datos?")
# print(output)  # Debería imprimir la respuesta a la consulta
# print(herramienta_perzonalizada.name)  # Imprime el nombre de la herramienta
# print(herramienta_perzonalizada.description)  # Imprime la descripción de la herramienta

mi_tool = StructuredTool.from_function(herramienta_perzonalizada2)
output = mi_tool.run("¿Cuántos usuarios hay en la base de datos?")
print(output)  # Debería imprimir la respuesta a la consulta
print(mi_tool.description)  # Imprime la descripción de la herramienta
print(mi_tool.name)  # Imprime el nombre de la herramienta