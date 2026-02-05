import os
from openai import OpenAI
import json
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self, api_key=None, base_url=None, model=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL") or "https://generativelanguage.googleapis.com/v1beta/openai/"
        self.model = model or os.getenv("OPENAI_MODEL", "gemini-3-flash-preview")
        
        if not self.api_key:
            self.api_key = "dummy-key"
            
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def generate(self, prompt, system_prompt="You are a helpful assistant.", tools=None, json_mode=False):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        params = {
            "model": self.model,
            "messages": messages,
        }

        if json_mode:
            params["response_format"] = {"type": "json_object"}

        if tools:
            params["tools"] = tools
            params["tool_choice"] = "auto"

        response = self.client.chat.completions.create(**params)
        return response.choices[0].message
