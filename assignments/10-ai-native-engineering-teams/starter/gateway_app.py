"""AI-Native Teams — gateway + routing skeleton for Week 10.

Two LLM tasks of different difficulty, both routed through ONE gateway function so you
can swap/route models in one place. Fill in the routing TODOs.

Uses LiteLLM (https://docs.litellm.ai) as an OpenAI-compatible gateway across providers.
You may point EASY_MODEL at a local Ollama model and HARD_MODEL at a hosted one.

Setup:
    pip install -r requirements.txt
    export OPENAI_API_KEY=...        # or whatever your chosen providers need
Run:
    python gateway_app.py
"""
import time

import litellm

# TODO: choose real model ids for your providers (see litellm docs for the prefixes).
EASY_MODEL = "ollama/llama3.1:8b"      # cheap/fast
HARD_MODEL = "gpt-4o-mini"             # stronger
FALLBACK_MODEL = "ollama/llama3.1:8b"  # used if the primary errors


def call_model(model: str, prompt: str) -> str:
    """Single choke point for all model calls — route, log, and fall back here."""
    try:
        resp = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            timeout=60,
        )
        return resp["choices"][0]["message"]["content"].strip()
    except Exception as exc:  # noqa: BLE001
        # TODO: on failure, fall back to FALLBACK_MODEL (guard against infinite loops).
        raise


def route(task: str, prompt: str) -> str:
    """TODO: pick EASY_MODEL for the easy task and HARD_MODEL for the hard task."""
    model = EASY_MODEL  # TODO: change based on `task`
    started = time.time()
    out = call_model(model, prompt)
    print(f"[{task}] model={model} latency={time.time() - started:.2f}s")
    return out


# --- The two tasks -----------------------------------------------------------------
def classify_sentiment(review: str) -> str:  # EASY
    return route("easy", f"Reply with one word (positive/negative/neutral): {review}")


def explain_bug(code: str) -> str:  # HARD
    return route("hard", f"Explain the bug in this code and suggest a fix:\n{code}")


if __name__ == "__main__":
    print(classify_sentiment("This product totally changed my morning routine!"))
    print(explain_bug("def avg(xs): return sum(xs) / len(xs)  # crashes on []"))
