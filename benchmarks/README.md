# benchmarks/

`paired_scenarios.jsonl` is the earliest prototype fixture (9 hand-written
scenarios, no generator script), used only by `experiments/run_benchmark.py`,
which `run_all.sh` does not call. It is not the source of any paper-reported
result. The current benchmark lives in `datasets/edgecase_benchmark_v1.jsonl`
(see `datasets/README.md`).
