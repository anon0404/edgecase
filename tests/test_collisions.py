from edgecase import Registry, Trace, detect


def test_block_vs_escalate():
    report = detect(
        Trace(signals=["jailbreak", "self_harm"]),
        Registry.default(),
    )
    assert report.collision_detected
    assert report.collision_type == "block_vs_escalate"
    assert report.recommended_mitigation == "constrain_and_escalate"


def test_verify_vs_accessibility():
    report = detect(
        Trace(signals=["fraud_risk", "disability_signal"]),
        Registry.default(),
    )
    assert report.collision_type == "verify_vs_accessibility"


def test_safety_vs_energy():
    report = detect(
        Trace(
            signals=["high_risk", "compute_pressure"],
            model_calls=4,
        ),
        Registry.default(),
    )
    assert report.collision_type == "safety_vs_energy"
    assert report.externalities.energy_cost == "high"
