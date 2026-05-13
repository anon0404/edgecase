# EdgeCase

Conflict-aware assurance for security, ethics, and energy trade-offs in agentic systems.

EdgeCase detects boundary collisions where legitimate governance obligations recommend incompatible actions, such as block vs escalate, verify vs accessibility, privacy vs safeguarding, and safety vs energy efficiency.

## Install

```bash
pip install -e .
# Example

from edgecase import Registry, Trace, detect

registry = Registry.default()

trace = Trace(
    signals=["jailbreak", "self_harm"],
    workflow="assistant_response"
)

report = detect(trace, registry)
print(report.model_dump_json(indent=2))

## Project structure

src/edgecase/       Core package
benchmarks/         Paired scenario benchmark
experiments/        Experiment runners
api/                Hosted API prototype
website/            Vercel site
tests/              Unit tests
docs/               Documentation
