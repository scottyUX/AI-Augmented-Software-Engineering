# Week 3 Writeup — Inside a Coding Agent

**Name:** Dilara Gültekin  
**Gemini CLI version (`gemini --version`):** 0.64.0  
**OS / shell:** Windows + Git Bash (MINGW64); Gemini CLI shell tool configured for PowerShell  
**Model(s) seen in trace:** `gemini-3.5-flash-lite`  
**Session commit:** `6828947`

> **Evidence convention:** `[OBSERVED]` denotes a fact visible in the session timeline, a call record, a source declaration, or the session commit's Git diff. `[INFERRED]` denotes a reasoned interpretation rather than direct access to the model's private reasoning.
>
> **Reference notation:** `TL` = `submission/session_timeline.txt` (timestamps and events); `call #n` = row n of `submission/session_calls.csv`; `system.md:n` = line n of `submission/session_system.md`; `diff` = `git diff 6828947^ 6828947`. Source links below use the Gemini CLI **v0.64.0** tag. Model-call totals count successful recorded responses; API errors are counted separately.

---

## Part I — Session

**Narrative (one paragraph):** **[OBSERVED]** I gave Gemini CLI one task prompt: “Read TASK.md and complete all of it. First write out your plan, then carry it out without waiting for my confirmation.” The agent began by updating its topic and reading `TASK.md`, then ran the existing test suite and inspected `shopcart/pricing.py`, `shopcart/cart.py`, `shopcart/catalog.py`, and the relevant tests (see `submission/session_timeline.txt`, approximately 08:07–08:09 UTC). It corrected `Cart.add_item()` so adding an existing SKU increments rather than overwrites its quantity; changed the calculation order so discounts precede tax; and implemented shipping of 599 cents, waived for empty carts or discounted subtotals of at least 5,000 cents. It modified only the existing `Cart.total()` assertions affected by shipping, added eight shipping tests, and reran pytest. The session log records 13 successful model responses, 19 successful tool calls, and eight API errors. An independent final pytest invocation reported **22 passed**, compared with **12 passed and 2 failed** before the agent's changes. I did not supply corrective prompts during the agent's implementation, although I approved tool execution when requested. **[INFERRED]** The sequence broadly resembles a research–implementation–validation loop, but the recorded topic updates do not by themselves establish that the agent presented a complete up-front plan in the format requested.

| Metric | Value |
|---|---|
| User prompts | **1** task prompt initiating the recorded agent run; the later independent `!python -m pytest -q` check was not a corrective task prompt |
| Model calls | **13** successful model responses (`session_calls.csv`, calls 1–13) |
| Tool calls (failed) | **19 (0 failed)**; eight separate API errors were observed and are **not** tool-call failures |
| Final `pytest` result | **22 passed** (`python -m pytest -q`, independently confirmed) |
| Did you step in? When / what? | **No corrective intervention.** I approved tool execution when prompted and independently checked the final test result. |

---

## Part II — System prompt annotation

### Outline

The exported prompt in `prompts/system.md` and `submission/session_system.md` contains the following major sections or functional groups:

1. **Core Mandates — Security & System Integrity:** credentials, safe operations, and source-control boundaries.
2. **Context Efficiency:** targeted retrieval, avoiding unnecessary context consumption.
3. **Engineering Standards:** code quality, conventions, testing, and project-instruction precedence.
4. **Topic Updates:** tracking and communicating the current task.
5. **Available Sub-Agents:** when delegation may be useful.
6. **Available Agent Skills:** guidance for skill-based workflows.
7. **Hook Context:** information supplied by hooks.
8. **Primary Workflows / Development Lifecycle:** research, strategy, execution, and validation.
9. **Operational Guidelines — Tone and Style:** concise user-facing communication.
10. **Security and Safety Rules:** precautions around commands and sensitive data.
11. **Tool Usage:** tool selection, sequencing, editing, and memory-file handling.
12. **Interaction Details:** user-facing command and interaction conventions.
13. **Git Repository:** repository-aware behavior and Git restrictions.

### Annotations (at least six)

#### 1. Section: Tone and Style — response verbosity

> “**Minimal Output:** Aim for fewer than 3 lines of text output”

- **Behavior it produces:** **[INFERRED]** Encourages brief status updates and a concise final explanation instead of narrating every internal decision.
- **Failure it prevents:** Excessive prose that obscures the task result and consumes attention or context.
- **Evidence:** The instruction appears in the exported system prompt under Operational Guidelines. Its effect on any individual response is an interpretation, not a proven causal relationship.

#### 2. Section: Security & System Integrity — when not to act

> “**Source Control:** Do not stage or commit changes unless specifically requested by the user.”

- **Behavior it produces:** Keeps Git staging and commits under explicit user control.
- **Failure it prevents:** Unrequested repository mutations or premature commits.
- **Evidence:** The agent's session focused on source and test edits; I created the session commit separately after the run. **[INFERRED]** This is consistent with the instruction, although the trace alone cannot prove motivation.

#### 3. Section: Primary Workflows — development lifecycle

> “Operate using a Research -> Strategy -> Execution lifecycle.”

> “For the Execution phase, resolve each sub-task through an iterative Plan -> Act -> Validate cycle.”

- **Behavior it produces:** Inspect the task and existing implementation, select a change, execute it, and check the outcome.
- **Failure it prevents:** Editing before understanding requirements or declaring success without validation.
- **Evidence:** **[OBSERVED]** `read_file` and an initial pytest invocation preceded edits; later `run_shell_command` calls tested the implementation (`session_timeline.txt`).

#### 4. Section: Engineering Standards — testing

> “**Testing:** ALWAYS search for and update related tests after making a code change.”

- **Behavior it produces:** Encourages regression coverage alongside implementation changes.
- **Failure it prevents:** A patch that appears correct but lacks verification for edge cases.
- **Evidence:** **[OBSERVED]** The agent edited `tests/test_cart.py` and `tests/test_pricing.py` and added tests for empty carts, the 4,999/5,000-cent boundary, and discounts affecting shipping eligibility (Git diff of commit `6828947`).

#### 5. Section: Topic Updates — visible task state

> “Always call update_topic in your first turn.”

- **Behavior it produces:** Announces the current activity and changes the topic as work progresses.
- **Failure it prevents:** A long-running task with no indication of its current phase.
- **Evidence:** **[OBSERVED]** `update_topic` was the first tool call, and the timeline records **five** `update_topic` calls in total.

#### 6. Section: Tool Usage — editing collisions

> “Do NOT make multiple calls to the replace tool for the SAME file in a single turn.”

- **Behavior it produces:** Encourages serialized edits when multiple replacements might depend on one another.
- **Failure it prevents:** Stale-string matches, race conditions, and conflicting writes.
- **Evidence:** **[OBSERVED]** The recorded session used `replace` once on `shopcart/cart.py` and `write_file` for broader changes to `shopcart/pricing.py` and the test files. **[INFERRED]** This choice is compatible with the instruction, but it does not prove the agent consciously applied it.

#### 7. Section: Context Efficiency — search before bulk reading

> “Prefer using tools like grep_search to identify points of interest instead of reading lots of files individually.”

- **Behavior it produces:** Encourages focused retrieval when a repository is large.
- **Failure it prevents:** Filling the model context with irrelevant file content.
- **Evidence:** **[OBSERVED]** The agent used `read_file` **seven** times and `grep_search` **zero** times. **[INFERRED]** For this small codebase, direct file reads were practical, although they did not follow the prompt's search-first preference literally.

#### 8. Section: Engineering Standards — project-specific instruction priority

> “**Contextual Precedence:** Instructions found in `GEMINI.md` files are foundational mandates.”

- **Behavior it produces:** Gives local project rules priority over generic agent defaults.
- **Failure it prevents:** A generic coding workflow overriding a repository's conventions.
- **Evidence:** **[OBSERVED]** `submission/session_system.md`, lines 41–42, explicitly states the precedence rule. Whether a particular project instruction changed this run is not established.

### Context injection (`GEMINI.md`)

**[OBSERVED — `submission/session_system.md`, lines 41–42]** The system prompt assigns higher priority to instructions found in `GEMINI.md` files than to general workflows and tool defaults. **[OBSERVED — lines 202–206]** It states that the contents of loaded `GEMINI.md` files are already in the agent's context and should not be reread unnecessarily. It distinguishes team-shared project instructions (`./GEMINI.md`), scoped subdirectory instructions, private project memory, and automatically loaded global personal instructions (`~/.gemini/GEMINI.md`).

**[INFERRED]** Such instructions can be incorporated into the model's working context before or alongside task execution, allowing persistent conventions to influence decisions without being restated in each user prompt. However, the exported prompt establishes the **intended precedence and loading behavior**, not a complete byte-for-byte map of the underlying API request. The available evidence does **not** independently identify which project-specific `GEMINI.md` files, if any, were loaded in this particular run or the exact position of their content in the model request. Therefore, I do not claim a verified injection offset or location beyond what the system prompt itself says.

---

## Part III — Tool design

### Inventory

**[OBSERVED]** The Gemini CLI `/tools` command displayed **16** available tools. The actual session's tool counts below come from `submission/session_timeline.txt`, not from availability alone. Categories are functional groupings; a tool may conceptually span categories, but each is listed only once here.

| Category | Tools available | Used in session (count) |
|---|---|---|
| File | `read_file`, `write_file`, `replace`, `list_directory`, `glob` | `read_file` **7**; `write_file` **3**; `replace` **1**; others **0** |
| Search | `grep_search` | **0** |
| Shell | `run_shell_command`, `list_background_processes`, `read_background_output` | `run_shell_command` **3**; others **0** |
| Web | `google_web_search`, `web_fetch` | **0** |
| Memory / other / orchestration | `activate_skill`, `ask_user`, `enter_plan_mode`, `invoke_agent`, `update_topic` | `update_topic` **5**; others **0** |
| **Total** | **16 available** | **19 calls, 0 failed** |

### Tool A: `replace`

- **Source files inspected:** [`gemini-3.ts`, lines 356–393](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/model-family-sets/gemini-3.ts#L356-L393) and [`default-legacy.ts`, lines 349–410](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/model-family-sets/default-legacy.ts#L349-L410); the underlying edit implementation is separate from these model-facing declarations.
- **Model-facing schema (essential fields):**

  ```text
  replace(
      file_path: string,        # required
      instruction: string,      # required
      old_string: string,       # required
      new_string: string,       # required
      allow_multiple?: boolean  # optional; defaults to false
  )
  ```

- **Why each parameter exists:** `file_path` identifies the target file; `instruction` communicates the intended change; `old_string` is an exact-match anchor; `new_string` is the replacement; and `allow_multiple` permits deliberately replacing repeated matches instead of assuming a unique target.
- **Description line that corrects a model mistake:** The Gemini 3 declaration says the tool “expects to find and replace exactly ONE occurrence of `old_string`” unless `allow_multiple` is true. **Mistake prevented:** Accidentally replacing multiple unrelated occurrences of a common fragment.
- **Deliberately does not:** It does not autonomously choose an edit location without a specified target string, and it is not a semantic refactoring or whole-repository rewrite tool.
- **Trace moment:** **[OBSERVED]** At approximately **08:09:45 UTC**, the agent called `replace` successfully on `shopcart/cart.py`. The Git diff shows the one-line substitution of `self.items[sku] = quantity` with `self.items[sku] = self.items.get(sku, 0) + quantity`.

### Tool B: `run_shell_command`

- **Source files inspected:** [`dynamic-declaration-helpers.ts`, lines 36–159](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/dynamic-declaration-helpers.ts#L36-L159), referenced by both `gemini-3.ts` and `default-legacy.ts`.
- **Model-facing schema (essential fields):**

  ```text
  run_shell_command(
      command: string,                  # required
      description?: string,             # optional
      dir_path?: string,                # optional
      is_background?: boolean,          # optional
      delay_ms?: number,                # optional
      additional_permissions?: object   # conditional: sandbox configuration
  )
  ```

- **Why each parameter exists:** `command` specifies what to execute; `description` explains its purpose to the user; `dir_path` selects the working directory; `is_background` permits long-running work; `delay_ms` influences how long the tool waits before returning control; and `additional_permissions` is exposed only in applicable sandbox configurations.
- **Description line that corrects a model mistake:** The shell declaration instructs the agent to use the configured platform shell (for this Windows environment, `powershell.exe -NoProfile -Command <command>`) and to prefer efficient, noninteractive commands. **Mistake prevented:** Assuming every shell is Bash or launching a pager/watch process that blocks unattended execution.
- **Deliberately does not:** It does not itself decide whether a shell command is safe, repair failing code, or guarantee that a command's exit status reflects the correctness of the entire project. Such judgments require surrounding agent logic and validation.
- **Trace moment:** **[OBSERVED]** Three `run_shell_command` calls executed pytest at different stages: the initial failure investigation, an intermediate check, and a final full-suite validation (see `session_timeline.txt`, approximately 08:08:40, 08:10:08, and 08:11:41 UTC).

### Why old/new string edits?

**Reason 1 — precision and reviewability:** An exact `old_string`/`new_string` replacement expresses a narrow, inspectable change and helps prevent unintended modifications to unrelated lines. **Reason 2 — efficiency and preservation:** For a small patch, replacing a short span avoids sending and rewriting an entire file, reducing token use and the risk of dropping surrounding code. **[OBSERVED]** The agent used `replace` for the single-line quantity fix in `cart.py` but `write_file` for the larger `pricing.py` update. **[INFERRED]** This is a plausible example of matching editing granularity to the scope of the change; the trace records the choice, not the agent's private rationale.

### Per-model tool descriptions

**[OBSERVED — v0.64.0 source comparison]** The `replace` tool is documented differently in the two model-family declaration files:

| Dimension | `default-legacy.ts` | `gemini-3.ts` |
|---|---|---|
| Description length | Longer, prescriptive instructions and examples | Shorter, surgical-edit-oriented explanation |
| Reading the target | Explicitly says to use `read_file` before replacement | No equivalent explicit read-first rule in the compared description |
| Matching context | Specifies at least **three lines** before and after the target | Requires **significant context**, without the fixed three-line number |
| `instruction` field | Explains intent with WHY / WHERE / WHAT / outcome guidance | Shorter semantic instruction description |
| `old_string` / `new_string` | Detailed warnings against omitted or escaped text | Concise exact-literal guidance |
| Rationale | Prevent common editing mistakes with extensive guardrails | Highlights token savings, reviewability, and avoiding accidental deletion |

**Shared behavior:** `run_shell_command` is created through the same `getShellDeclaration()` helper in both declaration sets; it is not independently described from scratch for each family.

**[OBSERVED — live `/tools` output]** The CLI displayed the longer legacy-style `replace` instructions, despite the selected model being `gemini-3.5-flash-lite`. Therefore, the model's name alone is insufficient to prove which family-specific schema was passed in the recorded API calls.

**[INFERRED]** Different model families may benefit from different levels of instruction scaffolding: detailed reminders can reduce common tool-use errors, while shorter descriptions can reduce repeated prompt overhead. This is a design interpretation, not an experimental comparison performed in this session.

---

## Part IV — Behavioral analysis

### 1. The loop

**[OBSERVED — `submission/session_timeline.txt`, 08:07–08:12 UTC]** The chronological trace supports this tool-level sequence. The timestamps identify logged tool events; the 13 model-response records are summarized separately in `session_calls.csv`.

```text
08:07:14  USER PROMPT: read TASK.md, write plan, complete autonomously
08:07:24  update_topic("Reading Task Instructions")
08:07:24  read_file(TASK.md)
08:07:35  update_topic("Running existing test suite...")
08:08:40  run_shell_command(pytest)                  [ok; initial tests fail]
08:08:40  read_file(shopcart/pricing.py)            [ok]
08:08:40  read_file(shopcart/cart.py)               [ok]
08:08:43  update_topic("Reading remaining project files...")
08:08:43  read_file(shopcart/catalog.py)            [ok]
08:08:43  read_file(tests/test_cart.py)             [ok]
08:08:43  read_file(tests/test_pricing.py)          [ok]
08:08:51  update_topic("Implementing Fixes and Shipping Feature")
08:09:45  replace(shopcart/cart.py)                 [ok]
08:09:54  write_file(shopcart/pricing.py)           [ok]
08:10:08  run_shell_command(pytest)                  [ok; checks changed behavior]
08:10:11  read_file(tests/test_cart.py)             [ok]
08:11:21  write_file(tests/test_cart.py)            [ok]
08:11:28  write_file(tests/test_pricing.py)         [ok]
08:11:41  run_shell_command(full pytest suite)      [ok; 22 passed]
08:11:45  update_topic("Recapping completed tasks...")
           FINAL MODEL RESPONSE; autonomous loop ends
```

**Total:** 5 `update_topic`, 7 `read_file`, 3 `run_shell_command`, 1 `replace`, 3 `write_file` = **19 tool calls**. No tool invocation was marked failed. A pytest command may execute successfully as a tool even if its test assertions fail; these are different notions of success.

**What ended the loop:** **[OBSERVED]** After the full suite passed, the agent issued a recap and final response. **[INFERRED]** It treated validation as sufficient to finish; there is no evidence of an external stop or a user correction during implementation.

### 2. Context growth


**[OBSERVED — `submission/session_calls.csv`]** The graph shows input-token counts for every successful model response. The complete underlying values are below:

| Call | Input tokens | Cached tokens | Thought tokens |
|---:|---:|---:|---:|
| 1 | 11,378 | 0 | 290 |
| 2 | 12,026 | 8,116 | 500 |
| 3 | 14,079 | 10,134 | 37 |
| 4 | 15,176 | 12,143 | 3,174 |
| 5 | 18,471 | 6,081 | 229 |
| 6 | 19,308 | 0 | 1,248 |
| 7 | 21,651 | 18,254 | 58 |
| 8 | 22,603 | 0 | 322 |
| 9 | 23,453 | 0 | 903 |
| 10 | 26,108 | 22,322 | 648 |
| 11 | 27,520 | 14,206 | 79 |
| 12 | 27,836 | 2,029 | 66 |
| 13 | 28,273 | 6,085 | 20 |

**Growth:** The input context increased from **11,378** to **28,273** tokens, a rise of **16,895** tokens (**148.5%**, or approximately **2.49×**). It increased monotonically across the recorded successful calls.

**[INFERRED]** The growth is consistent with repeated submission of conversation history and accumulated file reads, tool results, and edits. The relatively large jumps around calls #5 and #10 coincide with an increasingly populated working context; the available CSV does not isolate the exact contribution of each message.

**Caching:** `cached_content_token_count` fluctuates significantly, including **zero** on calls #1, #6, #8 and #9 and **22,322** on call #10. **[OBSERVED]** The API reported cache hits for some inputs, not all. **[INFERRED]** Reuse of an unchanged prompt prefix could reduce repeated processing; these counts alone do not establish actual billing or latency savings.

**Reasoning-token variation:** Call **#4** reports the peak of **3,174 thought tokens**; call **#6** reports **1,248**, while call **#13** reports **20**. The counters show variation in computation, but not the contents of the model’s private reasoning.

### 3. Planning

**[OBSERVED]** My prompt explicitly requested an up-front plan followed by autonomous execution. The agent called `update_topic` first and continued updating its topic across five phases: reading the task, investigating tests, reading remaining files, implementing fixes, and recapping. It inspected task requirements and ran tests before editing. **[INFERRED]** These actions show phase-level planning and progress tracking. However, topic updates are not equivalent to a complete written plan. **[OBSERVED]** No `enter_plan_mode` call appears in the 19 tool events; the prompt requested a plan before execution, but the trace only directly establishes topic updates and subsequent work. Based on the evidence reviewed, I can verify the sequence of work but cannot confidently claim that the agent provided a comprehensive user-facing plan **before** taking action. This is a limitation in instruction-following evidence, even though the implementation succeeded.

### 4. Error recovery

> Initial test outcome: **12 passed, 2 failed**. The failing tests were `test_add_same_item_twice_increments_quantity` and `test_fixed_discount_applied_before_tax`.

**[OBSERVED]** The initial failures concerned adding the same item twice and the order of a fixed discount relative to tax. After reading the affected code, the agent changed the cart's quantity assignment and revised `final_total()` to discount before taxation. It subsequently reran tests. **[OBSERVED]** The session also recorded **eight API errors** associated with service availability/high demand; these were separate from the 19 tool calls, all of which were marked successful. The agent ultimately completed the task without a corrective user prompt. **[INFERRED]** The recovery was effective at the session level: transient API problems did not prevent completion, and the code failures were addressed through inspection, editing, and validation. I cannot attribute a specific internal retry policy to the model solely from these records.

### 5. The tests

**[OBSERVED — `TASK.md`]** The task prohibited editing existing tests **to fix the original failures**, but explicitly permitted changing old `Cart.total()` expected values affected by the new shipping charge, with explanatory comments. It also required new shipping tests.

**[OBSERVED — Git diff `6828947^..6828947`]** The agent updated exactly three existing `Cart.total()` expectations, each by the 599-cent shipping fee, and added an explanatory comment:

```diff
-    assert cart.total() == 2160  # 2000 + 8% tax
+    # Updated expected value to include $5.99 shipping fee ...
+    assert cart.total() == 2759  # 2000 + 8% tax + 599 shipping
```

The other two changes were `2333 → 2932` and `3240 → 3839`, also increases of 599 cents. **[OBSERVED]** The agent added **eight** new shipping tests: four in `tests/test_cart.py` and four in `tests/test_pricing.py`. The cases include an empty cart, below-threshold shipping, the exact 5,000-cent boundary, free shipping above the threshold, and discounts that either preserve or remove free-shipping eligibility. The `4999` and `5000` checks are particularly useful boundary tests. **[OBSERVED]** The implementation's `calculate_shipping()` checks the discounted subtotal and returns either 0 or 599 cents; `final_total()` adds shipping **after** tax is calculated on the discounted subtotal. The final suite reported **22 passed**.

**Assessment:** **[INFERRED]** These edits comply with the test-editing exception in `TASK.md`; there is no evidence in the diff that the agent weakened the preexisting failure tests to conceal a bug. The expanded coverage is useful, although 22 passing tests do not prove correctness for every possible input. For example, behavior for an invalid discount code on an empty cart is not explicitly specified in `TASK.md` and was not established by these tests; it should not be labeled a requirement violation without further evidence.

### 6. Models

**[OBSERVED — `session_calls.csv`]** All **13** successful recorded model responses used `gemini-3.5-flash-lite`. No model switch or cross-model experiment appears in this trace. The number of reported thought tokens varied from call to call (for example, **3,174** at call #4 versus **20** at call #13). **[INFERRED]** This variation is consistent with different stages requiring different amounts of reasoning, but token counters alone cannot reveal the content or quality of the model's internal reasoning. Because only one model appears, the session supports analysis of **within-model behavior**, not claims that one Gemini model performs better than another.

---

## Evidence references

- `work/submission/session_timeline.txt` — chronological user, tool, and model activity.
- `work/submission/session_calls.csv` — model identifiers, token counts, and cache/thought token fields.
- `work/submission/session_system.md` and `work/prompts/system.md` — exported system instructions; `GEMINI.md` discussion at lines 41–42 and 202–206 of the former.
- `work/run/TASK.md` — task requirements and the narrow exception allowing shipping-related `Cart.total()` assertion updates.
- `git diff 6828947^ 6828947 -- tests/test_cart.py tests/test_pricing.py` — test changes and additions.
- `git diff 6828947^ 6828947 -- shopcart/cart.py shopcart/pricing.py` — implementation changes.
- Gemini CLI v0.64.0 source declarations: `packages/core/src/tools/definitions/model-family-sets/gemini-3.ts`, `default-legacy.ts`, and `packages/core/src/tools/definitions/dynamic-declaration-helpers.ts` — tool descriptions and parameter schemas.

**Privacy note:** The exported prompt artifacts were sanitized to replace the local Windows username with `REDACTED`. The raw telemetry file is not included in the submission commit.
