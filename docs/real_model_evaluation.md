# Real-Model Evaluation

EdgeCase evaluates governance conflict consistency across heterogeneous model ecosystems.

The recommended AIES model set is:

| Provider | Role |
|---|---|
| Anthropic Claude | Proprietary frontier assistant with strong safety behavior |
| Google Gemini | Proprietary multimodal / ecosystem-integrated assistant |
| Qwen via Ollama | Open-weight or locally deployable model family |

The goal is not to rank models. The goal is to evaluate whether boundary collisions recur across model-backed workflows.

## Mock reproducibility run

EDGECASE_PROVIDER=mock EDGECASE_LIMIT=50 python experiments/run_real_model_evaluation.py

## Anthropic Claude

export EDGECASE_PROVIDER=anthropic
export EDGECASE_MODEL=claude-sonnet-4-5
export ANTHROPIC_API_KEY=YOUR_KEY
EDGECASE_LIMIT=50 python experiments/run_real_model_evaluation.py

## Google Gemini

export EDGECASE_PROVIDER=gemini
export EDGECASE_MODEL=gemini-2.5-pro
export GEMINI_API_KEY=YOUR_KEY
EDGECASE_LIMIT=50 python experiments/run_real_model_evaluation.py

## Qwen through Ollama

Install Ollama and pull Qwen:

ollama pull qwen2.5:7b

Run the evaluation:

export EDGECASE_PROVIDER=qwen
export EDGECASE_MODEL=qwen2.5:7b
EDGECASE_LIMIT=50 python experiments/run_real_model_evaluation.py

For larger machines, use a larger Qwen model if available locally.
