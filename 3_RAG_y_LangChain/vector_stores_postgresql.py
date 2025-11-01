"""
Vector Store con PostgreSQL y pgvector - Ejemplo Documentado
===========================================================

Este ejemplo muestra cómo usar PostgreSQL con la extensión pgvector 
como vector store en lugar de Chroma para aplicaciones RAG con LangChain.

Requisitos previos:
------------------
1. PostgreSQL instalado con la extensión pgvector
2. Base de datos creada con pgvector habilitado
3. Variables de entorno configuradas para la conexión a PostgreSQL

Instalación de dependencias:
---------------------------
pip install langchain-postgres psycopg2-binary langchain-openai langchain-community

Configuración de PostgreSQL:
----------------------------
-- Conectarse a PostgreSQL y ejecutar:
CREATE EXTENSION IF NOT EXISTS vector;
CREATE DATABASE vectordb;
"""

from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Verificar que las variables de entorno estén configuradas
print("Verificando configuración...")
print(f"OpenAI API Key configurada: {'✓' if os.getenv('OPENAI_API_KEY') else '✗'}")
print(f"PostgreSQL Host: {os.getenv('POSTGRES_HOST', 'localhost')}")
print(f"PostgreSQL Database: {os.getenv('POSTGRES_DB', 'vectordb')}")

# Configuración de la conexión a PostgreSQL
# Estas variables deben estar en tu archivo .env:
# POSTGRES_HOST=localhost
# POSTGRES_PORT=5432
# POSTGRES_DB=vectordb
# POSTGRES_USER=tu_usuario
# POSTGRES_PASSWORD=tu_password
# OPENAI_API_KEY=tu_openai_api_key

CONNECTION_STRING = (
    f"postgresql://{os.getenv('POSTGRES_USER', 'postgres')}:"
    f"{os.getenv('POSTGRES_PASSWORD', 'password')}@"
    f"{os.getenv('POSTGRES_HOST', 'localhost')}:"
    f"{os.getenv('POSTGRES_PORT', '5432')}/"
    f"{os.getenv('POSTGRES_DB', 'vectordb')}"
)

# Nombre de la colección/tabla en PostgreSQL
COLLECTION_NAME = "contratos_embeddings"

print(f"\nConexión PostgreSQL: {CONNECTION_STRING.replace(os.getenv('POSTGRES_PASSWORD', 'password'), '***')}")

# 1. Cargar documentos PDF desde el directorio
print("\n1. Cargando documentos PDF...")
loader = PyPDFDirectoryLoader(
    "/home/jose/Ingenieria_de_LLM/LangChain_LangGraph_y_Agentes_AI_Python/3_RAG_y_LangChain/contratos"
)
documentos = loader.load()
print(f"✓ Se cargaron {len(documentos)} documentos desde el directorio")

# 2. Dividir documentos en chunks
print("\n2. Dividiendo documentos en chunks...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Tamaño de cada chunk en caracteres
    chunk_overlap=200     # Solapamiento entre chunks para mantener contexto
)

docs_split = text_splitter.split_documents(documentos)
print(f"✓ Se crearon {len(docs_split)} chunks de texto")

# 3. Configurar embeddings de OpenAI
print("\n3. Configurando modelo de embeddings...")
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",  # Modelo más reciente y potente
    # model="text-embedding-ada-002",  # Alternativa más económica
)
print("✓ Modelo de embeddings configurado: text-embedding-3-large")

# 4. Crear vector store con PostgreSQL
print("\n4. Creando vector store con PostgreSQL...")
try:
    # Crear el vector store conectándose a PostgreSQL
    vectorstore = PGVector.from_documents(
        documents=docs_split,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        connection_string=CONNECTION_STRING,
        # Configuraciones adicionales opcionales:
        # pre_delete_collection=True,  # Eliminar colección existente
        # use_jsonb=True,              # Usar JSONB para metadatos
    )
    print(f"✓ Vector store creado exitosamente en PostgreSQL")
    print(f"✓ Colección: {COLLECTION_NAME}")
    
except Exception as e:
    print(f"✗ Error al crear vector store: {e}")
    print("\nVerifica que:")
    print("- PostgreSQL esté ejecutándose")
    print("- La extensión pgvector esté instalada")
    print("- Las credenciales de conexión sean correctas")
    print("- La base de datos exista")
    exit(1)

# 5. Realizar búsqueda de similitud
print("\n5. Realizando búsqueda de similitud...")
consulta = "¿Dónde se encuentra el contrato en el que participó María Jiménez Campos?"
print(f"Consulta: {consulta}")

try:
    # Búsqueda por similitud (devuelve los k documentos más similares)
    resultados = vectorstore.similarity_search(
        query=consulta,
        k=2  # Número de resultados a devolver
    )
    
    print(f"\n✓ Se encontraron {len(resultados)} chunks de texto relevantes")
    
    # Mostrar resultados
    for i, doc in enumerate(resultados):
        print(f"\n--- Chunk {i+1} ---")
        # Mostrar solo los primeros 200 caracteres del contenido
        contenido_resumido = doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
        print(f"Contenido: {contenido_resumido}")
        print(f"Metadatos: {doc.metadata}")
        print("-" * 50)
    
    # 6. Búsqueda con puntuación de similitud
    print("\n6. Búsqueda con puntuaciones de similitud...")
    resultados_con_score = vectorstore.similarity_search_with_score(
        query=consulta,
        k=2
    )
    
    for i, (doc, score) in enumerate(resultados_con_score):
        print(f"\nChunk {i+1} - Puntuación: {score:.4f}")
        contenido_resumido = doc.page_content[:150] + "..." if len(doc.page_content) > 150 else doc.page_content
        print(f"Contenido: {contenido_resumido}")
    
except Exception as e:
    print(f"✗ Error en la búsqueda: {e}")

# 7. Información adicional sobre el vector store
print(f"\n7. Información del vector store:")
print(f"- Base de datos: PostgreSQL con pgvector")
print(f"- Colección: {COLLECTION_NAME}")
print(f"- Modelo de embeddings: text-embedding-3-large")
print(f"- Dimensiones del vector: 3072 (para text-embedding-3-large)")
print(f"- Total de documentos indexados: {len(docs_split)}")

"""
Ventajas de PostgreSQL vs Chroma:
================================

PostgreSQL con pgvector:
+ Escalabilidad empresarial
+ ACID compliance
+ Integración con sistemas existentes
+ Consultas SQL complejas
+ Backup y recovery robustos
+ Múltiples índices (IVFFlat, HNSW)
+ Soporte para metadatos complejos

Chroma:
+ Más simple de configurar
+ Optimizado específicamente para embeddings
+ Menor overhead para casos simples
+ Mejor para prototipado rápido

Comandos SQL útiles para PostgreSQL:
===================================

-- Ver las tablas creadas
SELECT tablename FROM pg_tables WHERE schemaname = 'public';

-- Ver información de la colección
SELECT COUNT(*) FROM langchain_pg_embedding WHERE collection_id = (
    SELECT uuid FROM langchain_pg_collection WHERE name = 'contratos_embeddings'
);

-- Ver metadatos de los documentos
SELECT cmetadata FROM langchain_pg_embedding LIMIT 5;

-- Eliminar una colección
DELETE FROM langchain_pg_embedding WHERE collection_id = (
    SELECT uuid FROM langchain_pg_collection WHERE name = 'contratos_embeddings'
);
DELETE FROM langchain_pg_collection WHERE name = 'contratos_embeddings';
"""