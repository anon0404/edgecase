from typing import Any, Dict
from edgecase import Trace
from .base import BaseWorkflow, WorkflowResult

class HealthcareWorkflow(BaseWorkflow):
    name = "healthcare_triage"

    def run(self, case: Dict[str, Any]) -> WorkflowResult:
        signals = list(case.get("signals", []))

        model_calls = 1
        tokens = 1200

        if "high_risk" in signals or "regulated_advice" in signals:
            model_calls += 2
            tokens += 1600

        if "uncertain" in signals:
            model_calls += 1
            tokens += 900

        if "compute_pressure" in signals or "latency_constraint" in signals:
            tokens += 300

        trace = Trace(
            signals=signals,
            workflow=self.name,
            route="triage_review_router",
            model_calls=model_calls,
            tokens_estimate=tokens,
            latency_ms=650 + model_calls * 520,
        )

        return WorkflowResult({
            "case_id": case["id"],
            "domain": "healthcare",
            "trace": trace.model_dump(),
            "edgecase_report": self.evaluate(trace),
        })
