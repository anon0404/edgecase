from .models import Trace, CollisionReport, Externalities

def always_block(trace: Trace) -> CollisionReport:
    return CollisionReport(
        collision_detected=False,
        recommended_mitigation="block",
        externalities=Externalities(care_suppression_risk=0.85, energy_cost="low"),
        audit={"baseline": "always_block", "signals": trace.signals},
    )

def always_escalate(trace: Trace) -> CollisionReport:
    return CollisionReport(
        collision_detected=False,
        recommended_mitigation="escalate",
        externalities=Externalities(security_risk=0.55, energy_cost="medium"),
        audit={"baseline": "always_escalate", "signals": trace.signals},
    )

def always_verify(trace: Trace) -> CollisionReport:
    return CollisionReport(
        collision_detected=False,
        recommended_mitigation="verify",
        externalities=Externalities(accessibility_burden=0.80, energy_cost="medium"),
        audit={"baseline": "always_verify", "signals": trace.signals},
    )

def strongest_stack(trace: Trace) -> CollisionReport:
    return CollisionReport(
        collision_detected=False,
        recommended_mitigation="maximum_review",
        externalities=Externalities(security_risk=0.15, accessibility_burden=0.45, energy_cost="high"),
        audit={"baseline": "strongest_stack", "signals": trace.signals},
    )
