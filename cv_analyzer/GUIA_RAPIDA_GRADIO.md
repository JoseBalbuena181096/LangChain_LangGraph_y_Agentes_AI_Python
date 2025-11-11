# 🚀 Guía Rápida de Inicio - Versión Gradio

## Inicio Rápido (3 pasos)

### 1️⃣ Configurar variables de entorno
```bash
cp .env.example .env
# Edita .env y agrega tu OPENAI_API_KEY
```

### 2️⃣ Instalar Gradio (si no lo tienes)
```bash
pip install gradio
```

### 3️⃣ Ejecutar la aplicación

**Opción A: Script automatizado**
```bash
./run_gradio.sh
```

**Opción B: Comando directo**
```bash
python app_gradio.py
```

## 🌐 Acceder a la Aplicación

Abre tu navegador en: **http://localhost:7860**

## 📱 Uso de la Interfaz

### Paso 1: Subir CV
- Haz clic en el área de archivo
- Selecciona un PDF con el currículum
- ✅ Verás confirmación de archivo cargado

### Paso 2: Describir Puesto
- Escribe la descripción detallada del puesto
- Incluye:
  - Requisitos obligatorios
  - Requisitos deseables
  - Responsabilidades
  - Experiencia necesaria

### Paso 3: Analizar
- Haz clic en "🔍 Analizar Candidato"
- Espera el procesamiento (5-15 segundos)
- Revisa los resultados detallados

### Paso 4: Limpiar (Opcional)
- Haz clic en "🗑️ Limpiar"
- Resetea todos los campos
- Listo para analizar otro CV

## 🎨 Características de la UI

### Resultados Visuales
- **Porcentaje de ajuste** grande y destacado
- **Código de colores**:
  - 🟢 Verde (80%+): Excelente candidato
  - 🟡 Amarillo (60-79%): Buen candidato
  - 🟠 Naranja (40-59%): Candidato regular
  - 🔴 Rojo (<40%): Candidato no recomendado

### Información Detallada
- 👤 **Perfil**: Nombre, experiencia, educación
- 💼 **Experiencia**: Resumen de trabajos relevantes
- 🛠️ **Habilidades**: Badges con tecnologías clave
- 💪 **Fortalezas**: Lista de puntos fuertes
- 📈 **Áreas de mejora**: Oportunidades de desarrollo
- 📋 **Recomendación**: Decisión final con contexto

## ⚡ Ventajas de Gradio

### Para Desarrolladores
- ✅ Código más simple y directo
- ✅ Menos configuración necesaria
- ✅ HTML personalizable
- ✅ Temas modernos integrados

### Para Usuarios
- ✅ Interfaz moderna y limpia
- ✅ Carga más rápida
- ✅ Responsive por defecto
- ✅ Fácil de usar

### Para Deployment
- ✅ Integración nativa con Hugging Face
- ✅ Compartir públicamente con 1 línea
- ✅ Menor consumo de recursos
- ✅ URLs públicas temporales

## 🔧 Personalización

### Cambiar Puerto
```python
# En app_gradio.py, línea del launch:
demo.launch(server_port=7860)  # Cambia a tu puerto preferido
```

### Compartir Públicamente
```python
# En app_gradio.py:
demo.launch(share=True)  # Genera URL pública temporal
```

### Cambiar Tema
```python
# En gradio_ui.py:
gr.Blocks(theme=gr.themes.Monochrome())  # Otros: Soft, Glass, Base
```

## 🐛 Solución de Problemas

### Puerto ya en uso
```bash
# Mata el proceso en el puerto 7860
lsof -ti:7860 | xargs kill -9
```

### Gradio no se instala
```bash
# Actualiza pip primero
pip install --upgrade pip
pip install gradio
```

### No carga la API key
```bash
# Verifica el archivo .env
cat .env | grep OPENAI_API_KEY
# Reinicia la aplicación después de configurar
```

## 📊 Comparar con Streamlit

| Feature | Streamlit | Gradio |
|---------|-----------|---------|
| Comando | `streamlit run app.py` | `python app_gradio.py` |
| Puerto | 8501 | 7860 |
| Recargas | Auto-reload | Manual restart |
| Compartir | Streamlit Cloud | share=True |

## 💡 Tips

### Mejor Rendimiento
- Usa PDFs con texto seleccionable
- Evita archivos muy grandes (>50 MB)
- Cierra tabs no utilizados

### Mejores Descripciones
- Sé específico con requisitos
- Usa viñetas y formato claro
- Incluye nivel de experiencia requerido
- Menciona tecnologías específicas

### Resultados Óptimos
- Asegúrate de que el CV esté actualizado
- Verifica que la descripción sea relevante
- Lee toda la recomendación antes de decidir

## 🎯 Próximos Pasos

1. ✅ Prueba con varios CVs
2. ✅ Compara resultados con tu evaluación
3. ✅ Ajusta las descripciones de puestos
4. ✅ Evalúa la precisión del sistema

## 📚 Recursos

- [Documentación Gradio](https://www.gradio.app/docs)
- [Ejemplos Gradio](https://www.gradio.app/demos)
- [Hugging Face Spaces](https://huggingface.co/spaces)

---

**¿Prefieres Streamlit?** Usa `streamlit run app.py` en su lugar.

Ambas versiones ofrecen la **misma calidad de análisis**, solo difieren en la presentación. 🚀
