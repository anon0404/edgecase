from typing import Dict

from edgecase import Trace, Registry, detect

from .nodes import RuntimeNode, RuntimeEvent

from .executors import (
    RuntimeContext,
    EXECUTOR_MAP,
)

class WorkflowRuntime:
    def __init__(
        self,
        nodes: Dict[str, RuntimeNode],
        start: str,
        prompt: str,
    ):
        self.nodes = nodes

        self.start = start

        self.prompt = prompt

        self.registry = Registry.default()

    def run(self):
        current = self.start

        context = RuntimeContext(
            prompt=self.prompt
        )

        events = []

        security = 0.3
        care = 0.7
        accessibility = 0.7
        privacy = 0.2
        energy = 0.1

        step = 0

        while current:
            step += 1

            node = self.nodes[current]

            executor = EXECUTOR_MAP.get(node.type)

            if executor:
                executor.execute(context, node)

            trace = Trace(
                signals=context.signals,
                workflow="runtime_workflow",
                model_calls=context.metrics["model_calls"],
                tokens_estimate=context.metrics["tokens"],
            )

            result = detect(trace, self.registry)

            if "fraud_risk" in context.signals:
                security += 0.18
                accessibility -= 0.12

            if "self_harm" in context.signals:
                care += 0.22
                privacy += 0.10

            if context.metrics["model_calls"] > 0:
                energy += 0.18

            if result.collision_detected:
                energy += 0.12

            event = RuntimeEvent(
                timestamp=step,
                node_id=node.id,
                label=node.label,
                type=node.type,
                active_signals=list(set(context.signals)),
                obligations=result.audit.get(
                    "obligations",
                    [],
                ),
                collision=result.audit.get(
                    "collision"
                ),
                mitigation=result.recommended_mitigation,
                metrics={
                    "security": round(
                        min(security, 1.0), 3
                    ),
                    "care": round(
                        min(care, 1.0), 3
                    ),
                    "accessibility": round(
                        max(accessibility, 0.0), 3
                    ),
                    "privacy": round(
                        min(privacy, 1.0), 3
                    ),
                    "energy": round(
                        min(energy, 1.0), 3
                    ),
                },
            )

            events.append(event)

            next_nodes = node.next_nodes

            current = (
                next_nodes[0]
                if next_nodes
                else None
            )

        return events
