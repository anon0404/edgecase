<div align="center">

# EdgeCase

### Conflict-aware assurance for security, ethics, and energy trade-offs in agentic systems

<p align="center">
  <a href="https://edgecase-two.vercel.app">
    <img src="https://img.shields.io/badge/Website-EdgeCase-black?style=for-the-badge">
  </a>
  <a href="https://github.com/anon0404/edgecase">
    <img src="https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github">
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/runtime-governance-red">
  <img src="https://img.shields.io/badge/agentic-systems-black">
  <img src="https://img.shields.io/badge/conflict-aware-orange">
  <img src="https://img.shields.io/badge/governance-observability-darkred">
  <img src="https://img.shields.io/badge/security-ethics-black">
  <img src="https://img.shields.io/badge/energy-tradeoffs-orange">
</p>

</div>

---

## What is EdgeCase?

EdgeCase is a conflict-aware governance framework for agentic AI systems.

Instead of treating security, care, fairness, accessibility, privacy, and efficiency as separable objectives, EdgeCase models them as:

- interacting obligations,
- runtime governance states,
- and measurable trade-offs.

The framework detects **boundary collisions** where legitimate objectives recommend incompatible actions:

| Collision | Example |
|---|---|
| Block vs Escalate | jailbreak signal + self-harm disclosure |
| Verify vs Accessibility | fraud prevention vs disability burden |
| Privacy vs Safeguarding | data minimization vs escalation evidence |
| Safety vs Energy | deeper review vs compute efficiency |
| Explain vs Exploitability | transparency vs policy gaming |
| Memory Care vs Poisoning | personalization vs memory attacks |
| Fairness vs Personalization | tailored support vs stereotyping risk |

---

# Core Architecture

```text
Agent Workflow
      ↓
Trace Instrumentation
      ↓
Obligation Registry
      ↓
Collision Detector
      ↓
Mitigation Router
      ↓
Audit Artifact
      ↓
Evaluation + Visualization
```

---

# Key Features

## Runtime governance observability

Track:
- workflow routing,
- tool usage,
- memory operations,
- escalation paths,
- validator execution,
- mitigation selection,
- governance state transitions.

---

## Conflict-aware mitigation

Move beyond:

allow / block

EdgeCase supports:
- constrain-and-escalate,
- adaptive verification,
- split logging,
- layered explanation,
- adaptive review depth,
- typed memory isolation,
- bounded personalization.

---

## Agentic workflow replay

Replay governance trajectories over:
- branching workflows,
- sequential interactions,
- model/tool orchestration,
- escalation chains,
- externality propagation.

---

## Governance trade-off analysis

Measure:
- security risk,
- care suppression,
- accessibility burden,
- privacy exposure,
- energy cost,
- mitigation accuracy,
- aggregate governance externality (`Xk`).

---

# Interactive Website

### Live system:
https://edgecase-two.vercel.app

Includes:
- collision network simulation,
- governance trajectory replay,
- runtime workflow tracing,
- trade-off frontier visualization,
- interactive governance explorer.

---

# Installation

```bash
python -m pip install -e .
python -m pip install -r requirements.txt
```

Requires Python 3.9+. `requirements.txt` includes everything needed to run
the full experiment pipeline (`matplotlib`, `pytest`) and the real-model
evaluation (`anthropic`, `google-genai`); a local [Ollama](https://ollama.com)
install with `qwen2.5:7b` pulled is needed for the open-weight comparison
(see below).

---

# Minimal Example

```python
from edgecase import Registry, Trace, detect

registry = Registry.default()

trace = Trace(
    signals=["jailbreak", "self_harm"],
    workflow="assistant_response",
)

report = detect(trace, registry)

print(report.model_dump_json(indent=2))
```

---

# Run Full Experiment Pipeline

```bash
./experiments/run_all.sh
```

This is the single entry point for reproducing every table in the paper
from scratch. In order, it:

1. builds `datasets/edgecase_benchmark_v1.jsonl` — 1,260 instances across 7
   domains (`experiments/build_edgecase_benchmark_v1.py`), plus
   `datasets/splits/{train,validation,test}.jsonl`;
2. runs the full policy comparison (5 policies × 1,260 cases) and writes
   `experiments/tables/full_evaluation_summary.md` (governance tradeoffs
   table, mitigation accuracy, and `Xk` under both severity-weighted and
   uniform dimension weighting);
3. builds the tradeoff frontier and website visualization data;
4. runs the deterministic ablation analysis
   (`experiments/ablation_analysis.py`), writing
   `experiments/tables/ablation_analysis.md` — mitigation accuracy with the
   obligation registry, collision detection, adaptive routing, and runtime
   instrumentation each disabled in turn;
5. runs the runtime dynamics analysis
   (`experiments/runtime_dynamics_analysis.py`), writing
   `experiments/tables/runtime_dynamics_summary.md` — what fraction of
   detected collisions require the full signal set versus a fast
   adversarial-pattern-only pre-filter.

`datasets/README.md` documents a few legacy fixture files
(`workflow_cases.jsonl`, `model_cases.jsonl`, `edgecase_benchmark.jsonl`)
kept for reference but not used by this pipeline or any reported result.

---

# Real-Model Evaluation

EdgeCase evaluates governance conflict consistency, and each model's actual
alignment with EdgeCase's recommended mitigation, across heterogeneous
model ecosystems.

| Model ecosystem | Role |
|---|---|
| Claude | frontier aligned assistant |
| Gemini | integrated long-context ecosystem |
| Qwen | open-weight deployable workflow model |

Collision detection itself runs on each case's ground-truth input signals
(properties of the prompt, not of the model), so it is identical across
providers by design — reported as `mitigation_accuracy_ground_truth_signals`,
a wiring sanity check, not a cross-model finding. The metric that actually
depends on model behavior is `response_alignment`: a heuristic keyword
classifier (`src/edgecase/response_classifier.py`) scores what fraction of
the detected collision's two colliding obligation actions each model's
*response* actually exhibits. Treat it as directional, not precise.

Run each provider, then summarize:

```bash
export EDGECASE_PER_DOMAIN=20   # stratified sample, 20 cases/domain (140 total)
# use EDGECASE_PER_DOMAIN=180 for the full 1,260-case benchmark (hours per provider)

export EDGECASE_PROVIDER=anthropic
export EDGECASE_MODEL=claude-sonnet-4-5
export ANTHROPIC_API_KEY=YOUR_KEY
python experiments/run_real_model_evaluation.py

export EDGECASE_PROVIDER=gemini
export EDGECASE_MODEL=gemini-2.5-pro
export GEMINI_API_KEY=YOUR_KEY
python experiments/run_real_model_evaluation.py

ollama pull qwen2.5:7b
export EDGECASE_PROVIDER=qwen
export EDGECASE_MODEL=qwen2.5:7b
python experiments/run_real_model_evaluation.py

python experiments/summarize_real_model_evaluation.py
```

This writes `experiments/tables/real_model_evaluation_summary.md` and, per
provider, `experiments/results/real_models/summary_<provider>_<model>.json`
with `governance_externality`, `avg_response_alignment`,
`avg_latency_ms`, and `avg_tokens_estimate`. This step makes real API calls
and incurs real cost/time — a 140-case stratified sample takes roughly
10-40 minutes per provider depending on latency; the full benchmark takes
several hours per provider run serially.

---

# Repository Structure

```text
src/edgecase/
├── benchmark/         legacy prototype benchmark generator (superseded)
├── runtime/            executable workflow engine
├── adapters/           model integrations (Anthropic, Gemini, Qwen/Ollama, mock)
├── policies/           mitigation strategies (rigid baselines + adaptive)
├── registry.py         obligation registry
├── detectors.py        collision detection
├── metrics.py          aggregate governance externality (Xk)
└── response_classifier.py   heuristic model-response classifier

experiments/           evaluation pipelines (see run_all.sh for the canonical order)
datasets/              generated benchmarks (see datasets/README.md)
benchmarks/            earliest prototype fixture, superseded (see benchmarks/README.md)
website/               Vercel deployment
docs/                  methodology + reproducibility notes
tests/                 unit + integration tests
```

---

# Research Positioning

EdgeCase is **not**:
- a model leaderboard,
- an alignment benchmark,
- or a refusal optimization framework.

Instead, it evaluates:

> how governance obligations interact during agentic execution,
> and whether safety interventions externalize harm into other domains.

---

# Citation

```bibtex
@misc{edgecase2026,
  title={EdgeCase: Conflict-Aware Assurance for Security, Ethics and Energy Trade-offs in Agentic Systems},
  author={Anonymous Authors},
  year={2026}
}
```
