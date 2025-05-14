"""Advanced research assistant example using NEURA's capabilities."""

import asyncio
import json
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from neura.agents.executor import ExecutorAgent
from neura.agents.planner import PlannerAgent
from neura.core.graph import create_agent_graph_with_tools
from neura.memory.vector import VectorMemory, VectorMemoryConfig
from neura.tools.web_scraper import ScrapingConfig, WebScraperTool
from neura.tools.web_search import WebSearchTool


class ResearchAssistant:
    """Advanced research assistant using NEURA."""
    
    def __init__(
        self,
        model_name: str = "gpt-4-turbo-preview",
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ):
        """Initialize the research assistant.
        
        Args:
            model_name: The name of the LLM to use
            temperature: The temperature for generation
            max_tokens: Maximum tokens to generate
        """
        # Initialize console for rich output
        self.console = Console()
        
        # Create agents
        self.planner = PlannerAgent(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )
        self.executor = ExecutorAgent(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # Initialize memory
        self.memory = VectorMemory(
            config=VectorMemoryConfig(
                collection_name="research_memory",
                persist_directory="./data/research_memory"
            )
        )
        
        # Create tools
        self.tools = [
            WebSearchTool(),
            WebScraperTool(
                config=ScrapingConfig(
                    wait_for_timeout=10000,
                    javascript_enabled=True
                )
            )
        ]
        
        # Create agent graph
        self.graph = create_agent_graph_with_tools(
            self.planner,
            self.executor,
            self.tools
        )
    
    def _format_result(self, result: Dict[str, Any]) -> str:
        """Format the research result.
        
        Args:
            result: The research result
            
        Returns:
            Formatted result string
        """
        messages = result["messages"]
        execution_results = result["context"].get("execution_results", {})
        
        # Format the output
        output = []
        
        # Add plan
        if "plan" in result["context"]:
            plan = json.loads(result["context"]["plan"])
            output.append("\n[bold blue]Research Plan:[/bold blue]")
            for step in plan["steps"]:
                output.append(f"\n• {step['description']}")
        
        # Add execution results
        if execution_results:
            output.append("\n[bold green]Research Findings:[/bold green]")
            for step_id, step_result in execution_results.items():
                output.append(f"\n{step_result}")
        
        # Add memory stats
        memory_stats = self.memory.get_stats()
        output.append(f"\n[bold yellow]Memory Stats:[/bold yellow]")
        output.append(f"• Total memories: {memory_stats['count']}")
        output.append(f"• Vector dimensions: {memory_stats['dimensions']}")
        
        return "\n".join(output)
    
    async def research(
        self,
        topic: str,
        max_steps: int = 5,
        save_to_memory: bool = True
    ) -> Dict[str, Any]:
        """Conduct research on a topic.
        
        Args:
            topic: The research topic
            max_steps: Maximum number of research steps
            save_to_memory: Whether to save results to memory
            
        Returns:
            Research results
        """
        # Initial state
        initial_state = {
            "messages": [{
                "role": "user",
                "content": f"Research the following topic and provide a comprehensive analysis: {topic}"
            }],
            "memory": {},
            "context": {
                "max_steps": max_steps,
                "save_to_memory": save_to_memory
            },
            "current_agent": "planner"
        }
        
        # Run the research
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task(
                "Conducting research...",
                total=None
            )
            
            result = await self.graph.ainvoke(initial_state)
            
            progress.update(task, completed=True)
        
        # Save to memory if requested
        if save_to_memory:
            self.memory.add_memory(
                content=json.dumps(result, indent=2),
                metadata={
                    "topic": topic,
                    "timestamp": result["context"].get("timestamp"),
                    "steps": len(result["context"].get("execution_results", {}))
                }
            )
        
        return result
    
    def display_result(self, result: Dict[str, Any]) -> None:
        """Display the research result.
        
        Args:
            result: The research result
        """
        formatted_result = self._format_result(result)
        
        self.console.print(
            Panel(
                formatted_result,
                title="Research Results",
                border_style="blue"
            )
        )


async def main():
    """Run the research assistant example."""
    # Load environment variables
    load_dotenv()
    
    # Create research assistant
    assistant = ResearchAssistant()
    
    # Example research topics
    topics = [
        "Latest developments in quantum computing",
        "Impact of AI on healthcare",
        "Future of renewable energy"
    ]
    
    # Conduct research on each topic
    for topic in topics:
        print(f"\n[bold]Researching: {topic}[/bold]")
        
        result = await assistant.research(
            topic=topic,
            max_steps=5,
            save_to_memory=True
        )
        
        assistant.display_result(result)


if __name__ == "__main__":
    asyncio.run(main()) 