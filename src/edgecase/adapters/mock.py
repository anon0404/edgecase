from typing import Dict, Any, Optional
from .base import BaseAdapter

class MockAdapter(BaseAdapter):
    name = "mock"

    def generate(self, prompt: str, system: Optional[str] = None) -> Dict[str, Any]:
        lower = prompt.lower()

        if "self-harm" in lower or "suicide" in lower:
            response = "Escalation recommended. Support-oriented response generated."
        elif "fraud" in lower:
            response = "Verification required before proceeding."
        elif "medical" in lower:
            response = "Additional review recommended due to regulated advice."
        else:
            response = "Standard assistant response."

        return {
            "model": self.name,
            "response": response,
            "tokens_estimate": len(prompt.split()) * 2 + 120,
            "latency_ms": 180,
        }
