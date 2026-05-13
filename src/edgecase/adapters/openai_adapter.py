from typing import Dict, Any, Optional
from .base import BaseAdapter

class OpenAIAdapter(BaseAdapter):
    name = "openai"

    def __init__(self, client, model: str = "gpt-4o"):
        self.client = client
        self.model = model

    def generate(self, prompt: str, system: Optional[str] = None) -> Dict[str, Any]:
        messages = []

        if system:
            messages.append({
                "role": "system",
                "content": system,
            })

        messages.append({
            "role": "user",
            "content": prompt,
        })

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        text = response.choices[0].message.content

        usage = getattr(response, "usage", None)

        return {
            "model": self.model,
            "response": text,
            "tokens_estimate": getattr(usage, "total_tokens", None),
        }
