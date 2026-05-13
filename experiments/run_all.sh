#!/usr/bin/env bash
set -euo pipefail

python experiments/generate_benchmark.py
python experiments/run_full_evaluation.py
python experiments/summarize_full_evaluation.py
python experiments/plot_full_evaluation.py
python experiments/run_policy_comparison.py
python experiments/build_tradeoff_frontier.py
python experiments/simulate_collision_network.py
python experiments/generate_governance_trajectories.py
python experiments/generate_runtime_replay.py

echo "All EdgeCase experiments completed."
