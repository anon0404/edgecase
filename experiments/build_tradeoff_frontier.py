import json
from pathlib import Path

DATA = Path("experiments/results/policy_comparison.json")

OUT = Path("website/public/data/tradeoff_frontier.json")

def main():
    data = json.loads(DATA.read_text())

    summary = data["summary"]

    points = []

    for policy, values in summary.items():
        points.append({
            "policy": policy,
            "security": round(1 - values["avg_security_risk"], 3),
            "care": round(1 - values["avg_care_suppression"], 3),
            "accessibility": round(1 - values["avg_accessibility_burden"], 3),
            "privacy": round(1 - values["avg_privacy_exposure"], 3),
            "energy_penalty": values["high_energy_rate"],
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)

    OUT.write_text(json.dumps(points, indent=2))

    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
