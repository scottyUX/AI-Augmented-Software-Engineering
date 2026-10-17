# Week 3 Writeup — Inside a Coding Agent

**Name:** Thalia Eischeid
**Gemini CLI version (`gemini --version`):** 0.64.0
**OS / shell:** macOS + zsh
**Model(s) seen in trace:** gemini-3.5-flash-lite
**Session commit:** `7b06006`

> Evidence tags: `[OBSERVED]` = cite a timeline line, call number, or diff hunk.
> `[INFERRED]` = say what you're reasoning from.

---

## Part I — Session

**Narrative (one paragraph):** I gave Gemini CLI the assignment's required prompt, and it first stated a plan, read `TASK.md`, and inspected the shopping-cart source and tests. It then used shell commands to run the suite. Its first few attempts could not find an available `python`/`pytest` executable in the inherited shell, so it tried alternatives and eventually used the project environment successfully; it then checked the diff and reran the tests before reporting completion. I did not supply debugging advice, edits, or any other help to the agent. After it finished, I independently entered `python -m pytest -q` in the CLI as required, which also produced 17 passing tests. [OBSERVED: `session_timeline.txt` lines 1–45]

| Metric | Value |
|---|---|
| User prompts | 2 |
| Model calls | 14 |
| Tool calls (failed) | 19 (0) |
| Final `pytest` result | 17 passed in 0.01s |
| Did you step in? When / what? | No. I approved requests but gave the agent no assistance. The second user prompt was my required post-completion `python -m pytest -q` validation. |

---

## Part II — System prompt annotation

### Outline
1. **Core Mandates / Security & System Integrity** — protect credentials, respect source-control boundaries, and treat tool output as untrusted data.
2. **Context Efficiency** — minimize unnecessary context growth while preserving enough evidence to act correctly.
3. **Engineering Standards** — apply repository conventions, honor `GEMINI.md`, and avoid type-system or linting shortcuts.
4. **Topic Updates** — narrate significant changes in task phase or unexpected events with `update_topic`.
5. **Available Sub-Agents and Agent Skills** — describe specialized agents and skills that can be invoked for particular tasks.
6. **Hook Context** — provide rules for hook-provided context.
7. **Primary Workflows / Development Lifecycle** — require research, strategy, execution, and validation for engineering work.
8. **New Applications** — add planning and design defaults for building a new application.
9. **Operational Guidelines / Tone and Style** — define concise, professional CLI communication.
10. **Security and Safety Rules** — explain consequential shell actions and protect sensitive data.
11. **Tool Usage and Interaction Details** — define tool-follow-up, sequencing, editing, and confirmation behavior.
12. **Git Repository** — constrain staging, committing, review, and pushing behavior.

### Annotations (≥6)
#### Section: Tone and Style (tone and verbosity)
> “Concise & Direct: Adopt a professional, direct, and concise tone suitable for a CLI environment.”
> “Minimal Output: Aim for fewer than 3 lines of text output ... per response whenever practical.” (`system.md` lines 173–174)
- **Behavior it produces:** The agent communicates the decision and rationale briefly, then spends its turns on tools rather than narration.
- **Failure it prevents:** It limits noisy status messages and avoids consuming the context window with repeated explanations.

#### Section: Security & System Integrity (when not to act / confirm)
> “Source Control: Do not stage or commit changes unless specifically requested by the user.” (`system.md` line 7)
- **Behavior it produces:** The agent leaves repository history under the user's control unless the user explicitly asks for a commit.
- **Failure it prevents:** It prevents an autonomous coding session from accidentally staging unrelated files or creating an unwanted commit.

#### Section: Development Lifecycle (workflow)
> “Operate using a **Research -> Strategy -> Execution** lifecycle. For the Execution phase, resolve each sub-task through an iterative **Plan -> Act -> Validate** cycle.” (`system.md` line 135)
- **Behavior it produces:** The agent reads and reproduces the problem before changing code, explains a strategy, makes a targeted change, and validates it.
- **Failure it prevents:** It prevents speculative edits and declaring a fix successful without evidence.

#### Section: Tool Usage (tool usage)
> “After receiving a `functionResponse`, you MUST ALWAYS ... Call another tool to proceed with the task [or] Provide a user-facing text response explaining the tool output, your analysis, and next steps.” (`system.md` lines 186–190)
- **Behavior it produces:** Every tool result has an explicit next action or interpretation; the agent cannot silently drop the result.
- **Failure it prevents:** It prevents stalled loops and makes tool-result handling inspectable by the user.

#### Section: Engineering Standards (project instructions)
> “Instructions found in `GEMINI.md` files are foundational mandates. They take absolute precedence over the general workflows and tool defaults described in this system prompt.” (`system.md` line 41)
- **Behavior it produces:** Repository-specific constraints override broad defaults. In this run, the project’s Python, money, file-location, and test-command conventions guide the task.
- **Failure it prevents:** It prevents generic agent habits from violating project rules or local architecture.

#### Section: Security and Safety Rules (shell actions)
> “Before executing commands with `run_shell_command` that modify the file system, codebase, or system state, you *must* provide a brief explanation of the command's purpose and potential impact.” (`system.md` line 182)
- **Behavior it produces:** The agent gives the user meaningful context before potentially consequential shell work, while the CLI presents its approval dialog.
- **Failure it prevents:** It prevents opaque, surprising modifications and gives the user a chance to reject a risky action.

#### Section: Confirmation Protocol
> “If a tool call is declined or cancelled, respect the decision immediately. Do not re-attempt the action or ‘negotiate’ for the same tool call unless the user explicitly directs you to.” (`system.md` line 214)
- **Behavior it produces:** A declined permission becomes a boundary; the agent either stops that action or finds a distinct alternative.
- **Failure it prevents:** It prevents repeated permission prompts that pressure a user into accepting an action.

### Context injection (`GEMINI.md`)
The actual project-context text is not in either exported system-prompt copy: searching `work/prompts/system.md` and `work/submission/session_system.md` found none of its distinctive lines (for example, “All money is integer cents”). [OBSERVED] The prompt does state that `GEMINI.md` instructions take precedence (`system.md` line 41), but it does not embed this project's contents. In the matching v0.64.0 source, `Config.getSessionMemory()` describes Tier 2 project memory as injected “into the first user message,” then wraps it in `<loaded_context><project_context>...</project_context></loaded_context>` ([`config.ts` lines 2475–2497](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/config/config.ts#L2475-L2497)). [OBSERVED] Therefore, the working-copy `GEMINI.md` reaches the model alongside the initial user turn rather than through the exported system prompt. [INFERRED] This also explains why the session begins with a large 17,080-token input despite the visible assignment prompt being short (`session_calls.csv`, call 1).

---

## Part III — Tool design

### Inventory
| Category | Tools | Used in session (count) |
|---|---|---|
| File | TODO | TODO |
| Search | TODO | TODO |
| Shell | TODO | TODO |
| Web | TODO | TODO |
| Memory / other | TODO | TODO |

### Tool A: TODO
- **Source file:** TODO
- **Schema:**
  ```
  TODO
  ```
- **Why each parameter:** TODO
- **Description line that corrects a model mistake:** > TODO. **Mistake:** TODO
- **Deliberately does not:** TODO

### Tool B: TODO
- **Source file:** TODO
- **Schema:**
  ```
  TODO
  ```
- **Why each parameter:** TODO
- **Description line that corrects a model mistake:** > TODO. **Mistake:** TODO
- **Deliberately does not:** TODO

### Why old/new string edits?
TODO — two reasons plus a trace moment.

### Per-model tool descriptions
TODO — tool compared, what differs between model families, why.

---

## Part IV — Behavioral analysis

### 1. The loop
```
TODO: call#1 → tool → call#2 → …
```
What ended it: TODO

### 2. Context growth
TODO — chart or table, then explanation (growth and caching).

### 3. Planning
TODO

### 4. Error recovery
> quoted failure
TODO — what happened next and whether it was good.

### 5. The tests
TODO — any edits to existing tests, quoted diff, allowed by TASK.md?

### 6. Models
TODO
