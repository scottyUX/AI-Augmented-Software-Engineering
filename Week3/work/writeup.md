# Week 3 Writeup — Inside a Coding Agent

**Name:** Mohammad Poorahmadi
**Gemini CLI version (`gemini --version`):** 0.64.0
**OS / shell:** macOS + zsh
**Model(s) seen in trace:** gemini-3.5-flash-lite
**Session commit:** `333a1eb`

> Evidence tags: `[OBSERVED]` = cite a timeline line, call number, or diff hunk.
> `[INFERRED]` = say what you're reasoning from.

---

## Part I — Session

**Narrative (one paragraph):** The agent began by reading `TASK.md` and running the test suite to identify the baseline failures. It then read the core cart and pricing files, successfully fixing the `add_item` quantity overwrite bug in `cart.py` and the discount application order bug in `pricing.py`. Next, it implemented the new shipping fee logic, updated the existing tests to account for the new baseline totals, and added comprehensive new tests for the shipping thresholds. It continuously ran `pytest` to verify its changes, successfully passing all 18 tests before using git to review its final diff and concluding the session.

| Metric | Value |
|---|---|
| User prompts | 2 |
| Model calls | 16 |
| Tool calls (failed) | 16 (1) |
| Final `pytest` result | 18 passed in 0.02s |
| Did you step in? When / what? | No. The agent completed the task without getting stuck. |

---

## Part II — System prompt annotation

### Outline
1. **Core Mandates:** Strict rules for security, context efficiency, engineering standards, and topic updates.
2. **Available Sub-Agents:** Definitions and delegation rules for specialized sub-agents (`codebase_investigator`, `cli_help`, `generalist`).
3. **Available Agent Skills:** Paths to activate specialized workflows (`skill-creator`, `antigravity-support`).
4. **Hook Context:** Rules for treating external hook data as read-only and non-executable.
5. **Primary Workflows:** The required step-by-step lifecycles for both general development and building new applications.
6. **Operational Guidelines:** Constraints on tone, output verbosity, tool parallelization, and memory file management.
7. **Git Repository:** Strict constraints for interacting with version control and formatting commits.

### Annotations (≥6)
#### Section: Operational Guidelines (tone and verbosity)
> "Aim for fewer than 3 lines of text output (excluding tool use/code generation) per response whenever practical. ... Avoid conversational filler, apologies, and unnecessary per-tool explanations."
- **Behavior it produces:** The agent outputs extremely brief, direct text responses, focusing solely on technical intent and the immediate next step.
- **Failure it prevents:** It prevents the model from wasting tokens and user time with long-winded apologies or unnecessary conversational padding before executing tools.

#### Section: Engineering Standards (when not to act / confirm)
> "If the user implies a change (for example reports a bug) without explicitly asking for a fix, **ask for confirmation first**."
- **Behavior it produces:** The agent halts execution and asks for explicit permission to modify files if the user's prompt was just a statement, bug report, or inquiry.
- **Failure it prevents:** It prevents accidental, destructive modifications to the codebase when the user just wanted to ask a question or report an observation without initiating an automatic fix.

#### Section: Primary Workflows (workflow)
> "Operate using a **Research -> Strategy -> Execution** lifecycle. For the Execution phase, resolve each sub-task through an iterative **Plan -> Act -> Validate** cycle."
- **Behavior it produces:** A structured approach where the agent reads files to gather context, states its strategy, edits the code, and finally runs tests/linters to verify.
- **Failure it prevents:** It prevents "blind" edits where the agent guesses file contents, and prevents "fire and forget" coding where the agent edits a file but never verifies if the code actually compiles or passes tests.

#### Section: Operational Guidelines (tool usage)
> "Do NOT make multiple calls to the `replace` tool for the SAME file in a single turn. To make multiple edits to the same file, you MUST perform them sequentially across multiple conversational turns"
- **Behavior it produces:** If the agent needs to edit multiple sections of `cart.py`, it issues one `replace` tool call, waits for the result, and then issues the next `replace` call in the following turn.
- **Failure it prevents:** It prevents file corruption and race conditions where multiple parallel edits target the same line numbers simultaneously, resulting in a broken file structure.

#### Section: Context Efficiency
> "Prefer using tools like grep_search to identify points of interest instead of reading lots of files individually."
- **Behavior it produces:** The agent uses `grep_search` to find specific keywords across the codebase rather than attempting to read entire large files to find a single variable.
- **Failure it prevents:** It prevents the agent from blowing out the context window (and API costs) by indiscriminately loading thousands of lines of irrelevant code into its memory.

#### Section: Git Repository
> "**NEVER** stage or commit your changes, unless you are explicitly instructed to commit."
- **Behavior it produces:** The agent will write code, fix bugs, and run tests, but it will leave the Git staging area completely untouched unless the user explicitly types "commit this."
- **Failure it prevents:** It prevents the agent from silently committing broken, incomplete, or experimental code to the repository's history without the user's consent.

### Context injection (`GEMINI.md`)
No, the actual *content* of `GEMINI.md` is **not** exported inside the static `system.md` file. Instead, `system.md` acts as a static set of rules instructing the model *how* to handle the `GEMINI.md` file once it is loaded. We know it enters the model dynamically because the `system.md` file states under the "Tool Usage" section: "The current contents of all loaded `GEMINI.md` files and the private project `MEMORY.md` index are already in your context — do not re-read them before editing." This proves the CLI dynamically reads the `GEMINI.md` files from the local directory tree and injects their contents directly into the context window at runtime.

---

## Part III — Tool design

### Inventory
| Category | Tools | Used in session (count) |
|---|---|---|
| File | `read_file`, `write_file`, `replace` | `read_file` (4), `replace` (3) |
| Search | `grep_search`, `glob` | None (0) |
| Shell | `run_shell_command` | `run_shell_command` (5) |
| Web | `fetch_url` | None (0) |
| Memory / other | `ask_user` | None (0) |
| Planning and Narration | `update_topic`, `enter_plan_mode` | `update_topic` (4) |
| Delegation | `invoke_agent`, `activate_skill` | None (0) |

### Tool A: `replace`
- **Source file:** `packages/core/src/tools/definitions/gemini-3.ts` (and `base-declarations.ts`)
- **Schema:**
  ```json
  {
    "path": "string",
    "old_string": "string",
    "new_string": "string"
  }
  ```
- **Why each parameter:** path: Identifies the exact file path on disk to modify. old_string: Ensures the model knows the exact current code block it is replacing, preventing unintended edits. new_string: Specifies the replacement code block to be inserted.
- **Description line that corrects a model mistake:** > "replace fails if old_string is ambiguous, causing extra turns.". **Mistake:** The model providing a vague or non-unique old_string (such as a generic return False or a common variable name) that matches multiple locations in the file, causing the edit to fail or overwrite the wrong code block.
- **Deliberately does not:** Accept line numbers, because LLMs struggle with accurate line counting and line numbers shift dynamically after previous code modifications.

### Tool B: run_shell_command
- **Source file:** packages/core/src/tools/definitions/dynamic-declaration-helpers.ts (and base-declarations.ts)
- **Schema:**
  ```json
  {
  "command": "string",
  "wait_for_previous": "boolean",
  "is_background": "boolean"
  }
  ```
- **Why each parameter:** command: The raw terminal string to execute in the system shell (for example python -m pytest). wait_for_previous: Ensures tool call sequencing so the shell command waits for prior dependent edits (for example waiting for replace to finish before running tests). is_background: Allows running long-lived asynchronous processes (for example starting a server) without blocking the agent's main execution turn.
- **Description line that corrects a model mistake:** > "Always prefer non-interactive commands (for example using 'run once' or 'CI' flags...)". **Mistake:** The model running an interactive CLI command (such as vim, less, or an interactive prompt) that hangs the execution loop waiting for input that the model cannot provide.
- **Deliberately does not:** Automatically pass flags like --yolo or bypass user approval natively; it delegates security confirmation entirely to the host environment.

### Why old/new string edits?
The edit tool uses exact old_string / new_string matching rather than line numbers or full-file replacements for two primary reasons: 1. LLM Counting & Attention Failures: Large Language Models frequently make off-by-one errors when counting lines in large source files, whereas string matching relies on exact text equality. 2. Shifting Line Coordinates: When making edits across multiple turns or when external files change, line numbers shift immediately. An edit near line 10 invalidates line indices for the rest of the file, whereas matching old_string remains accurate regardless of index shifts. Trace moment: When updating tests/test_cart.py to account for new shipping fee rules, the agent matched the exact assertion block via old_string and replaced it cleanly without needing to calculate line numbers or rewrite the rest of the test file.

### Per-model tool descriptions
When comparing gemini-3.ts against default-legacy.ts:
What changed: Tool definitions in default-legacy.ts contain heavy, defensive instructions explaining output syntax, warning against hallucinations, and reiterating basic JSON parameters. In contrast, gemini-3.ts provides leaner tool declarations that focus on high-level operational strategy and intent.
Why an agent describes it differently: Legacy model families require defensive, verbose prompting to prevent format errors, missing fields, or hallucinated schemas. Newer model families (like Gemini 3.5) possess far stronger native function-calling and schema compliance, enabling short, concise descriptions that save context tokens.

---

## Part IV — Behavioral analysis

### 1. The loop
```
call#1 → update_topic, read_file(TASK.md) → call#2 → run_shell_command(pytest) → call#3 → read_file(cart.py), read_file(pricing.py) → call#4 → read_file(test_pricing.py) → call#5 → update_topic(FAILED) → call#6 → update_topic → call#7 → replace(cart.py) → call#8 → replace(pricing.py) → call#9 → run_shell_command(pytest) → call#10 → replace(test_cart.py) → call#11 → run_shell_command(pytest) → call#12 → run_shell_command(git status & diff) → call#13 → update_topic → call#14 → [user prompt: pytest] → call#15 → run_shell_command(pytest -q) → call#16
```
What ended it: The agent decided it was done after Call #14 where it published a final update_topic summarizing that all tasks in TASK.md were completed [OBSERVED: session_timeline.txt lines 21-23]. The user then issued a final command (python -m pytest -q), which the agent executed in Call #15-16 before concluding [OBSERVED: session_timeline.txt lines 24-27].

### 2. Context growth
| Call # | Input Tokens | Cached Tokens | Thoughts Tokens | Total Tokens |
|---|---|---|---|---|
| 1 | 11,447 | 6,090 | 180 | 11,694 |
| 2 | 11,997 | 8,112 | 286 | 12,316 |
| 3 | 13,016 | 10,140 | 58 | 13,167 |
| 4 | 14,582 | 12,152 | 20 | 14,626 |
| 5 | 14,812 | 12,146 | 4,433 | 19,412 |
| 6 | 19,435 | 14,202 | 19 | 19,575 |
| 7 | 19,695 | 16,225 | 457 | 20,351 |
| 8 | 20,568 | 18,252 | 853 | 22,319 |
| 9 | 22,748 | 20,290 | 18 | 22,802 |
| 10 | 23,683 | 20,289 | 1,673 | 26,263 |
| 11 | 27,007 | 6,091 | 16 | 27,056 |
| 12 | 27,278 | 24,359 | 29 | 27,339 |
| 13 | 29,317 | 26,397 | 23 | 29,531 |
| 14 | 29,721 | 26,391 | 19 | 30,022 |
| 15 | 30,011 | 26,386 | 32 | 30,081 |
| 16 | 30,147 | 26,378 | 23 | 30,180 |
Why context grows: Context grows monotonically (from 11,447 input tokens in Call #1 up to 30,147 input tokens in Call #16) because the CLI appends every user prompt, model response, tool request, and tool execution output to the ongoing session transcript [OBSERVED: session_stats.csv].
Cached tokens & Caching importance: cached_content_token_count tracks how many prompt tokens were served from Gemini's server-side context cache rather than processed from scratch (averaging ~20,000–26,000 tokens per call later in the session) [OBSERVED: session_stats.csv]. Context caching significantly reduces API latency (speed) and drastically lowers token billing costs, as cached tokens are processed at a fraction of the cost of new input tokens [INFERRED: system prompt context efficiency rules].

### 3. Planning
How it tracked progress: The agent used the update_topic tool to structure its work into named strategic phases [OBSERVED: session_timeline.txt lines 5, 12, 22]. It called update_topic in Call #1 ("Reading TASK.md and Planning"), Call #6 ("Implementing bug fixes and shipping rules"), and Call #13 ("Completed all tasks in TASK.md") [OBSERVED: session_timeline.txt].
System prompt directives: The system prompt explicitly mandates: "Always call update_topic in your first turn... Each topic update should give a concise description of what you are doing... Do not use update_topic on every turn" [OBSERVED: system.md line 62].
Plan execution alignment: The agent's plan closely matched its actual execution. It first read the task and codebase, ran the test suite, made targeted code edits to cart.py and pricing.py, updated test assertions in tests/test_cart.py, and verified the fixes using pytest [OBSERVED: session_timeline.txt lines 4-20]. It did not depart from its plan [INFERRED].

### 4. Error recovery
> quoted failure
10:49:39 TOOL update_topic [FAILED] decision=None args={ "summary": "I have analyzed the failing tests, identified the bugs..." } [OBSERVED: session_timeline.txt line 11]
What happened next: In Call #5, the update_topic tool call failed because the model provided invalid or malformed schema arguments [OBSERVED: session_timeline.txt line 11]. On the very next model call (Call #6), the agent immediately retried the update_topic call with corrected parameters (strategic_intent), which succeeded cleanly ([ok] decision=accept) [OBSERVED: session_timeline.txt line 13]. The recovery was swift and effective, costing only a single fast turn without derailing the overall workflow [INFERRED].

### 5. The tests
Edits to existing tests: Yes, the agent edited tests/test_cart.py in Call #10 [OBSERVED: session_timeline.txt line 17].
Allowed by TASK.md: Yes, TASK.md explicitly required introducing a $5.99 flat shipping fee, which changed baseline cart total assertions and required updating existing test expected values [INFERRED: TASK.md requirements & session_timeline.txt line 17].
Quoted diff:- assert cart.total() == 3240 # (4000 - 1000) + 8% tax
+ # Updated to include flat $5.99 shipping fee since shipping was introduced
+ assert cart.total() == 3839 # (4000 - 1000) + 8% tax + 599 shipping
[OBSERVED: session commit 333a1eb / test_cart.py diff]
### 6. Models
Model confirmation: All 16 calls were executed using gemini-3.5-flash-lite [OBSERVED: session_stats.csv & session_timeline.txt line 30].
Peak "Thinking" analysis: The call with the highest reasoning output was Call #5 (thoughts_token_count = 4,433), followed by Call #10 (1,673 thoughts tokens) and Call #8 (853 thoughts tokens) [OBSERVED: session_stats.csv].
	In Call #5, the agent engaged in deep reasoning to analyze the baseline test failures 		across cart.py and pricing.py and formulate the complete shipping calculation logic 		[INFERRED: session_stats.csv & session_timeline.txt lines 9-11].
	In Call #10, it reasoned through calculating the updated test assertions for 			test_cart.py taking tax, discounts, and shipping thresholds into account simultaneously 	[INFERRED: session_stats.csv & session_timeline.txt line 17].
CLI Model Split Architecture: By default, Gemini CLI splits work between a lighter routing model (gemini-3.5-flash-lite) and a heavier execution model (gemini-3.8-flash). The light model quickly handles simple turns, tool routing, and basic context checks at low cost and latency, while the heavier model performs deep multi-step code generation and complex logic reasoning [INFERRED: Gemini CLI architecture].
Impact of running entirely on a larger model (for example Pro):
Speed: Slower response latency per turn due to larger parameter count and computation overhead [INFERRED].
Cost: Significantly higher token cost per API call, especially as context accumulates toward 30,000 tokens [INFERRED].
Quality: Higher reasoning precision, superior zero-shot instruction following, and lower likelihood of schema failures (such as the update_topic failure in Call #5) [INFERRED].