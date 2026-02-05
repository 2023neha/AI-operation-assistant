from ..llm.client import LLMClient

class VerifierAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def verify(self, original_task: str, execution_log: list):
        log_str = "\n".join([f"- {entry}" for entry in execution_log])
        
        system_prompt = """
        You are a Verifier Agent. Your job is to review the steps executed by the Executor Agent and determine if the Original User Task has been fully satisfyingly completed.
        
        If yes, provide a final concise answer to the user.
        If no, explain what is missing.
        
        Output format:
        Status: [PASS/FAIL]
        Reasoning: [Explanation]
        Final Answer: [The answer if PASS, else empty]
        """
        
        prompt = f"""
        Original Task: {original_task}
        
        Execution Log:
        {log_str}
        """
        
        try:
            response = self.llm.generate(prompt, system_prompt=system_prompt)
            return response.content
        except Exception as e:
            return f"Verification failed: {str(e)}"
