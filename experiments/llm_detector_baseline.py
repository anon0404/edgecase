"""LLM zero-shot collision-detection baseline: can a general-purpose model
replace EdgeCase's hand-built registry/lookup, given the same task framing
a human annotator gets (the Rubric sheet's collision-type definitions)?

Reuses the 152-case blinded, stratified sample already scored by two human
annotators (experiments/annotation/annotation_answer_key.csv), so results
are directly comparable on the identical cases to both the benchmark's own
ground truth and the human-annotator agreement numbers
(experiments/annotation/score_agreement.py), not a fresh, differently-
sampled comparison.

Two conditions:
  - with_signals: same (prompt, signals) input EdgeCase's own detect() and
    the human annotators saw. Isolates whether an LLM can do the
    classification step alone, apples-to-apples with existing accuracy
    numbers.
  - prompt_only: raw prompt, no signals. Harder and more realistic - tests
    whether an LLM could replace the whole registry (signal extraction +
    classification), at the cost of conflating the two failure modes if it
    does poorly.

Usage:
  EDGECASE_PROVIDER=mock python experiments/llm_detector_baseline.py   # free dry run
  EDGECASE_PROVIDER=anthropic ANTHROPIC_API_KEY=... python experiments/llm_detector_baseline.py
  EDGECASE_CONDITIONS=with_signals python experiments/llm_detector_baseline.py  # single condition
"""
import csv
import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "annotation"))
from build_annotation_sample import RUBRIC  # noqa: E402

from edgecase.adapters import AnthropicAdapter, MockAdapter  # noqa: E402

ANSWER_KEY = Path("experiments/annotation/annotation_answer_key.csv")
OUT_DIR = Path("experiments/results/llm_detector_baseline")

COLLISION_OPTIONS = [r[0] for r in RUBRIC] + ["none"]
MITIGATION_OPTIONS = [r[6] for r in RUBRIC] + ["none"]


def build_system_prompt() -> str:
    lines = [
        "You are classifying governance-obligation collisions in agentic AI workflows.",
        "There are exactly seven possible collision types, each a tension between two",
        "legitimate obligations. For each case, decide whether one of these seven",
        "collisions is present, or none.",
        "",
    ]
    for c_type, _ob_a, _trig_a, _ob_b, _trig_b, tension, mitigation in RUBRIC:
        lines.append(f"- {c_type}: {tension} Expected mitigation if present: {mitigation}.")
    lines.append("")
    lines.append(
        "Respond with ONLY a JSON object, no other text, no markdown fences: "
        '{"collision_type": "<one of: ' + ", ".join(COLLISION_OPTIONS) + '>", '
        '"mitigation": "<one of: ' + ", ".join(MITIGATION_OPTIONS) + '>"}'
    )
    return "\n".join(lines)


SYSTEM = build_system_prompt()


def build_user_prompt(case: dict, condition: str) -> str:
    if condition == "with_signals":
        return f"Prompt: {case['prompt']}\nSignals: {case['signals']}"
    return f"Prompt: {case['prompt']}"


def parse_response(text: str):
    try:
        obj = json.loads(text)
        return obj.get("collision_type", "parse_error"), obj.get("mitigation", "parse_error")
    except (json.JSONDecodeError, AttributeError):
        pass
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            obj = json.loads(match.group(0))
            return obj.get("collision_type", "parse_error"), obj.get("mitigation", "parse_error")
        except json.JSONDecodeError:
            pass
    return "parse_error", "parse_error"


def build_adapter(provider: str):
    if provider == "mock":
        return MockAdapter()
    if provider == "anthropic":
        import anthropic

        return AnthropicAdapter(
            client=anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"]),
            model=os.getenv("EDGECASE_MODEL") or "claude-sonnet-4-5",
        )
    raise ValueError(f"Unknown provider: {provider}")


def load_cases():
    with ANSWER_KEY.open() as f:
        return list(csv.DictReader(f))


def main():
    provider = os.getenv("EDGECASE_PROVIDER", "mock")
    conditions = os.getenv("EDGECASE_CONDITIONS", "with_signals,prompt_only").split(",")
    adapter = build_adapter(provider)
    cases = load_cases()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    all_rows = []
    for condition in conditions:
        rows = []
        for case in cases:
            user_prompt = build_user_prompt(case, condition)
            t0 = time.time()
            resp = adapter.generate(user_prompt, system=SYSTEM)
            latency_ms = int((time.time() - t0) * 1000)
            collision_pred, mitigation_pred = parse_response(resp["response"])
            rows.append({
                "row_number": case["row_number"],
                "id": case["id"],
                "domain": case["domain"],
                "condition": condition,
                "provider": provider,
                "model": resp["model"],
                "true_collision": case["true_collision"],
                "true_expected_mitigation": case["true_expected_mitigation"],
                "predicted_collision": collision_pred,
                "predicted_mitigation": mitigation_pred,
                "raw_response": resp["response"],
                "latency_ms": latency_ms,
            })
        out_path = OUT_DIR / f"{provider}_{condition}_rows.json"
        out_path.write_text(json.dumps(rows, indent=2))
        all_rows.extend(rows)
        print(f"[{condition}] wrote {out_path} ({len(rows)} rows)")

    from sklearn.metrics import cohen_kappa_score

    summary = {}
    for condition in conditions:
        cond_rows = [r for r in all_rows if r["condition"] == condition]
        n = len(cond_rows)
        collision_correct = sum(1 for r in cond_rows if r["predicted_collision"] == r["true_collision"])
        mitigation_correct = sum(1 for r in cond_rows if r["predicted_mitigation"] == r["true_expected_mitigation"])
        n_parse_errors = sum(1 for r in cond_rows if r["predicted_collision"] == "parse_error")
        kappa = (
            cohen_kappa_score(
                [r["true_collision"] for r in cond_rows],
                [r["predicted_collision"] for r in cond_rows],
            )
            if n else None
        )
        summary[condition] = {
            "n": n,
            "collision_accuracy": round(collision_correct / n, 4) if n else None,
            "mitigation_accuracy": round(mitigation_correct / n, 4) if n else None,
            "cohen_kappa_vs_ground_truth": round(kappa, 4) if kappa is not None else None,
            "n_parse_errors": n_parse_errors,
            "avg_latency_ms": round(sum(r["latency_ms"] for r in cond_rows) / n, 1) if n else None,
        }

    summary_path = OUT_DIR / f"{provider}_summary.json"
    summary_path.write_text(json.dumps({"provider": provider, "conditions": summary}, indent=2))
    print(json.dumps(summary, indent=2))
    print(f"Wrote {summary_path}")


if __name__ == "__main__":
    main()
