# Earliest prototype benchmark runner, reading benchmarks/paired_scenarios.jsonl
# (9 hand-written scenarios, no generator script) and using the standalone
# edgecase.baselines functions rather than the policies/ classes. Not called
# by run_all.sh and not the source of any paper-reported result. Kept for
# reference only.
import json
from pathlib import Path

from edgecase import Registry, Trace, detect
from edgecase.baselines import always_block, always_escalate, always_verify, strongest_stack
from edgecase.metrics import summarize

DATA = Path("benchmarks/paired_scenarios.jsonl")
OUT = Path("experiments/results")

POLICIES = {
    "edgecase": lambda trace: detect(trace, Registry.default()),
    "always_block": always_block,
    "always_escalate": always_escalate,
    "always_verify": always_verify,
    "strongest_stack": strongest_stack,
}

def evaluate_policy(name: str, fn, scenarios: list[dict]) -> dict:
    rows = []

    for item in scenarios:
        trace = Trace(
            signals=item["signals"],
            workflow=item["workflow"],
            model_calls=item.get("model_calls", 1),
            tokens_estimate=item.get("tokens_estimate", 1000),
        )

        report = fn(trace)

        rows.append({
            "policy": name,
            "id": item["id"],
            "expected_collision": item["expected_collision"],
            "detected_collision": report.collision_type,
            "expected_mitigation": item["expected_mitigation"],
            "recommended_mitigation": report.recommended_mitigation,
            "correct_collision": report.collision_type == item["expected_collision"],
            "correct_mitigation": report.recommended_mitigation == item["expected_mitigation"],
            "externalities": report.externalities.model_dump(),
            "audit": report.audit,
        })

    return {
        "policy": name,
        "summary": summarize(rows),
        "rows": rows,
    }

def main():
    scenarios = [json.loads(line) for line in DATA.read_text().splitlines()]
    OUT.mkdir(parents=True, exist_ok=True)

    results = {
        name: evaluate_policy(name, fn, scenarios)
        for name, fn in POLICIES.items()
    }

    Path(OUT / "benchmark_results.json").write_text(json.dumps(results, indent=2))

    summary = {
        name: result["summary"]
        for name, result in results.items()
    }

    Path(OUT / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
