from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv


load_dotenv()
print(os.getenv("OPENAI_API_KEY"))


vectorstore = Chroma(
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-large"),
    persist_directory="/home/jose/Ingenieria_de_LLM/LangChain_LangGraph_y_Agentes_AI_Python/3_RAG_y_LangChain/chroma_db"
)

retriver = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 2})

consulta = "¿Dónde se encuentra el contrato en el que participó María Jiménez Campos?"
resultados = retriver.invoke(consulta)

print(f"Se encontraron {len(resultados)} chunks de texto relevantes")
for i, doc in enumerate(resultados):
    print(f"Chunk {i+1}:")
    snipdoc = doc.page_content[:200] + "..."
    print(f"contenido: {snipdoc}")
    print(f"metadatos: {doc.metadata}")
    print("-----------------")