from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv


load_dotenv()
print(os.getenv("OPENAI_API_KEY"))

loader = PyPDFDirectoryLoader("/home/jose/Ingenieria_de_LLM/LangChain_LangGraph_y_Agentes_AI_Python/3_RAG_y_LangChain/contratos")
documentos = loader.load()
print(f"Se cargaron {len(documentos)} documentos desde el directorio")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200
)

docs_split = text_splitter.split_documents(documentos)
print(f"Se crearon {len(docs_split)} chunks de texto")

vectorstore = Chroma.from_documents(
    documents=docs_split,
    embedding=OpenAIEmbeddings(model="text-embedding-3-large"),
    persist_directory="/home/jose/Ingenieria_de_LLM/LangChain_LangGraph_y_Agentes_AI_Python/3_RAG_y_LangChain/chroma_db"
)

consulta = "¿Dónde se encuentra el contrato en el que participó María Jiménez Campos?"
resultados = vectorstore.similarity_search(consulta, k=2)

print(f"Se encontraron {len(resultados)} chunks de texto relevantes")
for i, doc in enumerate(resultados):
    print(f"Chunk {i+1}:")
    snipdoc = doc.page_content[:200] + "..."
    print(f"contenido: {snipdoc}")
    print(f"metadatos: {doc.metadata}")
    print("-----------------")