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
  <img src="https://img.shields.io/badge/AIES-2026-orange?style=for-the-badge">
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
- typed memory isolation.

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
- mitigation stability.

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
```

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

This generates:
- benchmark datasets,
- collision traces,
- trade-off frontiers,
- runtime replay artifacts,
- statistical summaries,
- website visualization assets.

---

# Real-Model Evaluation

EdgeCase evaluates governance conflict consistency across heterogeneous model ecosystems.

| Model ecosystem | Role |
|---|---|
| Claude | frontier aligned assistant |
| Gemini | integrated long-context ecosystem |
| Qwen | open-weight deployable workflow model |

---

## Anthropic Claude

```bash
export EDGECASE_PROVIDER=anthropic
export EDGECASE_MODEL=claude-sonnet-4-5
export ANTHROPIC_API_KEY=YOUR_KEY

python experiments/run_real_model_evaluation.py
```

---

## Google Gemini

```bash
export EDGECASE_PROVIDER=gemini
export EDGECASE_MODEL=gemini-2.5-pro
export GEMINI_API_KEY=YOUR_KEY

python experiments/run_real_model_evaluation.py
```

---

## Qwen via Ollama

```bash
ollama pull qwen2.5:7b

export EDGECASE_PROVIDER=qwen
export EDGECASE_MODEL=qwen2.5:7b

python experiments/run_real_model_evaluation.py
```

---

# Repository Structure

```text
src/edgecase/
├── benchmark/        synthetic conflict generation
├── runtime/          executable workflow engine
├── adapters/         model integrations
├── policies/         mitigation strategies
├── visualization/    governance visualization
└── detectors/        collision detection

experiments/          evaluation pipelines
datasets/             generated benchmarks
website/              Vercel deployment
docs/                 methodology + reproducibility
tests/                unit + integration tests
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

# Paper

**EdgeCase: Conflict-Aware Assurance for Security, Ethics and Energy Trade-offs in Agentic Systems**

Target venue:

AAAI/ACM Conference on AI, Ethics, and Society (AIES) 2026

---

# Citation

```bibtex
@misc{edgecase2026,
  title={EdgeCase: Conflict-Aware Assurance for Security, Ethics and Energy Trade-offs in Agentic Systems},
  author={Anonymous Authors},
  year={2026}
}
```

