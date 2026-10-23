# Week 3 Writeup — Inside a Coding Agent

**Name:** Mohamad Abdullah 
**Gemini CLI version (`gemini --version`):** 0.64.0
**OS / shell:** Windows 11 + Git Bash (inside the VS Code terminal)
**Model(s) seen in trace:** `gemini-3.5-flash-lite` (all 11 calls)
**Session commit:** `10bf72c`

> Evidence tags: `[OBSERVED]` = cite a timeline line, call number, or diff hunk.
> `[INFERRED]` = say what you're reasoning from.

---

## Part I — Session

**Narrative (one paragraph):** I started `gemini -m gemini-3.5-flash-lite` in `work/run/` and sent the required prompt once. The agent first published a topic ("Reading TASK.md") and read `TASK.md` (call #1). In call #2 it ran `pytest` to reproduce the failures and read all five source and test files in parallel. After one `503 high demand` error that the CLI retried automatically, call #3 spent the most "thinking" of the session (2,557 thought tokens) and published the topic "Executing Plan: Fixing Bugs & Adding Shipping". It then made five `replace` edits, one per turn (calls #4–#8): fixed `add_item` so a repeated SKU adds to the quantity, rewrote `final_total` so the discount is applied before tax and added a `shipping_fee` rule, updated three old `Cart.total()` expectations with comments, and added five new shipping tests. In call #9 it ran the full test suite, in call #10 it published "Task Complete", and call #11 was its final summary. The whole session took about 3 minutes (11:19:24 → 11:22:29). I approved every tool call and typed nothing else. Afterwards I ran `python -m pytest -q` myself: **19 passed** (before the session it was 2 failed, 12 passed).

| Metric | Value |
|---|---|
| User prompts | 1 |
| Model calls | 11 (plus 3 `503` API errors that were retried automatically) |
| Tool calls (failed) | 18 (0) — read_file 6, update_topic 5, replace 5, run_shell_command 2 |
| Final `pytest` result | 19 passed (I re-ran it myself after the session) |
| Did you step in? When / what? | No. I only approved tool calls ("Allow once"). |

---

## Part II — System prompt annotation

### Outline
1. Preamble (L1) — identity: "Gemini CLI, an interactive CLI agent", Default mode.
2. Core Mandates → Security & System Integrity (L3–8) — secrets, no commits, untrusted data.
3. Context Efficiency (L10–38) — how to save tokens and turns when searching/reading.
4. Engineering Standards (L40–51) — GEMINI.md precedence, conventions, testing, scope.
5. Topic Updates (L52–67) — how to narrate progress with `update_topic`.
6. Available Sub-Agents (L69–106) — when to delegate to `codebase_investigator`, `cli_help`, `generalist`.
7. Available Agent Skills (L108–123) — skills that can be loaded with `activate_skill`.
8. Hook Context (L125–130) — treat hook output as read-only data.
9. Primary Workflows → Development Lifecycle (L132–149) — Research → Strategy → Execution.
10. Primary Workflows → New Applications (L151–165) — defaults for building new apps.
11. Operational Guidelines → Tone and Style (L167–179) — short, direct CLI output.
12. Security and Safety Rules (L181–183) — explain risky commands.
13. Tool Usage (L185–214) — response rules, parallelism, edit collisions, memory files.
14. Interaction Details (L216–218) — `/help`, `/bug`.
15. Git Repository (L220–237) — never commit unless asked; how to commit when asked.

### Annotations (≥6)

#### Section: Tone and Style (tone and verbosity) — L174–175
> "**Minimal Output:** Aim for fewer than 3 lines of text output (excluding tool use/code generation) per response whenever practical."
> "**No Chitchat:** Avoid conversational filler, preambles ("Okay, I will now..."), or postambles ("I have finished the changes...") unless they are part of the **Topic Model**."
- **Behavior it produces:** The agent talks very little and spends its output on tool calls. `[OBSERVED]` Output tokens per call stayed small (61–533, `session_calls.csv`), and the only longer text was the final summary, which the Topic Model allows.
- **Failure it prevents:** A chatty agent that fills the terminal with "Sure! I'll now..." text, wastes output tokens and hides the important information.

#### Section: Confirm Ambiguity/Expansion + Git Repository (when not to act / confirm) — L51, L223
> "**Confirm Ambiguity/Expansion:** Do not take significant actions beyond the clear scope of the request without confirming with the user."
> "**NEVER** stage or commit your changes, unless you are explicitly instructed to commit."
- **Behavior it produces:** The agent stays inside the task and leaves version control to the user. `[OBSERVED]` The timeline contains no `git` command; the agent's changes were left uncommitted and I committed them myself as `10bf72c`.
- **Failure it prevents:** An agent that "helpfully" commits, pushes or expands the task (refactoring unrelated code) without permission — destructive or hard-to-undo actions the user did not ask for.

#### Section: Development Lifecycle (workflow) — L135, L144
> "Operate using a **Research -> Strategy -> Execution** lifecycle. For the Execution phase, resolve each sub-task through an iterative **Plan -> Act -> Validate** cycle."
> "**Validation is the only path to finality.** Never assume success or settle for unverified changes."
- **Behavior it produces:** Understand first, then plan, then change, then verify. `[OBSERVED]` Research in calls #1–#2 (read TASK.md, ran pytest, read all files), Strategy in call #3 (topic "Executing Plan…"), Execution in calls #4–#8 (five `replace` edits), Validation in call #9 (`run_shell_command` "Run pytest test suite to verify all tests pass").
- **Failure it prevents:** Editing code before understanding it, and declaring success without running the tests.

#### Section: Tool Usage — Parallelism & File Editing Collisions (tool usage) — L196–197
> "**Parallelism & Sequencing:** Tools execute in parallel by default. Execute multiple independent tool calls in parallel when feasible"
> "**File Editing Collisions:** Do NOT make multiple calls to the `replace` tool for the SAME file in a single turn."
- **Behavior it produces:** Independent reads are batched; edits are serialized. `[OBSERVED]` Response #2 issued 7 tool calls at once (update_topic, pytest, five `read_file`). In contrast, the two edits to `tests/test_cart.py` happened in different turns (calls #6 and #8), and every edit turn contained exactly one `replace`.
- **Failure it prevents:** Wasting many turns on one-file-at-a-time reads (expensive, see Context Efficiency), and race conditions where two edits to the same file overwrite each other.

#### Section: Engineering Standards — Testing — L49
> "**Testing:** ALWAYS search for and update related tests after making a code change. You must add a new test case to the existing test file (if one exists) or create a new test file to verify your changes."
- **Behavior it produces:** The agent adds tests together with features. `[OBSERVED]` Diff of `10bf72c`: three new tests in `tests/test_pricing.py` (`test_shipping_fee_empty_or_zero`, `_below_threshold`, `_at_or_above_threshold`) and two in `tests/test_cart.py` (`test_free_shipping_at_or_above_50_dollars`, `test_discount_influences_free_shipping_threshold`), added to the existing files instead of new ones.
- **Failure it prevents:** Features shipped without verification, which later break silently.

#### Section: Topic Updates — L56–61
> "Always call update_topic in your first turn."
> "The typical complex user message should call update_topic 3 or more times. Each corresponds to a distinct phase of the task"
- **Behavior it produces:** A visible, phase-by-phase narration for the user. `[OBSERVED]` `update_topic` was called in the very first response (#1, "Reading TASK.md") and 5 times in total, including "Executing Plan: Fixing Bugs & Adding Shipping" (#3) and "Task Complete" (#10).
- **Failure it prevents:** A long silent run where the user cannot tell what phase the agent is in or whether it is stuck.

#### Section: Security & System Integrity — Credential Protection — L6
> "**Credential Protection:** Never log, print, or commit secrets, API keys, or sensitive credentials."
- **Behavior it produces:** The agent avoids touching secrets. `[OBSERVED]` No tool call read environment variables or `.env`; my `GEMINI_API_KEY` appears in no committed file (`git grep "AIza"` returns nothing).
- **Failure it prevents:** Leaking API keys into logs, commits or public pull requests.

### Context injection (`GEMINI.md`)
`GEMINI.md` is **not** in the exported `system.md`. `[OBSERVED]` Its distinctive rule "All money is integer **cents**" does not appear anywhere in `prompts/system.md` or `submission/session_system.md`; the system prompt only refers to GEMINI.md files in general (L42: "Instructions found in `GEMINI.md` files are foundational mandates").

It reaches the model in the **first user message**. In the v0.64.0 source, `Config.getSessionMemory()` ([`packages/core/src/config/config.ts` L2615](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/config/config.ts#L2615)) wraps project memory in `<loaded_context><project_context>…</project_context></loaded_context>`. `getEnvironmentContext()` ([`packages/core/src/utils/environmentContext.ts` L66](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/utils/environmentContext.ts#L66)) puts it into a `<session_context>` block together with the date, OS and folder structure, and `getInitialChatHistory()` (same file, L84–106) inserts that block as the first message with `role: 'user'`. The comment in that file describes the "tiered context model": global memory → system instruction, extension + project memory → first user message, subdirectory memory → tool output (just-in-time).

`[OBSERVED]` The CLI status bar showed "1 GEMINI.md file" loaded, and the agent followed its rules: all new amounts are integer cents (`599`, `5000` in `shipping_fee`) and the shipping rule was put in `shopcart/pricing.py`, as GEMINI.md says ("pricing rules live in `shopcart/pricing.py`").

---

## Part III — Tool design

### Inventory
Built-in tool names from [`base-declarations.ts`](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/base-declarations.ts) (v0.64.0); counts from `session_timeline.txt`.

| Category | Tools | Used in session (count) |
|---|---|---|
| File | `read_file`, `read_many_files`, `write_file`, `replace` | `read_file` 6, `replace` 5 |
| Search | `glob`, `grep_search`, `list_directory` | 0 |
| Shell | `run_shell_command` (incl. background processes via `is_background`) | 2 |
| Web | `google_web_search`, `web_fetch` | 0 |
| Planning and narration | `update_topic`, `write_todos`, `enter_plan_mode`, `exit_plan_mode`, `complete_task` | `update_topic` 5 |
| Delegation | `invoke_agent` (sub-agents), `activate_skill` (skills) | 0 |
| Other | `ask_user`, `get_internal_docs`, `read_mcp_resource`, `list_mcp_resources` | 0 |

The agent used only 4 of these tools. It never needed search because the project is tiny: it read every file directly in one parallel batch (response #2).

### Tool A: `replace` (file edit)
- **Source file:** name/params in [`base-declarations.ts` L64–69](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/base-declarations.ts#L64-L69); description + schema in [`model-family-sets/gemini-3.ts` L356](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/model-family-sets/gemini-3.ts#L356); execution in [`edit.ts`](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/edit.ts) (`EditToolInvocation` L460, `validateToolParamValues` L1176).
- **Schema:**
  ```
  replace(
    file_path:      string   (required)
    instruction:    string   (required)
    old_string:     string   (required)
    new_string:     string   (required)
    allow_multiple: boolean  (optional, default false)
  )
  ```
- **Why each parameter:**
  - `file_path` — which file to change; validated and resolved inside the workspace (`validateToolParamValues`).
  - `instruction` — a plain-language explanation of the change ("acting as a high-quality prompt for an expert LLM assistant"). It documents intent for the user's approval dialog and can be used to repair a failed edit.
  - `old_string` — the exact text to find; it is the "address" of the edit, so the edit lands only where the model actually looked.
  - `new_string` — the exact replacement text.
  - `allow_multiple` — safety switch: by default exactly one match is required, so a repeated snippet is not changed everywhere by accident.
- **Description line that corrects a model mistake:** > "Do not use omission placeholders like '(rest of methods ...)', '...', or 'unchanged code'; provide exact literal code." (`new_string` description). **Mistake:** LLMs like to abbreviate code with "..." — written literally into a file, that would delete real code.
- **Deliberately does not:** guess. If `old_string` matches 0 times or more than once, it fails instead of choosing a location (`getErrorReplaceResult` in `edit.ts` L358: "Failed to edit, expected 1 occurrence but found N"; for 0 matches it tells the model to re-read the file with ReadFile). It also does not work by line numbers or rewrite the whole file.

### Tool B: `run_shell_command`
- **Source file:** name/params in [`base-declarations.ts` L56–58](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/base-declarations.ts#L56-L58); description + schema in [`dynamic-declaration-helpers.ts`](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/dynamic-declaration-helpers.ts) (`getShellToolDescription` L36, `getShellDeclaration` L85); execution in [`shell.ts`](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/shell.ts) (`ShellToolInvocation` L102, `validateToolParamValues` L1220).
- **Schema:**
  ```
  run_shell_command(
    command:       string   (required)
    description:   string   (optional)
    dir_path:      string   (optional)
    is_background: boolean  (optional)
    delay_ms:      integer  (optional)
    additional_permissions: object (only when tool sandboxing is enabled)
  )
  ```
- **Why each parameter:**
  - `command` — the exact command; on Windows the description says it runs as `powershell.exe -NoProfile -Command <command>`, elsewhere as `bash -c <command>`, so the model writes the right syntax for the OS.
  - `description` — a one-sentence summary shown to the user in the approval dialog. `[OBSERVED]` My session: "Run pytest to inspect failing tests" and "Run pytest test suite to verify all tests pass".
  - `dir_path` — where to run; must be inside the workspace (`validatePathAccess` in `validateToolParamValues`).
  - `is_background` + `delay_ms` — start long-running processes (servers, watchers) without blocking the agent loop, and wait briefly to catch startup errors.
  - `additional_permissions` — lets the model ask for extra filesystem/network access when a sandboxed command fails with "Operation not permitted".
- **Description line that corrects a model mistake:** > "To run a command in the background, set the `is_background` parameter to true. Do NOT use PowerShell background constructs." (Windows variant; on Mac/Linux: "Do NOT use `&` to background commands."). **Mistake:** starting a background process with `&`/`Start-Job`, which the CLI cannot track or stop, leaving orphan processes or hanging the loop.
- **Deliberately does not:** decide on its own whether a command is safe to run. Execution goes through the confirmation flow (`getConfirmationDetails`, `shell.ts` L433), which is why I had to approve both `pytest` runs. It also does not run interactive programs forever: an inactivity timeout (`getShellToolInactivityTimeout`, `shell.ts` L554) stops stuck commands.

### Why old/new string edits?
1. **Precision and safety:** line numbers go stale as soon as one edit shifts the file, and LLMs are bad at counting lines. An exact `old_string` only matches if the model really knows the current text, and the "exactly one match" rule prevents editing the wrong place.
2. **Cost and reviewability:** rewriting a whole file costs many output tokens and risks silently dropping code; a small old/new pair is cheap and gives the user a clear diff to approve (the description says it "minimizes token usage, simplifies code reviews, and avoids accidental deletions").

**Trace moment:** `[OBSERVED]` The agent edited `tests/test_cart.py` twice (calls #6 and #8) in separate turns. Because the second edit was addressed by exact text (`old_string` starting with `def test_fixed_discount_applied_before_tax():`), it still matched correctly after the first edit had already changed lines earlier in the same file — line numbers from the original read would have been wrong. All 5 `replace` calls succeeded (`[ok]`, 0 failed tool calls), so the failure path never came up. `[INFERRED]` That is because the agent had read every file in full in call #2, so its `old_string` values were exact.

### Per-model tool descriptions
I compared `replace` in [`gemini-3.ts` L356](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/model-family-sets/gemini-3.ts#L356) and [`default-legacy.ts` L349](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/model-family-sets/default-legacy.ts#L349).

- **Legacy (older models)** is much longer. It adds: "Always use the read_file tool to examine the file's current content before attempting a text replacement", a numbered "Expectation for required parameters" list, "NEVER escape `old_string` or `new_string`", "Include at least 3 lines of context BEFORE and AFTER the target text", "Prefer to break down complex and long changes into multiple smaller atomic calls", and GOOD/BAD examples for `instruction` ("Fix the bug." is a BAD example).
- **Gemini 3** is short. It drops the 3-lines-of-context rule, the read-first rule and the examples, and instead explains *why* the tool exists: "preferred for surgical edits to existing files as it minimizes token usage, simplifies code reviews, and avoids accidental deletions". It also says "unescaped" where legacy says "preferably unescaped".

**Why describe the same tool differently?** Older models made specific mistakes (escaping strings, too little context, editing without reading), so they need explicit rules and examples. Newer models follow intent with less scaffolding, and every tool description is sent with **every** request: `[OBSERVED]` call #1 already used 11,359 input tokens for a one-sentence user message, most of it system prompt and tool schemas. Shorter descriptions for capable models save tokens on every call; long ones are kept only where they prevent real errors.

---

## Part IV — Behavioral analysis

### 1. The loop
```
USER prompt
→ call#1  → update_topic("Reading TASK.md"), read_file(TASK.md)
→ call#2  → update_topic, run_shell_command(pytest), read_file ×5 (cart, pricing, catalog, test_cart, test_pricing)
→ [503 API error, CLI retried after ~6s]
→ call#3  → update_topic("Executing Plan: Fixing Bugs & Adding Shipping")
→ call#4  → replace(shopcart/cart.py)
→ call#5  → replace(shopcart/pricing.py)
→ call#6  → replace(tests/test_cart.py)
→ [503 API error, retried after ~4s]
→ call#7  → replace(tests/test_pricing.py)
→ call#8  → replace(tests/test_cart.py)
→ call#9  → update_topic, run_shell_command(pytest)
→ call#10 → update_topic("Task Complete")
→ [503 API error, retried after ~4s]
→ call#11 → final text summary, no tool call → loop ends
```
**What ended it:** the agent decided it was done. `[OBSERVED]` Response #11 is followed by no TOOL lines in `session_timeline.txt`, after the "Task Complete" topic at call #10. No limit was hit and I did not interrupt.

### 2. Context growth
`input_token_count` per call (`session_calls.csv`):

| Call | Input tokens | Cached tokens | Cached % | Thoughts |
|---|---|---|---|---|
| 1 | 11,359 | 0 | 0% | 202 |
| 2 | 11,919 | 0 | 0% | 367 |
| 3 | 15,028 | 0 | 0% | 2,557 |
| 4 | 18,088 | 14,194 | 78% | 202 |
| 5 | 18,896 | 6,082 | 32% | 602 |
| 6 | 20,509 | 0 | 0% | 646 |
| 7 | 22,298 | 0 | 0% | 620 |
| 8 | 23,812 | 20,292 | 85% | 254 |
| 9 | 25,321 | 22,325 | 88% | 35 |
| 10 | 25,729 | 22,312 | 87% | 315 |
| 11 | 26,359 | 18,253 | 69% | 17 |

```
call 1  ███████████                  11.4k
call 2  ████████████                 11.9k
call 3  ███████████████              15.0k
call 4  ██████████████████           18.1k
call 5  ███████████████████          18.9k
call 6  ████████████████████▌        20.5k
call 7  ██████████████████████       22.3k
call 8  ████████████████████████     23.8k
call 9  █████████████████████████    25.3k
call 10 █████████████████████████▌   25.7k
call 11 ██████████████████████████   26.4k
```

**Why it grows:** `[OBSERVED]` input grew from 11,359 to 26,359 tokens (2.3×) and summed to 219,318 tokens for a 3-minute task. The model is stateless, so every call re-sends the whole history: system prompt + tool schemas + the `<session_context>` message + every earlier model message, tool call and tool result. The biggest jump is call #2 → #3 (+3,109 tokens), right after the five `read_file` results and the pytest output entered the history. The system prompt itself says this (L16): "The agent passes the full history with each subsequent message."

**Caching:** `cached_content_token_count` is the part of the input the API recognized as an identical prefix from an earlier request, so it did not have to process it again. `[OBSERVED]` 103,458 of 219,318 input tokens (47%) were cached; in calls #8–#10, 85–88% of each request was cached (call #11: 69%). Calls #1–#3 had no cache yet, and calls #6–#7 had 0 cached. `[INFERRED]` Those misses are probably because implicit caching is best-effort and the request around the 503 retry (before call #7) may have been served without the cache. Caching matters because cached tokens are billed at a much lower rate and skip recomputation, so long agent sessions get cheaper and faster per call; without it, cost grows roughly with the square of the number of turns.

### 3. Planning
`[OBSERVED]` The agent planned with **plain text plus `update_topic`** — 5 topic calls with three distinct phases ("Reading TASK.md" → "Executing Plan: Fixing Bugs & Adding Shipping" → "Task Complete"). It never used `write_todos` or `enter_plan_mode`. This matches the system prompt's "Topic Updates" section (L52–67): a topic in the first turn, one per phase, and a recap at the end.

**Did the plan match?** Mostly yes: fix bugs → add shipping → add tests → run tests, which is the order of TASK.md. `[OBSERVED]` One departure from TASK.md's wording: TASK.md says "Put the shipping rule in `shopcart/pricing.py` and use it from `Cart.total()`", but the agent did not change `Cart.total()`; it added shipping inside `final_total()` in `pricing.py`, which `Cart.total()` already calls (`return final_total(self.subtotal(), self.discount_code)`). The behavior is correct and the tests pass, but the shipping is used *indirectly* from `Cart.total()`. A second detail: the bug fix and the shipping feature were done in the **same** edit of `pricing.py` (call #5), so there was no separate "all old tests pass" checkpoint between step 1 and step 2. `[INFERRED]` from the single `replace` on `pricing.py` and the absence of a pytest run between calls #3 and #9.

### 4. Error recovery
> `11:19:49  API ERROR   model=gemini-3.5-flash-lite … "code": 503, "message": "This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later."`

`[OBSERVED]` The first failure was not the agent's: the API returned `503` right after call #2's tool results were sent. The CLI waited and re-sent the same request at 11:19:55, and it succeeded as response #3. The same happened before calls #7 and #11. The recovery was handled by the harness (automatic retry with backoff), not by the model, and it was good: the session continued without losing work and I did not need to step in.

`[OBSERVED]` The agent had no tool failures (18 tool calls, 0 failed), and its first `pytest` run (call #2) was intentional reproduction of the 2 known failures (`test_add_same_item_twice_increments_quantity`, `test_fixed_discount_applied_before_tax`). It fixed both on the first try: the final pytest run in call #9 was followed directly by "Task Complete". `[INFERRED]` It got it right first time because it read all code and tests before editing, so the "Strategic Re-evaluation" rule (L146, rethink after 3 failed fixes) never triggered.

### 5. The tests
`[OBSERVED]` Yes, the agent edited three existing tests in `tests/test_cart.py` (diff of `10bf72c`):
```diff
-    assert cart.total() == 2160  # 2000 + 8% tax
+    assert cart.total() == 2759  # 2000 + 8% tax + $5.99 shipping fee (subtotal < $50)
-    assert cart.total() == 2333  # (2400 - 10%) + 8% tax
+    assert cart.total() == 2932  # (2400 - 10%) + 8% tax + $5.99 shipping fee (subtotal < $50)
-    assert cart.total() == 3240  # (4000 - 1000) + 8% tax
+    assert cart.total() == 3839  # (4000 - 1000) + 8% tax + $5.99 shipping fee (subtotal < $50)
```
**Allowed by TASK.md?** Yes. TASK.md step 2 says: "Some existing tests check `Cart.total()` with values from before shipping existed. You may update those expected values — and only those — and note why in a comment." All three are `Cart.total()` checks with pre-shipping values, each new value is exactly old value + 599, and each has a comment explaining the shipping fee. The agent did **not** weaken any test to make step 1 pass: `test_add_same_item_twice_increments_quantity` was fixed in the code (`self.items[sku] = self.items.get(sku, 0) + quantity`), and `test_fixed_discount_applied_before_tax` only changed by the +599 shipping, after the discount-before-tax bug was fixed in `final_total`. It also added 5 new tests and changed one import line in `test_pricing.py` to import `shipping_fee`.

### 6. Models
`[OBSERVED]` The `model` field is `gemini-3.5-flash-lite` for all 11 calls (`models: gemini-3.5-flash-lite x11` in the timeline summary).

**Most "thinking":** call #3 had by far the most thought tokens (2,557, ~4× the next one). `[INFERRED]` That is the moment right after it saw the failing pytest output and all five files: it was diagnosing both bugs and planning the whole change, and it published the "Executing Plan" topic in that same response. The next highest are calls #6 (646), #7 (620) and #5 (602) — the edits where it had to compute expected totals and write the shipping logic and tests. The lowest are #11 (17) and #9 (35): writing the final summary and simply running the tests needed almost no reasoning.

**Why split routing and work across two models?** `[INFERRED]` Without `-m`, a small fast model (`gemini-3.5-flash-lite`) decides how to route each request and a bigger model (`gemini-3.8-flash`) does the work. Routing is a simple classification, so a cheap, low-latency model is enough; the expensive model is used only where quality matters. It also protects the bigger model's tight free-tier quota (20 requests/day vs. our ~14 requests including retries). If the whole session ran on the bigger model, I would expect **higher cost and lower speed** per call, possibly **better quality** on harder tasks (deeper reasoning, fewer mistakes on complex bugs), but on this small task flash-lite already got 19/19 tests passing in 11 calls, so the gain would likely be small.
---

## Additional observations
- **Two tensions inside the system prompt.** (1) Topic Updates says "NEVER use update_topic for ... isolated lookup tasks" but also "Always call update_topic in your first turn" (system.md L55–56). (2) Sub-Agents says "You MUST delegate tasks to the sub-agent with the most relevant expertise" (L71) but also "Continue to handle 'surgical' tasks directly" (L85). `[OBSERVED]` In my session the agent resolved both in the same direction: it called update_topic in turn 1 (the task was multi-step), and it never called invoke_agent, handling all 18 tool calls itself because the repo is small.
- **A bug the agent did not touch.** `remove_item` in `shopcart/cart.py` accepts zero or negative quantities (a negative value increases the item count). `[OBSERVED]` The agent left it unchanged: it was outside TASK.md's scope and no existing test covers it, which matches the "Confirm Ambiguity/Expansion" rule (stay within the request). I left `run/` unchanged so it reflects exactly what the agent did.