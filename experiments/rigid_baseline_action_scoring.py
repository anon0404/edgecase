"""Action-specific (non-pole) externality re-scoring for the three rigid
baselines still in Table 1 (Strict Block, Always Escalate, Maximum Review).

The current `policies/rigid.py` scores a rigid policy's externalities by
which *pole* (restrictive/supportive) it occupies relative to whichever
obligation a case triggers, uniformly across all seven collision types.
That means Strict Block, Always Verify, and Maximum Review -- three
different fixed actions -- produce byte-identical externality profiles on
every dimension except energy cost, since the pole assignment (all three
are "restrictive") never depends on the policy's actual action or on
which specific collision type the case belongs to.

This script re-scores the same benchmark rows using an action-specific
rule instead: for each case, take its true collision type and the two
obligation actions actually in tension (INCOMPATIBLE_ACTIONS). If a rigid
policy's fixed action is one of those two actions, it addresses one side
of the real tension, so the case's real (collision-specific) externality
profile -- the same `_score_externalities(collision_type, trace)` used
for Adaptive EdgeCase and the Oracle -- is halved (0.5x, the same partial-
credit convention already used for mitigation_score). If the fixed action
addresses neither side, the policy incurs the FULL collision-specific
externality, on the grounds that an action irrelevant to the actual
tension leaves it exactly as unmanaged as a fully undetected collision.

This makes the four rigid policies differentiate by which collision types
their fixed action happens to be relevant to (Strict Block only on
block_vs_escalate; Always Escalate only on block_vs_escalate; Always
Verify only on verify_vs_accessibility; Maximum Review on both
privacy_vs_safeguarding and safety_vs_energy), rather than by a single
policy-wide restrictive/supportive label applied to all seven types
uniformly.
"""
import json
from pathlib import Path

import numpy as np

from build_edgecase_benchmark_v1 import generate_rows
from run_full_evaluation import RIGID_ACTIONS, score_resolution
from run_multi_seed_evaluation import SEEDS, BOOTSTRAP_RNG_SEED, bootstrap_metrics_for_policy
from edgecase.detectors import INCOMPATIBLE_ACTIONS, _score_externalities
from edgecase.models import Trace

ENERGY_COST = {
    "strict_block": "low",
    "always_escalate": "medium",
    "always_verify": "medium",
    "maximum_review": "high",
}

ADDRESSES = {
    policy: {
        c_type for pair, (c_type, _mitigation) in INCOMPATIBLE_ACTIONS.items()
        if fixed_action in pair
    }
    for policy, fixed_action in RIGID_ACTIONS.items()
}

OUT_JSON = Path("experiments/results/rigid_baseline_action_scoring.json")
OUT_MD = Path("experiments/tables/rigid_baseline_action_scoring.md")

def score_case(policy_name, case):
    collision_type = case["collision"]
    fixed_action = RIGID_ACTIONS[policy_name]
    trace = Trace(signals=case["signals"], workflow=case["domain"], model_calls=1, tokens_estimate=900)
    full = _score_externalities(collision_type, trace).model_dump()

    addresses_one_side = collision_type in ADDRESSES[policy_name]
    scale = 0.5 if addresses_one_side else 1.0

    return {
        "care_suppression_risk": round(full["care_suppression_risk"] * scale, 6),
        "security_risk": round(full["security_risk"] * scale, 6),
        "accessibility_burden": round(full["accessibility_burden"] * scale, 6),
        "privacy_exposure": round(full["privacy_exposure"] * scale, 6),
        "energy_cost": ENERGY_COST[policy_name],
        "mitigation_score": score_resolution(policy_name, fixed_action, case["expected_mitigation"], collision_type),
        "addresses_one_side": addresses_one_side,
    }

def main():
    all_rows = []
    for seed in SEEDS:
        cases = generate_rows(seed)
        for policy_name in RIGID_ACTIONS:
            for case in cases:
                scored = score_case(policy_name, case)
                all_rows.append({
                    "seed": seed,
                    "case_id": case["id"],
                    "policy": policy_name,
                    **scored,
                })

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    Path("experiments/results/rigid_baseline_action_scoring_rows.json").write_text(json.dumps(all_rows, indent=2))

    rng = np.random.default_rng(BOOTSTRAP_RNG_SEED)
    ci_results = {}
    for policy_name in RIGID_ACTIONS:
        rows_for_policy = [r for r in all_rows if r["policy"] == policy_name]
        ci_results[policy_name] = bootstrap_metrics_for_policy(rows_for_policy, rng)

    addressed_fraction = {
        policy_name: round(
            sum(1 for r in all_rows if r["policy"] == policy_name and r["addresses_one_side"])
            / sum(1 for r in all_rows if r["policy"] == policy_name),
            4,
        )
        for policy_name in RIGID_ACTIONS
    }

    result = {
        "seeds": SEEDS,
        "n_bootstrap": 10000,
        "scoring": "action-specific: fixed action vs true collision-type action pair, 0.5x scale if addressed, 1.0x if not",
        "fraction_of_cases_addressed_one_side": addressed_fraction,
        "ci_per_policy": ci_results,
    }
    OUT_JSON.write_text(json.dumps(result, indent=2))

    with OUT_MD.open("w") as f:
        f.write("# Rigid baseline externality re-scoring: action-specific vs. pole-based\n\n")
        f.write(
            "Same 10-seed benchmark rows as Table 1, but rigid-baseline externalities "
            "are scored by whether the policy's fixed action actually addresses one side "
            "of the case's real collision (0.5x the collision-specific externality) or "
            "neither side (1.0x, same as an unresolved collision), instead of by a "
            "policy-wide restrictive/supportive pole.\n\n"
        )
        f.write("| Policy | Fraction addressing one side | Metric | Mean | 95% CI |\n")
        f.write("| --- | --- | --- | --- | --- |\n")
        for policy_name, metrics in ci_results.items():
            for m in metrics:
                f.write(
                    f"| {policy_name} | {addressed_fraction[policy_name]} | {m['metric']} | "
                    f"{m['mean']} | [{m['ci_lower_95']}, {m['ci_upper_95']}] |\n"
                )

    print(json.dumps(result, indent=2, default=str)[:3000])
    print(f"Wrote {OUT_JSON}, {OUT_MD}")

if __name__ == "__main__":
    main()
