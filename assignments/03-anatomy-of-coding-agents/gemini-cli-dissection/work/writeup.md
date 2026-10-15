# Week 3 Writeup — Inside a Coding Agent

**Name:** Yousef Albayedoğlu  
**Gemini CLI version (`gemini --version`):** `0.64.0`  
**OS / shell:** Windows 11 + PowerShell  
**Model(s) seen in trace:** `gemini-3.5-flash-lite`  
**Session commit:** `dae37ca`  

> Evidence tags: `[OBSERVED]` = cite a timeline line, call number, or diff hunk.  
> `[INFERRED]` = say what you're reasoning from.  

---

## Part I — Session

**Narrative:**  
[OBSERVED: session_timeline.txt L1-L70] The session began when the user provided the directive to read `TASK.md` and complete all tasks autonomously. The agent immediately invoked `update_topic` (Call #1) to announce its planning phase and read `TASK.md`. In Call #2, it inspected the codebase by reading `shopcart/cart.py`, `shopcart/pricing.py`, `shopcart/catalog.py`, `tests/test_cart.py`, and `tests/test_pricing.py` in parallel. When its initial test command reported a missing `pytest` dependency, it read `requirements.txt` and installed it via pip (Calls #3–#7). Once pytest ran, reproducing the 2 initial failures, the agent entered an extensive thinking phase (Call #8, 3213 thinking tokens) and generated a structured execution plan via `update_topic`. It then systematically resolved the bugs: fixing the quantity accumulation bug in `cart.py` using `replace` (Call #9), correcting discount ordering and implementing `calculate_shipping()` in `pricing.py` (Call #10), updating existing test expectations to account for shipping (Call #13), and adding comprehensive test coverage for shipping rules in `test_pricing.py` (Call #16). After briefly backing off from a 429 per-minute quota threshold, it verified clean git status and 100% test pass rate (22/22 tests passing), recapped its achievements via `update_topic` (Call #19), and concluded the session cleanly.

| Metric | Value |
|---|---|
| User prompts | `1` [OBSERVED: session_timeline.txt L2, L72] |
| Model calls | `20` (19 successful responses, 1 transient 429 rate limit error) [OBSERVED: session_timeline.txt L73] |
| Tool calls (failed) | `25` (0 failed) [OBSERVED: session_timeline.txt L74] |
| Final `pytest` result | `22 passed in 0.03s` [OBSERVED: pytest output] |
| Did you step in? When / what? | `No` — The agent operated completely autonomously from the single initial prompt; all tool confirmations were approved directly when prompted. |

---

## Part II — System prompt annotation

### Outline
From `work/prompts/system.md`:
1. **Core Mandates** — Security & System Integrity, Context Efficiency, Engineering Standards, Topic Updates
2. **Available Sub-Agents** — Strategic Orchestration & Delegation
3. **Available Agent Skills** — Modular skill definitions and capabilities
4. **Hook Context** — Lifecycle extension points
5. **Primary Workflows** — Development Lifecycle, New Applications
6. **Operational Guidelines** — Tone and Style, Security and Safety Rules, Tool Usage, Interaction Details
7. **Git Repository** — Version control state and constraints

### Annotations (≥6)

#### Section 1: Operational Guidelines — Tone and Style (tone and verbosity)
> [OBSERVED: system.md L172-L178]  
> *"Be direct, concise, and technical. Skip pleasantries, conversational filler, and praise... Prioritize clear, dense code examples and terminal commands over text explanations. Summarize file changes and architectural decisions briefly instead of echoing full files back."*
- **Behavior it produces:** The agent outputs compact, factual status messages and immediate tool calls rather than conversational chatter or repetitive explanations.
- **Failure it prevents:** Prevents token bloat and conversational drift, saving context window capacity across multi-turn sessions.

#### Section 2: Core Mandates — Security & System Integrity (when not to act / confirm)
> [OBSERVED: system.md L6-L8]  
> *"Credential Protection: Never log, print, or commit secrets, API keys, or sensitive credentials. Rigorously protect `.env` files, `.git`, and system configuration folders. Source Control: Do not stage or commit changes unless specifically requested by the user."*
- **Behavior it produces:** The agent explicitly avoids staging or committing git changes during the run and refuses to display or leak environment secrets.
- **Failure it prevents:** Prevents accidental data exfiltration and prevents unreviewed commits from polluting repository history without explicit human instruction.

#### Section 3: Engineering Standards — Contextual Precedence & Safety (when not to act / confirm)
> [OBSERVED: system.md L51-L52]  
> *"Handle Ambiguity/Expansion: Do not take significant actions beyond the clear scope of the request. If the user implies a change (e.g., reports a bug) without explicitly asking for a fix, do not perform it automatically."*
- **Behavior it produces:** The agent confines its code edits strictly to what is instructed in `TASK.md`, avoiding speculative refactoring or unsolicited feature additions.
- **Failure it prevents:** Prevents scope creep and prevents the agent from rewriting unrelated working codebase modules.

#### Section 4: Primary Workflows — Development Lifecycle (workflow)
> [OBSERVED: system.md L135-L149]  
> *"Follow this sequence for all software engineering tasks: 1. Understand: Explore relevant code, read requirements, and inspect existing tests. 2. Plan: Define discrete steps before touching code. 3. Implement: Make targeted, minimal edits. 4. Verify: Run tests or linters to validate changes empirically."*
- **Behavior it produces:** The agent sequentially read `TASK.md` and tests first (Calls #1–#2), ran baseline pytest, formulated an explicit plan in Call #8, executed surgical replacements (Calls #9–#10), and re-verified with pytest (Calls #11, #14, #17).
- **Failure it prevents:** Prevents the agent from "blindly editing" code before understanding root causes or verifying failure reproduction.

#### Section 5: Operational Guidelines — Tool Usage (tool usage)
> [OBSERVED: system.md L190-L194]  
> *"Prefer `replace` for surgical modifications to existing files. Use `write_file` only when creating new files or when an existing file is being rewritten in its entirety... Always provide sufficient surrounding context in `old_string` to ensure uniqueness."*
- **Behavior it produces:** The agent exclusively used `replace` for modifying `cart.py`, `pricing.py`, and test files (Calls #9, #10, #13, #16), never overwriting entire files.
- **Failure it prevents:** Prevents destructive file overwrites and avoids wiping out untouched functions or comments.

#### Section 6: Core Mandates — Context Efficiency
> [OBSERVED: system.md L23-L27]  
> *"Combine turns whenever possible by utilizing parallel searching and reading... Prefer using tools like grep_search to identify points of interest instead of reading lots of files individually... Unnecessary turns are generally more expensive than other types of wasted context."*
- **Behavior it produces:** In Call #2, the model requested 5 `read_file` calls and 1 `run_shell_command` in a single parallel turn rather than making 6 separate back-and-forth round trips.
- **Failure it prevents:** Prevents turn explosion, reducing latency and avoiding compounding token costs across early turns.

### Context injection (`GEMINI.md`)
[OBSERVED: work/submission/session_calls.csv Call #1, telemetry.log]  
`GEMINI.md`'s content is **NOT** inside the exported `system.md` system prompt.  
Instead, it is dynamically loaded at session initialization and injected into the **very first user message** inside a dedicated `<session_context><loaded_context><project_context>` block:
```xml
<loaded_context>
<project_context>
--- Context from: .../work/run/GEMINI.md ---
# Project context
- Python 3.10+ library; no third-party runtime dependencies.
- All money is integer **cents**. Never use floats for stored amounts.
- Run tests with `python -m pytest -q` from the repository root.
- Keep functions small; pricing rules live in `shopcart/pricing.py`, cart state in `shopcart/cart.py`.
--- End of Context from: .../work/run/GEMINI.md ---
</project_context>
</loaded_context>
```
[INFERRED]: This ensures project-specific mandates take contextual precedence over system prompt defaults without requiring re-compilation or permanent mutation of the agent's core system prompt template.

---

## Part III — Tool design

### Inventory
| Category | Tools Available in Gemini CLI | Used in session (count) |
|---|---|---|
| File | `read_file`, `write_file`, `replace`, `read_many_files`, `save_memory` | `read_file` (9), `replace` (4) |
| Search | `grep_search`, `glob`, `find_files` | None (0) |
| Shell | `run_shell_command`, `write_process_input` | `run_shell_command` (9) |
| Web | `web_search`, `fetch_web_page` | None (0) |
| Narration & Planning | `update_topic`, `write_todos`, `enter_plan_mode`, `exit_plan_mode` | `update_topic` (3) |
| Delegation | `sub_agent`, `activate_skill` | None (0) |

Total tool calls in session: **25** (0 failed).

### Tool A: `replace`
- **Source file:** `packages/core/src/tools/edit.ts` (declarations in `base-declarations.ts` L64–L69; schema in `model-family-sets/gemini-3.ts` L356)
- **Schema:**
  ```json
  {
    "file_path": { "type": "string", "description": "Path to file to edit" },
    "instruction": { "type": "string", "description": "Brief description of the change for review" },
    "old_string": { "type": "string", "description": "Exact text sequence to replace" },
    "new_string": { "type": "string", "description": "Exact text sequence to substitute" },
    "allow_multiple": { "type": "boolean", "description": "Whether to replace all occurrences if found multiple times" }
  }
  ```
- **Why each parameter:**
  - `file_path`: Identifies target file on disk.
  - `instruction`: Generates clear user-facing justification in confirmation prompts.
  - `old_string`: Anchors edit via exact content matching without relying on fragile line numbers.
  - `new_string`: Complete drop-in replacement text.
  - `allow_multiple`: Explicit safety guard preventing accidental multi-site replacements when a substring matches multiple locations.
- **Description line that corrects a model mistake:**  
  > *"Remember that `old_string` must strictly match the current file contents, including all whitespace, indentation, and newlines."*  
  **Mistake:** Models frequently approximate whitespace or omit leading indentation, leading to failed edits.
- **Deliberately does not:** Does not perform regex or fuzzy string matching. This prevents catastrophic silent misplacements or corrupting similarly structured blocks.

### Tool B: `run_shell_command`
- **Source file:** `packages/core/src/tools/shell.ts` (declarations in `base-declarations.ts` L56–L58; dynamic helpers in `dynamic-declaration-helpers.ts` L36, L85)
- **Schema:**
  ```json
  {
    "command": { "type": "string", "description": "The exact shell command line string to execute" },
    "description": { "type": "string", "description": "Brief summary of what this command accomplishes" },
    "dir": { "type": "string", "description": "Optional working directory" },
    "timeout_ms": { "type": "number", "description": "Maximum execution time in milliseconds" }
  }
  ```
- **Why each parameter:**
  - `command`: The command string passed to the underlying shell process.
  - `description`: Displays the purpose in human-readable prompt approval dialogues.
  - `dir`: Specifies execution context without needing stateful `cd` commands.
  - `timeout_ms`: Guards against hung or infinite processes.
- **Description line that corrects a model mistake:**  
  > *"Do not run interactive commands that wait indefinitely for user input (e.g. interactive shells, nano, or unflagged commands).*  
  **Mistake:** Calling interactive commands that freeze the agent waiting for stdin that never arrives.
- **Deliberately does not:** Does not auto-elevate administrative privileges (no implicit sudo/admin) and blocks recursive root deletion attempts.

### Why old/new string edits?
1. **Resilience to Line Drift:** In a multi-step session, previous edits or concurrent changes shift line numbers. Line-number-based edits easily corrupt files when line offsets drift, whereas exact `old_string` matching is content-addressable and invariant to line shifts elsewhere in the file.
2. **Context and Token Efficiency:** Replacing a 10-line function via `old_string`/`new_string` requires transmitting only ~50 tokens. Transmitting the entire 300-line file would consume thousands of tokens per edit, rapidly exhausting context and bandwidth.  
[OBSERVED: Call #10, `session_timeline.txt` L37-L38]: In Call #10, the agent modified `shopcart/pricing.py` to fix discount ordering and add `calculate_shipping()`. By targeting only the 5 lines of `final_total()` and appending the helper, it completed the edit with only 387 output tokens rather than rewriting the whole module.

### Per-model tool descriptions
Comparing `model-family-sets/gemini-3.ts` vs `model-family-sets/default-legacy.ts`:
- In `default-legacy.ts`, tool descriptions are shorter, more defensive, and include rigid negative constraints (e.g., repeatedly warning NOT to include markdown code fences or multiple instructions).
- In `gemini-3.ts`, descriptions are richer and explicitly instruct the model on parallel tool execution, contextual optimization (`before`/`after` flags), and coordination with `update_topic`.  
[INFERRED]: Different model families have different reasoning capabilities and instruction-following fidelity. Legacy models need simplified schemas with defensive guardrails to avoid malformed JSON arguments, whereas Gemini 3 class models benefit from sophisticated operational guidance that leverages their native tool-use and reasoning strengths.

---

## Part IV — Behavioral analysis

### 1. The loop
```text
Call #1 (update_topic, read_file TASK.md)
  → Call #2 (run_shell_command pytest, read_file cart.py, pricing.py, catalog.py, test_cart.py, test_pricing.py [parallel])
  → Call #3 (run_shell_command pytest)
  → Call #4 (run_shell_command pip list)
  → Call #5 (read_file requirements.txt)
  → Call #6 (run_shell_command pip install)
  → Call #7 (run_shell_command pytest [failures confirmed])
  → Call #8 (update_topic: Plan and Execution [3213 thinking tokens])
  → Call #9 (replace: fix cart.py add_item)
  → Call #10 (replace: fix pricing.py discount order & add calculate_shipping)
  → Call #11 (run_shell_command pytest)
  → Call #12 (read_file tests/test_cart.py)
  → Call #13 (replace: update tests/test_cart.py totals for shipping)
  → Call #14 (run_shell_command pytest)
  → Call #15 (read_file tests/test_pricing.py)
  → Call #16 (replace: add shipping tests to tests/test_pricing.py)
  → Call #17 (run_shell_command pytest)
  [429 Quota Pause: backoff 53s]
  → Call #18 (run_shell_command git status)
  → Call #19 (update_topic: summary recap)
  → Call #20 (final completion response)
```
**What ended it:** [OBSERVED: session_timeline.txt L64-L70] The agent decided it was done after Call #18 verified `git status` was clean and all 22 tests were passing, followed by an `update_topic` completion summary (Call #19).

### 2. Context growth

| Call # | Model | Input Tokens | Output Tokens | Cached Tokens | Thoughts Tokens | Total Tokens |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | gemini-3.5-flash-lite | 11,354 | 62 | 6,093 | 186 | 11,602 |
| 2 | gemini-3.5-flash-lite | 11,900 | 149 | 8,115 | 154 | 12,203 |
| 3 | gemini-3.5-flash-lite | 13,876 | 27 | 10,121 | 110 | 14,013 |
| 4 | gemini-3.5-flash-lite | 14,177 | 31 | 12,140 | 56 | 14,264 |
| 5 | gemini-3.5-flash-lite | 14,577 | 20 | 12,136 | 47 | 14,644 |
| 6 | gemini-3.5-flash-lite | 14,661 | 37 | 12,129 | 31 | 14,729 |
| 7 | gemini-3.5-flash-lite | 15,352 | 32 | 12,128 | 25 | 15,409 |
| 8 | gemini-3.5-flash-lite | 16,074 | 47 | 12,128 | 3,213 | 19,334 |
| 9 | gemini-3.5-flash-lite | 19,386 | 195 | 14,173 | 502 | 20,083 |
| 10 | gemini-3.5-flash-lite | 20,499 | 387 | 6,075 | 311 | 21,197 |
| 11 | gemini-3.5-flash-lite | 21,790 | 34 | 18,229 | 29 | 21,853 |
| 12 | gemini-3.5-flash-lite | 22,710 | 24 | 20,255 | 424 | 23,158 |
| 13 | gemini-3.5-flash-lite | 23,662 | 762 | 20,255 | 819 | 25,243 |
| 14 | gemini-3.5-flash-lite | 26,097 | 35 | 22,295 | 16 | 26,148 |
| 15 | gemini-3.5-flash-lite | 26,352 | 24 | 24,315 | 58 | 26,434 |
| 16 | gemini-3.5-flash-lite | 26,620 | 585 | 24,309 | 147 | 27,352 |
| 17 | gemini-3.5-flash-lite | 27,782 | 35 | 24,311 | 21 | 27,838 |
| 18 | gemini-3.5-flash-lite | 28,040 | 27 | 24,305 | 37 | 28,104 |
| 19 | gemini-3.5-flash-lite | 28,268 | 120 | 24,299 | 130 | 28,518 |
| 20 | gemini-3.5-flash-lite | 28,637 | 233 | 26,318 | 21 | 28,891 |

[OBSERVED: session_calls.csv] Input tokens grow steadily from 11,354 on Call #1 to 28,637 on Call #20 because the agent transmits the entire conversation history, including previous tool call invocations, command outputs, file contents, and thinking traces, on every successive turn.  
**Caching significance:** Notice that `cached_content_token_count` scales right alongside input tokens (reaching 26,318 tokens by Call #20). On Call #20, out of 28,637 input tokens, over **91.9%** were served from cache! Prompt caching drastically reduces end-to-end latency and lowers compute cost by avoiding re-processing the invariant conversation prefix on every turn.

### 3. Planning
[OBSERVED: session_timeline.txt L5, L31-L32, L67] The agent used the `update_topic` tool to structure and signal its sub-phases:
- Call #1: `title`: "Reading Task and Planning"
- Call #8: `title`: "Plan and Execution"
- Call #19: `summary`: "Completed all tasks in TASK.md: fixed failing tests in shopcart/, implemented shipping rules... and added new test coverage for shipping. All 22 tests passing."
The plan matched what it actually executed. It diagnosed the two failing tests first, patched `cart.py` and `pricing.py`, updated cart total expectations for shipping in `test_cart.py`, and added new tests in `test_pricing.py`.

### 4. Error recovery
[OBSERVED: session_timeline.txt L8-L17, L61-L63]  
Two distinct error recovery events occurred during the session:
1. **Missing test runner (Call #2):**  
   > `run_shell_command "python -m pytest" -> exited with code 1: No module named pytest`  
   **Recovery:** Instead of guessing or failing, the agent inspected `pip list` (Call #4), examined `requirements.txt` (Call #5), ran `pip install -r requirements.txt` (Call #6), and successfully re-ran pytest (Call #7). The recovery was methodical, autonomous, and completely self-healing.
2. **Rate Limit 429 (Call #17):**  
   > `API ERROR: 429 Resource Exhausted ... limit: 250000 input tokens per minute ... retry in 53s`  
   **Recovery:** The CLI automatically waited out the 53-second quota window and resumed execution cleanly on Call #18 without losing session state or crashing.

### 5. The tests
Did the agent edit any existing test?  
[OBSERVED: git diff dae37ca^..dae37ca -- run/tests/test_cart.py] Yes, in `tests/test_cart.py`, the agent modified three existing assertions:
```python
 def test_total_includes_tax():
     cart = Cart()
     cart.add_item("TEE")
-    assert cart.total() == 2160  # 2000 + 8% tax
+    assert cart.total() == 2759  # 2000 + 8% tax + 599 shipping

 def test_percent_discount():
     cart = Cart()
     cart.add_item("MUG", 2)
     cart.apply_code("SAVE10")
-    assert cart.total() == 2333  # (2400 - 10%) + 8% tax
+    assert cart.total() == 2932  # (2400 - 10%) + 8% tax + 599 shipping

 def test_fixed_discount_applied_before_tax():
     cart = Cart()
     cart.add_item("TEE")
     cart.add_item("TEE")
     cart.apply_code("TENOFF")
-    assert cart.total() == 3240  # (4000 - 1000) + 8% tax
+    assert cart.total() == 3839  # (4000 - 1000) + 8% tax + 599 shipping
```
**Was this allowed by `TASK.md`?**  
[OBSERVED: TASK.md L15-L16] Yes! `TASK.md` explicitly allows this:  
> *"Some existing tests check `Cart.total()` with values from before shipping existed. You may update those expected values — and only those — and note why in a comment."*  
The agent obeyed this constraint precisely, updating only those three totals and adding explanatory comments (`+ 599 shipping`).

### 6. Models
[OBSERVED: session_calls.csv] Every request ran on `gemini-3.5-flash-lite`.  
**Thinking distribution:**  
The call with the highest thinking was **Call #8** with **3,213 thinking tokens**, followed by Call #13 (819 tokens) and Call #9 (502 tokens). At Call #8, the agent had completed codebase reconnaissance and was synthesizing the overall implementation and testing plan.  
**Why Gemini CLI splits models (flash-lite router vs flash work):**  
Without `-m`, Gemini CLI routes lightweight commands (or query triage) to `gemini-3.5-flash-lite` and delegates complex reasoning and editing to `gemini-3.8-flash`. This dual-tier architecture optimizes both latency and API cost: routing decisions and basic tool calls consume fast, cheap tokens, while high-parameter reasoning models are reserved for complex code synthesis. Running the entire session on a larger model would increase latency and token consumption, though it might reduce intermediate tool iterations on ambiguous tasks.
