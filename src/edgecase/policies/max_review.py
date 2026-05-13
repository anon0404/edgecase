from edgecase.models import CollisionReport, Externalities
from edgecase.models import Trace
from .base import BasePolicy

class MaximumReviewPolicy(BasePolicy):
    name = "maximum_review"

    def apply(self, trace: Trace) -> CollisionReport:
        return CollisionReport(
            collision_detected=False,
            recommended_mitigation="increase_review",
            externalities=Externalities(
                care_suppression_risk=0.21,
                security_risk=0.16,
                accessibility_burden=0.38,
                privacy_exposure=0.24,
                energy_cost="high",
            ),
            audit={
                "policy": self.name,
                "decision": "increase_review",
            },
        )
