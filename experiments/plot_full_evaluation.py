import json
from pathlib import Path

import matplotlib.pyplot as plt

DATA = Path("experiments/results/full_evaluation_summary.json")
OUT = Path("experiments/figures")
OUT.mkdir(parents=True, exist_ok=True)

def main():
    rows = json.loads(DATA.read_text())

    policies = [r["policy"] for r in rows]

    metrics = [
        "mitigation_accuracy",
        "avg_care_suppression",
        "avg_security_risk",
        "avg_accessibility_burden",
        "avg_privacy_exposure",
        "avg_energy_score",
    ]

    for metric in metrics:
        plt.figure(figsize=(9, 5))
        values = [r[metric] for r in rows]
        plt.bar(policies, values)
        plt.xticks(rotation=25, ha="right")
        plt.ylim(0, 1)
        plt.ylabel(metric.replace("_", " ").title())
        plt.title(metric.replace("_", " ").title() + " by Policy")
        plt.tight_layout()
        plt.savefig(OUT / f"{metric}.png", dpi=300)
        plt.close()

    plt.figure(figsize=(8, 6))
    x = [1 - r["avg_security_risk"] for r in rows]
    y = [
        (1 - r["avg_care_suppression"] + 1 - r["avg_accessibility_burden"]) / 2
        for r in rows
    ]
    sizes = [200 + r["avg_energy_score"] * 900 for r in rows]

    plt.scatter(x, y, s=sizes, alpha=0.75)

    for i, policy in enumerate(policies):
        plt.annotate(policy, (x[i], y[i]), xytext=(6, 6), textcoords="offset points")

    plt.xlabel("Security Robustness")
    plt.ylabel("Care + Accessibility Preservation")
    plt.title("Governance Tradeoff Frontier")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig(OUT / "governance_tradeoff_frontier.png", dpi=300)
    plt.close()

    print(f"Wrote plots to {OUT}")

if __name__ == "__main__":
    main()
