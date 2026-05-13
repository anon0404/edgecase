from edgecase.models import CollisionReport, Externalities
from edgecase.models import Trace
from .base import BasePolicy

class EscalationPolicy(BasePolicy):
    name = "always_escalate"

    def apply(self, trace: Trace) -> CollisionReport:
        return CollisionReport(
            collision_detected=False,
            recommended_mitigation="escalate",
            externalities=Externalities(
                care_suppression_risk=0.18,
                security_risk=0.62,
                accessibility_burden=0.22,
                privacy_exposure=0.31,
                energy_cost="medium",
            ),
            audit={
                "policy": self.name,
                "decision": "escalate",
            },
        )
