"""
Una base de datos vectorial es una base de datos que se utiliza para almacenar y recuperar vectores numéricos.

Estos vectores pueden representar datos como texto, imágenes, audio o video, y se utilizan 
para tareas como búsqueda semántica, recomendaciones y clustering.

En una base de datos vectorial se realizan operaciones de búsqueda basadas en la similitud vectorial,
en lugar de la búsqueda basada en texto. 

El elemento que se busca a nivel semántico es el vector que más se aproxima al vector de consulta.

En la mayoria de aplicaciones ocuparemos memoria a largo plazo para almacenar los vectores.
Los fragmento de texto, se vectorizan y se almacenan en la base de datos vectorial. Estas base de
datos pueden implementar diferentes algoritmos de indexación y búsqueda basados en vectores,
como el árbol de vecinos más cercanos (kNN) o el índice invertido. 
El mismo modelo de embeddings que se utilizó para vectorizar los fragmentos de texto,
se utilizará para vectorizar la consulta y realizar la búsqueda semántica.

Algunas base de datos vectoriales populares son:
- Pinecone
- Chroma

"""