import json
from pathlib import Path

import numpy as np
from scipy.stats import wilcoxon

from build_edgecase_benchmark_v1 import generate_rows
from run_full_evaluation import POLICIES, evaluate_cases
from edgecase.metrics import SEVERITY_WEIGHTS, aggregate_governance_externality

# Seeds are a fresh set, not overlapping with the canonical benchmark seed
# (404, used everywhere else in the repo/paper) - this run characterizes
# variance under the benchmark's generative randomness, it does not
# replace the canonical dataset.
SEEDS = list(range(1, 11))
N_BOOTSTRAP = 10000
BOOTSTRAP_CHUNK = 500
BOOTSTRAP_RNG_SEED = 12345  # separate from benchmark-generation seeds above

ENERGY_SCORE = {"low": 0.2, "medium": 0.5, "high": 0.9}
BASELINE_POLICIES = ["strict_block", "always_escalate", "maximum_review"]
ADAPTIVE_POLICY = "edgecase_adaptive"

OUT_JSON = Path("experiments/results/statistical_summary.json")
OUT_ROWS = Path("experiments/results/multi_seed_per_case.json")
OUT_MD = Path("experiments/tables/statistical_summary.md")

def collect_all_rows():
    all_rows = []
    for seed in SEEDS:
        cases = generate_rows(seed)
        for row in evaluate_cases(cases):
            row = dict(row)
            row["seed"] = seed
            all_rows.append(row)
    return all_rows

def bootstrap_means(values, rng, n_boot=N_BOOTSTRAP, chunk_size=BOOTSTRAP_CHUNK):
    # Chunked to bound memory: a single (n_boot x n) index matrix for
    # n~12,600 rows/policy and n_boot=10,000 would be ~1GB per array.
    n = len(values)
    boot_means = np.empty(n_boot)
    done = 0
    while done < n_boot:
        batch = min(chunk_size, n_boot - done)
        idx = rng.integers(0, n, size=(batch, n))
        boot_means[done:done + batch] = values[idx].mean(axis=1)
        done += batch
    return boot_means

def bootstrap_metrics_for_policy(rows_for_policy, rng):
    n = len(rows_for_policy)
    mitigation = np.array([r["mitigation_score"] for r in rows_for_policy])
    care = np.array([r["care_suppression_risk"] for r in rows_for_policy])
    security = np.array([r["security_risk"] for r in rows_for_policy])
    access = np.array([r["accessibility_burden"] for r in rows_for_policy])
    privacy = np.array([r["privacy_exposure"] for r in rows_for_policy])
    energy = np.array([ENERGY_SCORE[r["energy_cost"]] for r in rows_for_policy])

    # One consistent set of resample indices per chunk, applied to all six
    # raw arrays together, so governance_externality can be derived from
    # each bootstrap draw's own resampled dimension means rather than
    # computed independently per dimension (which would break the pairing
    # a single resample implies).
    boot_mitigation = np.empty(N_BOOTSTRAP)
    boot_care = np.empty(N_BOOTSTRAP)
    boot_security = np.empty(N_BOOTSTRAP)
    boot_access = np.empty(N_BOOTSTRAP)
    boot_privacy = np.empty(N_BOOTSTRAP)
    boot_energy = np.empty(N_BOOTSTRAP)

    done = 0
    while done < N_BOOTSTRAP:
        batch = min(BOOTSTRAP_CHUNK, N_BOOTSTRAP - done)
        idx = rng.integers(0, n, size=(batch, n))
        boot_mitigation[done:done + batch] = mitigation[idx].mean(axis=1)
        boot_care[done:done + batch] = care[idx].mean(axis=1)
        boot_security[done:done + batch] = security[idx].mean(axis=1)
        boot_access[done:done + batch] = access[idx].mean(axis=1)
        boot_privacy[done:done + batch] = privacy[idx].mean(axis=1)
        boot_energy[done:done + batch] = energy[idx].mean(axis=1)
        done += batch

    boot_xk = np.array([
        aggregate_governance_externality(
            care_suppression=c, accessibility_burden=a, privacy_exposure=p,
            security_risk=s, energy_score=e, weights=SEVERITY_WEIGHTS,
        )
        for c, a, p, s, e in zip(boot_care, boot_access, boot_privacy, boot_security, boot_energy)
    ])

    def summarize(name, observed, boot):
        lo, hi = np.percentile(boot, [2.5, 97.5])
        return {
            "metric": name,
            "mean": round(float(observed), 4),
            "ci_lower_95": round(float(lo), 4),
            "ci_upper_95": round(float(hi), 4),
        }

    return [
        summarize("mitigation_accuracy", mitigation.mean(), boot_mitigation),
        summarize("avg_care_suppression", care.mean(), boot_care),
        summarize("avg_security_risk", security.mean(), boot_security),
        summarize("avg_accessibility_burden", access.mean(), boot_access),
        summarize("avg_privacy_exposure", privacy.mean(), boot_privacy),
        summarize("avg_energy_score", energy.mean(), boot_energy),
        summarize("governance_externality", aggregate_governance_externality(
            care_suppression=care.mean(), accessibility_burden=access.mean(),
            privacy_exposure=privacy.mean(), security_risk=security.mean(),
            energy_score=energy.mean(), weights=SEVERITY_WEIGHTS,
        ), boot_xk),
    ]

def wilcoxon_vs_adaptive(all_rows):
    by_policy = {}
    for row in all_rows:
        by_policy.setdefault(row["policy"], {})[(row["seed"], row["case_id"])] = row["mitigation_score"]

    adaptive_by_key = by_policy[ADAPTIVE_POLICY]

    results = {}
    for baseline in BASELINE_POLICIES:
        baseline_by_key = by_policy[baseline]
        keys = sorted(set(adaptive_by_key) & set(baseline_by_key))
        adaptive_vals = np.array([adaptive_by_key[k] for k in keys])
        baseline_vals = np.array([baseline_by_key[k] for k in keys])
        diffs = adaptive_vals - baseline_vals
        n_nonzero = int(np.sum(diffs != 0))

        if n_nonzero == 0:
            results[baseline] = {
                "n_pairs": len(keys),
                "n_nonzero_diffs": 0,
                "statistic": None,
                "p_value": None,
                "note": "All paired differences are zero; the Wilcoxon signed-rank test is undefined.",
            }
            continue

        statistic, p_value = wilcoxon(adaptive_vals, baseline_vals)
        results[baseline] = {
            "n_pairs": len(keys),
            "n_nonzero_diffs": n_nonzero,
            "mean_diff_adaptive_minus_baseline": round(float(diffs.mean()), 4),
            "statistic": round(float(statistic), 4),
            "p_value": float(p_value),
        }

    return results

def main():
    print(f"Generating and evaluating {len(SEEDS)} benchmark seeds ({SEEDS})...")
    all_rows = collect_all_rows()

    OUT_ROWS.parent.mkdir(parents=True, exist_ok=True)
    OUT_ROWS.write_text(json.dumps(all_rows, indent=2))
    print(f"Wrote {OUT_ROWS} with {len(all_rows)} (seed x case x policy) rows")

    rng = np.random.default_rng(BOOTSTRAP_RNG_SEED)

    ci_results = {}
    for policy in POLICIES:
        rows_for_policy = [r for r in all_rows if r["policy"] == policy.name]
        ci_results[policy.name] = bootstrap_metrics_for_policy(rows_for_policy, rng)

    wilcoxon_results = wilcoxon_vs_adaptive(all_rows)

    n_cases_per_seed = len(all_rows) // (len(SEEDS) * len(POLICIES))
    result = {
        "seeds": SEEDS,
        "cases_per_seed": n_cases_per_seed,
        "n_bootstrap": N_BOOTSTRAP,
        "ci_per_policy": ci_results,
        "wilcoxon_vs_adaptive_on_mitigation_score": wilcoxon_results,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=2))

    with OUT_MD.open("w") as f:
        f.write(f"# Statistical summary ({len(SEEDS)} seeds, {N_BOOTSTRAP} bootstrap resamples)\n\n")
        f.write("## Mean ± bootstrap 95% CI per policy\n\n")
        f.write("| Policy | Metric | Mean | 95% CI |\n")
        f.write("| --- | --- | --- | --- |\n")
        for policy_name, metrics in ci_results.items():
            for m in metrics:
                f.write(f"| {policy_name} | {m['metric']} | {m['mean']} | [{m['ci_lower_95']}, {m['ci_upper_95']}] |\n")
        f.write("\n## Paired Wilcoxon signed-rank test: Adaptive EdgeCase vs. each baseline, mitigation_score\n\n")
        f.write("Matched by (seed, case_id) - same benchmark instance, both policies.\n\n")
        f.write("| Baseline | n pairs | n nonzero diffs | Mean diff (adaptive - baseline) | Statistic | p-value |\n")
        f.write("| --- | --- | --- | --- | --- | --- |\n")
        for baseline, r in wilcoxon_results.items():
            if r["statistic"] is None:
                f.write(f"| {baseline} | {r['n_pairs']} | 0 | - | - | undefined (all diffs zero) |\n")
            else:
                f.write(f"| {baseline} | {r['n_pairs']} | {r['n_nonzero_diffs']} | {r['mean_diff_adaptive_minus_baseline']} | {r['statistic']} | {r['p_value']:.3e} |\n")

    print(f"Wrote {OUT_JSON}, {OUT_MD}")

if __name__ == "__main__":
    main()
