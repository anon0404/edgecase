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
            label="LLM response generation",
            next_nodes=["router"],
        ),

        "router": RuntimeNode(
            id="router",
            type="router",
            label="Adaptive mitigation router",
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
            label="User request",
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
            label="Adaptive verification router",
            next_nodes=["audit"],
        ),

        "audit": RuntimeNode(
            id="audit",
            type="audit",
            label="Audit artifact export",
        ),
    }, "input"
