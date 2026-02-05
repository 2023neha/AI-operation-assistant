from ..llm.client import LLMClient
import json

class PlannerAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def plan(self, user_task: str):
        system_prompt = """
        You are a Planner Agent. Your job is to break down a complex user task into a sequence of simple, executable steps.
        Each step should be a self-contained action that can be performed by a tool or an agent.
        
        The available tools are:
        - get_weather(city, latitude, longitude): Get weather for a location.
        - get_crypto_price(coin_id, currency): Get crypto price.
        
        Output your plan as a JSON object with a key "steps", which is a list of strings describing each step.
        Example: {"steps": ["Get the weather in London", "Get the price of Bitcoin in USD"]}
        """
        
        try:
            response = self.llm.generate(
                prompt=f"Create a plan for: {user_task}",
                system_prompt=system_prompt,
                json_mode=True
            )
            return json.loads(response.content)
        except Exception as e:
            return {"error": f"Planning failed: {str(e)}", "raw": str(e)}
