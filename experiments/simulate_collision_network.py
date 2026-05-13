import json
import random
from pathlib import Path

OUT = Path("website/public/data")
OUT.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 404
random.seed(RANDOM_SEED)

COLLISION_TYPES = {
    "block_vs_escalate": {
        "signals": ["jailbreak", "policy_evasion", "self_harm", "crisis", "coercion"],
        "obligations": ["security.block", "care.escalate"],
        "mitigation": "constrain_and_escalate",
    },
    "verify_vs_accessibility": {
        "signals": ["fraud_risk", "identity_risk", "disability_signal", "language_barrier", "distress"],
        "obligations": ["fraud.verify", "accessibility.reduce_burden"],
        "mitigation": "adaptive_verification",
    },
    "privacy_vs_safeguarding": {
        "signals": ["sensitive_data", "private_context", "abuse_disclosure", "coercion"],
        "obligations": ["privacy.minimize", "safeguarding.preserve_context"],
        "mitigation": "split_logging",
    },
    "safety_vs_energy": {
        "signals": ["high_risk", "uncertain", "compute_pressure", "latency_constraint"],
        "obligations": ["safety.increase_review", "energy.reduce_compute"],
        "mitigation": "adaptive_depth",
    },
}

def score_collision(kind):
    if kind == "block_vs_escalate":
        return {
            "care_suppression": round(random.uniform(0.55, 0.92), 3),
            "security_risk": round(random.uniform(0.25, 0.55), 3),
            "accessibility_burden": round(random.uniform(0.05, 0.25), 3),
            "privacy_exposure": round(random.uniform(0.05, 0.25), 3),
            "energy_cost": round(random.uniform(0.10, 0.35), 3),
        }
    if kind == "verify_vs_accessibility":
        return {
            "care_suppression": round(random.uniform(0.20, 0.45), 3),
            "security_risk": round(random.uniform(0.25, 0.60), 3),
            "accessibility_burden": round(random.uniform(0.60, 0.95), 3),
            "privacy_exposure": round(random.uniform(0.10, 0.35), 3),
            "energy_cost": round(random.uniform(0.20, 0.45), 3),
        }
    if kind == "privacy_vs_safeguarding":
        return {
            "care_suppression": round(random.uniform(0.35, 0.70), 3),
            "security_risk": round(random.uniform(0.15, 0.40), 3),
            "accessibility_burden": round(random.uniform(0.05, 0.25), 3),
            "privacy_exposure": round(random.uniform(0.45, 0.85), 3),
            "energy_cost": round(random.uniform(0.25, 0.55), 3),
        }
    return {
        "care_suppression": round(random.uniform(0.10, 0.35), 3),
        "security_risk": round(random.uniform(0.20, 0.50), 3),
        "accessibility_burden": round(random.uniform(0.10, 0.35), 3),
        "privacy_exposure": round(random.uniform(0.05, 0.25), 3),
        "energy_cost": round(random.uniform(0.55, 0.95), 3),
    }

def simulate(n=240):
    cases = []
    nodes = {}
    links = []

    for i in range(n):
        kind = random.choice(list(COLLISION_TYPES.keys()))
        spec = COLLISION_TYPES[kind]

        signal_count = random.randint(2, min(4, len(spec["signals"])))
        signals = random.sample(spec["signals"], signal_count)

        severity = round(random.uniform(0.1, 1.0), 3)
        ambiguity = round(random.uniform(0.1, 1.0), 3)
        model_calls = random.randint(1, 6)
        tokens = random.randint(600, 8500)
        latency_ms = random.randint(220, 4800)

        externalities = score_collision(kind)

        case_id = f"sim_{i:04d}"
        case = {
            "id": case_id,
            "collision_type": kind,
            "signals": signals,
            "obligations": spec["obligations"],
            "mitigation": spec["mitigation"],
            "severity": severity,
            "ambiguity": ambiguity,
            "model_calls": model_calls,
            "tokens": tokens,
            "latency_ms": latency_ms,
            "externalities": externalities,
        }
        cases.append(case)

        collision_node = f"collision:{kind}"
        mitigation_node = f"mitigation:{spec['mitigation']}"

        nodes[collision_node] = {
            "id": collision_node,
            "label": kind.replace("_", " "),
            "type": "collision",
            "weight": nodes.get(collision_node, {}).get("weight", 0) + 1,
        }

        nodes[mitigation_node] = {
            "id": mitigation_node,
            "label": spec["mitigation"].replace("_", " "),
            "type": "mitigation",
            "weight": nodes.get(mitigation_node, {}).get("weight", 0) + 1,
        }

        links.append({
            "source": collision_node,
            "target": mitigation_node,
            "type": "resolved_by",
            "weight": 1,
        })

        for signal in signals:
            node_id = f"signal:{signal}"
            nodes[node_id] = {
                "id": node_id,
                "label": signal.replace("_", " "),
                "type": "signal",
                "weight": nodes.get(node_id, {}).get("weight", 0) + 1,
            }
            links.append({
                "source": node_id,
                "target": collision_node,
                "type": "triggers",
                "weight": 1,
            })

        for obligation in spec["obligations"]:
            node_id = f"obligation:{obligation}"
            nodes[node_id] = {
                "id": node_id,
                "label": obligation,
                "type": "obligation",
                "weight": nodes.get(node_id, {}).get("weight", 0) + 1,
            }
            links.append({
                "source": collision_node,
                "target": node_id,
                "type": "activates",
                "weight": 1,
            })

    aggregate = {}
    for kind in COLLISION_TYPES:
        subset = [c for c in cases if c["collision_type"] == kind]
        aggregate[kind] = {
            "count": len(subset),
            "avg_severity": round(sum(c["severity"] for c in subset) / len(subset), 3),
            "avg_ambiguity": round(sum(c["ambiguity"] for c in subset) / len(subset), 3),
            "avg_model_calls": round(sum(c["model_calls"] for c in subset) / len(subset), 3),
            "avg_tokens": round(sum(c["tokens"] for c in subset) / len(subset), 1),
            "avg_latency_ms": round(sum(c["latency_ms"] for c in subset) / len(subset), 1),
            "avg_externalities": {
                key: round(sum(c["externalities"][key] for c in subset) / len(subset), 3)
                for key in ["care_suppression", "security_risk", "accessibility_burden", "privacy_exposure", "energy_cost"]
            },
        }

    payload = {
        "metadata": {
            "name": "EdgeCase simulated collision network",
            "seed": RANDOM_SEED,
            "cases": len(cases),
            "description": "Synthetic agentic AI governance conflict simulation for interactive visualization."
        },
        "nodes": list(nodes.values()),
        "links": links,
        "cases": cases,
        "aggregate": aggregate,
    }

    (OUT / "collision_network.json").write_text(json.dumps(payload, indent=2))
    print(f"Wrote {OUT / 'collision_network.json'} with {len(nodes)} nodes, {len(links)} links, {len(cases)} cases.")

if __name__ == "__main__":
    simulate()
