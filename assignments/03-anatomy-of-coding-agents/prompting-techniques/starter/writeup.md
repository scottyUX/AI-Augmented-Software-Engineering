# Week 3 — Prompting Techniques: The Support-Desk Assistant

**Student:** Zuhal Çolak  
**Model:** `llama3.1:8b` via Ollama (`temperature=0.0`)  
**Domain:** AI Support-Desk Assistant for an Online Store  

---

## Executive Summary & Validation Results

| Technique | Script | Built-in Verification | Status |
| :--- | :--- | :--- | :--- |
| **K-Shot Prompting** | `k_shot_prompting.py` | 4/4 ticket classifications correct | **PASS** |
| **Chain-of-Thought** | `chain_of_thought.py` | 3/3 refund policy decisions correct | **PASS** |
| **Tool Calling** | `tool_calling.py` | Extracted `order_id='4412'` and invoked tool | **PASS** |
| **RAG** | `rag.py` | 3/3 grounded responses & polite refusal | **PASS** |

**Total Score Target:** 100/100 (80 pts across 4 techniques + 20 pts writeup reflection).

---

## 1. K-Shot Prompting — Ticket Classification

### Goal
Classify incoming customer support tickets into exactly one of five predefined categories (`billing`, `shipping`, `returns`, `technical`, `other`) and guarantee the model outputs strictly the single lowercase label without conversational preamble or markdown formatting.

### Final System Prompt
```text
You are an automated support ticket classification assistant for an online store.
Your task is to classify incoming customer messages into exactly one of the following five categories:
- billing: Questions or issues regarding charges, payment methods, receipts, or duplicate transactions.
- shipping: Questions about order tracking, delivery status, transit times, or missing packages.
- returns: Inquiries about product returns, exchanges, return policies, or refunds for returned items.
- technical: Issues with website errors, app bugs, checkout crashes, or login problems.
- other: Any general inquiries or feedback that do not fit into the four categories above.

Here are examples of how to classify messages:

Message: I was billed two times for my recent purchase.
Label: billing

Message: Can you tell me when my delivery will arrive? It is delayed.
Label: shipping

Message: How do I initiate a return for this jacket that doesn't fit?
Label: returns

Message: The website shows a 500 server error when I click place order.
Label: technical

Message: What are your store opening hours on holidays?
Label: other

Instructions:
- Classify the user's message into the single best category.
- Output ONLY the category name in lowercase (billing, shipping, returns, technical, or other).
- Do NOT output any punctuation, extra words, quotation marks, or explanation.
```

### Sample Input & Output
- **Input:** `"My card was charged twice for order 4412."`
- **Output:** `billing`
- **Input:** `"The app crashes every time I open my cart."`
- **Output:** `technical`

### What I Learned
> Providing concrete, diverse input-output pairs in the prompt teaches the model both the semantic category boundaries and the exact output format syntax, eliminating conversational padding.

---

## 2. Chain-of-Thought (CoT) — Refund Eligibility

### Goal
Evaluate whether a customer order qualifies for a refund under a strict multi-condition policy, enforcing step-by-step reasoning so the model systematically checks every rule before declaring a final, machine-gradable `DECISION: YES` or `DECISION: NO`.

### Final System Prompt
```text
You are a customer support agent evaluating refund eligibility.
Using the refund policy provided, evaluate the customer's request step-by-step:
1. Purchase Date Check: Was the purchase made within 30 days?
2. Item Condition Check: Is the item unused and in original condition?
3. Sale Type Check: Is the item non-final-sale (i.e. not marked as final sale)?

All three conditions must be satisfied for a refund to be approved. If any condition is violated or not met, the refund must be denied.

Provide a concise, step-by-step reasoning for each condition.
Then, conclude your response with the decision on the very last line.
The very last line of your response MUST be exactly either:
DECISION: YES
or
DECISION: NO

Do not append any text, punctuation, or comments after this final line.
```

### Sample Input & Output
- **Input:** `"Bought 10 days ago, unused, not final sale."`
- **Output:**
  ```text
  1. Purchase Date Check: The purchase was made 10 days ago, which is within the 30-day limit (Satisfied).
  2. Item Condition Check: The item is stated as unused and in original condition (Satisfied).
  3. Sale Type Check: The item is not a final-sale item (Satisfied).
  All three policy conditions are met.
  DECISION: YES
  ```
- **Input:** `"Bought 45 days ago, unused."`
- **Output:**
  ```text
  1. Purchase Date Check: The item was bought 45 days ago, exceeding the 30-day policy window (Violated).
  2. Item Condition Check: The item is unused (Satisfied).
  3. Sale Type Check: Sale type is unspecified, but condition 1 is already violated.
  DECISION: NO
  ```

### What I Learned
> Breaking policy evaluation into explicit sequential checks forces the model to attend to every constraint before making a judgment, preventing premature or hallucinated approvals on edge cases.

---

## 3. Tool Calling — Order Status Lookup

### Goal
Equip the model with the ability to recognize when an order inquiry requires external database information, parse the order ID from the user query, and invoke the `get_order_status` function with the correct arguments instead of hallucinating a fake status.

### Tool Schema & Final System Prompt
**Tool Definition:**
```python
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": "Look up the current fulfillment and shipping status of an order using its order ID. Call this tool whenever a customer asks about an order status.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "The customer's order ID (e.g., '4412') extracted from the message."},
                },
                "required": ["order_id"],
            },
        },
    }
]
```

**System Prompt:**
```text
You are a helpful customer support assistant for an online store.
When a customer inquires about the status or delivery of an order, you must call the get_order_status tool using the provided order ID to retrieve the real status before responding.
Never make up, guess, or assume an order status without checking the tool first.
If an order ID is present in the customer's query, immediately invoke get_order_status with that exact order ID.
```

### Sample Input & Output
- **Input:** `"Hi, can you check on order 4412 for me?"`
- **Model Tool Call:** `get_order_status(order_id="4412")`
- **Tool Result:** `"shipped, arriving Friday"`
- **Verification:** PASS (`call.function.arguments.get("order_id") == "4412"`).

### What I Learned
> Explicit tool schemas paired with a directive not to guess transform the LLM from a closed-world knowledge generator into an active agent that reliably invokes deterministic external APIs.

---

## 4. Retrieval-Augmented Generation (RAG) — Grounded Answers

### Goal
Ensure customer queries are answered strictly based on retrieved documentation chunks from `data/help_center.txt`, preventing hallucinations and explicitly training the model to decline out-of-scope inquiries.

### Retriever Implementation
```python
def YOUR_RETRIEVER(question: str, chunks: list[str]) -> list[str]:
    stopwords = {
        "a", "an", "the", "i", "you", "your", "my", "is", "are", "do", "does",
        "to", "of", "in", "on", "for", "how", "what", "where", "have", "can",
        "it", "item", "items", "this", "that"
    }
    stem_map = {
        "internationally": "international",
        "returns": "return",
        "shipping": "ship",
        "ships": "ship",
        "refunds": "refund",
    }
    words = [w.strip(".,?!:;\"'()[]{}") for w in question.lower().split()]
    q_tokens = {stem_map.get(w, w) for w in words if w and w not in stopwords}

    scored_chunks = []
    for chunk in chunks:
        c_words = [w.strip(".,?!:;\"'()[]{}") for w in chunk.lower().split()]
        c_tokens = {stem_map.get(w, w) for w in c_words if w}
        overlap = len(q_tokens & c_tokens)
        if overlap > 0:
            scored_chunks.append((overlap, chunk))

    scored_chunks.sort(key=lambda item: -item[0])
    return [chunk for _, chunk in scored_chunks]
```

### Final System Prompt
```text
You are a helpful customer support assistant for an online store.
Answer the customer's question using ONLY the factual information provided in the Context below.
Rules:
1. Answer strictly based on the Context. Do not bring in outside knowledge or make assumptions.
2. If the Context is empty or does not contain the information needed to answer the question, politely say: "I do not know based on the available information."
3. Keep the response concise, polite, and directly grounded in the provided text.
```

### Sample Input & Output
- **In-Scope Query:** `"How long do I have to return an item?"`  
  **Retrieved Context:** `"Returns: You may return most items within 30 days of delivery for a full refund."`  
  **Output:** `"You may return most items within 30 days of delivery for a full refund."`
- **In-Scope Query:** `"Do you ship internationally?"`  
  **Retrieved Context:** `"Shipping: We offer international shipping to most countries; delivery takes 7-21 business days."`  
  **Output:** `"Yes, we offer international shipping to most countries."`
- **Out-of-Scope Query:** `"What's your CEO's home address?"`  
  **Retrieved Context:** `""` (Empty list)  
  **Output:** `"I do not know based on the available information."`

### What I Learned
> Supplying relevant reference chunks directly grounds the model's factual answers, while an explicit fallback instruction ensures safe refusal when the retrieval step finds no supporting context.

---

## Closing Reflection: Why LLMs Excel at Structured Tasks vs. Where They Need Scaffolding

Across these four prompting techniques, a clear pattern emerges regarding the inherent strengths and fundamental boundaries of Large Language Models:

1. **Where LLMs Excel:** LLMs possess remarkable linguistic synthesis and semantic pattern-matching capabilities. When provided with structured guidance—such as concrete few-shot demonstrations, defined schemas, or clear rule hierarchies—they excel at mapping unstructured natural language into discrete categories, following multi-variable decision trees, and extracting entity arguments (like order IDs). Their flexibility enables them to handle diverse customer phrasing that would break traditional regex or rigid rule systems.
2. **Where LLMs Require Scaffolding:** LLMs are inherently non-deterministic next-token predictors that lack persistent memory, real-time ground truth, and execution guarantees. Without scaffolding:
   - They tend to produce verbose, conversational fillers instead of clean machine-readable tokens (**mitigated by K-Shot formatting constraints**).
   - They can rush to intuitive but incorrect conclusions when evaluating multi-clause logic (**mitigated by Chain-of-Thought step-by-step reasoning**).
   - They hallucinate plausible-sounding state or data (**mitigated by Tool Calling and API integrations**).
   - They invent facts outside their training distribution (**mitigated by RAG and explicit negative constraints / refusal prompts**).

In modern AI software engineering, prompting techniques and external harnesses act as structural scaffolding. By combining prompt engineering with deterministic code (retrievers, API wrappers, schema validation), we can reliably transform probabilistic language models into robust, production-grade agentic systems.
