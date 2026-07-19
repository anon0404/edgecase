import json
from pathlib import Path
from statistics import mean

from edgecase.detectors import INCOMPATIBLE_ACTIONS
from edgecase.models import Trace
from edgecase.registry import Registry

DATA = Path("datasets/edgecase_benchmark_v1.jsonl")
OUT_JSON = Path("experiments/results/ablation_analysis.json")
OUT_MD = Path("experiments/tables/ablation_analysis.md")

# Non-adaptive fallback mitigation used by the "- Adaptive Routing"
# configuration: a raw action name (not a compound mitigation string), so it
# can only ever earn partial credit, never an exact match.
FIXED_ROUTING_ACTION = "increase_review"

def score(mitigation, expected, collision_type):
    if mitigation == expected:
        return 1.0
    if collision_type is None:
        return 0.0
    for action_pair, (c_type, _) in INCOMPATIBLE_ACTIONS.items():
        if c_type == collision_type and mitigation in action_pair:
            return 0.5
    return 0.0

def full_edgecase(trace, registry):
    triggered = registry.triggered_by(trace.signals)
    actions = {o.action for o in triggered}
    for pair, (c_type, mitigation) in INCOMPATIBLE_ACTIONS.items():
        if pair.issubset(actions):
            return mitigation, c_type
    return None, None

def no_obligation_registry(trace, registry):
    # An empty registry: no obligations ever trigger, so no action set is
    # ever formed and no mitigation can be selected.
    return None, None

def no_collision_detection(trace, registry):
    # Obligations still trigger via the registry, but there is no pairing
    # table to recognize that two triggered actions collide, so no
    # mitigation is ever synthesized from them.
    return None, None

def no_adaptive_routing(trace, registry):
    # Collision detection is intact (the pair is still identified), but
    # mitigation selection is replaced by one fixed, non-adaptive action
    # regardless of which collision was found.
    _, collision_type = full_edgecase(trace, registry)
    if collision_type is None:
        return None, None
    return FIXED_ROUTING_ACTION, collision_type

def no_runtime_instrumentation(trace, registry):
    # Mitigation selection in detect() only ever reads trace.signals; trace
    # metadata (model_calls, tokens_estimate) is consumed solely by the
    # safety_vs_energy externality-scoring branch, not by mitigation
    # selection. Zeroing it out should therefore have no effect here - that
    # null result is itself the finding.
    stripped = Trace(signals=trace.signals, workflow=trace.workflow, model_calls=0, tokens_estimate=0)
    return full_edgecase(stripped, registry)

CONFIGURATIONS = {
    "Full EdgeCase": full_edgecase,
    "- Obligation Registry": no_obligation_registry,
    "- Collision Detection": no_collision_detection,
    "- Adaptive Routing": no_adaptive_routing,
    "- Runtime Instrumentation": no_runtime_instrumentation,
}

def main():
    cases = [json.loads(line) for line in DATA.read_text().splitlines() if line.strip()]
    registry = Registry.default()

    rows = []
    for name, resolve in CONFIGURATIONS.items():
        scores = []
        for case in cases:
            trace = Trace(signals=case["signals"], workflow=case["domain"], model_calls=1, tokens_estimate=900)
            mitigation, _ = resolve(trace, registry)
            # Partial credit is judged against the case's true collision type,
            # not whatever the (possibly ablated) detector believes - a
            # misdetecting configuration shouldn't get to grade itself
            # against its own wrong belief.
            scores.append(score(mitigation, case["expected_mitigation"], case["collision"]))
        rows.append({"configuration": name, "mitigation_accuracy": round(mean(scores), 3)})

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(rows, indent=2))

    with OUT_MD.open("w") as f:
        f.write("| Configuration | Mitigation Accuracy |\n")
        f.write("| --- | --- |\n")
        for row in rows:
            f.write(f"| {row['configuration']} | {row['mitigation_accuracy']} |\n")

    print(json.dumps(rows, indent=2))
    print(f"Wrote {OUT_JSON}, {OUT_MD}")

if __name__ == "__main__":
    main()
