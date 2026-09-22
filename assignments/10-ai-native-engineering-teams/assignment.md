# Week 10 — AI-Native Teams: Gateway, Routing & Cost

## Overview
On an AI-native team, model calls are infrastructure — and infrastructure needs a
control plane. This capstone-style week has you stand up an **LLM gateway** in front of
an application, **route** requests across models by task, and produce a **cost/latency
report** plus a proposal for your team's **standardized stack**. This is the one
assignment with no direct analog in the reference course — it targets how AI-native
teams actually operate.

## Learning goals
- Put a gateway (LiteLLM or OpenRouter) between your app and multiple model providers.
- Implement **model routing**: cheap/fast models for easy tasks, stronger models for
  hard ones, with fallback.
- Measure and optimize **cost, latency, and quality** tradeoffs.
- Articulate a standardized team stack and its guardrails.

---

## Choose a gateway
- **[LiteLLM](https://github.com/BerriAI/litellm)** — self-hostable proxy exposing an
  OpenAI-compatible API over many providers; supports routing, fallbacks, budgets,
  and logging.
- **[OpenRouter](https://openrouter.ai/)** — hosted gateway with one API across many
  models and per-request pricing.
Either is fine; you may mix a hosted model with a local Ollama model.

## The app (build or reuse a small one)
Use a small app with **at least two distinct LLM tasks** of different difficulty. Build
`ai-team-gateway/` or reuse a prior week's app. Example tasks:
- **Easy/cheap:** classify or tag short text, extract fields, format output.
- **Hard/expensive:** multi-step reasoning, code generation, or long-document summary.

## Part 1 — Put a gateway in front
Route **all** model calls through the gateway (no direct provider SDK calls in app
code). Configure at least **three** models spanning at least two providers (a small
model, a large model, and a local/OSS model are ideal).

## Part 2 — Model routing
Implement routing so each task hits an appropriate model:
- Cheap/fast model for the easy task; stronger model for the hard task.
- A **fallback** when the primary errors or times out.
- (Optional) a quality gate that escalates to a stronger model if the cheap one's
  output fails a check.

## Part 3 — Measure & optimize
Run a fixed benchmark set (e.g., 20 inputs per task) through your routing and record,
per model/route: **cost per request, latency, and a quality score** (your rubric or a
simple LLM-as-judge). Then propose a routing policy that **cuts cost** while keeping
quality acceptable, and show the projected savings.

## Part 4 — Standardized team stack
Write a one-page proposal for how a 5-person AI-native team would standardize on this
setup: gateway, model menu + routing rules, secret/key management, budget/rate limits,
logging/observability, and how humans stay in the loop. Note the top risks.

## Deliverables
Push `ai-team-gateway/` and a `writeup.md` with:
1. Gateway config (models, providers, routing/fallback rules) — keys via env, **never
   committed**.
2. A results table: cost, latency, and quality per model/route across your benchmark.
3. Your optimized routing policy and projected cost savings vs. "always use the big model."
4. The one-page standardized-team-stack proposal.

## Evaluation (100 pts)
- 25 — Gateway correctly fronts all calls; 3+ models across 2+ providers.
- 25 — Working task-aware routing with a fallback.
- 25 — Honest cost/latency/quality benchmark with a defensible optimization.
- 15 — Standardized-team-stack proposal.
- 10 — Clean `writeup.md`, no committed secrets.

## References
- LiteLLM: https://docs.litellm.ai/
- OpenRouter: https://openrouter.ai/docs
