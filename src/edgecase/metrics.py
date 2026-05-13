from statistics import mean

def summarize(rows: list[dict]) -> dict:
    total = len(rows)
    if total == 0:
        return {}

    return {
        "total_cases": total,
        "collision_accuracy": mean([r["correct_collision"] for r in rows]),
        "mitigation_accuracy": mean([r["correct_mitigation"] for r in rows]),
        "avg_care_suppression_risk": mean([r["externalities"]["care_suppression_risk"] for r in rows]),
        "avg_security_risk": mean([r["externalities"]["security_risk"] for r in rows]),
        "avg_accessibility_burden": mean([r["externalities"]["accessibility_burden"] for r in rows]),
        "avg_privacy_exposure": mean([r["externalities"]["privacy_exposure"] for r in rows]),
        "high_energy_rate": mean([1 if r["externalities"]["energy_cost"] == "high" else 0 for r in rows]),
    }
