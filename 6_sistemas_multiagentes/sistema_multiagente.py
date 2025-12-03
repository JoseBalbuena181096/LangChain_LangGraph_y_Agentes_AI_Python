from langchain.agents import create_agent
from langgraph_supervisor import create_supervisor
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

import os
from dotenv import load_dotenv
from pathlib import Path

# Cargar variables de entorno desde el directorio raíz del proyecto
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)

# Configurar el directorio de trabajo
original_dir = os.getcwd()
os.chdir(r"/home/jose/Ingenieria_de_LLM/LangChain_LangGraph_y_Agentes_AI_Python/6_sistemas_multiagentes")


model = ChatOpenAI(model="gpt-5-nano", temperature=0)

# Definir herramientas personalizadas
@tool
def buscar_web(query: str) -> str:
    """Buscar informacion en la web."""
    return f"Resultados de busqueda para: {query}"

@tool
def calcular(expresion: str) -> str:
    """Realizar calculos matematicos."""
    return f"Resultado: {eval(expresion)}"

# Crear agentes especializados
agente_investigacion = create_agent(
    model=model,
    tools=[buscar_web],
    system_prompt="Eres un especialista en investigacion web.",
    name="investigador"
)

agente_matematicas = create_agent(
    model=model,
    tools=[calcular],
    system_prompt="Eres un especialista en calculos matematicos.",
    name="matematico"
)

# Crear supervisor que coordina los agentes
supervisor_graph = create_supervisor(
    [agente_matematicas, agente_investigacion],
    model=model,
    prompt="Eres un supervisor que delega tareas a especialistas segun el tipo de consulta."
)

supervisor = supervisor_graph.compile()

# Uso del sistema multi-agente
response = supervisor.invoke({
    "messages": [{
        "role": "user",
        "content": "Suma 10 + 12"
    }]
})

for msg in response['messages']:
    print(msg.content)