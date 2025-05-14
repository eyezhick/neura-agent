"""Planner agent implementation for task decomposition and planning."""

from typing import Any, Dict, List, Optional

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain.tools import Tool

from neura.agents.base import AgentState, BaseAgent


class PlannerAgent(BaseAgent):
    """Agent responsible for task decomposition and planning."""
    
    def __init__(
        self,
        model_name: str = "gpt-4-turbo-preview",
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ):
        """Initialize the planner agent.
        
        Args:
            model_name: The name of the LLM to use
            temperature: The temperature for generation
            max_tokens: Maximum tokens to generate
        """
        super().__init__(
            name="planner",
            description="Task decomposition and planning agent"
        )
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )
        self._tools: List[Tool] = []
    
    def add_tool(self, tool: Tool) -> None:
        """Add a tool to the planner's toolkit.
        
        Args:
            tool: The tool to add
        """
        self._tools.append(tool)
    
    def _create_planning_prompt(self, task: str) -> List[Dict[str, str]]:
        """Create the planning prompt for task decomposition.
        
        Args:
            task: The task to decompose
            
        Returns:
            The formatted prompt messages
        """
        system_prompt = """You are a task planning expert. Your job is to break down complex tasks into smaller, 
        manageable steps that can be executed by an AI agent. Consider dependencies between steps and ensure 
        the plan is logical and complete.
        
        Available tools:
        {tools}
        
        Create a detailed plan that:
        1. Breaks down the task into clear, actionable steps
        2. Identifies any dependencies between steps
        3. Specifies which tools should be used for each step
        4. Includes any necessary context or information gathering steps
        
        Format your response as a JSON object with the following structure:
        {
            "steps": [
                {
                    "id": "step_1",
                    "description": "Description of the step",
                    "tool": "tool_name",
                    "dependencies": ["step_0"],
                    "expected_output": "What this step should produce"
                }
            ]
        }"""
        
        return [
            SystemMessage(content=system_prompt.format(
                tools="\n".join(f"- {tool.name}: {tool.description}" for tool in self._tools)
            )),
            HumanMessage(content=f"Task to plan: {task}")
        ]
    
    def process(self, state: AgentState) -> AgentState:
        """Process the current state and create a plan.
        
        Args:
            state: The current agent state
            
        Returns:
            The updated agent state with the plan
        """
        if not self._initialized:
            self.initialize()
        
        # Extract the task from the last message
        if not state.messages:
            return state
        
        last_message = state.messages[-1]
        task = last_message.get("content", "")
        
        # Generate the plan
        prompt = self._create_planning_prompt(task)
        response = self.llm.invoke(prompt)
        
        # Update the state with the plan
        state.context["plan"] = response.content
        state.messages.append({
            "role": "assistant",
            "content": f"Created execution plan:\n{response.content}"
        })
        
        return state 