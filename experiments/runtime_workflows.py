from edgecase.runtime.nodes import RuntimeNode

def crisis_workflow():
    return {
        "input": RuntimeNode(
            id="input",
            type="input",
            label="User input",
            next_nodes=["classifier"],
            metadata={"step": 1},
        ),

        "classifier": RuntimeNode(
            id="classifier",
            type="classifier",
            label="Risk classifier",
            next_nodes=["validator"],
            signals=["policy_evasion"],
            metadata={"step": 2},
        ),

        "validator": RuntimeNode(
            id="validator",
            type="validator",
            label="Safety validator",
            next_nodes=["care_router"],
            signals=["self_harm"],
            metadata={"step": 3},
        ),

        "care_router": RuntimeNode(
            id="care_router",
            type="router",
            label="Adaptive mitigation router",
            next_nodes=["audit"],
            metadata={"step": 4},
        ),

        "audit": RuntimeNode(
            id="audit",
            type="audit",
            label="Audit artifact export",
            metadata={"step": 5},
        ),
    }, "input"

def banking_workflow():
    return {
        "input": RuntimeNode(
            id="input",
            type="input",
            label="Account access request",
            next_nodes=["fraud"],
            metadata={"step": 1},
        ),

        "fraud": RuntimeNode(
            id="fraud",
            type="classifier",
            label="Fraud detector",
            next_nodes=["accessibility"],
            signals=["fraud_risk"],
            metadata={"step": 2},
        ),

        "accessibility": RuntimeNode(
            id="accessibility",
            type="validator",
            label="Accessibility evaluator",
            next_nodes=["router"],
            signals=["language_barrier"],
            metadata={"step": 3},
        ),

        "router": RuntimeNode(
            id="router",
            type="router",
            label="Adaptive verification router",
            next_nodes=["audit"],
            metadata={"step": 4},
        ),

        "audit": RuntimeNode(
            id="audit",
            type="audit",
            label="Audit artifact export",
            metadata={"step": 5},
        ),
    }, "input"
