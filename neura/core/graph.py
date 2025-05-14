"""LangGraph workflow implementation for NEURA."""

from typing import Any, Dict, List, Optional, Tuple, TypedDict

from langgraph.graph import END, Graph
from langgraph.prebuilt import ToolExecutor

from neura.agents.base import AgentState
from neura.agents.executor import ExecutorAgent
from neura.agents.planner import PlannerAgent


class AgentGraphState(TypedDict):
    """State for the agent graph."""
    
    messages: List[Dict[str, Any]]
    memory: Dict[str, Any]
    context: Dict[str, Any]
    current_agent: str


def create_agent_graph(
    planner: PlannerAgent,
    executor: ExecutorAgent,
) -> Graph:
    """Create the agent workflow graph.
    
    Args:
        planner: The planner agent
        executor: The executor agent
        
    Returns:
        The configured agent graph
    """
    
    def should_continue(state: AgentGraphState) -> Tuple[bool, str]:
        """Determine if the workflow should continue and which agent to use next.
        
        Args:
            state: The current graph state
            
        Returns:
            Tuple of (should_continue, next_agent)
        """
        # If we have a plan, move to execution
        if "plan" in state["context"]:
            return True, "executor"
        
        # If we have execution results, we're done
        if "execution_results" in state["context"]:
            return False, END
        
        # Otherwise, start with planning
        return True, "planner"
    
    def run_planner(state: AgentGraphState) -> AgentGraphState:
        """Run the planner agent.
        
        Args:
            state: The current graph state
            
        Returns:
            The updated state
        """
        agent_state = AgentState(
            messages=state["messages"],
            memory=state["memory"],
            context=state["context"]
        )
        
        updated_state = planner.process(agent_state)
        
        return {
            "messages": updated_state.messages,
            "memory": updated_state.memory,
            "context": updated_state.context,
            "current_agent": "planner"
        }
    
    def run_executor(state: AgentGraphState) -> AgentGraphState:
        """Run the executor agent.
        
        Args:
            state: The current graph state
            
        Returns:
            The updated state
        """
        agent_state = AgentState(
            messages=state["messages"],
            memory=state["memory"],
            context=state["context"]
        )
        
        updated_state = executor.process(agent_state)
        
        return {
            "messages": updated_state.messages,
            "memory": updated_state.memory,
            "context": updated_state.context,
            "current_agent": "executor"
        }
    
    # Create the workflow graph
    workflow = Graph()
    
    # Add nodes
    workflow.add_node("planner", run_planner)
    workflow.add_node("executor", run_executor)
    
    # Add edges
    workflow.add_edge("planner", should_continue)
    workflow.add_edge("executor", should_continue)
    
    # Set entry point
    workflow.set_entry_point("planner")
    
    return workflow.compile()


def create_agent_graph_with_tools(
    planner: PlannerAgent,
    executor: ExecutorAgent,
    tools: List[Any],
) -> Graph:
    """Create the agent workflow graph with tools.
    
    Args:
        planner: The planner agent
        executor: The executor agent
        tools: List of tools to add to both agents
        
    Returns:
        The configured agent graph
    """
    # Add tools to both agents
    for tool in tools:
        planner.add_tool(tool)
        executor.add_tool(tool)
    
    return create_agent_graph(planner, executor) 