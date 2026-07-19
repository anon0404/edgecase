from .models import CollisionReport, Externalities
from .registry import Registry

INCOMPATIBLE_ACTIONS = {
    frozenset(["block", "escalate"]): ("block_vs_escalate", "constrain_and_escalate"),
    frozenset(["verify", "constrain"]): ("verify_vs_accessibility", "adaptive_verification"),
    frozenset(["minimize", "increase_review"]): ("privacy_vs_safeguarding", "split_logging"),
    frozenset(["reduce_compute", "increase_review"]): ("safety_vs_energy", "adaptive_depth"),
    frozenset(["personalize", "protect_memory"]): ("memory_care_vs_memory_poisoning", "typed_memory"),
    frozenset(["explain", "limit_exploitability"]): ("explain_vs_exploitability", "layered_explanation"),
    frozenset(["personalize", "calibrate"]): ("fairness_vs_personalization", "bounded_personalization"),
}

def _score_externalities(collision_type, trace):
    if collision_type == "block_vs_escalate":
        return Externalities(care_suppression_risk=0.72, security_risk=0.41, energy_cost="low")
    if collision_type == "verify_vs_accessibility":
        return Externalities(accessibility_burden=0.78, security_risk=0.35, energy_cost="low")
    if collision_type == "privacy_vs_safeguarding":
        return Externalities(privacy_exposure=0.58, care_suppression_risk=0.44, energy_cost="medium")
    if collision_type == "safety_vs_energy":
        cost = "high" if trace.model_calls >= 3 or trace.tokens_estimate >= 3000 else "medium"
        return Externalities(security_risk=0.25, energy_cost=cost)
    if collision_type == "memory_care_vs_memory_poisoning":
        return Externalities(privacy_exposure=0.50, security_risk=0.45, energy_cost="medium")
    if collision_type == "explain_vs_exploitability":
        return Externalities(security_risk=0.30, accessibility_burden=0.20, energy_cost="low")
    if collision_type == "fairness_vs_personalization":
        return Externalities(care_suppression_risk=0.30, accessibility_burden=0.40, energy_cost="low")
    return Externalities()

def detect(trace, registry=None):
    registry = registry or Registry.default()
    triggered = registry.triggered_by(trace.signals)
    actions = {item.action for item in triggered}

    collision_type = None
    mitigation = None

    for pair, result in INCOMPATIBLE_ACTIONS.items():
        if pair.issubset(actions):
            collision_type, mitigation = result
            break

    return CollisionReport(
        collision_detected=collision_type is not None,
        collision_type=collision_type,
        triggered_obligations=[item.name for item in triggered],
        recommended_mitigation=mitigation,
        externalities=_score_externalities(collision_type, trace),
        audit={
            "workflow": trace.workflow,
            "signals": trace.signals,
            "actions": sorted(actions),
            "model_calls": trace.model_calls,
            "tokens_estimate": trace.tokens_estimate,
        },
    )
