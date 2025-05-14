"""Web search tool implementation using DuckDuckGo."""

from typing import Any, Dict, List, Optional

from langchain.tools import BaseTool
from langchain.utilities import DuckDuckGoSearchAPIWrapper


class WebSearchTool(BaseTool):
    """Tool for searching the web using DuckDuckGo."""
    
    name = "web_search"
    description = """Use this tool to search the web for information.
    Input should be a search query string.
    The tool will return a list of relevant search results."""
    
    def __init__(self):
        """Initialize the web search tool."""
        super().__init__()
        self.search = DuckDuckGoSearchAPIWrapper()
    
    def _run(self, query: str) -> str:
        """Run the web search.
        
        Args:
            query: The search query
            
        Returns:
            The search results as a formatted string
        """
        try:
            results = self.search.results(query, num_results=5)
            
            # Format the results
            formatted_results = []
            for result in results:
                formatted_results.append(
                    f"Title: {result['title']}\n"
                    f"Link: {result['link']}\n"
                    f"Snippet: {result['snippet']}\n"
                )
            
            return "\n\n".join(formatted_results)
            
        except Exception as e:
            return f"Error performing web search: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Run the web search asynchronously.
        
        Args:
            query: The search query
            
        Returns:
            The search results as a formatted string
        """
        return self._run(query) 