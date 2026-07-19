# Statistical summary (10 seeds, 10000 bootstrap resamples)

## Mean ± bootstrap 95% CI per policy

| Policy | Metric | Mean | 95% CI |
| --- | --- | --- | --- |
| strict_block | mitigation_accuracy | 0.0714 | [0.0683, 0.0744] |
| strict_block | avg_care_suppression | 0.3503 | [0.3432, 0.3571] |
| strict_block | avg_security_risk | 0.05 | [0.05, 0.05] |
| strict_block | avg_accessibility_burden | 0.2671 | [0.2624, 0.2718] |
| strict_block | avg_privacy_exposure | 0.05 | [0.05, 0.05] |
| strict_block | avg_energy_score | 0.2 | [0.2, 0.2] |
| strict_block | governance_externality | 0.1876 | [0.1857, 0.1895] |
| always_escalate | mitigation_accuracy | 0.0714 | [0.0684, 0.0745] |
| always_escalate | avg_care_suppression | 0.1286 | [0.1253, 0.1319] |
| always_escalate | avg_security_risk | 0.4088 | [0.4031, 0.4144] |
| always_escalate | avg_accessibility_burden | 0.05 | [0.05, 0.05] |
| always_escalate | avg_privacy_exposure | 0.2425 | [0.2365, 0.2486] |
| always_escalate | avg_energy_score | 0.5 | [0.5, 0.5] |
| always_escalate | governance_externality | 0.2468 | [0.2459, 0.2476] |
| always_verify | mitigation_accuracy | 0.0714 | [0.0684, 0.0744] |
| always_verify | avg_care_suppression | 0.3503 | [0.3433, 0.3572] |
| always_verify | avg_security_risk | 0.05 | [0.05, 0.05] |
| always_verify | avg_accessibility_burden | 0.2671 | [0.2623, 0.2718] |
| always_verify | avg_privacy_exposure | 0.05 | [0.05, 0.05] |
| always_verify | avg_energy_score | 0.5 | [0.5, 0.5] |
| always_verify | governance_externality | 0.2176 | [0.2157, 0.2195] |
| maximum_review | mitigation_accuracy | 0.1429 | [0.1388, 0.1468] |
| maximum_review | avg_care_suppression | 0.3503 | [0.3434, 0.3573] |
| maximum_review | avg_security_risk | 0.05 | [0.05, 0.05] |
| maximum_review | avg_accessibility_burden | 0.2671 | [0.2624, 0.2718] |
| maximum_review | avg_privacy_exposure | 0.05 | [0.05, 0.05] |
| maximum_review | avg_energy_score | 0.9 | [0.9, 0.9] |
| maximum_review | governance_externality | 0.2576 | [0.2558, 0.2596] |
| edgecase_adaptive | mitigation_accuracy | 0.8441 | [0.8378, 0.8504] |
| edgecase_adaptive | avg_care_suppression | 0.1523 | [0.1476, 0.157] |
| edgecase_adaptive | avg_security_risk | 0.2523 | [0.2493, 0.2553] |
| edgecase_adaptive | avg_accessibility_burden | 0.1621 | [0.1573, 0.1669] |
| edgecase_adaptive | avg_privacy_exposure | 0.1157 | [0.1118, 0.1196] |
| edgecase_adaptive | avg_energy_score | 0.3087 | [0.3062, 0.3112] |
| edgecase_adaptive | governance_externality | 0.1871 | [0.1852, 0.1889] |

## Paired Wilcoxon signed-rank test: Adaptive EdgeCase vs. each baseline, mitigation_score

Matched by (seed, case_id) - same benchmark instance, both policies.

| Baseline | n pairs | n nonzero diffs | Mean diff (adaptive - baseline) | Statistic | p-value |
| --- | --- | --- | --- | --- | --- |
| strict_block | 12600 | 10636 | 0.7727 | 0.0 | 0.000e+00 |
| always_escalate | 12600 | 10636 | 0.7727 | 0.0 | 0.000e+00 |
| maximum_review | 12600 | 11496 | 0.7013 | 1548430.0 | 0.000e+00 |
