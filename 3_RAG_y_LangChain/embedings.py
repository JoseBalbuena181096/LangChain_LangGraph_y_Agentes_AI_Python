"""
Los Embeddings
Son la piedra angular de la recuperación semántica. De obtener información mediante una consulta, en base
al significado semantico de esa información que esta almacenada.
Es una representacion numerica un vector, que captura el significado semantico de una palabra o una frase.
Para crear un embedding, se pasa una palabra o frase, y esta se transforma en vector de numeros de longitud fija,
este vector es una huella semantica de este texto, que representa ese texto de maneraunivoca y el significado del texto.
Los textos que tengan contenidos similares, producen vectores cercanos entre si en el espacio vectorial, textos que estan 
distantes en el espacio vectorial, tienen significados semánticos diferentes.

Por ejemplo:
La frase "la capital de francia es paris" y "en francia su capital es paris", difieren en el orden de las palabras,
pero tienen el mismo significado semantico, por lo que sus embeddings seran cercanos en el espacio vectorial. Un buen modelo de 
embedding, crearia dos vectores de estas dos fraces que casi se solapan, por que la distancia entre ellos es pequeña, porque 
semanticamente son iguales, tienen el mismo significado.

En lugar "paris es una capital de mascotas" y "paris es la capital de francia" 
estos textos tienen significados semánticos diferentes, por lo que sus embeddings seran distantes en el espacio vectorial.

Los embeddings son esenciales para la recuperación semántica, permitiendo que el modelo entienda y compare el significado 
de las consultas y los documentos almacenados. Un buen modelo de embeddings puede mejorar significativamente la precisión 
y la relevancia de los resultados de la recuperación.

OPENAI Embeddings
text-embedding-3-large (3072)

Existen muchas formas de diferenciar los embeddings y se diferencian del provedor de embeddings.
Por ejemplo, el modelo text-embedding-3-large de OpenAI, tiene una dimension de 3072, mientras que el modelo 
text-embedding-ada-002 tiene una dimension de 1536.

En langchain, todos los embeddings heredan de la misma clase, Embedding, la cual define los metodos basicos que deben 
implementar los embeddings, como la transformacion de texto en vector.
"""

from langchain_openai import OpenAIEmbeddings
import numpy as np

from dotenv import load_dotenv
load_dotenv()
import os

print(os.getenv("OPENAI_API_KEY"))

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

text1 = "La capital de Francia es París."
# text2 = "París es la ciudad capital de Francia."
text2 = "La capital de gatos en Francia esta en Paris."

# A pesar que las dos frases son diferentes, 
# el embedding de cada una de ellas es similar y de igual longitud,
#  por que tienen el mismo significado semantico.
vector1 = embeddings.embed_query(text1)
vector2 = embeddings.embed_query(text2)

print(f"Dime la longitud del vector1: {len(vector1)}")
print(f"Dime la longitud del vector2: {len(vector2)}")

# Similitud entre los vectores
# La distancia entre los vectores es pequeña, por lo que tienen un alto grado de similitud semantica
# para calcular la similitud semantica entre dos vectores, se utiliza la similitud coseno,
# que es el coseno del angulo entre los dos vectores, es basicamente el producto punto de los dos vectores,
# dividido por la multiplicacion de las normas de los dos vectores.
cosine_similarity = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
print(f"La similitud semantica entre los vectores es: {cosine_similarity:.3f}")



