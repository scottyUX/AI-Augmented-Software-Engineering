# Week 3 Writeup — Inside a Coding Agent

**Name:** `izzettin12` (GitHub username)  
**Gemini CLI version:** `0.64.0`  
**OS / shell:** Windows 11 / PowerShell in VS Code  
**Model(s) seen in trace:** `gemini-3.5-flash-lite`  
**Session commit:** None; the agent did not commit. Its changes are preserved in `run/`.

> Evidence tags: `[OBSERVED]` cites the exported session timeline, API-call CSV, or
> saved source file. `[INFERRED]` marks an interpretation rather than a directly
> recorded fact. Personal home-directory details have been redacted from exported files.

## Part I — Session

**Narrative:** [OBSERVED] I asked Gemini CLI to read `TASK.md`, plan, and complete the
shopcart task. It inspected the task and relevant code/tests, ran the initial suite,
found two failures, corrected quantity accumulation and the order of discount and tax,
implemented shipping, updated the affected total expectations, and added shipping tests.
It reran the suite successfully, then inspected Git status and the diff. I did not send
any additional task instructions or intervene while the agent worked. I independently
ran the final suite afterward; all 22 tests passed.

| Metric | Value |
|---|---|
| User prompts | 1 |
| Model calls | 14; 0 API errors |
| Tool calls | 19; 0 failed |
| Tool-call breakdown | `read_file` 6; `update_topic` 4; `run_shell_command` 4; `replace` 4; `grep_search` 1 |
| Final pytest result | 22 passed; independently rerun after the agent finished |
| Did I step in? | No; one initial task prompt, no mid-session interventions |
| Session commit | The agent did not commit; its changes remain in `run/` for the submission commit |

Evidence: [OBSERVED] `submission/session_timeline.txt` gives the event sequence and
summary; `submission/session_calls.csv` records the 14 responses and their model fields.
[OBSERVED] The trace records two tool calls as `auto_accept` (the baseline shell test
and the first `replace`) and the other accepted actions as `accept`; no YOLO flag was
used.

## Part II — System prompt annotation

### Outline

1. **Core Mandates:** security/source-control rules, context efficiency, and engineering
   expectations.
2. **Topic Updates:** when to narrate or change the current work phase.
3. **Available Sub-Agents / Available Agent Skills:** delegation and skill options.
4. **Hook Context:** treats hook-provided material as read-only data.
5. **Primary Workflows:** research, strategy, execution, and the development lifecycle.
6. **Operational Guidelines:** tone, safety, and tool-use behavior.
7. **Interaction Details:** help and feedback commands.
8. **Git Repository:** stage/commit/push restrictions and review steps.

### Annotations

#### Section: Security & System Integrity

> “Do not stage or commit changes unless specifically requested by the user.”

- **Behavior it produces:** The agent keeps edits in the working tree unless asked to
  commit.
- **Failure it prevents:** An unexpected commit or publication of unfinished changes.
- **Evidence:** [OBSERVED] The agent checked `git status` and `git diff` after tests but
  did not create a commit (`session_timeline.txt`, final two shell calls).

#### Section: Context Efficiency

> “Be strategic in use of the available tools to minimize unnecessary context.”

- **Behavior it produces:** It prefers targeted reads/searches over repeatedly loading
  large files.
- **Failure it prevents:** Spending context on irrelevant files and losing useful task
  information to context growth.

#### Section: Engineering Standards — intent alignment

> “Distinguish between Directives … and Inquiries.”

- **Behavior it produces:** It checks whether the user asked for action before changing
  files.
- **Failure it prevents:** Treating a question or observation as permission for a
  potentially unwanted code change.

#### Section: Primary Workflows — development lifecycle

> “Research -> Strategy -> Execution” and, within execution, “Plan -> Act -> Validate.”

- **Behavior it produces:** It reads the task and related code, states the intended
  implementation sequence, edits, then tests.
- **Failure it prevents:** Coding before understanding the failing behavior or declaring
  success without running validation.
- **Evidence:** [OBSERVED] The trace begins with task/code reads and a failing baseline,
  then code and test edits, then a passing suite (`session_timeline.txt`).

#### Section: Tone and Style

> “Concise & Direct” and “Aim for fewer than 3 lines of text output … whenever practical.”

- **Behavior it produces:** Short, technical user-facing summaries rather than extended
  conversational narration.
- **Failure it prevents:** Hiding important results in unnecessary chat.

#### Section: Security and Safety Rules

> “Before executing commands with `run_shell_command` that modify the file system, codebase, or system state, you must provide a brief explanation.”

- **Behavior it produces:** The agent is instructed to explain consequential shell
  actions before running them.
- **Failure it prevents:** A user being surprised by a command that changes files or
  system state.

#### Section: Tool Usage

> “After receiving a `functionResponse`, you MUST … call another tool … or provide a user-facing text response.”

- **Behavior it produces:** The agent continues the workflow or reports what happened
  after each tool response.
- **Failure it prevents:** Ending silently after a tool call or leaving the user unsure
  whether the task advanced.

#### Section: Git Repository

> “Do not use `git add .` or `git add -A` unprompted.”

- **Behavior it produces:** It should stage only explicitly selected files.
- **Failure it prevents:** Accidental inclusion of unrelated or sensitive untracked files.

### Context injection (`GEMINI.md`)

[OBSERVED] The first model input contained a separate “Context from: …/GEMINI.md” block
with the project rules, including “Python 3.10+ library” and “Never use floats for stored
amounts.” Those project-specific instructions do **not** appear as the `GEMINI.md` file
itself in the exported system prompt; Gemini CLI adds them to model context at runtime.
The source file is [`run/GEMINI.md`](./run/GEMINI.md), and the CLI's first prompt context
was verified from the local trace. Home-directory strings were not retained in the
submission.

## Part III — Tool design

### Inventory

The following inventory is from `/tools` in this `v0.64.0` session. “Used” counts are
from `submission/session_timeline.txt`; zero means no invocation appeared in the trace.

| Category | Available tools | Used in session |
|---|---|---:|
| File | `read_file`, `list_directory` (ReadFolder), `replace` (Edit), `write_file` | 10 (`read_file` 6, `replace` 4; others 0) |
| Search | `glob` (FindFiles), `grep_search` (SearchText) | 1 (`grep_search`) |
| Shell / background | `run_shell_command`, `list_background_processes`, `read_background_output` | 4 (`run_shell_command`; background tools 0) |
| Web | `google_web_search`, `web_fetch` | 0 |
| Planning and narration | `enter_plan_mode`, `update_topic` | 4 (`update_topic`; plan mode 0) |
| Delegation / skills | `invoke_agent`, `activate_skill` | 0 |
| Other | `ask_user` | 0 |

### Tool A: `replace`

**Versioned source:** [`gemini-3.ts`, lines 356–388](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/model-family-sets/gemini-3.ts#L356-L388);
shared parameter names are in
[`base-declarations.ts`, lines 64–69](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/base-declarations.ts#L64-L69).

**Schema (required parameters marked):**

```text
file_path: string              [required]
instruction: string            [required]
old_string: string             [required]
new_string: string             [required]
allow_multiple: boolean        [optional]
```

- `file_path` selects the workspace file.
- `instruction` conveys the intent and desired outcome of the edit.
- `old_string` is the exact existing text to locate.
- `new_string` is the exact replacement text.
- `allow_multiple` opts in to replacing repeated exact matches rather than requiring a
  single match by default.

**Description line that corrects a model mistake:** “expects to find and replace exactly
ONE occurrence of `old_string`.” This discourages broad or ambiguous edits that could
change unintended matches.

**Deliberately does not:** Treat a line number as a stable patch location or silently
rewrite an entire existing file. It relies on matching the current file content and
checking that the match is unique unless multiple replacements are explicitly requested.

**Why exact old/new strings?** [INFERRED] Line numbers can become stale as nearby code
changes, while exact context identifies the intended source text. A narrow replacement
also makes the change easier to inspect and reduces accidental collateral edits.
[OBSERVED] The agent used this style to change quantity handling in `cart.py` (tool call
near 14:43:10; visible in the session transcript as `Edit cart.py (+1, -1)`) and to add
shipping logic and tests.

### Tool B: `run_shell_command`

**Versioned source:** [`dynamic-declaration-helpers.ts`, lines 36–79 and 85–120](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/dynamic-declaration-helpers.ts#L36-L120);
the shared tool and parameter names are in
[`base-declarations.ts`, lines 55–58](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/base-declarations.ts#L55-L58).

**Schema for this Windows session (required parameters marked):**

```text
command: string                [required]
description: string            [optional]
dir_path: string               [optional]
is_background: boolean         [optional]
delay_ms: integer               [optional]
```

- `command` is the exact command to execute.
- `description` explains the command's purpose to the user.
- `dir_path` selects an existing working directory within the workspace.
- `is_background` requests managed background execution for long-running work.
- `delay_ms` controls how long to wait before returning from a background start.

The `v0.64.0` declaration makes only `command` required; the session's tool schema is
preserved in `submission/session_tools.md`.

**Description line that corrects a model mistake:** “executes a given shell command as
`powershell.exe -NoProfile -Command <command>`.” This prevents using Unix/Bash command
syntax on the Windows shell. The same source describes background execution through
`is_background` rather than a PowerShell background construct.

**Deliberately does not:** Convert arbitrary code edits into a structured patch. It runs
the supplied shell command; it does not offer the exact-match safeguards of `replace`.

### Why different model-family descriptions?

[`gemini-3.ts`](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/model-family-sets/gemini-3.ts#L356-L388)
describes `replace` as a surgical edit that minimizes token use and accidental
deletions. [`default-legacy.ts`](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/model-family-sets/default-legacy.ts#L349-L401)
is more prescriptive: it adds requirements for surrounding context, exact whitespace,
small atomic edits, and rereading after changes.

[INFERRED] Keeping schemas aligned while tailoring the explanation lets the CLI give
different model families the amount and style of guidance that best steers their tool
use. The Gemini 3 wording is compact and emphasizes the tool's design rationale; the
legacy wording more explicitly spells out operational steps to avoid malformed edits.

## Part IV — Behavioral analysis

### 1. The loop

```text
user prompt
→ call 1: update_topic + read TASK.md
→ call 2: read cart.py, pricing.py, and both test files
→ call 3: update_topic → run baseline pytest (2 failures)
→ call 4: grep_search("total")
→ call 5: update_topic
→ call 6: replace cart.py
→ call 7: replace pricing.py
→ call 8: replace test_cart.py
→ call 9: read test_pricing.py
→ call 10: replace test_pricing.py
→ call 11: update_topic → run pytest (22 passed)
→ call 12: git status
→ call 13: git diff
→ call 14: final response
```

[OBSERVED] This sequence is summarized in `submission/session_timeline.txt`. The agent
ended the session after the final checks and status review; it was not stopped by an
API error or an external intervention. It did not create a commit.

### 2. Context growth

[OBSERVED] `input_token_count` rises from 11,367 on the first API response to 27,160 on
the fourteenth: an increase of 15,793 tokens (about 139%). The table lists every
response; `cached_content_token_count` is the reusable cached portion recorded for that
call.

| Call | Input tokens | Cached tokens |
|---:|---:|---:|
| 1 | 11,367 | 0 |
| 2 | 11,937 | 8,115 |
| 3 | 13,782 | 10,132 |
| 4 | 14,462 | 12,150 |
| 5 | 19,074 | 14,206 |
| 6 | 20,604 | 18,268 |
| 7 | 21,232 | 0 |
| 8 | 22,725 | 20,297 |
| 9 | 25,187 | 22,338 |
| 10 | 25,438 | 22,331 |
| 11 | 26,454 | 24,360 |
| 12 | 26,784 | 24,346 |
| 13 | 27,065 | 24,340 |
| 14 | 27,160 | 24,332 |

[INFERRED] The input grows because the conversation history, code/test context, tool
results, and edits accumulate across calls. A nonzero cached count indicates that some
input content could be reused by the provider instead of being processed as entirely
new input; caching can reduce repeat processing latency and cost, subject to the
provider's billing rules. Call 7's zero shows caching was not reported for every call.

### 3. Planning

[OBSERVED] The agent used `update_topic` four times: to start task reading/planning, run
the initial tests, implement the fixes, and validate. It did not use `enter_plan_mode`.
The plan broadly matched the work: inspect task and code, reproduce failures, implement,
test, and inspect the result. It also ran `git status` and `git diff` after the passing
test run as a final review. Evidence: topic and tool events in `session_timeline.txt`.

### 4. Error recovery

> [OBSERVED] Initial pytest: `test_add_same_item_twice_increments_quantity` and
> `test_fixed_discount_applied_before_tax` failed; the baseline reported `2 failed,
> 12 passed`.

[OBSERVED] The agent searched for `total`, then changed `Cart.add_item` to accumulate
quantities and changed pricing so the discount is applied before tax. It implemented
shipping in `pricing.py`, updated affected cart-total expectations, and added shipping
coverage. The next full run passed all 22 tests. This was effective recovery: it used
the failing tests to identify the relevant behavior and then verified the correction.
There were no failed tool calls (`session_timeline.txt`).

### 5. The tests

[OBSERVED] The agent did not edit existing test behavior outside the assignment's
allowance. In `tests/test_cart.py`, it changed only three existing total expectations to
include shipping, with comments explaining the $599 fee; it added new cart shipping
cases. In `tests/test_pricing.py`, it added direct tests for empty-cart shipping,
below/at/above-threshold behavior, and a discount that moves the post-discount amount
below the free-shipping threshold. The assignment expressly allowed the old total
expectations to change and required shipping tests.

Example from the recorded edit:

```diff
- assert cart.total() == 2160  # 2000 + 8% tax
+ assert cart.total() == 2759  # 2000 + 8% tax + 599 shipping
```

The run copy and its tests are in `run/`; the final test result was also independently
confirmed after the CLI session.

### 6. Models

[OBSERVED] Every `model` value in `submission/session_calls.csv` is
`gemini-3.5-flash-lite` (14 calls). The CLI was explicitly started with
`-m gemini-3.5-flash-lite`, so this trace does not show the no-`-m` default router/work
model split.

[OBSERVED] The largest `thoughts_token_count` was 4,055 at call 4, after the failing
baseline and before `grep_search`; the next largest was 1,395 at call 5, before the
implementation phase. [INFERRED] These peaks are consistent with diagnosing the initial
failures and planning the fix, but token counts do not reveal the model's private
reasoning content.

[INFERRED] A CLI can use a smaller routing model to classify or route incoming requests
quickly and reserve a larger work model for code changes. If an entire session used a
larger model, latency and cost could rise while complex reasoning or code quality might
improve; neither outcome is guaranteed, and this run does not compare models.
