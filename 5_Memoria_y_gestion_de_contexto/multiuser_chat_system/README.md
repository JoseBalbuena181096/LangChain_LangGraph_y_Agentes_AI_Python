# 🧠 Sistema de Chat Multi-Usuario con Memoria Vectorial Avanzada

> **Documentación Técnica Detallada**
> Este documento proporciona una explicación profunda de la arquitectura, componentes y flujo de datos del sistema. Diseñado para desarrolladores e ingenieros de IA que deseen comprender cómo construir sistemas de memoria persistente.

---

## 📖 1. Introducción y Filosofía del Proyecto

Los LLMs (Large Language Models) tradicionales son "amnésicos" por diseño: cada nueva sesión es una pizarra en blanco. Si bien las ventanas de contexto han crecido (128k, 1M tokens), pasar todo el historial de conversaciones pasadas es ineficiente, costoso y lento.

Este proyecto resuelve el problema de la **continuidad** mediante una **Arquitectura de Memoria Híbrida**:
1.  **Memoria Episódica (Corto Plazo)**: Gestionada por `LangGraph`, mantiene el contexto inmediato de la conversación actual.
2.  **Memoria Semántica (Largo Plazo)**: Gestionada por `ChromaDB`, almacena hechos, preferencias y datos del usuario de forma permanente y consultable semánticamente.

El objetivo es crear un asistente que no solo "chatee", sino que **conozca** al usuario a lo largo del tiempo.

---

## 🏗️ 2. Arquitectura del Sistema

El sistema sigue una arquitectura modular desacoplada, donde la interfaz (Frontend) está separada de la lógica de negocio (Backend/Core), unidas por un gestor de estado.

### Diagrama de Alto Nivel

```mermaid
graph TD
    subgraph "Frontend (Streamlit)"
        UI[🖥️ Interfaz de Usuario]
        Session[📦 Session State]
    end

    subgraph "Orquestador (LangGraph)"
        Graph[🔄 Grafo de Estados]
        Nodes[📍 Nodos de Procesamiento]
    end

    subgraph "Capa de Memoria (Memory Manager)"
        Ext[🔍 Extractor de Hechos]
        Ret[🎣 Recuperador Semántico]
        VDB[(🧠 ChromaDB - Vectores)]
        MetaDB[(📄 JSON/SQLite - Metadatos)]
    end

    subgraph "Modelos (OpenAI)"
        ChatModel[🤖 GPT-4o (Chat)]
        ExtractModel[⛏️ GPT-3.5/4 (Extracción)]
        EmbedModel[🔢 Text-Embedding-3 (Vectores)]
    end

    UI <--> Session
    Session <--> Graph
    Graph <--> Nodes
    Nodes <--> ChatModel
    Nodes <--> Ext
    Nodes <--> Ret
    Ext <--> ExtractModel
    Ret <--> EmbedModel
    Ret <--> VDB
    Ext <--> VDB
```

---

## 🔬 3. Análisis Profundo de Componentes

A continuación, desglosamos cada archivo y su responsabilidad técnica.

### 3.1. `memory_manager.py`: El Hipocampo del Sistema

Este módulo es el cerebro de la memoria a largo plazo. No solo guarda texto, sino que **entiende** qué es importante guardar.

#### 🧠 Base de Datos Vectorial (ChromaDB)
Utilizamos **ChromaDB** como almacén vectorial.
*   **¿Qué es un Vector?**: Es una representación numérica (lista de floats) del *significado* de un texto. Frases como "Me gustan los perros" y "Amo a los caninos" tendrán vectores muy cercanos matemáticamente, aunque no compartan palabras.
*   **Embeddings**: Usamos `OpenAIEmbeddings` (modelo `text-embedding-3-large`) para convertir texto en estos vectores.

#### ⛏️ Sistema de Extracción Inteligente (`_init_extraction_system`)
En lugar de guardar *todo* lo que dice el usuario (lo cual llenaría la base de datos de ruido), usamos un LLM secundario para filtrar.
*   **Prompt de Extracción**: Analiza el mensaje y decide si contiene información de categorías específicas: `personal`, `profesional`, `preferencias`, `hechos_importantes`.
*   **Salida Estructurada**: Usamos `PydanticOutputParser` para obligar al LLM a responder en un formato JSON estricto (`ExtractedMemory`), garantizando que siempre tengamos una categoría y un nivel de importancia (1-5).

#### 📂 Persistencia Híbrida
*   **Vectores**: Se guardan en `users/{user_id}/chromadb`.
*   **Metadatos de Chat**: Títulos de chats, fechas de creación, etc., se guardan en `users/{user_id}/chats_meta.json` para un acceso rápido sin necesidad de inferencia vectorial.

---

### 3.2. `chatbot.py`: El Orquestador (LangGraph)

Aquí reside la lógica conversacional. Usamos **LangGraph** en lugar de cadenas lineales (LangChain Chains) porque necesitamos un flujo cíclico y con estado.

#### 🔄 El Grafo de Estados (`StateGraph`)
El grafo define una máquina de estados por donde pasa cada mensaje.
*   **Estado (`MemoryState`)**: Es un diccionario tipado que viaja por los nodos. Contiene:
    *   `messages`: Lista de mensajes (User/AI).
    *   `vector_memories`: Memorias recuperadas de ChromaDB.
    *   `last_memory_extraction`: Para evitar procesar el mismo mensaje dos veces.

#### 📍 Nodos del Grafo (Paso a Paso)

1.  **`memory_retrieval_node`**:
    *   Toma el último mensaje del usuario.
    *   Lo convierte en vector.
    *   Busca en ChromaDB los "recuerdos" más similares semánticamente.
    *   Inyecta estos recuerdos en el estado.

2.  **`context_optimization_node`**:
    *   Los LLMs tienen un límite de contexto. Si la conversación es muy larga, este nodo usa `trim_messages` para recortar los mensajes más antiguos, manteniendo siempre el mensaje del sistema y los más recientes.

3.  **`response_generation_node`**:
    *   Construye el prompt final.
    *   **Inyección de Contexto**: Toma las `vector_memories` recuperadas en el paso 1 y las inserta en el System Prompt. Así el LLM "sabe" lo que recordó.
    *   Genera la respuesta.

4.  **`memory_extraction_node`**:
    *   Este nodo corre *después* de generar la respuesta (o en paralelo conceptualmente).
    *   Llama al `memory_manager` para ver si el mensaje original del usuario tenía algo digno de guardarse a largo plazo.
    *   Esto asegura que el aprendizaje sea continuo.

---

### 3.3. `app.py`: La Interfaz (Streamlit)

Streamlit funciona recargando todo el script en cada interacción. Esto presenta un desafío para mantener el estado.

#### 📦 Gestión de Estado (`st.session_state`)
Para que el chatbot no se "reinicie" cada vez que pulsas un botón, usamos `st.session_state` intensivamente:
*   `current_user`: Quién está logueado.
*   `chatbot`: La instancia de la clase `ModernChatbot`.
*   `memory_manager`: La instancia de `ModernMemoryManager`.
*   `chat_history`: Cache local de mensajes para renderizado rápido.

#### 🎨 UI Dinámica
*   **Sidebar**: Cambia dinámicamente según si hay un usuario seleccionado. Muestra el historial de chats cargado desde el JSON de metadatos.
*   **Chat Interface**: Renderiza los mensajes con estilo diferenciado (User vs Assistant). Muestra metadatos como "Memorias usadas" o "Contexto optimizado" debajo de cada respuesta para transparencia.

---

## 🌊 4. Flujo de Datos: "Vida de un Mensaje"

Imagina que el usuario dice: *"Recuérdame comprar leche mañana"*

1.  **UI**: `app.py` captura el texto y llama a `chatbot.chat()`.
2.  **LangGraph - Inicio**: Se inicializa el estado con el mensaje.
3.  **Recuperación**:
    *   Se busca "comprar leche" en ChromaDB.
    *   Quizás encuentra una nota antigua: "Prefiero leche de almendras".
    *   Este recuerdo se añade al estado.
4.  **Optimización**: Se verifica que el historial total no exceda los tokens.
5.  **Generación**:
    *   Prompt al LLM:
        *   *System*: "Eres un asistente... Sabes esto del usuario: 'Prefiero leche de almendras'."
        *   *User*: "Recuérdame comprar leche mañana".
    *   El LLM responde: "Claro, te recordaré comprar leche de almendras mañana."
6.  **Extracción (Aprendizaje)**:
    *   El sistema analiza "Recuérdame comprar leche mañana".
    *   Clasifica como `hechos_importantes`.
    *   Guarda el vector en ChromaDB.
7.  **UI**: Muestra la respuesta y un indicador "🧠 1 memoria usada".

---

## ⚙️ 5. Configuración (`config.py`)

El archivo `config.py` centraliza las variables críticas para facilitar el mantenimiento.

| Variable | Descripción | Valor por Defecto |
| :--- | :--- | :--- |
| `DEFAULT_MODEL` | Modelo principal de chat | `gpt-5-nano` (o gpt-4o) |
| `MAX_VECTOR_RESULTS` | Cuántos recuerdos recuperar | `3` |
| `MEMORY_CATEGORIES` | Categorías de clasificación | personal, profesional, etc. |
| `USERS_DIR` | Ruta de almacenamiento | `./users` |

---

## 🚀 6. Guía de Instalación y Uso

### Requisitos Previos
*   **Python 3.9+**: Necesario para las últimas versiones de LangChain.
*   **OpenAI API Key**: Créditos activos.

### Instalación Paso a Paso

1.  **Clonar y Preparar Entorno**:
    ```bash
    git clone <repo>
    cd multiuser_chat_system
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    # venv\Scripts\activate  # Windows
    ```

2.  **Instalar Dependencias**:
    ```bash
    pip install streamlit langchain langgraph langchain-openai langchain-chroma chromadb python-dotenv pydantic
    ```

3.  **Configurar Secretos**:
    Crea un archivo `.env`:
    ```env
    OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx
    ```

4.  **Ejecutar**:
    ```bash
    streamlit run app.py
    ```

---

## 🔮 7. Extensibilidad y Futuro

Este sistema está diseñado para crecer:
*   **Cambiar Vector Store**: Cambiar ChromaDB por Pinecone o Weaviate es trivial modificando solo `_init_vector_db` en `memory_manager.py`.
*   **Modelos Locales**: Se puede reemplazar `ChatOpenAI` por `ChatOllama` para usar Llama 3 localmente, garantizando privacidad total.
*   **Herramientas (Tools)**: LangGraph permite añadir nodos de herramientas (búsqueda web, calendario) fácilmente al grafo.

---
---

## 🛠️ 8. Solución de Problemas (Troubleshooting)

### 🔴 Error: `sqlite3.OperationalError: database is locked`
*   **Causa**: LangGraph usa SQLite para checkpoints. Si intentas abrir la misma base de datos desde múltiples hilos o procesos (ej. corriendo `streamlit run` dos veces), se bloqueará.
*   **Solución**:
    1.  Detén todos los procesos de terminal (`Ctrl+C`).
    2.  Verifica que no haya procesos zombies de python.
    3.  Reinicia la app: `streamlit run app.py`.

### 🔴 Error: `RateLimitError` (OpenAI)
*   **Causa**: Has excedido tu cuota de API o los límites por minuto (RPM).
*   **Solución**:
    *   Verifica tu saldo en OpenAI Platform.
    *   En `config.py`, cambia `DEFAULT_MODEL` a uno más barato/rápido como `gpt-3.5-turbo`.
    *   Implementa un "backoff exponencial" en `utils.py` (actualmente no implementado por defecto).

### 🔴 La memoria no parece persistir
*   **Causa**: ChromaDB requiere que se llame a `persist()` o se configure correctamente el directorio.
*   **Verificación**:
    1.  Revisa la carpeta `users/{user_id}/chromadb`. Debería haber archivos `.bin` y `.sqlite`.
    2.  Si borras esta carpeta, el usuario perderá su memoria a largo plazo.

---

## 📚 9. Referencia de API (Clases Principales)

### `ModernMemoryManager` (`memory_manager.py`)

| Método | Firma | Descripción |
| :--- | :--- | :--- |
| `__init__` | `(user_id: str)` | Inicializa ChromaDB y el sistema de extracción para un usuario específico. |
| `save_vector_memory` | `(text, metadata) -> str` | Guarda un fragmento de texto como vector. Retorna el ID de la memoria. |
| `search_vector_memory` | `(query, k=3) -> list` | Busca los `k` recuerdos más similares semánticamente a `query`. |
| `extract_and_store_memories` | `(user_message) -> bool` | **Core Logic**. Usa un LLM para analizar si el mensaje merece ser guardado. |
| `create_new_chat` | `(first_message) -> str` | Crea una nueva sesión y genera un título automático usando LLM. |

### `ModernChatbot` (`chatbot.py`)

| Método | Firma | Descripción |
| :--- | :--- | :--- |
| `chat` | `(message, chat_id) -> dict` | Punto de entrada principal. Ejecuta el grafo de LangGraph. Retorna respuesta y metadatos. |
| `get_conversation_history` | `(chat_id, limit) -> list` | Recupera el historial formateado desde el estado de LangGraph. |
| `_create_app` | `() -> CompiledGraph` | Construye y compila el grafo de estados (Nodos + Aristas). |

---

## 🔍 10. Inspección de Base de Datos

Para depurar o auditar qué está guardando el sistema, puedes usar este script de utilidad (crear como `inspect_db.py`):

```python
import chromadb
from config import USERS_DIR
import os

def inspect_user_memory(user_id):
    path = os.path.join(USERS_DIR, user_id, "chromadb")
    client = chromadb.PersistentClient(path=path)
    collection = client.get_collection(f"memoria_{user_id}")
    
    print(f"--- Memorias de {user_id} ---")
    data = collection.get()
    for i, doc in enumerate(data['documents']):
        meta = data['metadatas'][i]
        print(f"[{meta['category'].upper()}] (Imp: {meta['importance']})")
        print(f"Contenido: {doc}")
        print("-" * 20)

# Uso
inspect_user_memory("usuario_ejemplo")
```

---
*Documentación generada automáticamente por Antigravity Agent.*
