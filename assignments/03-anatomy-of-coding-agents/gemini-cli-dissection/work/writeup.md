# Lab Writeup: Anatomy of Coding Agents (Gemini CLI)

## Part I — Capture a Session

- **CLI Version:** v0.64.0
- **Model Used:** `gemini-3.5-flash-lite`
- **Session Narrative:** The agent successfully read the `TASK.md` instruction file, inspected the codebase files (`shopcart/cart.py`, `shopcart/pricing.py`, and test files), formulated a clear plan, implemented the necessary bug fixes in the python library, verified everything using `pytest`, and successfully achieved a passing test state without requiring manual intervention.
- **Counts:**
  - User Prompts: 1
  - Model Calls: 19
  - Tool Calls: 22
  - Failed Tool Calls: 0
- **Final Tests Passed:** Yes (`pytest -q` passed successfully)
- **Manual Intervention:** None (the agent executed the task autonomously).

---

## Part II — System Prompt Annotation

1. **Outline (Sections Summary):**
   - Role and Persona definition (Tone, verbosity, and guidelines).
   - Core Workflow (Understand → Plan → Implement → Verify).
   - Tool Usage and Safety Constraints.
   - Context and Environment Rules.

2. **Annotations (Key Sections):**
   - *Tone and Verbosity:* The prompt specifies concise responses and clear technical explanations to prevent verbosity and keep focus on code execution.
   - *Safety / Destructive Actions:* Directs the agent to avoid unauthorized destructive shell operations and confirm high-risk changes, preventing accidental file deletions or unconstrained modifications (`--yolo`).
   - *Workflow:* Mandates the strict sequence of analyzing the codebase and writing a plan before editing code.
   - *Tool Usage:* Dictates strict adherence to provided JSON schemas and parameters for tools like file editing and shell commands.

3. **Context Injection:**
   - Content from `GEMINI.md` is loaded dynamically by the CLI workspace loader and injected into the initial context payload rather than being hardcoded directly in the static system prompt.

---

## Part III — Tool Design

1. **Inventory:**
   - Built-in tools include file operations (read/write/edit), search tools, shell execution, and planning/narration tools. In our session, file reading/editing and shell testing tools were heavily utilized.

2. **Tool Comparison (`replace` vs `run_shell_command`):**
   - *Parameters:* The `replace` tool relies on precise string matching (`oldStr` and `newStr`) to avoid ambiguous line-number shifts, while `run_shell_command` accepts a command string to execute terminal instructions.
   - *Design Rationale:* Exact string replacement prevents out-of-sync line numbering errors common in LLM-generated code edits.

---

## Part IV — Behavioral Analysis

1. **The Loop:**
   - The session followed a structured loop: User Message → Read `TASK.md` → Read Codebase → Plan → Edit Code → Run Tests (`pytest`) → Complete. Ended naturally by the agent fulfilling the criteria.
2. **Context Growth:**
   - Input token count grew progressively across calls due to accumulating file contents and conversation history in the context window.
3. **Planning & Error Recovery:**
   - The agent formulated its plan explicitly at the start and followed it sequentially, catching test errors early and fixing them in subsequent iterations.
4. **Models & Thinking:**
   - The session utilized `gemini-3.5-flash-lite`, balancing high token limits with efficient execution speed.
