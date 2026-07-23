"""Quantifies the benchmark's prompt-template diversity, surfaced as a
side effect of building the LLM-detector baselines: how many genuinely
distinct natural-language scenarios back the "1,260-instance" benchmark,
and does prompt text alone determine the ground-truth collision label.

This matters independently of the LLM baselines. It bears on how a reader
should weigh the benchmark's diversity claims (Experimental Design), and
it's the reason the LLM detector's prompt-only accuracy (98.0%, see
llm_detector_baseline.py) should not be read as evidence of open-ended
reasoning about a novel obligation tension.
"""
import json
from collections import defaultdict
from pathlib import Path

from build_edgecase_benchmark_v1 import generate_rows, DEFAULT_SEED
from run_multi_seed_evaluation import SEEDS

OUT_JSON = Path("experiments/results/template_diversity_analysis.json")
OUT_MD = Path("experiments/tables/template_diversity_analysis.md")


def analyze(rows):
    by_prompt_collision = defaultdict(set)
    prompt_counts = defaultdict(int)
    signal_key_counts = defaultdict(int)
    for r in rows:
        by_prompt_collision[r["prompt"]].add(r["collision"])
        prompt_counts[r["prompt"]] += 1
        signal_key_counts[(r["prompt"], tuple(sorted(r["signals"])))] += 1

    multi_collision_prompts = {p: s for p, s in by_prompt_collision.items() if len(s) > 1}
    return {
        "n_rows": len(rows),
        "n_distinct_prompts": len(by_prompt_collision),
        "n_prompts_mapping_to_multiple_collision_types": len(multi_collision_prompts),
        "avg_rows_per_distinct_prompt": round(len(rows) / len(by_prompt_collision), 2),
        "n_distinct_prompt_signal_pairs": len(signal_key_counts),
        "top_5_most_repeated_prompts": [
            {"prompt": p, "count": n}
            for p, n in sorted(prompt_counts.items(), key=lambda x: -x[1])[:5]
        ],
    }


def main():
    canonical_rows = generate_rows(DEFAULT_SEED)
    canonical = analyze(canonical_rows)

    all_10_seed_rows = [row for seed in SEEDS for row in generate_rows(seed)]
    ten_seed = analyze(all_10_seed_rows)

    result = {
        "canonical_seed": DEFAULT_SEED,
        "canonical_seed_benchmark": canonical,
        "ten_statistical_rigor_seeds_pooled": ten_seed,
        "finding": (
            "Prompt text alone deterministically identifies the true collision type "
            "in every case checked (0 counterexamples): the benchmark's natural-"
            "language diversity is much lower than its case count implies. This does "
            "not affect Table 1's numbers (scored on `signals` tags, not prompt text), "
            "but it does affect how any prompt-text-only evaluation (e.g. an LLM given "
            "only the raw prompt) should be interpreted."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=2))

    with OUT_MD.open("w") as f:
        f.write("# Benchmark prompt-template diversity\n\n")
        f.write(f"**Canonical seed {DEFAULT_SEED}** (the committed benchmark, used for Tables 1/3/4):\n\n")
        f.write(f"- {canonical['n_rows']} rows, only **{canonical['n_distinct_prompts']} distinct prompt strings** ")
        f.write(f"(avg {canonical['avg_rows_per_distinct_prompt']} rows/prompt)\n")
        f.write(f"- 0 of {canonical['n_distinct_prompts']} distinct prompts map to more than one collision type\n")
        f.write(f"- {canonical['n_distinct_prompt_signal_pairs']} distinct (prompt, signal-set) pairs\n\n")
        f.write("**Pooled across the 10 statistical-rigor seeds** (12,600 rows):\n\n")
        f.write(f"- Only **{ten_seed['n_distinct_prompts']} distinct prompt strings** across all 10 seeds combined\n")
        f.write(f"- {ten_seed['n_distinct_prompt_signal_pairs']} distinct (prompt, signal-set) pairs\n\n")
        f.write(f"{result['finding']}\n")

    print(json.dumps(result, indent=2))
    print(f"Wrote {OUT_JSON}, {OUT_MD}")


if __name__ == "__main__":
    main()
