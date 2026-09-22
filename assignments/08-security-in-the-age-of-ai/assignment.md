# Week 8 — Security in the Age of AI: Scan, Inject, Triage

## Overview
AI changes security in two directions: it helps you **find and fix** vulnerabilities
faster, and it introduces **new attack surfaces** (prompt injection against your own
agents). This week you'll do both — run static analysis with **[Semgrep](https://semgrep.dev/)**
and remediate findings with an AI tool, then probe and harden an **LLM-backed feature**
against prompt injection.

**New domain:** a deliberately-vulnerable **online bookstore** API (not the reference's
notes app).

> **Coding agent — IDE-agnostic.** Use whichever agent you set up in Week 1 (Antigravity
> by default) for the AI-assisted remediation and triage. Semgrep is the required
> scanner; the coding agent is your choice.

## Learning goals
- Run SAST/SCA and secret scanning; triage and remediate real findings.
- Understand prompt injection and agent-specific attack surfaces.
- Use an agent to assist triage and remediation — and to *attack* a feature.

---

## Learn about Semgrep
- Semgrep README + install: https://github.com/semgrep/semgrep
- Use either the CLI or the Semgrep AppSec Platform.

## The target app (build a small vulnerable one)
Create `vuln-bookstore/` — a small API (FastAPI or Express) for a bookstore with an
intentionally weak surface. Include at least: a raw-string SQL query (SQLi), an
unsanitized value written to the DOM on the frontend (XSS), permissive CORS (`*`), a
hardcoded secret/API key in a config file, and a knowingly outdated dependency in
`requirements.txt` / `package.json`. Also add **one LLM-backed endpoint** (e.g.,
`/summarize-review` that sends a user review to a model) for Part 3.

> If you'd rather not author vulnerabilities yourself, you may fork a known
> intentionally-vulnerable app instead — but document which and keep the same tasks.

## Part 1 — Scan
Run a general security scan plus focused secret and dependency scans:
```bash
semgrep ci            # or: semgrep scan --config auto
```
Scan backend code, frontend JS, dependencies, and config/env files.

## Part 2 — Triage & fix (≥3 issues, AI-assisted)
Pick **at least three** distinct findings across categories (SAST / Secrets / SCA) and
fix them with an AI coding tool. For each: show the precise edit and explain the
mitigation (parameterized SQL, safer DOM APIs, restricted CORS, secret moved to env,
dependency upgrade). **Re-run Semgrep** to confirm resolution and no new findings.
Ensure the app still runs and tests still pass.

## Part 3 — Prompt injection & agent-assisted triage
1. **Attack:** craft an input to your LLM-backed endpoint that makes the model ignore
   its instructions (e.g., a review containing "ignore previous instructions and…").
   Document the successful injection.
2. **Harden:** apply at least two mitigations (input framing/delimiters, output
   constraints, allow-listing, treating model output as untrusted) and show the attack
   now fails.
3. **Agent-assisted triage:** have an AI agent review your Semgrep report and *propose*
   a remediation plan. Critique its suggestions — where was it right, where would you
   not trust it?

## Deliverables
**Submit the GitHub repository link** for `vuln-bookstore/` and a `writeup.md` with:
1. **Findings overview:** categories Semgrep reported (SAST/Secrets/SCA); any false
   positives you ignored and why.
2. **Three fixes (before → after):** file + line, rule/category, risk, your change
   (diff + AI-tool usage), why it mitigates the issue, and the clean re-scan.
3. **Prompt injection:** the working attack, your mitigations, and proof it's blocked.
4. **Agent-assisted triage:** the agent's plan and your critique of it.
5. **What you learned:** 3–5 sentences on how AI both speeds up remediation and creates
   new attack surfaces.

## Evaluation (100 pts)
- 35 — Three+ correct, verified remediations across categories (with clean re-scans).
- 25 — Prompt-injection attack demonstrated **and** mitigated.
- 20 — Agent-assisted triage with a thoughtful critique.
- 20 — Clear findings overview and before/after documentation.

## Tips
- Prefer minimal, root-cause fixes; re-run Semgrep after each.
- For dependencies, document upgraded versions and link advisories.
