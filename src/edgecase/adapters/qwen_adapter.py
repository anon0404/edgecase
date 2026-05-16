from typing import Dict, Any, Optional
import json
import urllib.request

from .base import BaseAdapter

class QwenOllamaAdapter(BaseAdapter):
    name = "qwen_ollama"

    def __init__(
        self,
        model: str = "qwen2.5:7b",
        base_url: str = "http://localhost:11434",
    ):
        self.model = model
        self.base_url = base_url.rstrip("/")

    def generate(self, prompt: str, system: Optional[str] = None) -> Dict[str, Any]:
        full_prompt = prompt if not system else f"{system}\n\nUser:\n{prompt}"

        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
        }

        req = urllib.request.Request(
            f"{self.base_url}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=180) as response:
            data = json.loads(response.read().decode("utf-8"))

        text = data.get("response", "")

        prompt_eval_count = data.get("prompt_eval_count") or 0
        eval_count = data.get("eval_count") or 0

        return {
            "model": self.model,
            "response": text,
            "tokens_estimate": prompt_eval_count + eval_count,
        }
