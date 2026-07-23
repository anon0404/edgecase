# Statistical summary (10 seeds, 10000 bootstrap resamples)

## Mean ± bootstrap 95% CI per policy

| Policy | Metric | Mean | 95% CI |
| --- | --- | --- | --- |
| strict_block | mitigation_accuracy | 0.0714 | [0.0684, 0.0745] |
| strict_block | avg_care_suppression | 0.3883 | [0.3813, 0.3954] |
| strict_block | avg_security_risk | 0.05 | [0.05, 0.05] |
| strict_block | avg_accessibility_burden | 0.329 | [0.3243, 0.3337] |
| strict_block | avg_privacy_exposure | 0.05 | [0.05, 0.05] |
| strict_block | avg_energy_score | 0.2 | [0.2, 0.2] |
| strict_block | governance_externality | 0.2083 | [0.2065, 0.2103] |
| always_escalate | mitigation_accuracy | 0.0714 | [0.0684, 0.0745] |
| always_escalate | avg_care_suppression | 0.1286 | [0.1252, 0.1319] |
| always_escalate | avg_security_risk | 0.4088 | [0.4031, 0.4148] |
| always_escalate | avg_accessibility_burden | 0.05 | [0.05, 0.05] |
| always_escalate | avg_privacy_exposure | 0.2757 | [0.2693, 0.2823] |
| always_escalate | avg_energy_score | 0.5 | [0.5, 0.5] |
| always_escalate | governance_externality | 0.2534 | [0.2528, 0.254] |
| always_verify | mitigation_accuracy | 0.0714 | [0.0684, 0.0745] |
| always_verify | avg_care_suppression | 0.3883 | [0.3813, 0.3954] |
| always_verify | avg_security_risk | 0.05 | [0.05, 0.05] |
| always_verify | avg_accessibility_burden | 0.329 | [0.3242, 0.3338] |
| always_verify | avg_privacy_exposure | 0.05 | [0.05, 0.05] |
| always_verify | avg_energy_score | 0.5 | [0.5, 0.5] |
| always_verify | governance_externality | 0.2383 | [0.2365, 0.2402] |
| maximum_review | mitigation_accuracy | 0.1429 | [0.139, 0.1467] |
| maximum_review | avg_care_suppression | 0.3883 | [0.3812, 0.3953] |
| maximum_review | avg_security_risk | 0.05 | [0.05, 0.05] |
| maximum_review | avg_accessibility_burden | 0.329 | [0.3242, 0.3337] |
| maximum_review | avg_privacy_exposure | 0.05 | [0.05, 0.05] |
| maximum_review | avg_energy_score | 0.9 | [0.9, 0.9] |
| maximum_review | governance_externality | 0.2783 | [0.2764, 0.2803] |
| edgecase_adaptive | mitigation_accuracy | 1.0 | [1.0, 1.0] |
| edgecase_adaptive | avg_care_suppression | 0.2086 | [0.204, 0.2132] |
| edgecase_adaptive | avg_security_risk | 0.2514 | [0.2484, 0.2544] |
| edgecase_adaptive | avg_accessibility_burden | 0.1971 | [0.1923, 0.202] |
| edgecase_adaptive | avg_privacy_exposure | 0.1543 | [0.15, 0.1586] |
| edgecase_adaptive | avg_energy_score | 0.3286 | [0.3261, 0.3312] |
| edgecase_adaptive | governance_externality | 0.2187 | [0.2173, 0.2201] |

## Paired Wilcoxon signed-rank test: Adaptive EdgeCase vs. each baseline, mitigation_score

Matched by (seed, case_id) - same benchmark instance, both policies.

| Baseline | n pairs | n nonzero diffs | Mean diff (adaptive - baseline) | Statistic | p-value |
| --- | --- | --- | --- | --- | --- |
| strict_block | 12600 | 12600 | 0.9286 | 0.0 | 0.000e+00 |
| always_escalate | 12600 | 12600 | 0.9286 | 0.0 | 0.000e+00 |
| maximum_review | 12600 | 12600 | 0.8571 | 0.0 | 0.000e+00 |
