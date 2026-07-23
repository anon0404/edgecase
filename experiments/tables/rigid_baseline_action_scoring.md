# Rigid baseline externality re-scoring: action-specific vs. pole-based

Same 10-seed benchmark rows as Table 1, but rigid-baseline externalities are scored by whether the policy's fixed action actually addresses one side of the case's real collision (0.5x the collision-specific externality) or neither side (1.0x, same as an unresolved collision), instead of by a policy-wide restrictive/supportive pole.

| Policy | Fraction addressing one side | Metric | Mean | 95% CI |
| --- | --- | --- | --- | --- |
| strict_block | 0.1429 | mitigation_accuracy | 0.0714 | [0.0684, 0.0745] |
| strict_block | 0.1429 | avg_care_suppression | 0.1571 | [0.1539, 0.1604] |
| strict_block | 0.1429 | avg_security_risk | 0.2221 | [0.2193, 0.2249] |
| strict_block | 0.1429 | avg_accessibility_burden | 0.1971 | [0.1925, 0.202] |
| strict_block | 0.1429 | avg_privacy_exposure | 0.1543 | [0.1501, 0.1585] |
| strict_block | 0.1429 | avg_energy_score | 0.2 | [0.2, 0.2] |
| strict_block | 0.1429 | governance_externality | 0.1831 | [0.1821, 0.1841] |
| always_escalate | 0.1429 | mitigation_accuracy | 0.0714 | [0.0684, 0.0745] |
| always_escalate | 0.1429 | avg_care_suppression | 0.1571 | [0.1538, 0.1604] |
| always_escalate | 0.1429 | avg_security_risk | 0.2221 | [0.2194, 0.2249] |
| always_escalate | 0.1429 | avg_accessibility_burden | 0.1971 | [0.1923, 0.2019] |
| always_escalate | 0.1429 | avg_privacy_exposure | 0.1543 | [0.15, 0.1587] |
| always_escalate | 0.1429 | avg_energy_score | 0.5 | [0.5, 0.5] |
| always_escalate | 0.1429 | governance_externality | 0.2131 | [0.2121, 0.2141] |
| always_verify | 0.1429 | mitigation_accuracy | 0.0714 | [0.0684, 0.0745] |
| always_verify | 0.1429 | avg_care_suppression | 0.2086 | [0.2041, 0.2132] |
| always_verify | 0.1429 | avg_security_risk | 0.2264 | [0.2235, 0.2294] |
| always_verify | 0.1429 | avg_accessibility_burden | 0.1414 | [0.1383, 0.1444] |
| always_verify | 0.1429 | avg_privacy_exposure | 0.1543 | [0.1501, 0.1586] |
| always_verify | 0.1429 | avg_energy_score | 0.5 | [0.5, 0.5] |
| always_verify | 0.1429 | governance_externality | 0.2213 | [0.2198, 0.2228] |
| maximum_review | 0.2857 | mitigation_accuracy | 0.1429 | [0.139, 0.1467] |
| maximum_review | 0.2857 | avg_care_suppression | 0.1771 | [0.1727, 0.1814] |
| maximum_review | 0.2857 | avg_security_risk | 0.2336 | [0.2305, 0.2366] |
| maximum_review | 0.2857 | avg_accessibility_burden | 0.1971 | [0.1924, 0.2019] |
| maximum_review | 0.2857 | avg_privacy_exposure | 0.1129 | [0.1096, 0.1161] |
| maximum_review | 0.2857 | avg_energy_score | 0.9 | [0.9, 0.9] |
| maximum_review | 0.2857 | governance_externality | 0.2537 | [0.2522, 0.2551] |
