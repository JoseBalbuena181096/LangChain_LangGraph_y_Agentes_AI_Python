# Vector Store con PostgreSQL y pgvector

Este directorio contiene un ejemplo completo de cómo usar PostgreSQL con la extensión pgvector como vector store para aplicaciones RAG (Retrieval-Augmented Generation) con LangChain.

## 📁 Archivos incluidos

- `vector_stores_postgresql.py` - Ejemplo principal documentado
- `.env.postgresql.example` - Plantilla de variables de entorno
- `setup_postgresql.sql` - Script de configuración de la base de datos
- `README_PostgreSQL.md` - Esta documentación

## 🚀 Configuración inicial

### 1. Instalar PostgreSQL y pgvector

#### Ubuntu/Debian:
```bash
# Instalar PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Instalar pgvector
sudo apt install postgresql-14-pgvector
```

#### macOS (con Homebrew):
```bash
brew install postgresql
brew install pgvector
```

#### Docker (alternativa rápida):
```bash
docker run --name postgres-vector \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=vectordb \
  -p 5432:5432 \
  -d pgvector/pgvector:pg16
```

### 2. Configurar la base de datos

```bash
# Conectarse a PostgreSQL como superusuario
sudo -u postgres psql

# Ejecutar el script de configuración
\i setup_postgresql.sql

# O manualmente:
CREATE EXTENSION IF NOT EXISTS vector;
CREATE DATABASE vectordb;
```

### 3. Instalar dependencias de Python

```bash
pip install langchain-postgres psycopg2-binary langchain-openai langchain-community python-dotenv
```

### 4. Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
cp .env.postgresql.example .env

# Editar con tus valores reales
nano .env
```

## 🔧 Uso del ejemplo

### Ejecutar el script principal

```bash
python vector_stores_postgresql.py
```

### Estructura del código

El ejemplo incluye:

1. **Carga de documentos PDF** desde un directorio
2. **División en chunks** con solapamiento
3. **Generación de embeddings** con OpenAI
4. **Almacenamiento en PostgreSQL** con pgvector
5. **Búsqueda por similitud** con puntuaciones
6. **Manejo de errores** y validaciones

## 🔍 Comparación: PostgreSQL vs Chroma

| Característica | PostgreSQL + pgvector | Chroma |
|---|---|---|
| **Escalabilidad** | ✅ Empresarial | ⚠️ Limitada |
| **ACID Compliance** | ✅ Completo | ❌ No |
| **Consultas complejas** | ✅ SQL completo | ⚠️ Limitado |
| **Integración** | ✅ Sistemas existentes | ⚠️ Standalone |
| **Configuración** | ⚠️ Más compleja | ✅ Simple |
| **Performance** | ✅ Optimizable | ✅ Optimizado |
| **Backup/Recovery** | ✅ Robusto | ⚠️ Básico |

## 📊 Comandos SQL útiles

### Ver información del vector store

```sql
-- Listar colecciones
SELECT * FROM langchain_pg_collection;

-- Contar documentos por colección
SELECT 
    c.name as collection_name,
    COUNT(e.id) as document_count
FROM langchain_pg_collection c
LEFT JOIN langchain_pg_embedding e ON c.uuid = e.collection_id
GROUP BY c.name;

-- Ver metadatos de documentos
SELECT 
    cmetadata,
    LEFT(document, 100) as preview
FROM langchain_pg_embedding 
LIMIT 5;
```

### Optimización de rendimiento

```sql
-- Crear índices para búsquedas más rápidas
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_embedding_ivfflat 
ON langchain_pg_embedding 
USING ivfflat (embedding vector_cosine_ops) 
WITH (lists = 100);

-- Para datasets grandes, usar HNSW
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_embedding_hnsw 
ON langchain_pg_embedding 
USING hnsw (embedding vector_cosine_ops);
```

### Limpieza de datos

```sql
-- Eliminar una colección específica
DELETE FROM langchain_pg_embedding 
WHERE collection_id = (
    SELECT uuid FROM langchain_pg_collection 
    WHERE name = 'nombre_coleccion'
);

DELETE FROM langchain_pg_collection 
WHERE name = 'nombre_coleccion';
```

## 🛠️ Solución de problemas

### Error: "extension vector does not exist"
```bash
# Instalar pgvector
sudo apt install postgresql-14-pgvector
# Reiniciar PostgreSQL
sudo systemctl restart postgresql
```

### Error de conexión
```python
# Verificar que PostgreSQL esté ejecutándose
sudo systemctl status postgresql

# Verificar configuración de conexión
psql -h localhost -U postgres -d vectordb
```

### Error de permisos
```sql
-- Otorgar permisos al usuario
GRANT ALL PRIVILEGES ON DATABASE vectordb TO tu_usuario;
GRANT ALL ON SCHEMA public TO tu_usuario;
```

## 📈 Optimización para producción

### 1. Configuración de PostgreSQL

```sql
-- En postgresql.conf
shared_preload_libraries = 'vector'
max_connections = 100
shared_buffers = 256MB
effective_cache_size = 1GB
```

### 2. Índices apropiados

```sql
-- Para datasets pequeños (<1M vectores)
CREATE INDEX ON embeddings USING ivfflat (embedding vector_cosine_ops);

-- Para datasets grandes (>1M vectores)
CREATE INDEX ON embeddings USING hnsw (embedding vector_cosine_ops);
```

### 3. Monitoreo

```sql
-- Ver estadísticas de uso de índices
SELECT * FROM pg_stat_user_indexes 
WHERE relname LIKE 'langchain%';

-- Ver consultas lentas
SELECT query, mean_exec_time, calls 
FROM pg_stat_statements 
WHERE query LIKE '%vector%' 
ORDER BY mean_exec_time DESC;
```

## 🔗 Referencias

- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [LangChain PostgreSQL Integration](https://python.langchain.com/docs/integrations/vectorstores/pgvector)
- [PostgreSQL Performance Tuning](https://wiki.postgresql.org/wiki/Performance_Optimization)

## 📝 Notas adicionales

- **Dimensiones de embeddings**: text-embedding-3-large usa 3072 dimensiones
- **Límites de pgvector**: Máximo 16,000 dimensiones por vector
- **Backup**: Incluir tanto datos como esquemas en los backups
- **Escalabilidad**: Considerar particionado para datasets muy grandes