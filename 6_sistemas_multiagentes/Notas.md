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