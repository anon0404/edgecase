# LLM-Detected + EdgeCase-Routed (10 seeds, provider=anthropic)

Distinct (prompt, signal-set) pairs classified: 803, covering 12600 rows.

Outcome breakdown: {'correct': 12493, 'wrong_type': 107, 'predicted_none': 0, 'parse_error': 0}

## Original scoring (trust the LLM's own decision, same convention as Adaptive EdgeCase)

| Metric | Mean | 95% CI |
| --- | --- | --- |
| mitigation_accuracy | 0.9915 | [0.9898, 0.9931] |
| avg_care_suppression | 0.2147 | [0.2101, 0.2194] |
| avg_security_risk | 0.2519 | [0.2489, 0.255] |
| avg_accessibility_burden | 0.1905 | [0.1859, 0.1954] |
| avg_privacy_exposure | 0.1543 | [0.1501, 0.1585] |
| avg_energy_score | 0.3286 | [0.326, 0.3311] |
| governance_externality | 0.2197 | [0.2183, 0.2211] |

## Penalized scoring (any misdetection charged the true collision type's real cost)

| Metric | Mean | 95% CI |
| --- | --- | --- |
| mitigation_accuracy | 0.9915 | [0.9898, 0.9931] |
| avg_care_suppression | 0.2086 | [0.204, 0.2132] |
| avg_security_risk | 0.2514 | [0.2484, 0.2545] |
| avg_accessibility_burden | 0.1971 | [0.1925, 0.202] |
| avg_privacy_exposure | 0.1543 | [0.1501, 0.1585] |
| avg_energy_score | 0.3286 | [0.326, 0.3311] |
| governance_externality | 0.2187 | [0.2173, 0.2201] |
