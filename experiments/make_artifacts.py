import json
import csv
from pathlib import Path

import matplotlib.pyplot as plt

RESULTS = Path("experiments/results")
FIGURES = Path("experiments/figures")
TABLES = Path("experiments/tables")

SUMMARY = RESULTS / "summary.json"

def percent(x):
    return round(100 * x, 1)

def main():
    FIGURES.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)

    summary = json.loads(SUMMARY.read_text())

    rows = []
    for policy, metrics in summary.items():
        rows.append({
            "policy": policy,
            "collision_accuracy": percent(metrics.get("collision_accuracy", 0)),
            "mitigation_accuracy": percent(metrics.get("mitigation_accuracy", 0)),
            "care_suppression": round(metrics.get("avg_care_suppression_risk", 0), 3),
            "security_risk": round(metrics.get("avg_security_risk", 0), 3),
            "accessibility_burden": round(metrics.get("avg_accessibility_burden", 0), 3),
            "privacy_exposure": round(metrics.get("avg_privacy_exposure", 0), 3),
            "high_energy_rate": percent(metrics.get("high_energy_rate", 0)),
        })

    csv_path = TABLES / "summary_table.csv"
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    md_path = TABLES / "summary_table.md"
    headers = list(rows[0].keys())
    with md_path.open("w") as f:
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
        for row in rows:
            f.write("| " + " | ".join(str(row[h]) for h in headers) + " |\n")

    policies = [r["policy"] for r in rows]
    collision_acc = [r["collision_accuracy"] for r in rows]
    mitigation_acc = [r["mitigation_accuracy"] for r in rows]

    plt.figure(figsize=(9, 5))
    x = range(len(policies))
    plt.bar(x, collision_acc, label="Collision accuracy")
    plt.plot(x, mitigation_acc, marker="o", label="Mitigation accuracy")
    plt.xticks(x, policies, rotation=25, ha="right")
    plt.ylabel("Accuracy (%)")
    plt.title("EdgeCase vs Single-Objective Baselines")
    plt.ylim(0, 105)
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "accuracy_comparison.png", dpi=300)
    plt.close()

    care = [r["care_suppression"] for r in rows]
    security = [r["security_risk"] for r in rows]
    accessibility = [r["accessibility_burden"] for r in rows]

    plt.figure(figsize=(9, 5))
    plt.plot(policies, care, marker="o", label="Care suppression")
    plt.plot(policies, security, marker="o", label="Security risk")
    plt.plot(policies, accessibility, marker="o", label="Accessibility burden")
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Externality score")
    plt.title("Mitigation Externalities by Policy")
    plt.ylim(0, 1)
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "externality_comparison.png", dpi=300)
    plt.close()

    print(f"Wrote {csv_path}")
    print(f"Wrote {md_path}")
    print(f"Wrote {FIGURES / 'accuracy_comparison.png'}")
    print(f"Wrote {FIGURES / 'externality_comparison.png'}")

if __name__ == "__main__":
    main()
