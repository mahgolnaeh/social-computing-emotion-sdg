import httpx
from typing import Optional
from pydantic import BaseModel
from src.utils.model_loader import get_model_config
import json


class LLMResponse(BaseModel):
    role: str
    content: str


class LLMClient:
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.config = get_model_config(model)
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/mahgol/social-computing-project",
            "X-Title": "social_computing_project"
        }
        self.base_url = f"https://openrouter.ai/api/v1/{self.config['endpoint']}"
        self.client = httpx.AsyncClient(headers=self.headers)

    async def call(self, prompt: str, **overrides) -> Optional[str]:
        payload = {"model": self.model, "messages": [{"role": "user", "content": prompt}]}
        for key in self.config.get("supported_params", []):
            default_key = f"default_{key}"
            default = self.config.get(default_key, None)
            value = overrides.get(key, default)
            if value is not None:
                payload[key] = value
        try:
            resp = await self.client.post(self.base_url, json=payload, timeout=30)
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"]
            try:
                return json.loads(content.strip())  #   Parse JSON response
            except json.JSONDecodeError:
                return content.strip()  # Return raw content if JSON parsing fails
        except Exception as e:
            print(f"❌ LLM call error: {e}")
            return None

    async def close(self):
        await self.client.aclose()

    def call_sync(self, prompt: str, **kwargs) -> str:
        import asyncio
        return asyncio.run(self.call(prompt, **kwargs))

    def close_sync(self):
        import asyncio
        asyncio.run(self.close())