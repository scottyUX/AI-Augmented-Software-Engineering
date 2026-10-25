# Week 3 Prompting Techniques Submission: Riza Arslan

**Project repository:** https://github.com/xXx0001-crybto/week3-prompting

## Summary

All four checks pass with `llama3.1:8b` running locally on Ollama (temperature 0).

| Technique | Result |
| --- | --- |
| K-shot prompting | 4/4 checks passed |
| Chain-of-thought | 3/3 checks passed |
| Tool calling | `get_order_status` called with `order_id='4412'`; tool returned "shipped, arriving Friday" |
| RAG | 3/3 checks passed, including the "I do not know" refusal for the out-of-scope question |

The repository contains the four completed starter files and
[`writeup.md`](https://github.com/xXx0001-crybto/week3-prompting/blob/main/writeup.md)
(final prompts, sample input/output, and what I learned per technique, plus a closing
paragraph).
