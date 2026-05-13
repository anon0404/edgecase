from typing import Any, Dict
from edgecase import Trace
from .base import BaseWorkflow, WorkflowResult

class BankingWorkflow(BaseWorkflow):
    name = "banking_identity_verification"

    def run(self, case: Dict[str, Any]) -> WorkflowResult:
        signals = list(case.get("signals", []))

        model_calls = 1
        tokens = 900

        if "fraud_risk" in signals or "identity_risk" in signals:
            model_calls += 1
            tokens += 600

        if "disability_signal" in signals or "language_barrier" in signals:
            model_calls += 1
            tokens += 450

        trace = Trace(
            signals=signals,
            workflow=self.name,
            route="verification_router",
            model_calls=model_calls,
            tokens_estimate=tokens,
            latency_ms=400 + model_calls * 350,
        )

        return WorkflowResult({
            "case_id": case["id"],
            "domain": "banking",
            "trace": trace.model_dump(),
            "edgecase_report": self.evaluate(trace),
        })
