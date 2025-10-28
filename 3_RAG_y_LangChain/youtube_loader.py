from langchain_community.document_loaders import YoutubeLoader
import re
from urllib.parse import urlparse, parse_qs

def extract_video_id(url):
    """Extrae el ID del video de YouTube de diferentes formatos de URL"""
    parsed_url = urlparse(url)
    
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    elif parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query)['v'][0]
        elif parsed_url.path[:7] == '/embed/':
            return parsed_url.path.split('/')[2]
        elif parsed_url.path[:3] == '/v/':
            return parsed_url.path.split('/')[2]
    return None

def load_youtube_video(video_url):
    """Carga un video de YouTube con múltiples métodos de respaldo"""
    
    # Método 1: Usar YoutubeLoader directamente
    try:
        print("Intentando cargar con YoutubeLoader...")
        loader = YoutubeLoader.from_youtube_url(
            video_url,
            add_video_info=True,
            language=['es', 'en'],
            translation='es'
        )
        docs = loader.load()
        return docs
    except Exception as e:
        print(f"Error con YoutubeLoader: {e}")
    
    # Método 2: Intentar con diferentes configuraciones
    try:
        print("Intentando con configuración alternativa...")
        loader = YoutubeLoader.from_youtube_url(
            video_url,
            add_video_info=False,
            language=['es']
        )
        docs = loader.load()
        return docs
    except Exception as e:
        print(f"Error con configuración alternativa: {e}")
    
    # Método 3: Usar solo el ID del video
    try:
        video_id = extract_video_id(video_url)
        if video_id:
            print(f"Intentando con ID del video: {video_id}")
            clean_url = f"https://www.youtube.com/watch?v={video_id}"
            loader = YoutubeLoader.from_youtube_url(clean_url)
            docs = loader.load()
            return docs
    except Exception as e:
        print(f"Error con ID limpio: {e}")
    
    return None

# Cargar transcripción de un video educativo
video_url = "https://www.youtube.com/watch?v=mITI8vPQD_g"
# Cargar transcripción de un video educativo
video_url = "https://www.youtube.com/watch?v=mITI8vPQD_g"

print(f"Cargando video: {video_url}")
docs = load_youtube_video(video_url)

if docs:
    video_info = docs[0].metadata if docs[0].metadata else {}
    transcript = docs[0].page_content
    
    print("\n=== INFORMACIÓN DEL VIDEO ===")
    print(f"Título: {video_info.get('title', 'N/A')}")
    print(f"Autor: {video_info.get('author', 'N/A')}")
    print(f"Duración: {video_info.get('length', 'N/A')} segundos")
    print(f"Fecha de publicación: {video_info.get('publish_date', 'N/A')}")
    print(f"Vistas: {video_info.get('view_count', 'N/A')}")
    
    print(f"\n=== ANÁLISIS DE TRANSCRIPCIÓN ===")
    print(f"Longitud de transcripción: {len(transcript):,} caracteres")
    print(f"Palabras aproximadas: {len(transcript.split()):,}")
    
    # Extraer temas principales (palabras frecuentes)
    words = re.findall(r'\b[a-záéíóúñ]{4,}\b', transcript.lower())
    from collections import Counter
    common_words = Counter(words).most_common(10)
    
    print("\nPalabras más frecuentes:")
    for word, count in common_words:
        print(f"  {word}: {count} veces")
        
    print(f"\nPrimeros 500 caracteres:")
    print(transcript)
else:
    print("\n❌ No se pudo cargar el video con ningún método.")
    print("Posibles soluciones:")
    print("1. Verificar que el video sea público")
    print("2. Verificar que tenga subtítulos/transcripción disponible")
    print("3. Intentar con otro video de YouTube")
    print("4. Verificar la conexión a internet")
    print("5. Actualizar las dependencias: pip install --upgrade langchain-community yt-dlp")