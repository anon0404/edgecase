from abc import ABC, abstractmethod
from typing import Any, Dict
from edgecase import Trace, detect, Registry

class WorkflowResult(dict):
    pass

class BaseWorkflow(ABC):
    name: str = "base"

    def __init__(self):
        self.registry = Registry.default()

    @abstractmethod
    def run(self, case: Dict[str, Any]) -> WorkflowResult:
        raise NotImplementedError

    def evaluate(self, trace: Trace) -> dict:
        report = detect(trace, self.registry)
        return report.model_dump()
