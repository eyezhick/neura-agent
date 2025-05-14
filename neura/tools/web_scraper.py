"""Web scraping tool implementation using Playwright."""

import asyncio
from typing import Any, Dict, List, Optional, Union

from bs4 import BeautifulSoup
from langchain.tools import BaseTool
from playwright.async_api import async_playwright
from pydantic import BaseModel, Field


class ScrapingConfig(BaseModel):
    """Configuration for web scraping."""
    
    wait_for_selector: Optional[str] = Field(default=None)
    wait_for_timeout: int = Field(default=5000)
    javascript_enabled: bool = Field(default=True)
    viewport_size: Dict[str, int] = Field(
        default_factory=lambda: {"width": 1280, "height": 800}
    )
    user_agent: str = Field(
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )


class WebScraperTool(BaseTool):
    """Tool for scraping web content using Playwright."""
    
    name = "web_scraper"
    description = """Use this tool to scrape content from web pages.
    Input should be a URL and optional CSS selectors to extract specific content.
    The tool will return the scraped content in a structured format."""
    
    def __init__(
        self,
        config: Optional[ScrapingConfig] = None,
        playwright_context: Optional[Any] = None
    ):
        """Initialize the web scraper tool.
        
        Args:
            config: Scraping configuration
            playwright_context: Optional Playwright context
        """
        super().__init__()
        self.config = config or ScrapingConfig()
        self._playwright_context = playwright_context
        self._browser = None
        self._context = None
    
    async def _setup(self) -> None:
        """Set up Playwright browser and context."""
        if not self._browser:
            playwright = await async_playwright().start()
            self._browser = await playwright.chromium.launch(
                headless=True
            )
            self._context = await self._browser.new_context(
                viewport=self.config.viewport_size,
                user_agent=self.config.user_agent,
                javascript_enabled=self.config.javascript_enabled
            )
    
    async def _cleanup(self) -> None:
        """Clean up Playwright resources."""
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()
    
    def _parse_content(
        self,
        html: str,
        selectors: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Parse HTML content using BeautifulSoup.
        
        Args:
            html: The HTML content to parse
            selectors: Optional list of CSS selectors
            
        Returns:
            Dictionary containing parsed content
        """
        soup = BeautifulSoup(html, "html.parser")
        
        # Extract basic metadata
        result = {
            "title": soup.title.string if soup.title else None,
            "meta_description": soup.find("meta", {"name": "description"})["content"]
            if soup.find("meta", {"name": "description"}) else None,
            "headings": [
                {
                    "level": int(h.name[1]),
                    "text": h.get_text(strip=True)
                }
                for h in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
            ],
            "links": [
                {
                    "text": a.get_text(strip=True),
                    "href": a.get("href")
                }
                for a in soup.find_all("a", href=True)
            ]
        }
        
        # Extract content based on selectors
        if selectors:
            result["selected_content"] = {}
            for selector in selectors:
                elements = soup.select(selector)
                result["selected_content"][selector] = [
                    {
                        "text": el.get_text(strip=True),
                        "html": str(el)
                    }
                    for el in elements
                ]
        
        return result
    
    async def _scrape_page(
        self,
        url: str,
        selectors: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Scrape a web page.
        
        Args:
            url: The URL to scrape
            selectors: Optional list of CSS selectors
            
        Returns:
            Dictionary containing scraped content
        """
        await self._setup()
        
        try:
            page = await self._context.new_page()
            await page.goto(url)
            
            # Wait for content to load
            if self.config.wait_for_selector:
                await page.wait_for_selector(
                    self.config.wait_for_selector,
                    timeout=self.config.wait_for_timeout
                )
            else:
                await page.wait_for_load_state("networkidle")
            
            # Get page content
            content = await page.content()
            
            # Parse content
            result = self._parse_content(content, selectors)
            
            # Add metadata
            result["metadata"] = {
                "url": url,
                "timestamp": page.evaluate("() => new Date().toISOString()"),
                "viewport": self.config.viewport_size
            }
            
            return result
            
        finally:
            await self._cleanup()
    
    def _run(
        self,
        url: str,
        selectors: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Run the web scraper.
        
        Args:
            url: The URL to scrape
            selectors: Optional list of CSS selectors
            
        Returns:
            Dictionary containing scraped content
        """
        return asyncio.run(self._scrape_page(url, selectors))
    
    async def _arun(
        self,
        url: str,
        selectors: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Run the web scraper asynchronously.
        
        Args:
            url: The URL to scrape
            selectors: Optional list of CSS selectors
            
        Returns:
            Dictionary containing scraped content
        """
        return await self._scrape_page(url, selectors) 