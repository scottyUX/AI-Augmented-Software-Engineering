# Week 3 Writeup — Inside a Coding Agent

**Name:** Aykut Akkus
**Gemini CLI version (`gemini --version`):** 0.64.0
**OS / shell:** macOS + zsh
**Model(s) seen in trace:** gemini-3.5-flash-lite
**Session commit:** `20d7232`

> Evidence tags: `[OBSERVED]` = cite a timeline line, call number, or diff hunk.
> `[INFERRED]` = say what you're reasoning from.

---

## Part I — Session

**Narrative (one paragraph):** [OBSERVED] Gemini first read `TASK.md`, the relevant source files, and the tests, then ran the existing test suite to reproduce the failures. It fixed the bugs, implemented the shipping rules, added tests, reran the suite, and reviewed the Git status and diff. One task prompt resulted in 18 model calls and 18 tool calls with no failed tool calls, and my independent final run confirmed that all 19 tests passed. I did not give the agent any additional help. I had used loops many times before, but this was the first time I saw such an efficient loop system. [INFERRED] I think the main reason was its strong and specific system prompt, especially the `Research -> Strategy -> Execution` and `Plan -> Act -> Validate` workflows. This made me want to research and use more task-specific agent systems in the future.

| Metric | Value |
|---|---|
| User prompts | 2 |
| Model calls | 18 |
| Tool calls (failed) | 18 (0) |
| Final `pytest` result | 19 passed in 0.01s |
| Did you step in? When / what? | No. The second user input was the required independent final test command, `!python -m pytest -q`, not assistance to the agent. |

---

## Part II — System prompt annotation

### Outline
1. Core Mandates — protects credentials, source control, and system integrity.
2. Context Efficiency — reduces unnecessary turns, searches, and file reads.
3. Engineering Standards — defines code quality, testing, scope, and persistence rules.
4. Topic Updates — keeps the user informed during multi-step work.
5. Available Sub-Agents — delegates suitable work while protecting context and avoiding conflicts.
6. Available Agent Skills — exposes optional specialist instruction packages.
7. Hook Context — treats injected hook data as untrusted, read-only context.
8. Primary Workflows — defines the research, strategy, execution, and validation lifecycle.
9. Operational Guidelines — controls tone, safety, tool sequencing, and interaction behavior.
10. Git Repository — defines safe repository inspection, staging, and commit behavior.

### Annotations (≥6)
#### Section: Tone and Style (tone and verbosity)
> "Focus exclusively on intent and technical rationale. Avoid conversational filler, apologies, and unnecessary per-tool explanations."
>
> "Adopt a professional, direct, and concise tone suitable for a CLI environment."
>
> "Aim for fewer than 3 lines of text output (excluding tool use/code generation) per response whenever practical."
- **Behavior it produces:** [OBSERVED] The agent kept its messages short and focused on the technical purpose of the next action before moving to tool use.
- **Failure it prevents:** [INFERRED] Without these rules, the model could produce many unnecessary explanations and long sentences, lose track of the relevant context, or make comments that are disconnected from its command-line actions.

#### Section: Expertise and Intent Alignment (when not to act / confirm)
> "For Inquiries, or whenever the user explicitly instructs you NOT to make changes just yet, your scope is strictly limited to research and analysis; you may propose a solution or strategy, but you MUST NOT modify files until a subsequent Directive is issued."
>
> "Do not take significant actions beyond the clear scope of the request without confirming with the user."
- **Behavior it produces:** [INFERRED] This rule makes the model work in the way the user actually requested and keeps its actions controlled.
- **Failure it prevents:** [INFERRED] Without this rule, the model could unintentionally move into related systems or files outside the requested scope and modify their code.

#### Section: Development Lifecycle (workflow)
> "Operate using a **Research -> Strategy -> Execution** lifecycle. For the Execution phase, resolve each sub-task through an iterative **Plan -> Act -> Validate** cycle."
- **Behavior it produces:** [OBSERVED] The model can use validation results to revise and fix its work quickly instead of requiring a new user prompt after every step. In this session it read the files, ran the tests, edited the implementation, and tested again.
- **Failure it prevents:** [INFERRED] Without this workflow, the model could produce an incorrect result and stop to wait for the user instead of correcting itself in a systematic way.

#### Section: Tool Execution Response Rules (tool usage)
> "After receiving a `functionResponse`, you MUST ALWAYS execute one of the following two actions: a) Call another tool to proceed with the task. b) Provide a user-facing text response explaining the tool output, your analysis, and next steps."
- **Behavior it produces:** [OBSERVED] This rule tells the model how far to continue after each tool result and keeps it moving forward along the task path instead of treating one tool call as the end of the job.
- **Failure it prevents:** [INFERRED] It prevents the model from stopping suddenly after an operation, returning an empty response, or producing an unrelated answer instead of continuing with the relevant next step.

#### Section: Context Efficiency
> "The agent passes the full history with each subsequent message. The larger context is early in the session, the more expensive each subsequent turn is."
>
> "Prefer using tools like grep_search to identify points of interest instead of reading lots of files individually."
- **Behavior it produces:** [OBSERVED] The rule makes the model focus its reads and searches on relevant information, reducing unnecessary token usage, complexity, and the risk of unrelated changes. The input context still grew from 11,417 tokens on call 1 to 29,460 on call 18 as useful tool results accumulated.
- **Failure it prevents:** [INFERRED] Without this rule, the model could waste tokens by repeatedly reading irrelevant areas and then make different or incorrect inferences from unnecessary context, possibly leading to changes outside the intended scope.

#### Section: Testing and Validation
> "Testing: ALWAYS search for and update related tests after making a code change. You must add a new test case to the existing test file (if one exists) or create a new test file to verify your changes."
>
> "Validation is the only path to finality. Never assume success or settle for unverified changes."
- **Behavior it produces:** [OBSERVED] After revising the code, the model reran the tests to check whether the revision actually passed and added new tests for the new shipping behavior. This step-by-step verification helped bring the whole system to a correctly working state.
- **Failure it prevents:** [INFERRED] Without this rule, the model might make an incorrect code revision and fail to run the tests consistently. It could also introduce new behavior without writing tests for it, leaving those cases unchecked.

### Context injection (`GEMINI.md`)
[OBSERVED] The project-specific contents of `GEMINI.md` are not present in the exported `prompts/system.md` or in `submission/session_system.md`; searching both files for phrases such as `All money is integer **cents**` returns no match. Instead, Gemini CLI loads the file separately at session startup and injects it into the request immediately before the user's prompt. In the raw telemetry, the `request_text` and `gen_ai.input.messages` attributes contain the rules inside `<session_context><loaded_context><project_context>` and end with `--- End of Context from: .../work/run/GEMINI.md ---`. The next text part is the user's `Read TASK.md...` prompt. This shows that the base system instruction and project context are separate inputs even though both reach the model on every subsequent request as the conversation history is resent.

---

## Part III — Tool design

### Inventory
| Category | Tools | Used in session (count) |
|---|---|---|
| File | `read_file`, `list_directory`, `replace`, `write_file` | `read_file` (5), `replace` (4); others 0 |
| Search | `glob`, `grep_search` | None (0) |
| Shell | `run_shell_command`, `list_background_processes`, `read_background_output` | `run_shell_command` (6); others 0 |
| Web | `google_web_search`, `web_fetch` | None (0) |
| Planning and narration | `enter_plan_mode`, `update_topic` | `update_topic` (3), `enter_plan_mode` (0) |
| Delegation and skills | `invoke_agent`, `activate_skill` | None (0) |
| Interaction / other | `ask_user` | None (0) |

[OBSERVED] `/tools desc` listed 16 built-in tools. The session timeline recorded 18 tool calls in total: 6 `run_shell_command`, 5 `read_file`, 4 `replace`, and 3 `update_topic`, with 0 failed tool calls.

### Tool A: `replace`
- **Source file:** [`packages/core/src/tools/definitions/model-family-sets/gemini-3.ts` (v0.64.0, lines 356-394)](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/model-family-sets/gemini-3.ts#L356-L394); implementation in [`packages/core/src/tools/edit.ts`](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/edit.ts)
- **Schema:**
  ```text
  replace({
    file_path: string,
    instruction: string,
    old_string: string,
    new_string: string,
    allow_multiple?: boolean
  })
  ```
- **Why each parameter:** `file_path` identifies the target file. `instruction` gives a self-contained semantic goal so the proposed edit can be understood or modified by a human or another model. `old_string` anchors the change to exact existing content. `new_string` provides the complete replacement content. `allow_multiple` makes broad replacement an explicit choice; when omitted or false, exactly one match is required.
- **Description line that corrects a model mistake:** > "The exact literal text to replace, unescaped. If this string is not the exact literal text ... or does not match exactly, the tool will fail." **Mistake:** [INFERRED] A model may provide an ambiguous or approximate snippet that matches the wrong location or conflicts with multiple locations. Requiring an exact unique match stops the tool instead of silently editing the wrong code.
- **Deliberately does not:** It does not guess which occurrence the model intended, replace every matching occurrence by default, or accept omission placeholders such as `...` in newly generated code. This prevents conflicts, accidental broad edits, and deletion of code that the model left out. Multiple matches require the explicit `allow_multiple: true` parameter.

### Tool B: `run_shell_command`
- **Source file:** [`packages/core/src/tools/definitions/dynamic-declaration-helpers.ts` (v0.64.0, lines 36-159)](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/dynamic-declaration-helpers.ts#L36-L159); implementation in [`packages/core/src/tools/shell.ts`](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/shell.ts)
- **Schema:**
  ```text
  run_shell_command({
    command: string,
    description?: string,
    dir_path?: string,
    is_background?: boolean,
    delay_ms?: integer
  })
  ```
- **Why each parameter:** `command` is the exact command to run. `description` briefly tells the user what it does. `dir_path` chooses an existing directory inside the workspace. `is_background` lets the CLI manage a long-running process. `delay_ms` gives a background process time to produce its first output.
- **Description line that corrects a model mistake:** > "To run a command in the background, set the `is_background` parameter to true. Do NOT use `&` to background commands." **Mistake:** [INFERRED] A model may add `&` itself, leaving a process that Gemini CLI cannot properly track. The parameter lets the CLI follow its output and stop it when needed.
- **Deliberately does not:** It does not allow `dir_path` to point to a directory outside the workspace, and it does not treat `&` as the managed background mechanism. These limits keep commands inside the task scope and prevent background processes from becoming uncontrolled.

### Why old/new string edits?
[INFERRED] First, changing only an exact old string uses fewer tokens than sending and rewriting the whole file. Second, it reduces confusion and the risk of repeatedly changing unrelated old code, which could push the project toward spaghetti code. [OBSERVED] In the session, the first `replace` call changed only `self.items[sku] = quantity` to `self.items[sku] = self.items.get(sku, 0) + quantity` in `shopcart/cart.py`. The rest of the file stayed untouched, and the exact change was easy to review.

### Per-model tool descriptions
The `replace` schema has the same main parameters in the Gemini 3 and legacy sets, but its description is different. The legacy description is much longer: it tells the model to read the file first, include at least three lines before and after the target, explains what a good `instruction` must contain, and gives good and bad examples. The Gemini 3 description is shorter and instead emphasizes surgical edits, lower token use, easier reviews, and avoiding accidental deletions. [INFERRED] The older model family needs more explicit guidance to avoid vague or conflicting edits, while Gemini 3 can follow a shorter schema. The shorter description also saves context tokens. `run_shell_command` does not differ between these two sets because both call the same dynamic declaration helper; its text changes by operating system instead, using `bash -c` on Mac/Linux and PowerShell on Windows.

---

## Part IV — Behavioral analysis

### 1. The loop
```
user task -> response #1 -> read TASK.md -> response #2-3 -> read code/tests
-> run pytest -> response #4-7 -> edit implementation -> run pytest
-> response #8-12 -> read/edit tests -> run full pytest -> response #13-15
-> git status/diff -> update_topic -> response #16 (final answer)
```
What ended it: [OBSERVED] The final tests passed, then the agent checked `git status` and `git diff`. The loop technically ended at response #16, when the model returned `Task Completed Successfully` without requesting another tool. The later `!python -m pytest -q` input was the required independent user check after the agent's loop had already ended.

### 2. Context growth
| Model call | Input tokens | Cached tokens |
|---:|---:|---:|
| 1 | 11,417 | 8,120 |
| 4 | 14,565 | 12,146 |
| 8 | 22,056 | 18,258 |
| 12 | 25,968 | 22,313 |
| 16 | 29,047 | 26,360 |
| 18 | 29,460 | 26,348 |

[OBSERVED] Input context grew from 11,417 tokens on the first call to 29,460 on the last call. Each file read, test result, edit, and model response became part of the history sent on later calls. This is why unnecessary reads could waste tokens or add confusing information. Cached tokens grew from 8,120 to about 26,000 because much of the earlier system prompt and conversation history was repeated. [INFERRED] Caching does not remove content from the context, but reusing already processed tokens can make later calls faster and cheaper than processing the full repeated history from scratch.

### 3. Planning
[OBSERVED] The agent used `update_topic` three times: `Reading Task & Planning` at the start, an implementation phase after the first failing test run, and `Task Completed Successfully` at the end. It did not use `write_todos` or enter plan mode. Its implementation matched the broad phases it tracked: inspect, implement, test, and finish. However, it immediately called `read_file` on `TASK.md` and then read the code and tests without first showing the user a clear written plan. Because no explicit plan was shown, a detailed plan-versus-action comparison is not possible; the first departure from the requested process was call #1, where it began tool use before presenting the plan. It followed the request to continue without waiting for confirmation, but it did not fully follow `First write out your plan`. [INFERRED] This is a weakness because the user cannot understand or review the intended path before work begins. If the agent only explains what it did several steps later, the user has less control and becomes less familiar with what is happening in the project.

### 4. Error recovery
> "FAILED tests/test_cart.py::test_add_same_item_twice_increments_quantity"
>
> "FAILED tests/test_cart.py::test_fixed_discount_applied_before_tax"
>
> "2 failed, 12 passed in 0.03s — Exit Code: 1"

[OBSERVED] The agent used the failing assertions to identify the problems, edited `cart.py` and `pricing.py`, and ran the tests again. It then added tests for the missing shipping cases and finished with 19 passing tests. There were no failed tool calls; the non-zero exit code was the expected starting state of the project. [INFERRED] The recovery was good because it fixed the failed behavior, added tests for missing cases, and brought the system to the requested working state instead of stopping after the first failure.

### 5. The tests
[OBSERVED] The agent changed three existing `Cart.total()` expected values. For example:

```diff
- assert cart.total() == 2160  # 2000 + 8% tax
+ assert cart.total() == 2759  # (2000 + 8% tax) + $5.99 shipping
```

It made the same type of update to the percentage and fixed-discount total tests. These edits were allowed by `TASK.md`, which permitted updates only to old `Cart.total()` expectations and required a comment explaining why. The inline `+$5.99 shipping` comments provide that explanation. It did not rewrite the purpose of those tests. It also added a cart-level free-shipping threshold test and four direct `calculate_shipping` tests for below, at, above, and zero subtotals, which satisfied the separate instruction to add shipping coverage.

### 6. Models
[OBSERVED] All 18 model calls used `gemini-3.5-flash-lite`; there was no model switch or fallback. The highest `thoughts_token_count` was call #4 with 2,954 tokens, immediately after the initial failing test run, when the agent was deciding how to fix the two bugs and add shipping. The next largest were call #5 (835) before the first implementation edit, call #6 (709) before the pricing edit, call #8 (661) after rerunning the tests, and call #10 (529) before editing the cart tests. These peaks happened around decisions about implementation and test updates rather than simple status checks.

[INFERRED] Without `-m`, a small router model can cheaply and quickly decide where each request should go, while a larger work model handles the harder coding. This split saves time and cost on routing. Running the whole session on the bigger model would probably be slower and more expensive but could improve reasoning and code quality or reduce mistakes on difficult steps. For this lab, forcing one model made every call easier to compare and ensured one tool-description set was used throughout.
