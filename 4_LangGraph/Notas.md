## LangGraph
LangGraph es una biblioteca de Python diseñada para facilitar la creación y gestión de grafos de conocimiento utilizando modelos de lenguaje. Proporciona herramientas para construir, manipular y consultar grafos de conocimiento de manera eficiente, integrando capacidades avanzadas de procesamiento del lenguaje natural.

### Características principales
- **Construcción de grafos**: Permite crear grafos de conocimiento a partir de diversas fuentes de datos, incluyendo texto sin estructurar.
- **Manipulación de grafos**: Ofrece funciones para agregar, eliminar y modificar nodos y aristas en el grafo.
- **Consultas avanzadas**: Soporta consultas complejas utilizando lenguaje natural para extraer información relevante del grafo.
- **Integración con modelos de lenguaje**: Compatible con varios modelos de lenguaje para mejorar la comprensión y generación de texto.
- **Visualización de grafos**: Proporciona herramientas para visualizar grafos de conocimiento de manera interactiva.   
- **Extensibilidad**: Diseñado para ser fácilmente extensible, permitiendo a los desarrolladores agregar nuevas funcionalidades según sus necesidades.

## Lectura: Componentes fundamentales de LangGraph
Fundamentos de LangGraph: State, Nodes y Edges Explicados
LangGraph representa una evolución natural en la construcción de aplicaciones de IA complejas. Mientras que las chains lineales de LangChain nos permitieron crear flujos secuenciales básicos, LangGraph introduce un paradigma completamente nuevo basado en grafos que nos habilita a construir workflows verdaderamente sofisticados y adaptativos.

En este artículo, exploraremos los tres componentes fundamentales que hacen de LangGraph una herramienta tan poderosa: State (Estado), Nodes (Nodos) y Edges (Aristas). Comprender estos conceptos es esencial para aprovechar al máximo las capacidades de LangGraph en tus aplicaciones de IA.

El Paradigma del StateGraph
Antes de profundizar en los componentes individuales, es crucial entender el concepto central que los unifica: el StateGraph.

Un StateGraph es un tipo especial de grafo donde todos los nodos comparten un estado mutable común. Esto representa un cambio fundamental respecto a las arquitecturas tradicionales:

Arquitectura Chain Lineal:

Input → Paso A → Output A → Paso B → Output B → Paso C → Final Output


StateGraph de LangGraph:

                    Estado Global Compartido
                      ↕        ↕        ↕
Input → Nodo A ←→ Nodo B ←→ Nodo C ←→ Output


Esta diferencia arquitectónica permite funcionalidades avanzadas como memoria persistente, acumulación de resultados y flujos de control complejos con loops y ramificaciones condicionales.



1. State (Estado): La Memoria Compartida del Grafo
¿Qué es el State?
El State es la información compartida y persistente a lo largo de todo el grafo. Piensa en él como una "base de datos" común donde todos los nodos pueden leer y escribir información de manera colaborativa.

A diferencia de una chain lineal donde cada paso produce una salida que es la entrada del siguiente, en LangGraph todos los nodos pueden acceder y modificar un estado global común. Esto proporciona una flexibilidad extraordinaria para manejar información compleja y flujos de trabajo no lineales.

Características clave del State
Global y Accesible: Todos los nodos del grafo pueden leer cualquier información almacenada en el estado. Esto elimina la necesidad de pasar datos explícitamente entre nodos.

Mutable y Evolutivo: El estado se actualiza a medida que los nodos ejecutan. Cada nodo puede modificar parcial o totalmente el diccionario de estado según sus necesidades.

Tipado y Estructurado: Se define mediante esquemas claros (como TypedDict o dataclass) que especifican las claves y tipos de datos que contendrá. Esto proporciona claridad sobre qué información está disponible.

Flexible: Permite compartir datos complejos entre diferentes partes del workflow, desde strings simples hasta objetos complejos, listas de mensajes, resultados de búsquedas, etc.

El Estado como Contrato
El estado actúa como un "contrato" entre todos los nodos del grafo. Cuando definimos el esquema del estado, estamos estableciendo:

Qué campos estarán disponibles

Qué tipo de datos contendrá cada campo

Cómo los nodos pueden interactuar con esa información

Por ejemplo, podríamos definir un estado con campos como pregunta: str, respuesta: str, intentos: int, documentos_relevantes: List[str], etc. Esto da a todos los nodos una comprensión clara de qué información pueden esperar y cómo pueden contribuir.

Ventajas del State Compartido
Memoria de Conversación: Mantiene el contexto completo entre diferentes pasos del workflow, permitiendo conversaciones naturales y coherentes.

Acumulación de Resultados: Permite que múltiples nodos contribuyan información complementaria que se va construyendo gradualmente.

Decisiones Informadas: Los nodos posteriores pueden tomar decisiones basadas en toda la información acumulada por nodos anteriores.

Flexibilidad de Flujo: No requiere predefinir todas las conexiones entrada-salida, permitiendo workflows más dinámicos y adaptativos.



2. Nodes (Nodos): Las Unidades de Trabajo
¿Qué es un Nodo?
Un Nodo es la unidad básica de trabajo en LangGraph. Representa una acción o tarea atómica que puede leer del estado global y contribuir actualizaciones específicas al mismo.

La filosofía detrás de los nodos es simple pero poderosa: cada nodo es una función que recibe el estado completo como entrada y devuelve un diccionario parcial con las actualizaciones que quiere aplicar al estado.

La Firma de un Nodo: State → PartialState
Esta es la característica más importante de entender sobre los nodos: no devuelven un estado completo, solo devuelven las partes del estado que ellos modifican.

LangGraph se encarga automáticamente de:

Pasar el estado completo al nodo

Recibir las actualizaciones parciales del nodo

Fusionar esas actualizaciones con el estado global

Propagar el estado actualizado al siguiente nodo

Esto significa que cada nodo puede enfocarse únicamente en su tarea específica sin preocuparse por mantener o propagar información que no le concierne.

Tipos Conceptuales de Nodos
Nodos de Procesamiento: Realizan transformaciones sobre datos existentes en el estado. Por ejemplo, un nodo que procesa resultados de búsqueda o que analiza el sentimiento de un texto.

Nodos de Generación: Crean nuevo contenido, típicamente usando LLMs. Por ejemplo, un nodo que genera una respuesta basada en documentos recuperados.

Nodos de Recuperación: Obtienen información externa y la añaden al estado. Por ejemplo, un nodo que busca información en bases de datos o APIs externas.

Nodos de Decisión: Evalúan condiciones y pueden modificar flags o contadores en el estado que luego influencian el flujo de ejecución.

Nodos de Validación: Verifican la calidad o corrección de información en el estado y pueden añadir métricas de confianza o indicadores de validez.

Principios de Diseño de Nodos
Responsabilidad Única: Cada nodo debe tener un propósito claro y específico. Un nodo que hace "demasiadas cosas" es difícil de debuggear y reutilizar.

Atomicidad: Los nodos deben representar tareas atómicas que se pueden ejecutar de manera independiente y completa.

Actualizaciones Mínimas: Solo deben devolver las claves del estado que realmente modifican, no todo el estado.

Determinismo: Idealmente, ejecutar el mismo nodo con el mismo estado debería producir el mismo resultado (cuando sea posible).



3. Edges (Aristas): El Control de Flujo
¿Qué son los Edges?
Los Edges son las conexiones dirigidas entre nodos que determinan el orden de ejecución y el flujo de control del grafo. Son fundamentalmente diferentes a las simples "tuberías" entre funciones porque pueden ser condicionales y dinámicos.

Tipos de Edges
Edges Normales (Fijos): Representan conexiones determinísticas que siempre dirigen el flujo de un nodo específico a otro. Son útiles para secuencias de pasos que siempre deben ejecutarse en orden.

Edges Condicionales: Permiten ramificación dinámica basada en el estado actual. Una función de decisión examina el estado y determina cuál debe ser el próximo nodo a ejecutar. Esto es lo que hace posible workflows realmente inteligentes y adaptativos.

Nodos Especiales: START y END
START: Es el punto de entrada del grafo. No ejecuta lógica propia, simplemente recibe el estado inicial que proporcionamos al invocar el grafo.

END: Es el punto de terminación del grafo. Indica que el workflow ha completado exitosamente y devuelve el estado final.

Estos nodos especiales proporcionan puntos de anclaje claros para el flujo de ejecución y hacen que el grafo sea más fácil de entender y debuggear.

Control de Flujo Avanzado
Los edges condicionales son donde LangGraph realmente brilla. Permiten implementar lógica de control sofisticada como:

Bucles de Retry: Si un nodo no produce un resultado satisfactorio, el flujo puede volver a ejecutar nodos anteriores.

Ramificación Basada en Calidad: Diferentes caminos de ejecución según la calidad o confianza de los resultados.

Escalamiento Gradual: Intentar métodos simples primero, y escalar a métodos más complejos o costosos si es necesario.

Paralelización Condicional: Ejecutar diferentes ramas del grafo en paralelo según las condiciones del estado.



Consideraciones de Diseño
Planificación del Estado
El diseño del estado es crucial. Debes planificar cuidadosamente qué información necesitará estar disponible, cómo evolucionará a lo largo del workflow, y cómo evitar conflictos cuando múltiples nodos escriben información relacionada.

Gestión de Complejidad
Aunque LangGraph permite workflows muy complejos, es importante mantener un equilibrio. Un grafo demasiado complejo puede volverse difícil de entender, debuggear y mantener.

Funciones Reducer
Cuando múltiples nodos pueden escribir en las mismas claves del estado, LangGraph usa funciones "reducer" para determinar cómo combinar las actualizaciones. Entender este concepto es crucial para workflows avanzados. (Lo veremos en las siguientes clases)

Conclusión
Los componentes fundamentales de LangGraph (State, Nodes y Edges) trabajan juntos para crear un paradigma poderoso y flexible que va mucho más allá de las chains lineales tradicionales.

Conceptos clave para recordar:

State actúa como memoria compartida y persistente entre todos los nodos

Nodes encapsulan lógica específica y solo devuelven actualizaciones parciales del estado

Edges proporcionan control de flujo inteligente con capacidades condicionales

StateGraph habilita workflows no-lineales, adaptativos y con memoria

Esta arquitectura conceptual abre la puerta a aplicaciones de IA verdaderamente sofisticadas que pueden:

Adaptar su comportamiento dinámicamente

Mantener contexto complejo a largo plazo

Manejar flujos de trabajo iterativos y de refinamiento

Implementar lógica de decisión compleja basada en múltiples factores

En los siguientes videos del curso, veremos cómo estos conceptos se traducen en código práctico y construiremos juntos workflows reales que demuestran el poder de este paradigma.

¿Estás comenzando a visualizar las posibilidades? La verdadera magia de LangGraph emerge cuando estos conceptos fundamentales se combinan con las capacidades avanzadas que exploraremos en las próximas lecciones.

## Los tres componentes fundamentales de LangGraph: State, Nodes y Edges
- **State (Estado)**: Es la memoria compartida y persistente a lo largo de todo el grafo. Todos los nodos pueden leer y escribir información en este estado global, lo que permite mantener contexto y acumular resultados de manera colaborativa.
- **Nodes (Nodos)**: Son las unidades básicas de trabajo en LangGraph. Cada nodo representa una acción o tarea específica que puede leer del estado global y contribuir actualizaciones parciales al mismo.
- **Edges (Aristas)**: Son las conexiones dirigidas entre nodos que determinan el orden de ejecución y el flujo de control del grafo. Pueden ser fijos o condicionales, permitiendo ramificación dinámica basada en el estado actual.

## Proyecto: Sistema de Procesamiento de Reuniones con IA y LangGraph
A continuación te vas a enfrentar a uno de los desafíos más complejos del curso hasta el momento. Para este proyecto, asumiré que eres un ingeniero de IA trabajando en una empresa tecnológica y has recibido el encargo de desarrollar una aplicación de procesamiento automático de reuniones que cumpla con la siguiente especificación técnica. Este ejercicio te permitirá aplicar todo el conocimiento adquirido sobre LangGraph y arquitectura de workflows en un contexto profesional. Encontrarás la resolución en la siguiente clase.

Objetivos del Proyecto
Desarrollar un sistema de procesamiento automático que transforme grabaciones de reuniones o notas desordenadas en documentación empresarial estructurada utilizando LangGraph y modelos de lenguaje.

Nota importante: Este es un proyecto de complejidad considerable. No se espera una implementación completa, sino un enfoque metodológico en el diseño de la solución. El objetivo principal es desarrollar capacidades de pensamiento arquitectónico y comprensión de workflows con LangGraph. La solución completa se presentará en el material complementario.

Descripción del Sistema
Entradas del Sistema
El sistema debe procesar dos tipos de entrada:

Archivos multimedia: Video y audio de reuniones (MP4, MOV, MP3, WAV, M4A, WEBM, MKV)

Documentos de texto: Notas escritas en formato TXT o Markdown

Salidas Estructuradas
Para cada entrada, el sistema debe generar:

Lista identificada de participantes

Temas principales discutidos (3-5 elementos)

Acciones acordadas con responsables asignados

Minuta formal de reunión (máximo 150 palabras)

Resumen ejecutivo conciso (máximo 30 palabras)

Arquitectura del Workflow
Consideraciones de Diseño
Antes de implementar, analice las siguientes cuestiones arquitectónicas:

Modularidad del Proceso: ¿Debería implementarse como un único prompt o como múltiples nodos especializados? Considere las ventajas de la especialización versus la simplicidad.

Secuenciación de Operaciones: Determine el orden óptimo de procesamiento. ¿Es necesario extraer participantes antes que temas? ¿Qué dependencias existen entre las diferentes extracciones de información?

Gestión del Estado: ¿Cómo debe estructurarse la información que fluye entre los diferentes nodos del workflow? ¿Qué campos son necesarios y cuáles opcionales?

Robustez del Sistema: ¿Cómo manejaría casos donde la información está incompleta o es ambigua? ¿Qué estrategias implementaría para inputs de baja calidad?

Estado del Sistema
```python
class State(TypedDict):
    notes: str              # Texto original de entrada
    participants: List[str] # Participantes identificados
    topics: List[str]       # Temas principales
    action_items: List[str] # Acciones y responsables
    minutes: str            # Minuta formal
    summary: str            # Resumen ejecutivo
```

Nodos del Workflow
El sistema debe implementar cinco nodos especializados:

1. Extractor de Participantes

Responsabilidad: Identificar nombres de personas en el texto

Desafío técnico: Distinguir nombres propios de otros términos

Formato de salida: Lista de nombres separados por comas

2. Analizador de Temas

Responsabilidad: Identificar temas principales de discusión

Desafío técnico: Evitar categorías demasiado generales o específicas

Formato de salida: Temas separados por punto y coma

3. Extractor de Acciones

Responsabilidad: Localizar compromisos y asignaciones de responsabilidad

Desafío técnico: Identificar acciones implícitas versus explícitas

Formato de salida: Acciones separadas por pipe (|)

4. Generador de Minutas

Responsabilidad: Crear documento formal estructurado

Input: Información procesada de nodos anteriores

Restricciones: Máximo 150 palabras, tono profesional

5. Creador de Resumen

Responsabilidad: Generar síntesis ejecutiva ultra-concisa

Input: Toda la información procesada

Restricciones: Máximo 30 palabras, enfoque en puntos clave

Flujo de Procesamiento
START → extract_participants → identify_topics → extract_actions → generate_minutes → create_summary → END


Especificaciones Técnicas
Stack Tecnológico
```python
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, List
import openai  # Para transcripción Whisper
from tkinter import filedialog
```

Configuración del Modelo
```python
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
```

Procesamiento de Audio/Video
Para archivos multimedia, implemente transcripción utilizando la API Whisper de OpenAI:

```python
def transcribe_media(file_path: str) -> str:
    client = openai.OpenAI()
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="es",
            response_format="text"
        )
    return transcript
```

Guía de Implementación
Fase 1: Estructura Básica
Defina la clase State con todos los campos requeridos

```python
class State(TypedDict):
    notes: str
    participants: List[str]
    topics: List[str]
    action_items: List[str]
    minutes: str
    summary: str
```

Configure el grafo básico de LangGraph sin lógica de negocio

Implemente un nodo de prueba que procese texto hardcodeado

Verifique que el flujo end-to-end funcione correctamente

Fase 2: Nodos Especializados
Desarrolle prompts específicos para cada tipo de extracción

Implemente la lógica de procesamiento de respuestas del LLM

Conecte todos los nodos en el flujo secuencial definido

Pruebe con datos de ejemplo para validar la calidad de outputs

Fase 3: Integración Completa
Añada capacidad de procesamiento de archivos de texto

Integre la transcripción de archivos multimedia

Implemente interfaz de selección de archivos

Añada manejo de errores y casos edge

Plantilla de Código

```python
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, List
 
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
 
class State(TypedDict):
    notes: str
    participants: List[str]
    topics: List[str]
    action_items: List[str]
    minutes: str
    summary: str
 
def extract_participants(state: State) -> State:
    prompt = f"""
    Analiza las siguientes notas de reunión y extrae únicamente los nombres de los participantes.
    
    Notas: {state['notes']}
    
    Instrucciones:
    - Responde SOLO con nombres separados por comas
    - No incluyas explicaciones adicionales
    - Formato: Juan García, María López, Carlos Ruiz
    """
    
    response = llm.invoke(prompt)
    participants = [p.strip() for p in response.content.split(',') if p.strip()]
    
    return {'participants': participants}
 
def create_workflow():
    workflow = StateGraph(State)
    workflow.add_node("extract_participants", extract_participants)
    # Añadir resto de nodos
    
    workflow.add_edge(START, "extract_participants")
    # Definir resto del flujo
    
    return workflow.compile()
 
if __name__ == "__main__":
    app = create_workflow()
    
    test_state = {
        'notes': "Reunión con Juan García y María López sobre el proyecto...",
        'participants': [],
        'topics': [],
        'action_items': [],
        'minutes': '',
        'summary': ''
    }
    
    result = app.invoke(test_state)
    print(result)
```