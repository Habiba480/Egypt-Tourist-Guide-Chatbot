from langchain.tools import Tool
from langchain.utilities import SerpAPIWrapper
from src.config import SERPAPI_API_KEY

def serpapi_tool():
    search = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY)
    return Tool(
        name="Search",
        func=search.run,
        description="Useful for real-time information about Egypt if not found in the PDF"
    )
