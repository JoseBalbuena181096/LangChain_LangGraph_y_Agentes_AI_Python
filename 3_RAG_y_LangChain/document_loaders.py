from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("/home/jose/Ingenieria_de_LLM/LangChain_LangGraph_y_Agentes_AI_Python/3_RAG_y_LangChain/Profile.pdf")
pages = loader.load()

for i, page in enumerate(pages):
    print("=== Página ", i+1, " ===")
    print(f"Contenido de la página {i+1}:")
    print(page.page_content)
    print("Metadata:", page.metadata)

