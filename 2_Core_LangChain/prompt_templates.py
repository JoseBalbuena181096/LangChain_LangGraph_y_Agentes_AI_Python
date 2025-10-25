from langchain_core.prompts import PromptTemplate

template = "Eres un experto en marketing. Sugiere un eslogan creativo para un producto de {producto}"

## construimos el prompt con la plantilla
prompt = PromptTemplate(
    template=template,
    input_variables=["producto"]
)

## probar la plantilla antes de enviarlo al modelo
full_prompt = prompt.format(producto="tecnología")
print(full_prompt)

