"""Resolves the paper's bracketed uncertainty note: is Adaptive EdgeCase's
aggregate externality advantage over Strict Block real, or partly an
artifact of undetected collisions silently scoring zero externality
(_score_externalities's fallback `return Externalities()`)?

For each of Adaptive EdgeCase's cases across the 10 statistical-rigor
seeds, if detect() failed to find the collision, this substitutes the
case's TRUE collision type's real externality profile
(_score_externalities(case["collision"], trace)) for the zero default --
i.e. an undetected collision is charged exactly as much externality as a
detected-but-completely-unmanaged one, rather than nothing. This uses the
benchmark's ground-truth label, which the detector itself never sees; it
answers "what would Adaptive EdgeCase's own reported number look like if
we, the evaluators, refused to let a detection failure count as free,"
not a claim about what the detector could do differently.
"""
import json
from pathlib import Path

import numpy as np

from build_edgecase_benchmark_v1 import generate_rows
from run_full_evaluation import score_resolution
from run_multi_seed_evaluation import SEEDS, BOOTSTRAP_RNG_SEED, bootstrap_metrics_for_policy
from edgecase.detectors import detect, _score_externalities
from edgecase.models import Trace
from edgecase.registry import Registry

OUT_JSON = Path("experiments/results/undetected_penalty_analysis.json")
OUT_MD = Path("experiments/tables/undetected_penalty_analysis.md")

def main():
    registry = Registry.default()
    all_rows = []
    n_undetected = 0
    n_total = 0

    for seed in SEEDS:
        cases = generate_rows(seed)
        for case in cases:
            trace = Trace(signals=case["signals"], workflow=case["domain"], model_calls=1, tokens_estimate=900)
            report = detect(trace, registry)
            n_total += 1

            if report.collision_detected:
                ext = report.externalities.model_dump()
            else:
                n_undetected += 1
                ext = _score_externalities(case["collision"], trace).model_dump()

            all_rows.append({
                "seed": seed,
                "case_id": case["id"],
                "policy": "edgecase_adaptive_penalized",
                "mitigation_score": score_resolution(
                    "edgecase_adaptive", report.recommended_mitigation, case["expected_mitigation"], case["collision"]
                ),
                "care_suppression_risk": ext["care_suppression_risk"],
                "security_risk": ext["security_risk"],
                "accessibility_burden": ext["accessibility_burden"],
                "privacy_exposure": ext["privacy_exposure"],
                "energy_cost": ext["energy_cost"],
            })

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    Path("experiments/results/undetected_penalty_analysis_rows.json").write_text(json.dumps(all_rows, indent=2))

    rng = np.random.default_rng(BOOTSTRAP_RNG_SEED)
    ci_metrics = bootstrap_metrics_for_policy(all_rows, rng)

    result = {
        "seeds": SEEDS,
        "n_total_cases": n_total,
        "n_undetected": n_undetected,
        "undetected_fraction": round(n_undetected / n_total, 4),
        "scoring": "undetected collisions charged the true collision type's real externality profile instead of the zero default",
        "ci_metrics": ci_metrics,
    }
    OUT_JSON.write_text(json.dumps(result, indent=2))

    with OUT_MD.open("w") as f:
        f.write("# Adaptive EdgeCase externality under a nonzero undetected-collision penalty\n\n")
        f.write(
            f"{n_undetected} of {n_total} cases ({result['undetected_fraction']*100:.1f}%) across 10 seeds "
            "went undetected by Adaptive EdgeCase and were re-scored with the true collision type's real "
            "externality profile instead of the zero default `_score_externalities` currently falls through to.\n\n"
        )
        f.write("| Metric | Mean | 95% CI |\n| --- | --- | --- |\n")
        for m in ci_metrics:
            f.write(f"| {m['metric']} | {m['mean']} | [{m['ci_lower_95']}, {m['ci_upper_95']}] |\n")

    print(json.dumps(result, indent=2))
    print(f"Wrote {OUT_JSON}, {OUT_MD}")

if __name__ == "__main__":
    main()
