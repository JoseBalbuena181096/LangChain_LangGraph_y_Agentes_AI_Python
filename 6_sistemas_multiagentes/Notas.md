## Agente de IA
Un agente es un sistema impulsado por un LLM, pero que decide sus propias acciones para cumplir con un objetivo final.

El rasgo que define a los agentes es su capacidad para elegir el merjor orden de acciones para resolver un problema dado un conjunto de herramientas.

### Combina varios componentes

1. Un modelo de LLM (el cerebro del agente)
2. Un sistema de herramientas (hacer diferesntes acciones que el agente puede realizar)
3. El promt del agente (Plantilla de razonamiento, con el patron REACT 
    Pensamiento
    Accion
    Observacion
    Respuesta
)
4. Memoria (recirdar interacciones anteriores)

## Ciclo de pensamiento general de un agente es el siguiente: 

- Recibir la instruccion del usuario 
- El agente va a pensar sengun la plantilla de razonamiento
- El acente va elegir la accion que va a realizar, (llamar a una herramienta dentro de sus herramientas disponibles)
- Ejecutar la herramienta escogida por el agente
- Obtener la respuesta de la herramienta
- Realizar una observacion  de la respuesta de la herramienta (el agente incorpora el resultado de la herramienta a su contexto)
- Volver a pensar desde donde lo dejo
- Lo repite hasta que el agente llegue a su objetivo final, que es la respuesta al usuario+


## Sistema multiagente
Un sistema multiagente es un sistema compuesto por varios agentes de IA que interactúan entre sí para lograr objetivos individuales o colectivos. Es preferible cuando una tarea es demasiado compleja para un solo agente o cuando se requiere especialización en diferentes áreas.

Red de agentes (Network): Los agentes pueden comunicarse y colaborar entre sí para compartir información y coordinar acciones.

Supervisor central (Supervisor): Un agente supervisor puede monitorear y gestionar las interacciones entre los agentes para asegurar que se mantenga el enfoque en los objetivos generales del sistema.

Equipos jerárquicos (Hierarchical Teams): Los agentes pueden organizarse en equipos con diferentes niveles de autoridad y responsabilidad para manejar tareas complejas de manera más eficiente.

La mas frecuente de usar es supervisor central.

## Lectura: Agentes preconfigurados recomendados en LangChain y LangGraph
El ecosistema de agentes en LangChain ha evolucionado significativamente. Mientras que las versiones anteriores dependían de tipos de agente enumerados (AgentType.ZERO_SHOT_REACT_DESCRIPTION, etc.), el enfoque moderno se basa en builders (constructores) más flexibles y la migración hacia LangGraph para casos de producción.

LangChain Builders (Compatibilidad y Casos Específicos)
LangChain mantiene varios builders para compatibilidad con proyectos existentes y casos de uso específicos:

Agentes modernos recomendados:

create_tool_calling_agent: Builder "moderno" que usa tool-calling nativo del modelo (OpenAI, Anthropic, Gemini, etc.). Recomendado por defecto si tu LLM soporta herramientas estructuradas. Este agente aprovecha las capacidades nativas de function calling de los modelos más recientes, resultando en llamadas más precisas y eficientes.

create_react_agent: Implementa el patrón ReAct (razonar-actuar) dentro de LangChain tradicional. Útil si quieres el bucle ReAct clásico, aunque la documentación oficial recomienda preferir la versión de LangGraph para producción.

Agentes especializados:

create_openai_functions_agent: Builder para el antiguo esquema de function calling de OpenAI. Úsalo si necesitas compatibilidad con flujos legacy que dependían de la implementación anterior.

create_openai_tools_agent: Variante centrada en el formato OpenAI Tools. Conveniente si ya estandarizas tus prompts/parsers a ese esquema.

create_structured_chat_agent: Diseñado para herramientas con múltiples entradas y flujos de diálogo estructurados. Útil cuando tus herramientas requieren parámetros complejos.

create_json_chat_agent: Requiere que el LLM emita JSON para su lógica/acciones. Útil para auditoría y parsing determinista.

create_self_ask_with_search_agent: Implementa el patrón self-ask (preguntas descompuestas + búsqueda). Útil para QA con descomposición explícita de problemas complejos.

create_xml_agent: Usa XML para formatear razonamiento/acciones. Interesante si tus sistemas de parseo o guardrails ya esperan XML.

LangGraph Prebuilt (Recomendado para Producción)
LangGraph representa el futuro de los agentes en el ecosistema LangChain, proporcionando mayor control, robustez y características avanzadas:

Agente principal:

create_react_agent (langgraph-prebuilt): El prebuilt recomendado para producción. Incluye bucle de tool-calling con memoria opcional, prompt estático/dinámico, structured output (response_format), y manejo robusto de errores. Es la vía rápida y confiable para un agente de propósito general.

Arquitecturas multi-agente:

Supervisor: Paquete langgraph-supervisor con create_supervisor para coordinar varios agentes especializados. Incluye herramientas de handoff y forwarding. Útil cuando quieres orquestar un "equipo de agentes" bajo supervisión central.

Swarm: Paquete langgraph-swarm con create_swarm y utilidades de handoff routing entre agentes. Útil para sistemas donde los agentes se pasan el control dinámicamente según especialidad.

APIs de bajo nivel: Para casos que requieren control total, LangGraph ofrece Graph API / Functional API (StateGraph, nodos, herramientas, memoria, pausing, etc.) para construir agentes completamente personalizados.