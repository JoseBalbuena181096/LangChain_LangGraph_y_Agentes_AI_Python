-- Script de configuración para PostgreSQL con pgvector
-- Ejecutar como superusuario de PostgreSQL

-- 1. Crear la extensión pgvector (requiere permisos de superusuario)
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Crear la base de datos para vectores (opcional, puedes usar una existente)
-- CREATE DATABASE vectordb;

-- 3. Conectarse a la base de datos vectordb y verificar la extensión
-- \c vectordb;

-- 4. Verificar que pgvector esté instalado correctamente
SELECT * FROM pg_extension WHERE extname = 'vector';

-- 5. Crear un usuario específico para la aplicación (opcional pero recomendado)
-- CREATE USER langchain_user WITH PASSWORD 'secure_password';
-- GRANT ALL PRIVILEGES ON DATABASE vectordb TO langchain_user;

-- 6. Verificar que se pueden crear vectores
-- SELECT '[1,2,3]'::vector;

-- 7. Ejemplo de tabla con vectores (LangChain la creará automáticamente)
/*
CREATE TABLE IF NOT EXISTS example_embeddings (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(1536),  -- Dimensión para text-embedding-ada-002
    metadata JSONB
);

-- Crear índice para búsquedas eficientes
CREATE INDEX ON example_embeddings USING ivfflat (embedding vector_cosine_ops);
*/

-- Comandos útiles para administración:

-- Ver todas las tablas relacionadas con LangChain
-- SELECT tablename FROM pg_tables WHERE tablename LIKE 'langchain%';

-- Ver el tamaño de las tablas
-- SELECT 
--     schemaname,
--     tablename,
--     pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
-- FROM pg_tables 
-- WHERE tablename LIKE 'langchain%';

-- Limpiar todas las tablas de LangChain (¡CUIDADO!)
-- DROP TABLE IF EXISTS langchain_pg_embedding CASCADE;
-- DROP TABLE IF EXISTS langchain_pg_collection CASCADE;