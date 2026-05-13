<div align="right">

<img src="website/public/edgecase-logo.png" alt="EdgeCase logo" width="170"/>

### Conflict-Aware Assurance for Agentic AI Systems

EdgeCase detects and manages **boundary collisions** where valid governance obligations recommend incompatible actions:  
**block vs escalate**, **verify vs accessibility**, **privacy vs safeguarding**, and **safety vs energy efficiency**.

<br/>

![Python](https://img.shields.io/badge/python-3.10%2B-101010?style=for-the-badge&logo=python)
![TypeScript](https://img.shields.io/badge/typescript-website-101010?style=for-the-badge&logo=typescript)
![Next.js](https://img.shields.io/badge/next.js-vercel-101010?style=for-the-badge&logo=nextdotjs)
![FastAPI](https://img.shields.io/badge/fastapi-api-101010?style=for-the-badge&logo=fastapi)
![D3](https://img.shields.io/badge/d3-visualizations-ff2a00?style=for-the-badge&logo=d3dotjs)
![Status](https://img.shields.io/badge/status-research_artifact-ff2a00?style=for-the-badge)

</div>

---

## Overview

Agentic AI systems are often evaluated as if security, fairness, privacy, accessibility, care, and efficiency were separable objectives. In high-stakes settings, they are not.

A single signal may indicate:

- a jailbreak attempt,
- a vulnerable user in crisis,
- a fraud pattern,
- a privacy-sensitive disclosure,
- or a case requiring costly oversight.

EdgeCase models governance as interacting obligations and detects moments where legitimate objectives recommend incompatible interventions.

---

## Core Idea

Most safety evaluations ask:

> Did the system violate a rule?

EdgeCase asks:

> Which obligations were active, did they conflict, what mitigation was selected, and what harms were displaced elsewhere?

---

## What EdgeCase Provides

| Component | Purpose |
|---|---|
| **Obligation Registry** | Models security, care, privacy, fairness, accessibility, compliance, and energy as triggerable governance obligations. |
| **Collision Detector** | Detects incompatible obligation pairs such as `security.block` vs `care.escalate`. |
| **Policy Engine** | Compares strict block, escalation-heavy, verification-heavy, maximum-review, and adaptive EdgeCase policies. |
| **Workflow Runtime** | Executes replayable governance DAGs with node-level runtime traces. |
| **Model Adapters** | Supports mock/reproducible runs and real-model adapters for model-backed workflows. |
| **Experiment Harness** | Generates benchmark results, policy comparisons, figures, and website-ready JSON. |
| **Interactive Website** | Provides D3 visualizations for collision networks, tradeoff frontiers, trajectories, and runtime replay. |
| **API Prototype** | Exposes a FastAPI `/v1/detect` endpoint for collision detection. |

---

## Repository Structure

```text
edgecase/
├── src/edgecase/
│   ├── adapters/          # Mock, OpenAI, Anthropic adapters
│   ├── policies/          # Governance policy baselines and adaptive routing
│   ├── runtime/           # Executable governance workflow DAG engine
│   ├── workflows/         # Domain workflows: banking, crisis support, healthcare
│   ├── detectors.py       # Collision detection logic
│   ├── registry.py        # Obligation registry
│   ├── models.py          # Core data models
│   └── metrics.py         # Evaluation metrics
│
├── experiments/           # Experiment runners and artifact generators
├── benchmarks/            # Paired scenario benchmark cases
├── datasets/              # Workflow and model cases
├── api/                   # FastAPI prototype
├── website/               # Next.js + D3 website
├── docs/                  # Concept and API docs
└── tests/                 # Unit tests
