from typing import List, Optional

# Severity-ordered weighting for Xk: care suppression risks physical/
# psychological harm to a vulnerable user, the most severe and least
# reversible outcome in scope; security risk concerns system integrity and
# downstream unsafe completions; privacy exposure is serious but more
# remediable after the fact; accessibility burden is procedural friction
# with no safety dimension; energy cost is an operational externality on
# the system operator, not a harm to any stakeholder. Order: care > security
# > privacy > accessibility > energy. Weights (order matches the `deltas`
# list below: care, accessibility, privacy, security, energy):
SEVERITY_WEIGHTS = [0.30, 0.15, 0.20, 0.25, 0.10]

def aggregate_governance_externality(
    care_suppression: float,
    accessibility_burden: float,
    privacy_exposure: float,
    security_risk: float,
    energy_score: float,
    weights: Optional[List[float]] = None,
) -> float:
    """Xk = sum(lambda_i * delta_i), lambda_i uniform (1/5) by default."""
    deltas = [care_suppression, accessibility_burden, privacy_exposure, security_risk, energy_score]
    if weights is None:
        weights = [1 / len(deltas)] * len(deltas)
    return sum(w * d for w, d in zip(weights, deltas))
