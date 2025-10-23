# 🤖 Chatbot Básico con LangChain y Streamlit

Este proyecto implementa un chatbot interactivo utilizando LangChain y Streamlit con funcionalidad de streaming en tiempo real.

## Características

- **Interfaz web intuitiva** con Streamlit
- **Streaming de respuestas** con cursor parpadeante
- **Configuración personalizable** de temperatura y modelo
- **Historial de conversación** persistente durante la sesión
- **Manejo de errores** robusto
- **Sidebar con controles** para personalizar la experiencia

## Requisitos

- Python 3.8+
- OpenAI API Key
- Dependencias listadas en requirements.txt

## Instalación

1. Clona o descarga el proyecto
2. Instala las dependencias:
   ```bash
   pip install streamlit langchain-openai python-dotenv
   ```
3. Configura tu API Key de OpenAI en un archivo `.env`:
   ```
   OPENAI_API_KEY=tu_api_key_aqui
   ```

## Uso

Ejecuta la aplicación con:
```bash
streamlit run streamlit_chatbot_work.py
```

## Funcionalidades

### Streaming de Respuestas
- Las respuestas se muestran en tiempo real con efecto de escritura
- Cursor parpadeante (▌) durante la generación
- Pausa configurable para simular velocidad de escritura

### Configuración
- **Temperatura**: Controla la creatividad de las respuestas (0.0 - 1.0)
- **Modelo**: Selección entre diferentes modelos de OpenAI
- **Nueva conversación**: Botón para limpiar el historial

### Manejo de Errores
- Captura y muestra errores de API
- Mensajes informativos para troubleshooting
- Validación de configuración de API Key

## Estructura del Código

- `streamlit_chatbot_work.py`: Aplicación principal
- Configuración de página y sidebar
- Gestión de estado de sesión
- Implementación de streaming con LangChain
- Manejo de historial de mensajes

## Modelos Soportados

- gpt-5-nano
- gpt-3.5-turbo  
- gpt-4o-mini

## Notas Técnicas

- Utiliza `st.session_state` para persistir mensajes
- Implementa cadenas LangChain con operador `|`
- Streaming mediante `cadena.stream()`
- Placeholder dinámico para efectos visuales