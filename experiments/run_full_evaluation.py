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

DATA = Path("datasets/edgecase_benchmark.jsonl")
OUT = Path("experiments/results/full_evaluation.json")

POLICIES = [
    StrictBlockPolicy(),
    EscalationPolicy(),
    VerificationPolicy(),
    MaximumReviewPolicy(),
    AdaptiveEdgeCasePolicy(),
]

def score_resolution(policy_name, mitigation, expected):
    if policy_name == "edgecase_adaptive":
        return mitigation == expected

    return mitigation == expected

def main():
    cases = [
        json.loads(line)
        for line in DATA.read_text().splitlines()
        if line.strip()
    ]

    rows = []

    for case in cases:
        trace = Trace(
            signals=case["signals"],
            workflow=case["domain"],
            model_calls=1,
            tokens_estimate=900,
        )

        for policy in POLICIES:
            report = policy.apply(trace)
            ext = report.externalities.model_dump()

            rows.append({
                "case_id": case["id"],
                "domain": case["domain"],
                "collision_type": case["collision_type"],
                "severity": case["severity"],
                "ambiguity": case["ambiguity"],
                "policy": policy.name,
                "expected_mitigation": case["expected_mitigation"],
                "recommended_mitigation": report.recommended_mitigation,
                "correct_mitigation": score_resolution(
                    policy.name,
                    report.recommended_mitigation,
                    case["expected_mitigation"],
                ),
                "care_suppression_risk": ext["care_suppression_risk"],
                "security_risk": ext["security_risk"],
                "accessibility_burden": ext["accessibility_burden"],
                "privacy_exposure": ext["privacy_exposure"],
                "energy_cost": ext["energy_cost"],
            })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rows, indent=2))

    print(f"Wrote {OUT} with {len(rows)} policy-case rows.")

if __name__ == "__main__":
    main()
