from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# Definir el estado
class State(TypedDict):
    numero: int
    resultado: str

graph = StateGraph(State)

# Definir nodos del workflow

def caso_par(state):
    return {
        'resultado': "El número es par"
    }

def caso_impar(state):
    return {
        'resultado': "El número es impar"
    }

graph.add_node("Par", caso_par)
graph.add_node("Impar", caso_impar)

# Definir la función de routing para decidir la rama de ejecución

def decidir_rama(state):
    if state['numero'] % 2 == 0:
        return "Par"
    return "Impar"

# Añadir el edge conditional al workflow
graph.add_conditional_edges(START, decidir_rama)

# Conectar los nodos finales
graph.add_edge("Par", END)
graph.add_edge("Impar", END)

compiled = graph.compile()

# Probar el workflow con diferentes entradas
print(compiled.invoke({'numero': 43}))
print(compiled.invoke({'numero': 72}))