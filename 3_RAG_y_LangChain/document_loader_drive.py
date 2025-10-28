#  pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
from langchain_community.document_loaders import GoogleDriveLoader

credentials_path = "/home/jose/Ingenieria_de_LLM/LangChain_LangGraph_y_Agentes_AI_Python/3_RAG_y_LangChain/credential.json"
token_path = "/home/jose/Ingenieria_de_LLM/LangChain_LangGraph_y_Agentes_AI_Python/3_RAG_y_LangChain/token.json"

loader = GoogleDriveLoader(
    folder_id = "1VavObe5RjKI9I4oCPHIbAVKSKZ1-K4qK",
    credentials_path = credentials_path,
    token_path = token_path,
    recursive = True
)


documents = loader.load()
print(f'Metadatos: {documents[0].metadata}')
print(f'Contenido: {documents[0].page_content}')
