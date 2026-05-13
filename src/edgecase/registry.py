from .models import Obligation

class Registry:
    def __init__(self):
        self.obligations = []

    def add(self, obligation: Obligation) -> None:
        self.obligations.append(obligation)

    def triggered_by(self, signals):
        signal_set = set(signals)
        return [
            obligation
            for obligation in self.obligations
            if signal_set.intersection(obligation.triggers)
        ]

    @classmethod
    def default(cls):
        registry = cls()

        registry.add(Obligation(
            name="security.block",
            domain="security",
            triggers=["jailbreak", "malicious_request", "policy_evasion"],
            action="block",
            description="Prevent unsafe or adversarial assistance."
        ))

        registry.add(Obligation(
            name="care.escalate",
            domain="care",
            triggers=["self_harm", "crisis", "coercion", "abuse_disclosure"],
            action="escalate",
            description="Escalate credible vulnerability or crisis signals."
        ))

        registry.add(Obligation(
            name="fraud.verify",
            domain="security",
            triggers=["fraud_risk", "account_anomaly", "identity_risk"],
            action="verify",
            description="Increase verification when fraud risk is present."
        ))

        registry.add(Obligation(
            name="accessibility.reduce_burden",
            domain="accessibility",
            triggers=["disability_signal", "language_barrier", "distress"],
            action="constrain",
            description="Avoid disproportionate interaction burden."
        ))

        registry.add(Obligation(
            name="privacy.minimize",
            domain="privacy",
            triggers=["sensitive_data", "private_context"],
            action="minimize",
            description="Minimize retention and exposure of sensitive data."
        ))

        registry.add(Obligation(
            name="safeguarding.preserve_context",
            domain="safeguarding",
            triggers=["abuse_disclosure", "self_harm", "coercion"],
            action="increase_review",
            description="Preserve protected evidence for safeguarding review."
        ))

        registry.add(Obligation(
            name="energy.reduce_compute",
            domain="environment",
            triggers=["low_risk", "compute_pressure", "latency_constraint"],
            action="reduce_compute",
            description="Avoid unnecessary compute-intensive processing."
        ))

        registry.add(Obligation(
            name="safety.increase_review",
            domain="safety",
            triggers=["high_risk", "uncertain", "regulated_advice"],
            action="increase_review",
            description="Increase review depth for high-risk cases."
        ))

        return registry
