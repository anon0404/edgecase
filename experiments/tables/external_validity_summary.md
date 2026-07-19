# External validity: AgentHarm and Agent-SafetyBench

Neither AgentHarm nor Agent-SafetyBench provides an expected-mitigation label compatible with EdgeCase's schema. This analysis reports obligation-triggering coverage and collision-detection rate on externally-sourced, externally-labeled data. It does NOT validate mitigation accuracy, and does NOT test whether EdgeCase can independently classify raw prompt text into signals - the mapping goes directly from each dataset's own ground-truth category label to a known EdgeCase trigger signal, not from re-derived text classification. Separately: the 0% collision-detected rate reported per source is only a genuine test on the subset of mapped cases where 2+ obligations actually fire (n_multi_obligation_mapped) - see correct_non_collision_rate_of_multi_obligation. On single-obligation cases (n_single_obligation_mapped), a collision is mechanically impossible regardless of detector quality, so 0% there is a structural guarantee of the input, not a demonstrated detector behavior.

## AgentHarm (harmful_behaviors_test_public)

- Total cases: 176
- Cases with a mapped EdgeCase signal (coverage): 176 (100.0%)
- Of mapped cases, obligation triggered: 100.0% (expected ~100%, see honesty note - a direct-lookup mapping onto a known trigger fires by construction)
- Multi-obligation cases (2+ obligations fire simultaneously): 24 - the genuine collision-avoidance test
- Single-obligation cases: 152 - non-collision here is structural, not demonstrated
- Of mapped cases, collision_detected=True: 0.0% (diluted by single-obligation cases, see above)
- Of multi-obligation cases specifically, correctly NOT flagged as a collision: 100.0%

| Category | Cases | Mapped | Obligation Triggered | Multi-Obligation | Collision Detected |
| --- | --- | --- | --- | --- | --- |
| Copyright | 24 | 24 | 24 | 0 | 0 |
| Cybercrime | 20 | 20 | 20 | 0 | 0 |
| Disinformation | 20 | 20 | 20 | 0 | 0 |
| Drugs | 20 | 20 | 20 | 0 | 0 |
| Fraud | 24 | 24 | 24 | 24 | 0 |
| Harassment | 24 | 24 | 24 | 0 | 0 |
| Hate | 20 | 20 | 20 | 0 | 0 |
| Sexual | 24 | 24 | 24 | 0 | 0 |

## Agent-SafetyBench (released_data)

- Total cases: 2000
- Cases with a mapped EdgeCase signal (coverage): 1000 (50.0%)
- Of mapped cases, obligation triggered: 100.0% (expected ~100%, see honesty note - a direct-lookup mapping onto a known trigger fires by construction)
- Multi-obligation cases (2+ obligations fire simultaneously): 250 - the genuine collision-avoidance test
- Single-obligation cases: 750 - non-collision here is structural, not demonstrated
- Of mapped cases, collision_detected=True: 0.0% (diluted by single-obligation cases, see above)
- Of multi-obligation cases specifically, correctly NOT flagged as a collision: 100.0%

| Category | Cases | Mapped | Obligation Triggered | Multi-Obligation | Collision Detected |
| --- | --- | --- | --- | --- | --- |
| Compromise availability | 250 | 0 | 0 | 0 | 0 |
| Contribute to harmful / vulnerable code | 250 | 0 | 0 | 0 | 0 |
| Lead to physical harm | 250 | 0 | 0 | 0 | 0 |
| Lead to property loss | 250 | 250 | 250 | 0 | 0 |
| Leak sensitive data / information | 250 | 250 | 250 | 250 | 0 |
| Produce unsafe information / misinformation | 250 | 250 | 250 | 0 | 0 |
| Spread unsafe information / misinformation | 250 | 0 | 0 | 0 | 0 |
| Violate law or ethics / damage society | 250 | 250 | 250 | 0 | 0 |

