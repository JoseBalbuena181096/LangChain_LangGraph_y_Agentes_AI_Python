# 📄 Analizador de CVs con LangChain

Una aplicación web que utiliza LangChain y OpenAI para analizar currículums vitae y evaluar su ajuste a descripciones de puestos de trabajo. Disponible con dos interfaces: **Streamlit** y **Gradio**.

## 🚀 Características

- **Extracción de texto PDF con LangChain**: Procesa archivos PDF usando PyPDFLoader
- **Análisis con IA**: Utiliza modelos de OpenAI para evaluar candidatos
- **Interfaz intuitiva**: Disponible en Streamlit o Gradio
- **Feedback en tiempo real**: Mensajes de progreso durante todo el análisis
- **Validaciones robustas**: Detecta PDFs corruptos, vacíos o ilegibles
- **Evaluación estructurada**: Proporciona análisis detallado con porcentajes de ajuste
- **Compartir públicamente**: Gradio permite generar enlaces públicos temporales
- **Dos versiones de UI**: Elige entre Streamlit (clásica) o Gradio (moderna)

## 📋 Requisitos

- Python 3.11+
- Conda (recomendado para gestión de entornos)
- Clave API de OpenAI

## ⚙️ Configuración

### 1. Clonar y navegar al proyecto
```bash
cd cv_analyzer
```

### 2. Activar el entorno conda
```bash
conda activate llms
```

### 3. Configurar variables de entorno
```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env y agregar tu clave de OpenAI
OPENAI_API_KEY=tu_clave_openai_aqui
```

### 4. Ejecutar la aplicación

**Opción A: Con Streamlit (Interfaz clásica)**
```bash
streamlit run app.py
```

**Opción B: Con Gradio (Interfaz moderna - Solo local)**
```bash
python app_gradio.py
# o
conda run -n llms python app_gradio.py
```

**Opción C: Con Gradio (Compartir públicamente)**
```bash
python app_gradio.py --share
# Genera un enlace público temporal (válido 72 horas)
```

**Nota**: Asegúrate de tener instalado Gradio y langchain-community:
```bash
conda run -n llms pip install gradio langchain-community pypdf
```

## 🔧 Uso

1. **Subir CV**: Arrastra y suelta un archivo PDF con el currículum
2. **Describir puesto**: Escribe una descripción detallada del trabajo
3. **Analizar**: Haz clic en "Analizar Candidato"
4. **Revisar resultados**: Obtén un análisis completo con:
   - Porcentaje de ajuste al puesto
   - Habilidades técnicas identificadas
   - Fortalezas y áreas de mejora
   - Experiencia relevante

## 📁 Estructura del proyecto

```
cv_analyzer/
├── .streamlit/
│   └── config.toml          # Configuración de Streamlit
├── models/
│   └── cv_model.py          # Modelos de datos Pydantic
├── prompts/
│   └── cv_prompts.py        # Plantillas de prompts
├── services/
│   ├── cv_evaluator.py      # Lógica de evaluación con LangChain
│   └── pdf_processor.py     # Procesamiento de archivos PDF
├── ui/
│   ├── streamlit_ui.py      # Interfaz Streamlit
│   └── gradio_ui.py         # Interfaz Gradio (NUEVA)
├── app.py                   # Punto de entrada Streamlit
├── app_gradio.py            # Punto de entrada Gradio (NUEVO)
├── .env.example             # Plantilla de variables de entorno
└── README.md               # Este archivo
```

## 🛠️ Solución de problemas

### Error: "OPENAI_API_KEY no está configurada"
- Asegúrate de haber creado el archivo `.env`
- Verifica que tu clave de OpenAI sea válida
- Reinicia la aplicación después de configurar las variables

### Error: "AxiosError 400" al subir PDF
- Verifica que el archivo sea un PDF válido
- Asegúrate de que el archivo no exceda 200MB
- Intenta con un PDF que contenga texto seleccionable

### PDF no se procesa correctamente
- Los PDFs escaneados (solo imágenes) no son compatibles
- Usa PDFs con texto seleccionable para mejores resultados

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.