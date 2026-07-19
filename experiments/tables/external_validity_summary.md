# External validity: AgentHarm and Agent-SafetyBench

Neither AgentHarm nor Agent-SafetyBench provides an expected-mitigation label compatible with EdgeCase's schema. This analysis reports obligation-triggering coverage and collision-detection rate on externally-sourced, externally-labeled data. It does NOT validate mitigation accuracy, and does NOT test whether EdgeCase can independently classify raw prompt text into signals - the mapping goes directly from each dataset's own ground-truth category label to a known EdgeCase trigger signal, not from re-derived text classification.

## AgentHarm (harmful_behaviors_test_public)

- Total cases: 176
- Cases with a mapped EdgeCase signal (coverage): 176 (100.0%)
- Of mapped cases, obligation triggered: 100.0% (expected ~100%, see honesty note - a direct-lookup mapping onto a known trigger fires by construction)
- Of mapped cases, collision_detected=True: 0.0% (the genuinely informative number: false-positive-collision rate on single-threat data)

| Category | Cases | Mapped | Obligation Triggered | Collision Detected |
| --- | --- | --- | --- | --- |
| Copyright | 24 | 24 | 24 | 0 |
| Cybercrime | 20 | 20 | 20 | 0 |
| Disinformation | 20 | 20 | 20 | 0 |
| Drugs | 20 | 20 | 20 | 0 |
| Fraud | 24 | 24 | 24 | 0 |
| Harassment | 24 | 24 | 24 | 0 |
| Hate | 20 | 20 | 20 | 0 |
| Sexual | 24 | 24 | 24 | 0 |

## Agent-SafetyBench (released_data)

- Total cases: 2000
- Cases with a mapped EdgeCase signal (coverage): 1000 (50.0%)
- Of mapped cases, obligation triggered: 100.0% (expected ~100%, see honesty note - a direct-lookup mapping onto a known trigger fires by construction)
- Of mapped cases, collision_detected=True: 0.0% (the genuinely informative number: false-positive-collision rate on single-threat data)

| Category | Cases | Mapped | Obligation Triggered | Collision Detected |
| --- | --- | --- | --- | --- |
| Compromise availability | 250 | 0 | 0 | 0 |
| Contribute to harmful / vulnerable code | 250 | 0 | 0 | 0 |
| Lead to physical harm | 250 | 0 | 0 | 0 |
| Lead to property loss | 250 | 250 | 250 | 0 |
| Leak sensitive data / information | 250 | 250 | 250 | 0 |
| Produce unsafe information / misinformation | 250 | 250 | 250 | 0 |
| Spread unsafe information / misinformation | 250 | 0 | 0 | 0 |
| Violate law or ethics / damage society | 250 | 250 | 250 | 0 |

