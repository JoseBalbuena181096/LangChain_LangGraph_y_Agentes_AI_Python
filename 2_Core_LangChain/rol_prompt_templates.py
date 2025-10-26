from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

plantilla_sistema = SystemMessagePromptTemplate.from_template(
    "Eres un {rol} especializado en {especialidad}. Responde de manera {tono}"
)

plantilla_humano = HumanMessagePromptTemplate.from_template(
    "Mi pregunta sobre {tema} es: {pregunta}"
)

chat_prompt = ChatPromptTemplate.from_messages([
    plantilla_sistema,
    plantilla_humano
])

mensajes = chat_prompt.format_messages(
    rol="maestro de robótica",
    especialidad="en colegios de prescolar hasta preparatoria",
    tono="conciso y profesional",
    tema="Electrónica",
    pregunta="¿Qué es un led?"
)

for m in mensajes:
    print(m.content)