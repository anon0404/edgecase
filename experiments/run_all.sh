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
python experiments/rigid_baseline_action_scoring.py
python experiments/undetected_penalty_analysis.py
python experiments/robustness_matrix.py
python experiments/severity_weight_sensitivity.py
python experiments/template_diversity_analysis.py
python experiments/specification_bug_analysis.py
python experiments/build_edgecase_benchmark_v2.py

# Not included above (run manually when their inputs exist / real API cost applies):
#   experiments/energy_proxy_sensitivity.py         - needs experiments/results/real_models/
#                                                      summary_*.json from run_real_model_evaluation.py
#                                                      (real, costed API calls; not part of this pipeline)
#   experiments/annotation/score_agreement.py       - needs completed annotator xlsx files
#                                                      (human annotation, not reproducible by this script)
#   experiments/llm_detector_baseline.py            - real, costed Claude API calls (304 calls:
#                                                      152-case sample x 2 conditions). Run:
#                                                        EDGECASE_PROVIDER=mock python experiments/llm_detector_baseline.py   # free dry run first
#                                                        EDGECASE_PROVIDER=anthropic ANTHROPIC_API_KEY=... python experiments/llm_detector_baseline.py
#   experiments/llm_detected_edgecase_routed.py     - real, costed Claude API calls (803 distinct
#                                                      (prompt, signal-set) keys, cached and applied
#                                                      across all 12,600 seed x case rows - see the
#                                                      script's own docstring for why 803, not 12,600).
#                                                      Checkpoints to disk every 50 calls (resumable).
#                                                        EDGECASE_PROVIDER=mock python experiments/llm_detected_edgecase_routed.py       # free dry run first
#                                                        EDGECASE_PROVIDER=anthropic ANTHROPIC_API_KEY=... python experiments/llm_detected_edgecase_routed.py
#                                                      Not yet re-run against EdgeCase-Benchmark-v2 (see Limitations) - flagged
#                                                      as the natural next check, not claimed as a result we have run.

echo "All EdgeCase experiments completed."
