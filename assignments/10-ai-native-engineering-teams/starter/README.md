# Starter — LLM Gateway & Routing

A skeleton with two LLM tasks (easy: sentiment, hard: bug-explanation) routed through one
`call_model` choke point via **LiteLLM**. You fill in the routing and fallback.

## Setup
```bash
pip install -r requirements.txt
# set the keys your providers need, e.g.:
export OPENAI_API_KEY=...
python gateway_app.py
```
Tip: point `EASY_MODEL` at a local **Ollama** model (`ollama/llama3.1:8b`) to keep the
easy task's cost at $0.

## Your job (in `gateway_app.py`)
- `route()` — send the easy task to `EASY_MODEL`, the hard task to `HARD_MODEL`.
- `call_model()` — fall back to `FALLBACK_MODEL` on error/timeout (guard against loops).
- Measure latency + cost across 10 inputs per task and recommend a routing policy.

## Files
- `gateway_app.py` — the skeleton (two tasks + routing TODOs)
