import json
from pathlib import Path

from edgecase.detectors import INCOMPATIBLE_ACTIONS
from edgecase.models import Trace
from edgecase.policies import (
    StrictBlockPolicy,
    EscalationPolicy,
    VerificationPolicy,
    MaximumReviewPolicy,
    AdaptiveEdgeCasePolicy,
)

DATA = Path("datasets/edgecase_benchmark_v1.jsonl")
OUT = Path("experiments/results/full_evaluation.json")

POLICIES = [
    StrictBlockPolicy(),
    EscalationPolicy(),
    VerificationPolicy(),
    MaximumReviewPolicy(),
    AdaptiveEdgeCasePolicy(),
]

# A rigid policy's single fixed action is never one of the compound reference
# mitigations (e.g. "constrain_and_escalate"), so exact-match scoring alone
# always gives it 0. Give partial credit when its fixed action is at least
# one of the two obligation actions actually in tension for this case (e.g.
# always_escalate's "escalate" against block_vs_escalate's expected
# "constrain_and_escalate") - it got half of the compound answer right, as
# opposed to a case where its fixed action addresses neither side at all.
RIGID_ACTIONS = {
    "strict_block": "block",
    "always_escalate": "escalate",
    "always_verify": "verify",
    "maximum_review": "increase_review",
}

def score_resolution(policy_name, mitigation, expected, collision_type):
    if mitigation == expected:
        return 1.0

    fixed_action = RIGID_ACTIONS.get(policy_name)
    if fixed_action is None:
        return 0.0

    for action_pair, (c_type, _) in INCOMPATIBLE_ACTIONS.items():
        if c_type == collision_type and fixed_action in action_pair:
            return 0.5

    return 0.0

def evaluate_cases(cases: list[dict], policies=None) -> list[dict]:
    policies = policies if policies is not None else POLICIES
    rows = []

    for case in cases:
        trace = Trace(
            signals=case["signals"],
            workflow=case["domain"],
            model_calls=1,
            tokens_estimate=900,
        )

        for policy in policies:
            report = policy.apply(trace)
            ext = report.externalities.model_dump()

            rows.append({
                "case_id": case["id"],
                "domain": case["domain"],
                "collision_type": case["collision"],
                "severity": case["severity"],
                "ambiguity": case["ambiguity"],
                "policy": policy.name,
                "expected_mitigation": case["expected_mitigation"],
                "recommended_mitigation": report.recommended_mitigation,
                "mitigation_score": score_resolution(
                    policy.name,
                    report.recommended_mitigation,
                    case["expected_mitigation"],
                    case["collision"],
                ),
                "care_suppression_risk": ext["care_suppression_risk"],
                "security_risk": ext["security_risk"],
                "accessibility_burden": ext["accessibility_burden"],
                "privacy_exposure": ext["privacy_exposure"],
                "energy_cost": ext["energy_cost"],
            })

    return rows

def main():
    cases = [
        json.loads(line)
        for line in DATA.read_text().splitlines()
        if line.strip()
    ]

    rows = evaluate_cases(cases)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rows, indent=2))

    print(f"Wrote {OUT} with {len(rows)} policy-case rows.")

if __name__ == "__main__":
    main()
