# Week 2 — Prompting Techniques: The Support-Desk Assistant

## Overview
To understand how coding agents work, you first need to understand the model at their
core. This week you'll hand-craft prompts using six foundational techniques, running
open models **locally with [Ollama](https://ollama.com/)** — no cloud keys, so you can
see exactly how each technique changes model behavior.

Instead of generic toy tasks, every technique targets one coherent domain: an
**AI support-desk assistant** for a small online store. Same skills as any prompting
lab; a scenario you'll actually reason about.

## Learning goals
- Run state-of-the-art open models locally and inspect their raw behavior.
- Implement and compare six prompting techniques.
- Build intuition for *why* LLMs are good at structured/coding tasks — and where they
  break without the right prompt scaffolding.

---

## Setup

1. Install **Ollama**:
   - macOS: `brew install --cask ollama && ollama serve`
   - Linux: `curl -fsSL https://ollama.com/install.sh | sh`
   - Windows: installer from [ollama.com/download](https://ollama.com/download)
   - Verify: `ollama -v`
2. Pull the models we'll use (once):
   ```bash
   ollama pull llama3.1:8b
   ollama pull mistral-nemo:12b
   ```
3. Create a project `prompting-support-desk/` with one Python file per technique
   (below). Use the Ollama Python client or plain HTTP to `http://localhost:11434`.

> **Rule:** you may only change the **prompts** (everything marked `TODO`). Do not
> swap models or post-process outputs to fake a pass — the point is prompt design.

## The six techniques and their tasks
Each file targets the support-desk domain. Include a small built-in check that prints
PASS/FAIL so you can iterate.

1. **`k_shot_prompting.py` — Ticket classification.**
   Given a customer message, classify it into `billing | shipping | returns |
   technical | other`. Use k-shot examples to lock the label format.
2. **`chain_of_thought.py` — Refund eligibility.**
   Given an order date, item condition, and a written refund policy, reason step by
   step to a YES/NO refund decision with a one-line justification.
3. **`tool_calling.py` — Order lookup.**
   Define a fake `get_order_status(order_id)` tool. The model must decide when to call
   it, produce a valid call, and use the returned data in its reply.
4. **`self_consistency_prompting.py` — Priority scoring.**
   Sample multiple reasoning paths for a tricky "how urgent is this ticket (1–5)?"
   judgment and take the majority vote. Show that self-consistency beats a single pass.
5. **`rag.py` — Policy-grounded answers.**
   Retrieve from a small local knowledge base (`data/help_center.txt`: shipping times,
   warranty, return window) and answer a customer question grounded **only** in
   retrieved text. Refuse politely when the answer isn't in the docs.
6. **`reflexion.py` — Self-improving reply.**
   Draft a customer reply, have the model critique its own draft against a rubric
   (tone, correctness, completeness), then produce an improved final reply.

## Deliverables
Push `prompting-support-desk/` to a repo containing:
1. All six completed files with every `TODO` resolved and their checks passing.
2. `data/help_center.txt` for the RAG task.
3. A `writeup.md` with, **per technique**:
   - Your final prompt(s).
   - A sample input and the model's output.
   - 1–2 sentences on how the technique changed the result vs. a naive prompt.

## Evaluation (60 pts)
- 10 points per technique: prompt is well-designed **and** the task check passes.

## References
- Ollama structured outputs: https://ollama.com/blog/structured-outputs
- Ollama model library: https://ollama.com/library
