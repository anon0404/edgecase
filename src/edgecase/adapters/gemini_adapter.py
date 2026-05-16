from typing import Dict, Any, Optional
from .base import BaseAdapter

class GeminiAdapter(BaseAdapter):
    name = "gemini"

    def __init__(self, client, model: str = "gemini-2.5-pro"):
        self.client = client
        self.model = model

    def generate(self, prompt: str, system: Optional[str] = None) -> Dict[str, Any]:
        full_prompt = prompt if not system else f"{system}\n\nUser:\n{prompt}"

        response = self.client.models.generate_content(
            model=self.model,
            contents=full_prompt,
        )

        text = getattr(response, "text", "")

        usage = getattr(response, "usage_metadata", None)
        total_tokens = None

        if usage is not None:
            total_tokens = getattr(usage, "total_token_count", None)

        return {
            "model": self.model,
            "response": text,
            "tokens_estimate": total_tokens,
        }
