# Robustness matrix: Adaptive EdgeCase vs. each baseline on aggregate severity-weighted Xk

| Baseline | Baseline scoring | Baseline Xk | Adaptive scoring | Adaptive Xk | Verdict |
| --- | --- | --- | --- | --- | --- |
| strict_block | pole-based (original) | 0.2083 [0.2065,0.2103] | original (undetected=free) | 0.2187 [0.2173,0.2201] | Baseline wins (lower Xk, non-overlapping) |
| strict_block | pole-based (original) | 0.2083 [0.2065,0.2103] | penalized (undetected=charged real cost) | 0.2187 [0.2173,0.2201] | Baseline wins (lower Xk, non-overlapping) |
| strict_block | action-specific | 0.1831 [0.1821,0.1841] | original (undetected=free) | 0.2187 [0.2173,0.2201] | Baseline wins (lower Xk, non-overlapping) |
| strict_block | action-specific | 0.1831 [0.1821,0.1841] | penalized (undetected=charged real cost) | 0.2187 [0.2173,0.2201] | Baseline wins (lower Xk, non-overlapping) |
| always_escalate | pole-based (original) | 0.2534 [0.2528,0.254] | original (undetected=free) | 0.2187 [0.2173,0.2201] | Adaptive EdgeCase wins (lower Xk, non-overlapping) |
| always_escalate | pole-based (original) | 0.2534 [0.2528,0.254] | penalized (undetected=charged real cost) | 0.2187 [0.2173,0.2201] | Adaptive EdgeCase wins (lower Xk, non-overlapping) |
| always_escalate | action-specific | 0.2131 [0.2121,0.2141] | original (undetected=free) | 0.2187 [0.2173,0.2201] | Baseline wins (lower Xk, non-overlapping) |
| always_escalate | action-specific | 0.2131 [0.2121,0.2141] | penalized (undetected=charged real cost) | 0.2187 [0.2173,0.2201] | Baseline wins (lower Xk, non-overlapping) |
| maximum_review | pole-based (original) | 0.2783 [0.2764,0.2803] | original (undetected=free) | 0.2187 [0.2173,0.2201] | Adaptive EdgeCase wins (lower Xk, non-overlapping) |
| maximum_review | pole-based (original) | 0.2783 [0.2764,0.2803] | penalized (undetected=charged real cost) | 0.2187 [0.2173,0.2201] | Adaptive EdgeCase wins (lower Xk, non-overlapping) |
| maximum_review | action-specific | 0.2537 [0.2522,0.2551] | original (undetected=free) | 0.2187 [0.2173,0.2201] | Adaptive EdgeCase wins (lower Xk, non-overlapping) |
| maximum_review | action-specific | 0.2537 [0.2522,0.2551] | penalized (undetected=charged real cost) | 0.2187 [0.2173,0.2201] | Adaptive EdgeCase wins (lower Xk, non-overlapping) |
