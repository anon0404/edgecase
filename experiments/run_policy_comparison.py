import json
from pathlib import Path

from edgecase.models import Trace
from edgecase.policies import (
    StrictBlockPolicy,
    EscalationPolicy,
    VerificationPolicy,
    MaximumReviewPolicy,
    AdaptiveEdgeCasePolicy,
)

DATA = Path("datasets/edgecase_benchmark_v1.jsonl")

OUT = Path("experiments/results/policy_comparison.json")

POLICIES = [
    StrictBlockPolicy(),
    EscalationPolicy(),
    VerificationPolicy(),
    MaximumReviewPolicy(),
    AdaptiveEdgeCasePolicy(),
]

def summarize(rows):
    summary = {}

    for row in rows:
        name = row["policy"]

        summary.setdefault(name, {
            "cases": 0,
            "care_suppression": 0.0,
            "security_risk": 0.0,
            "accessibility_burden": 0.0,
            "privacy_exposure": 0.0,
            "high_energy": 0,
        })

        ext = row["externalities"]

        summary[name]["cases"] += 1
        summary[name]["care_suppression"] += ext["care_suppression_risk"]
        summary[name]["security_risk"] += ext["security_risk"]
        summary[name]["accessibility_burden"] += ext["accessibility_burden"]
        summary[name]["privacy_exposure"] += ext["privacy_exposure"]

        if ext["energy_cost"] == "high":
            summary[name]["high_energy"] += 1

    for name in summary:
        n = summary[name]["cases"]

        summary[name]["avg_care_suppression"] = round(
            summary[name]["care_suppression"] / n, 3
        )

        summary[name]["avg_security_risk"] = round(
            summary[name]["security_risk"] / n, 3
        )

        summary[name]["avg_accessibility_burden"] = round(
            summary[name]["accessibility_burden"] / n, 3
        )

        summary[name]["avg_privacy_exposure"] = round(
            summary[name]["privacy_exposure"] / n, 3
        )

        summary[name]["high_energy_rate"] = round(
            summary[name]["high_energy"] / n, 3
        )

    return summary

def main():
    cases = [
        json.loads(line)
        for line in DATA.read_text().splitlines()
    ]

    rows = []

    for case in cases:
        trace = Trace(
            signals=case["signals"],
            workflow=case["domain"],
            model_calls=2,
            tokens_estimate=1200,
        )

        for policy in POLICIES:
            result = policy.apply(trace)

            rows.append({
                "case_id": case["id"],
                "policy": policy.name,
                "signals": case["signals"],
                "workflow": case["domain"],
                "recommended_mitigation": result.recommended_mitigation,
                "externalities": result.externalities.model_dump(),
            })

    summary = summarize(rows)

    OUT.parent.mkdir(parents=True, exist_ok=True)

    OUT.write_text(json.dumps({
        "summary": summary,
        "rows": rows,
    }, indent=2))

    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
