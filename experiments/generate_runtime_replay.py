import json
from pathlib import Path

from edgecase.runtime.engine import WorkflowRuntime

from runtime_workflows import (
    crisis_workflow,
    banking_workflow,
)

OUT = Path("website/public/data/runtime_replay.json")

def serialize(events):
    return [
        {
            "timestamp": e.timestamp,
            "node_id": e.node_id,
            "label": e.label,
            "type": e.type,
            "signals": e.active_signals,
            "obligations": e.obligations,
            "collision": e.collision,
            "mitigation": e.mitigation,
            "metrics": e.metrics,
        }
        for e in events
    ]

def main():
    replay = []

    for name, builder in [
        ("crisis", crisis_workflow),
        ("banking", banking_workflow),
    ]:
        nodes, start = builder()

        runtime = WorkflowRuntime(
            nodes=nodes,
            start=start,
        )

        events = runtime.run()

        replay.append({
            "workflow": name,
            "events": serialize(events),
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)

    OUT.write_text(json.dumps(replay, indent=2))

    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
