# EdgeCase

Conflict-aware assurance for security, ethics, and energy trade-offs in agentic systems.

EdgeCase models governance as interacting obligations and detects boundary collisions where legitimate objectives recommend incompatible actions, such as block versus escalate, verify versus accessibility, privacy versus safeguarding, or safety versus energy efficiency.

## Architecture

Agent Workflow
→ Trace Instrumentation
→ Obligation Registry
→ Collision Detector
→ Mitigation Router
→ Audit Artifact
→ Evaluation + Visualization

## Install

python -m pip install -e .

## Minimal example

from edgecase import Registry, Trace, detect

registry = Registry.default()

trace = Trace(
    signals=["jailbreak", "self_harm"],
    workflow="assistant_response"
)

report = detect(trace, registry)
print(report.model_dump_json(indent=2))

## Run experiments

./experiments/run_all.sh

## Run real-model evaluation

EdgeCase supports model-backed evaluation across Anthropic Claude, Google Gemini, and Qwen through Ollama.

### Mock

EDGECASE_PROVIDER=mock EDGECASE_LIMIT=50 python experiments/run_real_model_evaluation.py

### Anthropic Claude

export EDGECASE_PROVIDER=anthropic
export EDGECASE_MODEL=claude-sonnet-4-5
export ANTHROPIC_API_KEY=YOUR_KEY
python experiments/run_real_model_evaluation.py

### Google Gemini

export EDGECASE_PROVIDER=gemini
export EDGECASE_MODEL=gemini-2.5-pro
export GEMINI_API_KEY=YOUR_KEY
python experiments/run_real_model_evaluation.py

### Qwen through Ollama

ollama pull qwen2.5:7b
export EDGECASE_PROVIDER=qwen
export EDGECASE_MODEL=qwen2.5:7b
python experiments/run_real_model_evaluation.py

## Repository structure

src/edgecase/              Core Python package
src/edgecase/runtime/      Runtime DAG execution engine
src/edgecase/benchmark/    Benchmark generation
experiments/               Evaluation scripts
datasets/                  Generated and hand-authored cases
website/                   Vercel site
docs/                      Methodology and reproducibility docs
tests/                     Unit tests

## Research framing

EdgeCase is not a model leaderboard. It evaluates how governance objectives interact during agentic execution and whether mitigation strategies externalize harm across security, care, accessibility, privacy, and environmental dimensions.
