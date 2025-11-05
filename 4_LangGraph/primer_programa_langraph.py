from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. Definir el esquema del estado
class State(TypedDict):
    texto_original: str
    texto_mayus: str
    longitud: int

# 2. Crear el grafo de estados
graph = StateGraph(State)

# 3. Definir las funciones de los nodos
def poner_mayusculas(estado: State) -> State:
    texto = estado['texto_original']
    return {
        'texto_mayus': texto.upper(),
    }

def contar_caracteres(estado: State) -> State:
    texto = estado['texto_original']
    return {
        'longitud': len(texto),
    }

# 4. Agregar nodos al grafo
graph.add_node(
    "Mayus", poner_mayusculas
)
graph.add_node(
    "Contar", contar_caracteres
)

# Conectar los nodos en secuencia
graph.add_edge(START, "Mayus")
graph.add_edge("Mayus", "Contar")
graph.add_edge("Contar", END)

#6. Compilar y ejecutar el grafo
compiled_graph = graph.compile()

# 7. Invocar el grafo con un estado inicial
estado_inicial: State = {
    'texto_original': "Hola, LangGraph!",
    'texto_mayus': "",
    'longitud': 0
}

resultado = compiled_graph.invoke(estado_inicial)
print("Estado final:", resultado)