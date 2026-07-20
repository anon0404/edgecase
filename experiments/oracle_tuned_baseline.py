import json
from collections import defaultdict
from pathlib import Path
from statistics import mean

import numpy as np

from build_edgecase_benchmark_v1 import generate_rows
from run_full_evaluation import score_resolution
from run_multi_seed_evaluation import (
    SEEDS,
    BOOTSTRAP_RNG_SEED,
    bootstrap_metrics_for_policy,
)
from edgecase.detectors import INCOMPATIBLE_ACTIONS, _score_externalities
from edgecase.models import Trace

# Oracle-tuned fixed: for each collision type, the single fixed mitigation
# string that maximizes score on that type's train-split cases, evaluated
# on the held-out test split using the true collision type (ground truth,
# not detected) to select which fixed answer to apply. This is not a
# detection baseline - it isolates whether mitigation *selection* is hard
# once the collision type is already known, as a ceiling against which to
# read Adaptive EdgeCase's own detection-limited accuracy.
POLICY_NAME = "oracle_tuned_fixed"

ALL_MITIGATION_STRINGS = sorted({info[1] for info in INCOMPATIBLE_ACTIONS.values()})
COLLISION_TYPES = sorted({info[0] for info in INCOMPATIBLE_ACTIONS.values()})

OUT_ROWS = Path("experiments/results/oracle_tuned_baseline_rows.json")
OUT_JSON = Path("experiments/results/oracle_tuned_baseline.json")
OUT_MD = Path("experiments/tables/oracle_tuned_baseline.md")

def split_rows(rows):
    # Matches build_edgecase_benchmark_v1.main()'s own 70/15/15 split logic
    # exactly, applied here to each seed's regenerated (already-shuffled)
    # row list rather than the on-disk canonical-seed splits.
    n = len(rows)
    train = rows[: int(0.7 * n)]
    test = rows[int(0.85 * n):]
    return train, test

def tune_best_action_per_type(train_cases):
    by_type = defaultdict(list)
    for case in train_cases:
        by_type[case["collision"]].append(case)

    best_action_per_type = {}
    for ctype in COLLISION_TYPES:
        type_cases = by_type[ctype]
        action_means = {}
        for candidate in ALL_MITIGATION_STRINGS:
            scores = [
                score_resolution(POLICY_NAME, candidate, c["expected_mitigation"], c["collision"])
                for c in type_cases
            ]
            action_means[candidate] = mean(scores) if scores else 0.0
        best_action_per_type[ctype] = max(action_means, key=action_means.get)
    return best_action_per_type

def evaluate_seed(seed):
    rows = generate_rows(seed)
    train_cases, test_cases = split_rows(rows)
    best_action_per_type = tune_best_action_per_type(train_cases)

    rows_out = []
    for case in test_cases:
        ctype = case["collision"]
        chosen = best_action_per_type[ctype]
        mitigation_score = score_resolution(POLICY_NAME, chosen, case["expected_mitigation"], ctype)

        trace = Trace(signals=case["signals"], workflow=case["domain"], model_calls=1, tokens_estimate=900)
        ext = _score_externalities(ctype, trace).model_dump()

        rows_out.append({
            "case_id": case["id"],
            "seed": seed,
            "policy": POLICY_NAME,
            "chosen_mitigation": chosen,
            "expected_mitigation": case["expected_mitigation"],
            "mitigation_score": mitigation_score,
            "care_suppression_risk": ext["care_suppression_risk"],
            "security_risk": ext["security_risk"],
            "accessibility_burden": ext["accessibility_burden"],
            "privacy_exposure": ext["privacy_exposure"],
            "energy_cost": ext["energy_cost"],
        })
    return rows_out, best_action_per_type

def main():
    all_rows = []
    tuning_by_seed = {}
    for seed in SEEDS:
        rows, best_action_per_type = evaluate_seed(seed)
        all_rows.extend(rows)
        tuning_by_seed[seed] = best_action_per_type

    OUT_ROWS.parent.mkdir(parents=True, exist_ok=True)
    OUT_ROWS.write_text(json.dumps(all_rows, indent=2))
    print(f"Wrote {OUT_ROWS} with {len(all_rows)} (seed x test case) rows")

    # Sanity check surfaced directly, not just asserted: does the tuned
    # choice match the benchmark's own known-correct per-type mitigation on
    # every seed, or did the search ever land on something else?
    known_correct = {info[0]: info[1] for info in INCOMPATIBLE_ACTIONS.values()}
    mismatches = {
        seed: {c: chosen for c, chosen in tuning.items() if chosen != known_correct[c]}
        for seed, tuning in tuning_by_seed.items()
    }
    mismatches = {seed: m for seed, m in mismatches.items() if m}

    rng = np.random.default_rng(BOOTSTRAP_RNG_SEED)
    ci_metrics = bootstrap_metrics_for_policy(all_rows, rng)

    result = {
        "policy": POLICY_NAME,
        "seeds": SEEDS,
        "n_test_cases_total": len(all_rows),
        "tuning_mismatches_vs_known_correct_mapping": mismatches,
        "ci_metrics": ci_metrics,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=2))

    with OUT_MD.open("w") as f:
        f.write(f"# Oracle-tuned fixed baseline ({len(SEEDS)} seeds, train-tuned/test-evaluated)\n\n")
        f.write(
            "Per collision type, the single fixed mitigation string that maximizes "
            "score on that type's train-split cases, evaluated on the held-out test "
            "split using the true collision type to select which fixed answer to "
            "apply. Isolates whether mitigation selection is hard once the collision "
            "type is already known - a ceiling reading for Adaptive EdgeCase's own "
            "detection-limited accuracy, not a detection baseline itself.\n\n"
        )
        f.write("| Metric | Mean | 95% CI |\n| --- | --- | --- |\n")
        for m in ci_metrics:
            f.write(f"| {m['metric']} | {m['mean']} | [{m['ci_lower_95']}, {m['ci_upper_95']}] |\n")
        f.write(f"\nTuning mismatches vs. the benchmark's own known-correct per-type mapping: {mismatches}\n")

    print(json.dumps(result, indent=2))
    print(f"Wrote {OUT_JSON}, {OUT_MD}")

if __name__ == "__main__":
    main()
