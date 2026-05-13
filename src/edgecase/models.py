from typing import Dict, List, Literal, Optional
from pydantic import BaseModel, Field

Action = Literal[
    "allow",
    "block",
    "escalate",
    "verify",
    "minimize",
    "explain",
    "constrain",
    "reduce_compute",
    "increase_review",
]

class Obligation(BaseModel):
    name: str
    domain: str
    triggers: List[str]
    action: Action
    description: str = ""

class Trace(BaseModel):
    signals: List[str] = Field(default_factory=list)
    workflow: str = "unknown"
    user_context: Dict[str, str] = Field(default_factory=dict)
    route: Optional[str] = None
    model_calls: int = 0
    tokens_estimate: int = 0
    latency_ms: Optional[int] = None

class Externalities(BaseModel):
    care_suppression_risk: float = 0.0
    security_risk: float = 0.0
    accessibility_burden: float = 0.0
    privacy_exposure: float = 0.0
    energy_cost: str = "low"

class CollisionReport(BaseModel):
    collision_detected: bool
    collision_type: Optional[str] = None
    triggered_obligations: List[str] = Field(default_factory=list)
    recommended_mitigation: Optional[str] = None
    externalities: Externalities = Field(default_factory=Externalities)
    audit: Dict = Field(default_factory=dict)
