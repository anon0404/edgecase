import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean

DATA = Path("experiments/results/full_evaluation.json")
OUT_JSON = Path("experiments/results/full_evaluation_summary.json")
OUT_CSV = Path("experiments/tables/full_evaluation_summary.csv")
OUT_MD = Path("experiments/tables/full_evaluation_summary.md")

ENERGY_SCORE = {
    "low": 0.2,
    "medium": 0.5,
    "high": 0.9,
}

def main():
    rows = json.loads(DATA.read_text())

    grouped = defaultdict(list)
    for row in rows:
        grouped[row["policy"]].append(row)

    summary_rows = []

    for policy, items in grouped.items():
        summary_rows.append({
            "policy": policy,
            "cases": len(items),
            "mitigation_accuracy": round(mean([i["correct_mitigation"] for i in items]), 3),
            "avg_care_suppression": round(mean([i["care_suppression_risk"] for i in items]), 3),
            "avg_security_risk": round(mean([i["security_risk"] for i in items]), 3),
            "avg_accessibility_burden": round(mean([i["accessibility_burden"] for i in items]), 3),
            "avg_privacy_exposure": round(mean([i["privacy_exposure"] for i in items]), 3),
            "avg_energy_score": round(mean([ENERGY_SCORE[i["energy_cost"]] for i in items]), 3),
        })

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(summary_rows, indent=2))

    with OUT_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary_rows)

    with OUT_MD.open("w") as f:
        headers = list(summary_rows[0].keys())
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
        for row in summary_rows:
            f.write("| " + " | ".join(str(row[h]) for h in headers) + " |\n")

    print(json.dumps(summary_rows, indent=2))
    print(f"Wrote {OUT_JSON}, {OUT_CSV}, {OUT_MD}")

if __name__ == "__main__":
    main()
