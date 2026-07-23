"""Answers "can you show the severity weights were picked before seeing
results?" more rigorously than a git timestamp can.

Git history cannot establish temporal precedence here: SEVERITY_WEIGHTS
and the first correct Xk computation landed in the same commit
(4d109325 / c1e839b, 2026-07-19), so there is no independently-verifiable
artifact separating "weights chosen" from "results observed." Rather than
assert a stronger guarantee than the repository can support, this script
tests the underlying worry directly: does the paper's Xk ranking depend on
having cherry-picked this one specific weight vector, or does it hold
across the whole range of weightings consistent with the paper's stated
normative ordering (care > security > privacy > access > energy)?

Since Xk = sum_i lambda_i * delta_i is linear in lambda for fixed
per-policy per-dimension means, the sign of (Xk_adaptive - Xk_baseline)
is a linear functional of lambda. We sample many lambda vectors uniformly
from the ordering-constrained simplex (Dirichlet(1,1,1,1,1) draws sorted
to enforce the ordering, then mapped back onto the five named dimensions)
and report the fraction of draws under which Adaptive EdgeCase's Xk is
lower than each baseline's, using both the original (pole-based baseline,
undetected=free) and the corrected (action-specific baseline,
undetected=penalized) per-dimension means from the two prior analyses.
"""
import json
from pathlib import Path

import numpy as np

N_DRAWS = 20000
RNG_SEED = 20260722  # distinct from the bootstrap RNG seeds used elsewhere
# Normative-severity order per the paper's stated ranking (care > security >
# privacy > access > energy). NOT metrics.py's internal storage order
# ([care, accessibility, privacy, security, energy]) - that distinction
# matters here because sorted weight draws are assigned by rank, and a
# mismatch against the wrong dimension order would silently swap the
# security/accessibility weights.
DIMENSIONS = ["care_suppression", "security_risk", "privacy_exposure", "accessibility_burden", "energy_score"]
PAPER_WEIGHTS = np.array([0.30, 0.25, 0.20, 0.15, 0.10])  # same DIMENSIONS order as above

OUT_JSON = Path("experiments/results/severity_weight_sensitivity.json")
OUT_MD = Path("experiments/tables/severity_weight_sensitivity.md")

def dim_means(metrics):
    m = {x["metric"]: x["mean"] for x in metrics}
    return {
        "care_suppression": m["avg_care_suppression"],
        "security_risk": m["avg_security_risk"],
        "privacy_exposure": m["avg_privacy_exposure"],
        "accessibility_burden": m["avg_accessibility_burden"],
        "energy_score": m["avg_energy_score"],
    }

def sample_ordered_weights(rng, n):
    # Dirichlet(1,...,1) is uniform over the simplex; sorting descending
    # and assigning to (care, security, privacy, access, energy) enforces
    # the paper's stated ordering care > security > privacy > access >
    # energy on every draw, while leaving the *magnitude* of each gap
    # between adjacent weights free to vary.
    draws = rng.dirichlet(np.ones(5), size=n)
    draws.sort(axis=1)
    draws = draws[:, ::-1]
    return draws

def main():
    orig = json.load(open("experiments/results/statistical_summary.json"))["ci_per_policy"]
    action = json.load(open("experiments/results/rigid_baseline_action_scoring.json"))["ci_per_policy"]
    penalized_metrics = json.load(open("experiments/results/undetected_penalty_analysis.json"))["ci_metrics"]

    adaptive_variants = {
        "original (undetected=free)": dim_means(orig["edgecase_adaptive"]),
        "penalized (undetected=charged real cost)": dim_means(penalized_metrics),
    }
    baseline_variants = {
        "strict_block": {
            "pole-based (original)": dim_means(orig["strict_block"]),
            "action-specific": dim_means(action["strict_block"]),
        },
        "always_escalate": {
            "pole-based (original)": dim_means(orig["always_escalate"]),
            "action-specific": dim_means(action["always_escalate"]),
        },
        "maximum_review": {
            "pole-based (original)": dim_means(orig["maximum_review"]),
            "action-specific": dim_means(action["maximum_review"]),
        },
    }

    rng = np.random.default_rng(RNG_SEED)
    weights = sample_ordered_weights(rng, N_DRAWS)  # (N_DRAWS, 5), columns = DIMENSIONS order

    results = []
    for baseline_name, baseline_scorings in baseline_variants.items():
        for baseline_scoring_name, b_means in baseline_scorings.items():
            b_vec = np.array([b_means[d] for d in DIMENSIONS])
            for adaptive_scoring_name, a_means in adaptive_variants.items():
                a_vec = np.array([a_means[d] for d in DIMENSIONS])
                xk_adaptive = weights @ a_vec
                xk_baseline = weights @ b_vec
                adaptive_wins = np.sum(xk_adaptive < xk_baseline)
                win_rate = float(adaptive_wins) / N_DRAWS
                results.append({
                    "baseline": baseline_name,
                    "baseline_scoring": baseline_scoring_name,
                    "adaptive_scoring": adaptive_scoring_name,
                    "n_draws": N_DRAWS,
                    "adaptive_win_rate": round(win_rate, 4),
                    "paper_reported_weights_result": "adaptive wins" if (
                        PAPER_WEIGHTS @ a_vec < PAPER_WEIGHTS @ b_vec
                    ) else "baseline wins",
                })

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(results, indent=2))

    with OUT_MD.open("w") as f:
        f.write(f"# Severity-weight sensitivity sweep ({N_DRAWS} draws, ordering-constrained simplex)\n\n")
        f.write(
            "Fraction of weight vectors respecting care > security > privacy > access > energy "
            "(the paper's stated normative ordering) under which Adaptive EdgeCase's Xk is lower "
            "than each baseline's, using point-estimate means from the 10-seed evaluation.\n\n"
        )
        f.write("| Baseline | Baseline scoring | Adaptive scoring | Adaptive win rate | Paper's specific weights (0.30/0.15/0.20/0.25/0.10) |\n")
        f.write("| --- | --- | --- | --- | --- |\n")
        for r in results:
            f.write(
                f"| {r['baseline']} | {r['baseline_scoring']} | {r['adaptive_scoring']} | "
                f"{r['adaptive_win_rate']*100:.1f}% | {r['paper_reported_weights_result']} |\n"
            )

    for r in results:
        print(f"{r['baseline']:<18} {r['baseline_scoring']:<24} {r['adaptive_scoring']:<40} win_rate={r['adaptive_win_rate']*100:.1f}%  (paper weights: {r['paper_reported_weights_result']})")
    print(f"\nWrote {OUT_JSON}, {OUT_MD}")

if __name__ == "__main__":
    main()
