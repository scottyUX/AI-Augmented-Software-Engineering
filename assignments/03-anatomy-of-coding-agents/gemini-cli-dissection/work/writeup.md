# Week 3 Writeup — Inside a Coding Agent

**Name:** Riza Arslan
**Gemini CLI version (`gemini --version`):** 0.64.0  <!-- confirm from your terminal -->
**OS / shell:** Windows + Git Bash (VS Code terminal)
**Model(s) seen in trace:** TODO — read the `model` column of `submission/session_calls.csv` (expected: `gemini-3.5-flash-lite`)
**Session commit:** `TODO-sha`  <!-- git log --oneline -1 after the "Gemini CLI session" commit -->

> Evidence tags: `[OBSERVED]` = cite a timeline line, call number, or diff hunk.
> `[INFERRED]` = say what you're reasoning from.
> Source links point at the `v0.64.0` tag of google-gemini/gemini-cli.

---

## Part I — Session

**Narrative (one paragraph):** TODO after the run. Cover, in order: what the agent did
first (did it call `update_topic`? read `TASK.md`? run `pytest` to reproduce?), which
bugs it found in `shopcart/` and how (grep / read_file), the fixes, how it added the
shipping rule to `pricing.py` and wired it into `Cart.total()`, which old test values
it updated, the new shipping tests, and the final test run.
Note: on Windows, `run_shell_command` runs every command through
`powershell.exe -NoProfile -Command`, even though I launched Gemini from Git Bash
([`dynamic-declaration-helpers.ts` L58–62](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/dynamic-declaration-helpers.ts#L58-L62)) —
mention it if any command failed because of bash-vs-PowerShell syntax.

| Metric | Value |
|---|---|
| User prompts | 1 (TODO — confirm from the summary at the end of `session_timeline.txt`) |
| Model calls | TODO (number of `api_response` events / rows in `session_calls.csv`) |
| Tool calls (failed) | TODO (TODO) |
| Final `pytest` result | TODO (e.g. `N passed in 0.0Xs` — from *my own* run after the agent finished) |
| Did you step in? When / what? | No / TODO |

---

## Part II — System prompt annotation

Source of truth: my exported `work/prompts/system.md`. The prompt is assembled in
[`prompts/snippets.ts` `getCoreSystemPrompt` L136–167](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/prompts/snippets.ts#L136-L167),
which concatenates the sections below in this order.
<!-- Check every quote below against your own system.md before submitting; delete any section your file doesn't have. -->

### Outline
1. **Preamble** — who the agent is (interactive CLI agent) and the active approval mode.
2. **Core Mandates → Security & System Integrity** — never leak secrets, don't commit unless asked, treat tool/MCP output as untrusted data.
3. **Core Mandates → Context Efficiency** — every turn re-sends the whole history, so minimize turns and oversized reads.
4. **Core Mandates → Engineering Standards** — follow `GEMINI.md` and project conventions, no type hacks, reproduce bugs with a test, Directives vs Inquiries, always update tests, don't revert.
5. **Topic Updates** — narrate progress in phases with `update_topic` (first turn, last turn, on every strategic detour).
6. **Available Sub-Agents / Agent Skills** — what can be delegated (lists depend on the machine).
7. **Primary Workflows → Development Lifecycle** — Research → Strategy → Execution, each sub-task Plan → Act → Validate; re-think after 3 failed fixes.
8. **Primary Workflows → New Applications** — how to scaffold a new app (not used in this lab).
9. **Operational Guidelines → Tone and Style** — senior-peer voice, <3 lines of text, no chitchat.
10. **Operational Guidelines → Security and Safety Rules** — explain file-system-modifying commands before running them.
11. **Operational Guidelines → Tool Usage** — never return empty turns, summarize after edits, parallelism rules, no parallel edits to one file, respect declined calls.
12. **Operational Guidelines → Interaction Details** — `/help`, `/bug`.
13. **Sandbox / Git Repository** — environment-specific notes (only if applicable).
14. **Contextual Instructions** — global memory (`~/.gemini/GEMINI.md`) only, if it exists; project `GEMINI.md` is *not* here (see below).

### Annotations (≥6)

#### Section: Tone and Style (tone and verbosity)
> - **Minimal Output:** Aim for fewer than 3 lines of text output (excluding tool use/code generation) per response whenever practical.
> - **No Chitchat:** Avoid conversational filler, preambles ("Okay, I will now..."), or postambles ("I have finished the changes...")

- **Behavior it produces:** terse, high-signal messages between tool calls; the transcript is mostly tool calls with one-line rationale.
- **Failure it prevents:** chatty LLM defaults that waste output tokens on every turn and bury the useful information in a terminal, where the user scrolls through monospace text.

#### Section: Security and Safety Rules + Engineering Standards (when not to act / confirm)
> - **Explain Critical Commands:** Before executing commands with `run_shell_command` that modify the file system, codebase, or system state, you *must* provide a brief explanation of the command's purpose and potential impact. … You should not ask permission to use the tool; the user will be presented with a confirmation dialogue upon use

> For Inquiries, or whenever the user explicitly instructs you NOT to make changes just yet … you MUST NOT modify files until a subsequent Directive is issued.

- **Behavior it produces:** the agent states *why* before a state-changing command, then relies on the CLI's approval dialog (the human-in-the-loop gate) rather than asking in chat; and it only edits files when the request is an explicit instruction.
- **Failure it prevents:** (1) the user approving a destructive command blindly because they don't know what it does; (2) double-confirmation loops ("may I run this?" → dialog → approve again); (3) the agent "helpfully" changing code when the user only asked a question.

#### Section: Development Lifecycle (workflow)
> Operate using a **Research -> Strategy -> Execution** lifecycle. For the Execution phase, resolve each sub-task through an iterative **Plan -> Act -> Validate** cycle.

> **Validation is the only path to finality.** Never assume success or settle for unverified changes.

- **Behavior it produces:** the agent reads before writing, plans per sub-task, and runs the tests after each change instead of declaring victory. In this lab: understand the failures → fix → `pytest` → add shipping → `pytest`.
- **Failure it prevents:** "edit and hope" — changes that look plausible but break other code, and premature "done" messages without a passing test run.

#### Section: Tool Usage (tool usage)
> - **File Editing Collisions:** Do NOT make multiple calls to the `replace` tool for the SAME file in a single turn. To make multiple edits to the same file, you MUST perform them sequentially across multiple conversational turns

> 2. You MUST NEVER return an empty response with no text and no tool calls.

- **Behavior it produces:** parallel calls only for independent work (reads, searches, edits to *different* files); edits to one file are serialized; every turn either calls a tool or says something.
- **Failure it prevents:** race conditions where two edits are computed against the same original text and the second one fails (its `old_string` no longer exists) or overwrites the first; and silent empty turns that stall the agent loop.

#### Section: Context Efficiency
> - The agent passes the full history with each subsequent message. The larger context is early in the session, the more expensive each subsequent turn is.

- **Behavior it produces:** the agent prefers `grep_search` with limits over reading many whole files, batches reads in parallel, and reads enough to make a `replace` unambiguous on the first try.
- **Failure it prevents:** context bloat — a big early read is paid for on *every* later call (exactly the growth I measure in Part IV.2) — and extra turns caused by failed, ambiguous edits.

#### Section: Engineering Standards → Contextual Precedence / Testing
> - **Contextual Precedence:** Instructions found in `GEMINI.md` files are foundational mandates. They take absolute precedence over the general workflows and tool defaults described in this system prompt.

> - **Testing:** ALWAYS search for and update related tests after making a code change.

- **Behavior it produces:** project rules from `GEMINI.md` (integer cents, pricing rules live in `pricing.py`, run `python -m pytest -q`) override the agent's defaults; every feature comes with tests.
- **Failure it prevents:** the agent applying generic habits that break this repo (e.g. floats for money, putting shipping logic in `cart.py`), and shipping untested features.

#### Section: Core Mandates → Security & System Integrity
> - **Source Control:** Do not stage or commit changes unless specifically requested by the user.

- **Behavior it produces:** the agent leaves changes in the working tree; I committed them myself as one "agent's changes" commit.
- **Failure it prevents:** unreviewed commits (possibly including secrets or half-finished work) entering history without the human seeing them.

### Context injection (`GEMINI.md`)
**`GEMINI.md`'s content is NOT in the exported `system.md`.** <!-- Verify: grep -n "integer" work/prompts/system.md → expect no hit -->
In v0.64.0 Gemini CLI uses a *tiered* context model:

- `config.getSystemInstructionMemory()` returns only **Tier 1** (global `~/.gemini/GEMINI.md` + user-project memory) for the system prompt — [`config/config.ts` L2591–2611](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/config/config.ts#L2591-L2611). Its comment says extension and project memory "are placed in the first user message instead".
- The project file is **Tier 2**: `getEnvironmentContext()` calls `config.getSessionMemory()` and puts the result into the **first user message**, inside a `<session_context>` block together with the date, OS and folder structure — [`utils/environmentContext.ts` L62–77](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/utils/environmentContext.ts#L62-L77). `getInitialChatHistory()` puts that message at the start of the history — [`core/client.ts` L422](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/core/client.ts#L422).
- Tier 3 (sub-directory `GEMINI.md` files) arrives just-in-time in tool output.

**Trace evidence:** TODO — run
`python ../../tools/summarize_log.py ../telemetry.log --context ../submission/session_context.md`
and quote the line from `<session_context>` showing "All money is integer **cents**". [OBSERVED]

---

## Part III — Tool design

### Inventory
<!-- Paste your actual /tools output; this list is from the v0.64.0 source and some tools only appear with certain settings. -->
| Category | Tools | Used in session (count) |
|---|---|---|
| File | `read_file`, `read_many_files`, `write_file`, `replace`, `list_directory` | TODO |
| Search | `glob`, `grep_search` | TODO |
| Shell | `run_shell_command` (incl. `is_background`) | TODO |
| Web | `google_web_search`, `web_fetch` | TODO |
| Planning and narration | `update_topic`, `write_todos`, `enter_plan_mode`, `exit_plan_mode`, `tracker_*` (`create_task`, `update_task`, `get_task`, `list_tasks`, `add_dependency`, `visualize`) | TODO |
| Delegation | `invoke_agent` (sub-agents), `activate_skill` | TODO |
| Other | `ask_user`, `get_internal_docs`, `complete_task`, `list_mcp_resources`, `read_mcp_resource` | TODO |

Counts: from the `tool_call` lines in `session_timeline.txt` (e.g. `grep -c "read_file" session_timeline.txt`).

### Tool A: `replace` (file edit)
- **Source file:** name/params [`base-declarations.ts` L64–69](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/base-declarations.ts#L64-L69); schema [`model-family-sets/gemini-3.ts` L356–394](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/model-family-sets/gemini-3.ts#L356-L394); implementation [`edit.ts`](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/edit.ts)
- **Schema:**
  ```
  replace(
    file_path:      string   (required)  "The path to the file to modify."
    instruction:    string   (required)  "A clear, semantic instruction for the code change …"
    old_string:     string   (required)  "The exact literal text to replace, unescaped. …"
    new_string:     string   (required)  "The exact literal text to replace `old_string` with …"
    allow_multiple: boolean  (optional, default false)
  )
  ```
- **Why each parameter:**
  - `file_path` — which file; validated and resolved, and must pass `validatePathAccess` so the agent can't write outside the workspace (`validateToolParamValues`, edit.ts L1176–1239).
  - `old_string` — the *anchor*: the edit is located by content, not position, so it is self-checking — if the text isn't there (or isn't unique) the edit fails loudly (edit.ts L366–376).
  - `new_string` — the exact replacement; small and reviewable in the approval diff.
  - `instruction` — not needed for the happy path. It exists for **self-correction**: when the match fails, `attemptSelfCorrection` sends `instruction`, `old_string`, `new_string`, the error and the current file to a *separate* LLM call, `FixLLMEditWithInstruction` (edit.ts L547–600), which repairs the edit. The instruction tells that second model what the edit was *for*.
  - `allow_multiple` — explicit opt-in for replace-all; without it, 2+ matches is an error ("expected 1 occurrence but found N"), so the agent can't accidentally edit the wrong copy.
- **Description line that corrects a model mistake:**
  > Do not use omission placeholders like '(rest of methods ...)', '...', or 'unchanged code'; provide exact literal code.

  **Mistake:** "lazy" elision — models abbreviate unchanged code with `...`, which would literally write `...` into the file and delete the real code. It is also *enforced*: `validateToolParamValues` rejects a `new_string` with a new placeholder via `detectOmissionPlaceholders` (edit.ts L1225–1236).
- **Deliberately does not:** guess which match you meant. If `old_string` appears more than once and `allow_multiple` is false, it refuses instead of picking the first one (edit.ts L372–376). Why: silently editing the wrong occurrence (e.g. a second identical `return total` line) produces a bug that looks like success. It also doesn't take line numbers (see the design question).

### Tool B: `run_shell_command`
- **Source file:** name/params [`base-declarations.ts` L56–58](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/base-declarations.ts#L56-L58); description + schema built at runtime by [`getShellToolDescription` L36 / `getShellDeclaration` L85 in `dynamic-declaration-helpers.ts`](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/dynamic-declaration-helpers.ts#L36-L140); implementation [`shell.ts`](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/shell.ts)
- **Schema:**
  ```
  run_shell_command(
    command:       string   (required)  Windows: "Exact command to execute as `powershell.exe -NoProfile -Command <command>`"
                                        Mac/Linux: "Exact bash command to execute as `bash -c <command>`"
    description:   string   (optional)  "Brief description of the command for the user …"
    dir_path:      string   (optional)  directory to run in; must exist inside the workspace
    is_background: boolean  (optional)  run long-lived processes (servers, watchers) in background
    delay_ms:      integer  (optional)  wait after starting a background process to capture early output
    additional_permissions: object (only when tool sandboxing is enabled)
  )
  ```
- **Why each parameter:**
  - `command` — the command itself; its description names the exact interpreter so the model writes the right syntax for the OS.
  - `description` — shown to the human in the approval dialog; this is the "explain critical commands" rule turned into a field.
  - `dir_path` — run in a sub-folder without `cd … &&` chains; checked by `validatePathAccess` (shell.ts L1220–1233).
  - `is_background` + `delay_ms` — lets the agent start a server without blocking the loop forever, while still catching an immediate crash.
  - `additional_permissions` — request more sandbox access after an "Operation not permitted" failure instead of giving up.
- **Description line that corrects a model mistake:**
  > To run a command in the background, set the `is_background` parameter to true. Do NOT use `&` to background commands.

  (Windows wording: "Do NOT use PowerShell background constructs.") **Mistake:** models trained on shell scripts append `&`; the CLI then can't track the process — output is lost, the process is orphaned, or the call hangs.
- **Deliberately does not:** run commands that contain command substitution (`$()`, backticks, `<()`, `>()`; on PowerShell also `@()`). `execute()` blocks them with "Command injection detected … the command was blocked" (shell.ts L529–539). Why: approvals and "always allow" rules are keyed on the command's root (e.g. `pytest`, `getCommandRoots`); substitution could hide a second command inside an approved one. It also doesn't run forever — an inactivity timeout cancels stuck commands (shell.ts L554–661, L876–882).

### Why old/new string edits?
1. **Robust to drift.** Line numbers go stale the moment an earlier edit adds or removes a line, and models are unreliable at counting lines. Exact text is self-locating and self-verifying: if the file changed, the match fails loudly instead of editing the wrong line.
2. **Cheap and safe compared with rewriting the file.** The model outputs only the changed region (fewer output tokens), it can't accidentally drop unrelated code with `...`, and the human reviews a small diff in the approval dialog (the description itself says it "minimizes token usage, simplifies code reviews, and avoids accidental deletions").
   (Bonus: there's a recovery path — flexible whitespace matching (edit.ts ~L180–235) and the `FixLLMEditWithInstruction` fixer — which only works because the edit is described semantically.)

**Trace moment:** TODO — search `session_timeline.txt` for a failed `replace` (e.g. "0 occurrences" / "expected 1 occurrence"). If one exists, quote it and describe the retry. If none: [INFERRED] the agent read each file in full before editing (small files), so every `old_string` matched on the first try — it never came up.

### Per-model tool descriptions
Tool compared: `replace` —
[`gemini-3.ts` L356](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/model-family-sets/gemini-3.ts#L356) vs
[`default-legacy.ts` L349](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/model-family-sets/default-legacy.ts#L349).

| | `default-legacy.ts` (older models) | `gemini-3.ts` (Gemini 3.x) |
|---|---|---|
| Length | Long: a numbered "Expectation for required parameters" list (5 rules) + **Important**/**CRITICAL** warnings | 2 short paragraphs |
| Context rule | "Include at least 3 lines of context BEFORE and AFTER the target text" (in both the description and `old_string`) | Only "requires providing significant context" |
| Read first | "Always use the read_file tool to examine the file's current content before attempting a text replacement." | Removed |
| Escaping | "NEVER escape `old_string` or `new_string`"; params say "*preferably* unescaped" | Params say "unescaped" (one line) |
| `instruction` param | Long guide: WHY / WHERE / WHAT / outcome + GOOD and BAD examples | One sentence |
| Rationale | — | Adds *why* to prefer it: "minimizes token usage, simplifies code reviews, and avoids accidental deletions" |

**Why describe the same tool differently?** Tool schemas are sent with *every* request, so every word costs input tokens on every call. Older/weaker models made specific mistakes (too little context → ambiguous matches, escaped strings, vague instructions for the fixer), so their description spells out each rule with examples. Newer models follow a short spec reliably, so the extra rules are pure overhead and the description becomes a concise contract. In other words, the tool description is a prompt tuned to the model, just like the system prompt (there are separate `snippets.ts` and `snippets.legacy.ts` too).
Interesting contrast: `run_shell_command` is **identical** across both files — both call the same `getShellDeclaration()` — because its description depends on the OS (bash vs PowerShell), not on the model.

---

## Part IV — Behavioral analysis

### 1. The loop
```
TODO: write it from session_timeline.txt, e.g.
user_prompt → call#1 → update_topic + read_file(TASK.md) → call#2 → run_shell_command(pytest) [FAIL]
→ call#3 → read_file(pricing.py), read_file(cart.py) → call#4 → replace(pricing.py) → … → call#N (text only, no tool) → end
```
What ended it: TODO — normally [OBSERVED] the last model call returned text with no tool call (the agent decided it was done); cite that call number.

### 2. Context growth
TODO — run `python plot_context.py submission/session_calls.csv --out submission/context_growth.png` and embed:
`![Context growth](submission/context_growth.png)`

Explanation to adapt: [OBSERVED] `input_token_count` rises roughly monotonically from call #1 to call #N. [INFERRED] The model is stateless — each call re-sends the system prompt, the tool schemas, the `<session_context>` message, and the *entire* history so far, including every file the agent read and every test output; each turn appends more, so input grows. Big jumps line up with calls right after a `read_file` or a `pytest` run (cite them). `cached_content_token_count` [OBSERVED values] shows how much of that input was served from the provider's context cache — the unchanged prefix (system prompt + earlier history). Cached tokens are billed at a discount and skip re-processing, so a long session costs and waits far less than the raw input count suggests; this is why the agent appends to history instead of rewriting it, and why the system prompt says early large reads make every later turn more expensive.

### 3. Planning
TODO. Check: did call #1 contain an `update_topic`? How many `update_topic` calls in total, and with which titles? Did it use `write_todos`, a tracker tool, or plan mode? Compare against the "Topic Updates" section ("Always call update_topic in your first turn", "call … when you experience an unexpected event", "3 or more times"). Point to where it departed from its written plan (e.g. a test failure caused an extra fix phase).

### 4. Error recovery
> TODO — quote the first failure (most likely the first `pytest` run: the starter tests fail on purpose).

TODO — what the agent did next (read the failing module? grep the function?), how many calls until that failure was fixed, and whether recovery was good (targeted vs. trial-and-error; did it re-run tests to confirm?).

### 5. The tests
TODO — run `git show <session-sha> -- run/tests/` and quote the diff. TASK.md rules: step 1 must **not** edit tests; step 2 may update *only* the `Cart.total()` expected values that changed because of shipping, *with a comment explaining why*; step 3 should **add** new shipping tests. Check every hunk against those three rules.

### 6. Models
- [OBSERVED] `model` field: TODO (every row should be `gemini-3.5-flash-lite`).
- [OBSERVED] Highest `thoughts_token_count`: calls #TODO, #TODO. At those points the agent was TODO (typically: planning right after reading TASK.md, diagnosing the first failing test run, deciding how to structure the shipping rule).
- **Why split router and worker?** [INFERRED] Most requests are easy to classify ("simple question" vs "multi-step coding task"), and a small, fast, cheap model does that well; the expensive model is reserved for the actual reasoning and coding. That cuts cost and latency per turn without hurting quality where it matters — and, on the free tier, it keeps the big model's small per-day request quota for real work.
- **If the whole session ran on a bigger model:** [INFERRED] slower and more expensive per call (and on the free tier it would hit the 20-requests/day limit mid-session), but likely fewer total calls — better diagnosis on the first try, fewer failed edits or test runs, and closer adherence to TASK.md's test-editing rules.
