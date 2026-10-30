# Week 3 Writeup — Prompting Techniques

**Model:** `llama3.1:8b` via local Ollama
**Run date:** 2026-10-29

All four scripts were run against the local model. The observed checks passed: K-shot
classification **4/4**, refund decisions **3/3**, tool-call argument **passed**, and RAG
answers **3/3**.

## 1. K-shot classification

**Final prompt:**

```text
You are a support-ticket classifier. Classify each customer message using the examples
below. Reply with exactly one lowercase label and nothing else: billing, shipping,
returns, technical, or other.

Examples:
Message: My card was charged twice for order 4412.
Label: billing

Message: Where is my package? It has been two weeks.
Label: shipping

Message: I want to send the shoes back for a refund.
Label: returns

Message: The app crashes every time I open my cart.
Label: technical

Message: Can I speak with a person about a question?
Label: other
```

**Sample input:** `My card was charged twice for order 4412.`

**Observed output:** `billing`

**What I learned:** Labeled examples show the model how to map natural-language
complaints to a fixed vocabulary and output shape.

## 2. Refund eligibility

**Final prompt** (the policy is appended to this system prompt by the script):

```text
Evaluate the order against every rule in the supplied refund policy. Briefly state the
policy facts that determine eligibility, then put exactly one final line in this
format: DECISION: YES or DECISION: NO. A final-sale item is never eligible, even if the
purchase is recent. Do not add text after the decision.
```

**Sample input:** `Bought 45 days ago, unused.`

**Observed sample input/output:** For `Bought 45 days ago, unused.`, the check returned
`NO`. The script extracts the final decision marker from the model response; the
displayed result is the normalized grading value.

**What I learned:** Explicitly enumerating policy criteria and constraining the final
line makes the decision easier to inspect and grade.

## 3. Order lookup tool

**Final prompt:**

```text
You are a support assistant. For an order-status question, you must call
get_order_status with the exact order ID from the customer's message before answering.
Do not guess or invent status information. Use the tool result to answer briefly; if
the order is not found, say so.
```

**Sample input:** `Hi, can you check on order 4412 for me?`

**Observed check output:** `[PASS] tool called with order_id='4412'`

The script then printed the local fixture result: `shipped, arriving Friday`. The
starter's built-in check does not send that result back to the model for a second reply;
it only verifies the tool call and prints the function result.

**What I learned:** Tool descriptions and required arguments give the model a structured
way to request current order data instead of inventing an answer.

## 4. Retrieval-augmented answer

**Final prompt:**

```text
Answer the customer's question using only the supplied help center context. Do not use
outside knowledge or infer details that are not stated. If the context does not contain
the answer, politely say you don't know based on the available information. Keep the
answer concise.
```

The retriever in `rag.py` selects help-center lines with question-term overlap.

**Sample input:** `How long do I have to return an item?`

**Observed output:** `you have 30 days from delivery to return an item.`

**What I learned:** Retrieval supplies relevant evidence, while an explicit abstention
rule constrains answers when no relevant fact is present.

## Closing reflection

Structured tasks become more reliable when the prompt narrows the task, supplies
examples or authoritative context, and defines a predictable answer format. In these
checks, examples guided classification, an explicit policy led to the expected refund
decisions, the order ID was passed to the lookup tool, and retrieval supported grounded
answers and an abstention. Scaffolding remains important: these checks cover only a few
cases, and the tool starter verifies the call and fixture result rather than testing a
second model response after the tool runs.
