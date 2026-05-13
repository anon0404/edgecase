import json
from pathlib import Path

from edgecase import Registry, Trace, detect


DATA = Path("benchmarks/paired_scenarios.jsonl")


def main():
    registry = Registry.default()
    rows = []

    for line in DATA.read_text().splitlines():
        item = json.loads(line)

        trace = Trace(
            signals=item["signals"],
            workflow=item["workflow"],
            model_calls=item.get("model_calls", 1),
            tokens_estimate=item.get("tokens_estimate", 1000),
        )

        report = detect(trace, registry)

        rows.append(
            {
                "id": item["id"],
                "expected": item["expected_collision"],
                "detected": report.collision_type,
                "correct": item["expected_collision"] == report.collision_type,
                "mitigation": report.recommended_mitigation,
                "externalities": report.externalities.model_dump(),
            }
        )

    total = len(rows)
    correct = sum(row["correct"] for row in rows)

    Path("experiments/results").mkdir(parents=True, exist_ok=True)
    Path("experiments/results/benchmark_results.json").write_text(
        json.dumps(
            {
                "total": total,
                "correct": correct,
                "accuracy": correct / total if total else 0,
                "rows": rows,
            },
            indent=2,
        )
    )

    print(
        json.dumps(
            {
                "total": total,
                "correct": correct,
                "accuracy": correct / total if total else 0,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
