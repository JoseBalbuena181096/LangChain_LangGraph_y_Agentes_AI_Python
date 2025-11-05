# ⚖️ Sistema RAG – Asistente Legal (Contratos de Arrendamiento)

Asistente legal especializado en contratos de arrendamiento que usa Recuperación Aumentada por Generación (RAG). Combina técnicas de recuperación MMR con generación de múltiples consultas (MultiQuery) y un enfoque híbrido mediante Ensemble para encontrar los fragmentos más relevantes de tus contratos y responder con precisión.

## 📦 Qué incluye
- Interfaz en `Streamlit` para chat y visualización de fragmentos relevantes.
- Pipeline RAG en `LangChain` con `Chroma` como vector store.
- Recuperación híbrida: `MMR + Similarity` con `EnsembleRetriever`.
- Prompts personalizados para consulta múltiple y respuesta legal estructurada.

## 🗂️ Estructura del proyecto
```
./asistente_legal_RAG/
├── app.py               # UI en Streamlit
├── rag_system.py        # Pipeline RAG y retrievers
├── config.py            # Parámetros de modelos, búsqueda y almacenamiento
├── prompts.py           # Plantillas de prompts
└── contratos/           # PDFs con contratos de arrendamiento
```

## 🔧 Arquitectura y flujo
1. Usuario escribe una consulta en la UI (`app.py`).
2. El sistema inicializa el RAG y el retriever (`rag_system.initialize_rag_system`).
3. `MultiQueryRetriever` genera 3 variaciones de la consulta usando `llm_queries`.
4. Se consulta el vector store `Chroma` con `MMR` para diversidad y relevancia.
5. Si `ENABLE_HYBRID_SEARCH=True`, se combina `MMR` + `similarity` con `EnsembleRetriever` (pesos configurables).
6. Se formatea el contexto (`format_docs`) y se pasa al `PromptTemplate` (`RAG_TEMPLATE`).
7. `llm_generation` produce la respuesta final que se muestra en el chat.
8. En el panel derecho se enumeran los fragmentos de documentos usados: fuente, página y contenido.

## ⚙️ Configuración principal (`config.py`)
- `EMBEDDING_MODEL`: modelo de embeddings (`text-embedding-3-large`).
- `QUERY_MODEL`: LLM para generar variaciones de consulta.
- `GENERATION_MODEL`: LLM para generar respuestas finales.
- `CHROMA_DB_PATH`: directorio persistente del vector store.
- `SEARCH_TYPE`: `mmr` por defecto.
- `MMR_DIVERSITY_LAMBDA`: equilibrio relevancia/diversidad (0–1).
- `MMR_FETCH_K`: candidatos para MMR.
- `SEARCH_K`: número de documentos finales.
- `ENABLE_HYBRID_SEARCH`: activa el `EnsembleRetriever`.
- `SIMILARITY_THRESHOLD`: umbral de similitud para el ensemble.

Nota: La UI muestra nombres ilustrativos de modelos. Los modelos efectivos se definen en `config.py`.

## 🧩 Prompts (`prompts.py`)
- `RAG_TEMPLATE`: encuadre legal, cita cuando sea relevante y estructura la respuesta.
- `MULTI_QUERY_PROMPT`: guía para generar 3 variaciones útiles de la consulta.
- `RELEVANCE_PROMPT` y `ENTITY_EXTRACTION_PROMPT`: disponibles para futuras extensiones.

## ✅ Requisitos
- Python 3.10+
- OpenAI API Key válida
- Dependencias:
  - `streamlit`, `python-dotenv`
  - `langchain`, `langchain-openai`, `langchain-community`
  - `chromadb`

Instala dependencias:

```bash
pip install streamlit python-dotenv langchain langchain-openai langchain-community chromadb
```

## 🔑 Variables de entorno
Este proyecto carga variables desde `.env` (vía `dotenv`). Asegúrate de definir:

```bash
OPENAI_API_KEY="tu_api_key"
```

Puedes ubicar el `.env` en el directorio raíz donde ejecutas `streamlit run app.py`.

## 🧱 Preparar la base vectorial (Chroma)
Si es la primera vez o no existe `CHROMA_DB_PATH`, crea la base vectorial a partir de los PDFs de `contratos/` con este script de ejemplo:

```python
# ingest.py
import os
from glob import glob
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_DB_PATH = "/home/jose/Ingenieria_de_LLM/LangChain_LangGraph_y_Agentes_AI_Python/3_RAG_y_LangChain/chroma_db"
CONTRACTS_DIR = "./contratos"

# Cargar PDFs
docs = []
for pdf_path in glob(os.path.join(CONTRACTS_DIR, "*.pdf")):
    loader = PyPDFLoader(pdf_path)
    docs.extend(loader.load())

# Partir en fragmentos
splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150)
chunks = splitter.split_documents(docs)

# Crear y persistir vector store
emb = OpenAIEmbeddings(model="text-embedding-3-large")
Chroma.from_documents(chunks, embedding=emb, persist_directory=CHROMA_DB_PATH)
print(f"Persistido en: {CHROMA_DB_PATH}")
```

Ejecuta:

```bash
python ingest.py
```

## 🚀 Ejecución
Desde la carpeta `asistente_legal_RAG`:

```bash
streamlit run app.py
```

- Escribe tu consulta en el chat: ejemplo “¿Quién es el arrendatario en el contrato de vivienda 1?”
- A la derecha verás los fragmentos relevantes con fuente y página.

## 🔍 Recuperación y parámetros
- `MMR` equilibra diversidad y relevancia: ajusta `MMR_DIVERSITY_LAMBDA`.
- `SEARCH_K` define cuántos documentos finales se pasan al LLM.
- `MultiQueryRetriever` usa `QUERY_MODEL` para reformular la consulta 3 veces.
- `EnsembleRetriever` combina `MMR` y `similarity` con `weights=[0.7, 0.3]` y `SIMILARITY_THRESHOLD`.

## 🛠️ Personalización rápida
- Cambia modelos en `config.py` según tu disponibilidad.
- Desactiva el híbrido: `ENABLE_HYBRID_SEARCH = False`.
- Aumenta `SEARCH_K` para respuestas más contextualizadas.
- Eleva `MMR_FETCH_K` si tienes más documentos y quieres mayor diversidad.

## 🧪 Ejemplos de consulta
- “¿Cuál es la duración del contrato de arrendamiento de vivienda 2?”
- “Importe mensual del alquiler y forma de pago del local de negocio.”
- “Dirección de la propiedad en la plaza de garaje.”

## 🩺 Troubleshooting
- “No se encuentra `OPENAI_API_KEY`” → crea `.env` con tu clave o exporta en entorno.
- “Ruta `CHROMA_DB_PATH` no existe” → ejecuta `ingest.py` o corrige la ruta en `config.py`.
- “Respuestas vacías o poco relevantes” → incrementa `SEARCH_K` y/o ajusta `MMR_DIVERSITY_LAMBDA`.
- “Modelos no disponibles” → reemplaza por modelos compatibles en `config.py`.

## 🔒 Nota legal
Este asistente no sustituye asesoría legal profesional. Úsalo como apoyo para lectura y análisis de contratos.

## 📎 Créditos
- [LangChain](https://python.langchain.com/)
- [ChromaDB](https://www.trychroma.com/)
- OpenAI API