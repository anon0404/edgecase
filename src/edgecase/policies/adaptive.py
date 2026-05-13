from edgecase import detect, Registry
from edgecase.models import Trace

from .base import BasePolicy

class AdaptiveEdgeCasePolicy(BasePolicy):
    name = "edgecase_adaptive"

    def __init__(self):
        self.registry = Registry.default()

    def apply(self, trace: Trace):
        return detect(trace, self.registry)
