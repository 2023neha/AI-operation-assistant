from .planner import PlannerAgent
from .executor import ExecutorAgent
from .verifier import VerifierAgent
from ..llm.client import LLMClient
from ..tools.base import ToolRegistry
from ..tools.weather import WeatherTool
from ..tools.crypto import CryptoTool

class Orchestrator:
    def __init__(self):
        self.llm = LLMClient()
        
        self.registry = ToolRegistry()
        self.registry.register(WeatherTool())
        self.registry.register(CryptoTool())
        
        self.planner = PlannerAgent(self.llm)
        self.executor = ExecutorAgent(self.llm, self.registry)
        self.verifier = VerifierAgent(self.llm)

    def run(self, user_task: str):
        yield {"type": "status", "content": f"Processing task: {user_task}"}
        
        plan_result = self.planner.plan(user_task)
        if "error" in plan_result:
            yield {"type": "error", "content": plan_result.get('error')}
            return

        steps = plan_result.get("steps", [])
        yield {"type": "plan", "content": steps}
        
        execution_log = []
        
        for step in steps:
            yield {"type": "status", "content": f"Executing: {step}"}
            result = self.executor.execute_step(step)
            execution_log.append(f"Step: {step} | Result: {result}")
            yield {"type": "execution", "step": step, "result": result}
            
        yield {"type": "status", "content": "Verifying results..."}
        verification = self.verifier.verify(user_task, execution_log)
        yield {"type": "verification", "content": verification}
