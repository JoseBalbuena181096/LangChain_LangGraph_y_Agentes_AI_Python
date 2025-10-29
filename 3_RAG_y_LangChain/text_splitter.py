# No ejecutar para no gastar tokens
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
load_dotenv()
import os

print(os.getenv("OPENAI_API_KEY"))

# 1. cargar el pdf
loader = PyPDFLoader("/home/jose/Ingenieria_de_LLM/LangChain_LangGraph_y_Agentes_AI_Python/3_RAG_y_LangChain/quijote.pdf")
pages = loader.load()

# Dividir el texto en chunks mas paqueños
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=3000, # El tamaño de cada chunk en caracteres, el fragmento de aproximadamente 3000 caracteres
    chunk_overlap=200 # El número de caracteres que se superponen entre dos fragmentos consecutivos, existe un solapamiento de 200 caracteres 
)

chunks = text_splitter.split_documents(pages)


# 3. pasar el texto a llm
llm = ChatOpenAI(model = "gpt-5-nano", temperature = 0.7)
sumaries = []
for chunk in chunks:
    response = llm.invoke(f"Haz un resumen de los puntos mas importantes del siguiente texto:  { chunk.page_content}")
    sumaries.append(response.content)

print(sumaries)

final_summary = llm.invoke(f"Combina y sintetiza estos resumenes en un resumen coherente y completo: {' '.join(sumaries)}")
print(final_summary.content)