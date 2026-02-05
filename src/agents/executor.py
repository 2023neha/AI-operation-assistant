from ..llm.client import LLMClient
from ..tools.base import ToolRegistry
import json

class ExecutorAgent:
    def __init__(self, llm: LLMClient, tool_registry: ToolRegistry):
        self.llm = llm
        self.registry = tool_registry

    def execute_step(self, step_description: str):
        tools_schema = self.registry.get_openai_tools()
        
        system_prompt = f"""
        You are an Executor Agent. Your goal is to execute the following step: "{step_description}".
        You have access to the following tools. Select the right tool and parameters.
        If no tool is needed (e.g., pure reasoning), just answer the question.
        """
        
        try:
            response = self.llm.generate(
                prompt=step_description,
                system_prompt=system_prompt,
                tools=tools_schema
            )
            
            if response.tool_calls:
                tool_call = response.tool_calls[0]
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                
                tool = self.registry.get_tool(function_name)
                if tool:
                    try:
                        result = tool.run(**arguments)
                        return f"Tool '{function_name}' output: {result}"
                    except Exception as e:
                        return f"Error executing tool '{function_name}': {str(e)}"
                else:
                    return f"Tool '{function_name}' not found."
            else:
                return response.content
        except Exception as e:
            return f"Error executing step: {str(e)}"
