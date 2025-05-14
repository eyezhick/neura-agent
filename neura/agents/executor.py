"""Executor agent implementation for executing planned steps."""

import json
from typing import Any, Dict, List, Optional

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.tools import Tool

from neura.agents.base import AgentState, BaseAgent


class ExecutorAgent(BaseAgent):
    """Agent responsible for executing planned steps."""
    
    def __init__(
        self,
        model_name: str = "gpt-4-turbo-preview",
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ):
        """Initialize the executor agent.
        
        Args:
            model_name: The name of the LLM to use
            temperature: The temperature for generation
            max_tokens: Maximum tokens to generate
        """
        super().__init__(
            name="executor",
            description="Task execution agent"
        )
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )
        self._tools: Dict[str, Tool] = {}
        self._step_results: Dict[str, Any] = {}
    
    def add_tool(self, tool: Tool) -> None:
        """Add a tool to the executor's toolkit.
        
        Args:
            tool: The tool to add
        """
        self._tools[tool.name] = tool
    
    def _create_execution_prompt(
        self,
        step: Dict[str, Any],
        context: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Create the execution prompt for a step.
        
        Args:
            step: The step to execute
            context: Additional context for execution
            
        Returns:
            The formatted prompt messages
        """
        system_prompt = """You are an execution expert. Your job is to execute the given step using the 
        appropriate tool and provide clear, detailed results.
        
        Available tools:
        {tools}
        
        Previous step results:
        {previous_results}
        
        Execute the step and provide:
        1. The exact tool to use and why
        2. The input parameters for the tool
        3. How to handle the tool's output
        4. Any necessary error handling
        
        Format your response as a JSON object with the following structure:
        {
            "tool": "tool_name",
            "parameters": {
                "param1": "value1"
            },
            "error_handling": "How to handle potential errors",
            "expected_output": "What output to expect"
        }"""
        
        return [
            SystemMessage(content=system_prompt.format(
                tools="\n".join(f"- {name}: {tool.description}" for name, tool in self._tools.items()),
                previous_results=json.dumps(self._step_results, indent=2)
            )),
            HumanMessage(content=f"Step to execute: {json.dumps(step, indent=2)}\nContext: {json.dumps(context, indent=2)}")
        ]
    
    def _execute_step(self, step: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """Execute a single step using the appropriate tool.
        
        Args:
            step: The step to execute
            context: Additional context for execution
            
        Returns:
            The result of the step execution
        """
        # Generate execution plan
        prompt = self._create_execution_prompt(step, context)
        response = self.llm.invoke(prompt)
        execution_plan = json.loads(response.content)
        
        # Get the tool
        tool = self._tools.get(execution_plan["tool"])
        if not tool:
            raise ValueError(f"Tool {execution_plan['tool']} not found")
        
        # Execute the tool
        try:
            result = tool(**execution_plan["parameters"])
            return result
        except Exception as e:
            # Handle errors based on the execution plan
            raise RuntimeError(f"Error executing step {step['id']}: {str(e)}")
    
    def process(self, state: AgentState) -> AgentState:
        """Process the current state and execute planned steps.
        
        Args:
            state: The current agent state
            
        Returns:
            The updated agent state with execution results
        """
        if not self._initialized:
            self.initialize()
        
        # Get the plan from context
        plan = state.context.get("plan")
        if not plan:
            return state
        
        try:
            plan_data = json.loads(plan)
            steps = plan_data.get("steps", [])
            
            # Execute each step
            for step in steps:
                step_id = step["id"]
                
                # Check dependencies
                dependencies = step.get("dependencies", [])
                for dep in dependencies:
                    if dep not in self._step_results:
                        raise ValueError(f"Dependency {dep} not satisfied")
                
                # Execute the step
                result = self._execute_step(step, state.context)
                self._step_results[step_id] = result
                
                # Update state
                state.messages.append({
                    "role": "assistant",
                    "content": f"Executed step {step_id}:\n{json.dumps(result, indent=2)}"
                })
            
            # Store final results
            state.context["execution_results"] = self._step_results
            
        except Exception as e:
            state.messages.append({
                "role": "assistant",
                "content": f"Error during execution: {str(e)}"
            })
        
        return state 