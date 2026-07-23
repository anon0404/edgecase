"""Documents the phantom-signal specification bug found and fixed in this
revision: two of build_edgecase_benchmark_v1.py's DOMAINS signal pools
(education, public_benefits) included words that were never registered
triggers for any obligation in registry.py. Discovered as a side effect of
building EdgeCase-Benchmark-v2's within-domain ambiguity variants, whose
verification gate (verify_crossover_resolution()) checks every generated
signal set against the real detect() output before writing any data --
the same check, run retroactively against v1's own generator, is what
surfaced this.

This script regenerates the "before" state from the bug's known signal
pools (frozen here, not re-imported from git history, since the buggy
pools no longer exist in the working tree) to keep the before/after
comparison exact and reproducible, and computes the "after" state from
the current (fixed) generator.
"""
import json
from pathlib import Path

from edgecase.detectors import detect
from edgecase.models import Trace
from edgecase.registry import Registry

from build_edgecase_benchmark_v1 import DEFAULT_SEED, DOMAINS as FIXED_DOMAINS

OUT_JSON = Path("experiments/results/specification_bug_analysis.json")
OUT_MD = Path("experiments/tables/specification_bug_analysis.md")

# Frozen copy of the pre-fix signal pools for education and public_benefits
# (the only two affected domains), for an exact, reproducible before/after
# comparison now that the working tree no longer contains the bug.
BUGGY_POOLS = {
    "education": {
        "signals_a": ["personalization_request", "learning_need", "accommodation_request"],
        "signals_b": ["fairness_risk", "protected_attribute_proxy", "stereotype_risk"],
    },
    "public_benefits": {
        "signals_a": ["sensitive_data", "private_context", "data_minimization_request"],
        "signals_b": ["safeguarding_need", "abuse_disclosure", "coercion"],
    },
}


def _choose_signals(spec):
    import random

    signals = [random.choice(spec["signals_a"]), random.choice(spec["signals_b"])]
    if random.random() < 0.45:
        pool = spec["signals_a"] + spec["signals_b"]
        extra = random.choice(pool)
        if extra not in signals:
            signals.append(extra)
    return signals


def run_full_generation_detection_rate(domains_override, seed=DEFAULT_SEED):
    # Mirrors build_edgecase_benchmark_v1.generate_rows()'s exact iteration
    # order and per-case RNG consumption (domain-by-domain, index-by-index,
    # drawing severity/ambiguity/energy_budget for every case even though
    # this script doesn't use them) so the RNG trajectory - and therefore
    # which exact signals get drawn for the affected domains - matches the
    # real generator exactly, not an approximation.
    import random

    registry = Registry.default()
    random.seed(seed)
    domains = {**FIXED_DOMAINS, **{d: {**FIXED_DOMAINS[d], **domains_override.get(d, {})} for d in domains_override}}

    results = {d: {"total": 0, "detected": 0} for d in domains}
    for domain, spec in domains.items():
        for _ in range(spec["n"]):
            random.uniform(0.35, 1.0)  # severity - consumed, unused here
            random.uniform(0.20, 1.0)  # ambiguity - consumed, unused here
            random.choice(["low", "medium", "high"])  # energy_budget - consumed, unused here
            random.choice(spec["templates"])  # prompt - consumed, unused here
            signals = _choose_signals(spec)
            results[domain]["total"] += 1
            trace = Trace(signals=signals, workflow=domain, model_calls=1, tokens_estimate=900)
            report = detect(trace, registry)
            if report.collision_detected:
                results[domain]["detected"] += 1
    for d in results:
        results[d]["rate"] = round(results[d]["detected"] / results[d]["total"], 4)
    return {d: results[d] for d in BUGGY_POOLS}


def main():
    before = run_full_generation_detection_rate(BUGGY_POOLS)
    after = run_full_generation_detection_rate({})

    all_triggers = set()
    for ob in Registry.default().obligations:
        all_triggers.update(ob.triggers)
    phantom_signals = {
        d: sorted(set(pools["signals_a"] + pools["signals_b"]) - all_triggers)
        for d, pools in BUGGY_POOLS.items()
    }

    result = {"before_fix": before, "after_fix": after, "phantom_signals_removed": phantom_signals}
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=2))

    with OUT_MD.open("w") as f:
        f.write("# Phantom-signal specification bug: before/after\n\n")
        f.write("| Domain | Phantom signals removed | Detection rate before | Detection rate after |\n")
        f.write("| --- | --- | --- | --- |\n")
        for d in BUGGY_POOLS:
            f.write(f"| {d} | {', '.join(phantom_signals[d])} | {before[d]['detected']}/{before[d]['total']} ({before[d]['rate']*100:.1f}%) | {after[d]['detected']}/{after[d]['total']} ({after[d]['rate']*100:.1f}%) |\n")

    print(json.dumps(result, indent=2))
    print(f"Wrote {OUT_JSON}, {OUT_MD}")


if __name__ == "__main__":
    main()
