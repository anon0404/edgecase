from edgecase.models import CollisionReport, Externalities
from edgecase.models import Trace
from .base import BasePolicy

class VerificationPolicy(BasePolicy):
    name = "always_verify"

    def apply(self, trace: Trace) -> CollisionReport:
        return CollisionReport(
            collision_detected=False,
            recommended_mitigation="verify",
            externalities=Externalities(
                care_suppression_risk=0.32,
                security_risk=0.28,
                accessibility_burden=0.84,
                privacy_exposure=0.18,
                energy_cost="medium",
            ),
            audit={
                "policy": self.name,
                "decision": "verify",
            },
        )
