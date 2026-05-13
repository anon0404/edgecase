from typing import Any, Dict
from edgecase import Trace
from .base import BaseWorkflow, WorkflowResult

class CrisisWorkflow(BaseWorkflow):
    name = "crisis_assistant"

    def run(self, case: Dict[str, Any]) -> WorkflowResult:
        signals = list(case.get("signals", []))

        model_calls = 1
        tokens = 1000

        if "jailbreak" in signals or "policy_evasion" in signals:
            model_calls += 1
            tokens += 500

        if "self_harm" in signals or "crisis" in signals or "coercion" in signals:
            model_calls += 2
            tokens += 900

        trace = Trace(
            signals=signals,
            workflow=self.name,
            route="safety_and_care_router",
            model_calls=model_calls,
            tokens_estimate=tokens,
            latency_ms=500 + model_calls * 420,
        )

        return WorkflowResult({
            "case_id": case["id"],
            "domain": "crisis",
            "trace": trace.model_dump(),
            "edgecase_report": self.evaluate(trace),
        })
