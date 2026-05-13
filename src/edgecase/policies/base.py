from abc import ABC, abstractmethod
from typing import Dict

from edgecase.models import Trace, CollisionReport

class BasePolicy(ABC):
    name = "base"

    @abstractmethod
    def apply(self, trace: Trace) -> CollisionReport:
        raise NotImplementedError

    def externality_profile(
        self,
        care=0.0,
        security=0.0,
        accessibility=0.0,
        privacy=0.0,
        energy="low",
    ):
        return {
            "care_suppression_risk": care,
            "security_risk": security,
            "accessibility_burden": accessibility,
            "privacy_exposure": privacy,
            "energy_cost": energy,
        }
