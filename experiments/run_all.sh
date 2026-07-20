#!/usr/bin/env bash
set -euo pipefail

python experiments/build_edgecase_benchmark_v1.py
python experiments/run_full_evaluation.py
python experiments/summarize_full_evaluation.py
python experiments/plot_full_evaluation.py
python experiments/run_policy_comparison.py
python experiments/build_tradeoff_frontier.py
python experiments/simulate_collision_network.py
python experiments/generate_governance_trajectories.py
python experiments/generate_runtime_replay.py
python experiments/ablation_analysis.py
python experiments/runtime_dynamics_analysis.py
python experiments/run_multi_seed_evaluation.py
python experiments/oracle_tuned_baseline.py

echo "All EdgeCase experiments completed."
