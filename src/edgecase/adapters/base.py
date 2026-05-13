from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseAdapter(ABC):
    name: str = "base"

    @abstractmethod
    def generate(self, prompt: str, system: Optional[str] = None) -> Dict[str, Any]:
        raise NotImplementedError
