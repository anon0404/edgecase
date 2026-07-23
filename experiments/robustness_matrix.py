"""Combines rigid_baseline_action_scoring.py and undetected_penalty_analysis.py
into a single robustness matrix for Adaptive EdgeCase's aggregate severity-
weighted externality (Xk) claim against each of the three Table 1 baselines,
under all four combinations of:
  - rigid-baseline scoring: original (pole-based) vs. action-specific
  - Adaptive EdgeCase scoring: original (undetected = free) vs. penalized
    (undetected = charged the true collision type's real externality)

A policy "wins" only when its 95% CI does not overlap the comparison
policy's -- ties/overlaps are reported as such, not resolved by point
estimate alone, consistent with how Table 1's own CIs are read elsewhere
in this paper.
"""
import json
from pathlib import Path

OUT_JSON = Path("experiments/results/robustness_matrix.json")
OUT_MD = Path("experiments/tables/robustness_matrix.md")

def load_xk(path, key_path):
    d = json.load(open(path))
    for k in key_path:
        d = d[k]
    return next(m for m in d if m["metric"] == "governance_externality")

def verdict(adaptive_ci, baseline_ci):
    a_lo, a_hi = adaptive_ci
    b_lo, b_hi = baseline_ci
    if a_hi < b_lo:
        return "Adaptive EdgeCase wins (lower Xk, non-overlapping)"
    if b_hi < a_lo:
        return "Baseline wins (lower Xk, non-overlapping)"
    return "No significant difference (CIs overlap)"

def main():
    orig = json.load(open("experiments/results/statistical_summary.json"))["ci_per_policy"]
    action = json.load(open("experiments/results/rigid_baseline_action_scoring.json"))["ci_per_policy"]
    penalized = json.load(open("experiments/results/undetected_penalty_analysis.json"))["ci_metrics"]

    def m(metrics):
        return next(x for x in metrics if x["metric"] == "governance_externality")

    adaptive_variants = {
        "original (undetected=free)": m(orig["edgecase_adaptive"]),
        "penalized (undetected=charged real cost)": m(penalized),
    }
    baseline_variants = {
        "strict_block": {
            "pole-based (original)": m(orig["strict_block"]),
            "action-specific": m(action["strict_block"]),
        },
        "always_escalate": {
            "pole-based (original)": m(orig["always_escalate"]),
            "action-specific": m(action["always_escalate"]),
        },
        "maximum_review": {
            "pole-based (original)": m(orig["maximum_review"]),
            "action-specific": m(action["maximum_review"]),
        },
    }

    matrix = []
    for baseline_name, baseline_scorings in baseline_variants.items():
        for baseline_scoring_name, b in baseline_scorings.items():
            for adaptive_scoring_name, a in adaptive_variants.items():
                v = verdict(
                    (a["ci_lower_95"], a["ci_upper_95"]),
                    (b["ci_lower_95"], b["ci_upper_95"]),
                )
                matrix.append({
                    "baseline": baseline_name,
                    "baseline_scoring": baseline_scoring_name,
                    "baseline_xk": b["mean"],
                    "baseline_ci": [b["ci_lower_95"], b["ci_upper_95"]],
                    "adaptive_scoring": adaptive_scoring_name,
                    "adaptive_xk": a["mean"],
                    "adaptive_ci": [a["ci_lower_95"], a["ci_upper_95"]],
                    "verdict": v,
                })

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(matrix, indent=2))

    with OUT_MD.open("w") as f:
        f.write("# Robustness matrix: Adaptive EdgeCase vs. each baseline on aggregate severity-weighted Xk\n\n")
        f.write("| Baseline | Baseline scoring | Baseline Xk | Adaptive scoring | Adaptive Xk | Verdict |\n")
        f.write("| --- | --- | --- | --- | --- | --- |\n")
        for row in matrix:
            f.write(
                f"| {row['baseline']} | {row['baseline_scoring']} | {row['baseline_xk']} [{row['baseline_ci'][0]},{row['baseline_ci'][1]}] | "
                f"{row['adaptive_scoring']} | {row['adaptive_xk']} [{row['adaptive_ci'][0]},{row['adaptive_ci'][1]}] | {row['verdict']} |\n"
            )

    for row in matrix:
        print(f"{row['baseline']:<18} {row['baseline_scoring']:<28} vs {row['adaptive_scoring']:<40} -> {row['verdict']}")
    print(f"\nWrote {OUT_JSON}, {OUT_MD}")

if __name__ == "__main__":
    main()
