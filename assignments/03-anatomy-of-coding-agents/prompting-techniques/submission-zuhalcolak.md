# Week 3 Submission (Prompting Techniques) — Zuhal Çolak

**Repository:** https://github.com/zuhalcolak/week3-prompting-techniques

All four techniques were completed using Ollama running `llama3.1:8b` locally at `temperature=0.0`.

| Technique | File | Check result |
|---|---|---|
| K-shot prompting | `k_shot_prompting.py` | 4/4 PASS |
| Chain-of-thought | `chain_of_thought.py` | 3/3 PASS |
| Tool calling | `tool_calling.py` | PASS (`order_id='4412'`) |
| RAG | `rag.py` | 3/3 PASS |

All 11 built-in checks passed successfully.

[`writeup.md`](https://github.com/zuhalcolak/week3-prompting-techniques/blob/main/writeup.md) includes, for each technique, the final prompt, a sample input and output, and what was learned, plus a closing reflection on why LLMs handle structured tasks well and where they need scaffolding.
