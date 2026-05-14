from edgecase.runtime.nodes import RuntimeNode

def crisis_workflow():
    return {
        "input": RuntimeNode(
            id="input",
            type="input",
            label="User input",
            next_nodes=["classifier"],
        ),

        "classifier": RuntimeNode(
            id="classifier",
            type="classifier",
            label="Risk classifier",
            next_nodes=["model"],
        ),

        "model": RuntimeNode(
            id="model",
            type="model",
            label="LLM generation",
            next_nodes=["router"],
        ),

        "router": RuntimeNode(
            id="router",
            type="router",
            label="Governance router",

            conditional_routes={
                "escalate": "escalation",

                "verify": "verification",

                "review": "human_review",

                "respond": "response",
            },
        ),

        "escalation": RuntimeNode(
            id="escalation",
            type="audit",
            label="Protected escalation",
            next_nodes=["audit"],
        ),

        "verification": RuntimeNode(
            id="verification",
            type="audit",
            label="Adaptive verification",
            next_nodes=["audit"],
        ),

        "human_review": RuntimeNode(
            id="human_review",
            type="audit",
            label="Human review queue",
            next_nodes=["audit"],
        ),

        "response": RuntimeNode(
            id="response",
            type="audit",
            label="Standard response",
            next_nodes=["audit"],
        ),

        "audit": RuntimeNode(
            id="audit",
            type="audit",
            label="Audit artifact export",
        ),
    }, "input"

def banking_workflow():
    return {
        "input": RuntimeNode(
            id="input",
            type="input",
            label="Account request",
            next_nodes=["classifier"],
        ),

        "classifier": RuntimeNode(
            id="classifier",
            type="classifier",
            label="Fraud detector",
            next_nodes=["model"],
        ),

        "model": RuntimeNode(
            id="model",
            type="model",
            label="Verification assistant",
            next_nodes=["router"],
        ),

        "router": RuntimeNode(
            id="router",
            type="router",
            label="Verification router",

            conditional_routes={
                "verify": "verification",

                "respond": "response",
            },
        ),

        "verification": RuntimeNode(
            id="verification",
            type="audit",
            label="Adaptive verification",
            next_nodes=["audit"],
        ),

        "response": RuntimeNode(
            id="response",
            type="audit",
            label="Standard response",
            next_nodes=["audit"],
        ),

        "audit": RuntimeNode(
            id="audit",
            type="audit",
            label="Audit export",
        ),
    }, "input"
