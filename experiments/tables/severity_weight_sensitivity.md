# Severity-weight sensitivity sweep (20000 draws, ordering-constrained simplex)

Fraction of weight vectors respecting care > security > privacy > access > energy (the paper's stated normative ordering) under which Adaptive EdgeCase's Xk is lower than each baseline's, using point-estimate means from the 10-seed evaluation.

| Baseline | Baseline scoring | Adaptive scoring | Adaptive win rate | Paper's specific weights (0.30/0.15/0.20/0.25/0.10) |
| --- | --- | --- | --- | --- |
| strict_block | pole-based (original) | original (undetected=free) | 68.2% | baseline wins |
| strict_block | pole-based (original) | penalized (undetected=charged real cost) | 68.2% | baseline wins |
| strict_block | action-specific | original (undetected=free) | 0.0% | baseline wins |
| strict_block | action-specific | penalized (undetected=charged real cost) | 0.0% | baseline wins |
| always_escalate | pole-based (original) | original (undetected=free) | 79.4% | adaptive wins |
| always_escalate | pole-based (original) | penalized (undetected=charged real cost) | 79.4% | adaptive wins |
| always_escalate | action-specific | original (undetected=free) | 1.8% | baseline wins |
| always_escalate | action-specific | penalized (undetected=charged real cost) | 1.8% | baseline wins |
| maximum_review | pole-based (original) | original (undetected=free) | 93.7% | adaptive wins |
| maximum_review | pole-based (original) | penalized (undetected=charged real cost) | 93.7% | adaptive wins |
| maximum_review | action-specific | original (undetected=free) | 37.1% | adaptive wins |
| maximum_review | action-specific | penalized (undetected=charged real cost) | 37.1% | adaptive wins |
