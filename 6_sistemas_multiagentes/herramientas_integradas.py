from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper


wiki = WikipediaAPIWrapper(
    api_wrapper=WikipediaAPIWrapper()
)
respones = wiki.run("¿Mexico?")
print(respones)