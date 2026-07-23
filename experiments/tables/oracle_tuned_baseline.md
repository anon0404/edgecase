# Oracle-tuned fixed baseline (10 seeds, train-tuned/test-evaluated)

Per collision type, the single fixed mitigation string that maximizes score on that type's train-split cases, evaluated on the held-out test split using the true collision type to select which fixed answer to apply. Isolates whether mitigation selection is hard once the collision type is already known - a ceiling reading for Adaptive EdgeCase's own detection-limited accuracy, not a detection baseline itself.

| Metric | Mean | 95% CI |
| --- | --- | --- |
| mitigation_accuracy | 1.0 | [1.0, 1.0] |
| avg_care_suppression | 0.2158 | [0.2037, 0.2278] |
| avg_security_risk | 0.2515 | [0.2438, 0.2591] |
| avg_accessibility_burden | 0.1952 | [0.183, 0.2076] |
| avg_privacy_exposure | 0.1486 | [0.1379, 0.1597] |
| avg_energy_score | 0.3265 | [0.32, 0.3332] |
| governance_externality | 0.2192 | [0.2156, 0.2229] |

Tuning mismatches vs. the benchmark's own known-correct per-type mapping: {}
