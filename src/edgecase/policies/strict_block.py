from edgecase.models import CollisionReport, Externalities
from edgecase.models import Trace
from .base import BasePolicy

class StrictBlockPolicy(BasePolicy):
    name = "strict_block"

    def apply(self, trace: Trace) -> CollisionReport:
        return CollisionReport(
            collision_detected=False,
            recommended_mitigation="block",
            externalities=Externalities(
                care_suppression_risk=0.88,
                security_risk=0.12,
                accessibility_burden=0.44,
                privacy_exposure=0.08,
                energy_cost="low",
            ),
            audit={
                "policy": self.name,
                "decision": "block",
            },
        )
