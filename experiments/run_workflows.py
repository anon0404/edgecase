import json
from pathlib import Path

from edgecase.workflows import BankingWorkflow, CrisisWorkflow, HealthcareWorkflow

DATA = Path("datasets/workflow_cases.jsonl")
OUT = Path("experiments/results/workflow_results.json")

WORKFLOWS = {
    "banking": BankingWorkflow(),
    "crisis": CrisisWorkflow(),
    "healthcare": HealthcareWorkflow(),
}

def main():
    cases = [json.loads(line) for line in DATA.read_text().splitlines()]
    results = []

    for case in cases:
        workflow = WORKFLOWS[case["workflow"]]
        results.append(workflow.run(case))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, indent=2))

    summary = {}
    for row in results:
        domain = row["domain"]
        report = row["edgecase_report"]
        summary.setdefault(domain, {
            "cases": 0,
            "collisions": 0,
            "model_calls": 0,
            "tokens": 0,
        })
        summary[domain]["cases"] += 1
        summary[domain]["collisions"] += int(report["collision_detected"])
        summary[domain]["model_calls"] += row["trace"]["model_calls"]
        summary[domain]["tokens"] += row["trace"]["tokens_estimate"]

    for domain, values in summary.items():
        values["collision_rate"] = values["collisions"] / values["cases"]
        values["avg_model_calls"] = values["model_calls"] / values["cases"]
        values["avg_tokens"] = values["tokens"] / values["cases"]

    Path("experiments/results/workflow_summary.json").write_text(
        json.dumps(summary, indent=2)
    )

    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
