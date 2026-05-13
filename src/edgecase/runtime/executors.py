from typing import Dict, Any, List

from edgecase.adapters import MockAdapter

class RuntimeContext:
    def __init__(self, prompt: str):
        self.prompt = prompt

        self.signals: List[str] = []

        self.outputs: Dict[str, Any] = {}

        self.metrics = {
            "tokens": 0,
            "latency_ms": 0,
            "model_calls": 0,
        }

class BaseExecutor:
    name = "base"

    def execute(self, context: RuntimeContext, node):
        raise NotImplementedError

class InputExecutor(BaseExecutor):
    name = "input"

    def execute(self, context: RuntimeContext, node):
        context.outputs[node.id] = {
            "prompt": context.prompt,
        }

class ClassifierExecutor(BaseExecutor):
    name = "classifier"

    def execute(self, context: RuntimeContext, node):
        prompt = context.prompt.lower()

        detected = []

        if any(x in prompt for x in [
            "ignore policies",
            "bypass",
            "override",
        ]):
            detected.append("policy_evasion")

        if any(x in prompt for x in [
            "fraud",
            "bank account",
            "identity",
        ]):
            detected.append("fraud_risk")

        if any(x in prompt for x in [
            "suicide",
            "self-harm",
            "don't want to live",
        ]):
            detected.append("self_harm")

        if any(x in prompt for x in [
            "urgent medical",
            "dosage",
            "medical advice",
        ]):
            detected.append("high_risk")

        context.signals.extend(detected)

        context.outputs[node.id] = {
            "detected_signals": detected,
        }

class ModelExecutor(BaseExecutor):
    name = "model"

    def __init__(self):
        self.adapter = MockAdapter()

    def execute(self, context: RuntimeContext, node):
        result = self.adapter.generate(
            prompt=context.prompt
        )

        context.metrics["model_calls"] += 1

        context.metrics["tokens"] += (
            result.get("tokens_estimate") or 0
        )

        context.metrics["latency_ms"] += (
            result.get("latency_ms") or 0
        )

        context.outputs[node.id] = result

class RouterExecutor(BaseExecutor):
    name = "router"

    def execute(self, context: RuntimeContext, node):
        signals = list(set(context.signals))

        if (
            "policy_evasion" in signals
            and "self_harm" in signals
        ):
            mitigation = "constrain_and_escalate"

        elif (
            "fraud_risk" in signals
            and "language_barrier" in signals
        ):
            mitigation = "adaptive_verification"

        elif (
            "high_risk" in signals
            and "compute_pressure" in signals
        ):
            mitigation = "adaptive_depth"

        else:
            mitigation = "standard_response"

        context.outputs[node.id] = {
            "selected_mitigation": mitigation,
        }

class AuditExecutor(BaseExecutor):
    name = "audit"

    def execute(self, context: RuntimeContext, node):
        context.outputs[node.id] = {
            "signals": list(set(context.signals)),
            "metrics": context.metrics,
        }

EXECUTOR_MAP = {
    "input": InputExecutor(),
    "classifier": ClassifierExecutor(),
    "model": ModelExecutor(),
    "router": RouterExecutor(),
    "audit": AuditExecutor(),
}
