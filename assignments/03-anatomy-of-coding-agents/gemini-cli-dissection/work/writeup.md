# Week 3 Writeup — Inside a Coding Agent

**Name:** Riza Arslan
**Gemini CLI version (`gemini --version`):** 0.64.0
**OS / shell:** Windows 11 + Git Bash (VS Code integrated terminal)
**Model(s) seen in trace:** `gemini-3.5-flash-lite` (all 15 calls)
**Session commit:** `fc22dd0` ("Week 3: Gemini CLI session (agent's changes)")

> Evidence tags: `[OBSERVED]` = cite a timeline line, call number, or diff hunk.
> `[INFERRED]` = say what I'm reasoning from.
> "timeline HH:MM:SS" = a line in `submission/session_timeline.txt` (UTC);
> "call #N" = row N of `submission/session_calls.csv`; "system.md LN" = line N of
> `prompts/system.md`. Source links point at the `v0.64.0` tag of google-gemini/gemini-cli.

---

## Part I — Session

**Narrative:** I started `gemini -m gemini-3.5-flash-lite` in `work/run/`, ran `/tools`,
and sent the required prompt once. The agent opened with an `update_topic` call and read
`TASK.md` (call #2), then read `cart.py`, `pricing.py`, `test_cart.py` and `test_pricing.py`
in parallel (call #3), published a second topic update analysing the failures (call #4),
and ran `pytest` to see the failing tests (call #5). After the longest "thinking" step of
the session (call #6, 1,568 thought tokens) it read `catalog.py` to get the prices, then
announced the "Implementing Shipping & Fixes" phase (call #7). In one turn (call #8) it
made two edits: the quantity bug in `Cart.add_item` (`=` → accumulate) and, in
`pricing.py`, the discount-before-tax bug plus a new `calculate_shipping()` used by
`final_total()`. It then updated three expected totals and added three shipping tests in
`test_cart.py` (call #9) and four `calculate_shipping` unit tests in `test_pricing.py`
(call #10), ran `python -m pytest -v` (call #12) and `git status` (call #13). The next
request hit a free-tier **429 quota error** (timeline 05:58:26); the CLI waited ~34 s and
retried automatically, and the agent finished with a "Task Completed" topic recap
(call #14) and a text-only summary (call #15). When I ran the tests myself afterwards, all
21 passed. Note: on Windows, `run_shell_command` runs commands through
`powershell.exe -NoProfile -Command` even though I launched Gemini from Git Bash
([`dynamic-declaration-helpers.ts` L58–62](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/dynamic-declaration-helpers.ts#L58-L62));
the agent's three commands (`pytest`, `pytest -v`, `git status`) work in both shells, so
this never caused a failure.

| Metric | Value |
|---|---|
| User prompts | 1 [OBSERVED: timeline summary `user prompts: 1`] |
| Model calls | 15 (+1 failed request: 429 quota error) [OBSERVED: `model calls: 15 (errors: 1)`] |
| Tool calls (failed) | 18 (0) — `read_file` 6, `update_topic` 5, `replace` 4, `run_shell_command` 3 |
| Final `pytest` result | `21 passed in 0.02s` (my own run after the session; baseline before it was `2 failed, 12 passed`) |
| Did you step in? When / what? | No. I only approved tool calls ("Allow once") and typed nothing else. |

---

## Part II — System prompt annotation

Source: my exported `work/prompts/system.md` (281 lines). It is assembled by
[`prompts/snippets.ts` `getCoreSystemPrompt` L136–167](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/prompts/snippets.ts#L136-L167).
`submission/session_system.md` (captured from the trace) has the same text.

### Outline
1. **Preamble (L1)** — "You are Gemini CLI, an interactive CLI agent…", currently in **Default** approval mode.
2. **Core Mandates → Security & System Integrity (L5)** — protect secrets, don't commit unless asked, treat tool/MCP output as untrusted data.
3. **Core Mandates → Context Efficiency (L10)** — the whole history is re-sent every turn, so minimise turns and oversized reads.
4. **Core Mandates → Engineering Standards (L40)** — `GEMINI.md` takes precedence, follow conventions, reproduce bugs, Directives vs Inquiries, always update tests, don't revert.
5. **Topic Updates (L52)** — narrate progress in phases with `update_topic` (first turn, last turn, every detour).
6. **Available Sub-Agents (L69)** — what can be delegated with `invoke_agent`.
7. **Available Agent Skills (L108)** — 8 skills with file locations (built-in + my `chrome-devtools-mcp` and `context7` extensions).
8. **Hook Context (L168)** — how to treat output from user-configured hooks.
9. **Primary Workflows → Development Lifecycle (L177)** — Research → Strategy → Execution; Plan → Act → Validate per sub-task; re-think after 3 failed fixes.
10. **Primary Workflows → New Applications (L194)** — how to scaffold a new app (not used here).
11. **Operational Guidelines → Tone and Style (L212)** — senior-peer voice, <3 lines of text, no chitchat.
12. **Operational Guidelines → Security and Safety Rules (L224)** — explain state-changing commands; rely on the approval dialog.
13. **Operational Guidelines → Tool Usage (L228)** — never return empty turns, summarise after edits, parallelism, no parallel edits to one file, respect declined calls.
14. **Operational Guidelines → Interaction Details (L259)** — `/help`, `/bug`.
15. **Git Repository (L263)** — never commit or push unless asked; how to prepare a commit if asked.

There is **no "Contextual Instructions" section**: the project `GEMINI.md` is not in the system prompt (see below).

### Annotations (≥6)

#### Section: Tone and Style (tone and verbosity) — system.md L217–218
> - **Minimal Output:** Aim for fewer than 3 lines of text output (excluding tool use/code generation) per response whenever practical.
> - **No Chitchat:** Avoid conversational filler, preambles ("Okay, I will now..."), or postambles

- **Behavior it produces:** terse turns. [OBSERVED] output tokens per call were tiny — 23 to 94 for every pure tool-calling turn (calls #2–#7, #11–#14); only the edit turns (#8–#10) and the final summary (#15, 355 tokens) were longer.
- **Failure it prevents:** chatty LLM defaults that waste output tokens on every turn and bury the useful information in a terminal.

#### Section: Security and Safety Rules + Engineering Standards (when not to act / confirm) — system.md L225, L47
> - **Explain Critical Commands:** Before executing commands with `run_shell_command` that modify the file system, codebase, or system state, you *must* provide a brief explanation of the command's purpose and potential impact. … You should not ask permission to use the tool; the user will be presented with a confirmation dialogue upon use

> For Inquiries, or whenever the user explicitly instructs you NOT to make changes just yet … you MUST NOT modify files until a subsequent Directive is issued.

- **Behavior it produces:** the agent states *why* before a command and relies on the CLI's approval dialog instead of asking in chat; it only edits files for explicit instructions. [OBSERVED] every shell call carries a `description` ("Running pytest to observe current test failures…", timeline 05:56:18) and every tool call shows `decision=accept`, i.e. it went through my approval.
- **Failure it prevents:** blind approval of commands the user doesn't understand, double confirmation loops, and the agent changing code when the user only asked a question.

#### Section: Development Lifecycle (workflow) — system.md L178, L187
> Operate using a **Research -> Strategy -> Execution** lifecycle. For the Execution phase, resolve each sub-task through an iterative **Plan -> Act -> Validate** cycle.

> **Validation is the only path to finality.** Never assume success or settle for unverified changes.

- **Behavior it produces:** [OBSERVED] research first (reads in calls #2–#3, `pytest` at #5, `catalog.py` at #6), then edits (#8–#10), then validation (`pytest -v` at #12) before finishing.
- **Failure it prevents:** "edit and hope" — plausible but broken changes, and premature "done" messages without a passing test run.

#### Section: Tool Usage (tool usage) — system.md L240, L233
> - **File Editing Collisions:** Do NOT make multiple calls to the `replace` tool for the SAME file in a single turn.

> 2. You MUST NEVER return an empty response with no text and no tool calls.

- **Behavior it produces:** parallel calls only for independent work. [OBSERVED] call #8 issued two `replace` calls in one turn, but on **different** files (`cart.py` and `pricing.py`, timeline 05:57:50–51), which the rule allows; the two test files were edited in separate turns (#9, #10).
- **Failure it prevents:** two edits computed against the same original text, where the second `old_string` no longer exists or overwrites the first; and silent empty turns that stall the loop.

#### Section: Context Efficiency — system.md L16
> - The agent passes the full history with each subsequent message. The larger context is early in the session, the more expensive each subsequent turn is.

- **Behavior it produces:** [OBSERVED] the four source/test files were read in **one** parallel turn (call #3) instead of four turns.
- **Failure it prevents:** context bloat and extra turns. [OBSERVED] this matters on the free tier: five calls in ~35 s (#9–#13, 255,925 input tokens) crossed the 250,000 input-tokens-per-minute limit and triggered the 429 at 05:58:26 (see Part IV.2).

#### Section: Engineering Standards → Contextual Precedence / Testing — system.md L41, L49
> - **Contextual Precedence:** Instructions found in `GEMINI.md` files are foundational mandates. They take absolute precedence over the general workflows and tool defaults described in this system prompt.

> - **Testing:** ALWAYS search for and update related tests after making a code change.

- **Behavior it produces:** project rules override defaults, and features come with tests. [OBSERVED] the agent kept money in integer cents (`SHIPPING_FEE = 599`, `FREE_SHIPPING_THRESHOLD = 5000`) and put the rule in `pricing.py`, exactly as `GEMINI.md` asks, and it added 7 new tests (session diff).
- **Failure it prevents:** generic habits that break this repo (floats for money, shipping logic in `cart.py`) and untested features.

#### Section: Git Repository — system.md L266
> - **NEVER** stage or commit your changes, unless you are explicitly instructed to commit.

- **Behavior it produces:** [OBSERVED] the agent ran `git status` (call #13, timeline 05:58:26) but never `git add`/`git commit`; I committed its changes myself as `fc22dd0`.
- **Failure it prevents:** unreviewed commits (possibly with secrets or half-finished work) entering history without the human seeing them.

### Context injection (`GEMINI.md`)
**`GEMINI.md`'s content is NOT in the exported `system.md`.** [OBSERVED] searching
`prompts/system.md` and `submission/session_system.md` for "integer" or "cents" finds no
match, and neither file has a "Contextual Instructions" section. But the CLI did load it:
the status bar read **"1 GEMINI.md file · 3 MCP servers · 8 skills"** [OBSERVED].

Where it enters: v0.64.0 uses a *tiered* context model.
- `config.getSystemInstructionMemory()` returns only **Tier 1** (global `~/.gemini/GEMINI.md` + user-project memory) for the system prompt — [`config/config.ts` L2591–2611](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/config/config.ts#L2591-L2611). Its comment says extension and project memory "are placed in the first user message instead". I have no global `GEMINI.md`, so the system prompt gets none.
- The project file is **Tier 2**: `getEnvironmentContext()` calls `config.getSessionMemory()` and puts it in the **first user message**, inside a `<session_context>` block with the date, OS and folder structure — [`utils/environmentContext.ts` L62–77](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/utils/environmentContext.ts#L62-L77); `getInitialChatHistory()` places it at the start of the history ([`core/client.ts` L422](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/core/client.ts#L422)).
- [OBSERVED] `submission/session_context.md` shows that block arriving as a **user** turn (`User: <session_context> This is the Gemini CLI. We are setting up the context for our chat. … My operating system is: win32`), not as system instructions.
- [OBSERVED] call #2 — the first call after my prompt — already had 39,881 input tokens while the system prompt is ~36 KB of text: the system prompt, 16 tool schemas and the `<session_context>` user message are all sent before the agent has read a single file.
- [OBSERVED] The workspace list in `<session_context>` includes `…\Desktop\week3-gemini` as well as `work\run`. [INFERRED] Gemini CLI's VS Code integration adds the editor's open folder as an extra workspace directory, which is why it earlier asked me to trust that folder.

---

## Part III — Tool design

### Inventory
`/tools` in my session listed **16 built-in tools** [OBSERVED: `/tools` output]:
Activate Skill (`activate_skill`), Ask User (`ask_user`), Edit (`replace`), Enter Plan Mode
(`enter_plan_mode`), FindFiles (`glob`), GoogleSearch (`google_web_search`), Invoke Subagent
(`invoke_agent`), List Background Processes (`list_background_processes`), Read Background
Output (`read_background_output`), ReadFile (`read_file`), ReadFolder (`list_directory`),
SearchText (`grep_search`), Shell (`run_shell_command`), Update Topic Context
(`update_topic`), WebFetch (`web_fetch`), WriteFile (`write_file`).
The status bar also showed 3 MCP servers and 8 skills from extensions on my machine
(`chrome-devtools-mcp`, `context7`).

| Category | Tools | Used in session (count) |
|---|---|---|
| File | `read_file`, `write_file`, `replace`, `list_directory` | `read_file` 6, `replace` 4 |
| Search | `glob`, `grep_search` | 0 |
| Shell | `run_shell_command`, `list_background_processes`, `read_background_output` | `run_shell_command` 3 |
| Web | `google_web_search`, `web_fetch` | 0 |
| Planning and narration | `update_topic`, `enter_plan_mode` | `update_topic` 5 |
| Delegation | `invoke_agent` (sub-agents), `activate_skill` (skills) | 0 |
| Other | `ask_user` | 0 |

[OBSERVED: timeline summary] 18 tool calls, 0 failed. [INFERRED] The search tools were never
needed: the repo has only four small source files, so the agent read them whole (system.md
L35: "It's most efficient to read small files in their entirety").
[INFERRED] The v0.64.0 source also defines `write_todos`, `read_many_files`,
`exit_plan_mode`, `complete_task`, `get_internal_docs` and `tracker_*` tools, but they were
not registered in my session; they are enabled only by specific settings or modes
(e.g. `exit_plan_mode` only exists inside plan mode).

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
  - `instruction` — not needed for the happy path. It exists for **self-correction**: when the match fails, `attemptSelfCorrection` sends `instruction`, `old_string`, `new_string`, the error and the current file to a *separate* LLM call, `FixLLMEditWithInstruction` (edit.ts L547–600), which repairs the edit. The instruction tells that second model what the edit was *for*. [OBSERVED] the agent filled it in, e.g. "Add unit tests for calculate_shipping in test_pric…" (timeline 05:58:06).
  - `allow_multiple` — explicit opt-in for replace-all; without it, 2+ matches is an error ("expected 1 occurrence but found N"), so the agent can't accidentally edit the wrong copy.
- **Description line that corrects a model mistake:**
  > Do not use omission placeholders like '(rest of methods ...)', '...', or 'unchanged code'; provide exact literal code.

  **Mistake:** "lazy" elision — models abbreviate unchanged code with `...`, which would literally write `...` into the file and delete the real code. It is also *enforced*: `validateToolParamValues` rejects a `new_string` containing a new placeholder via `detectOmissionPlaceholders` (edit.ts L1225–1236).
- **Deliberately does not:** guess which match you meant. If `old_string` appears more than once and `allow_multiple` is false, it refuses instead of picking the first one (edit.ts L372–376). Why: silently editing the wrong occurrence produces a bug that looks like success. It also doesn't take line numbers (see the design question).

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
  - `command` — the command itself; its description names the exact interpreter, so the model writes the right syntax for the OS (on my Windows machine: PowerShell).
  - `description` — shown to the human in the approval dialog; it is the "Explain Critical Commands" rule turned into a field. [OBSERVED] all three shell calls set it (e.g. "Checking git status to …", timeline 05:58:26).
  - `dir_path` — run in a sub-folder without `cd … &&` chains; checked by `validatePathAccess` (shell.ts L1220–1233).
  - `is_background` + `delay_ms` — start a server without blocking the loop forever while still catching an immediate crash; `list_background_processes` / `read_background_output` then let the agent check on it.
  - `additional_permissions` — request more sandbox access after an "Operation not permitted" failure (not offered in my session: "no sandbox").
- **Description line that corrects a model mistake:**
  > To run a command in the background, set the `is_background` parameter to true. Do NOT use PowerShell background constructs.

  (Mac/Linux wording: "Do NOT use `&` to background commands.") **Mistake:** models trained on shell scripts background processes themselves (`&`, `Start-Job`); the CLI can't track them, so output is lost, the process is orphaned, or the call hangs.
- **Deliberately does not:** run commands containing command substitution (`$()`, backticks, `<()`, `>()`; on PowerShell also `@()`). `execute()` blocks them with "Command injection detected … the command was blocked" (shell.ts L529–539). Why: approvals and "allow for this session" rules are keyed on the command's root (e.g. `python`, via `getCommandRoots`); substitution could hide a second command inside an approved one. It also doesn't run forever — an inactivity timeout cancels stuck commands (shell.ts L554–661, L876–882).

### Why old/new string edits?
1. **Robust to drift.** Line numbers go stale as soon as an earlier edit adds or removes a line, and models are unreliable at counting lines. Exact text is self-locating and self-verifying: if the file changed, the match fails loudly instead of editing the wrong line.
2. **Cheap and safe compared with rewriting the file.** The model outputs only the changed region (fewer output tokens), it can't drop unrelated code with `...`, and the human reviews a small diff in the approval dialog (the description itself says it "minimizes token usage, simplifies code reviews, and avoids accidental deletions").

**Trace moment:** [OBSERVED] it mattered in call #8, where `pricing.py` and `cart.py` were
edited in the same turn (timeline 05:57:50–51). The `pricing.py` edit (its `new_string`
begins `SHIPPING_FEE = 599 …`) inserted 13 new lines (`SHIPPING_FEE`,
`FREE_SHIPPING_THRESHOLD`, `calculate_shipping`) above `final_total` and rewrote
`final_total`'s body (session diff), shifting every line below it. With line-number
edits, any later edit to that file computed against the earlier read would have hit the
wrong lines; anchoring on text avoids that. [OBSERVED] all 4 `replace` calls succeeded on
the first try (0 failed tool calls), so the self-correction path never ran. [INFERRED] that
is because the agent had read every file in full just before editing (call #3), so each
`old_string` matched exactly once.

### Per-model tool descriptions
Tool compared: `replace` —
[`gemini-3.ts` L356](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/model-family-sets/gemini-3.ts#L356) vs
[`default-legacy.ts` L349](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/model-family-sets/default-legacy.ts#L349).

| | `default-legacy.ts` (older models) | `gemini-3.ts` (Gemini 3.x, what my session used) |
|---|---|---|
| Length | Long: a numbered "Expectation for required parameters" list (5 rules) + **Important**/**CRITICAL** warnings | 2 short paragraphs |
| Context rule | "Include at least 3 lines of context BEFORE and AFTER the target text" (in both the description and `old_string`) | Only "requires providing significant context" |
| Read first | "Always use the read_file tool to examine the file's current content before attempting a text replacement." | Removed |
| Escaping | "NEVER escape `old_string` or `new_string`"; params say "*preferably* unescaped" | Params say "unescaped" |
| `instruction` param | Long guide: WHY / WHERE / WHAT / outcome + GOOD and BAD examples | One sentence |
| Rationale | — | Adds why to prefer it: "minimizes token usage, simplifies code reviews, and avoids accidental deletions" |

**Why describe the same tool differently?** Tool schemas are sent with *every* request, so
every word costs input tokens on every call — [OBSERVED] in my session the fixed overhead
before any file was read was already ~40k tokens (call #2). Older models made specific
mistakes (too little context → ambiguous matches, escaped strings, vague instructions for
the fixer), so their description spells out each rule with examples. Newer models follow a
short spec reliably, so the extra rules become pure overhead and the description shrinks to
a concise contract. The tool description is a prompt tuned to the model, just like the
system prompt (the CLI also keeps separate `snippets.ts` and `snippets.legacy.ts`).
Contrast: `run_shell_command` is **identical** in both files — both call the same
`getShellDeclaration()` — because its description depends on the **OS** (bash vs
PowerShell), not on the model.

---

## Part IV — Behavioral analysis

### 1. The loop
```
(call #1: startup utility call, before my prompt)
user prompt
→ call#2  → update_topic + read_file(TASK.md)
→ call#3  → read_file ×4 in parallel (cart.py, pricing.py, test_cart.py, test_pricing.py)
→ call#4  → update_topic ("Analyzing test failures in final_total …")
→ call#5  → run_shell_command(pytest)            [2 tests fail]
→ call#6  → read_file(catalog.py)                 [most thinking: 1,568 tokens]
→ call#7  → update_topic ("Implementing fixes for cart item quantity acc…")
→ call#8  → replace(cart.py) + replace(pricing.py)
→ call#9  → replace(test_cart.py)
→ call#10 → replace(test_pricing.py)
→ call#11 → update_topic ("Running pytest to validate …")
→ call#12 → run_shell_command(python -m pytest -v)   [21 passed]
→ call#13 → run_shell_command(git status)
→ [429 quota error, CLI waits ~34 s and retries]
→ call#14 → update_topic ("Task Completed")
→ call#15 → final text summary, no tool call → end
```
[OBSERVED: timeline 05:54:37–05:59:05] One user message produced 14 model calls and 18 tool
calls. [OBSERVED] call #1 (05:52:40, 409 input tokens) happened *before* my prompt;
`submission/session_context.md` shows a request of that shape ("Summarize the user's primary
intent … in ONE sentence (max 80 characters)"). [INFERRED] it is a background utility call
that titles a session, not part of the agent loop.

**What ended it:** [OBSERVED] the agent decided it was done — call #15 returned only text
(355 output tokens, no tool call), right after the "Task Completed" topic update (call #14).
No limit was reached, and I didn't intervene.

### 2. Context growth
![Context growth](submission/context_growth.png)

| call | input | cached | cached % | thoughts | output | what came before it |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 409 | 0 | 0% | 398 | 5 | startup utility call |
| 2 | 39,881 | 0 | 0% | 180 | 67 | my prompt (+ system prompt, tools, `<session_context>`) |
| 3 | 40,431 | 36,582 | 90% | 482 | 94 | TASK.md |
| 4 | 42,410 | 38,598 | 91% | 14 | 63 | 4 files read |
| 5 | 42,555 | 38,590 | 91% | 83 | 38 | topic update |
| 6 | 43,197 | 40,616 | 94% | 1,568 | 23 | pytest output |
| 7 | 44,986 | 42,652 | 95% | 812 | 75 | catalog.py |
| 8 | 45,953 | 42,650 | 93% | 1,175 | 576 | topic update |
| 9 | 48,697 | 0 | 0% | 294 | 794 | 2 edits (cart, pricing) |
| 10 | 50,685 | 46,723 | 92% | 270 | 506 | test_cart edit |
| 11 | 51,817 | 48,754 | 94% | 26 | 52 | test_pricing edit |
| 12 | 51,952 | 48,745 | 94% | 20 | 39 | topic update |
| 13 | 52,774 | 48,742 | 92% | 88 | 34 | pytest -v output |
| 14 | 53,064 | 50,766 | 96% | 15 | 71 | git status |
| 15 | 53,226 | 50,758 | 95% | 19 | 355 | topic update |

**Why it grows:** [OBSERVED] `input_token_count` rose from 39,881 (call #2) to 53,226
(call #15), +34%, and never fell. [INFERRED from the system prompt's L16 and the numbers] the
model is stateless, so every call re-sends the system prompt, the 16 tool schemas,
`<session_context>` and the **entire** history: each file read, each test output, each edit
and each of the model's own replies is appended and then paid for again on every later call.
The biggest jumps follow the big payloads: +1,979 after the four file reads (#3→#4), +1,789
after `catalog.py` (#6→#7), +2,744 after the two edits and their 576-token tool call
(#8→#9), +1,988 after the test edit (#9→#10). Small steps (+135, +145, +162) follow
`update_topic` calls. Over the session the model received **662,037** input tokens to make
changes to four small files.

**What `cached_content_token_count` tells me:** [OBSERVED] from call #3 on, 90–96% of each
request was served from the provider's context cache — 534,176 of 662,037 input tokens
(80.7%) overall. The cached part is the unchanged **prefix** (system prompt, tools, earlier
history); only the newest turns are new. Cached tokens are billed at a discount and skip
re-processing, so a long agent session is much cheaper and faster than the raw input count
suggests. That is also why agents append to history instead of rewriting it, which would
break the prefix. [OBSERVED] two calls had **no** cache hit: #2 (the first full request,
nothing cached yet) and #9. [INFERRED] #9 came after a ~80 s pause while I reviewed and
approved two edits (05:56:32 → 05:57:51); the provider's implicit cache is best-effort and
short-lived, so the prefix had to be re-processed in full.

**Cost in practice:** [OBSERVED] the 429 error at 05:58:26 says I exceeded the free tier's
"input tokens per minute" limit (250,000) for `gemini-3.5-flash-lite`. Calls #9–#13 ran
within ~35 s and together sent **255,925** input tokens. [INFERRED] that quota counts every
input token, including cached ones, so context growth hits rate limits even when caching
keeps the bill low.

### 3. Planning
[OBSERVED] The agent planned and tracked progress with **`update_topic`** (5 calls), not
`write_todos` (not available in my session) and not plan mode. It followed the system
prompt's "Topic Updates" section (system.md L52–63) closely:
- "Always call update_topic in your first turn" (L56) → call #2 started with `update_topic` ("Reading TASK.md and analyzing the requirement…").
- New phases got new topics: failure analysis (#4), "Implementing Shipping & Fixes" (#7), validation (#11). My prompt asked it to "First write out your plan"; it did that inside the call #7 topic summary ("Implementing fixes for cart item quantity accumulation and pricing final_total discount-before-tax order, adding shipping calculation rule in pricing.py, updating Cart.total(), updating existing test assertions for shipping, and adding new tests for shipping rules"), not as a separate text message.
- "call update_topic in your last turn to recap" (L57) → "Task Completed" (#14).
- 5 topic updates for ~14 turns matches "a topic is typically … every 3 to 10 turns" and "3 or more times".

**Where it departed from the plan:**
- [OBSERVED] The plan says "updating Cart.total()", and the final summary claims "Updated Cart.total() to include shipping", but the session diff touches only `add_item` in `cart.py`; `Cart.total()` still just calls `final_total(...)`. Shipping was wired into `pricing.final_total()` instead. [INFERRED] the behaviour is correct (`Cart.total()` gets shipping through `final_total`), but the summary over-claims what it changed, so a reviewer must check the diff rather than trust the summary.
- [OBSERVED] `git status` (call #13) was not in the plan; it only inspected, which is consistent with the Git Repository rule (L266).
- [INFERRED] It skipped one system-prompt step: "For bug fixes, you must empirically reproduce the failure with a new test case" (L46). It relied on the existing failing tests instead of writing its own reproduction, which was reasonable here because the provided tests already reproduce both bugs.

### 4. Error recovery
**First failure — the failing test run (call #5).** Before the agent's changes, the suite
fails (my baseline run of the same command):
> `FAILED tests/test_cart.py::test_fixed_discount_applied_before_tax - assert 1160 == 3240`
> `2 failed, 12 passed`

[OBSERVED] The tool call itself is logged as `[ok]` (timeline 05:56:18): a shell tool
"succeeds" whenever the command runs, even if the tests fail, so the model has to read the
output to notice the failure. What it did next: [OBSERVED] call #6 had the most thinking of
the session (1,568 thought tokens), then it read `catalog.py` to get the real prices,
published the implementation topic (#7), and fixed **both** bugs in one turn (#8): quantity
accumulation in `add_item`, and swapping the order in `final_total` to discount first, then
tax (the comment already said "Discount is applied before tax, per store policy"). It then
re-ran the full suite (#12). **Good recovery:** [INFERRED] diagnosis was targeted (it went to
the exact functions the two failures pointed at, with no trial-and-error edits), it needed
one fix attempt, and it verified with a full test run before finishing.

**Second failure — the 429 quota error (05:58:26).** [OBSERVED] "You exceeded your current
quota … Quota exceeded for metric … input_token_count, limit: 250000 … Please retry in
32.7s". The next request went out at 05:59:00, ~34 s later, and succeeded (call #14).
[INFERRED] this recovery was done by the **CLI**, not the model: it honoured the
`retryDelay` and re-sent the same request, and the model never saw the error. That's good
infrastructure design — transient API errors shouldn't cost a model turn.

### 5. The tests
[OBSERVED: `git show fc22dd0 -- work/run/tests/`] The agent edited three existing
assertions in `test_cart.py` and only added new tests elsewhere:
```diff
 def test_total_includes_tax():
-    assert cart.total() == 2160  # 2000 + 8% tax
+    assert cart.total() == 2759  # 2000 + 8% tax + 599 cents shipping
 def test_percent_discount():
-    assert cart.total() == 2333  # (2400 - 10%) + 8% tax
+    assert cart.total() == 2932  # (2400 - 10%) + 8% tax + 599 cents shipping
 def test_fixed_discount_applied_before_tax():
-    assert cart.total() == 3240  # (4000 - 1000) + 8% tax
+    assert cart.total() == 3839  # (4000 - 1000) + 8% tax + 599 cents shipping
```
**Allowed by TASK.md?**
- **Step 1 ("do not edit them for this step"): yes.** [OBSERVED] The bugs were fixed in the code, not the tests. `test_fixed_discount_applied_before_tax` was one of the failing tests, and the agent did *not* change 3240 to the buggy 1160; it fixed `final_total` so that 3240 became correct, and every new value equals the old intended value + 599 (2160+599, 2333+599, 3240+599).
- **Step 2 ("update those expected values — and only those — and note why in a comment"): mostly.** Only `Cart.total()` assertions with below-$50 subtotals changed, which are exactly the ones shipping affects. Each new comment shows the shipping term, but none says explicitly *why* the value changed (e.g. "updated: shipping added in TASK step 2"), so the "note why" part is only partly met.
- **Step 3 (add tests): yes.** It added 3 cart-level tests (free at a 6000 subtotal, free after a SAVE10 discount brings it to 5400, shipping not taxed) and 4 unit tests for `calculate_shipping` (0 → 0, 4999 → 599, 5000 → 0, 7500 → 0), covering the exact $50.00 threshold.

[INFERRED] One gap the tests didn't catch: `calculate_shipping` returns 0 whenever the
*discounted* subtotal is 0, so a non-empty cart discounted to $0 (e.g. a $10 item with
TENOFF) also ships free. TASK.md says an *empty cart* pays no shipping, which is not the
same condition.

### 6. Models
- [OBSERVED] The `model` field is `gemini-3.5-flash-lite` for all 15 calls (timeline summary: `models: gemini-3.5-flash-lite x15`). Because I passed `-m`, no router model appears in the trace.
- [OBSERVED] Most thinking (`thoughts_token_count`): **#6 (1,568)** right after the failing `pytest` output, where the agent was diagnosing both failures and deciding what to fix; **#8 (1,175)** where it composed the two code edits, including the design of `calculate_shipping` and the new `final_total`; **#7 (812)** after reading `catalog.py`, planning the implementation phase; **#3 (482)** after reading TASK.md, deciding which files to read. Routine turns (topic updates, re-running tests) used only 14–26 thought tokens (#4, #11, #12, #14, #15). [INFERRED] thinking concentrates on *decisions* (diagnosis and design), not on mechanical steps.
- **Why split router and worker?** [INFERRED] Many requests are easy to classify (a quick question vs. a multi-step coding task), and a small, fast, cheap model does that well. The expensive model is kept for the reasoning and coding. That cuts cost and latency per turn without hurting quality where it matters, and on the free tier it saves the big model's tiny 20-requests-per-day quota for real work.
- **If the whole session ran on a bigger model:** [INFERRED] each call would be slower and more expensive. On the free tier it wouldn't even finish: this session made 15 calls, and `gemini-3.8-flash` allows ~20 per day. Quality might improve where this run was weakest — an accurate final summary (it over-claimed a `Cart.total()` change), explicit "why" comments on updated tests, and catching the "empty cart vs $0 subtotal" distinction — and it might need fewer, better-targeted turns.
