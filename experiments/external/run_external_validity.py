import json
from collections import defaultdict
from pathlib import Path

from huggingface_hub import hf_hub_download

from edgecase.detectors import detect
from edgecase.models import Trace
from edgecase.registry import Registry
from label_mapping import map_agentharm_case, map_safetybench_case

OUT_JSON = Path("experiments/results/external_validity.json")
OUT_MD = Path("experiments/tables/external_validity_summary.md")

# IMPORTANT (see label_mapping.py header for full context): mapping goes
# from each case's own ground-truth external label directly to an EdgeCase
# signal already known to be a registered trigger for some obligation. This
# means "does the mapped obligation fire" is close to tautological - a
# direct-lookup mapping onto a known trigger will always fire, by
# construction of set intersection in Registry.triggered_by(). It is
# reported below for completeness, but should not be read as evidence that
# EdgeCase can independently recognize these harm categories from raw
# prompt text; no text classifier is built or tested here. What IS a
# genuine, non-tautological check on out-of-distribution data: whether
# detect() spuriously reports collision_detected=True on cases that are, by
# both external benchmarks' own design, single-threat rather than paired
# conflicts - a well-behaved detector should not hallucinate a second side
# of a collision that isn't there.
#
# Neither benchmark provides a mitigation-accuracy-compatible label.
# mitigation_accuracy is NOT computed anywhere in this script.

def load_agentharm():
    path = hf_hub_download(
        repo_id="ai-safety-institute/AgentHarm",
        filename="benchmark/harmful_behaviors_test_public.json",
        repo_type="dataset",
    )
    return json.load(open(path))["behaviors"]

def load_safetybench():
    path = hf_hub_download(
        repo_id="thu-coai/Agent-SafetyBench",
        filename="released_data.json",
        repo_type="dataset",
    )
    return json.load(open(path))

def evaluate(cases, get_category_key, map_fn, workflow_name):
    registry = Registry.default()
    by_category = defaultdict(lambda: {"n_cases": 0, "n_mapped": 0, "n_obligation_triggered": 0, "n_collision_detected": 0})
    rows = []

    for case in cases:
        category_key = get_category_key(case)
        by_category[category_key]["n_cases"] += 1

        mapped_signals = map_fn(case)
        row = {"category": category_key, "mapped": mapped_signals is not None, "mapped_signals": mapped_signals}

        if mapped_signals is not None:
            by_category[category_key]["n_mapped"] += 1
            trace = Trace(signals=mapped_signals, workflow=workflow_name)
            report = detect(trace, registry)

            obligation_triggered = len(report.triggered_obligations) > 0
            if obligation_triggered:
                by_category[category_key]["n_obligation_triggered"] += 1
            if report.collision_detected:
                by_category[category_key]["n_collision_detected"] += 1

            row["triggered_obligations"] = report.triggered_obligations
            row["collision_detected"] = report.collision_detected

        rows.append(row)

    return by_category, rows

def summarize_source(by_category, source_name):
    total_cases = sum(v["n_cases"] for v in by_category.values())
    total_mapped = sum(v["n_mapped"] for v in by_category.values())
    total_triggered = sum(v["n_obligation_triggered"] for v in by_category.values())
    total_collision = sum(v["n_collision_detected"] for v in by_category.values())

    print(f"\n=== {source_name} ===")
    print(f"{'category':45s} {'n':>5s} {'mapped':>7s} {'triggered':>10s} {'collision':>10s}")
    for category, v in sorted(by_category.items()):
        print(f"{category:45s} {v['n_cases']:5d} {v['n_mapped']:7d} {v['n_obligation_triggered']:10d} {v['n_collision_detected']:10d}")

    return {
        "source": source_name,
        "total_cases": total_cases,
        "total_mapped": total_mapped,
        "coverage_rate": round(total_mapped / total_cases, 3) if total_cases else None,
        "obligation_trigger_rate_of_mapped": round(total_triggered / total_mapped, 3) if total_mapped else None,
        "collision_detected_rate_of_mapped": round(total_collision / total_mapped, 3) if total_mapped else None,
        "by_category": dict(by_category),
    }

def main():
    agentharm_cases = load_agentharm()
    ah_by_category, ah_rows = evaluate(
        agentharm_cases,
        get_category_key=lambda c: c["category"],
        map_fn=lambda c: map_agentharm_case(c["category"]),
        workflow_name="external_agentharm",
    )
    ah_summary = summarize_source(ah_by_category, "AgentHarm (harmful_behaviors_test_public)")

    safetybench_cases = load_safetybench()
    sb_by_category, sb_rows = evaluate(
        safetybench_cases,
        get_category_key=lambda c: c["risks"][0] if c["risks"] else "(none)",
        map_fn=lambda c: map_safetybench_case(c["risks"]),
        workflow_name="external_safetybench",
    )
    sb_summary = summarize_source(sb_by_category, "Agent-SafetyBench (released_data)")

    result = {
        "honesty_note": (
            "Neither AgentHarm nor Agent-SafetyBench provides an "
            "expected-mitigation label compatible with EdgeCase's schema. "
            "This analysis reports obligation-triggering coverage and "
            "collision-detection rate on externally-sourced, "
            "externally-labeled data. It does NOT validate mitigation "
            "accuracy, and does NOT test whether EdgeCase can independently "
            "classify raw prompt text into signals - the mapping goes "
            "directly from each dataset's own ground-truth category label "
            "to a known EdgeCase trigger signal, not from re-derived text "
            "classification."
        ),
        "agentharm": ah_summary,
        "agent_safetybench": sb_summary,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=2))

    with OUT_MD.open("w") as f:
        f.write("# External validity: AgentHarm and Agent-SafetyBench\n\n")
        f.write(result["honesty_note"] + "\n\n")
        for summary in (ah_summary, sb_summary):
            f.write(f"## {summary['source']}\n\n")
            f.write(f"- Total cases: {summary['total_cases']}\n")
            f.write(f"- Cases with a mapped EdgeCase signal (coverage): {summary['total_mapped']} ({summary['coverage_rate']:.1%})\n")
            f.write(f"- Of mapped cases, obligation triggered: {summary['obligation_trigger_rate_of_mapped']:.1%} (expected ~100%, see honesty note - a direct-lookup mapping onto a known trigger fires by construction)\n")
            f.write(f"- Of mapped cases, collision_detected=True: {summary['collision_detected_rate_of_mapped']:.1%} (the genuinely informative number: false-positive-collision rate on single-threat data)\n\n")
            f.write("| Category | Cases | Mapped | Obligation Triggered | Collision Detected |\n")
            f.write("| --- | --- | --- | --- | --- |\n")
            for category, v in sorted(summary["by_category"].items()):
                f.write(f"| {category} | {v['n_cases']} | {v['n_mapped']} | {v['n_obligation_triggered']} | {v['n_collision_detected']} |\n")
            f.write("\n")

    print(f"\nWrote {OUT_JSON}, {OUT_MD}")

if __name__ == "__main__":
    main()
