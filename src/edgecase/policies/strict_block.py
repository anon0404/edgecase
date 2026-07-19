from edgecase.models import CollisionReport
from edgecase.models import Trace
from edgecase.registry import Registry
from .base import BasePolicy
from .rigid import rigid_externalities

BASE_FLOOR = {
    "care_suppression_risk": 0.05,
    "security_risk": 0.05,
    "accessibility_burden": 0.05,
    "privacy_exposure": 0.05,
}

class StrictBlockPolicy(BasePolicy):
    name = "strict_block"

    def __init__(self):
        self.registry = Registry.default()

    def apply(self, trace: Trace) -> CollisionReport:
        externalities = rigid_externalities(
            pole="restrictive",
            base_floor=BASE_FLOOR,
            energy_cost="low",
            trace=trace,
            registry=self.registry,
        )
        return CollisionReport(
            collision_detected=False,
            recommended_mitigation="block",
            externalities=externalities,
            audit={
                "policy": self.name,
                "decision": "block",
            },
        )
