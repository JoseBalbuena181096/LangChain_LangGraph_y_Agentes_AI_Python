from langchain_core.runnables import RunnableLambda

# Con runnable lambda permite definir funciones como runnables de lanchaning
paso1 = RunnableLambda(lambda x: f"Numero {x}")

def duplicar_text(texto):
    return [texto] * 2

paso2 = RunnableLambda(duplicar_text)

# creamos nuestra cadena con el operador |, con el paso 1 y 2
cadena = paso1 | paso2

ressultado = cadena.invoke(3)
print(ressultado)
