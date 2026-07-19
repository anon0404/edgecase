from edgecase.models import Externalities, Trace
from edgecase.registry import Registry

# Each obligation sits on one pole of its domain's collision: "restrictive"
# (adds control/friction) or "supportive" (preserves care/access/efficiency).
# A rigid policy always resolves in favor of one pole; when a case also
# triggers an obligation on the *other* pole, that obligation's demand goes
# unmet, and its home externality dimension takes the suppression penalty.
RESTRICTIVE_OBLIGATIONS = {
    "security.block",
    "fraud.verify",
    "privacy.minimize",
    "safety.increase_review",
    "memory.protect",
    "security.limit_exploitability",
    "fairness.calibrate",
}

OBLIGATION_HOME_DIMENSION = {
    "security.block": "security_risk",
    "care.escalate": "care_suppression_risk",
    "fraud.verify": "security_risk",
    "accessibility.reduce_burden": "accessibility_burden",
    "privacy.minimize": "privacy_exposure",
    "safeguarding.preserve_context": "care_suppression_risk",
    "energy.reduce_compute": None,
    "safety.increase_review": "security_risk",
    "memory.personalize": "accessibility_burden",
    "memory.protect": "privacy_exposure",
    "transparency.explain": "care_suppression_risk",
    "security.limit_exploitability": "security_risk",
    "fairness.calibrate": "care_suppression_risk",
}

SUPPRESSION_BONUS = 0.55

def rigid_externalities(
    pole: str,
    base_floor: dict,
    energy_cost: str,
    trace: Trace,
    registry: Registry = None,
) -> Externalities:
    registry = registry or Registry.default()
    triggered = registry.triggered_by(trace.signals)

    dims = dict(base_floor)
    for obligation in triggered:
        obligation_pole = "restrictive" if obligation.name in RESTRICTIVE_OBLIGATIONS else "supportive"
        if obligation_pole == pole:
            continue
        dimension = OBLIGATION_HOME_DIMENSION.get(obligation.name)
        if dimension:
            dims[dimension] = min(1.0, dims[dimension] + SUPPRESSION_BONUS)

    return Externalities(energy_cost=energy_cost, **dims)
