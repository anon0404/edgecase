import json
from pathlib import Path

RESULTS_DIR = Path("experiments/results/real_models")
OUT_MD = Path("experiments/tables/real_model_evaluation_summary.md")

def main():
    summaries = sorted(RESULTS_DIR.glob("summary_*.json"))
    if not summaries:
        raise SystemExit(
            f"No summary_*.json files in {RESULTS_DIR}. "
            "Run experiments/run_real_model_evaluation.py once per provider first."
        )

    rows = [json.loads(p.read_text()) for p in summaries]

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    with OUT_MD.open("w") as f:
        headers = [
            "provider", "model", "cases", "governance_externality",
            "avg_response_alignment", "mitigation_accuracy_ground_truth_signals",
            "avg_latency_ms", "avg_tokens_estimate",
        ]
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
        for row in rows:
            f.write("| " + " | ".join(str(row.get(h, "")) for h in headers) + " |\n")

    print(json.dumps(rows, indent=2))
    print(f"Wrote {OUT_MD}")

if __name__ == "__main__":
    main()
