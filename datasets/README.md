# EdgeCase Benchmark v1

`edgecase_benchmark_v1.jsonl` contains 1260 synthetic paired governance-conflict workflow instances.

The benchmark is designed for evaluating conflict-aware assurance in agentic systems. Each instance contains a workflow prompt, triggering signals, activated governance obligations, an expected boundary collision, and a reference mitigation strategy.

## Domains

| Domain | Instances |
|---|---:|
| crisis_support | 180 |
| banking_fintech | 180 |
| healthcare_triage | 180 |
| enterprise_copilot | 180 |
| education | 180 |
| moderation | 180 |
| public_benefits | 180 |

## Files

- `edgecase_benchmark_v1.jsonl`: full benchmark
- `edgecase_benchmark_schema.json`: field schema
- `splits/train.jsonl`: training/development split
- `splits/validation.jsonl`: validation split
- `splits/test.jsonl`: held-out test split

## Annotation provenance

This is a synthetic benchmark generated from paired governance-conflict templates. It is intended for reproducible evaluation, ablation studies, and workflow-level stress testing. It is not a dataset of real user conversations.

## Citation

If using this benchmark, cite the EdgeCase paper and repository.

## Other files in this directory

`workflow_cases.jsonl`, `model_cases.jsonl`, and `edgecase_benchmark.jsonl`
are earlier prototype fixtures (hand-written or from a superseded 4-domain
generator) used only by scripts `run_all.sh` does not call
(`run_workflows.py`, `run_model_workflows.py`, `run_real_model_evaluation.py`).
They are not the source of any paper-reported result.
