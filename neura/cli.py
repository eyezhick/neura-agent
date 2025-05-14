"""Command-line interface for NEURA."""

import asyncio
from typing import List, Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from neura.agents.executor import ExecutorAgent
from neura.agents.planner import PlannerAgent
from neura.core.graph import create_agent_graph_with_tools
from neura.memory.vector import VectorMemory, VectorMemoryConfig
from neura.tools.web_scraper import ScrapingConfig, WebScraperTool
from neura.tools.web_search import WebSearchTool


app = typer.Typer(
    name="neura",
    help="NEURA - Neural Entity for Understanding, Reasoning, and Autonomy",
    add_completion=False
)
console = Console()


class NEURACLI:
    """CLI interface for NEURA."""
    
    def __init__(
        self,
        model_name: str = "gpt-4-turbo-preview",
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ):
        """Initialize the CLI.
        
        Args:
            model_name: The name of the LLM to use
            temperature: The temperature for generation
            max_tokens: Maximum tokens to generate
        """
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
                collection_name="cli_memory",
                persist_directory="./data/cli_memory"
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
    
    async def execute_task(
        self,
        task: str,
        max_steps: int = 5,
        save_to_memory: bool = True
    ) -> dict:
        """Execute a task.
        
        Args:
            task: The task to execute
            max_steps: Maximum number of steps
            save_to_memory: Whether to save results to memory
            
        Returns:
            Task results
        """
        # Initial state
        initial_state = {
            "messages": [{
                "role": "user",
                "content": task
            }],
            "memory": {},
            "context": {
                "max_steps": max_steps,
                "save_to_memory": save_to_memory
            },
            "current_agent": "planner"
        }
        
        # Run the task
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task_progress = progress.add_task(
                "Executing task...",
                total=None
            )
            
            result = await self.graph.ainvoke(initial_state)
            
            progress.update(task_progress, completed=True)
        
        # Save to memory if requested
        if save_to_memory:
            self.memory.add_memory(
                content=task,
                metadata={
                    "type": "task",
                    "steps": len(result["context"].get("execution_results", {}))
                }
            )
        
        return result
    
    def display_result(self, result: dict) -> None:
        """Display the task result.
        
        Args:
            result: The task result
        """
        # Format the output
        output = []
        
        # Add plan
        if "plan" in result["context"]:
            plan = result["context"]["plan"]
            output.append("\n[bold blue]Execution Plan:[/bold blue]")
            output.append(plan)
        
        # Add execution results
        if "execution_results" in result["context"]:
            output.append("\n[bold green]Results:[/bold green]")
            for step_id, step_result in result["context"]["execution_results"].items():
                output.append(f"\n{step_result}")
        
        # Add memory stats
        memory_stats = self.memory.get_stats()
        output.append(f"\n[bold yellow]Memory Stats:[/bold yellow]")
        output.append(f"• Total memories: {memory_stats['count']}")
        output.append(f"• Vector dimensions: {memory_stats['dimensions']}")
        
        # Display the result
        console.print(
            Panel(
                "\n".join(output),
                title="Task Results",
                border_style="blue"
            )
        )


@app.command()
def run(
    task: str = typer.Argument(..., help="The task to execute"),
    model: str = typer.Option(
        "gpt-4-turbo-preview",
        help="The LLM model to use"
    ),
    temperature: float = typer.Option(
        0.7,
        help="The temperature for generation"
    ),
    max_tokens: int = typer.Option(
        2000,
        help="Maximum tokens to generate"
    ),
    max_steps: int = typer.Option(
        5,
        help="Maximum number of execution steps"
    ),
    save_memory: bool = typer.Option(
        True,
        help="Whether to save results to memory"
    )
):
    """Execute a task using NEURA."""
    # Create CLI instance
    cli = NEURACLI(
        model_name=model,
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    # Execute the task
    result = asyncio.run(
        cli.execute_task(
            task=task,
            max_steps=max_steps,
            save_to_memory=save_memory
        )
    )
    
    # Display the result
    cli.display_result(result)


@app.command()
def memory(
    query: Optional[str] = typer.Option(
        None,
        help="Query to search memories"
    ),
    clear: bool = typer.Option(
        False,
        help="Clear all memories"
    )
):
    """Manage NEURA's memory."""
    # Create CLI instance
    cli = NEURACLI()
    
    if clear:
        cli.memory.clear()
        console.print("[green]Memory cleared successfully![/green]")
        return
    
    if query:
        # Search memories
        results = cli.memory.get_memory(query)
        
        # Display results
        console.print("\n[bold blue]Search Results:[/bold blue]")
        for doc in results:
            console.print(f"\n[bold]{doc.metadata.get('type', 'Unknown')}[/bold]")
            console.print(doc.page_content)
            console.print("-" * 80)
    else:
        # Display memory stats
        stats = cli.memory.get_stats()
        console.print(
            Panel(
                f"Total memories: {stats['count']}\n"
                f"Vector dimensions: {stats['dimensions']}\n"
                f"Distance metric: {stats['distance_metric']}",
                title="Memory Statistics",
                border_style="blue"
            )
        )


if __name__ == "__main__":
    app() 