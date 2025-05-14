"""Base agent implementation for NEURA framework."""

from typing import Any, Dict, List, Optional, Protocol, runtime_checkable

from pydantic import BaseModel, Field


class AgentState(BaseModel):
    """Base state model for agents."""
    
    messages: List[Dict[str, Any]] = Field(default_factory=list)
    memory: Dict[str, Any] = Field(default_factory=dict)
    context: Dict[str, Any] = Field(default_factory=dict)


@runtime_checkable
class Agent(Protocol):
    """Protocol defining the interface for all NEURA agents."""
    
    def initialize(self) -> None:
        """Initialize the agent with any necessary setup."""
        ...
    
    def process(self, state: AgentState) -> AgentState:
        """Process the current state and return the updated state."""
        ...
    
    def finalize(self) -> None:
        """Clean up any resources used by the agent."""
        ...


class BaseAgent:
    """Base implementation of the Agent protocol."""
    
    def __init__(self, name: str, description: Optional[str] = None):
        """Initialize the base agent.
        
        Args:
            name: The name of the agent
            description: Optional description of the agent's purpose
        """
        self.name = name
        self.description = description
        self._initialized = False
    
    def initialize(self) -> None:
        """Initialize the agent with any necessary setup."""
        if not self._initialized:
            self._initialized = True
    
    def process(self, state: AgentState) -> AgentState:
        """Process the current state and return the updated state.
        
        Args:
            state: The current agent state
            
        Returns:
            The updated agent state
        """
        if not self._initialized:
            self.initialize()
        return state
    
    def finalize(self) -> None:
        """Clean up any resources used by the agent."""
        self._initialized = False 