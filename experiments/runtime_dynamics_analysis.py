import json
from pathlib import Path
from statistics import mean

from edgecase.detectors import INCOMPATIBLE_ACTIONS, detect
from edgecase.models import Trace
from edgecase.registry import Registry

DATA = Path("datasets/edgecase_benchmark_v1.jsonl")
OUT_JSON = Path("experiments/results/runtime_dynamics.json")
OUT_MD = Path("experiments/tables/runtime_dynamics_summary.md")

# Signals a cheap, fast first-pass filter could plausibly catch before any
# deeper (model-level) processing: explicit adversarial/policy-evasion
# patterns and directly-stated fraud/security red flags - the class of
# content a rule-based pre-filter is specifically built to catch quickly.
# Everything else (vulnerability disclosures, situational/contextual
# signals, procedural or fairness-related requests) is treated as only
# detectable once the pipeline engages more deeply with the content - this
# is a stated modeling assumption, not a measured fact, and is fixed here
# independent of what percentage it produces.
FAST_FILTER_SIGNALS = {
    "jailbreak", "policy_evasion", "malicious_request",
    "fraud_risk", "identity_risk", "account_anomaly",
    "policy_override", "adversarial_probe", "request_for_policy_details",
}

def tentative_action(trace, registry):
    triggered = registry.triggered_by(trace.signals)
    actions = sorted({o.action for o in triggered})
    return actions[0] if actions else None

def main():
    cases = [json.loads(line) for line in DATA.read_text().splitlines() if line.strip()]
    registry = Registry.default()

    rows = []
    for case in cases:
        step1_signals = [s for s in case["signals"] if s in FAST_FILTER_SIGNALS]
        full_signals = case["signals"]

        trace_step1 = Trace(signals=step1_signals, workflow=case["domain"])
        trace_full = Trace(signals=full_signals, workflow=case["domain"])

        report_step1 = detect(trace_step1, registry)
        report_full = detect(trace_full, registry)

        rows.append({
            "case_id": case["id"],
            "domain": case["domain"],
            "collision_detected_step1": report_step1.collision_detected,
            "collision_detected_full": report_full.collision_detected,
            "tentative_action_step1": tentative_action(trace_step1, registry),
            "final_mitigation_full": report_full.recommended_mitigation,
        })

    detected = [r for r in rows if r["collision_detected_full"]]
    delayed = [r for r in detected if not r["collision_detected_step1"]]
    immediate = [r for r in detected if r["collision_detected_step1"]]

    # Non-monotonic trajectory: at step 1, the system tentatively acts on a
    # single obligation (or nothing); once the full signal set is known, the
    # correct response is a different, bounded mitigation. A "revision" is
    # any detected-collision case where the step-1 tentative action isn't
    # even one of the two actions the final mitigation actually resolves.
    revised = 0
    for r in detected:
        collision_type = None
        for pair, (c_type, mitigation) in INCOMPATIBLE_ACTIONS.items():
            if mitigation == r["final_mitigation_full"]:
                collision_type = c_type
                action_pair = pair
                break
        if r["tentative_action_step1"] is None or r["tentative_action_step1"] not in action_pair:
            revised += 1

    summary = {
        "total_cases": len(rows),
        "collisions_detected_full": len(detected),
        "delayed_collisions": len(delayed),
        "delayed_rate_of_detected": round(len(delayed) / len(detected), 3) if detected else None,
        "immediate_collisions": len(immediate),
        "immediate_rate_of_detected": round(len(immediate) / len(detected), 3) if detected else None,
        "mitigation_revised_rate_of_detected": round(revised / len(detected), 3) if detected else None,
    }

    by_domain = {}
    for r in detected:
        by_domain.setdefault(r["domain"], {"detected": 0, "delayed": 0})
        by_domain[r["domain"]]["detected"] += 1
        if not r["collision_detected_step1"]:
            by_domain[r["domain"]]["delayed"] += 1
    for domain, counts in by_domain.items():
        counts["delayed_rate"] = round(counts["delayed"] / counts["detected"], 3)

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps({"summary": summary, "by_domain": by_domain, "rows": rows}, indent=2))

    with OUT_MD.open("w") as f:
        f.write("| Metric | Value |\n| --- | --- |\n")
        for k, v in summary.items():
            f.write(f"| {k} | {v} |\n")
        f.write("\n| Domain | Detected | Delayed | Delayed Rate |\n| --- | --- | --- | --- |\n")
        for domain, counts in sorted(by_domain.items()):
            f.write(f"| {domain} | {counts['detected']} | {counts['delayed']} | {counts['delayed_rate']} |\n")

    print(json.dumps(summary, indent=2))
    print(f"Wrote {OUT_JSON}, {OUT_MD}")

if __name__ == "__main__":
    main()
