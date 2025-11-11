# 🎨 Comparación: Streamlit vs Gradio

## Resumen

Este proyecto ofrece **dos interfaces** diferentes para el mismo sistema de análisis de CVs:

### 📱 Streamlit (`app.py`)
- **Estilo**: Aplicación web tipo dashboard
- **Layout**: Columnas personalizadas y componentes nativos
- **Ventajas**:
  - Más opciones de personalización visual
  - Mejor para aplicaciones complejas con múltiples páginas
  - Comunidad más grande en data science
  - Componentes ricos (metrics, progress bars, etc.)

### 🎯 Gradio (`app_gradio.py`)
- **Estilo**: Interfaz moderna y minimalista
- **Layout**: Diseño basado en bloques y filas
- **Ventajas**:
  - Más rápido de desarrollar
  - Ideal para demos de machine learning
  - Integración nativa con Hugging Face Spaces
  - API más simple y directa

## 🚀 ¿Cuál usar?

| Caso de uso | Recomendación |
|-------------|---------------|
| Demo rápida | **Gradio** |
| Aplicación empresarial | **Streamlit** |
| Compartir en Hugging Face | **Gradio** |
| Dashboard complejo | **Streamlit** |
| Prototipo de ML | **Gradio** |
| Múltiples páginas | **Streamlit** |

## 💡 Características de cada versión

### Streamlit Features
- ✅ Progress bar durante el análisis
- ✅ Estado de sesión persistente
- ✅ Métricas visuales con deltas
- ✅ Configuración de tema personalizable
- ✅ Sidebar opcional

### Gradio Features
- ✅ Output HTML enriquecido
- ✅ Interfaz más limpia por defecto
- ✅ Fácil de compartir públicamente
- ✅ Temas modernos integrados
- ✅ Responsive por defecto

## 🔧 Instalación

```bash
# Solo Streamlit
pip install streamlit

# Solo Gradio
pip install gradio

# Ambas (recomendado)
pip install -r requirements.txt
```

## 🎮 Uso

```bash
# Ejecutar versión Streamlit
streamlit run app.py

# Ejecutar versión Gradio
python app_gradio.py
```

## 📊 Rendimiento

| Aspecto | Streamlit | Gradio |
|---------|-----------|---------|
| Tiempo de inicio | ~2-3 seg | ~1-2 seg |
| Memoria | ~150 MB | ~120 MB |
| Velocidad de carga | Media | Rápida |
| Actualización UI | Rerun completo | Componentes individuales |

## 🌐 Deployment

### Streamlit Cloud
```bash
# Gratuito y simple
# Conecta tu repo de GitHub
# Automáticamente detecta app.py
```

### Hugging Face Spaces
```bash
# Mejor para Gradio
# Compartir fácilmente
# GPU opcional disponible
```

### Docker
```dockerfile
# Funciona igual para ambos
# Especifica el comando de inicio
# Expone puerto 8501 (Streamlit) o 7860 (Gradio)
```

## 🎨 Personalización

### Streamlit
```python
# .streamlit/config.toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
```

### Gradio
```python
# En el código
gr.Blocks(theme=gr.themes.Soft())
# o
gr.Blocks(theme=gr.themes.Monochrome())
```

## 📝 Conclusión

**Ambas interfaces son igualmente funcionales** y ofrecen la misma calidad de análisis. La elección depende de:

- **Preferencia personal** de desarrollo
- **Requisitos** del proyecto
- **Audiencia** objetivo
- **Plataforma** de deployment

¡Prueba ambas y decide cuál prefieres! 🚀
