"""Simple example demonstrating NEURA's web search capabilities."""

import os
from typing import List

from dotenv import load_dotenv

from neura.agents.executor import ExecutorAgent
from neura.agents.planner import PlannerAgent
from neura.core.graph import create_agent_graph_with_tools
from neura.tools.web_search import WebSearchTool


def main():
    """Run a simple web search example."""
    # Load environment variables
    load_dotenv()
    
    # Create agents
    planner = PlannerAgent()
    executor = ExecutorAgent()
    
    # Create tools
    tools: List[WebSearchTool] = [WebSearchTool()]
    
    # Create the agent graph
    graph = create_agent_graph_with_tools(planner, executor, tools)
    
    # Initial state
    initial_state = {
        "messages": [{
            "role": "user",
            "content": "Research the latest developments in quantum computing and summarize the key findings."
        }],
        "memory": {},
        "context": {},
        "current_agent": "planner"
    }
    
    # Run the graph
    print("Starting NEURA agent...")
    result = graph.invoke(initial_state)
    
    # Print results
    print("\nFinal Results:")
    print("=" * 80)
    for message in result["messages"]:
        if message["role"] == "assistant":
            print(f"\n{message['content']}\n")
            print("-" * 80)


if __name__ == "__main__":
    main() 