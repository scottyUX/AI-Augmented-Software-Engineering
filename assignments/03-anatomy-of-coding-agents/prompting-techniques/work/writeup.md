# Week 3 — Prompting Techniques: Writeup

Model: `llama3.1:8b` via Ollama, `temperature=0.0`, CPU only (GitHub Codespaces, 4 cores).
Every check passes: **k-shot 4/4, CoT 3/3, tool calling PASS, RAG 3/3**.

To see what each prompt actually changes, I also re-ran every file with an **empty prompt**
(`YOUR_SYSTEM_PROMPT = ""`, plus empty tool descriptions for tool calling). Full outputs are in
[`results.txt`](results.txt) and [`baseline.txt`](baseline.txt).

| Technique | Empty prompt | Final prompt |
|---|---|---|
| k-shot classification | 0/4 | **4/4** |
| chain-of-thought | 0/3 | **3/3** |
| tool calling | PASS | **PASS** |
| RAG | 2/3 | **3/3** |

## 1. K-shot prompting — ticket classification

**Final prompt:** a label list with a one-line definition for each label, a strict "one
lowercase word, no explanation" output rule, and 9 labeled `Message:` / `Label:` examples
(at least two per class). See `k_shot_prompting.py`.

**Sample:**
```
[PASS] 'My card was charged twice for order 4412.' -> got 'billing', expected 'billing'
[PASS] 'The app crashes every time I open my cart.' -> got 'technical', expected 'technical'
4/4 correct
```
**What I learned:** With an empty prompt the model *acted as the support agent*. It wrote a
paragraph of help ("i'm so sorry to hear that your card was charged twice…") instead of a
label, so 0/4. The examples fixed the **task and the output format** more than the
classification itself.

## 2. Chain-of-thought — refund eligibility

**Final prompt:** one line per policy rule in a fixed order (days → condition → final sale),
each marked PASS/FAIL. It also states that any FAIL means NO, sets defaults for missing
information ("not mentioned" = unused / not final sale), includes one worked example, and
requires the last line to be exactly `DECISION: YES` or `DECISION: NO`.

**Sample:**
```
[PASS] 'Bought 10 days ago, unused, not final sale.' -> YES, expected YES
[PASS] 'Bought 45 days ago, unused.' -> NO, expected NO
[PASS] 'Bought 5 days ago but it was a final-sale item.' -> NO, expected NO
3/3 correct
```
**What I learned:** With an empty prompt every answer parsed as `?`. The model never ended
on a `DECISION:` line, so even when its reasoning was right it couldn't be graded.
Step-by-step reasoning only helps when it ends in a format code can rely on.

## 3. Tool calling — order lookup

**Final prompt and schema:** the tool description says *when* to call it ("whenever the user
asks about an order and gives an order number") and forbids guessing. The `order_id`
description pins the format (digits only, example `"4412"`). The system prompt says the
assistant can't see order data and MUST call the tool first.

**Sample:**
```
[PASS] tool called with order_id='4412'
tool result: shipped, arriving Friday
```
**What I learned:** This one passed even with an empty prompt and empty descriptions.
llama3.1 is trained for function calling, and "check on order 4412" plus a tool named
`get_order_status` is an obvious match. The descriptions matter for ambiguous cases (several
tools, a missing id, ids written as `#4412`), which this single check doesn't test.

## 4. RAG — grounded answers

**Retriever:** keyword overlap. It lowercases and tokenizes, drops stopwords, maps question
words to the help center's vocabulary (`ship → shipping`, `internationally → international`,
`refund → returns`), does crude singularization, and keeps the top 3 lines with a score above
0. The CEO question retrieves **nothing**.

**Final prompt:** answer only from the context, reuse the context's wording for key facts,
and reply with a fixed sentence (*"I'm sorry, I don't know the answer to that based on our
help center."*) when the context doesn't contain the answer.

**Sample:**
```
[PASS] 'How long do I have to return an item?' -> 'you may return most items within 30 days of delivery for a full refund.'
[PASS] 'Do you ship internationally?' -> 'yes, we offer international shipping to most countries.'
[PASS] "What's your CEO's home address?" -> "i'm sorry, i don't know the answer to that based on our help center."
```
**What I learned:** With an empty prompt the model still answered the two policy questions
from the retrieved text. It even refused the CEO question, but in its own words
("i can't provide that information"), which the check doesn't recognize. The prompt's
job was to make the refusal **predictable**. I also tried giving it *all* chunks
instead of my retriever, and it still passed 3/3. On a 7-line help center the prompt does
the grounding, so retrieval would matter more with a large knowledge base.

## Closing — why LLMs are good at structured tasks, and where they need scaffolding

LLMs are strong at structured tasks because they have seen huge amounts of text that already
follows patterns: labels, step lists, JSON, Q&A, function calls. A few examples or a clear
schema is usually enough for them to copy the pattern, and tool calling worked with no
prompt at all. Without scaffolding, though, an instruction-tuned model falls back to its
default role, a chatty helpful assistant. That gave 0/4 and 0/3 in my baselines even where
the underlying judgment was fine. The scaffolding they need is mostly about **contracts**:
exact output formats, an explicit rule order for multi-condition logic, defaults for missing
information, and a fixed way to say "I don't know". Facts the model can't have, such as order
status or store policy, must come from a tool or retrieved context, together with a rule not
to guess.
