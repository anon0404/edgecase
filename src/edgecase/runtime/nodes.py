from dataclasses import dataclass, field
from typing import Dict, List, Optional
import uuid

@dataclass
class RuntimeNode:
    id: str

    type: str

    label: str

    next_nodes: List[str] = field(default_factory=list)

    conditional_routes: Dict[str, str] = field(default_factory=dict)

    signals: List[str] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)

@dataclass
class RuntimeEvent:
    timestamp: float

    node_id: str

    label: str

    type: str

    active_signals: List[str]

    obligations: List[str]

    collision: Optional[str]

    mitigation: Optional[str]

    metrics: Dict

    route_taken: Optional[str] = None

    event_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )
