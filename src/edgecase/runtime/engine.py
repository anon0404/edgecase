from typing import Dict, List

from edgecase import Trace, Registry, detect

from .nodes import RuntimeNode, RuntimeEvent

class WorkflowRuntime:
    def __init__(self, nodes: Dict[str, RuntimeNode], start: str):
        self.nodes = nodes
        self.start = start
        self.registry = Registry.default()

    def run(self):
        current = self.start

        active_signals = []

        events = []

        security = 0.3
        care = 0.7
        accessibility = 0.7
        privacy = 0.2
        energy = 0.1

        while current:
            node = self.nodes[current]

            active_signals.extend(node.signals)

            trace = Trace(
                signals=active_signals,
                workflow="runtime_workflow",
                model_calls=1,
                tokens_estimate=600,
            )

            result = detect(trace, self.registry)

            if "fraud" in " ".join(active_signals):
                security += 0.18
                care -= 0.07

            if "self_harm" in active_signals:
                care += 0.24
                privacy += 0.12

            if "compute_pressure" in active_signals:
                energy += 0.28

            if result.collision_detected:
                energy += 0.15

            event = RuntimeEvent(
                timestamp=node.metadata.get("step", 0),
                node_id=node.id,
                label=node.label,
                type=node.type,
                active_signals=list(set(active_signals)),
                obligations=result.audit.get("obligations", []),
                collision=result.audit.get("collision"),
                mitigation=result.recommended_mitigation,
                metrics={
                    "security": round(min(security, 1.0), 3),
                    "care": round(min(care, 1.0), 3),
                    "accessibility": round(min(accessibility, 1.0), 3),
                    "privacy": round(min(privacy, 1.0), 3),
                    "energy": round(min(energy, 1.0), 3),
                },
            )

            events.append(event)

            next_nodes = node.next_nodes

            current = next_nodes[0] if next_nodes else None

        return events
