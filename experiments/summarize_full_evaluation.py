import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean

from edgecase.metrics import SEVERITY_WEIGHTS, aggregate_governance_externality

DATA = Path("experiments/results/full_evaluation.json")
OUT_JSON = Path("experiments/results/full_evaluation_summary.json")
OUT_CSV = Path("experiments/tables/full_evaluation_summary.csv")
OUT_MD = Path("experiments/tables/full_evaluation_summary.md")

ENERGY_SCORE = {
    "low": 0.2,
    "medium": 0.5,
    "high": 0.9,
}

# Table 2 in the paper compares 4 policies (Strict Block, Always Escalate,
# Maximum Review, Adaptive EdgeCase). always_verify is kept in the full
# per-case results and the JSON summary, but left out of the Table 2 CSV/MD
# since the paper doesn't describe or report it.
TABLE_2_POLICIES = {"strict_block", "always_escalate", "maximum_review", "edgecase_adaptive"}

def main():
    rows = json.loads(DATA.read_text())

    grouped = defaultdict(list)
    for row in rows:
        grouped[row["policy"]].append(row)

    summary_rows = []

    for policy, items in grouped.items():
        avg_care_suppression = mean([i["care_suppression_risk"] for i in items])
        avg_security_risk = mean([i["security_risk"] for i in items])
        avg_accessibility_burden = mean([i["accessibility_burden"] for i in items])
        avg_privacy_exposure = mean([i["privacy_exposure"] for i in items])
        avg_energy_score = mean([ENERGY_SCORE[i["energy_cost"]] for i in items])

        summary_rows.append({
            "policy": policy,
            "cases": len(items),
            "mitigation_accuracy": round(mean([i["mitigation_score"] for i in items]), 3),
            "avg_care_suppression": round(avg_care_suppression, 3),
            "avg_security_risk": round(avg_security_risk, 3),
            "avg_accessibility_burden": round(avg_accessibility_burden, 3),
            "avg_privacy_exposure": round(avg_privacy_exposure, 3),
            "avg_energy_score": round(avg_energy_score, 3),
            "governance_externality": round(aggregate_governance_externality(
                care_suppression=avg_care_suppression,
                accessibility_burden=avg_accessibility_burden,
                privacy_exposure=avg_privacy_exposure,
                security_risk=avg_security_risk,
                energy_score=avg_energy_score,
                weights=SEVERITY_WEIGHTS,
            ), 3),
            "governance_externality_uniform": round(aggregate_governance_externality(
                care_suppression=avg_care_suppression,
                accessibility_burden=avg_accessibility_burden,
                privacy_exposure=avg_privacy_exposure,
                security_risk=avg_security_risk,
                energy_score=avg_energy_score,
            ), 3),
        })

    table_2_rows = [row for row in summary_rows if row["policy"] in TABLE_2_POLICIES]

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(summary_rows, indent=2))

    with OUT_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(table_2_rows[0].keys()))
        writer.writeheader()
        writer.writerows(table_2_rows)

    with OUT_MD.open("w") as f:
        headers = list(table_2_rows[0].keys())
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
        for row in table_2_rows:
            f.write("| " + " | ".join(str(row[h]) for h in headers) + " |\n")

    print(json.dumps(summary_rows, indent=2))
    print(f"Wrote {OUT_JSON}, {OUT_CSV}, {OUT_MD}")

if __name__ == "__main__":
    main()
