from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://www.atlixco.tecnm.mx/inicio")
pages = loader.load()
print(pages)
