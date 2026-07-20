# Oracle-tuned fixed baseline (10 seeds, train-tuned/test-evaluated)

Per collision type, the single fixed mitigation string that maximizes score on that type's train-split cases, evaluated on the held-out test split using the true collision type to select which fixed answer to apply. Isolates whether mitigation selection is hard once the collision type is already known - a ceiling reading for Adaptive EdgeCase's own detection-limited accuracy, not a detection baseline itself.

| Metric | Mean | 95% CI |
| --- | --- | --- |
| mitigation_accuracy | 1.0 | [1.0, 1.0] |
| avg_care_suppression | 0.212 | [0.1999, 0.2243] |
| avg_security_risk | 0.2557 | [0.248, 0.2633] |
| avg_accessibility_burden | 0.1967 | [0.1842, 0.2096] |
| avg_privacy_exposure | 0.1593 | [0.1482, 0.1707] |
| avg_energy_score | 0.3294 | [0.3227, 0.336] |
| governance_externality | 0.2218 | [0.2182, 0.2254] |

Tuning mismatches vs. the benchmark's own known-correct per-type mapping: {}
