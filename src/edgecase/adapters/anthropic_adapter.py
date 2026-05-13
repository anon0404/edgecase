from typing import Dict, Any, Optional
from .base import BaseAdapter

class AnthropicAdapter(BaseAdapter):
    name = "anthropic"

    def __init__(self, client, model: str = "claude-3-5-sonnet-latest"):
        self.client = client
        self.model = model

    def generate(self, prompt: str, system: Optional[str] = None) -> Dict[str, Any]:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=512,
            system=system or "",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        text = response.content[0].text

        usage = getattr(response, "usage", None)

        return {
            "model": self.model,
            "response": text,
            "tokens_estimate": getattr(usage, "input_tokens", None),
        }
