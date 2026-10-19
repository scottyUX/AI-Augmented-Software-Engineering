# Week 3 Writeup — Inside a Coding Agent

**Name:** Parwana Babakarkhil
**Gemini CLI version (`gemini --version`):** 0.64.0
**OS / shell:** Windows 11 + PowerShell (Windows Terminal), Python 3.12 venv
**Model(s) seen in trace:** `gemini-3.5-flash-lite` only (14/14 calls)
**Session commit:** `d4d6a8a` ("Week 3: Gemini CLI session (agent's changes)")

> Evidence tags: `[OBSERVED]` = cite a timeline line, call number, or diff hunk.
> `[INFERRED]` = say what you're reasoning from.
>
> Evidence files: `submission/session_timeline.txt` (timeline), `submission/session_calls.csv`
> (one row per model call), `submission/session_system.md` (system instruction captured in the
> trace), `submission/session_context.md` (first message the model received),
> `submission/session_tools.md` (the 16 tool declarations sent to the model), and
> `prompts/system.md` (exported with `GEMINI_WRITE_SYSTEM_MD`). Line numbers for `system.md`
> refer to `prompts/system.md`.

---

## Part I — Session

**Narrative (one paragraph):** I started `gemini -m gemini-3.5-flash-lite` in `work/run/` and
sent the required prompt once. The agent opened a topic ("Reading Task and Planning") and read
`TASK.md` in the same turn, then ran `pytest` to reproduce the failures before touching any code.
It read all five source and test files in one parallel turn (5 × `read_file` at 13:14:11), then
spent the most "thinking" of the session (2,656 thought tokens, call #4) deciding on the fixes.
It made two code edits: one `replace` in `cart.py` (make `add_item` add to the existing quantity)
and one in `pricing.py` (apply the discount before tax, plus the new `shipping_fee` rule). After
re-running the tests it switched topic to "Updating existing test assertions for Cart.total",
updated the three pre-shipping totals in `test_cart.py`, added shipping tests in both test files,
ran the full suite, closed the topic with "Task Completed", and finished with
`git --no-pager status`. It did not stage or commit anything. The whole session took 2 m 58 s of
wall time; my own `python -m pytest -q` afterwards gave **18 passed** (before the session it was
2 failed, 12 passed).

| Metric | Value |
|---|---|
| User prompts | 1 |
| Model calls | 14 (0 errors) |
| Tool calls (failed) | 19 (0) — `read_file` 6, `update_topic` 5, `run_shell_command` 4, `replace` 4 |
| Final `pytest` result | `18 passed in 0.03s` |
| Did you step in? When / what? | No. I only approved tool calls (all 19 accepted, "User Agreement 100% (19 reviewed)" in the exit summary). |

Notes on the run: a first attempt failed before any model call because the `GEMINI_API_KEY`
variable held placeholder text with a non-ASCII character (`Cannot convert argument to a
ByteString ... value of 305`). I fixed the variable, deleted that `telemetry.log`, and started
again, so the trace above contains only the clean session.

---

## Part II — System prompt annotation

### Outline
1. **Identity line** (L1) — "You are Gemini CLI ... operating in **Default** mode."
2. **Core Mandates → Security & System Integrity** (L5–8) — secrets, no unrequested commits, untrusted tool output.
3. **Core Mandates → Context Efficiency** (L10–38) — how to spend tokens and turns.
4. **Core Mandates → Engineering Standards** (L40–51) — `GEMINI.md` precedence, conventions, testing, directives vs inquiries, confirm scope.
5. **Topic Updates** (L52–66) — when and how to call `update_topic`.
6. **Available Sub-Agents** (L69–106) — delegation rules.
7. **Available Agent Skills** (L108–123) — installed skills list (paths redacted).
8. **Hook Context** (L125–130) — how to treat hook output.
9. **Primary Workflows → Development Lifecycle** (L134–149) — Research → Strategy → Execution (Plan → Act → Validate).
10. **Primary Workflows → New Applications** (L151–165) — defaults for building new apps.
11. **Operational Guidelines → Tone and Style** (L169–179) — short, direct CLI output.
12. **Operational Guidelines → Security and Safety Rules** (L181–183) — explain modifying commands.
13. **Operational Guidelines → Tool Usage** (L185–214) — response rules, parallelism, edit collisions, memory files.
14. **Interaction Details** (L216–218) — `/help`, `/bug`.
15. **Git Repository** (L220–237) — never commit unless asked; how to commit when asked.

### Annotations (≥6)

#### Section: Tone and Style (tone and verbosity), L174
> "**Minimal Output:** Aim for fewer than 3 lines of text output (excluding tool use/code generation) per response whenever practical."
- **Behavior it produces:** short replies between tool calls; progress is shown through tool calls and topic titles instead of prose. In my trace most responses have very small output (e.g. 36–62 output tokens for calls #1, #2, #7, #11, #12, #13) `[OBSERVED]` (`session_calls.csv`).
- **Failure it prevents:** a chatty agent that floods a terminal with "Okay, I will now..." text, wastes output tokens, and makes the actual actions hard to follow.

#### Section: Security and Safety Rules + Engineering Standards (when not to act / confirm), L182 and L51
> "Before executing commands with `run_shell_command` that modify the file system ... you *must* provide a brief explanation ... You should not ask permission to use the tool; the user will be presented with a confirmation dialogue upon use"
>
> "If the user implies a change (e.g., reports a bug) without explicitly asking for a fix, **ask for confirmation first**."
- **Behavior it produces:** the model explains risky commands but leaves the yes/no decision to the CLI's own confirmation dialog, and it does not start fixing things the user only mentioned. Every `run_shell_command` in my trace carries a `description` argument (e.g. "Running pytest to observe current test failures") `[OBSERVED]` (timeline 13:14:08, 13:14:47, 13:15:20, 13:15:36). My prompt was an explicit directive ("complete all of it"), so it did not stop to ask `[OBSERVED]` (no `ask_user` call).
- **Failure it prevents:** destructive or surprising actions the user did not request, and double-prompting (the model asking "may I?" and then the CLI asking again).

#### Section: Development Lifecycle (workflow), L135 and L144
> "Operate using a **Research -> Strategy -> Execution** lifecycle. For the Execution phase, resolve each sub-task through an iterative **Plan -> Act -> Validate** cycle."
>
> "**Validation is the only path to finality.** Never assume success or settle for unverified changes."
- **Behavior it produces:** read first, reproduce, then edit, then test. My session follows this order: `read_file TASK.md` → `pytest` (reproduce) → read 5 files → edits → `pytest` → edit tests → full `pytest -v` `[OBSERVED]` (timeline 13:13:43–13:15:20).
- **Failure it prevents:** "blind" edits based on guesses, and declaring success without running the tests.

#### Section: Tool Usage (tool usage), L196–197
> "**File Editing Collisions:** Do NOT make multiple calls to the `replace` tool for the SAME file in a single turn."
- **Behavior it produces:** parallel calls for independent work, but sequential edits for the same file. In my trace the five reads happen in one turn (13:14:11) while each `replace` is in its own turn, one per model response (#5, #6, #9, #10) `[OBSERVED]`.
- **Failure it prevents:** race conditions where a second edit's `old_string` no longer matches because the first edit already changed the file.

#### Section: Context Efficiency, L17
> "Unnecessary turns are generally more expensive than other types of wasted context."
- **Behavior it produces:** batching reads into one turn instead of five, and reading small files whole. The 5 parallel `read_file` calls at 13:14:11 saved four round trips `[OBSERVED]`.
- **Failure it prevents:** context and cost blow-up — every extra turn re-sends the whole history (see Part IV §2: input grows from 11,379 to 25,665 tokens).

#### Section: Topic Updates, L56
> "Always call update_topic in your first turn."
- **Behavior it produces:** named phases the user can follow. The first tool call of the session is `update_topic` ("Reading Task and Planning") and there are 5 topics in total, including a closing "Task Completed" `[OBSERVED]` (timeline 13:13:43, 13:15:22).
- **Failure it prevents:** a long silent run where the user cannot tell what phase the agent is in or why it changed direction.

#### Section: Engineering Standards → Testing, L49
> "**Testing:** ALWAYS search for and update related tests after making a code change. You must add a new test case ..."
- **Behavior it produces:** the agent added 4 new tests (3 in `test_cart.py`, 1 in `test_pricing.py`) even though TASK.md only said "add tests covering the shipping rules" `[OBSERVED]` (session commit diff).
- **Failure it prevents:** features shipped without tests, and silent regressions.

### Context injection (`GEMINI.md`)
`GEMINI.md`'s content is **not** in the exported `system.md`. Neither `prompts/system.md` nor
the system instruction captured in the trace (`submission/session_system.md`) contains its
text: searching both for "integer **cents**" or "Project context" finds nothing `[OBSERVED]`.
The system prompt only refers to the file by name ("Instructions found in `GEMINI.md` files are
foundational mandates", L41).

Instead, it enters as part of the **first user message**. `submission/session_context.md`
(extracted with `summarize_log.py --context`) shows the first message the model got: a
`<session_context>` block with the date, OS (`win32`), workspace directory tree, and then:

```
<loaded_context>
<project_context>
--- Context from: .../work/run/GEMINI.md ---
# Project context
- Python 3.10+ library; no third-party runtime dependencies.
- All money is integer **cents**. ...
```

followed directly by my prompt `[OBSERVED]`.

Source confirmation (Gemini CLI `v0.64.0`):
- `packages/core/src/utils/environmentContext.ts` L62–66: comment "Tier 1 (global): system
  instruction only / Tier 2 (extension + project): first user message (here) / Tier 3
  (subdirectory): tool output (JIT)", then `const environmentMemory = config.getSessionMemory();`
  which is placed inside `<session_context>`.
- `packages/core/src/config/config.ts` L2615–2636: `getSessionMemory()` wraps the project
  memory in `<project_context>` and `<loaded_context>` tags.
- `packages/core/src/prompts/promptProvider.ts` L320–333: `maybeWriteSystemMd()` writes the
  base system prompt to the `GEMINI_WRITE_SYSTEM_MD` path, which is why the export never
  contains project context.

---

## Part III — Tool design

### Inventory
Source: the 16 declarations sent to the model (`submission/session_tools.md`, extracted with
`summarize_log.py --tools`; same list as `/tools`). Counts from the timeline summary.

| Category | Tools | Used in session (count) |
|---|---|---|
| File | `read_file`, `write_file`, `replace`, `list_directory` | `read_file` 6, `replace` 4 |
| Search | `glob`, `grep_search` | 0 |
| Shell | `run_shell_command`, `list_background_processes`, `read_background_output` | `run_shell_command` 4 |
| Web | `google_web_search`, `web_fetch` | 0 |
| Planning and narration | `update_topic`, `enter_plan_mode`, `ask_user` | `update_topic` 5 |
| Delegation | `invoke_agent`, `activate_skill` | 0 |

The agent never searched (`glob`/`grep_search`): the repo is tiny and its directory tree was
already in the first message (`session_context.md`), so it read the files directly
`[INFERRED]` from the context file plus the 0 search calls.

### Tool A: `replace` (file edit)
- **Source file:** name and parameters `packages/core/src/tools/definitions/base-declarations.ts` L64–69; description and schema sent to Gemini 3 models `definitions/model-family-sets/gemini-3.ts` L356; implementation `packages/core/src/tools/edit.ts` (`EditToolInvocation` L460, `validateToolParamValues` L1176).
- **Schema (as sent, `session_tools.md`):**
  ```
  file_path      string   required   "The path to the file to modify."
  instruction    string   required   "A clear, semantic instruction for the code change ..."
  old_string     string   required   "The exact literal text to replace, unescaped. ..."
  new_string     string   required   "The exact literal text to replace `old_string` with ..."
  allow_multiple boolean  optional   "If true, the tool will replace all occurrences ..."
  ```
- **Why each parameter:**
  - `file_path`: which file; validated and resolved inside the workspace (edit.ts L1176+).
  - `instruction`: a plain-language intent. It is shown to the user for review and gives the CLI something to work from if the literal match fails. In my trace the first edit's instruction was "Increment item quantity when adding an item that a[lready exists]" `[OBSERVED]` (13:14:25).
  - `old_string`: an anchor that must match exactly once, so the edit lands in exactly one place.
  - `new_string`: the full replacement text, never a diff or placeholder.
  - `allow_multiple`: an explicit opt-in for mass replacement; default is one match.
- **Description line that corrects a model mistake:** > "Do not use omission placeholders like '(rest of methods ...)', '...', or 'unchanged code'; provide exact literal code." **Mistake:** models often abbreviate unchanged code with "..." when writing edits; written literally, that deletes real code.
- **Deliberately does not:** replace more than one match unless asked. `edit.ts` L372–375 fails with "Expected 1 occurrence but found N ... If you intended to replace multiple occurrences, set 'allow_multiple' to true." It also refuses no-op edits ("old_string and new_string are identical", L377+). Why: an ambiguous anchor would silently edit the wrong place.

### Tool B: `run_shell_command`
- **Source file:** name and parameters `base-declarations.ts` L56–58; description `definitions/dynamic-declaration-helpers.ts` (`getShellToolDescription` L36, `getShellDeclaration` L85); implementation `packages/core/src/tools/shell.ts` (`ShellToolInvocation` L102, `validateToolParamValues` L1220).
- **Schema (as sent, Windows variant):**
  ```
  command        string   required   "Exact command to execute as `powershell.exe -NoProfile -Command <command>`"
  description    string   optional   "Brief description of the command for the user ..."
  dir_path       string   optional   "... Must be a directory within the workspace and must already exist."
  is_background  boolean  optional   "Set to true if this command should be run in the background ..."
  delay_ms       integer  optional   "Delay in milliseconds to wait after starting the process in the background ..."
  ```
- **Why each parameter:**
  - `command`: the exact command. The description names the real interpreter (`powershell.exe -NoProfile`), so the model writes PowerShell on Windows instead of bash.
  - `description`: what the user sees in the confirmation dialog. Every shell call in my trace had one `[OBSERVED]`.
  - `dir_path`: run in a subfolder without `cd` chains; limited to the workspace.
  - `is_background` / `delay_ms`: start servers and watchers without blocking the agent loop, and wait briefly to catch startup errors.
- **Description line that corrects a model mistake:** > "Pagination: Always disable terminal pagination to ensure commands terminate (e.g., use `git --no-pager` ...)". **Mistake:** running `git log`/`git diff` opens a pager that waits for keyboard input forever, so the tool call hangs. The agent followed it: its last call was `git --no-pager status` `[OBSERVED]` (13:15:36). (I hit this exact problem myself when I ran `git grep` without `--no-pager` and got stuck in the pager.)
- **Deliberately does not:** run outside the workspace or run empty commands. `shell.ts` L1220–1233 returns "Command cannot be empty." and checks `dir_path` with `validatePathAccess`. It also does not keep a stuck command alive forever: an inactivity timeout cancels it (L554–L652, L876–882 "Command was automatically cancelled because it exceeded the timeout"). Why: the shell is the most powerful tool, so the CLI limits where it runs and puts a human confirmation in front of it.

### Why old/new string edits?
1. **Robust to stale positions.** Line numbers become wrong as soon as an earlier edit adds or removes lines, and the model often can't count lines reliably. An exact text anchor still finds the right place after earlier edits. If the file changed under it, the tool fails loudly ("Could not find an exact match ... please use ReadFile to inspect the target lines before retrying", edit.ts L366–370) instead of editing the wrong line.
2. **Cheap and safe compared to rewriting the whole file.** The `replace` description itself says it "minimizes token usage, simplifies code reviews, and avoids accidental deletions": the model only outputs the changed snippet, and the user reviews a small diff instead of a whole file in which the model might have dropped or "summarized" code.

**Trace moment:** It mattered in `pricing.py`. One `replace` (call #6, 429 output tokens, 13:14:33) inserted the shipping constants and `shipping_fee()` and rewrote `final_total` in the middle of the file, while the untouched code above and below (`apply_discount`, `apply_tax`) stayed byte-for-byte the same `[OBSERVED]` (session commit diff, `pricing.py` hunks @@ -27 and @@ -34). No edit failed in my session (0 failed tool calls), so the "fail loudly" path never came up; the agent had read every file in full right before editing, so its anchors were current `[INFERRED]` from the read at 13:14:11 followed by the edits from 13:14:25 on.

### Per-model tool descriptions
Tool compared: `replace` in `gemini-3.ts` (L356) vs `default-legacy.ts` (L349).
- **What differs:** the legacy description is much longer and prescriptive. It adds "Always use the read_file tool to examine the file's current content before attempting a text replacement", a numbered list of requirements, "Include at least 3 lines of context BEFORE and AFTER the target text", "Prefer to break down complex and long changes into multiple smaller atomic calls", and a long `instruction` parameter guide with GOOD/BAD examples. The Gemini 3 version keeps the schema identical but drops these rules, adding instead one line of rationale ("preferred for surgical edits ... minimizes token usage, simplifies code reviews, and avoids accidental deletions") and a shorter `instruction` description. The version actually sent in my session is the Gemini 3 one `[OBSERVED]` (`session_tools.md` matches `gemini-3.ts`, not legacy).
- **Why:** older models needed step-by-step guardrails to make good edits (read first, enough context, small edits), and every rule spent tokens in every request. Newer models follow intent better, so the CLI explains *why* and trusts the model with *how*, which keeps the tool list shorter on every call `[INFERRED]`. Some rules moved into the system prompt instead (e.g. "replace fails if old_string is ambiguous ... read enough", L27) `[OBSERVED]`.

---

## Part IV — Behavioral analysis

### 1. The loop
`[OBSERVED]` from `session_timeline.txt`:
```
user prompt
→ call#1  → update_topic("Reading Task and Planning") + read_file(TASK.md)
→ call#2  → run_shell_command(pytest -q)               # reproduce failures
→ call#3  → update_topic + read_file ×5 (cart, catalog, pricing, test_cart, test_pricing)
→ call#4  → update_topic("Implementing bug fixes ...")  # 2,656 thought tokens
→ call#5  → replace(shopcart/cart.py)                   # add_item increments quantity
→ call#6  → replace(shopcart/pricing.py)                # discount before tax + shipping_fee
→ call#7  → run_shell_command(pytest -q)
→ call#8  → update_topic("Updating existing test assertions for Cart.total ...")
→ call#9  → replace(tests/test_cart.py)                 # update 3 totals + 3 new tests
→ call#10 → replace(tests/test_pricing.py)              # import + test_shipping_fee_rules
→ call#11 → run_shell_command(full pytest, verbose)
→ call#12 → update_topic("Task Completed")
→ call#13 → run_shell_command(git --no-pager status)
→ call#14 → final text summary (no tool call)
```
**What ended it:** the agent decided it was done. Call #14 returned text only (no tool call), which ends the loop; I then typed `/quit`. No limit was hit (0 errors, 14 calls).

### 2. Context growth
`input_token_count` per call (`submission/session_calls.csv`) `[OBSERVED]`:

| Call | Input tokens | Cached tokens | Cached share | Thoughts |
|---:|---:|---:|---:|---:|
| 1 | 11,379 | 6,093 | 54% | 163 |
| 2 | 11,902 | 8,115 | 68% | 172 |
| 3 | 12,630 | 10,142 | 80% | 85 |
| 4 | 14,520 | 12,144 | 84% | 2,656 |
| 5 | 17,293 | 14,186 | 82% | 156 |
| 6 | 18,053 | 14,185 | 79% | 737 |
| 7 | 19,793 | 16,218 | 82% | 35 |
| 8 | 20,573 | 18,244 | 89% | 1,109 |
| 9 | 21,789 | 18,246 | 84% | 17 |
| 10 | 23,416 | 20,279 | 87% | 241 |
| 11 | 24,475 | 22,307 | 91% | 72 |
| 12 | 25,260 | 22,305 | 88% | 49 |
| 13 | 25,390 | 22,297 | 88% | 46 |
| 14 | 25,665 | 22,291 | 87% | 154 |

```
input tokens (each █ ≈ 1,000)
#1  ███████████            11,379
#4  ██████████████         14,520
#5  █████████████████      17,293   ← after 5 file reads
#8  ████████████████████   20,573   ← after test output
#11 ████████████████████████ 24,475
#14 █████████████████████████ 25,665
```

**Why it grows:** the CLI re-sends the whole conversation on every call: system prompt and tool
declarations, the first context message, every previous model turn, and every tool result.
The biggest jumps come right after large tool results: +1,890 after reading five files
(#4 → #5) and the steady growth after each `pytest` output and edit `[OBSERVED]`. Input never
shrinks because nothing is dropped in a short session `[INFERRED]`. Even call #1 is already
11,379 tokens: that's the fixed cost of the system prompt (~240 lines), 16 tool schemas, the
directory tree, and `GEMINI.md`, before any work `[INFERRED]` from the size of those files.

**Caching:** `cached_content_token_count` is the part of the input the API had already seen in
an earlier call (the unchanged prefix of the conversation), so it was served from cache. It
rises from 54% to about 87–91% `[OBSERVED]`; over the session 227,052 of 272,138 input tokens
(≈ 83%) were cache reads (exit summary). That matters because cached tokens are billed at a
much lower rate and skip re-processing, so each additional turn costs and waits mostly for the
new part only. Without caching the cost of a session grows roughly with the square of the
number of turns, since every turn re-sends everything `[INFERRED]` from the input growth above.

### 3. Planning
The agent planned and tracked progress with **`update_topic`**, not `write_todos` (which wasn't
even in its tool list) and not plan mode `[OBSERVED]` (`session_tools.md`; 0 `enter_plan_mode`
calls). This matches the system prompt's "Topic Updates" section ("Always call update_topic in
your first turn", "call update_topic in your last turn to recap"). It also matches the
Development Lifecycle rule "Do NOT use Plan Mode for straightforward bug fixes" (L137). Its five
topics were: "Reading Task and Planning" (#1) → inspecting the codebase (#3) → "Implementing
bug fixes for add_item quantity ..." (#4) → "Updating existing test assertions for
Cart.total ..." (#8) → "Task Completed" (#12) `[OBSERVED]`.

**Where it departed from the plan:** the topic opened at call #4 was about the *bug fixes*, and
the shipping feature should have been a separate phase (TASK.md step 2). But the single
`replace` on `pricing.py` (call #6) also added `SHIPPING_FEE_CENTS`, `shipping_fee()` and the
shipping term in `final_total` `[OBSERVED]` (timeline 13:14:33: `new_string` starts with
`SHIPPING_FEE_CENTS = 599`), without a topic update for "adding shipping". Also, it never opened
a topic for the existing-test breakage before it happened; the "Updating existing test
assertions" topic at #8 was a reaction to the test run at #7, i.e. an unplanned detour
`[INFERRED]` from its timing (right after `pytest`) and the system prompt rule to call
`update_topic` "when you experience an unexpected event (e.g., a test failure ...)".

### 4. Error recovery
No tool call failed (19/19 ok), so the first failure is a **failing test run**: the first
`pytest` at 13:14:08 (call #2), which reproduced the two starter failures. I saw the same
output myself before the session:
> `FAILED tests/test_cart.py::test_add_same_item_twice_increments_quantity - AssertionError: assert {'MUG': 2} == {'MUG': 3}`
> `FAILED tests/test_cart.py::test_fixed_discount_applied_before_tax - assert 1160 == 3240`

**What it did next:** it read all relevant files in one turn (#3), reasoned for 2,656 thought
tokens (#4), and fixed the root causes in the code, not in the tests: `add_item` now adds to the
existing quantity (`self.items[sku] = self.items.get(sku, 0) + quantity`) and `final_total`
now applies the discount before tax `[OBSERVED]` (session diff, `cart.py` @@ -14 and
`pricing.py` @@ -34).

A second failure came after the edits: the `pytest` run at 13:14:47 (call #7) was followed by
the topic "Updating existing test assertions for Cart.total" and 1,109 thought tokens (#8), so
the older total tests must have failed once shipping was added `[INFERRED]` (the test output
text isn't in the timeline, but these three old expected values were exactly the ones it then
changed). It updated only those values, added comments explaining the shipping fee, and the
final run passed.

**Was the recovery good?** Yes. It reproduced before fixing, fixed the code rather than
weakening the tests, and verified with a full run. One small gap: the system prompt says that
for bug fixes it "must empirically reproduce the failure with a new test case" (L46); it relied
on the existing failing tests instead of adding a new reproduction test, which was reasonable
here because the starter tests already reproduced both bugs.

### 5. The tests
Yes, the agent edited existing tests: three expected values in `tests/test_cart.py` `[OBSERVED]`
(session commit diff):
```diff
 def test_total_includes_tax():
-    assert cart.total() == 2160  # 2000 + 8% tax
+    assert cart.total() == 2759  # 2000 + 8% tax + $5.99 shipping

 def test_percent_discount():
-    assert cart.total() == 2333  # (2400 - 10%) + 8% tax
+    assert cart.total() == 2932  # (2400 - 10%) + 8% tax + $5.99 shipping

 def test_fixed_discount_applied_before_tax():
-    assert cart.total() == 3240  # (4000 - 1000) + 8% tax
+    assert cart.total() == 3839  # (4000 - 1000) + 8% tax + $5.99 shipping
```
**Allowed by TASK.md?** Yes. TASK.md step 1 forbids editing tests to make the bug fixes pass,
and the agent didn't: it fixed `cart.py` and `pricing.py`. Step 2 says "Some existing tests
check `Cart.total()` with values from before shipping existed. You may update those expected
values — and only those — and note why in a comment." All three edits are `Cart.total()`
checks for orders under $50 that now pay $5.99 shipping, each with a comment naming the
shipping fee. Checking the math: 2160 + 599 = 2759, 2333 + 599 = 2932, 3240 + 599 = 3839. Note
that 3240 was already the *correct* pre-shipping value of a test that failed because of the
discount bug; after the code fix it would have passed, and only shipping changed it. Every
other edit to test files only **added** tests (3 in `test_cart.py`, `test_shipping_fee_rules`
in `test_pricing.py`, plus the `shipping_fee` import) `[OBSERVED]`.

### 6. Models
**Confirmed:** every call in the trace has `model=gemini-3.5-flash-lite` (14/14), and the exit
summary lists only that model `[OBSERVED]` (`session_timeline.txt` summary "gemini-3.5-flash-lite
x14").

**Most "thinking"** (`thoughts_token_count`) `[OBSERVED]`:
- **Call #4 — 2,656 tokens.** Right after reading all five files. It was deciding the whole fix: what the two bugs were and how to add shipping. The next topic was "Implementing bug fixes for add_item quantity ..." `[INFERRED]` from the topic that followed.
- **Call #8 — 1,109 tokens.** Right after the second `pytest` run. It was deciding how to handle the broken pre-shipping totals and whether TASK.md allowed changing them, then opened "Updating existing test assertions for Cart.total" `[INFERRED]`.
- **Call #6 — 737 tokens.** Writing the `pricing.py` edit: the order of discount, tax and shipping and the free-shipping threshold (≥ 5000 cents, after discount, before tax).

Routine calls (e.g. #7 and #9, 35 and 17 thought tokens) barely thought at all: the decision
was already made and the model was just emitting a tool call `[OBSERVED]`.

**Why split routing and work across two models?** Many requests are simple (a greeting, a quick
lookup, "run the tests"), so a cheap, fast model like flash-lite can classify each request and
handle the easy ones, while the bigger `gemini-3.8-flash` is used for the hard reasoning. That
keeps the common case fast and cheap and saves the big model's quota (only 20 free requests
per day) for the turns that need it `[INFERRED]` (lecture's model landscape: cost/latency vs.
capability trade-off).

**If the whole session ran on a bigger model** I'd expect: **slower** calls (my calls took
1.1–6.8 s, `ms` column), **higher cost** per token (and on the free tier, the 20-request daily
quota would run out, since this session alone used 14 requests), and **better quality** mainly
on the hard calls like #4 and #8 — e.g. maybe noticing the "add a new reproduction test" rule,
or separating the shipping work into its own phase. For a small, well-specified task like this
one, flash-lite was already enough: 18/18 tests passed with 0 failed tool calls `[INFERRED]`.
